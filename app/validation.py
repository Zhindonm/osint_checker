import socket
from IPy import IP

def is_valid_ip_address(address):
    try:
        socket.inet_aton(address)

    except socket.error:
        return False

    return IP(address).iptype()=='PUBLIC'
