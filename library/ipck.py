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
module:
description:
 pruefen, ob zwie IP Adressen im gleichen Netz sind
 also die Interface Adresse und der GW
notes:
 Aufbau Quellfile
 {{ ContextName }};{{ interface.Nameif }};"{{ interface.Ip }}";"{{ route.NextHop }}";"{{ interface.Mask }}";"{{ route.Network }}";
author: Joerg Ullrich
version: 0.1
requirements:
options:

'''

EXAMPLES = '''

- ipck:
    logfile: "{{ sroute }}"
'''

RETURN = '''
changed:
    description:
    returned: always
    type: bool

'''

import sys
import re
import ipcalc



def netmask_to_cidr(netmask):
    return sum([bin(int(x)).count('1') for x in netmask.split('.')])

def main():

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
    CurrentLine = 0
    LastErrorLine = 0
    changed = True


    module = AnsibleModule(
        argument_spec=dict(
            logfile=dict(required=False)
        )
    )

    logfile = module.params['logfile']

    facts = {}
    try:
        with open ( logfile, 'r') as src_file:
            lines = src_file.readlines()
    except:
        module.fail_json(msg="cannot open ...")

    for line in lines:

        CurrentLine += 1
        matched = re.match(LINE, line)
        context, intf, ip1, ip2, mask, network = ( matched.groups())

        cidr = netmask_to_cidr(mask)
        ipaddr1 = ip1 + "/" + repr(cidr)
        ipaddr2 = ip2 + "/" + repr(cidr)

        network1 = ipcalc.Network(ipaddr1)
        network2 = ipcalc.Network(ipaddr2)
        if repr(network1.network()) != repr(network2.network()):
            messsage = "Line {}: INTF {} und GW {} nicht im gleichen Netz".format(CurrentLine, network1.network(), network2.network())
            module.fail_json(msg=messsage)

    messsage = "{} Zeile(n) getestet".format(CurrentLine)
    module.exit_json(changed=changed, msg=messsage, ansible_facts=facts)

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
