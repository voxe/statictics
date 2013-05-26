# -*- coding: utf-8 -*-

from bson import decode_all
from reader import BSONInput
from sys import getsizeof
import copy
'''
for s in ['candidacies','election_tags','propositions','tags','candidates','elections','events']:
    globals()[s]=decode_all(open(s+'.bson').read())
    print s,'loaded'
'''
data=[]
for d in BSONInput(open('events.bson'))._reads():
    datum={}
    for k in [u'candidacy_ids', u'user_driven', u'updated_at', u'ip_address', u'tag_ids', u'processed']:
        if k in d:
            datum[k]=d[k]
    data.append(datum)
    
   
print 'events',(
    getsizeof(data)+
    sum(getsizeof(d) for d in data)+
    sum(sum(getsizeof(d[k]) for k in d.keys()) for d in data)
)


