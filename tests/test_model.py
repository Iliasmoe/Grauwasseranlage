import unittest
from copy import deepcopy
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from model import Project, Profile, evaluate, default_calendar


def simple(raw=1,need=2,investment=100,waterprice=2,horizon=10):
    p=Project(); p.sources=[Profile('Quelle','Individuell',1,1,raw*1000,365)]; p.demands=[Profile('WC','Individuell',1,1,min(need,1)*1000,365)]
    # Spezifische Menge max. 1000 L; größere Bedarfe über Nutzerzahl abbilden.
    p.demands[0].users=need if need>1 else 1
    p.yield_rate=p.availability=p.overlap=1; p.storage=0; p.storage_loss=0; p.capacity=100
    p.planning=p.installation=p.extra_investment=p.grant=0; p.equipment=investment
    p.maintenance=p.other_cost=p.energy_intensity=0; p.water_price=waterprice
    p.sewage_credit=p.discount=p.water_growth=p.cost_growth=p.energy_growth=p.sewage_growth=0
    p.replacement_year=p.replacement_cost=p.residual=0; p.horizon=horizon; p.other_water=0
    p.hygiene=p.technical=p.legal='Nachgewiesen'
    return p,[(0,0,1)]*365

class ReferenceTests(unittest.TestCase):
    def test_no_greywater(self):
        p,c=simple(raw=0); r=evaluate(p,c); self.assertEqual(r['used'],0); self.assertEqual(r['resource'],'Rot')
    def test_no_demand(self):
        p,c=simple(need=0); r=evaluate(p,c); self.assertEqual(r['used'],0); self.assertEqual(r['makeup'],0)
    def test_supply_below_demand_hand_reference(self):
        p,c=simple(); r=evaluate(p,c)
        self.assertEqual(r['raw'],365); self.assertEqual(r['demand'],730); self.assertEqual(r['used'],365)
        self.assertEqual(r['makeup'],365); self.assertEqual(r['npv'],7200); self.assertEqual(r['static'],100/730)
    def test_supply_above_demand_hand_reference(self):
        p,c=simple(raw=1,need=.5); r=evaluate(p,c)
        self.assertEqual(r['used'],182.5); self.assertEqual(r['overflow'],182.5); self.assertEqual(r['quota'],1)
    def test_high_investment(self):
        p,c=simple(investment=1e7); self.assertEqual(evaluate(p,c)['economic'],'Rot')
    def test_negative_net_cashflow(self):
        p,c=simple(waterprice=0); p.maintenance=100
        r=evaluate(p,c); self.assertIsNone(r['static']); self.assertIsNone(r['dynamic']); self.assertLess(r['cashflow'],0)
    def test_payback_within_horizon(self):
        p,c=simple(investment=1460); r=evaluate(p,c)
        self.assertEqual(r['static'],2); self.assertEqual(r['dynamic'],2); self.assertTrue(r['stable_recovery'])
    def test_payback_outside_horizon(self):
        p,c=simple(investment=14600); r=evaluate(p,c)
        self.assertEqual(r['static'],20); self.assertIsNone(r['dynamic'])
    def test_missing(self):
        for field in ['water_price','horizon','year','name','yield_rate']:
            with self.subTest(field=field):
                p=Project(); setattr(p,field,None); self.assertFalse(evaluate(p)['valid'])
    def test_invalid(self):
        for field,value in [('water_price',-1),('yield_rate',1.1),('horizon',3.5),('discount','x'),('resource_green',None)]:
            with self.subTest(field=field):
                p=Project(); setattr(p,field,value); self.assertFalse(evaluate(p)['valid'])
    def test_unknown_hygiene(self):
        p,c=simple(); p.hygiene='Ungeklärt'; r=evaluate(p,c); self.assertEqual(r['overall'],'Gelb')
    def test_hygiene_not_met_cannot_be_compensated(self):
        p,c=simple(); p.hygiene='Nicht erfüllt'; self.assertEqual(evaluate(p,c)['overall'],'Rot')
    def test_threshold_changes(self):
        p=Project(); a=evaluate(p); p.resource_green=.8; p.resource_yellow=.3; b=evaluate(p)
        self.assertEqual(a['resource'],'Grün'); self.assertEqual(b['resource'],'Rot')
    def test_days_change(self):
        p=Project(); a=evaluate(p); p.sources[0].days=100; b=evaluate(p)
        self.assertLess(b['raw'],a['raw']); self.assertLess(b['used'],a['used'])
    def test_scenarios(self):
        p=Project(); base=evaluate(p); high=evaluate(p,factors=(.8,1.1,1.1,1.2,.8,-.01)); low=evaluate(p,factors=(1.2,.9,.9,.8,1.2,.01))
        self.assertLess(low['npv'],base['npv']); self.assertGreater(high['npv'],base['npv'])
    def test_independent_discount_reference(self):
        p,c=simple(investment=1000); p.discount=.05; r=evaluate(p,c)
        annuity=730*(1-(1.05)**-10)/.05
        self.assertAlmostEqual(r['npv'],-1000+annuity,places=8)
    def test_storage_and_temporal_reference(self):
        p,c=simple(raw=1,need=1); p.sources[0].group='Schulbetrieb'; p.sources[0].days=1
        p.demands[0].group='Halle'; p.demands[0].days=1; p.storage=1; p.overlap=0; p.storage_loss=.1
        c=[(1,0,0),(0,1,0)]+[(0,0,0)]*363; r=evaluate(p,c)
        self.assertAlmostEqual(r['used'],.9); self.assertAlmostEqual(r['storage_losses'],.1); self.assertAlmostEqual(r['makeup'],.1)
    def test_old_water_is_discarded(self):
        p,c=simple(); p.sources[0].days=1; p.demands[0].days=1; p.sources[0].group='Schulbetrieb'; p.demands[0].group='Halle'
        p.storage=1; p.overlap=0; c=[(1,0,0),(0,0,0),(0,1,0)]+[(0,0,0)]*362
        self.assertEqual(evaluate(p,c)['used'],0)
    def test_invariants(self):
        p=Project(); r=evaluate(p)
        self.assertAlmostEqual(r['available'],r['used']+r['overflow']+r['storage_losses']+r['end_storage'],places=8)
        self.assertAlmostEqual(r['demand'],r['used']+r['makeup'],places=8)
        for row in r['daily']:
            self.assertGreaterEqual(row['used'],0); self.assertLessEqual(row['used'],row['demand']+1e-8)
    def test_zero_rate(self):
        p,c=simple(); self.assertEqual(evaluate(p,c)['npv'],7200)
    def test_grant_and_zero_investment(self):
        p,c=simple(); p.grant=100; r=evaluate(p,c); self.assertEqual(r['net_investment'],0); self.assertEqual(r['economic'],'Grün')
        p.grant=101; self.assertFalse(evaluate(p,c)['valid'])
    def test_sewage_billing_guard(self):
        p=Project(); a=evaluate(p); p.sewage_credit=1; self.assertFalse(evaluate(p)['valid'])
        p.billing_evidence='Beleg 123: bestätigter variabler Nachlass'; b=evaluate(p); self.assertGreater(b['avoided'],a['avoided'])
    def test_replacement_can_reverse_payback(self):
        p,c=simple(investment=730); p.replacement_year=3; p.replacement_cost=10000
        r=evaluate(p,c); self.assertEqual(r['dynamic'],1); self.assertFalse(r['stable_recovery']); self.assertLess(r['npv'],0)
    def test_end_inventory_is_not_used(self):
        p,c=simple(raw=1,need=0); p.sources[0].days=1; p.storage=1; p.overlap=0
        c=[(0,0,0)]*364+[(0,0,1)]; r=evaluate(p,c)
        self.assertEqual(r['end_storage'],1); self.assertEqual(r['used'],0)
    def test_leap_year(self):
        p=Project(); p.year=2028; r=evaluate(p); self.assertTrue(r['valid']); self.assertEqual(len(r['daily']),366)
    def test_invalid_scenario(self):
        self.assertFalse(evaluate(Project(),factors=(1,1,1,1,1,-.04))['valid'])

if __name__=='__main__': unittest.main(verbosity=2)
