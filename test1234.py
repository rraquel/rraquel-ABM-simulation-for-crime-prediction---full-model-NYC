from collections import defaultdict

a=dict()
c=dict()
b=defaultdict(dict)


c[3]=30
c[4]=40

a[55]=c
print(a)
temp=a[55]
temp[10]=20
a[55]=temp
print(temp)
print(a)

print(a[55][10])

b[1]=10
b[2]=20



print(a)
print(c)
