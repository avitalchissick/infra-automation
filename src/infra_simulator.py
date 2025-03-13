"""
Simulating getting a virtual machine definition from the user
"""

import json
from OperatingSystem import OperatingSystemType
from Machine import Machine

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
        print(f"Invalid name: {e}")
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
        print("Invalid selection. The number must correspond to an operating system")
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
        print("CPU cores must be a integer greater then 0")
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
        print(f"{memory_type} memory must be a integer greater then 0")
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
            print("Goodbye.")
            break

        user_machine = get_machine_config_from_user()
        if user_machine is not None and Machine.validate(user_machine):
            machines.append(user_machine)

        print("")

    return machines


# gets machines configuration from the user and saves it to the file
machine_instances = get_user_machines()
data = [m.to_dict() for m in machine_instances]
with open("configs/instances.json", "w") as f:
    json.dump(data, f, indent=4)
