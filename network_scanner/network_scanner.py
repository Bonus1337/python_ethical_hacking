#!/usr/bin/env python
import scapy.all as scapy
import optparse


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Target IP / IP range.")
    options, arguments = parser.parse_args()
    return options

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

def print_result(results_list):
    print("IP\t\t\tMAC Address\n-------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])


print("""
  _   _      _                      _                                          
 | \ | |    | |                    | |                                         
 |  \| | ___| |___      _____  _ __| | __  ___  ___ __ _ _ __  _ __   ___ _ __ 
 | . ` |/ _ \ __\ \ /\ / / _ \| '__| |/ / / __|/ __/ _` | '_ \| '_ \ / _ \ '__|
 | |\  |  __/ |_ \ V  V / (_) | |  |   <  \__ \ (_| (_| | | | | | | |  __/ |   
 |_| \_|\___|\__| \_/\_/ \___/|_|  |_|\_\ |___/\___\__,_|_| |_|_| |_|\___|_|   
  _             ____                       __ ____ ____ ______                 
 | |           |  _ \                     /_ |___ \___ \____  |                
 | |__  _   _  | |_) | ___  _ __  _   _ ___| | __) |__) |  / /                 
 | '_ \| | | | |  _ < / _ \| '_ \| | | / __| ||__ <|__ <  / /                  
 | |_) | |_| | | |_) | (_) | | | | |_| \__ \ |___) |__) |/ /                   
 |_.__/ \__, | |____/ \___/|_| |_|\__,_|___/_|____/____//_/                    
         __/ |                                                                 
        |___/                                                                  

"""
options = get_arguments()


scan_result = scan(options.target)
print_result(scan_result)