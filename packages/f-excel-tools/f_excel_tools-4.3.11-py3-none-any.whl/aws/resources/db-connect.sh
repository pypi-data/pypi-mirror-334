#!/bin/bash

# Note: this script is a demo only file that retrieves a secret key and value from a secret whom name is set in the environment
# it installs pip3 and pgcli if needed and connects to a database whom address is specified as env variable

# Set environment variables and initialize
export LD_LIBRARY_PATH=""
export DB_HOST_NAME=${DB_HOST_NAME:-$DATABASE_HOST}
export DB_NAME=${DB_NAME:-$DATABASE_NAME}
export SECRET_NAME=${DB_ACCESS_SECRET:-$DB_ACCESS_SECRET_NAME}
export AWS_REGION=$(echo "$DB_HOST_NAME" | grep -oP '\.\K[a-z]{2}-[a-z]+-\d')

# Function to install pgcli and dependencies
install_pgcli() {
    if ! command -v pgcli &> /dev/null; then
        echo "pgcli not found. Installing dependencies and pgcli..."
        if ! command -v pip3 &> /dev/null; then
            dnf install -y zlib-devel bzip2-devel openssl-devel ncurses-devel \
                sqlite-devel readline-devel tk-devel gdbm-devel libpcap-devel \
                xz-devel libpq-devel python3
            python3 -m ensurepip
        fi
        # Check if --break-system-packages is supported
        if pip3 install --help | grep -q -- '--break-system-packages'; then
            pip3 install --break-system-packages pgcli || {
                echo "Failed to install pgcli with --break-system-packages"; exit 1;
            }
        else
            pip3 install pgcli || {
                echo "Failed to install pgcli"; exit 1;
            }
        fi
    else
        echo "pgcli is already installed."
    fi
}

# Fetch secret using python3
fetch_secret() {
    eval $(python3 - <<EOC
import os
import json
import boto3
import sys

secret_name = os.getenv("SECRET_NAME")
region = os.getenv("AWS_REGION")

client = boto3.client("secretsmanager", region_name=region)

try:
    response = client.get_secret_value(SecretId=secret_name)
    secret = json.loads(response["SecretString"])

    user = secret.get("id")
    password = secret.get("password")

    print(f'export USER="{user}"')
    print(f'export PASSWORD="{password}"')

except Exception as e:
    print(f'echo "Error fetching secret: {e}" >&2', file=sys.stderr)
    sys.exit(1)
EOC
    )
}


install_pgcli
fetch_secret
pgcli "postgres://$USER:$PASSWORD@$DB_HOST_NAME:5432/$DB_NAME?sslmode=require"
