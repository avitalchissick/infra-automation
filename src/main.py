"""
The main function for the project
"""
from infra_simulator import get_user_machines, run_setup_service_script


def main():
    # Tasks 1+2 - gets machines configuration
    get_user_machines()

    # Task 3 - Automating Service Installation with Bash
    run_setup_service_script("nginx")


if __name__ == "__main__":
    main()
