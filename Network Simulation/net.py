#!/usr/bin/env python
#
# Computer Networks Prgramming Assignment 1
#
# Thomas Ingram <taingram@mtu.edu>
#
# Simulate a network

import argparse
import re

class Switch:
    def __init__(self, switch_num):
        self.ports = []
        self.forward = {}
        self.num = switch_num
        self.string = 'SW' + str(switch_num)

    def set_port(self, port_num, dest):
        if len(self.ports) > port_num:
            self.ports.remove(port_num)
        self.ports.insert(port_num, dest)

    def __str__(self):
        out = "Switch " + str(self.num) + ":"
        index = 0
        for port in self.ports:
            out += " Port " + str(index) + ": " + self.ports[index]
            index += 1

        return out

class Packet:
    def __init__(self, start, end, cir):
        self.start = 'H' + start
        self.end = 'H' + end
        self.cir = cir

parser = argparse.ArgumentParser(description='Simulate a network')
parser.add_argument('inputfile', metavar='FILE', type=str,
                    help='a file containing the description of a network')

args = parser.parse_args()

switches = []
packets = []

with open(args.inputfile, 'r') as file:
    for line in file:
        words = line.split()
        if 'hosts' in words[0]:
            num_hosts = int(words[2])
        elif 'switches' in words[0]:
            num_switches = int(words[2])
        elif 'SW' in words[0]:
            index = int(words[0][2])
            if len(switches) <= index:
                switches.append(Switch(index))
            switches[index].set_port(int(words[0][4]), words[2])
        elif 'P' in words[0][0]:
            words = words[0].split('-')
            packets.append(Packet(words[0][1:], words[1], False))
        elif 'V' in words[0][0]:
            words = words[0].split('-')
            packets.append(Packet(words[0][1:], words[1], True))

# Generate forwarding tables
# for switch in switches:
#     for i in range(len(ports)):
#         if ports[i]
#     print(switch)

hosts = []
for i in range(num_hosts):
    hosts.append('H' + str(i))



def switch_ports(switch):
    regex = re.compile('SW*')
    swlist = filter(regex.match, switch.ports)

    return swlist

# Generate forwarding tables
for host in hosts:
    for switch in switches:
        if host in switch.ports:
            switch.forward[host] = switch.ports.index(host)
        else:
            # find fastest route to host
            sw = switch_ports(switch)
            if len(sw) == 0:
                print('Error switch ' + str(switch.num) + ' not connected to other switches')
            elif len(sw) == 1:
                switch.forward[host] = switch.ports.index(sw[0])
            else: # sw greater than 1, determine which leads to dest host
                visited = []
                visited.append(switch.string)
                i = 0
                initial_switches = []
                for s in sw:
                    initial_switches.append(switches[int(s[2:])])
                tmpsws = []
                new = []
                while host not in switch.forward and i < num_switches:

                    for init in initial_switches:
                        del tmpsws[:]
                        tmpsws.append(init)
                        for _ in range(i): # move i connections down the network
                            for tmp in tmpsws:
                                conn = switch_ports(tmp)
                                for c in conn:
                                    if c not in visited:
                                        new.append(c)

                            for n in new:
                                tmpsws.append(switches[int(n[2:])])

                        for tmp in tmpsws:
                            if host in tmp.ports:
                                if host in init.forward and init.ports[init.forward[host]] == switch.string:
                                    visited.append(tmp.string)
                                else:
                                    switch.forward[host] = switch.ports.index(init.string)
                                    break
                            else:
                                visited.append(tmp.string)
                    i += 1

# debug printing
# print('Fowarding tables')
# for switch in switches:
#     print(switch)

#     print(switch.string)
#     print(switch.forward)

for packet in packets:
    if not packet.cir:
        print("Packet starting at Host " + packet.start[1:])
        for switch in switches:
            if packet.start in switch.ports:
                while packet.end not in switch.ports:
                    port = switch.forward[packet.end]
                    addr = switch.ports[port]
                    newswitch = switches[int(addr[2:])]
                    print('Switch ' + str(switch.num) + ' forwarding packet to Switch ' +
                          str(newswitch.num) + ' on interface ' + str(port))
                    switch = newswitch
                print('Packet delivered to Host ' + packet.end[1:])
                break
    else:
        print("Circuit requested by Host " + packet.start[1:])
        for switch in switches:
            if packet.start in switch.ports:
                last = packet.start
                while packet.end not in switch.ports:
                    port = switch.forward[packet.end]
                    addr = switch.ports[port]
                    newswitch = switches[int(addr[2:])]
                    print('Switch ' + str(switch.num) + ' creating circuit with incoming interface ' +
                          str(switch.ports.index(last)) + ' and outgoing interface ' + str(port))
                    last = switch.string
                    switch = newswitch
                print('Host ' + packet.end[1:] + ' requests incoming VCI ' + packet.start[1:])
                while packet.start not in switch.ports:
                    port = switch.forward[packet.start]
                    addr = switch.ports[port]
                    newswitch = switches[int(addr[2:])]
                    print('Switch ' + str(switch.num) + ' requests incoming VCI ' + packet.start[1:])
                    switch = newswitch
                print('Circuit established')
                break
