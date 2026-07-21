#!/usr/bin/env python3
"""Extrae contacto (WhatsApp / telefono / email / link de reservas) de la BIO de un perfil de IG.

Uso: python3 scripts/ig_contact.py <ig_handle>   -> imprime JSON {handle,email,phone,whatsapp,booking,bio}

Muchos negocios (nail techs, barberos, spas) ocultan el telefono en Booksy pero SI ponen su
WhatsApp/telefono/email o un link de reservas en la bio de Instagram. Este script renderiza el
perfil con Playwright local (IP residencial, confiable) y saca:
- bio (texto del header) -> regex de email y telefono US
- links del perfil -> wa.me / api.whatsapp (numero de WhatsApp), mailto, tel, linktree/booksy/glossgenius
NUNCA inventa nada: solo devuelve lo que el perfil publica. IG rate-limitea bursts: espaciar.
"""
import json
import os
import re
import subprocess
import sys

VENV_PY = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.venv-pw', 'bin', 'python'))

_DRIVER = r'''
import sys, json, re
from playwright.sync_api import sync_playwright
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
h=sys.argv[1]
out={'handle':h,'email':'','phone':'','whatsapp':'','booking':'','bio':'','login_wall':False}
with sync_playwright() as p:
    b=p.chromium.launch(headless=True, args=['--no-sandbox'])
    pg=b.new_page(user_agent=UA, viewport={'width':1280,'height':1600})
    pg.goto(f'https://www.instagram.com/{h}/', wait_until='domcontentloaded', timeout=45000)
    pg.wait_for_timeout(2800)
    data=pg.evaluate("""() => {
      const metaDesc=(document.querySelector('meta[property=\"og:description\"]')||{}).content||'';
      let bio='';
      const hs=document.querySelector('header section');
      if(hs) bio=hs.innerText||'';
      const links=[...document.querySelectorAll('a')].map(a=>a.href).filter(Boolean);
      const login=!!document.querySelector('input[name=\"username\"]');
      return {metaDesc, bio, links, login};
    }""")
    b.close()
out['login_wall']=bool(data.get('login'))
bio=(data.get('bio') or '')
meta=(data.get('metaDesc') or '')
# la og:description trae la bio entre comillas al final normalmente
mq=re.search(r':\s*"?(.+)"?\s*$', meta.replace('\n',' '))
text=(bio+' '+ (mq.group(1) if mq else meta))
out['bio']=(bio or meta)[:400]
links=data.get('links') or []
# email
m=re.search(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', text)
if m: out['email']=m.group(0)
for l in links:
    if l.startswith('mailto:') and not out['email']:
        out['email']=l.replace('mailto:','').split('?')[0]
# whatsapp (wa.me / api.whatsapp.com/send?phone=)
for l in links:
    mm=re.search(r'(?:wa\.me/|whatsapp\.com/send\?phone=|whatsapp\.com/)(\+?\d{7,15})', l)
    if mm: out['whatsapp']=mm.group(1); break
# booking / link en bio
for l in links:
    if re.search(r'booksy\.com|glossgenius\.com|linktr\.ee|linktree|vagaro\.com|square\.site|calendly', l):
        out['booking']=l.split('?')[0]; break
# telefono US en el texto (o desde tel:)
for l in links:
    if l.startswith('tel:') and not out['phone']:
        out['phone']=l.replace('tel:','')
if not out['phone']:
    mp=re.search(r'(\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}', text)
    if mp: out['phone']=mp.group(0)
if out['whatsapp'] and not out['phone']:
    out['phone']=out['whatsapp']
print(json.dumps(out))
'''


def fetch_contact(handle):
    handle = handle.lstrip('@').strip('/')
    driver = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_ig_contact_driver.py')
    with open(driver, 'w') as f:
        f.write(_DRIVER)
    out = subprocess.run([VENV_PY, driver, handle], capture_output=True, text=True, timeout=90)
    try:
        return json.loads(out.stdout.strip().splitlines()[-1])
    except Exception:
        return {'handle': handle, 'email': '', 'phone': '', 'whatsapp': '', 'booking': '', 'bio': '', '_err': out.stderr[-200:]}


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    print(json.dumps(fetch_contact(sys.argv[1]), ensure_ascii=False, indent=1))
