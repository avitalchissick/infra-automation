class Machine:
    """
    This class represents a virtual machine.

    Properties
        name (str): The name of the machine.
        os (str): Type of operating system.
        cpu_cores (int): Number of CPU cores allocated to the machine.
        ram_gb (int): Amount of RAM (in GB) allocated to the machine.
        storage_gb (int): Amount of storage (in GB) allocated to the machine.

    Methods:
        is_running (bool): The current state of the virtual machine (running or stopped).
    """

    def __init__(
        self, name: str, os: str, cpu_cores: int, ram_gb: int, storage_gb: int
    ):
        self.name = name
        self.os = os
        self.cpu_cores = cpu_cores
        self.ram_gb = ram_gb
        self.storage_gb = storage_gb
