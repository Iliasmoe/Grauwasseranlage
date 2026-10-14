"""Unabhängige Python-Referenz des dokumentierten Tages-/Kapitalwertmodells."""
from dataclasses import dataclass, field
from datetime import date, timedelta
from math import isfinite

@dataclass
class Profile:
    name: str
    group: str
    users: float
    frequency: float
    liters: float
    days: int

@dataclass
class Project:
    name: str = 'OGS mit Sporthalle – RECHENBEISPIEL'
    building: str = 'Offene Ganztagsschule mit Sporthalle'
    location: str = 'Beispielstandort – keine realen Projektdaten'
    plant: str = 'Modellanlage – Herstellerdaten ergänzen'
    users: int = 300
    year: int = 2026
    horizon: int = 20
    other_water: float = 1500
    yield_rate: float = .9
    availability: float = .95
    capacity: float = 5
    storage: float = 2
    overlap: float = .7
    storage_loss: float = .02
    hygiene: str = 'Ungeklärt'
    technical: str = 'Ungeklärt'
    legal: str = 'Ungeklärt'
    evidence: str = 'Projektbezogene Nachweise fehlen; kein Freigabenachweis.'
    planning: float = 3000
    equipment: float = 15000
    installation: float = 5000
    extra_investment: float = 2000
    grant: float = 0
    maintenance: float = 450
    energy_intensity: float = 1.0
    energy_price: float = .3
    other_cost: float = 120
    water_price: float = 2.5
    sewage_price: float = 2.2
    sewage_credit: float = 0
    discount: float = .03
    water_growth: float = .02
    cost_growth: float = .02
    energy_growth: float = .02
    replacement_year: int = 10
    replacement_cost: float = 4000
    residual: float = 0
    sewage_growth: float = .02
    billing_evidence: str = 'Keine bestätigte Gebührenentlastung; Ansatz 0 %.'
    data_status: str = 'Beispieldaten'
    resource_green: float = .15
    resource_yellow: float = .05
    economic_green: float = 0
    economic_yellow: float = -.2
    sources: list = field(default_factory=lambda: [
        Profile('Duschen Sporthalle','Halle',120,.6,25,280),
        Profile('Handwaschbecken Schule','Schulbetrieb',300,3,1,190),
        Profile('Handwaschbecken Halle','Halle',120,2,1,280),
        Profile('Weitere zulässige Quelle 1','Individuell',0,0,0,0),
        Profile('Weitere zulässige Quelle 2','Individuell',0,0,0,0),
        Profile('Weitere zulässige Quelle 3','Individuell',0,0,0,0)])
    demands: list = field(default_factory=lambda: [
        Profile('WC Schule','Schulbetrieb',300,3,4.5,190),
        Profile('WC Halle','Halle',120,1.5,4.5,280),
        Profile('Urinale Halle','Halle',80,1,1,280),
        Profile('Weitere zulässige Nutzung 1','Individuell',0,0,0,0),
        Profile('Weitere zulässige Nutzung 2','Individuell',0,0,0,0),
        Profile('Weitere zulässige Nutzung 3','Individuell',0,0,0,0)])

# Zeilen im Blatt Eingaben; gemeinsam für Generator und Testeingaben, nicht für Formeln.
INPUT_ROWS = {
'name':5,'building':6,'location':7,'plant':8,'users':9,'year':10,
'horizon':11,'other_water':12,'yield_rate':15,'availability':16,'capacity':17,
'storage':18,'overlap':19,'storage_loss':20,'hygiene':21,'technical':22,
'legal':23,'evidence':24,'planning':27,'equipment':28,'installation':29,
'extra_investment':30,'grant':31,'maintenance':32,'energy_intensity':33,
'energy_price':34,'other_cost':35,'water_price':36,'sewage_price':37,
'sewage_credit':38,'discount':39,'water_growth':40,'cost_growth':41,
'energy_growth':42,'replacement_year':43,'replacement_cost':44,'residual':45,
'sewage_growth':46,'billing_evidence':47,'data_status':48}

def default_calendar(year):
    """190 ausgewählte Schultage, 280 Hallentage; fiktiv, keine Ferienquelle."""
    n=(date(year+1,1,1)-date(year,1,1)).days
    days=[date(year,1,1)+timedelta(days=i) for i in range(n)]
    excluded=lambda d: d.month in (7,8) or (d.month==12 and d.day>=21)
    school=[i for i,d in enumerate(days) if d.weekday()<5 and not excluded(d)][:190]
    hall=[i for i,d in enumerate(days) if not (d.month==12 and d.day>=21)][:280]
    return [(int(i in school),int(i in hall),0) for i in range(n)]

def validate(p, calendar):
    errors=[]
    integer={'users','year','horizon','replacement_year'}
    bounds={'users':(0,1e6),'year':(2020,2100),'horizon':(1,50),
            'other_water':(0,1e7),'yield_rate':(0,1),'availability':(0,1),
            'capacity':(0,1e5),'storage':(0,1e5),'overlap':(0,1),
            'storage_loss':(0,1),'sewage_credit':(0,1),'discount':(0,1),
            'water_growth':(-.5,1),'cost_growth':(-.5,1),
            'energy_growth':(-.5,1),'sewage_growth':(-.5,1),
            'replacement_year':(0,50)}
    for k in INPUT_ROWS:
        v=getattr(p,k)
        if k in ('name','building','location','plant','evidence','billing_evidence'):
            if not isinstance(v,str) or not v.strip(): errors.append(k)
        elif k in ('hygiene','technical','legal'):
            if v not in ('Ungeklärt','Nachgewiesen','Nicht erfüllt'): errors.append(k)
        elif k=='data_status':
            if v not in ('Beispieldaten','Projektdaten'): errors.append(k)
        else:
            lo,hi=bounds.get(k,(0,1e9))
            if (not isinstance(v,(int,float)) or not isfinite(v) or
                not lo<=v<=hi or (k in integer and v!=int(v))): errors.append(k)
    if errors: return errors
    if p.grant>sum([p.planning,p.equipment,p.installation,p.extra_investment]): errors.append('grant')
    if p.replacement_year>p.horizon: errors.append('replacement_year')
    if p.replacement_cost>0 and p.replacement_year==0: errors.append('replacement_year')
    if p.sewage_credit>0 and p.billing_evidence.startswith('Keine bestätigte'): errors.append('billing_evidence')
    if not (all(isinstance(x,(int,float)) and isfinite(x) for x in [p.resource_yellow,p.resource_green]) and 0<=p.resource_yellow<=p.resource_green<=1): errors.append('resource thresholds')
    if not (all(isinstance(x,(int,float)) and isfinite(x) for x in [p.economic_yellow,p.economic_green]) and -1<=p.economic_yellow<=p.economic_green<=1): errors.append('economic thresholds')
    expected=(date(p.year+1,1,1)-date(p.year,1,1)).days
    if len(calendar)!=expected or any(len(row)!=3 or any(x not in (0,1) for x in row) for row in calendar):
        errors.append('calendar'); return errors
    counts={g:sum(row[i] for row in calendar) for i,g in enumerate(('Schulbetrieb','Halle','Individuell'))}
    for item in p.sources+p.demands:
        vals=[item.users,item.frequency,item.liters,item.days]
        if item.group not in counts or not item.name or any(not isinstance(v,(int,float)) or not isfinite(v) for v in vals):
            errors.append('profile'); continue
        if not (0<=item.users<=1e6 and 0<=item.frequency<=100 and 0<=item.liters<=1000 and 0<=item.days<=366 and item.days==int(item.days)):
            errors.append('profile'); continue
        if item.users*item.frequency*item.liters*item.days>0 and item.days>counts[item.group]: errors.append('profile days')
    return errors

def evaluate(p, calendar=None, factors=(1,1,1,1,1,0)):
    if not isinstance(p.year,(int,float)) or not isfinite(p.year) or p.year!=int(p.year) or not 2020<=p.year<=2100:
        return {'valid':False,'errors':['year'],'overall':'Nicht bewertbar'}
    calendar=calendar if calendar is not None else default_calendar(int(p.year))
    errors=validate(p,calendar)
    if errors: return {'valid':False,'errors':errors,'overall':'Nicht bewertbar'}
    invest,water_factor,demand_factor,supply_factor,op_factor,rate_delta=factors
    rate=p.discount+rate_delta
    if any(not isinstance(v,(int,float)) or not isfinite(v) or not 0<=v<=10 for v in factors[:5]) or not 0<=rate<=1:
        return {'valid':False,'errors':['scenario'],'overall':'Nicht bewertbar'}
    groups=('Schulbetrieb','Halle','Individuell')
    counts=[sum(row[i] for row in calendar) for i in range(3)]
    def daily(profiles,flags,scale):
        amount=0
        for item in profiles:
            idx=groups.index(item.group)
            if counts[idx]: amount+=item.users*item.frequency*item.liters*item.days/1000*flags[idx]/counts[idx]
        return amount*scale
    tank=0.; totals={k:0. for k in ('raw','demand','processed','available','used','makeup','overflow','storage_losses')}
    records=[]
    for flags in calendar:
        raw=daily(p.sources,flags,supply_factor)
        need=daily(p.demands,flags,demand_factor)
        processed=min(raw,p.capacity)*p.availability
        available=processed*p.yield_rate
        start=tank*(1-p.storage_loss)
        from_tank=min(start,need)
        direct=min(available*p.overlap,max(0,need-from_tank))
        end=min(p.storage,max(0,available-direct))
        row={'raw':raw,'demand':need,'processed':processed,'available':available,
             'used':from_tank+direct,'makeup':need-from_tank-direct,
             'overflow':max(0,available-direct-end),
             'storage_losses':tank*p.storage_loss+start-from_tank,'end':end}
        records.append(row)
        for k in totals: totals[k]+=row[k]
        tank=end
    gross=sum([p.planning,p.equipment,p.installation,p.extra_investment])*invest
    grant=min(p.grant,gross)
    net=gross-grant
    energy=totals['processed']*p.energy_intensity
    costs=(p.maintenance+p.other_cost+energy*p.energy_price)*op_factor
    avoided=totals['used']*(p.water_price*water_factor+p.sewage_price*p.sewage_credit)
    cf=avoided-costs
    flow=[-net]
    disc=[-net]
    pv_cost=net
    pv_volume=0
    for t in range(1,p.horizon+1):
        benefit=totals['used']*(p.water_price*water_factor*(1+p.water_growth)**(t-1)+p.sewage_price*p.sewage_credit*(1+p.sewage_growth)**(t-1))
        op=((p.maintenance+p.other_cost)*(1+p.cost_growth)**(t-1)+energy*p.energy_price*(1+p.energy_growth)**(t-1))*op_factor
        replacement=p.replacement_cost*invest*(1+p.cost_growth)**(t-1) if t==p.replacement_year else 0
        residual=p.residual*invest if t==p.horizon else 0
        flow.append(benefit-op-replacement+residual)
        disc.append(flow[-1]/(1+rate)**t)
        pv_cost+=(op+replacement-residual)/(1+rate)**t
        pv_volume+=totals['used']/(1+rate)**t
    npv=sum(disc)
    dynamic=None
    cumulative=-net
    for t,x in enumerate(disc[1:],1):
        if cumulative<0 and cumulative+x>=0 and dynamic is None: dynamic=t-1-cumulative/x
        cumulative+=x
    # Erste Rückgewinnung und Stabilität nach Ersatzinvestition getrennt ausweisen.
    stable_recovery=net>0 and dynamic is not None and min(sum(disc[:t+1]) for t in range(int(dynamic)+1,len(disc)))>=-1e-8
    baseline=totals['demand']+p.other_water
    quota=totals['used']/baseline if baseline else 0
    cover=totals['used']/totals['demand'] if totals['demand'] else 0
    econ=(1 if npv>=0 else 3) if net==0 else (1 if npv/net>=p.economic_green else 2 if npv/net>=p.economic_yellow else 3)
    resource=3 if totals['used']<=0 else 1 if quota>=p.resource_green else 2 if quota>=p.resource_yellow else 3
    gate=3 if 'Nicht erfüllt' in (p.hygiene,p.technical,p.legal) else 2 if 'Ungeklärt' in (p.hygiene,p.technical,p.legal) else 1
    labels={1:'Grün',2:'Gelb',3:'Rot'}
    return dict(valid=True,**totals,end_storage=tank,gross=gross,net_investment=net,
                costs=costs,avoided=avoided,cashflow=cf,npv=npv,quota=quota,cover=cover,
                utilization=totals['used']/totals['raw'] if totals['raw'] else 0,
                specific_cost=pv_cost/pv_volume if pv_volume else None,
                static=net/cf if cf>0 and net>0 else None,dynamic=dynamic,
                stable_recovery=stable_recovery,economic=labels[econ],resource=labels[resource],
                overall=labels[max(econ,resource,gate)],gate=labels[gate],
                flows=flow,discounted=disc,daily=records)
