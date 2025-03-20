import boto3
import json
import sys
import subprocess
import os
import inquirer
import importlib.resources

# Dynamically get the script filename (without extension)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]

# Define the folder where the scripts are located (mount folder in the current module directory)
AWS_DIR = importlib.resources.files('aws')
CONFIG_FILE = AWS_DIR / f"{SCRIPT_NAME}_config.json"

# Access resources correctly using importlib.resources for directory access
RESOURCES_DIR = importlib.resources.files('aws.resources')

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def get_user_input(prompt, options, default=None):
    questions = [
        inquirer.List(
            prompt,
            message=f"{prompt}:",
            choices=options,
            default=default
        )
    ]
    answer = inquirer.prompt(questions)
    return answer[prompt]

def list_aws_regions():
    ec2_client = boto3.client('ec2')
    regions = ec2_client.describe_regions()
    return [region['RegionName'] for region in regions['Regions']]

def list_ecs_clusters(region):
    ecs_client = boto3.client('ecs', region_name=region)
    response = ecs_client.list_clusters()
    cluster_arns = response.get('clusterArns', [])
    return [arn.split('/')[-1] for arn in cluster_arns]

def list_ecs_services(region, cluster):
    ecs_client = boto3.client('ecs', region_name=region)
    response = ecs_client.list_services(cluster=cluster)
    service_arns = response.get('serviceArns', [])
    return [arn.split('/')[-1] for arn in service_arns]

def list_ecs_containers(ecs_client, cluster, task_arn):
    response = ecs_client.describe_tasks(
        cluster=cluster,
        tasks=[task_arn]
    )
    containers = response['tasks'][0]['containers']
    return [container['name'] for container in containers]

def get_first_task_arn(ecs_client, cluster, service_name):
    response = ecs_client.list_tasks(
        cluster=cluster,
        serviceName=service_name
    )
    task_arns = response.get('taskArns', [])
    if not task_arns:
        print(f"Error: No tasks found for service {service_name} in cluster {cluster}.")
        sys.exit(1)
    return task_arns[0]

def get_task_role_arn(ecs_client, cluster, task_arn):
    response = ecs_client.describe_tasks(
        cluster=cluster,
        tasks=[task_arn]
    )
    task_definition_arn = response['tasks'][0]['taskDefinitionArn']
    response = ecs_client.describe_task_definition(
        taskDefinition=task_definition_arn
    )
    return response['taskDefinition'].get('taskRoleArn', None)

def add_permissions_to_role(iam_client, role_name):
    policy_name = "ecs-ssm-exec"
    try:
        existing_policy = iam_client.get_role_policy(
            RoleName=role_name,
            PolicyName=policy_name
        )['PolicyDocument']
    except iam_client.exceptions.NoSuchEntityException:
        existing_policy = {}

    required_permissions = [
        "ssmmessages:CreateControlChannel",
        "ssmmessages:CreateDataChannel",
        "ssmmessages:OpenControlChannel",
        "ssmmessages:OpenDataChannel"
    ]

    if "ssmmessages:CreateControlChannel" in json.dumps(existing_policy):
        print("Required permissions already exist in the task role policy.")
    else:
        print("Adding required permissions to the task role.")
        new_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": required_permissions,
                    "Resource": "*"
                }
            ]
        }
        iam_client.put_role_policy(
            RoleName=role_name,
            PolicyName=policy_name,
            PolicyDocument=json.dumps(new_policy)
        )

def check_enable_execute_command(ecs_client, cluster, service_name):
    response = ecs_client.describe_services(
        cluster=cluster,
        services=[service_name]
    )
    services = response.get('services', [])
    if not services:
        print(f"Error: No service found with name {service_name} in cluster {cluster}.")
        sys.exit(1)
    service = services[0]
    return service.get('enableExecuteCommand', False)

def update_service(ecs_client, cluster, service_name):
    response = ecs_client.update_service(
        cluster=cluster,
        service=service_name,
        enableExecuteCommand=True,
        forceNewDeployment=True
    )
    # Correct way to wait for service stability
    waiter = ecs_client.get_waiter('services_stable')
    waiter.wait(
        cluster=cluster,
        services=[service_name]
    )

def execute_command_on_container(task_name, container_name, region, cluster, RESOURCES_DIR, temp_dir="/tmp"):
    # List all resource files in the provided script directory
    script_files = [entry.name for entry in RESOURCES_DIR.iterdir() if entry.is_file() and not entry.name.endswith('__init__.py')]

    # Prepare the combined command to create and execute each script inside the container
    combined_script = ""

    for script_file in script_files:
        # Read the content of the script file
        with open(RESOURCES_DIR / script_file, "r") as f:
            script_content = f.read()

        # Append the script creation and execution commands to the combined command
        combined_script += f"""cat <<'EOF' > {temp_dir}/{script_file}
{script_content}
EOF
chmod +x /tmp/{script_file}
"""

    # Escape the combined_script to avoid issues with unescaped quotes
    escaped_script = combined_script.replace("'", r"'\''")

    # Run an interactive bash shell after copying the scripts
    subprocess.run([
        "aws", "ecs", "execute-command",
        "--region", region,
        "--cluster", cluster,
        "--task", task_name,
        "--container", container_name,
        "--command", f"/bin/sh -c '{escaped_script}; export PATH={temp_dir}:$PATH; export NODE_PATH=$(pwd)/node_modules; exec /bin/sh'",
        "--interactive"
    ])

def main():
    # Load last used region from the config file
    config = load_config()

    # Get AWS regions
    regions = list_aws_regions()
    region = get_user_input("Select AWS region", regions, default=config.get("region"))

    # Save the selected region for future use
    config["region"] = region
    save_config(config)

    # Initialize boto3 client with selected region
    ecs_client = boto3.client('ecs', region_name=region)
    iam_client = boto3.client('iam', region_name=region)

    # Get ECS clusters
    clusters = list_ecs_clusters(region)
    cluster = get_user_input("Select ECS cluster", clusters, default=config.get("cluster"))

    # Save the selected cluster for future use
    config["cluster"] = cluster
    save_config(config)

    # Get ECS services
    services = list_ecs_services(region, cluster)
    service_name = get_user_input("Select ECS service", services, default=config.get("service"))

    # Save the selected service for future use
    config["service"] = service_name
    save_config(config)

    # Fetch first task ARN
    first_task_arn = get_first_task_arn(ecs_client, cluster, service_name)

    # Get list of containers for the first task
    containers = list_ecs_containers(ecs_client, cluster, first_task_arn)
    container_name = get_user_input("Select ECS container", containers, default=config.get("container"))

    # Save the selected container for future use
    config["container"] = container_name
    save_config(config)

    # Fetch task role ARN
    task_role_arn = get_task_role_arn(ecs_client, cluster, first_task_arn)

    if task_role_arn:
        role_name = task_role_arn.split('/')[-1]
        add_permissions_to_role(iam_client, role_name)
    else:
        print("No task role is associated with the task.")

    # Check if enableExecuteCommand is enabled for the service
    enable_execute_command = check_enable_execute_command(ecs_client, cluster, service_name)

    if enable_execute_command:
        print("Task was launched with enable-execute-command, skipping service update.")
    else:
        # Update ECS service and wait for stabilization
        print("Updating service with enable-execute-command flag.")
        update_service(ecs_client, cluster, service_name)

    # Execute command on selected container
    task_name = first_task_arn.split('/')[-1]
    execute_command_on_container(task_name, container_name, region, cluster, RESOURCES_DIR)

if __name__ == "__main__":
    main()
