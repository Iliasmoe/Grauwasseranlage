import unittest
from copy import deepcopy
from dataclasses import asdict
from io import BytesIO
from math import sqrt
from pathlib import Path
import sys
from fastapi.testclient import TestClient
from openpyxl import load_workbook
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from web.backend.app import app, Project, evaluate, default_calendar, study_statistics

class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client=TestClient(app)
        cls.default=cls.client.get('/api/default').json()
    def payload(self): return deepcopy(self.default)
    def calculate(self,body):
        r=self.client.post('/api/evaluate',json=body); self.assertEqual(r.status_code,200,r.text); return r.json()
    def test_health_and_production_page(self):
        self.assertEqual(self.client.get('/api/health').json()['status'],'ok')
        r=self.client.get('/'); self.assertEqual(r.status_code,200); self.assertIn('id="root"',r.text)
        self.assertIn("default-src 'self'",r.headers['content-security-policy'])
    def test_exact_excel_reference(self):
        d=self.calculate(self.payload()); self.assertTrue(d['valid'])
        self.assertAlmostEqual(d['result']['used'],555.3897572,places=7)
        self.assertAlmostEqual(d['result']['npv'],-17797.8728210468,places=6)
        self.assertEqual(d['result']['overall'],'Rot')
        self.assertEqual(len(d['result']['daily']),365)
    def test_water_and_monthly_balance(self):
        d=self.calculate(self.payload()); r=d['result']
        self.assertAlmostEqual(r['used']+r['makeup'],r['demand'])
        self.assertAlmostEqual(r['used']+r['overflow']+r['storage_losses']+r['end_storage'],r['available'])
        self.assertAlmostEqual(sum(m['used'] for m in d['monthly']),r['used'])
        self.assertEqual(d['payments'][-1]['year'],20)
        self.assertAlmostEqual(d['payments'][-1]['cumulative'],r['npv'])
    def test_all_scenarios_and_sensitivities(self):
        body=self.payload(); d=self.calculate(body); p=Project()
        self.assertEqual(len(d['scenarios']),3); self.assertEqual(len(d['sensitivity']),12)
        for s in d['scenarios']+d['sensitivity']:
            expected=evaluate(p,body['calendar'],tuple(s['factors']))
            self.assertAlmostEqual(s['result']['npv'],expected['npv'])
            self.assertAlmostEqual(s['result']['used'],expected['used'])
    def test_no_greywater(self):
        b=self.payload()
        for p in b['project']['sources']: p['users']=0
        d=self.calculate(b); self.assertTrue(d['valid']); self.assertEqual(d['result']['used'],0); self.assertEqual(d['result']['resource'],'Rot')
    def test_no_demand(self):
        b=self.payload()
        for p in b['project']['demands']: p['users']=0
        d=self.calculate(b); self.assertTrue(d['valid']); self.assertEqual(d['result']['used'],0); self.assertEqual(d['result']['makeup'],0)
    def test_missing_input(self):
        b=self.payload(); b['project']['water_price']=None; d=self.calculate(b)
        self.assertFalse(d['valid']); self.assertIn('water_price',[e['path'] for e in d['errors']]); self.assertNotIn('result',d)
    def test_invalid_input(self):
        for key,value in [('water_price',-1),('year',2026.5),('horizon',51),('yield_rate',1.2),('discount','oops'),('users',True)]:
            with self.subTest(key=key):
                b=self.payload(); b['project'][key]=value; self.assertFalse(self.calculate(b)['valid'])
    def test_unknown_and_absent_fields(self):
        b=self.payload(); b['project']['secret']=42; self.assertFalse(self.calculate(b)['valid'])
        b=self.payload(); del b['project']['discount']; self.assertFalse(self.calculate(b)['valid'])
    def test_sewage_evidence_required(self):
        b=self.payload(); b['project']['sewage_credit']=1; self.assertFalse(self.calculate(b)['valid'])
        b['project']['billing_evidence']='Beleg 123 bestätigt Entlastung'; self.assertTrue(self.calculate(b)['valid'])
    def test_hygiene_gate(self):
        b=self.payload(); b['project']['equipment']=0; b['project']['planning']=0; b['project']['installation']=0; b['project']['extra_investment']=0; b['project']['replacement_cost']=0
        d=self.calculate(b); self.assertEqual(d['result']['economic'],'Grün'); self.assertEqual(d['result']['overall'],'Gelb')
        b['project']['hygiene']='Nicht erfüllt'; self.assertEqual(self.calculate(b)['result']['overall'],'Rot')
    def test_threshold_update(self):
        b=self.payload(); b['project']['resource_green']=.8; b['project']['resource_yellow']=.3
        self.assertEqual(self.calculate(b)['result']['resource'],'Rot')
        b['project']['resource_yellow']=.9; self.assertFalse(self.calculate(b)['valid'])
    def test_days_update(self):
        b=self.payload(); b['project']['sources'][0]['days']=100
        self.assertAlmostEqual(self.calculate(b)['result']['raw'],418.2)
    def test_profiles_cannot_exceed_calendar(self):
        b=self.payload(); b['project']['sources'][1]['days']=200; self.assertFalse(self.calculate(b)['valid'])
    def test_year_change_requires_new_calendar(self):
        b=self.payload(); b['project']['year']=2028; self.assertFalse(self.calculate(b)['valid'])
        c=self.client.get('/api/calendar/2028').json(); b.update(c)
        d=self.calculate(b); self.assertTrue(d['valid']); self.assertEqual(len(d['result']['daily']),366)
    def test_invalid_calendar_flags(self):
        for flags in [[1,0],[2,0,0],[True,0,0]]:
            b=self.payload(); b['calendar'][0]=flags; self.assertFalse(self.calculate(b)['valid'])
    def test_scenario_failure_is_local(self):
        for factors in [[1,1,1,1,1,-.1],[None,1,1,1,1,0],[11,1,1,1,1,0]]:
            b=self.payload(); b['scenarios'][0]['factors']=factors; d=self.calculate(b)
            self.assertTrue(d['valid']); self.assertFalse(d['scenarios'][0]['result']['valid']); self.assertTrue(d['scenarios'][1]['result']['valid'])
    def test_negative_cashflow_and_high_investment(self):
        b=self.payload(); b['project']['water_price']=0; d=self.calculate(b)
        self.assertLess(d['result']['cashflow'],0); self.assertIsNone(d['result']['static']); self.assertIsNone(d['result']['dynamic'])
        b['project']['equipment']=1e7; self.assertEqual(self.calculate(b)['result']['economic'],'Rot')
    def test_study_statistics(self):
        records=[{'id':'P1','ratings':[2]*7,'minutes':10,'mistakes':0},{'id':'P2','ratings':[4]*7,'minutes':20,'mistakes':2},{'id':'P3','ratings':['3']*7,'minutes':'abc','mistakes':1.5},{'id':'','ratings':[5]*7}]
        s=study_statistics(records)
        self.assertEqual(s['ratings'][0]['n'],2); self.assertEqual(s['ratings'][0]['mean'],3)
        self.assertAlmostEqual(s['ratings'][0]['std'],sqrt(2)); self.assertEqual(s['ratings'][0]['invalid'],1)
        self.assertEqual(s['mean_minutes'],15); self.assertEqual(s['mean_mistakes'],1); self.assertEqual(s['orphaned'],1)
    def test_empty_study_placeholder_is_not_orphaned(self):
        s=study_statistics([{'id':'','ratings':[None]*7,'tasks':['']*4,'minutes':None,'mistakes':None,'role':''}])
        self.assertEqual(s['orphaned'],0);self.assertEqual(s['count'],0)
    def test_duplicate_study_ids_reported(self):
        s=study_statistics([{'id':'P1','ratings':[1]},{'id':'P1','ratings':[3]}]); self.assertEqual(s['duplicates'],['P1'])
    def test_invalid_export_rejected(self):
        b=self.payload(); b['project']['water_price']=None
        self.assertEqual(self.client.post('/api/export/xlsx',json=b).status_code,422)
    def test_export_contains_actual_project_and_literal_text(self):
        b=self.payload(); b['project']['name']='=SUM(1,2)'; b['project']['water_price']=4.25
        b['scenarios'][0]['factors'][0]=1.5
        b['studies']=[{'id':'P001','ratings':[1,2,3,4,5,None,None],'comment':'=HYPERLINK("x")'}]
        r=self.client.post('/api/export/xlsx',json=b); self.assertEqual(r.status_code,200,r.text[:200] if r.status_code!=200 else '')
        self.assertIn('spreadsheetml',r.headers['content-type'])
        w=load_workbook(BytesIO(r.content))
        self.assertEqual(w['Eingaben']['B5'].value,'=SUM(1,2)'); self.assertEqual(w['Eingaben']['B5'].data_type,'s')
        self.assertEqual(w['Eingaben']['B36'].value,4.25); self.assertEqual(w['Szenarien']['B8'].value,1.5)
        self.assertEqual(w['Nutzertest']['F6'].value,1); self.assertEqual(w['Nutzertest']['R6'].data_type,'s')
        self.assertEqual(w['Kalender']['C5'].value,b['calendar'][0][0]); self.assertEqual(len(w._external_links),0)
    def test_document_allowlist(self):
        self.assertEqual(self.client.get('/api/documents/methodik').status_code,200)
        self.assertEqual(self.client.get('/api/documents/not-found').status_code,404)
    def test_api_schema_errors_and_size_limit(self):
        self.assertEqual(self.client.post('/api/evaluate',json={'project':{},'unexpected':1}).status_code,422)
        self.assertEqual(self.client.post('/api/evaluate',content='{}',headers={'content-length':'2000001','content-type':'application/json'}).status_code,413)
        b=self.payload(); b['studies']=[{'id':'P1','comment':{'invalid':True}}]
        self.assertEqual(self.client.post('/api/evaluate',json=b).status_code,422)

if __name__=='__main__':unittest.main(verbosity=2)
