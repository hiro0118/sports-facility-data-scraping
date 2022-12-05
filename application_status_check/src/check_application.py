from time import sleep

from appilcation import get_application_status

INITAL_WAIT = 10

def main():
    print("Waiting for selenium service to be ready...")
    sleep(INITAL_WAIT)
    get_application_status()

if __name__ == "__main__":
    main()
