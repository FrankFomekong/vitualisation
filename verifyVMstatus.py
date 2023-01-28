import os
import sys
out=os.popen('xl list')
out=out.read().split('\n')
#print(out)
if len(out)>=4:
	#print('====domU running===')
	print(1)
	sys.exit(1)
sys.exit(0)
print(0)
