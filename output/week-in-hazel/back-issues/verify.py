"""Check final outputs and byte-for-byte preservation of screenshot pixels."""
from pathlib import Path
from datetime import datetime,timezone
import json,re,hashlib
from PIL import Image
from pypdf import PdfReader
import pdfplumber
R=Path(__file__).resolve().parent;checks=[]
for e in json.loads((R/'selection.json').read_text()):
 m=json.loads((R/e['slug']/'copy.json').read_text());p=R.parents[1]/'pdf'/f"week-in-hazel-{e['slug']}.pdf";reader=PdfReader(p)
 assert len(reader.pages)==len(m['pages'])+1
 shot=Image.open(R/e['slug']/'assets/screenshot.png').convert('RGB');expected=shot.tobytes();matched=0;images=[];links=[];off=0;text=''
 with pdfplumber.open(p) as doc:
  for page in doc.pages:
   text+=(page.extract_text() or '')+'\n'
   off+=sum(c['x0']<-.1 or c['x1']>page.width+.1 or c['top']<-.1 or c['bottom']>page.height+.1 for c in page.chars)
 for page in reader.pages:
  for a in page.get('/Annots',[]):
   uri=a.get_object().get('/A',{}).get('/URI')
   if uri:assert uri.startswith('https://github.com/hazelgrove/hazel/');links.append(uri)
  for o in page['/Resources'].get('/XObject',{}).values():
   o=o.get_object()
   if o.get('/Subtype')!='/Image':continue
   size=(o['/Width'],o['/Height']);filters=str(o.get('/Filter'));assert 'DCTDecode' not in filters
   images.append({'pixels':size,'filters':filters})
   if size==shot.size:assert o.get_data()==expected;matched+=1
 assert matched==1 and off==0
 assert '\ufffd' not in text and not re.search(r'\b(TODO|TBD|PLACEHOLDER)\b',text)
 (R/e['slug']/'research/final-text.txt').write_text(text)
 checks.append({'issue':e['id'],'file':p.name,'pages':len(reader.pages),'words':len(text.split()),'links':len(links),'unique_links':len(set(links)),'offpage_characters':off,'exact_screenshot_pixels':True,'no_jpeg_images':True,'images':images,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
t=json.loads((R/'typesetting/metrics.json').read_text());assert all(not f['errors'] for f in t['files']);assert all(m['pretty']=='pretty' for f in t['files'] for m in f['measures'])
result={'verified_utc':datetime.now(timezone.utc).isoformat(),'pdf_checks':checks,'browser_typography':{'engine':t['engine'],'files':[{k:f[k] for k in ['name','comparison','errors']} for f in t['files']]}}
(R/'verification.json').write_text(json.dumps(result,indent=2))
for c in checks:print({k:v for k,v in c.items() if k not in ['images','sha256']})
