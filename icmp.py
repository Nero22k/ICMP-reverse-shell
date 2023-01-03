import os
import socket
import struct
import threading

# Constants
ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0

# Functions
def checksum(data: bytes) -> int:
    """Calculate the checksum of the given data."""
    s = 0
    n = len(data) % 2
    for i in range(0, len(data) - n, 2):
        s += (data[i] << 8) + data[i + 1]
    if n:
        s += (data[i + 1] << 8)
    while s >> 16:
        s = (s & 0xffff) + (s >> 16)
    return ~s & 0xffff

def create_packet(id: int, sequence: int) -> bytes:
    """Create an ICMP echo request packet with the given ID and sequence number."""
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, ICMP_ECHO_REPLY, 0, id, sequence)
    data = b'test'
    packet = header + data
    checksum_val = checksum(packet)
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, ICMP_ECHO_REPLY, checksum_val, id, sequence)
    return header + data

def send_packet(packet: bytes, destination: str) -> None:
    """Send the given packet to the destination."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    sock.sendto(packet, (destination, 1))

def receive_packet(id: int, sequence: int, timeout: float) -> bool:
    """Receive a packet with the given ID and sequence number.
    Return True if the packet is received, False otherwise.
    """
    start_time = time.time()
    while True:
        current_time = time.time()
        if current_time - start_time > timeout:
            return False
        try:
            packet, source = sock.recvfrom(2048)
            icmp_header = packet[20:28]
            packet_type, code, checksum_val, packet_id, packet_sequence = struct.unpack('bbHHh', icmp_header)
            if packet_type == ICMP_ECHO_REPLY and packet_id == id and packet_sequence == sequence:
                return True
        except socket.error:
            pass

# Main
def ping(destination: str, timeout: float = 1.0) -> float:
    """Send an ICMP echo request to the given destination and return the time taken for the response.
    If no response is received within the given timeout, return None.
    """
    id = os.getpid() & 0xFFFF
    sequence = 1
    packet = create_packet(id, sequence)
    send_packet(packet, destination)
    start_time = time.time()
    if receive_packet(id, sequence, timeout):
        return time.time() - start_time
    else:
        return None

if __name__ == '__main__':
    address = input('Enter the IP address: ')
    response_time = ping(address)
    if response_time:
        print('Response time:', response_time, 'seconds')
    else:
        print('No response received')
