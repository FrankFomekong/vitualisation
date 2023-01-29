iptables --flush
iptables --table nat --flush
iptables --delete-chain
iptables --table nat --delete-chain
iptables --table nat --append POSTROUTING --out-interface wlp3s0 -j MASQUERADE
iptables --append FORWARD --in-interface xenbr0 -j ACCEPT
echo 1 > /proc/sys/net/ipv4/ip_forward
