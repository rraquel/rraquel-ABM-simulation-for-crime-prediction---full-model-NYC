
c=set()
c.update('a', 'b', 'c', '33', '678', '395', '5896')
agent=[1, 2, 3, 4]
len(list([item for sublist in (map(list(c) ,agent)) for item in sublist]))