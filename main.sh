xl destroy myvm
rm /mnt/nfs_share/features.txt
rm /mnt/nfs_share/test.txt
xl create myvm.cfg
while [ ! -f "/mnt/nfs_share/features.txt" ]
do
echo '====waiting vm features====='
done
python3 count.py >configCPUID
python3 genFile.py
xl destroy  myvm
source loop.sh 
rm /mnt/nfs_share/features.txt
rm /mnt/nfs_share/test.txt
echo '================ execution terminee consulter la liste des features necessaires trouvee dans le fichier finalFeature.txt ==========='
