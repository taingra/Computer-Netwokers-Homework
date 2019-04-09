#!/usr/bin/python

entries = {'C4.50.0.0/12' : 'A',
           'C4.5E.10.0/20' : 'B',
           'C4.60.0.0/12' : 'C',
           'C4.68.0.0/14' : 'D',
           '80.0.0.0/01' : 'E',
           '40.0.0.0/02' : 'F',
           '0.0.0.0/02' : 'G'}


print("Welcome! to this simple routing simulator")
while True:
    raw = raw_input('> ')
    args = raw.split()
    if (args[0] == 'r'):
        print('Next Hop ' + entries[args[1]])
    elif (args[0] == 'a'):
        print('Adding ' + args[1])
        entries[args[1]] = args[2]
    elif (args[0] == 'd' and args[1] in entries):
        print('Deleting ' + args[1])
        del entries[args[1]]
    elif (args[0] == 'e'):
        print('Bye!')
        exit
