echo '======================== installation script start ====================================================='
#nfs config
echo '======================= install and configure nfs ======================================================'
apt-get update -y
apt install nfs-kernel-server
cp nfs/nfs_share -r /mnt
chown -R nobody:nogroup /mnt/nfs_share/
chmod 777 /mnt/nfs_share/ -R
cp nfs/exports /etc/
exportfs -a
echo '======================== enable nfs  and firewall ==================================================================='
systemctl restart nfs-kernel-server
ufw allow from any to any port nfs
ufw enable
echo '===================== nfs installation and configuration finished ==================================================================='

#config du service
echo '======================== create and enable service network for xen VM ==============================================================='

chmod +x service/Network.sh
cp service/Network.sh /root/
cp service/networkxen.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable networkxen.service
source /root/Network.sh

echo '======================== sevice enabled ==================================================================='
echo '======================== installtion completed ==================================================================='

