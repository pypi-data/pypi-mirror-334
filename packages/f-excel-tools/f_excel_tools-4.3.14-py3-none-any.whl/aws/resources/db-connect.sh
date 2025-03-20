#!/bin/bash

# Note: this script is a demo only file that retrieves a secret key and value from a secret whom name is set in the environment
# it installs pip3, pgcli, and aws-cli if needed, then connects to a database whose address is specified as an environment variable.

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
                xz-devel libpq-devel python3 postgresql-devel
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

# Function to install aws-cli if not installed
install_aws_cli() {
    if ! command -v aws &> /dev/null; then
        echo "aws-cli not found. Installing aws-cli..."
        dnf install -y aws-cli || {
            echo "Failed to install aws-cli"; exit 1;
        }
    else
        echo "aws-cli is already installed."
    fi
}

# Fetch secret using AWS CLI
fetch_secret() {
    SECRET_NAME=${SECRET_NAME}
    AWS_REGION=${AWS_REGION}

    # Fetch secret values directly using AWS CLI query arguments
    USER=$(aws secretsmanager get-secret-value --secret-id "$SECRET_NAME" --region "$AWS_REGION" --query SecretString --output text 2>/dev/null | grep -o '"id":"[^"]*"' | cut -d':' -f2 | tr -d '"')
    PASSWORD=$(aws secretsmanager get-secret-value --secret-id "$SECRET_NAME" --region "$AWS_REGION" --query SecretString --output text 2>/dev/null | grep -o '"password":"[^"]*"' | cut -d':' -f2 | tr -d '"')

    # Check if extraction was successful
    if [ -z "$USER" ] || [ -z "$PASSWORD" ]; then
        echo "Error fetching or parsing secret" >&2
        exit 1
    fi

    # Export the variables
    export USER
    export PASSWORD

    # Print the exports (optional, for debugging)
    echo "USER and PASSWORD have been exported."
}

install_aws_cli
install_pgcli
fetch_secret
pgcli "postgres://$USER:$PASSWORD@$DB_HOST_NAME:5432/$DB_NAME?sslmode=require"
