#!/usr/bin/python

import json
from pprint import pprint
import ast
import sys

f = sys.argv[1]
# print f
cdplog = "cfg/" + f + "/cdp.log"
# print cdplog

with open(cdplog, 'r') as elist:
    CdpLists = ast.literal_eval(elist.read())
    # rtr1 = dict(cdp = daten)
    # pprint(rtr1)
    #print json.dumps(rtr1)

for CdpList in CdpLists:
    print CdpList['local_interface'], CdpList['neighbor'], CdpList['neighbor_interface']
    #print "\nbla"
