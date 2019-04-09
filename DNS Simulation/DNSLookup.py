#!/usr/bin/python2

import argparse
import socket

parser = argparse.ArgumentParser(description='Simple DNS lookup')
parser.add_argument("server", metavar="SERVER", type=str,
                    help='DNS server address')
parser.add_argument("url", metavar="URL", type=str,
                    help='Server URL to be lookedup')

args = parser.parse_args()

# print('the server:  ' + args.server)
# print('the URL: ' + args.URL)


sock = socket.socket(socket.AF_INET, # internet
                     socket.SOCK_DGRAM) # udp
PORT = 1039

HOST = socket.gethostbyname(args.server)

sock.sendto(args.url, (HOST, PORT))

recv = sock.recv(1024)
print("DNSLookup: " + args.url + " is " + recv.strip())
