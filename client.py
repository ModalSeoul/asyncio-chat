"""
Socket client to connect to the CRI server. Feel free to make your own,
but understand that you'll need to basically port this and add on to it
from there. The server will reject anything it doesn't recognize.
"""
from socket import *
import sys

sock = socket(AF_INET, SOCK_STREAM)
server_address = (sys.argv[2], 25000)
sock.connect(server_address)

try:
    message = sys.argv[1]
    sock.sendall(message)
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)

finally:
    sock.close()
