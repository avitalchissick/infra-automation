"""
The main function for the project
"""
from infra_simulator import get_user_machines, save_machines, create_machines, run_setup_service_script


def main():
    # Tasks 1 - gets machines configuration
    user_machines = get_user_machines()

    # Task 2 - saves machines to the configuration file
    save_machines(user_machines)

    # creating the machines
    create_machines(user_machines)

    # Task 3 - Automating Service Installation with Bash
    run_setup_service_script("nginx")


if __name__ == "__main__":
    main()
