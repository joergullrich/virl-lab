#!/usr/bin/python

'''
Copyright 2016 Joerg Ullrich <joerg.ullrich@gmx.de>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

'''

'''
 pruefen, ob zwie IP Adressen im gleichen Netz sind
 also die Interface Adresse und der GW

 Aufbau Quellfile
 {{ ContextName }};{{ interface.Nameif }};"{{ interface.Ip }}";"{{ route.NextHop }}";"{{ interface.Mask }}";"{{ route.Network }}";

'''

import sys
import re
import ipcalc

f =  sys.argv[1]
CONTEXT = r'(\w+)'
INTF = r'(\w+)'
IPv4 = r'(\d+\.\d+\.\d+\.\d+)'
NETWORK = r'(\d+\.\d+\.\d+\.\d+\s\d+\.\d+\.\d+\.\d+)'
DELIMITER = r';'
LINE = (CONTEXT + DELIMITER +
        INTF + DELIMITER  +
        IPv4 + DELIMITER +
        IPv4 + DELIMITER +
        IPv4 + DELIMITER +
        NETWORK)


def netmask_to_cidr(netmask):
    return sum([bin(int(x)).count('1') for x in netmask.split('.')])

with open ( f, 'r') as src_file:
    lines = src_file.readlines()

LineNr = 1

for line in lines:
    matched = re.match(LINE, line)

    context, intf, ip1, ip2, mask, network = ( matched.groups())
    cidr = netmask_to_cidr(mask)
    ipaddr1 = ip1 + "/" + repr(cidr)
    ipaddr2 = ip2 + "/" + repr(cidr)

    network1 = ipcalc.Network(ipaddr1)
    network2 = ipcalc.Network(ipaddr2)
    if network1.network() == network2.network():
        # print "{} gleich {}".format(network1.network(), network2.network())
        error = 0
    else:
        # print "{} nicht gleich {}".format(network1.network(), network2.network())
        error = LineNr

    LineNr += 1

print "Fehler in Zeile {}".format(LineNr)
