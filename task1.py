#!/usr/bin/env python

keys = ['key1', 'key2', 'key3', 'key4']
values = [1, 2, 3]

print(dict(zip(keys, values + [None] * (len(keys) - len(values)))))



