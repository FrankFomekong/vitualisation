import os
import glob
import subprocess
res=open('testSuiteResult.txt','w')

def testSuiteStatus():
	"check test suite status"
	try:
		p=open("/mnt/nfs_share/test.txt")
		t=p.readlines()
		p.close()
		taille=len(t)
		print(t[taille-1])
		if t[taille-1]=="make[1]: Leaving directory '/mnt/nfs_clientshare/postgresql-12.0/src/test/regress'\n":
			print('=======================finish test =========================')
			return True,t[taille-4] 
		else:
			print('=======================test pending =========================')
			return False,""
	except:
		return False,""
	
files=glob.glob("myvm1*.cfg")
#print(files)
tmp1=False
tmp2=""
#for e in files:
#	p=os.popen("./launchVm.sh ./"+str(e))

while True:
	tmp1,tmp2=testSuiteStatus()
	if tmp1==True:
		print(tmp2)
		if tmp2==' All 192 tests passed. \n':
			#print(tmp2)
			res.write("1")
		else :
			res.write("0")
		res.close()
		break
