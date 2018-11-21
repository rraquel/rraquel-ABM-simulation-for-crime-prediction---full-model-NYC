from collections import defaultdict
from time import sleep


pWeightList=[0.2, 0.3, 0.4, 0.05]
spweight=sum(pWeightList)
while (spweight)!= 1:
    val=min(pWeightList)
    print(val)
    idx=pWeightList.index(val)
    print(idx)
    rest=1-spweight
    print(round(rest,2))
    pWeightList[idx]=val+rest
print(pWeightList)