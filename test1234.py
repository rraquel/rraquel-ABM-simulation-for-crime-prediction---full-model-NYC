from collections import defaultdict
from time import sleep

d=dict()
c=dict()
c['burglarycount']=0
c['robberycount']=0
c['larcenycount']=0
c['larcenyMotorcount']=0
c['assaultcount']=0
#tuple=(ctftus, crimecount, burglarycount, robberycount, larcenycount, larcenyMotorcount, assaultcount)
cts=[12, 15, 20]
for ct in cts:
    if not ct in d:
        d[ct]=c
    crimetype="'BURGLARY'"
    if crimetype=="'BURGLARY'":
        burglarycount=10
        d[ct]['burglarycount']+=burglarycount
        print(d[ct]['burglarycount'])
    if crimetype=="'BURGLARY'":
        burglarycount=15
        d[ct]['burglarycount']+=burglarycount
        print(d[ct]['burglarycount'])
print(d[12])