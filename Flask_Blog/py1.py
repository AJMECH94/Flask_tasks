import csv
import collections
with open('a.csv','r') as file:
    csvdata = csv.reader(file)
    data = list(csvdata)
duplicate = []
for i in data:
    if i not in duplicate:
        duplicate.append(i)

c = collections.defaultdict(int)
for i in duplicate:
    c[i[0]] += 1

for i in c.items():
    print(f"Areacode of {i[0]} having {i[1]} building ")




'''
d = [[('400102', 'b-1', 'india')], [('400102', 'b-2', 'india')], [('400102', 'b-2', 'india')], [('400103', 'b-1', 'india')]]

import collections
from collections import Counter
from itertools import chain
c1 = Counter(chain(*d))
c2 = []
for i in dict(c1).items():
    if i not in c2:
        c2.append(i)
print(c2)
'''


