"""Echte Chromium-Nutzungsabläufe, Desktop/Mobil, Import/Export und Persistenz."""
from __future__ import annotations
import argparse, json, math, sys
from pathlib import Path
from io import BytesIO
from openpyxl import load_workbook
from playwright.sync_api import sync_playwright, expect
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'src'))
from model import Project,evaluate


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--url',default='http://127.0.0.1:8000');parser.add_argument('--browser',default='/usr/bin/chromium');parser.add_argument('--output',default='web/test-results');parser.add_argument('--html',help='HTML via Playwright an lokaler Testadresse ausliefern, alle anderen Anfragen sperren');args=parser.parse_args()
    output=ROOT/args.output;output.mkdir(parents=True,exist_ok=True)
    records=[]; errors=[]; external=[]
    def passed(name): records.append({'case':name,'status':'passed'});print('PASS',name,flush=True)
    def ready(page): expect(page.get_by_text('Tagesbilanz vollständig berechnet',exact=True)).to_be_visible(timeout=15000)
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path=args.browser,headless=True,args=['--no-sandbox'])
        context=browser.new_context(viewport={'width':1440,'height':1080},accept_downloads=True)
        def load_offline(ctx):
            if not args.html:return
            html=(ROOT/args.html).read_bytes()
            def route(r):
                if r.request.url.split('#')[0]==args.url:r.fulfill(body=html,content_type='text/html')
                else:external.append(r.request.url);r.abort()
            ctx.route('**/*',route);ctx.set_offline(True)
        load_offline(context)
        if args.url.startswith('file:'): context.set_offline(True)
        page=context.new_page()
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('console',lambda m:errors.append('console: '+m.text) if m.type=='error' else None)
        page.on('request',lambda r:external.append(r.url) if not r.url.startswith((args.url,'data:','about:')) else None)
        current='Start'
        try:
            page.goto(args.url,wait_until='networkidle');ready(page)
            expect(page.get_by_test_id('saved-water')).to_have_text('555 m³/a')
            expect(page.get_by_test_id('npv')).to_contain_text('-17.798')
            assert not page.evaluate('document.documentElement.scrollWidth>window.innerWidth')
            page.screenshot(path=str(output/'dashboard-desktop.png'),full_page=True)
            page.screenshot(path=str(output/'dashboard-preview.png'),full_page=False)
            passed('Dashboard stimmt mit Excel-Referenz überein')

            current='Diagrammumschaltung'
            page.get_by_role('button',name='Monat',exact=True).click()
            expect(page.get_by_role('img',name='Trinkwassereinsparung über 12 Zeitpunkte')).to_be_visible()
            page.get_by_role('button',name='Jährlich',exact=True).click()
            expect(page.get_by_role('img',name='Jährlicher Cashflow über 21 Zeitpunkte')).to_be_visible()
            passed('Monatsbilanz und jährlicher Cashflow umschaltbar')

            current='Profiländerung'
            page.get_by_role('button',name='Nutzungsprofile',exact=True).click()
            page.get_by_label('Nutzungstage Duschen Sporthalle',exact=True).fill('100');ready(page)
            page.get_by_role('button',name='Projektbewertung',exact=True).click()
            p=Project();p.sources[0].days=100
            expected=evaluate(p)
            expect(page.get_by_test_id('saved-water')).to_contain_text(str(round(expected['used'])))
            passed('Nutzungstage ändern Tagesrechnung und Dashboard')

            current='Wirtschaftliche Eingaben'
            page.get_by_role('button',name='Projekt & Anlage',exact=True).click()
            page.get_by_role('button',name='Wirtschaftlichkeit',exact=True).click()
            water=page.get_by_label('Vermiedener Trinkwasserpreis (€/m³)',exact=True)
            water.fill('4.25');ready(page)
            page.get_by_role('button',name='Projektbewertung',exact=True).click()
            p.water_price=4.25;expected=evaluate(p)
            displayed=page.get_by_test_id('npv').inner_text().replace('\xa0','').replace('€','').replace('.','').replace(',','.').strip()
            assert abs(float(displayed)-expected['npv'])<1
            passed('Preisänderung bis Kapitalwert durchgerechnet')

            current='Fehlende Eingabe'
            page.get_by_role('button',name='Projekt & Anlage',exact=True).click()
            water=page.get_by_label('Vermiedener Trinkwasserpreis (€/m³)',exact=True);water.fill('')
            expect(page.get_by_role('alert')).to_contain_text('Trinkwasserpreis')
            page.get_by_role('button',name='Projektbewertung',exact=True).click()
            expect(page.get_by_role('heading',name='Bewertung noch nicht möglich')).to_be_visible()
            expect(page.get_by_test_id('npv')).to_have_count(0)
            expect(page.get_by_role('button',name='Excel exportieren',exact=True)).to_be_disabled()
            page.get_by_role('button',name='Projekt & Anlage',exact=True).click()
            page.get_by_label('Vermiedener Trinkwasserpreis (€/m³)',exact=True).fill('4.25');ready(page)
            passed('Fehlender Wert sperrt Bewertung und Export; keine veralteten KPIs')

            current='Schwellenwerte'
            page.get_by_role('button',name='Methodik & KPIs',exact=True).click()
            page.get_by_label('Ressourcen: Grün ab',exact=True).fill('80')
            page.get_by_label('Ressourcen: Gelb ab',exact=True).fill('30');ready(page)
            page.get_by_role('button',name='Projektbewertung',exact=True).click()
            expect(page.locator('.assessment-categories>div').nth(1).get_by_text('Rot',exact=True)).to_be_visible()
            page.get_by_role('button',name='Methodik & KPIs',exact=True).click()
            page.get_by_label('Ressourcen: Grün ab',exact=True).fill('15');page.get_by_label('Ressourcen: Gelb ab',exact=True).fill('5');ready(page)
            passed('Schwellenänderung verändert Ressourcenampel')

            current='Szenarioänderung'
            page.get_by_role('button',name='Szenarien',exact=True).click()
            page.get_by_label('Konservativ: Investition',exact=True).fill('1.5');ready(page)
            scenario=evaluate(p,factors=(1.5,.9,.9,.8,1.2,.01))
            text=page.locator('.scenario-result>strong').first.inner_text().replace('\xa0','').replace('€','').replace('.','').replace(',','.').strip()
            assert abs(float(text)-scenario['npv'])<1
            page.get_by_label('Konservativ: Investition',exact=True).fill('');ready(page)
            expect(page.locator('.scenario-result').first).to_contain_text('Nicht bewertbar')
            expect(page.locator('.scenario-result').nth(1)).not_to_contain_text('Nicht bewertbar')
            page.get_by_label('Konservativ: Investition',exact=True).fill('1.5');ready(page)
            page.screenshot(path=str(output/'scenarios-desktop.png'),full_page=True)
            passed('Szenarien unabhängig konfigurierbar; ungültige Variante lokal gesperrt')

            current='Kalenderänderung'
            page.get_by_role('button',name='Tageskalender',exact=True).click()
            checkbox=page.get_by_label('Schule am 01.01.2026',exact=True)
            checkbox.uncheck();expect(page.get_by_role('alert')).to_contain_text('Profiltage')
            checkbox.check();ready(page)
            page.get_by_role('button',name='Zeitraum setzen',exact=True).click()
            dialog=page.get_by_role('dialog')
            dialog.get_by_label('Von',exact=True).fill('2026-01-02');dialog.get_by_label('Bis',exact=True).fill('2026-01-03')
            dialog.get_by_role('button',name='Zeitraum anwenden',exact=True).click()
            expect(page.get_by_role('alert')).to_contain_text('Profiltage')
            page.get_by_role('button',name='Beispielkalender neu erstellen',exact=True).click()
            page.get_by_role('dialog').get_by_role('button',name='Neu erstellen',exact=True).click();ready(page)
            passed('Einzeltage, Zeitraumänderung und Kalenderwiederherstellung')

            current='Probandenauswertung'
            page.get_by_role('button',name='Probandentest',exact=True).click()
            page.get_by_role('button',name='Erste Testperson erfassen',exact=True).click()
            dialog=page.get_by_role('dialog')
            dialog.get_by_label('Bearbeitungszeit (Minuten)',exact=True).fill('12.5')
            dialog.get_by_label('Beobachtete Fehlerzahl',exact=True).fill('2')
            for q in ['Verständlichkeit','Bedienbarkeit','Übersichtlichkeit','Rechenweg verständlich','Ampel verständlich','Fehlersicherheit','Praxistauglichkeit']:
                dialog.get_by_role('button',name=q+': 4',exact=True).click()
            dialog.get_by_role('button',name='Testergebnis speichern',exact=True).click();ready(page)
            expect(page.locator('.study-summary>div').first).to_contain_text('1 / 50')
            expect(page.locator('.study-summary>div').nth(1)).to_contain_text('12,5')
            expect(page.locator('.rating-result').first).to_contain_text('4,0 / 5')
            page.get_by_role('button',name='Bearbeiten',exact=True).click()
            page.get_by_role('dialog').get_by_role('button',name='Verständlichkeit: 2',exact=True).click()
            page.get_by_role('dialog').get_by_role('button',name='Testergebnis speichern',exact=True).click();ready(page)
            expect(page.locator('.rating-result').first).to_contain_text('2,0 / 5')
            with page.expect_download() as d:page.get_by_role('button',name='CSV exportieren',exact=True).click()
            d.value.save_as(str(output/'Probandenauswertung.csv'))
            assert 'P001' in (output/'Probandenauswertung.csv').read_text()
            passed('Probanden erfassen, bearbeiten, auswerten und CSV exportieren')

            current='JSON und Excel Export'
            with page.expect_download() as d:page.get_by_role('button',name='Projektdatei',exact=True).click()
            d.value.save_as(str(output/'Grauwasser_Projekt.json'))
            payload=json.loads((output/'Grauwasser_Projekt.json').read_text())
            assert payload['project']['water_price']==4.25 and payload['project']['sources'][0]['days']==100
            assert payload['scenarios'][0]['factors'][0]==1.5 and payload['studies'][0]['ratings'][0]==2
            with page.expect_download(timeout=60000) as d:page.get_by_role('button',name='Excel exportieren',exact=True).click()
            d.value.save_as(str(output/'Grauwasser_Bewertungstool.xlsx'))
            wb=load_workbook(output/'Grauwasser_Bewertungstool.xlsx')
            assert wb['Eingaben']['B36'].value==4.25 and wb['Nutzungsprofile']['F6'].value==100
            assert wb['Szenarien']['B8'].value==1.5 and wb['Nutzertest']['F6'].value==2
            passed('JSON- und Excel-Export enthalten tatsächliche Projekteingaben')

            current='Lokale Persistenz und JSON Import'
            page.reload(wait_until='networkidle');ready(page)
            page.get_by_role('button',name='Projektbewertung',exact=True).click()
            text=page.get_by_test_id('npv').inner_text().replace('\xa0','').replace('€','').replace('.','').replace(',','.').strip()
            assert abs(float(text)-expected['npv'])<1
            page.locator('input[type=file]').set_input_files(str(output/'Grauwasser_Projekt.json'));ready(page)
            expect(page.get_by_label('Aktives Projekt').locator('option')).to_have_count(2)
            passed('Projekte überleben Neuladen und lassen sich wieder importieren')

            current='Projektverwaltung'
            page.get_by_role('button',name='Neues Projekt',exact=True).click()
            dialog=page.get_by_role('dialog');dialog.get_by_label('Projektname',exact=True).fill('Webtest Schule Köln')
            dialog.get_by_label('Standort',exact=True).fill('Köln')
            dialog.get_by_role('button',name='Projekt anlegen',exact=True).click();ready(page)
            expect(page.get_by_label('Aktives Projekt').locator('option')).to_have_count(3)
            expect(page.get_by_label('Projektname',exact=True)).to_have_value('Webtest Schule Köln')
            page.get_by_role('button',name='Projektbewertung',exact=True).click()
            expect(page.get_by_test_id('saved-water')).to_have_text('555 m³/a')
            page.get_by_role('button',name='Projekt löschen',exact=True).click()
            page.get_by_role('dialog').get_by_role('button',name='Projekt löschen',exact=True).click();ready(page)
            expect(page.get_by_label('Aktives Projekt').locator('option')).to_have_count(2)
            page.get_by_role('button',name='Neues Projekt',exact=True).click();page.keyboard.press('Escape')
            expect(page.get_by_role('dialog')).to_have_count(0)
            passed('Projekte anlegen, wechseln, löschen; Dialog per Tastatur schließen')

            current='Fehlerhafter Import'
            page.locator('input[type=file]').set_input_files({'name':'wrong.json','mimeType':'application/json','buffer':b'{"version":1} '})
            expect(page.get_by_role('status')).to_contain_text('Keine gültige')
            expect(page.get_by_label('Aktives Projekt').locator('option')).to_have_count(2)
            passed('Fehlerhafter Import zerstört keine vorhandenen Projekte')

            current='Gesamtbegründung bei Nachweisveto'
            from web.backend.app import defaults
            proof=defaults()
            proof['project']['name']='Nachweisprüfung'
            for key in ['planning','equipment','installation','extra_investment','replacement_cost']:
                proof['project'][key]=0
            proof['project']['hygiene']='Nicht erfüllt'
            proof['project']['technical']=proof['project']['legal']='Nachgewiesen'
            fixture=json.dumps({'format':'grauwasser-web','version':1,**proof}).encode()
            page.locator('input[type=file]').set_input_files({'name':'proof.json','mimeType':'application/json','buffer':fixture});ready(page)
            expect(page.locator('.assessment-main h2')).to_have_text('Nachweis nicht erfüllt')
            expect(page.get_by_text('Keine Nettoinvestition; Amortisationsdauer nicht definiert.',exact=True)).to_be_visible()
            expect(page.locator('.assessment-categories>div').first.get_by_text('Grün',exact=True)).to_be_visible()
            expect(page.locator('.assessment-main').get_by_text('Rot',exact=True)).to_be_visible()
            passed('Nachweisveto wird bei günstiger Ökonomie korrekt begründet')

            current='Mobilansicht'
            mobile=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,device_scale_factor=1)
            load_offline(mobile)
            if args.url.startswith('file:'): mobile.set_offline(True)
            mp=mobile.new_page();mp.on('pageerror',lambda e:errors.append('mobile: '+str(e)))
            mp.goto(args.url,wait_until='networkidle');ready(mp)
            assert not mp.evaluate('document.documentElement.scrollWidth>window.innerWidth')
            expect(mp.get_by_test_id('saved-water')).to_have_text('555 m³/a')
            mp.screenshot(path=str(output/'dashboard-mobile.png'),full_page=True)
            mp.get_by_role('button',name='Navigation öffnen',exact=True).click()
            mp.get_by_role('button',name='Projekt & Anlage',exact=True).click()
            expect(mp.get_by_label('Projektname',exact=True)).to_be_visible()
            assert not mp.evaluate('document.documentElement.scrollWidth>window.innerWidth')
            mp.get_by_label('Projektname',exact=True).fill('Mobiles Testprojekt')
            ready(mp);mp.reload(wait_until='networkidle');ready(mp)
            expect(mp.get_by_label('Projektname',exact=True)).to_have_value('Mobiles Testprojekt')
            mobile.close();passed('Mobil 390 px: kein Seitenüberlauf, Navigation, Eingaben und Persistenz')
            assert not errors,errors
            assert not external,external
            passed('Keine Browserfehler und keine externen Laufzeit-Anfragen')
        except Exception as e:
            page.screenshot(path=str(output/'failure.png'),full_page=True)
            records.append({'case':current,'status':'failed','error':str(e)})
            raise
        finally:
            (output/'browser-results.json').write_text(json.dumps({'cases':records,'browser_errors':errors,'external_requests':external},ensure_ascii=False,indent=2)+'\n')
            browser.close()
    print(f'{len(records)} Browserabläufe bestanden.',flush=True)

if __name__=='__main__':main()
