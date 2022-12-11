import os

from check_availability import check_availability, check_availability_scheduled

MODE_KEY = 'MODE'
SCHEDULED_MODE = 'scheduled'


def main():
    mode = os.environ.get(MODE_KEY)
    print(f"Execution mode: {mode}")
    if mode == SCHEDULED_MODE:
        check_availability_scheduled()
    else:
        check_availability()


if __name__ == "__main__":
    main()
