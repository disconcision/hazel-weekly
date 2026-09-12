"""Typeset the pilot and two art-direction studies. Run with bundled Python."""
from pathlib import Path
import json, random, math, re, os, sys, subprocess
from browser_layer import BrowserLayer
from xml.sax.saxutils import escape
from html import unescape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from PIL import Image
ROOT=Path(__file__).resolve().parent; ASSETS=ROOT/'assets'; OUT=ROOT.parents[1]/'pdf'; OUT.mkdir(exist_ok=True)
def font_dir():
 candidates=[]
 if os.environ.get('HAZEL_ZINE_FONT_DIR'):candidates.append(Path(os.environ['HAZEL_ZINE_FONT_DIR']))
 if os.environ.get('CODEX_PRIMARY_RUNTIME_ROOT'):
  candidates.extend(Path(os.environ['CODEX_PRIMARY_RUNTIME_ROOT']).glob('**/fonts/truetype'))
 candidates.append(Path('/Users/andrewblinn/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/libreoffice-headless/libreoffice/LibreOfficeDev.app/Contents/Resources/fonts/truetype'))
 required={'LinLibertine_R_G.ttf','LinLibertine_RB_G.ttf','LinLibertine_RI_G.ttf','Rubik-Regular.ttf','Rubik-Bold.ttf','LiberationMono-Regular.ttf'}
 for candidate in candidates:
  if candidate.is_dir() and required.issubset(p.name for p in candidate.iterdir()):return candidate
 raise FileNotFoundError('Week in Hazel fonts not found; set HAZEL_ZINE_FONT_DIR')
F=font_dir()
for name,filename in [('Serif','LinLibertine_R_G.ttf'),('SerifBold','LinLibertine_RB_G.ttf'),('SerifItalic','LinLibertine_RI_G.ttf'),('Sans','Rubik-Regular.ttf'),('SansBold','Rubik-Bold.ttf'),('Mono','LiberationMono-Regular.ttf')]: pdfmetrics.registerFont(TTFont(name,str(F/filename)))
pdfmetrics.registerFontFamily('Serif',normal='Serif',bold='SerifBold',italic='SerifItalic',boldItalic='SerifBold')
pdfmetrics.registerFontFamily('Sans',normal='Sans',bold='SansBold',italic='Sans',boldItalic='SansBold')
W,H=540,720; M=36; CW=W-2*M
PAPER='#F3EBDD'; INK='#222A23'; GREEN='#355B43'; RED='#BB3E27'; MUTED='#6C7267'; PALE='#DCE2CC'; LINE='#B6B9A7'
LAYER=BrowserLayer(ROOT,F)
pages=[]; textlog=[]
class Zine:
 def __init__(self,path,meta,treatment='retrospective'):
  self.meta=meta;self.assets=ROOT/meta['slug']/'assets'
  base_path=LAYER.add_file(self,path);self.c=canvas.Canvas(str(base_path),pagesize=(W,H)); self.c.setTitle('Week in Hazel | Issue '+meta['id']+' | '+meta['date']);self.c.setAuthor('Week in Hazel - edited by Astra for Andrew Blinn');self.n=0;self.path=path;self.treatment=treatment
 def rect(self,x,y,w,h,fill,stroke=None,lw=.5):
  c=self.c;c.setFillColor(HexColor(fill));c.setStrokeColor(HexColor(stroke or fill));c.setLineWidth(lw);c.rect(x,H-y-h,w,h,fill=1,stroke=bool(stroke))
 def line(self,x1,y1,x2,y2,color=INK,lw=1):
  c=self.c;c.setStrokeColor(HexColor(color));c.setLineWidth(lw);c.line(x1,H-y1,x2,H-y2)
 def sketch_line(self,x1,y1,x2,y2,color=GREEN,lw=.85):
  c=self.c;c.saveState();c.setStrokeColor(HexColor(color));c.setLineWidth(lw);c.setLineCap(1)
  dx=x2-x1;dy=y2-y1;length=max(1,math.hypot(dx,dy));bend=min(.65,length/80)
  p=c.beginPath();p.moveTo(x1,H-y1)
  p.curveTo(x1+dx*.34-dy/length*bend,H-(y1+dy*.34+dx/length*bend),x1+dx*.7+dy/length*bend,H-(y1+dy*.7-dx/length*bend),x2,H-y2)
  c.drawPath(p,stroke=1);c.restoreState()
 def paper_patch(self,x,y,w,h,fill,fold=10,grain=True):
  # Uneven printed scraps: cut angles and nicked edges, rather than tidy page curls.
  c=self.c;c.saveState();rng=random.Random(int(x*53+y*37+w*11+h*7))
  rough=fold>0;amplitude=min(2.8,h*.07) if rough else .25
  left_tilt=rng.uniform(-1.6,1.6) if rough else 0
  right_tilt=-left_tilt+rng.uniform(-1.3,1.3) if rough else 0
  pts=[]
  for i in range(13):
   t=i/12;pts.append((x+w*t,y+left_tilt*(1-t)+right_tilt*t+rng.uniform(-amplitude,amplitude)))
  for i in range(1,5):pts.append((x+w+rng.uniform(-amplitude,amplitude),y+h*i/4))
  for i in range(1,14):
   t=1-i/13;pts.append((x+w*t,y+h-left_tilt*(1-t)-right_tilt*t+rng.uniform(-amplitude,amplitude)))
  for i in range(1,5):pts.append((x+rng.uniform(-amplitude,amplitude),y+h*(1-i/5)))
  def polygon(points,color,alpha=1):
   c.setFillColor(HexColor(color));c.setFillAlpha(alpha);p=c.beginPath();p.moveTo(points[0][0],H-points[0][1])
   for xx,yy in points[1:]:p.lineTo(xx,H-yy)
   p.close();c.drawPath(p,stroke=0,fill=1)
  polygon([(xx+1.2,yy+.8) for xx,yy in pts],INK,.12);polygon(pts,fill)
  if grain:
   rng=random.Random(int(x*53+y*37+w*11+h*7))
   c.setStrokeColor(HexColor(PAPER if fill==INK else INK));c.setStrokeAlpha(.19 if fill==INK else .115)
   for _ in range(int(w*h/95)):
    xx=rng.uniform(x+2,x+w-2);yy=rng.uniform(y+2,y+h-2)
    c.setLineWidth(rng.uniform(.14,.4));c.line(xx,H-yy,min(x+w-2,xx+rng.uniform(.4,3.8)),H-yy+rng.uniform(-.2,.2))
  if rough:
   c.setStrokeColor(HexColor(INK));c.setStrokeAlpha(.25);c.setLineWidth(.4)
   for edge in [pts[:13],pts[17:30]]:
    for i in range(0,len(edge)-1,3):
     ax,ay=edge[i];bx,by=edge[i+1];c.line(ax,H-ay,bx,H-by)
  c.restoreState()
 def ink_bar(self,x,y,w,h,fill):
  # Keep data boundaries exact; distress only the interior ink.
  if h<=0:return
  self.rect(x,y,w,h,fill);c=self.c;c.saveState();c.setStrokeColor(HexColor(PAPER));c.setStrokeAlpha(.17)
  rng=random.Random(int(x*19+y*29+h*7))
  for _ in range(int(w*h/44)):
   xx=rng.uniform(x+.8,x+w-1.8);yy=rng.uniform(y+.5,y+h-.5)
   c.setLineWidth(.22);c.line(xx,H-yy,xx+rng.uniform(.4,1.5),H-yy)
  c.restoreState()
 def text(self,s,x,y,size=11,font='Serif',color=INK):
  self.c.setFont(font,size);self.c.setFillColor(HexColor(color));self.c.drawString(x,H-y-size*.78,s);textlog.append(s)
 def para(self,s,x,y,w,size=11.3,font='Serif',color=INK,leading=None,maxh=None):
  textlog.append(unescape(re.sub('<[^>]+>',' ',s)))
  if size>=17:
   style=ParagraphStyle('display',fontName=font,fontSize=size,leading=leading or size*1.3,textColor=HexColor(color))
   p=Paragraph(s,style);_,h=p.wrap(w,H)
   if maxh is not None and h>maxh+.1:raise ValueError(f'Display overflow on page {self.n}: {h}>{maxh}')
   p.drawOn(self.c,x,H-y-h);return h
  return LAYER.add(self,'para',s,x,y,w,size,font,color,leading or size*1.3,maxh)
 def dropcap(self,s,x,y,w,size=11.3,leading=14.5,maxh=None):
  textlog.append(unescape(re.sub('<[^>]+>',' ',s)))
  return LAYER.add(self,'drop',s,x,y,w,size,'Serif',INK,leading,maxh)
 def image(self,name,x,y,w,h=None):
  path=self.assets/name
  iw,ih=Image.open(path).size;h=h or w*ih/iw
  assert Image.open(path).format=='PNG'
  self.c.drawImage(str(path),x,H-y-h,width=w,height=h,mask='auto')
  return h
 def label(self,s,x,y,color=RED,angle=0,size=8.2,bg=None):
  c=self.c;c.saveState();c.translate(x,H-y);c.rotate(angle)
  width=pdfmetrics.stringWidth(s,'Mono',size)+14
  if bg:c.setFillColor(HexColor(bg));c.rect(-5,-size-4,width,size+11,fill=1,stroke=0)
  c.setFillColor(HexColor(color));c.setFont('Mono',size);c.drawString(0,-size*.78,s);c.restoreState();textlog.append(s)
 def page(self,section,paper=PAPER,ink=INK,texture=True,folio=True):
  if self.n:self.c.showPage()
  self.n+=1;self.rect(0,0,W,H,paper)
  if texture:
   rng=random.Random(100+self.n)
   self.c.setFillColor(Color(.25,.25,.17,alpha=.065))
   for i in range(1200):
    x=rng.random()*W;y=rng.random()*H;self.c.circle(x,y,rng.uniform(.12,.4),fill=1,stroke=0)
  if folio:
   self.text('WEEK IN HAZEL',M,20,7.3,'Mono',ink);self.text(section.upper(),270,20,7.3,'Mono',ink)
   self.line(M,36,W-M,36,ink,.6)
   self.line(M,H-29,W-M,H-29,ink,.5);self.text(self.meta['id']+'  /  '+self.meta['date'],M,H-20,7,'Mono',ink)
   self.text(f'{self.n:02d}',W-M-12,H-20,7,'Mono',ink)
  pages.append({'file':self.path.name,'page':self.n,'section':section})
 def sources(self,items,y=651):
  s='  /  '.join(f'<link href="{url}" color="{GREEN}"><u>{escape(label)}</u></link>' for label,url in items)
  self.para(s,M,y,CW,size=7.8,font='Sans',leading=10,maxh=30)
 def title(self,s,kicker=None,y=68,size=36):
  if kicker:self.label(kicker,M,49)
  return self.para(s,M,y,CW,size=size,font='SerifBold',leading=size*.98)
 def save(self):self.c.save()
def pr(n):return f'https://github.com/hazelgrove/hazel/pull/{n}'
def issue(n):return f'https://github.com/hazelgrove/hazel/issues/{n}'
def commit(sha):return 'https://github.com/hazelgrove/hazel/commit/'+sha
