file1=open("myvm.cfg",'r')
file2=open("configCPUID",'r')

filecontent=file1.readlines()
filecontent2=file2.readlines()

file1txt=""
for e in filecontent:
	file1txt=file1txt+e
#print(file1txt)
Beg='''\ncpuid="'''
end='''"\n'''
i=1
for e in filecontent2:
	tmp=file1txt+Beg+(e.replace('\n',''))+end
	f=open("./conf/myvm1"+str(i)+".cfg",'w')
	f.write(tmp)
	i=i+1


file1.close()
file2.close()
