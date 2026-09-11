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
ROOT=Path(__file__).resolve().parent; ASSETS=ROOT/'assets'; OUT=ROOT.parent/'pdf'; OUT.mkdir(exist_ok=True)
F=Path('/Users/andrewblinn/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/libreoffice-headless/libreoffice/LibreOfficeDev.app/Contents/Resources/fonts/truetype')
for name,filename in [('Serif','LinLibertine_R_G.ttf'),('SerifBold','LinLibertine_RB_G.ttf'),('SerifItalic','LinLibertine_RI_G.ttf'),('Sans','Rubik-Regular.ttf'),('SansBold','Rubik-Bold.ttf'),('Mono','LiberationMono-Regular.ttf')]: pdfmetrics.registerFont(TTFont(name,str(F/filename)))
pdfmetrics.registerFontFamily('Serif',normal='Serif',bold='SerifBold',italic='SerifItalic',boldItalic='SerifBold')
pdfmetrics.registerFontFamily('Sans',normal='Sans',bold='SansBold',italic='Sans',boldItalic='SansBold')
W,H=540,720; M=36; CW=W-2*M
PAPER='#F3EBDD'; INK='#222A23'; GREEN='#355B43'; RED='#BB3E27'; MUTED='#6C7267'; PALE='#DCE2CC'; LINE='#B6B9A7'
LAYER=BrowserLayer(ROOT,F)
metrics=json.loads((ROOT/'research/metrics.json').read_text()); pages=[]; textlog=[]
class Zine:
 def __init__(self,path,treatment='clean'):
  base_path=LAYER.add_file(self,path);self.c=canvas.Canvas(str(base_path),pagesize=(W,H)); self.c.setTitle('Week in Hazel | Issue 001, revision 5 | '+treatment+' edition');self.c.setAuthor('Week in Hazel - edited by Astra for Andrew Blinn');self.n=0;self.path=path;self.treatment=treatment
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
  stem=Path(name).stem; is_shot=stem in ('probes-cards','modular-focus','fumola-scene','constellation-score')
  path=ASSETS/(stem+'-'+self.treatment+'.png') if is_shot else ASSETS/name
  reference=ASSETS/(stem+'-clean.png') if is_shot else path
  iw,ih=Image.open(reference).size;h=h or w*ih/iw
  if is_shot:
   assert Image.open(path).format=='PNG',f'Expected real PNG: {path}'
  if is_shot and self.treatment=='clean':
   self.rect(x-4,y-4,w+8,h+8,'#FCF7EB',GREEN,.7)
  self.c.drawImage(str(path),x,H-y-h,width=w,height=h,mask='auto')
  if is_shot and self.treatment=='clean':
   for xx,yy,dx,dy in [(x-4,y-4,1,1),(x+w+4,y-4,-1,1),(x-4,y+h+4,1,-1),(x+w+4,y+h+4,-1,-1)]:
    self.line(xx,yy,xx+dx*5,yy,RED,1.2);self.line(xx,yy,xx,yy+dy*5,RED,1.2)
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
   self.line(M,H-29,W-M,H-29,ink,.5);self.text('001  /  04-10 SEP 2026',M,H-20,7,'Mono',ink)
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

def cover(z):
 z.page('cover',folio=False)
 z.text('A SMALL MAGAZINE ABOUT A VERY LIVE LANGUAGE',M,23,8,'Mono')
 z.text('Week in',M,55,30,'SerifItalic');z.text('HAZEL',M,91,85,'SansBold')
 z.label('ISSUE 001',397,63,angle=-4,bg=RED,color=PAPER,size=10)
 z.text('04-10 SEPTEMBER 2026',M,180,8.8,'Mono');z.text('PILOT / ABOUT 15 MINUTES',293,180,8.8,'Mono')
 z.image('drawer-tree.png',0,208,W,360)
 z.rect(25,545,383,55,PAPER);z.text('The cabinet is open.',36,553,32,'SerifBold')
 z.para('Probes IV reaches dev. Modules II tests new boundaries. Constellation becomes an editor. Fumola connects two runtimes.',M,618,CW,size=17,leading=20,maxh=49)
 z.text('A WEEKLY LETTER FROM THE HAZEL WORKBENCH',M,692,7.5,'Mono')

def lead(z):
 z.page('The big landing');z.title('More room to inspect<br/>a running program.', 'MERGED INTO DEV / PROBES IV',size=33)
 z.image('probes-cards.png',65,150,410)
 z.para('<b>Cards / dev.</b> '+'Insertion sort compares card ranks and builds ordered hands. Alexander’s card renderer makes those intermediate values readable beside the recursive program.',M,405,CW,size=8.7,font='Sans',leading=11.3,maxh=34)
 a='Andrew Blinn’s <b>Probes IV</b> reached dev on September 8, merged by Cyrus Omar. A sample can now expand into a multiline drawer below its source line. Each probe has its own drawer state; values longer than fifteen rows scroll within that space.<br/><br/>The Cards example shows why room helps. Its <b>insert</b> function compares a card with the first card in a hand, then places it before that hand or recurses through the tail. Probes expose the comparisons and intermediate hands. The renderer comes from Alexander Bandukwala’s earlier work, integrated into dev this week. Small rich views stay inside the chip, preserving its controls; taller views open the drawer.'
 b='Automatic rich views are on by default. A probe can return to text; tables remain an explicit&#160;choice.<br/><br/>Auto-probe now offers <b>Off / Caret / All</b>: manual placement, the current top-level definition, or one probe per row across the program. Adding a probe also refreshes analysis so a cached evaluation cannot leave it empty until another edit.<br/><br/>Step-into reaches indirect calls, sample navigation scrolls its selection into view, and menus open on right- or alt-click. Try <b>Documentation → Cards</b> on dev to follow a recursive call through its arguments and results.'
 z.dropcap(a,M,446,222,size=11.1,leading=14,maxh=218);z.para(b,282,446,222,size=11.1,leading=14,maxh=218)
 z.sources([('#2363: features, discussion & merge',pr(2363)),('Try dev','https://hazel.org/build/dev/')],y=673)


def aftermath(z):
 z.page('After the landing');z.title('The first drawer reports.','OPEN ISSUES / A MERGED CI CHANGE',size=34)
 z.para('Three interaction reports and a recursive-ascription regression followed the Probes IV merge. All four remained open on September 11.',M,119,CW,size=13.2,leading=17,maxh=51)
 z.label('01 / INTERACTION',M,188);z.label('02 / PERFORMANCE',282,188)
 z.para('Missing menus.',M,207,222,size=21,font='SerifBold',leading=23,maxh=25)
 z.para('A cost inside recursion.',282,207,222,size=21,font='SerifBold',leading=23,maxh=25)
 z.para('Closing a tall table can leave its renderer selected after the picture disappears: the menu still says “Hide table.” Recovering it requires hiding and selecting it again (<b>#2519</b>). Inside the drawer, the sample context menu is unavailable; right-click can fall through to the editor’s menu (<b>#2520</b>).<br/><br/>Short tables expose a separate fault. A positioning rule left from the old modal anchors the column menu below the entire drawer. Tall, scrolling tables use a sticky header and avoid this particular problem (<b>#2521</b>).',M,240,222,size=11.1,leading=14,maxh=203)
 z.para('In <b>#2524</b>, a recursive sum with an ascription on each call exhausts memory at 12,800 calls after the merge. The reporter’s pre-merge version completes; removing the ascription also restores roughly linear behavior.<br/><br/>The report traces the growth to copying and retaining call-stack identifiers at each relevant evaluation step. Removing the ascription changes the scaling without changing the recursive structure, giving the investigation a narrower target than recursion itself.',282,240,222,size=11.1,leading=14,maxh=203)
 z.line(M,447,504,447,LINE,.6);z.label('03 / CI: A FAILURE THAT CAUSED A NEEDLESS REVERT',M,460,size=8)
 z.para('Matthew Hammer’s comment on <b>#2482</b> gives flaky tests a concrete cost: his team reverted a good Fumola commit after an unrelated evaluator property failed. Alexander’s merged change disables two unstable randomized properties, retains their bodies for compilation, and runs fixed counterexamples instead.',M,483,222,size=11,leading=13.8,maxh=98)
 z.para('Those checks expect the evaluators to disagree. If the examples start agreeing, the checks fail with a reminder to restore the properties. They do not pin an exact wrong result or fix either semantic bug. Matthew also notes that the separate Pattern equivalence test can still exhaust memory.',282,483,222,size=11,leading=13.8,maxh=98)
 z.paper_patch(M,596,CW,50,PALE,fold=11)
 for i,(value,label) in enumerate([('12','issues opened'),('4','issues closed'),('344','issues outstanding*')]):
  x=M+12+i*154;z.text(value,x,599,28,'SerifBold',GREEN);z.text(label,x,632,8.2,'Sans')
 z.para('Opened and closed: September 4-10 UTC. *Outstanding on September 11.',M,652,CW,size=7.7,font='Sans',leading=9.5,maxh=20)
 z.sources([('#2519',issue(2519)),('#2520',issue(2520)),('#2521',issue(2521)),('#2524',issue(2524)),('#2482 & discussion',pr(2482)),('Open issues','https://github.com/hazelgrove/hazel/issues?q=is%3Aissue%20is%3Aopen')],y=675)


def modules(z):
 z.page('The branch garden');z.title('Modules, all the way up.','MODULES II / NINE DRAFT PRs',size=37)
 z.para('Alexander Bandukwala’s nine-part draft stack makes modules distinct values, repairs their boundaries, and tries a modular standard library.',M,122,CW,size=14.2,leading=18,maxh=56)
 z.label('THE STACK / VALUES → BOUNDARIES → LIBRARY',M,174,size=7.6)
 groups=[('1-3','A module gets an identity','Signatures, width matching, abstract members',[(2493,'values'),(2494,'width'),(2495,'sealing')]),('4-7','Make the edges behave','Module functions, errors, expectations, duplicates',[(2498,'functions'),(2500,'errors'),(2501,'nested'),(2503,'duplicates')]),('8-9','Try the language on itself','Modular implicits + a modular standard library',[(2508,'implicits'),(2510,'library')])]
 y=195
 for i,(no,title,sub,links) in enumerate(groups):
  x=M+i*14;w=CW-i*14;z.paper_patch(x,y,w,59,[PALE,'#E9DEBD','#E8C7B4'][i],fold=13+i*2);z.text(no,x+13,y+12,26,'SerifItalic',GREEN);z.text(title,x+78,y+8,16,'SerifBold');z.text(sub,x+78,y+28,9,'Sans');z.para('  '.join(f'<link href="{pr(n)}" color="{GREEN}">#{n}</link>' for n,_ in links),x+78,y+44,w-90,size=8.5,font='Mono');y+=70
 z.para('A module becomes a value with a signature, rather than a labeled tuple. Members evaluate in order and projections resolve by name. One follow-up fixes a revealing bug: <b>let f(x) = …</b> exported the argument <b>x</b> instead of the function <b>f</b>.<br/><br/>Width matching lets a function asking only for <b>name : String</b> accept a module containing both name and age. The function sees the narrower interface. But differently shaped <b>if</b> arms do not silently find a shared signature: the author must write a narrowing ascription.<br/><br/>Abstract members hide representation while retaining identity. Outside a sealed module <b>M</b>, a member can have type <b>M.T</b>. Aliases preserve that identity; independently sealed modules get distinct types.',M,411,222,size=11.1,leading=14,maxh=253)
 z.para('The middle drafts improve error locations and rules around names. A nested signature mismatch should identify the offending inner definition. Duplicate declarations in a signature are errors; repeated bindings in a module body deliberately shadow earlier ones.<br/><br/>The last two PRs remain early prototypes. Modular implicits explore how arguments are found. The library sketch exposes <b>Int, Float, String, List, Option</b> and <b>Pair</b>, while keeping existing flat names available.<br/><br/>There is a concrete cost to investigate: looking up <b>List.map</b> currently copies a 65-member module value. That cost is unmeasured. Sharing constraints and implicit-resolution design also remain unfinished; the prototypes make those costs and design choices available to examine.',282,411,222,size=11.1,leading=14,maxh=253)
 z.sources([('Start at #2493',pr(2493)),('Nested errors #2501',pr(2501)),('Duplicates #2503',pr(2503)),('Implicits #2508',pr(2508)),('Library #2510',pr(2510))],y=673)


def agent(z):
 z.page('Aiject / the workspace');z.title('Edit a definition.<br/>Keep the program live.','DRAFT: MODULAR EDITORS / OPEN: AGENT HARDENING',size=34)
 z.image('modular-focus.png',M,155,CW)
 cap='<b>Modular editors / Mega 1k.</b> '
 z.para(cap+'<b>RunningSums.running_sum</b> from Mega 1k. A probe on <b>total</b> collects eight samples from the surrounding program, whose result remains <b>true</b>.',M,348,CW,size=8.5,font='Sans',leading=11,maxh=34)
 z.dropcap('Andrew’s modular editors open focused cells from a collapsible outline. Each cell has a header and body, while the master document supplies context, tests and results. A probe can collect calls from outside the definition being edited.<br/><br/>The screenshot’s function accumulates partial sums in reverse order, then reverses the list. The probe exposes intermediate totals without opening the rest of Mega 1k. This is the useful promise of the smaller view: its values still belong to the whole program.<br/><br/>One of this week’s fixes repairs a failure of that arrangement. Editing a later definition could leave evaluation stuck on an old result.',M,393,222,size=11.1,leading=14,maxh=238)
 z.para('The incremental evaluator saw an apparently unchanged enclosing term and reused its answer, although the program below it had changed. The fix includes that remaining program in the term and adds a regression test.<br/><br/>Analysis also works from the affected dependencies. An edit in the PR review’s Mega 4k headless benchmark analyzed 16 of 891 items. Autosave still has a whole-text fallback, so an edit does not avoid all document-sized work.<br/><br/>The related agent-hardening PR waits up to roughly ten seconds for probe evaluation to settle. Edit, view and probe tools gain owner/member paths, and persistence moves to per-chat records. Both PRs remain open.',282,393,222,size=11.1,leading=14,maxh=238)
 z.paper_patch(M,640,CW,22,PALE);z.para('<b>The check:</b> values in a focused cell must agree with the master document.',M+10,645,CW-20,size=9.4,leading=12,maxh=13)
 z.sources([('Editors #2469',pr(2469)),('Evaluation repair',commit('46bdb6b16e')),('Hardening #2427',pr(2427)),('Performance review',pr(2469)+'#issuecomment-5486808215')],y=673)


def constellation(z):
 z.page('Aiject / Constellation');z.title('A graph you can<br/>edit through.','DRAFT #2505 / GRAPH, EDITOR, AGENT',size=35)
 z.image('constellation-score.png',50,166,194)
 cap='<b>Scorekeeper / agent-canvas.</b> '
 z.para(cap+'A module hull groups <b>Score</b> and its member <b>bonus</b>. Passing-test dots attach to <b>tally</b> and <b>capped</b>. The arrows describe relationships between definitions and their types.',M,436,222,size=8.4,font='Sans',leading=10.6,maxh=64)
 h=z.dropcap('Constellation arranges a program by types and definitions. Type aliases become nodes; functions become arrows from input to output. Values attach to their types, and tests to the functions they mention. Small builtin-type terminals keep <b>Int</b> from collecting every arrow in one place.',282,166,222,size=11.1,leading=14,maxh=144)
 z.para('In Scorekeeper, <b>Score</b> supplies a base of 10, a doubling bonus and a cap of 50. <b>tally</b> adds the base to the bonus; <b>capped</b> limits the answer. For an input of 7, the program returns 24.<br/><br/>This week’s main canvas mode turns selection into navigation. Selecting <b>tally</b>, or Counter App’s <b>update</b>, opens its definition below the graph. Leaving the mode restores the whole program. The relationships help locate a definition; the panel gives access to its source, values and tests.',282,166+h+7,222,size=11.1,leading=14,maxh=202)
 z.line(M,510,504,510,LINE,.6);z.label('KEEPING SAMPLES AND MOTION IN SYNC',M,523,color=GREEN,size=7.6)
 z.para('Value wells needed a matching repair: their samples belonged to the master editor, but clicks and arrow keys went to the active definition cell. The fix routes actions to the owner of the displayed values and outlines the selected sample.<br/><br/>For agent edits, <b>pace</b> separates travel, act and settle; <b>follow</b> controls camera attention.',M,546,222,size=10.8,leading=13.5,maxh=118)
 z.para('The animation code moves module hulls with their nodes and holds the camera when the program is already visible. These controls aim to make agent edits easier to follow.<br/><br/>One demo switch with a definition open left the graph blank until reload. Six demos include nested modules, many callers and pipeline depth.',282,546,222,size=10.8,leading=13.5,maxh=118)
 z.sources([('Canvas #2505',pr(2505)),('Canvas mode',commit('b1d83917ce')),('Sample fix',commit('73325cb58c')),('Hull motion',commit('03f4c2badc')),('Camera hold',commit('a5b6dbf4c6'))],y=675)


def fumola(z):
 z.page('A visitor moves in');z.title('Two languages.<br/>One notebook.','OPEN PR / FUMOLA LIVELITS / EXPERIMENTAL',size=37)
 z.image('fumola-scene.png',M,161,CW)
 z.para('<b>Fumola / fumola-livelit-mvp.</b> A GCD calculation and a named-cell read return <b>(6, 42)</b> to Hazel. Both expressions use the same runtime instance.',M,364,CW,size=8.6,font='Sans',leading=11,maxh=33)
 z.dropcap('Matthew Hammer’s Fumola integration lets a Hazel document name and use an external runtime. Livelits sharing an instance id communicate with the same store; named thunks give successive edits an identity within it.<br/><br/>The current branch has four entry points. <b>fumola_new</b> declares a runtime and mode. <b>fumola_put_force</b> evaluates inside a named thunk; <b>fumola_eval</b> runs without that wrapper. <b>fumola_with</b> passes a Hazel value across as <b>input</b>. Its example doubles 21 and returns 42. Holes and functions cannot cross this boundary.',M,404,222,size=11.1,leading=14,maxh=212)
 z.para('Runtime mode matters. <b>Simple</b> is the default and keeps no dependency graph. <b>Graphical</b> records nodes, dependencies and events; one example returns its event log as a Hazel table. Those records are groundwork for repair, which the example above does not exercise.<br/><br/>Two loader changes merged into the Fumola feature branch: source fallback and a manifest that selects a matched JavaScript/Wasm pair at content-addressed URLs, identifying the loaded build.<br/><br/>The runtime remains unpinned, but identifying the loaded build makes stale-version problems easier to diagnose.',282,404,222,size=11.1,leading=14,maxh=212)
 z.paper_patch(M,621,CW,41,PALE,fold=9)
 z.para('<b>A testing gap:</b> translation fixtures cover expected formats, but the evaluator suite skips the four live forms. Those tests can stay green when the published runtime changes incompatibly.',M+12,629,CW-24,size=10.3,leading=13,maxh=27)
 z.sources([('#2492',pr(2492)),('Branch merges #2504',pr(2504)),('#2509',pr(2509)),('Runtime docs','https://github.com/hazelgrove/hazel/blob/583e84d07b/docs/fumola-runtime-changes.md')],y=675)


def people(z):
 z.page('People & small things');z.title('Around the workbench.','THIS WEEK’S THREADS',size=35)
 people=[('Andrew Blinn','@disconcision','Probes IV reaches dev after accumulated work on drawers, sample navigation and rich views. His open workspace stack tackles a related problem at document scale: selecting a definition while retaining the surrounding program’s evaluation, tests and observations.'),('Alexander Bandukwala','@7h3kk1d','Modules II combines signature design with fixes to member binding and error locations. Generating random signatures exposed failures that part 4 reports converting into deterministic regressions. Alongside that stack: editable tutorials, CI changes and reports of new probe problems.'),('Matthew Hammer','@matthewhammer','Fumola and the Wasm spike both cross runtime boundaries. His benchmark correction matches answers and settings before narrowing the speedup claim. His comment on a flaky evaluator test traces an unnecessary Fumola revert, connecting CI behavior to a specific development cost.'),('Cyrus Omar','@cyrus-','Merged Probes IV into dev and opened the dependency update that also landed there. Probes IV’s arrival also brings its follow-up reports onto the shared build, where people outside the branch can encounter the new interactions.')]
 y=124
 for name,handle,body in people:
  z.text(name,M,y,18,'SerifBold');z.text(handle,314,y+3,8.5,'Mono',MUTED);z.para(body,M,y+24,CW,size=11.1,leading=14,maxh=43);z.line(M,y+71,504,y+71,LINE,.5);y+=84
 z.label('SMALL THINGS, REAL CONSEQUENCES',M,469)
 z.para('Editable lessons expose broken tests.',M,488,CW,size=22,font='SerifBold')
 z.para('The open tutorial stack replaces 25 generated lesson files with <b>.hzt</b> text: prose, code, hints and hidden tests get separate sections. Conversion exposed six hidden tests containing <b>$==</b>, which Hazel cannot lex. Alexander reports fixing the operator and passing the affected suites.<br/><br/>Three recovered Gradebook tasks bring the branch to 28 lessons. Previous and next stay inside a folder; a dropdown changes folders.',M,521,222,size=10.9,leading=13.6,maxh=143)
 z.para('Lesson identities stay separate from titles, so reorganization need not discard saved work. The authors ask to merge the three dependent PRs together.<br/><br/>Issue <b>#2518</b> explains another editing cost: <b>[¿]</b> reloads as <b>[]</b>. Removing the marker leaves a valid empty list, so loading does not restore its blank. The workaround, <b>[?]</b>, preserves an explicit hole but makes the student select and replace a tile instead of typing into a gap.',282,521,222,size=10.9,leading=13.6,maxh=143)
 z.sources([('#2363',pr(2363)),('#2493',pr(2493)),('#2492',pr(2492)),('#2511',pr(2511)),('Tutorials #2485',pr(2485)),('#2513',pr(2513)),('#2518',issue(2518))],y=675)

def stats(z):
 z.page('The instrument panel');z.title('A busy week.<br/>An imperfect instrument.','REPOSITORY ACTIVITY / UTC WINDOW',size=33)
 vals=[('23','PRs opened'),('13','of those are drafts*'),('5','PRs merged'),('65','recent branch tips**')]
 for i,(v,l) in enumerate(vals):
  x=M+i*119;z.paper_patch(x,154,111,69,PALE,fold=7+i%2*2);z.text(v,x+10,159,33,'SansBold',GREEN);z.text(l,x+9,202,7.7,'Sans')
 z.para('The 5 merges: 3 into dev, 2 into fumola-livelit-mvp. *Draft state at retrieval.<br/>**Tip committer dates fall in the week; this is not a count of branch pushes.',M,234,CW,size=8.8,font='Sans',leading=12,maxh=28)
 z.text('VISIBLE CLAUDE CO-AUTHOR CREDITS',M,281,8.4,'Mono');z.text('277 / 382',M,303,31,'SerifBold',GREEN)
 z.para('unique reachable commit objects carry a Claude co-author trailer (72.5%). Among 294 non-merge objects, 271 carry one (92.2%).',228,301,276,size=10.1,font='Sans',leading=13,maxh=43)
 z.label('DAILY COMMIT OBJECTS / SEPTEMBER 2026',M,359,size=7.5,color=INK)
 chart_y=482;scale=.72
 for i,(day,v) in enumerate(metrics['daily'].items()):
  x=M+15+i*65;total=v['total'];a=v['claude'];z.ink_bar(x,chart_y-total*scale,34,total*scale,'#C3C5B9');z.ink_bar(x,chart_y-a*scale,34,a*scale,GREEN)
  z.text(str(total),x+4,chart_y-total*scale-16,9,'Mono');z.text(day[-2:],x+10,494,8,'Mono')
 z.sketch_line(M+10,chart_y+.5,493,chart_y+.5,LINE,.55)
 z.ink_bar(M,517,9,9,GREEN);z.text('Claude credited',M+15,518,8.5,'Sans');z.ink_bar(180,517,9,9,'#C3C5B9');z.text('No Claude trailer',195,518,8.5,'Sans')
 z.line(M,544,504,544,LINE,.6)
 z.para('<b>Counting the activity.</b> The sample covers commits reachable from 690 remote branch tips, with committer dates in September 4-10 UTC. Shared SHAs count once. Rebases and cherry-picks can create different SHAs for similar work; 88 objects are merges. This is activity, not a productivity leaderboard.',M,558,222,size=10.3,leading=13,maxh=126)
 z.para('<b>Reading the credits.</b> 128 commit objects contain signature headers (signatures unchecked). These are separate from agent credits. Zero OpenAI/Codex/ChatGPT co-author trailers were found; this does not establish zero use. Missing trailers mean assistance is unknown. Trailers measure disclosed assistance, not its share of the work.',282,558,222,size=10.3,leading=13,maxh=126)

def dispatch(z):
 z.page('Bench notes & the back room');z.title('What the Wasm<br/>benchmark measures.','WASM SPIKE / AUTHOR-REPORTED RESULTS',size=30)
 z.para('Matthew’s Wasm spike gets <b>SInt</b> and <b>Float</b> workloads running, avoiding the arbitrary-precision runtime still needed by <b>Int</b> and <b>Nat</b>. Corrected evaluator benchmarks report <b>3.0-4.1×</b>, roughly 3.5×. Both backends use <font name="Serif" size="11.1">js_of_ocaml</font> 6.2.0 and Node 22, with 20 iterations and matching result checksums.',M,145,222,size=11.1,leading=14.3,maxh=115)
 z.para('Probe recording made little difference on these tiny, compute-heavy workloads. Large documents with short evaluations remain a different question. The initial cold-statics timing was distorted by warm-up and does not support a speedup claim. The branch also removes livelits as a shortcut; it is not for merge.',282,145,222,size=11.1,leading=14.3,maxh=115)
 z.paper_patch(M,272,CW,45,INK,fold=10);z.text('~3.5×',M+12,280,28,'SansBold',PAPER);z.para('The evaluator, on these workloads.<br/>No measured app-wide speedup.',184,282,299,size=11.5,font='Sans',color=PAPER,leading=14)
 z.label('THE FICTION DEPARTMENT',M,349,color=RED)
 z.image('observable-comic.png',M,372,CW)
 z.para('“Unfinished business” / an original comic',M,536,CW,size=8.3,font='Sans',color=MUTED)
 z.para('<b>Branch postcards.</b> <font name="Mono" size="9">resizable-type-probe</font> gives tuple types a shared abbreviation budget; <font name="Mono" size="9">fix/probe-rich-depth-clamp</font> frees rich chips from a one-row clamp. Both were branch-only changes on September 11.',M,569,CW,size=10.8,leading=14,maxh=58)
 z.para('<b>Late wire:</b> Matthew also opened Blackboard MVP: a proof-assistant kernel and editor sort. Editor statics and tactics remain future work. Draft #2525.',M,633,CW,size=9.2,leading=11.5,maxh=26)
 z.sources([('Wasm correction',pr(2490)+'#issuecomment-5534741226'),('Type budget',commit('14aa84c23c')),('Rich depth',commit('e644dcb91b')),('Blackboard #2525',pr(2525))],y=673)

def back(z):
 z.page('Still on the bench');z.title('Still on the bench.','OPEN QUESTIONS',size=39)
 z.para('Several of this week’s changes make a small part of a program easier to work with. The unresolved questions concern what must remain connected: a sample to its call, a member to its module, an edit to its runtime state.',M,134,CW,size=14,leading=18,maxh=75)
 z.label('01 / PROBES',M,237,color=GREEN);z.label('02 / MODULES',282,237,color=GREEN)
 z.para('How much of the call stack<br/>does a sample need?',M,258,222,size=19,font='SerifItalic',leading=21,maxh=44)
 z.para('Where should narrowing<br/>happen automatically?',282,258,222,size=19,font='SerifItalic',leading=21,maxh=44)
 z.para('The recursive sum in <b>#2524</b> needs an ascription to trigger its memory growth. The report points to retained copies of call-stack identifiers. That makes the lifetime and representation of probe metadata central to the fix: inspection should remain useful as the number of calls grows.',M,315,222,size=11.2,leading=14.4,maxh=106)
 z.para('Width matching accepts a richer module at a typed argument, but a list of wider modules does not automatically become a list of narrower signatures. The draft’s workaround is to ascribe each element. That gap puts a concrete usability question beside the rules for hiding members.',282,315,222,size=11.2,leading=14.4,maxh=106)
 z.line(M,437,504,437,LINE,.6)
 z.label('03 / FUMOLA',M,457,color=GREEN);z.label('04 / CONSTELLATION',282,457,color=GREEN)
 z.para('What should a copy share?',M,478,222,size=19,font='SerifItalic',leading=21,maxh=23)
 z.para('Can several edits stay legible?',282,478,222,size=18.5,font='SerifItalic',leading=21,maxh=23)
 z.para('A Fumola instance id connects livelits to one store. Reusing it preserves that connection; assigning a new id separates state. Copying a document raises a further choice: which identities and cached results should the copy inherit? Loader versioning helps identify the runtime, but leaves that ownership question open.',M,515,222,size=11,leading=14,maxh=106)
 z.para('Constellation’s pace and follow controls organize motion as well as layout. Keeping a module hull with its definitions and holding a useful camera position are small but necessary steps. The harder case is a sequence of agent edits: additions, deletions and changed relationships must remain understandable together.',282,515,222,size=11,leading=14,maxh=106)
 z.line(M,637,504,637,GREEN,1)
 z.para('<b>Editor</b> Astra · <b>Reporting</b> Ellis, Rowan &amp; Mica · AI editorial team<br/>Illustrations and screenshot treatments: ImageGen. '+('Screenshots are illustrated reproductions; the clean edition preserves exact UI.' if z.treatment=='woodcut' else 'Screenshots show running branch examples.'),M,650,CW,size=8.1,font='Sans',leading=10.5,maxh=33)


for treatment,filename in [("clean","week-in-hazel-001.pdf"),("woodcut","week-in-hazel-001-woodcut.pdf")]:
 z=Zine(OUT/filename,treatment)
 for fn in [cover,lead,aftermath,modules,agent,constellation,fumola,people,stats,dispatch,back]:fn(z)
 z.save()

s=Zine(OUT/'week-in-hazel-001-style-lab.pdf')
s.page('Field notes / direction A',paper='#F1F0E3',folio=False)
s.text('WEEK IN HAZEL / ART-DIRECTION STUDY A',M,25,8,'Mono',GREEN)
s.text('Field notes',M,66,50,'SerifItalic',GREEN);s.text('from the branch garden',M,124,22,'Serif',GREEN)
s.line(M,163,504,163,GREEN,.7);s.label('SPECIMEN 001 / MODULES II',M,183,color=GREEN)
s.image('drawer-tree.png',M,215,CW,312)
s.paper_patch(327,479,177,85,'#E0E6D4',fold=13);s.para('Nine draft PRs.<br/>One growing idea.<br/><br/><b>Still under cultivation.</b>',340,491,150,size=12,font='Serif',color=GREEN,leading=15)
s.para('A quieter treatment: botanical specimen sheet, generous margins, marginal numbers, one idea at a time. The unfinished system is something to observe closely.',M,587,CW,size=15,leading=19,maxh=59)
s.text('04-10 SEP 2026  /  TWO-PAGE THEME STUDY',M,685,8,'Mono',GREEN)
s.page('Field notes / names',paper='#F1F0E3',ink=GREEN)
s.title('Names that keep<br/>their meaning.','DRAFT MODULES / EXPERIMENTAL FUMOLA',size=36)
s.label('I. A BOUNDARY',M,169,color=GREEN);s.para('A sealed module gives an abstract type a path: <b>M.T</b>. The name says where its identity comes from, even when its representation stays hidden. Modules II is still working out the rules around that boundary.',M,191,222,size=12,leading=16,maxh=113)
s.label('II. A MEMORY',282,169,color=GREEN);s.para('A Fumola livelit names a runtime and, in one form, a thunk. Reusing that name can keep an edit attached to prior state. Copying or reloading raises a different question: which history should the new object inherit?',282,191,222,size=12,leading=16,maxh=113)
s.image('fumola-scene.png',M,335,CW)
s.para('FIELD OBSERVATION 02 / A GCD and a named-cell read return (6, 42) from Fumola to Hazel.',M,538,CW,size=8.7,font='Mono',color=GREEN,leading=11.5,maxh=36)
s.para('A module can hide its representation.<br/>A runtime can remember an earlier value.<br/>Both need a name that survives the edit.',M,593,CW,size=17,font='SerifItalic',color=GREEN,leading=21,maxh=65)
s.sources([('Abstract types #2495',pr(2495)),('Fumola #2492',pr(2492)),('Runtime identity #2509',pr(2509))],y=670)
s.page('Night shift / direction B',paper='#E9E7DF',folio=False)
s.rect(0,0,W,192,INK);s.text('WEEK IN HAZEL / ART-DIRECTION STUDY B',M,25,8,'Mono',PAPER)
s.text('NIGHT',M,54,70,'SansBold',PAPER);s.text('SHIFT',171,124,70,'SansBold',PAPER)
s.label('THE MACHINES HAVE A WORKBENCH',39,226,angle=3,bg=RED,color=PAPER,size=10)
s.para('277',M,276,460,size=116,font='SansBold',leading=110)
s.para('visible Claude co-author credits<br/>among 382 commit objects',M,407,CW,size=22,font='SansBold',leading=25)
s.line(M,480,504,480,INK,3)
s.para('No, this is not the percentage<br/>of Hazel “written by AI.”',M,505,CW,size=26,font='SerifItalic',leading=29,maxh=63)
s.para('The credits record disclosed assistance. Missing trailers leave the rest unknown; rebases and cherry-picks can count related work more than once. The numbers belong beside the stories, not above them.',M,600,CW,size=13.5,leading=18,maxh=60)
s.text('PHOTOCOPY ENERGY / BLACK INK / VERMILION / DEADPAN',M,690,7.5,'Mono')
s.page('Night shift / observed',paper='#E9E7DF')
s.label('DRAFT WORKSPACE / OPEN AGENT HARDENING',M,52,angle=-1,color=RED)
s.title('Somewhere to watch<br/>the edits happen.',y=83,size=33)
s.image('modular-focus.png',M,181,CW)
s.para('One definition open. A thousand-line program still running around it. Probes collect its calls; tests and the final result stay in view. Constellation adds another way to find the next definition.',M,382,CW,size=13,leading=17,maxh=72)
s.label('FICTION DEPARTMENT',M,474,color=RED);s.image('observable-comic.png',M,499,CW)
s.sources([('Modular editors #2469',pr(2469)),('Constellation #2505',pr(2505)),('Hardening #2427',pr(2427))],y=672)
s.save()
(ROOT/'layout-manifest.json').write_text(json.dumps(pages,indent=2))
(ROOT/'typeset-text.txt').write_text('\n\n'.join(textlog))

report=LAYER.finish()
if not os.environ.get('HAZEL_ZINE_MEASURED_PASS'):
 env=dict(os.environ,HAZEL_ZINE_MEASURED_PASS='1')
 subprocess.run([sys.executable,__file__],env=env,check=True)
else:
 errors=[e for f in report['files'] for e in f['errors']]
 if errors:raise ValueError(f'Browser text overflows: {errors}')
 print('Created and measured clean, woodcut, and style-lab PDFs in',OUT)
