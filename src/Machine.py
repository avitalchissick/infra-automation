from jsonschema import validate, ValidationError, exceptions

from OperatingSystem import OperatingSystemType
from StorageType import StorageType
from logger import logger


class Machine:
    """
    This class represents a virtual machine.

    Properties
        name (str): The name of the machine.
        os (OperatingSystemType): Type of operating system.
        cpu_cores (int): Number of CPU cores allocated to the machine.
        ram_gb (int): Amount of RAM (in GB) allocated to the machine.
        storage_gb (int): Amount of storage (in GB) allocated to the machine.
        storage_type (StorageType): Type of storage disk.
        is_running (bool): The current state of the virtual machine (running or stopped).
    """

    # Define the JSON schema for validation
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "os": {"type": "string"},
            "cpu_cores": {"type": "number", "minimum": 1, "multipleOf": 0.5},
            "ram_gb": {"type": "integer", "minimum": 1},
            "storage_gb": {"type": "integer", "minimum": 1},
            "storage_type": {"type": "string"},
        },
        "required": ["name", "os", "cpu_cores", "ram_gb", "storage_type", "storage_gb"],
        "additionalProperties": False,  # Prevent extra properties
    }

    def __init__(
        self,
        name: str,
        os: OperatingSystemType,
        cpu_cores: int,
        ram_gb: int,
        storage_type: StorageType,
        storage_gb: int,
    ):
        """
        Initialize the virtual machine with the provided configuration.

        Args:
            name (str): The name of the virtual machine.
            os (OperatingSystemType): The operating system
            cpu_cores (int): Number of CPU cores to allocate.
            ram_gb (int): Amount of RAM (in GB) to allocate.
            storage_type (StorageType): Type of storage disk.
            storage_gb (int): Amount of storage (in GB) to allocate.
        """
        self.name = name
        self.os = os
        self.cpu_cores = cpu_cores
        self.ram_gb = ram_gb
        self.storage_type = storage_type
        self.storage_gb = storage_gb
        self.is_running = False

    def start(self):
        """
        Start the machine.

        If the machine is already running, it will notify the user.
        Otherwise, it will start the machine.
        """
        if not self.is_running:
            self.is_running = True
            logger.info("Machine %s is now running.", self.name)
        else:
            logger.info("Machine %s is already running.", self.name)

    def stop(self):
        """
        Stop the  machine.

        If the machine is already stopped, it will notify the user.
        Otherwise, it will stop the machine.
        """
        if self.is_running:
            self.is_running = False
            logger.info("Machine %s has been stopped.", self.name)
        else:
            logger.info("Machine %s is already stopped.", self.name)

    def restart(self):
        """
        Restart the machine.

        The machine will be stopped and then started again.
        """
        logger.info("Restarting machine %s...", self.name)
        self.stop()
        self.start()

    def status(self):
        """
        Print the current status of the machine.

        Displays whether the machine is running or stopped.
        """
        running_status = "running" if self.is_running else "stopped"
        logger.info("Machine %s is %s.", self.name, running_status)

    def allocate_resources(self, cpu_cores=None, ram_gb=None, storage_gb=None):
        """
        Allocate or update resources for the machine.

        You can update one or more of the VM's resources (CPU cores, RAM, storage).

        Args:
            cpu_cores (int, optional): The number of CPU cores to allocate. Defaults to None.
            ram_gb (int, optional): The amount of RAM (in GB) to allocate. Defaults to None.
            storage_gb (int, optional): The amount of storage (in GB) to allocate. Defaults to None.
        """
        if cpu_cores:
            self.cpu_cores = cpu_cores
        if ram_gb:
            self.ram_gb = ram_gb
        if storage_gb:
            self.storage_gb = storage_gb

        logger.info(
            "Machine %s resources updated: CPU Cores = %.1f, RAM = %i GB, Storage = %i GB.",
            self.name,
            self.cpu_cores,
            self.ram_gb,
            self.storage_gb,
        )

    def __str__(self):
        """
        Return a string representation of the machine.

        This method provides a concise overview of the machine's current configuration and state.
        """
        return (
            f"Machine(name={self.name}, "
            f"os={self.os.name}, "
            f"cpu_cores={self.cpu_cores}, "
            f"ram_gb={self.ram_gb}, "
            f"storage_type={self.storage_type.name}, "
            f"storage_gb={self.storage_gb}, "
            f"is_running={self.is_running})"
        )

    def to_dict(self):
        """
        Returns a dictionary representation of the machine
        """
        return {
            "name": self.name,
            "os": self.os.name,
            "cpu_cores": self.cpu_cores,
            "ram_gb": self.ram_gb,
            "storage_type": self.storage_type.name,
            "storage_gb": self.storage_gb,
        }

    @staticmethod
    def validate(machine) -> bool:
        """
        Using json schema for validation.
        """
        try:
            validate(instance=machine.to_dict(), schema=Machine.schema)
            return True
        except ValidationError as e:
            logger.error("Validation error: %s", e.message)
        except exceptions.SchemaError as e:
            logger.error("Schema error: %s", e.message)
        return False


# Example usage:
if __name__ == "__main__":
    # Creating a machine with initial resources
    m1 = Machine("UbuntuVM", OperatingSystemType.LINUX, 4.5, 16, StorageType.SSD, 100)

    # Starting the VM and checking its status
    m1.start()
    m1.status()

    # Allocating new resources
    m1.allocate_resources(cpu_cores=8.5, ram_gb=32)

    # Restarting the VM and checking its status again
    m1.restart()
    m1.status()

    # Printing the VM object (it will show the string representation)
    print(m1)
