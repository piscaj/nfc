import socket
import struct
import sys

def wake_on_lan(ip,mac_address):
    print('start send magic packet to ' + mac_address)
    mac_address_fmt = mac_address.replace('-', '').replace(':', '')
    host = (ip[: ip.rindex('.') + 1] + '255', 9)
    data = ''.join(['FFFFFFFFFFFF', mac_address_fmt * 16])
    send_data = b''

    for i in range(0, len(data), 2):
        send_data = b''.join([send_data, struct.pack('B', int(data[i: i + 2], 16))])

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(send_data, host)
