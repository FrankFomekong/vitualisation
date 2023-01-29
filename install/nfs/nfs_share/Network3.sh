ip link set eth0 up 
ip addr add 192.168.1.102/24 dev eth0 
ip route add 192.168.1.0/24 dev eth0 
ip route add default via 192.168.1.101 dev eth0 
mount $1:/mnt/nfs_share /mnt/nfs_clientshare
/mnt/nfs_clientshare/main >features.txt

