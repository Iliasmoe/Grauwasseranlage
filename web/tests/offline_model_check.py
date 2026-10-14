"""Differentialprüfung der echten Browsermodell-Quelle gegen die Python-Referenz."""
import json, math, random, subprocess, sys
from dataclasses import asdict
from pathlib import Path
from copy import deepcopy
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests'))
from web.backend.app import EvaluationInput, compute, defaults, study_statistics
from test_model import simple
cases=[]
def add(name, data): cases.append({'name':name,'data':data,'expected':compute(EvaluationInput(**data))})
base=defaults();add('Basis',base)
for year in [2020,2024,2028,2100]:
    d=defaults();d['project']['year']=year;d['calendar_year']=year
    from src.model import default_calendar
    d['calendar']=default_calendar(year);add('Kalender '+str(year),d)
for name,kwargs in [('Ohne Anfall',{'raw':0}),('Ohne Bedarf',{'need':0}),('Handreferenz',{}),('Überschuss',{'need':.5}),('Hohe Investition',{'investment':1e7}),('Nulltarif',{'waterprice':0}),('Amortisation',{'investment':1460}),('Späte Amortisation',{'investment':14600})]:
    p,c=simple(**kwargs);d=deepcopy(base);d['project']=asdict(p);d['calendar']=c;add(name,d)
for key,value in [('water_price',None),('horizon',None),('year',None),('name',None),('yield_rate',None),('water_price',-1),('yield_rate',1.1),('horizon',3.5),('discount','x'),('resource_green',None),('hygiene','Nicht erfüllt'),('grant',30000),('sewage_credit',1),('replacement_year',0),('economic_yellow',.5),('resource_yellow',.5)]:
    d=deepcopy(base);d['project'][key]=value;add(key+' '+str(value),d)
for name in ['Speicherübertrag','Altwasser','Restbestand','Ersatz kippt Amortisation','Förderung 100%','Gebührennachweis','Profil fehlt','Profil zu viele Tage','Kalenderlänge','Kalenderflags','Falsches Kalenderjahr','Fehlendes Feld','Unbekanntes Feld','Leeres Szenario','Negativer Szenariozins','Studien']:
    d=deepcopy(base)
    if name in ['Speicherübertrag','Altwasser','Restbestand','Ersatz kippt Amortisation','Förderung 100%']:
        p,c=simple(raw=1,need=1);p.storage=1;p.overlap=0;p.sources[0].days=p.demands[0].days=1;p.sources[0].group='Schulbetrieb';p.demands[0].group='Halle'
        c=[(1,0,0),(0,1,0)]+[(0,0,0)]*363
        if name=='Speicherübertrag':p.storage_loss=.1
        if name=='Altwasser':c=[(1,0,0),(0,0,0),(0,1,0)]+[(0,0,0)]*362
        if name=='Restbestand':c=[(0,0,0)]*364+[(1,0,0)]
        if name=='Ersatz kippt Amortisation':p,c=simple(investment=730);p.replacement_year=3;p.replacement_cost=10000
        if name=='Förderung 100%':p,c=simple();p.grant=100
        d['project']=asdict(p);d['calendar']=c
    if name=='Gebührennachweis':d['project'].update(sewage_credit=1,billing_evidence='Bescheid 123')
    if name=='Profil fehlt':d['project']['sources'][0].pop('days')
    if name=='Profil zu viele Tage':d['project']['sources'][0]['days']=366
    if name=='Kalenderlänge':d['calendar']=d['calendar'][:-1]
    if name=='Kalenderflags':d['calendar'][0]=[2,1,0]
    if name=='Falsches Kalenderjahr':d['calendar_year']=2025
    if name=='Fehlendes Feld':d['project'].pop('water_price')
    if name=='Unbekanntes Feld':d['project']['unknown']=2
    if name=='Leeres Szenario':d['scenarios'][0]['factors'][0]=None
    if name=='Negativer Szenariozins':d['scenarios'][0]['factors'][5]=-.04
    if name=='Studien':d['studies']=[{'id':'P001','ratings':[1,2,3,4,5,None,8],'minutes':12,'mistakes':2,'tasks':['Erfüllt','Teilweise']},{'id':'P002','ratings':[5,4,3,2,1,True,'bad'],'minutes':14.5,'mistakes':4},{'id':'P001','ratings':[3]*7,'minutes':-1,'mistakes':2.5},{'id':'','ratings':[None]*7,'tasks':['']*4},{'id':'','role':'Ohne Zuordnung'}]
    add(name,d)
rng=random.Random(941)
for i in range(60):
    d=deepcopy(base);p=d['project']
    p.update(yield_rate=rng.random(),availability=rng.random(),capacity=rng.randrange(0,9),storage=rng.randrange(0,6),overlap=rng.random(),storage_loss=rng.random(),water_price=rng.uniform(0,10),discount=rng.uniform(0,.15),water_growth=rng.uniform(-.1,.15),cost_growth=rng.uniform(-.1,.15),energy_growth=rng.uniform(-.1,.15),equipment=rng.randrange(0,30001),grant=0)
    p['sources'][0]['days']=rng.randrange(0,281);p['demands'][0]['days']=rng.randrange(0,191)
    p['hygiene']=rng.choice(['Nachgewiesen','Nicht erfüllt','Ungeklärt'])
    add('Zufall '+str(i),d)
source=ROOT/'web/frontend/src/model.ts'
runner="import {readFileSync} from 'node:fs'; import {compute} from "+json.dumps(source.as_uri())+"; console.log(JSON.stringify(JSON.parse(readFileSync(0,'utf8')).map(c=>compute(c.data))));"
proc=subprocess.run(['node','--experimental-strip-types','--input-type=module','-e',runner],input=json.dumps(cases),text=True,capture_output=True)
assert proc.returncode==0,proc.stderr
actual=json.loads(proc.stdout)
comparisons=0
def compare(a,b,path=''):
    global comparisons
    if isinstance(b,dict):
        for key in b:
            if key=='errors':continue # Genaue Fehlertexte dürfen lokal hilfreicher formuliert sein.
            assert key in a,(path,key);compare(a[key],b[key],path+'.'+key)
    elif isinstance(b,list):
        assert len(a)==len(b),(path,len(a),len(b))
        for i,(x,y) in enumerate(zip(a,b)):compare(x,y,path+'.'+str(i))
    elif isinstance(b,(int,float)) and not isinstance(b,bool):assert isinstance(a,(int,float)) and math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-7),(path,a,b);comparisons+=1
    else:assert a==b,(path,a,b);comparisons+=1
for c,a in zip(cases,actual):compare(a,c['expected'],c['name'])
# Dezimale Beträge und Kapazitäten direkt gegen das wissenschaftliche Modell;
# die ältere API behandelt einige historisch ganzzahlige Defaults strenger.
from model import Project, evaluate, default_calendar
fractional=[]
for i in range(12):
    p=Project();p.capacity=1.125+i*.375;p.storage=.125+i*.25;p.equipment=15000.55+i*.15;p.other_water=1500.75
    fractional.append({'name':'Dezimalwerte '+str(i),'data':{'project':asdict(p),'calendar':default_calendar(p.year)},'expected':evaluate(p)})
runner="import {readFileSync} from 'node:fs'; import {evaluate} from "+json.dumps(source.as_uri())+"; console.log(JSON.stringify(JSON.parse(readFileSync(0,'utf8')).map(c=>evaluate(c.data.project,c.data.calendar))));"
proc=subprocess.run(['node','--experimental-strip-types','--input-type=module','-e',runner],input=json.dumps(fractional),text=True,capture_output=True);assert proc.returncode==0,proc.stderr
for c,a in zip(fractional,json.loads(proc.stdout)):compare(a,c['expected'],c['name'])
report={'status':'passed','cases':len(cases)+len(fractional),'value_comparisons':comparisons,'reference':'src/model.py + web/backend/app.py','tolerance':{'relative':1e-9,'absolute':1e-7},'names':[c['name'] for c in cases+fractional]}
(ROOT/'web/validation-results/offline-model-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='names'},ensure_ascii=False))
