#!/bin/bash

# Check if the service exists
service_exists() {
    local service_name="$1"
    if systemctl list-unit-files --all --type=service | grep -q "^.*$service_name.*"; then
        echo "Service '$service_name' exists."
        return 0
    else
        echo "Service '$service_name' does not exist."
        return 1
    fi
}

# checks if there's a parameter for the service name
if [ -z "$1" ]; then
    echo "Usage: $0 <service-name>"
    exit 1
fi

service_exists "$1"