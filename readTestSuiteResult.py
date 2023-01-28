import ast
import sys

p=open('mapping.txt')
txt=p.readlines()
mix=""
for e in txt:
    mix=mix+e
#print(mix)
result = ast.literal_eval(mix)

# print result
#print("The converted dictionary is : " + str(result))

tmstr=''
tmp=result[sys.argv[1]]
if len(tmp)==1:
	tmstr=result[sys.argv[1]][0]
else:
	tmstr=''
	for e in tmp:
		tmstr=tmstr+e+' '
	#print(tmstr)
p.close()

featr=open('finalFeature.txt','a')


if sys.argv[2]=='1':
	p=open('testSuiteResult.txt','r')
	t=p.readlines()[0]
	p.close()
	if t=='0':
		featr.write(tmstr)
else:
		featr.write(' '+tmstr)
print(tmstr)
featr.close()
#ici on recoit deux arguments le fichier de config utilise pour lancer la vm et le un entier 1 pour dire de prendre en conte les resultat des tests suites et 0 pour dire de ne pas prendre en compte


