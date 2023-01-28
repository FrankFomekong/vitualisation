import sys
p=sys.argv[1]
fle=open("tmpflags.txt",'w')
fle.write(' '+str(p))
fle.close()
