#!/usr/bin/env pythin


import scapy.all as scapy
import subprocess
import re


def print_result(results_list):
    print("IP\t\t\tMAC Address\n-------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])


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

def get_current_ip(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    ip_address_search_result = re.search(r"[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}", str(ifconfig_result))
    if ip_address_search_result:
        print(ip_address_search_result.group(1))
    else:
        print("[-] Could not find IP address")


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not find MAC address")


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["sudo", "ifconfig", interface, "up"])


def mac_changer():
    interface = input('Interface to change MAC address\n>')
    new_mac = input('New MAC address\n>')
    current_mac = get_current_mac(interface)
    print("Current MAC = " + str(current_mac))
    change_mac(interface, new_mac)
    current_mac = get_current_mac(interface)
    if current_mac == new_mac:
        print("[+] MAC address was successfully changed to " + current_mac)
    else:
        print("[-] MAC address did not get changed")


def network_scanner():
    target = input('Target IP / IP range.\n>')
    scan_result = scan(target)
    print_result(scan_result)


print("""
  _    _            _ _______          _                     
 | |  | |          | |__   __|        | |                    
 | |__| | __ _  ___| | _| | ___   ___ | |                    
 |  __  |/ _` |/ __| |/ / |/ _ \ / _ \| |                    
 | |  | | (_| | (__|   <| | (_) | (_) | |                    
 |_|  |_|\__,_|\___|_|\_\_|\___/ \___/|_|__ ____ ____ ______ 
 | |         |  _ \                     /_ |___ \___ \____  |
 | |__  _   _| |_) | ___  _ __  _   _ ___| | __) |__) |  / / 
 | '_ \| | | |  _ < / _ \| '_ \| | | / __| ||__ <|__ <  / /  
 | |_) | |_| | |_) | (_) | | | | |_| \__ \ |___) |__) |/ /   
 |_.__/ \__, |____/ \___/|_| |_|\__,_|___/_|____/____//_/    
         __/ |                                               
        |___/                                                                                                                           
""")
print("---------------------------------------------------")
print("[1]. Change your mac address")
print("[2]. Scan network")
print("[3]. Informations")
print("[4]. Exit")

try:
	choose = input('Choose a function\n >')
	if(choose == "1"):
	    mac_changer()
	elif(choose == "2"):
	    interface = input('Select the interface\n>')
	    get_current_ip(interface)
	    network_scanner()
	elif(choose == "3"):
	    print("In future this will be a big hacking program designed by Bonus1337" )
	elif(choose == "4"):
	    exit()
except KeyboardInterrupt:
	print("\nYou off the program")
