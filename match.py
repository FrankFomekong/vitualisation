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
tmp=result[sys.argv[1]]
if len(tmp)==1:
	print(result[sys.argv[1]][0])
else:
	tmstr=''
	for e in tmp:
		tmstr=tmstr+e+' '
	print(tmstr)
p.close()
