# -*- coding: utf-8 -*-

import cPickle
data=cPickle.load(open('data.pk'))
candidate=cPickle.load(open('candidate.pk'))
candidatn=cPickle.load(open('candidatn.pk'))
election=cPickle.load(open('election.pk'))
tags=cPickle.load(open('tags.pk'))
print 'okload'


from datetime import datetime
from json import dumps

from collections import Counter

co=Counter()
for d in data:
    if ( len(d['cs'])==2 and d['cs'][0] in candidatn and d['cs'][1] in candidatn
            and candidate[d['cs'][0]]=='4f16fe2299c7a10001000012' and
                candidate[d['cs'][0]]=='4f16fe2299c7a10001000012' and d['tag']):
        c1=candidatn[d['cs'][0]]
        c2=candidatn[d['cs'][1]]
        if c1<c2:
            co[(c1,c2,tags[d['tag']])]+=1
        else:
            co[(c2,c1,tags[d['tag']])]+=1

res=[]

for (c1,c2,tag),nb in dict(co).items():
    res.append([c1,c2,tag,nb])
with open('liens.json','w') as f:
        f.write(dumps(res))
        
with open('candidats.json','w') as f:
        f.write(dumps(map(lambda c:candidatn[c],filter(lambda c:candidate[c]=='4f16fe2299c7a10001000012',candidate.keys()))))
        
#import pprint
#for c in el,can,error,mois:
#    pprint.pprint(dict(c))

