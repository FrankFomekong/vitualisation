#nfs config
apt-get update -y
apt install nfs-kernel-server
cp nfs/nfs_share -r /mnt
chown -R nobody:nogroup /mnt/nfs_share/
chmod 777 /mnt/nfs_share/ -R
cp nfs/exports /etc/
exportfs -a
systemctl restart nfs-kernel-server
ufw allow from any to any port nfs
ufw enable
#config du service
chmod +x service/Network.sh
cp service/Network.sh /root/
cp service/networkxen.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable networkxen.service
source /root/Network.sh

