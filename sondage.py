# -*- coding: utf-8 -*-

import locale
locale.setlocale(locale.LC_TIME,'fr_FR.utf8')
from datetime import datetime
from json import dumps

sondages=[]
for l in open('sondage3.csv'):
    v=l.split('\t')
    if len(v)>2:
        d={}
        mois=v[0].split(' ')[0]
        jour=int(v[2].split(' ')[0])
        d['date']=datetime.strptime('-'.join([str(jour),mois,'2012']),'%d-%B-%Y').strftime('%Y-%m-%d')
        d['institut']=v[1]        
        d['echantillon']=int(v[3].replace('.','').replace('¹','').replace(' ','').replace(' ','').split(',')[0])
        d['val']=[]
        for r in v[5].split('|'):
            s=r.split(' ')
            if len(s)>1:
                if s[0]:
                    d['val'].append([s[0],float(s[1].replace(',','.'))])
                elif s[1]:
                    if len(s)>2:
                        d['val'].append([s[1],float(s[2].replace(',','.'))])
                    else:
                        print s
                        d['val'].append([s[1],0.0])
        sondages.append(d)   


with open('sondages.json','w') as f:
        f.write(dumps(sondages)) 


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
co=Counter()
for d in BSONInput(open('data/events.bson'))._reads():
    if not d['tag_ids'] or not str(d['tag_ids'][0]) in tagsname:
         erreur['tag']+=1
    for c in (d['candidacy_ids'] or []):
        if str(c) not in candidate or str(c) not in candidatn:
            erreur['candidate']+=1
            
    if d['candidacy_ids']:
      for c in d['candidacy_ids']:
         if str(c) in candidate and candidate[str(c)]=='4f16fe2299c7a10001000012':
            co[(candidatn[str(c)],d['updated_at'].strftime('%Y-%m-%d'))]+=1

res={}

for c,day in co:
    if '2011-12-20'<=day<='2012-05-10':
        if c not in res:
            res[c]=[]
        res[c]+=[[day,co[(c,day)]]]

for v in res:
    res[v]=sorted(res[v])

with open('sondage.json','w') as f:
        f.write(dumps(res))  

