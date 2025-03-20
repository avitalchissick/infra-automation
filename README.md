## DevOps Infrastructure Provisioning & Configuration Automation Project
[GitHub repository](https://github.com/avitalchissick/infra-automation)


### Setup
```
git clone https://github.com/avitalchissick/infra-automation.git
cd infra-automation
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

Run the project with: python main.py

### Project phases
**Phase 1** - build a skeleton of an infrastructure provisioning tool using mockup to simulate automation.

### Documentation
The project uses python to allow the user to enter configuration for virtual machines.  
User input will be validated.  
The project will also use a Bash script to automate service setup.  
Logging and error handeling will be used in the code and script.  

**Project structure:**
configs folder - holds configuration files.  
Phase 1 - files instances.json stores the list of machines configured by the user.  

logs folder - holds log files.  
provisioning.log - log of the provisioning process.  

scripts folder - holds Bash scripts.  
setup_service.sh - script for setting up a service.  

src folder - holds python code files.  
main.py is the main execution file.  
Running it will prompt the user for machines configuration.  
Machines configuration will be saved to configs\instance.json.  

logger.py defines and configures a logger for the project.  
Machine.py defines a class to hold a machine configuration.  
OperatingSystem.py defines an enum class to hold a list of available operating systems for the virtual machines.  
StorageType.py defines an enum class to hold a list of available storage disk types for the virtual machines.  
infra_simulator.py defines functions used in the simulations proceess and calling the Bash script to automate service setup.  

**submitted by:** Avital Chissick
