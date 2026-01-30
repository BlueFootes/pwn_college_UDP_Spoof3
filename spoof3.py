import socket
import threading
from itertools import repeat
def listener():
    try:
        main_soc=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        main_soc.bind(("0.0.0.0",31338))
        while True:
                data=main_soc.recvfrom(1024)
                print(data)
                
    except Exception as e:
        print("error: " ,e)


 
ports = list(range(1,65536))

t=threading.Thread(target=listener, daemon=True)
t.start()


s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(("0.0.0.0",31337))
udp_ip = "10.0.0.2"
message = b"FLAG:10.0.0.1:31338"   
for i in ports:
    try:
        #print(i)
        s.sendto(message,(udp_ip,i))
    except socket.timeout:
        pass
    except Exception as e:
        print("error: " , e)

s.close()
