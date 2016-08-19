#!/usr/bin/env python

file = open('access.log', 'r')
d = dict()

for i in file:
    ip = i.split()[0]
    if ip not in d:
        d[ip]=1
    else:
        d[ip]+=1
result = sorted(d,key=d.get, reverse=True)[:11]

for r in result:
    print("%s - %s" % (r, d[r]))