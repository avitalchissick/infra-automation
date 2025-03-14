"""
Simulating getting a virtual machine configuration from the user
Calling a bash script to install a service
"""

import subprocess
import json
from OperatingSystem import OperatingSystemType
from Machine import Machine
from logger import logger

CONFIG_FILE = "configs/instances.json"


class InvalidName(Exception):
    pass


def get_machine_name():
    """
    Asks the user for a name for the machine and validates that
    it is not empty and that it contains only alpha numeric characters.
    """
    try:
        user_name = input("Enter machine name: ").strip()
        if len(user_name) == 0:
            raise InvalidName("Name cannot be empty.")
        if not user_name.isalnum():
            raise InvalidName("Name must be alpha-numeric.")
    except InvalidName as e:
        logger.error(f"Invalid name: {e}")
        user_name = None

    return user_name


def get_machine_os():
    """
    Ask the user which operating system will be installed on the machine
    """
    print("Please select an operating system from the following list: ")
    for os_type in OperatingSystemType:
        print(f"{os_type.value}: {os_type.name.capitalize()}")

    try:
        user_choice = int(input("Enter your selection:"))
        return OperatingSystemType(user_choice)
    except ValueError:
        logger.error(
            "Invalid selection for operating system. The number must correspond to an operating system"
        )
    return None


def get_cpu_cores():
    """
    Ask the user how many CPU cores the machine will have
    """
    try:
        user_choice = int(input("Enter the number of CPU cores:"))
        if user_choice <= 0:
            raise ValueError
        return user_choice
    except ValueError:
        logger.error("CPU cores must be a integer greater then 0")
    return None


def get_machine_memory(memory_type: str):
    """
    Ask the user how much memory of the given type, the machine will have
    """
    try:
        user_choice = int(input(f"Enter the amount in GB of {memory_type} memory:"))
        if user_choice <= 0:
            raise ValueError
        return user_choice
    except ValueError:
        logger.error(f"{memory_type} memory must be a integer greater then 0")
    return None


def get_machine_config_from_user():
    """
    Asks the user for machine configuration.
    """
    name = get_machine_name()
    if not name:
        return None

    os = get_machine_os()
    if not os:
        return None

    cpu_cores = get_cpu_cores()
    if not cpu_cores:
        return None

    ram = get_machine_memory("RAM")
    if not ram:
        return None

    storage = get_machine_memory("Storage")
    if not storage:
        return None

    return Machine(name, os, cpu_cores, ram, storage)


def get_user_machines():
    """
    Gets a list of machines from the user
    """
    machines = []
    while True:
        yes_no_reply = (
            input("Would to like to define a virtual machine (yes/no): ")
            .strip()
            .lower()
        )
        if yes_no_reply != "yes":
            logger.info("Ending user configuration")
            break

        user_machine = get_machine_config_from_user()
        if user_machine is not None and Machine.validate(user_machine):
            logger.info(f"User added machine configuration: {user_machine}")
            machines.append(user_machine)

    data = [m.to_dict() for m in machines]
    if len(data) > 0:
        logger.info(f"User configured {len(machines)} machines")
        with open("configs/instances.json", "w") as f:
            json.dump(data, f, indent=4)
    else:
        logger.info("No machines were configured by the user")

    return machines


def run_setup_service_script(service_name):
    """
    Function to run a bash install script for a service
    """
    try:
        subprocess.run(["bash", "scripts/setup_service.sh", service_name], check=True)
        logger.info(f"{service_name} setup completed.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install {service_name}: {e}")
    except subprocess.TimeoutExpired as e:
        logger.error(f"Timeout while attempting to install {service_name}: {e}")
