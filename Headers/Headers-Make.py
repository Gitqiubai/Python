import re
import os
import json
#-----------------------------------------------
#headers.txt文件保存地址，可根据自身需求改动位置
desktop=os.path.join(os.path.expanduser("~"), 'Desktop')+'/headers.txt'
#-----------------------------------------------
F=open(desktop,'r')
heders={}
for each in F:
    N=[]
    N=re.split(':', each,1)
    heders.setdefault(N[0],N[1].replace('\n','').replace(' ',''))
#print(heders)

print(json.dumps(heders, sort_keys=True, indent=4, separators=(',', ': ')))


F.close()



