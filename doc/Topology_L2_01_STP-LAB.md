# Topology_L2_01_STP-LAB

## STP LAB

Start mit Ctrl+B, also initialer Konfiguration

### server-1

Initiale Konfigration

    lo: 127.0.0.1
    eth0: 10.255.0.166/16
    eth1: 10.0.0.1/16
    gw: 10.255.0.1

#### Anpassung Routing

alt:

    content: |-
      #!/bin/sh
      ifconfig eth1 up 10.0.0.1 netmask 255.255.0.0
      route add -net 10.0.0.0/16 gw 10.0.0.2 dev eth1
      route add -net 192.168.0.0/30 gw 10.0.0.2 dev eth1
      exit 0
