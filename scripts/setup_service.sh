#!/bin/bash

# checks the result of the last command and outputs a message accordingly.
# if failed then exiting the script
check_result() {
    if [ $? -eq 0 ]; then
        echo "...Succesful"
    else
        echo "...Failed"
        exit 1
    fi
}

# Check if the service exists
install_service() {
    local service_name="$1"
    if systemctl list-unit-files --all --type=service | grep -q "^.*$service_name.*"; then
        echo "Service '$service_name' already exists."
        return 0
    else
        echo "Service '$service_name' does not exist."

        echo "Updating package lists..."
        sudo apt update -y
        check_result

        echo "Installing '$service_name'..."
        sudo apt install -y $service_name
        check_result

        echo "Enabling '$service_name' to start on boot..."
        sudo systemctl enable $service_name
        check_success

        echo "Starting '$service_name'..."
        sudo systemctl start $service_name
        check_success

        echo "Checking '$service_name' status..."
        sudo systemctl status $service_name --no-pager

        echo "'$service_name' has been installed successfully"
    fi
}

# checks if there's a parameter for the service name
if [ -z "$1" ]; then
    echo "Usage: $0 <service-name>"
    exit 1
fi

install_service "$1"