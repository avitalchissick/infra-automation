# DevOps Infrastructure Provisioning & Configuration Automation Project
[GitHub repository](https://github.com/avitalchissick/infra-automation)

## Setup Instructions
```
git clone https://github.com/avitalchissick/infra-automation.git
cd infra-automation
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

Run the project using `python main.py`

## Project phases
**Phase 1** - Develop the foundational structure of an infrastructure provisioning tool, using mockup to simulate automation.

## Project Overview
The project uses python to allow the user to enter configuration for virtual machines.  
Key features include:  
* User input validation.  
* Bash scripting for automating service setup.  
* Comprehensive logging and error handeling.  

### Project Structure:
**Configuration Files**
* `configs/` - Contains configuration files.  
* `configs/instances.json` - Stores the list of machines configured by the user.  

**Logging**
* `logs/` - Contains log files.  
* `logs/provisioning.log` - Logs the provisioning process.  

**Scripts**
* `scripts/` - Containss Bash scripts.  
* `scripts/setup_service.sh` - Script for automating service setup.  

**Sorce Code**
* `src/` - Stores python code files.  
* `main.py` - Entry point for the project. Prompting the user for machines configuration. Configuration will be saved to configs\instance.json.  
* `logger.py` -  Configures and manages logging.  
* `Machine.py` - Defines a class representing a machine configuration.  
* `OperatingSystem.py` - Enum class listing available operating systems for the virtual machines.  
* `StorageType.py` - Enum class listing of available storage disk types for the virtual machines.  
* `infra_simulator.py` - Implements functions used in the simulations proceess and triggers Bash script to automate service setup.  

**submitted by:** Avital Chissick
