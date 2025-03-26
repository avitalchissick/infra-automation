"""
Simulating getting a virtual machine configuration from the user
Calling a bash script to install a service
"""

import subprocess
import json
from pathlib import Path
from OperatingSystem import OperatingSystemType
from StorageType import StorageType
from Machine import Machine
from logger import logger

CONFIG_FILE = Path("configs/instances.json")


class InvalidName(Exception):
    """
    Exception used when the user enters an invalid name.
    """

    pass


def get_machine_name():
    """
    Asks the user for a name for the machine and validates that
    it is not empty and that it contains only alpha numeric characters.
    """
    try:
        user_name = input("Enter machine name: ").strip()
        if not user_name:
            raise InvalidName("Name cannot be empty.")
        if not user_name.isalnum():
            raise InvalidName("Name must be alpha-numeric.")
        return user_name
    except InvalidName as e:
        logger.error("Invalid name: %s", e)
        return None
    except KeyboardInterrupt:
        logger.info("User exited input process")
        return None


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
        logger.error("Invalid selection. Enter a valid OS number.")
        return None
    except KeyboardInterrupt:
        logger.info("User exited input process")
        return None


def get_cpu_cores():
    """
    Ask the user how many CPU cores the machine will have
    """
    try:
        user_choice = float(
            input(
                "Enter the number of CPU cores (must be an integer or multiplication of 0.5):"
            )
        )
        if user_choice % 0.5 == 0 and user_choice > 0:
            return user_choice
        raise ValueError
    except ValueError:
        logger.error(
            "CPU cores must be a numerical value greater then 0 and in multiplication of 0.5"
        )
        return None
    except KeyboardInterrupt:
        logger.info("User exited input process")
        return None


def get_machine_memory(memory_type: str):
    """
    Ask the user how much memory of the given type, the machine will have
    """
    try:
        user_choice = int(input(f"Enter the amount in GB of {memory_type} memory:"))
        if user_choice <= 10:
            raise ValueError
        return user_choice
    except ValueError:
        logger.error("%s memory must be a integer greater then 1", memory_type)
        return None
    except KeyboardInterrupt:
        logger.info("User exited input process")
        return None


def get_machine_storage_type():
    """
    Ask the user which storage type will be installed on the machine
    """
    print("Please select the storage type from the following list: ")
    for storage_type in StorageType:
        print(f"{storage_type.value}: {storage_type.name}")

    try:
        user_choice = int(input("Enter your selection:"))
        return StorageType(user_choice)
    except ValueError:
        logger.error("Invalid selection. Enter a value storage type number.")
        return None
    except KeyboardInterrupt:
        logger.info("User exited input process")
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

    storage_type = get_machine_storage_type()
    if not storage_type:
        return None

    storage = get_machine_memory("Storage")
    if not storage:
        return None

    return Machine(name, os, cpu_cores, ram, storage_type, storage)


def get_user_machines():
    """
    Gets a list of machines from the user
    """
    machines = []
    while True:
        try:
            yes_no_reply = (
                input("Would to like to define a virtual machine (yes/no): ")
                .strip()
                .lower()
            )
            if yes_no_reply != "yes":
                logger.info("Ending user configuration")
                break

            user_machine = get_machine_config_from_user()
            if not user_machine:
                continue  # Skip invalid machine configurations

            if Machine.validate(user_machine):
                logger.info("User added machine configuration: %s", user_machine)
                machines.append(user_machine)

        except KeyboardInterrupt:
            logger.info("User exited machine configuration.")
            break
    return machines


def save_machines(machines: list):
    """
    Save listed machines to the confiiguration file.
    """
    if not machines:
        logger.info("No machines were configured by the user")

    data = [m.to_dict() for m in machines]
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists

    with CONFIG_FILE.open("w") as f:
        json.dump(data, f, indent=4)

    logger.info("Save %i machines to %s", len(machines), CONFIG_FILE.name)


def create_machines(machines: list):
    """
    Creates listed machines.
    """
    for m in machines:
        create_machine(m)


def create_machine(machine: Machine):
    try:
        logger.info("Creating machine: %s", machine)
    except Exception as ex:
        logger.error("Failed to create machine %s. Error: %s", machine, ex)


def run_setup_service_script(service_name):
    """
    Function to run a bash install script for a service
    """
    try:
        subprocess.run(["bash", "scripts/setup_service.sh", service_name], check=True)
        logger.info("%s setup completed.", service_name)
    except subprocess.CalledProcessError as e:
        logger.error("Failed to install %s: %s", service_name, e)
    except subprocess.TimeoutExpired as e:
        logger.error("Timeout while attempting to install %s: %s", service_name, e)
    except FileNotFoundError:
        logger.error("Setup script not found: scripts/setup_service.sh")
