from collections import Counter
from json import dumps

candidatn={}
candidate={}
with open('candidacies.csv') as f:
    next(f)
    for l in f:
        li=l.split(',')
        candidatn[li[0]]=(li[3]+' '+li[4]).replace('"','').strip()
        candidate[li[0]]=li[1]

election={}
with open('elections.csv') as f:
    next(f)
    for l in f:
        li=l.split(',')
        election[li[0]]=li[1]

tags={}
with open('tags.csv') as f:
    next(f)
    for l in f:
        li=l.split(',')
        tags[li[0]]=li[1].strip(' \n"')

#print tags.values()

#for c in candidate:
#    print candidatn[c],election[candidate[c]]
    
from collections import Counter 
import re,time

reid='([0-9a-f]{24})'
redate='(20\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ)'
reip=re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
rcand=   re.compile(r'{ ""\$oid"" : ""'+reid+r'"" }')
reevent= re.compile(r'^((?:"\[.*]")|),(.*),(.*),((?:"\[.*]")|),(.*$)')

error=Counter()
nbcand=Counter()

nbelec=Counter()
nbcling=Counter()
badcand=Counter()

data=[]

with open('events.csv') as f:
    next(f)
    for l in f:
        m=reevent.search(l)
        if m:
            cs,date,ip,tag,cling=m.groups()
            
            cs=cs.strip('"[] ')
            if cs:
                cs=cs.split(',')
                if None in map(lambda x: rcand.search(x),cs):
                    error['badmatch cands']+=1
                    #print 'badmatch cands',l,
                    continue
                else:
                    cs=map(lambda x: rcand.search(x).groups()[0],cs)
                if filter(lambda x : x not in candidate,cs):
                    error['bad candidate']+=1
                    #print 'bad candidacie',l,
                    badcand[cs[0]]+=1
                    continue
                else:
                    nbelec[election[candidate[cs[0]]]]+=1
            else:
                cs=[]
            nbcand[len(cs)]+=1
            tag=tag.strip('"[] ')
            if tag:
                if not rcand.search(tag):
                    error['badmatch tag']+=1
                    #print 'badmatch tag',l,
                    continue
                else:
                    tag=rcand.search(tag).groups()[0]
                    if tag not in tags:
                        error['tag notin tags']+=1
                        print 'tag notin tags',tag
                        continue
            else:
                error['notag']+=1
                tag=''
            date=time.strptime(date,'%Y-%m-%dT%H:%M:%SZ')
            nbcling[cling]+=1
            if ip:
                ip=ip.strip('"')
                if not reip.match(ip):
                    print ip     
            data.append({'cs':cs,'date':int(time.strftime('%s',date)),'ip':ip,'tag':tag,'cling':cling})
                
        else:
            error['pasmatch']+=1
            #print 'notmatch',l,
            continue

print 'saving'
import cPickle
cPickle.dump(data,open('data.pk','w'))
cPickle.dump(candidate,open('candidate.pk','w'))
cPickle.dump(candidatn,open('candidatn.pk','w'))
cPickle.dump(election,open('election.pk','w'))
cPickle.dump(tags,open('tags.pk','w'))
        
import pprint
for c in error,nbcand,nbcling,badcand:
    pprint.pprint(dict(c))
