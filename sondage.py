# -*- coding: utf-8 -*-

res=[]
for l in open('sondage3.csv'):
    v=l.split('\t')
    if len(v)>2:
        d={}
        d['mois']=v[0].split(' ')[0]
        d['institut']=v[1]
        d['jour']=int(v[2].split(' ')[0])
        d['echantillon']=int(v[3].replace('.','').replace('¹','').replace(' ','').replace(' ','').split(',')[0])
        d['dik']={}
        for r in v[5].split('|'):
            s=r.split(' ')
            if len(s)>1:
                if s[0]:
                    d['dik'][s[0]]=float(s[1].replace(',','.'))
                elif s[1]:
                    if len(s)>2:
                        d['dik'][s[1]]=float(s[2].replace(',','.'))
                    else:
                        d['dik'][s[1]]=0.0
        res.append(d)   
               
print res
