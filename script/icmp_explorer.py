#!/usr/bin/env python3

import signal
import argparse
import re
from ipaddress import ip_network
from ping3 import ping
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor

status = 0

# Close the program and change the status to stop threads
def def_handler(sig, frame):
    global status
    status = 1
    print(colored("\n[!] Quitting the program...\n", "red"))
    exit(1)

signal.signal(signal.SIGINT, def_handler) # CTRL + C

# Create and return menu arguments
def get_arguments():
    argparser = argparse.ArgumentParser(description="Fast ICMP Network Scanner")
    argparser.add_argument("-t", "--target", dest="target", required=True, help="Target host with bitmask to scan. (Ex: 10.23.10.1/21)")

    arguments = argparser.parse_args()

    return arguments.target

# Verify the correct format target: 10.10.10.10/21
def verify(target):
    match = re.match(r"([0-9]{1,3}\.){3}[0-9]{1,3}\/[1-3]{1}[0-9]{1}", target)
    host, bitmask = [False, False]

    if match:
        host, bitmask = target.split('/')
        bitmask = int(bitmask)

    return (True if match else False) and host and (bitmask < 33), target

# Get the list of ip's to scan
def subnetting(target):    
    red = ip_network(target, strict=False)
    
    return list(red.hosts())

# Make ping to each ip
def make_ping(ip):
    if status:
        return

    isUp = ping(f"{ip}", timeout=0.6)

    if isUp:
        print(colored(f"\t[+] {ip}", "green"))

# Control of the scan with threads
def scan(hosts):

    print(colored("\n[~] Scanning...\n", "blue"))

    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(make_ping, hosts)

# Sammy-ulfh Banner
def print_banner():
    print(colored("""
█ █▀▀ █▀▄▀█ █▀█   █▀▀ ▀▄▀ █▀█ █░░ █▀█ █▀█ █▀▀ █▀█
█ █▄▄ █░▀░█ █▀▀   ██▄ █░█ █▀▀ █▄▄ █▄█ █▀▄ ██▄ █▀▄\n""", 'white'))

    print(colored("""Mᴀᴅᴇ ʙʏ sᴀᴍᴍʏ-ᴜʟғʜ\n""", 'yellow'))

# Main function
def main():
    print_banner()
    target = get_arguments()
    isValid, data = verify(target)

    if isValid:
        hosts = subnetting(data)
        scan(hosts)
    else:
        print(colored("\n[!] Target not valid.\n", "red"))

if __name__ == "__main__":
    main()
