#!/bin/bash

# checks the result of the last command and outputs a message accordingly.
# if failed then exiting the script

log_message() {
    local log_time
    log_time=$(date +"%Y-%m-%d %H:%M:%S,%3N") # Get formatted timestamp
    local log_level="${1}"                   # Log level
    local log_text="${2}"                    # Log message

    echo "$log_time - $log_level - $log_text"
}

check_result() {
    if [ $? -eq 0 ]; then
        log_message "INFO" "...Succesful"
    else
        log_message "ERROR" "...Failed"
        exit 1
    fi
}

# Check if the service exists
install_service() {
    local service_name="$1"
    if systemctl list-unit-files --all --type=service | grep -q "^.*$service_name.*"; then
        log_message "INFO" "Service '$service_name' already exists."
        return 0
    else
        log_message "INFO" "Service '$service_name' does not exist."

        log_message "INFO" "Updating package lists..."
        #sudo apt update -y
        check_result

        log_message "INFO" "Installing '$service_name'..."
        #sudo apt install -y $service_name
        check_result

        log_message "INFO" "Enabling '$service_name' to start on boot..."
        #sudo systemctl enable $service_name
        check_success

        log_message "INFO" "Starting '$service_name'..."
        #sudo systemctl start $service_name
        check_success

        log_message "INFO" "Checking '$service_name' status..."
        #sudo systemctl status $service_name --no-pager

        log_message "INFO" "'$service_name' has been installed successfully"
    fi
}

# checks if there's a parameter for the service name
if [ -z "$1" ]; then
    log_message "ERROR" "Usage: $0 <service-name>"
    exit 1
fi

install_service "$1"