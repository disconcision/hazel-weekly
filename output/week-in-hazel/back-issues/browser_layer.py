"""HTML paragraph layer with measured geometry and lossless PDF art composition."""
from pathlib import Path
import json,subprocess,os,hashlib,shutil
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from pypdf import PdfReader,PdfWriter

class BrowserLayer:
 def __init__(self,root,fonts):
  self.root=root;self.fonts=fonts;self.files=[];self.tmp=root.parents[2]/'tmp/pdfs/back-issues';self.tmp.mkdir(parents=True,exist_ok=True)
  (root/'typesetting').mkdir(exist_ok=True)
  p=root/'typesetting/metrics.json';self.old=json.loads(p.read_text()) if p.exists() else {'files':[]}
 def add_file(self,z,path):
  z.text_nodes=[];z.output_path=path;z.base_path=self.tmp/(path.stem+'-art.pdf');self.files.append(z);return z.base_path
 def add(self,z,kind,s,x,y,w,size,font,color,leading,maxh):
  idx=sum(n['page']==z.n for n in z.text_nodes);id=f'p{z.n}-n{idx}'
  n=dict(id=id,kind=kind,page=z.n,text=s,x=x,y=y,w=w,size=size,font=font,color=color,leading=leading,maxh=maxh,styleStudy='style-lab' in z.output_path.name)
  n['key']=hashlib.sha256(json.dumps([kind,s,w,size,font,leading],ensure_ascii=False).encode()).hexdigest()
  z.text_nodes.append(n)
  oldfile=next((f for f in self.old['files'] if f['name']==z.output_path.name),None)
  measured=next((v for v in oldfile['measures'] if v['id']==id and v.get('key')==n['key']),None) if oldfile else None
  if measured:return measured['h']
  st=ParagraphStyle('estimate',fontName=font,fontSize=size,leading=leading)
  _,h=Paragraph(s,st).wrap(w-(12 if kind=='drop' else 0),720);return h
 def finish(self):
  jobs=[]
  for z in self.files:jobs.append(dict(name=z.output_path.name,pages=z.n,nodes=z.text_nodes,textPDF=str(self.tmp/(z.output_path.stem+'-text.pdf'))))
  (self.root/'typesetting/layout.json').write_text(json.dumps({'fontDir':str(self.fonts),'files':jobs},indent=2))
  node=os.environ.get('HAZEL_ZINE_NODE') or os.environ.get('CODEX_PRIMARY_RUNTIME_NODE') or shutil.which('node')
  if not node:raise FileNotFoundError('Node not found; set HAZEL_ZINE_NODE')
  subprocess.run([node,str(self.root/'browser_typeset.cjs')],check=True)
  report=json.loads((self.root/'typesetting/metrics.json').read_text())
  if not os.environ.get('HAZEL_ZINE_MEASURED_PASS'):return report
  errors=[e for f in report['files'] for e in f['errors']]
  if errors:raise ValueError(f'Browser text exceeds its allocated area: {errors}')
  for z,job in zip(self.files,jobs):
   base=PdfReader(z.base_path);overlay=PdfReader(job['textPDF']);assert len(base.pages)==len(overlay.pages)==z.n
   writer=PdfWriter()
   for p,t in zip(base.pages,overlay.pages):p.merge_page(t);writer.add_page(p)
   writer.add_metadata({'/Title':f"Week in Hazel | Issue {z.meta['id']} | {z.meta['title']}", '/Author':'Astra (AI editor); ImageGen (illustrations)', '/Subject':z.meta['date']+'; retrospective edition, September 2026'})
   with z.output_path.open('wb') as out:writer.write(out)
  return report
