# -*- coding: utf-8 -*-

from bson import decode_all
from data.reader import BSONInput
'''from pprint import pprint 
for s in ['candidacies','candidates','elections']:
    globals()[s]=decode_all(open('data/'+s+'.bson').read())
    pprint(globals()[s])'''


candidatn={}
candidate={}
candidat={}
election={}
for d in decode_all(open('data/candidates.bson').read()):
    candidat[str(d['_id'])]=(d['first_name'] or '')+' '+d['last_name']
for d in decode_all(open('data/candidacies.bson').read()):
    #if d['published']==True:
        candidatn[str(d['_id'])]=candidat[str(d['candidate_ids'][0])]
        candidate[str(d['_id'])]=str(d[u'election_id'])

for d in decode_all(open('data/elections.bson').read()):
    election[str(d['_id'])]=d['name']

tags={}
tagsname={}
for d in decode_all(open('data/tags.bson').read()):
    tagsname[str(d['_id'])]=d['name']


from collections import Counter
erreur=Counter()
from datetime import datetime
from json import dumps

co=Counter()
for d in BSONInput(open('data/events.bson'))._reads():
    if not d['tag_ids'] or not str(d['tag_ids'][0]) in tagsname:
         erreur['tag']+=1
    for c in (d['candidacy_ids'] or []):
        if str(c) not in candidate or str(c) not in candidatn:
            erreur['candidate']+=1
            
    if ( len(d['candidacy_ids'] or [])==2 and str(d['candidacy_ids'][0]) in candidatn and str(d['candidacy_ids'][1]) in candidatn
            and candidate[str(d['candidacy_ids'][0])]=='4f16fe2299c7a10001000012' and
                candidate[str(d['candidacy_ids'][1])]=='4f16fe2299c7a10001000012' ):
        c1=candidatn[str(d['candidacy_ids'][0])]
        c2=candidatn[str(d['candidacy_ids'][1])]
        if c1<c2:
            co[(c1,c2,d['updated_at'].strftime('%Y-%m-%d'))]+=1
        else:
            co[(c2,c1,d['updated_at'].strftime('%Y-%m-%d'))]+=1

res={}

for c1,c2,day in co:
    if '2011-12-20'<=day<='2012-05-10':
        if c1+' Vs '+c2 not in res:
            res[c1+' Vs '+c2]=[]
        res[c1+' Vs '+c2]+=[[day,co[(c1,c2,day)]]]

for v in res:
    res[v]=sorted(res[v])

with open('versus.json','w') as f:
        f.write(dumps(res))
        
with open('candidats.json','w') as f:
        f.write(dumps(list(set(candidatn.values()))))
        
#import pprint
#for c in el,can,error,mois:
#    pprint.pprint(dict(c))

