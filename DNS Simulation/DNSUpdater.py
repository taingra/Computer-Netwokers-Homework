#!/usr/bin/python2

import argparse
import socket
import sys

parser = argparse.ArgumentParser(description='Update entries in the DNS table')
parser.add_argument("server", metavar="SERVER", type=str,
                    help='the DNS server to be updated')
parser.add_argument("cmd", metavar="COMMAND", type=str,
                    help='the command to be executed (add, delete, update)')
parser.add_argument("url", metavar="URL", type=str,
                    help='the domain whose IP is to be modified')
parser.add_argument("ip", metavar="IP", type=str, nargs='?',
                    help='the IP address to be added, or updated')

args = parser.parse_args()

prefix = "DNSUpdater: "

if args.cmd == "add" or args.cmd == "update":
    if not args.ip:
        sys.exit(prefix + args.cmd + " requires IP argument, see " +
                 sys.argv[0] + " --help")
    data = " ".join([args.cmd, args.url, args.ip])
elif args.cmd == "delete":
    data = " ".join([args.cmd, args.url])
else:
    sys.exit(prefix + args.cmd + " is not a valid command, see " +
             sys.argv[0] + " --help")

sock = socket.socket(socket.AF_INET, # internet
                     socket.SOCK_DGRAM) # udp
PORT = 1039
HOST = socket.gethostbyname(args.server)

sock.sendto(data, (HOST, PORT))

recv = sock.recv(1024)
# Handle Authentication
while recv == "AUTHENTICATION CODE":
    passwd = raw_input("DNSResolver is requesting authentication code: ")
    sock.sendto(passwd, (HOST, PORT))
    recv = sock.recv(1024)

print(prefix + recv)
