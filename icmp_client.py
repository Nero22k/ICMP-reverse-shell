import socket
import struct
import os

def start_client(host, port):
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
    icmp_socket.settimeout(3)
    icmp_socket.connect((host, port))
    
    while True:
        cmd = input("#> ")
        if cmd == "exit":
            break

        # Create ICMP packet
        packet = struct.pack("!HHH", 8, 0, 0) + os.urandom(4) + cmd.encode()

        # Send the packet
        icmp_socket.send(packet)

        # Receive the response
        try:
            data, addr = icmp_socket.recvfrom(1024)
            print(data.decode())
        except socket.timeout:
            print("No response from server")

start_client("127.0.0.1", 0)
