from collections import defaultdict
from time import sleep


list_ids=list()
for id in range(697,699):
    list_ids.append(id)
#for test
#select_ids='run_id=620 OR run_id=62'
for id in list_ids:
    #select_ids="'run_id="+str(id)+"'"
    select_ids='run_id='+str(id)
    print(select_ids)