"""Validate final PDF structure and that clean UI plates embed exact native pixels."""
from pathlib import Path
from datetime import datetime,timezone
import json,re,hashlib
from PIL import Image
from pypdf import PdfReader
import pdfplumber
R=Path(__file__).resolve().parent;out=R.parent/'pdf';checks=[]
plates={}
for f in (R/'assets').glob('*-clean.png'):
 im=Image.open(f).convert('RGB');assert Image.open(f).format=='PNG'
 plates[im.size]=(f.name,im.tobytes())
for name,count,treatment in [('week-in-hazel-001.pdf',11,'clean'),('week-in-hazel-001-woodcut.pdf',11,'woodcut'),('week-in-hazel-001-style-lab.pdf',4,'clean')]:
 path=out/name;reader=PdfReader(path);assert len(reader.pages)==count
 images=[];links=[];text='';offpage=0;matched=[]
 with pdfplumber.open(path) as p:
  for page in p.pages:
   text+=(page.extract_text() or '')+'\n'
   offpage+=sum(c['x0']<-.1 or c['x1']>page.width+.1 or c['top']<-.1 or c['bottom']>page.height+.1 for c in page.chars)
 for page in reader.pages:
  for ann in page.get('/Annots',[]):
   a=ann.get_object().get('/A',{});uri=a.get('/URI')
   if uri:assert uri.startswith('https://');links.append(uri)
  for key,value in page['/Resources'].get('/XObject',{}).items():
   o=value.get_object()
   if o.get('/Subtype')!='/Image':continue
   size=(o['/Width'],o['/Height']);filters=str(o.get('/Filter'));images.append({'width':size[0],'height':size[1],'filter':filters})
   assert 'DCTDecode' not in filters, f'Unexpected JPEG in {name}'
   if treatment=='clean' and size in plates:
    f,expected=plates[size];actual=o.get_data();assert actual==expected,f'Native pixels changed in {name}: {f}';matched.append(f)
 if treatment=='clean':
  expected=set(f for f,_ in plates.values())
  if 'style-lab' in name:expected -= {'probes-cards-clean.png','constellation-score-clean.png'}
  assert set(matched)==expected
 assert offpage==0
 assert '\ufffd' not in text and not re.search(r'\b(TODO|TBD|PLACEHOLDER)\b',text)
 checks.append({'file':name,'pages':count,'words':len(text.split()),'links':len(links),'unique_links':len(set(links)),'offpage_characters':offpage,'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'lossless_image_filters':True,'exact_native_clean_plates':matched,'images':images})
result={'revision':3,'verified_utc':datetime.now(timezone.utc).isoformat(),'metric_reproduction':'Weekly snapshot unchanged from verified revision 1; new open backlog query saved separately.','pdf_checks':checks}
(R/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
for c in checks:print({k:v for k,v in c.items() if k not in ['images','sha256']})
