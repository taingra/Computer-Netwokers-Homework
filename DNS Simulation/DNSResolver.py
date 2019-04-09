#!/usr/bin/python2


# Load know dns list
import csv

with open('dnsentries.csv', mode='r') as infile:
    reader = csv.reader(infile)
    entries = dict((rows[0], rows[1]) for rows in reader)



# Start server
import socket

HOST, PORT = "localhost", 1039
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

password = "12345" # a verry good password
prefix = "DNSResolver: "

while True: # Serve forever
    print(prefix + "waiting for request...")
    data, addr = sock.recvfrom(1024)
    args = data.split()
    if args[0] == "add" or args[0] == "update" or args[0] == "delete":
        print(prefix + "\""+ args[0] + "\" request recieved")

        # REQUEST PASSWORD AUTHENTICATION
        auth = False
        for _ in range(3): # try 3 times before giving up
            sock.sendto("AUTHENTICATION CODE", (addr))
            userpass, addr = sock.recvfrom(1024)
            if userpass.strip() == password:
                auth = True
                break

        if not auth:
            sock.sendto("Authentication failed.", (addr))

        if args[0] == "add":
            try:
                entries[args[1]] = args[2]
                response = "Successfully added " + args[1] + " as " + args[2]
            except:
                response = "Failed to add " + args[1] + " as " + args[2]


        elif args[0] == "update":
            if args[1] in entries:
                entries[args[1]] = args[2]
                response = "Successfully updated " + args[1] + " as " + args[2]
            else:
                response = "Failed to update " + args[1] + " as " + args[2]

        elif args[0] == "delete":
            try:
                del entries[args[1]]
                response = "Successfully deleted " + args[1] + " as " + args[2]
            except:
                response = "Failed to delete " + args[1]


        print(prefix + response + "; sending " + response  + " response")

    else:
        print(prefix + "Request received - " + args[0])
        try:
            response = entries[args[0]].strip()
        except:
            response = "null"

        print(prefix + "Responding with " + response)

    sock.sendto(response, (addr))
