"""Typeset the pilot and two art-direction studies. Run with bundled Python."""
from pathlib import Path
import json, random, math, re
from xml.sax.saxutils import escape
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
metrics=json.loads((ROOT/'research/metrics.json').read_text()); pages=[]; textlog=[]
class Zine:
 def __init__(self,path,treatment='clean'):
  self.c=canvas.Canvas(str(path),pagesize=(W,H)); self.c.setTitle('Week in Hazel | Issue 001, revision 2 | '+treatment+' edition');self.c.setAuthor('Week in Hazel - edited by Astra for Andrew Blinn');self.n=0;self.path=path;self.treatment=treatment
 def rect(self,x,y,w,h,fill,stroke=None,lw=.5):
  c=self.c;c.setFillColor(HexColor(fill));c.setStrokeColor(HexColor(stroke or fill));c.setLineWidth(lw);c.rect(x,H-y-h,w,h,fill=1,stroke=bool(stroke))
 def line(self,x1,y1,x2,y2,color=INK,lw=1):
  c=self.c;c.setStrokeColor(HexColor(color));c.setLineWidth(lw);c.line(x1,H-y1,x2,H-y2)
 def text(self,s,x,y,size=11,font='Serif',color=INK):
  self.c.setFont(font,size);self.c.setFillColor(HexColor(color));self.c.drawString(x,H-y-size*.78,s);textlog.append(s)
 def para(self,s,x,y,w,size=11.3,font='Serif',color=INK,leading=None,maxh=None):
  style=ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.3,textColor=HexColor(color),spaceAfter=0,allowWidows=0,allowOrphans=0)
  p=Paragraph(s,style);_,h=p.wrap(w,H)
  if maxh is not None and h>maxh+.1:raise ValueError(f'Overflow page {self.n}: {h:.1f}>{maxh}: {s[:80]}')
  if y+h>H-34:raise ValueError(f'Bottom overflow page {self.n}: y={y}, h={h}: {s[:60]}')
  p.drawOn(self.c,x,H-y-h);textlog.append(re.sub('<[^>]+>','',s));return h
 def dropcap(self,s,x,y,w,size=11.3,leading=14.5,maxh=None):
  initial=s[0]; rest=s[1:]; inset=37; first_height=leading*3+1
  style=ParagraphStyle('drop',fontName='Serif',fontSize=size,leading=leading,textColor=HexColor(INK),allowWidows=1,allowOrphans=1)
  p=Paragraph(rest,style);p.wrap(w-inset,H);chunks=p.split(w-inset,first_height)
  if not chunks:raise ValueError('drop cap paragraph too short')
  first=chunks[0];_,fh=first.wrap(w-inset,first_height)
  cap_size=min(36,(fh-5)/.78,31/pdfmetrics.stringWidth(initial,'SerifBold',1))
  self.rect(x,y+1,32,fh-4,PALE);self.text(initial,x+1,y+1,cap_size,'SerifBold',RED)
  self.line(x,y+fh-1,x+32,y+fh-1,GREEN,.65)
  first.drawOn(self.c,x+inset,H-y-fh);total=fh
  for remainder in chunks[1:]:
   _,rh=remainder.wrap(w,H);remainder.drawOn(self.c,x,H-y-total-rh);total+=rh
  if maxh is not None and total>maxh+.1:raise ValueError(f'Drop cap overflow {self.n}: {total}>{maxh}')
  textlog.append(re.sub('<[^>]+>','',s));return total
 def image(self,name,x,y,w,h=None):
  stem=Path(name).stem; is_shot=stem in ('probes-cards','modular-focus','fumola-scene')
  path=ASSETS/(stem+'-'+self.treatment+'.png') if is_shot else ASSETS/name
  reference=ASSETS/(stem+'-clean.png') if is_shot else path
  iw,ih=Image.open(reference).size;h=h or w*ih/iw
  if is_shot:
   assert Image.open(path).format=='PNG',f'Expected real PNG: {path}'
   self.rect(x-7,y-7,w+14,h+14,'#FCF7EB',GREEN,.75)
   self.rect(x-3,y-3,w+6,h+6,'#FCF7EB',LINE,.35)
  self.c.drawImage(str(path),x,H-y-h,width=w,height=h,mask='auto')
  if is_shot:
   for xx,yy,dx,dy in [(x-7,y-7,1,1),(x+w+7,y-7,-1,1),(x-7,y+h+7,1,-1),(x+w+7,y+h+7,-1,-1)]:
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
   self.text('R2 / '+('WOODCUT STUDY' if self.treatment=='woodcut' else 'CLEAN PLATES'),298,H-20,6.5,'Mono',ink);self.text(f'{self.n:02d}',W-M-12,H-20,7,'Mono',ink)
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
 z.text('04-10 SEPTEMBER 2026',M,180,8.8,'Mono');z.text('PILOT / ABOUT 10 MINUTES',293,180,8.8,'Mono')
 z.image('drawer-tree.png',0,208,W,360)
 z.rect(25,545,383,55,PAPER);z.text('The cabinet is open.',36,553,32,'SerifBold')
 z.para('Probes IV lands. Modules grow another floor. A foreign runtime moves in. The experiments have experiments.',M,618,CW,size=17,leading=20,maxh=49)
 z.text('REVISION 2 / '+('WOODCUT SCREENSHOT STUDY' if z.treatment=='woodcut' else 'CLEAN SCREENSHOT EDITION'),M,692,7.5,'Mono')

def lead(z):
 z.page('The big landing');z.title('A little more room<br/>to see what happens.', 'MERGED INTO DEV / PROBES IV',size=33)
 z.image('probes-cards.png',M,157,CW)
 z.para(('Woodcut facsimile of a <b>dev</b> capture. ' if z.treatment=='woodcut' else 'Lossless <b>dev</b> capture. ')+'Insertion sort, with intermediate hands displayed as cards. The renderer arrived here from Alexander\'s work; these are runtime values beside the program.',M,453,CW,size=8.7,font='Sans',leading=11.3,maxh=36)
 a='On September 8, Andrew Blinn\'s long-running <b>Probes IV</b> branch became part of <b>dev</b>, merged by Cyrus Omar. The headline is a drawer: a sample can unfold into a multiline view below its source line. A cramped chip gets a room of its own.<br/><br/>Auto-probe also grows from a switch into <b>Off / Caret / All</b>. Rich views can appear inside the sample display, and a quieter green palette makes focus easier to follow.'
 b='The less photogenic fixes matter just as much. Newly placed probes should show values without waiting for another edit. Step-into reaches indirect calls. Sample navigation scrolls with the selection. Menus move from overeager hover to right- or alt-click.<br/><br/>Try <b>Documentation → Cards</b> on dev. Then open a sample drawer. This is the week\'s biggest change to the everyday feel of Hazel.'
 z.dropcap(a,M,495,222,size=11,leading=14,maxh=168);z.para(b,282,495,222,size=11,leading=14,maxh=155)
 z.sources([('#2363: features, review & merge',pr(2363)),('Try dev','https://hazel.org/build/dev/')],y=673)

def aftermath(z):
 z.page('After the landing');z.title('And then the drawer<br/>had a few complaints.','FOLLOW-UPS / STILL OPEN',size=34)
 z.para('A landing is an event. Settling in takes longer.',M,152,CW,size=17,font='SerifItalic')
 z.label('01 / INTERACTION',M,192);z.label('02 / PERFORMANCE',282,192)
 z.para('Menus lose their<br/>footing.',M,212,222,size=23,font='SerifBold',leading=24)
 z.para('Recursion gets<br/>expensive.',282,212,222,size=23,font='SerifBold',leading=24)
 z.para('Reports <b>#2519-2521</b> describe rich-table drawer trouble: a hidden table still has a “Hide table” menu, sample context menus are hard to reach, and a column menu can anchor below the whole drawer. Small slips in where controls appear become large interruptions when you are following a value.',M,272,222,size=11.2,leading=14.5,maxh=115)
 z.para('Issue <b>#2524</b> reports a Probes IV regression: ascription bookkeeping grows with call-stack depth. In the reporter’s CLI example, 12,800 recursive calls run out of memory after the merge; the pre-merge version completes. This is a reported regression, not an independent benchmark.',282,272,222,size=11.2,leading=14.5,maxh=115)
 z.line(M,390,504,390,LINE,.6)
 z.label('03 / TEST SIGNAL',M,409);z.label('AT THE WORKBENCH',282,409,color=GREEN)
 z.para('A green build<br/>with an asterisk.',M,430,222,size=22,font='SerifBold',leading=23)
 z.para('Merged <b>#2482</b> disables two intermittent evaluator properties, keeps their bodies compiling, and adds deterministic checks for known disagreements. The underlying bugs remain open. The test signal changed; those bugs did not vanish.',M,487,222,size=10.7,leading=13.5,maxh=83)
 z.dropcap('Matthew’s review of #2482 says a good Fumola change had been reverted after an unrelated flaky test failed. That gives a noisy test a very concrete cost: a useful change is removed, someone must trace the failure, and the experiment waits. Better diagnostics protect branch work as well as dev.',282,438,222,size=11,leading=14,maxh=130)
 z.rect(M,588,CW,58,PALE)
 for i,(value,label) in enumerate([('12','issues opened'),('4','issues closed'),('344','issues outstanding*')]):
  x=M+12+i*154;z.text(value,x,594,29,'SerifBold',GREEN);z.text(label,x,630,8.2,'Sans')
 z.para('Flows: September 4-10 UTC. *Open backlog at the September 11 revision capture; not a historical end-of-week reconstruction.',M,653,CW,size=7.7,font='Sans',leading=9.5,maxh=20)
 z.sources([('#2519',issue(2519)),('#2520',issue(2520)),('#2521',issue(2521)),('#2524',issue(2524)),('#2482 & review',pr(2482)),('Open issues','https://github.com/hazelgrove/hazel/issues?q=is%3Aissue%20is%3Aopen')],y=675)

def modules(z):
 z.page('The branch garden');z.title('Modules, all the way up.','NINE DRAFT PRs / NOT A RELEASE',size=37)
 z.para('Alexander Bandukwala has built a nine-part staircase from real module values to a modular standard library. The higher floors are explicitly provisional.',M,122,CW,size=14.2,leading=18,maxh=56)
 z.label('A READING MAP, NOT NINE INDEPENDENT FEATURES',M,201,size=7.6)
 groups=[('1-3','A module gets an identity','Signatures, width matching, abstract members',[(2493,'values'),(2494,'width'),(2495,'sealing')]),('4-7','Make the edges behave','Module functions, errors, expectations, duplicates',[(2498,'functions'),(2500,'errors'),(2501,'nested'),(2503,'duplicates')]),('8-9','Try the language on itself','Modular implicits + a modular standard library',[(2508,'implicits'),(2510,'library')])]
 y=228
 for i,(no,title,sub,links) in enumerate(groups):
  x=M+i*14;w=CW-i*14;z.rect(x,y,w,80,[PALE,'#E9DEBD','#E8C7B4'][i]);z.text(no,x+13,y+14,26,'SerifItalic',GREEN);z.text(title,x+78,y+13,16,'SerifBold');z.text(sub,x+78,y+37,9,'Sans');z.para('  '.join(f'<link href="{pr(n)}" color="{GREEN}">#{n}</link>' for n,_ in links),x+78,y+57,w-90,size=8.5,font='Mono');y+=93
 z.para('The useful shift is conceptual: a module becomes a value with a signature, rather than a dressed-up labeled tuple. Width matching lets a richer module satisfy a smaller interface where an expected type is given. Abstract members give names such as <b>M.T</b> a meaningful boundary.',M,531,222,size=11.1,leading=14.5,maxh=109)
 z.para('Upstairs, the drafts ask what implicit module arguments and <b>List.map</b>-style library names could feel like. Parts 8 and 9 say they are not close to done. Missing sharing constraints, unresolved implicit-design questions and unmeasured library costs are part of the story.',282,531,222,size=11.1,leading=14.5,maxh=109)
 z.sources([('Start at #2493',pr(2493)),('Read the caveats in #2508',pr(2508)),('Library sketch #2510',pr(2510))],y=667)

def agent(z):
 z.page('Aiject / the workspace');z.title('Give the work<br/>a place to happen.','DRAFT: MODULAR EDITORS + CONSTELLATION',size=34)
 z.image('modular-focus.png',M,155,CW)
 cap=('Woodcut treatment of a staged capture. ' if z.treatment=='woodcut' else 'Lossless capture, staged in <b>modular-editors</b>. ')
 z.para(cap+'One function from Mega 1k, eight probe samples, and the whole-program result <b>true</b>. We added the probe. This is an experimental branch.',M,348,CW,size=8.5,font='Sans',leading=11,maxh=34)
 z.dropcap('Andrew’s agent-facing work is becoming a place you can look around. <b>Modular editors</b> lets a definition occupy the editing surface while its program keeps supplying context, results and tests. A recent fix makes edits beyond the first definition feed whole-program evaluation.',M,398,222,size=11.1,leading=14.2,maxh=122)
 z.para('<b>Constellation</b> maps type aliases to nodes and functions to edges; values dock beside their types, and tests attach to functions they mention. An avatar follows edits. The draft combines several branches, so its diff is not all new canvas code. Its preview returned 404; the source supplies the rules for the explainer below.',282,398,222,size=11.1,leading=14.2,maxh=122)
 z.rect(M,540,CW,113,PALE,GREEN,.5);z.label('READ THE CARDS PROGRAM AS A MAP',M+11,550,color=GREEN,size=8)
 z.para('The same <b>Card</b> and <b>Hand</b> types from page 2. Two inputs combine before <b>insert</b>; <b>sort</b> maps a hand to another hand.',M+11,570,150,size=9.6,leading=12.5,maxh=72)
 def node(label,x,y,w=57):
  z.rect(x,y,w,22,'#FCF7EB',GREEN,.65);z.text(label,x+6,y+6,8.5,'Mono',INK)
 node('Card',217,572);node('Hand',217,607)
 # Product node extended to contain its second line, as an explicitly labeled tuple.
 z.rect(302,580,70,45,'#FCF7EB',GREEN,.65);z.text('(Card,',309,589,8.5,'Mono');z.text(' Hand)',309,603,8.5,'Mono')
 node('Hand',431,592)
 z.line(274,583,302,591,GREEN,.8);z.line(274,618,302,609,GREEN,.8);z.line(372,602,431,602,GREEN,1)
 z.line(425,598,431,602,GREEN,1);z.line(425,606,431,602,GREEN,1);z.text('insert',382,582,8.2,'Mono',RED)
 z.line(459,614,459,638,GREEN,.8);z.line(459,638,245,638,GREEN,.8);z.line(245,638,245,629,GREEN,.8)
 z.line(241,633,245,629,GREEN,.8);z.line(249,633,245,629,GREEN,.8);z.text('sort : Hand -> Hand',304,640,7.5,'Mono',RED)
 z.para('Editorial explainer of the extraction rules, not a rendering of the canvas UI.',M,659,CW,size=7.5,font='Sans',leading=9)
 z.sources([('Modular editors #2469',pr(2469)),('Constellation #2505',pr(2505)),('Graph rules','https://github.com/hazelgrove/hazel/blob/25c6c57790/src/web/app/canvas/CanvasGraph.re')],y=674)

def fumola(z):
 z.page('A visitor moves in');z.title('Two languages.<br/>One notebook.','OPEN PR / FUMOLA LIVELITS / EXPERIMENTAL',size=37)
 z.image('fumola-scene.png',M,166,CW)
 z.para(('Woodcut facsimile. ' if z.treatment=='woodcut' else '')+'A staged, running example on <b>fumola-livelit-mvp</b>: Fumola calculates a GCD and reads a named cell; Hazel receives <b>(6, 42)</b>. The shot shows the bridge working. It does not measure incremental reuse.',M,369,CW,size=8.8,font='Sans',leading=11.4,maxh=35)
 z.dropcap('Matthew Hammer\'s Fumola integration puts a foreign runtime inside a Hazel document. The interesting boundary is ownership: the livelit carries a name for state that lives elsewhere. Sharing an instance can mean sharing its store and history. Copying or reloading the document raises questions an ordinary slider never had to answer.',M,429,222,size=11.3,leading=14.5,maxh=138)
 z.para('The branch has already outgrown its original two-widget PR description: its current documentation names four livelits. The interface is still moving.<br/><br/>Two loader PRs merged this week, both <b>into the Fumola feature branch</b>. They add source fallback and content-addressed loading, plus a way to identify the runtime that actually loaded.',282,429,222,size=11.3,leading=14.5,maxh=153)
 z.rect(M,594,CW,54,PALE);z.para('<b>Small infrastructure, large consequence.</b> The runtime lives outside Hazel\'s repo and can change independently. The branch\'s runtime notes explicitly identify gaps in live integration testing. A content hash makes a surprise version diagnosable; it does not make the dependency pinned.',M+12,604,CW-24,size=10.3,leading=13,maxh=39)
 z.sources([('#2492',pr(2492)),('Branch merges #2504',pr(2504)),('#2509 & runtime notes',pr(2509)),('Try the preview','https://hazel.org/build/fumola-livelit-mvp/')],y=667)

def people(z):
 z.page('People & small things');z.title('Around the workbench.','RECURRING CHARACTERS / THIS WEEK\'S THREADS',size=35)
 people=[('Andrew Blinn','@disconcision','Probes IV reaches dev; modular editors, agent hardening and the canvas keep stretching the workspace around it. The recurring question: how much more of a live program can we keep in view?'),('Alexander Bandukwala','@7h3kk1d','Modules II is the big construction site. Alongside it: tutorial authoring, precise error reports, CI hygiene and the first reports of several probe regressions. A language grows; its seams become visible.'),('Matthew Hammer','@matthewhammer','Fumola livelits and the Wasm spike both cross runtime boundaries. Loader fixes, benchmark corrections and a review tracing a flaky test to a needless revert make the costs concrete.'),('Cyrus Omar','@cyrus-','Merged Probes IV and opened the dependency update that also landed on dev. This week\'s role in the story is the point where branch work becomes shared ground.')]
 y=126
 for name,handle,body in people:
  z.text(name,M,y,18,'SerifBold');z.text(handle,314,y+3,8.5,'Mono',MUTED);z.para(body,M,y+28,CW,size=11.1,leading=14.3,maxh=44);z.line(M,y+82,504,y+82,LINE,.5);y+=98
 z.label('SMALL THING, REAL CONSEQUENCE',M,534)
 z.para('A missing blank in a lesson',M,554,CW,size=23,font='SerifBold')
 z.para('The tutorial stack moves lessons into readable .hzt text and folders, including three recovered Gradebook tasks. Along the way, #2518 records a tiny betrayal: <b>[¿]</b> reloads as <b>[]</b>. The workaround uses an explicit hole, which a learner must select and replace instead of simply typing into a gap. A persistence detail becomes a teaching detail.',M,590,CW,size=11.1,leading=14.3,maxh=60)
 z.sources([('#2363',pr(2363)),('#2493',pr(2493)),('#2492',pr(2492)),('#2511',pr(2511)),('Tutorials #2485',pr(2485)),('#2513',pr(2513)),('#2518',issue(2518))],y=669)

def stats(z):
 z.page('The instrument panel');z.title('A busy week.<br/>An imperfect instrument.','REPOSITORY ACTIVITY / UTC WINDOW',size=33)
 vals=[('23','PRs opened'),('13','of those are drafts*'),('5','PRs merged'),('65','recent branch tips**')]
 for i,(v,l) in enumerate(vals):
  x=M+i*119;z.rect(x,154,111,69,PALE);z.text(v,x+10,159,33,'SansBold',GREEN);z.text(l,x+9,202,7.7,'Sans')
 z.para('The 5 merges: 3 into dev, 2 into fumola-livelit-mvp. *Draft state at retrieval.<br/>**Tip committer dates fall in the week; this is not a count of branch pushes.',M,234,CW,size=8.8,font='Sans',leading=12,maxh=28)
 z.text('VISIBLE CLAUDE CO-AUTHOR CREDITS',M,281,8.4,'Mono');z.text('277 / 382',M,303,31,'SerifBold',GREEN)
 z.para('unique reachable commit objects carry a Claude co-author trailer (72.5%). Among 294 non-merge objects, 271 carry one (92.2%).',228,301,276,size=10.1,font='Sans',leading=13,maxh=43)
 z.label('DAILY COMMIT OBJECTS / SEPTEMBER 2026',M,359,size=7.5,color=INK)
 chart_y=482;scale=.72
 for i,(day,v) in enumerate(metrics['daily'].items()):
  x=M+15+i*65;total=v['total'];a=v['claude'];z.rect(x,chart_y-total*scale,34,total*scale,'#C3C5B9');z.rect(x,chart_y-a*scale,34,a*scale,GREEN)
  z.text(str(total),x+4,chart_y-total*scale-16,9,'Mono');z.text(day[-2:],x+10,494,8,'Mono')
 z.rect(M,517,9,9,GREEN);z.text('Claude credited',M+15,518,8.5,'Sans');z.rect(180,517,9,9,'#C3C5B9');z.text('No Claude trailer',195,518,8.5,'Sans')
 z.line(M,544,504,544,LINE,.6)
 z.para('<b>What the chart can say.</b> We counted commit objects reachable from 690 captured remote branch tips, filtered by committer timestamp, September 4-10 UTC. Shared SHAs count once. Rebases and cherry-picks can create different SHAs for similar work; 88 objects are merges. This is activity, not a productivity leaderboard.',M,558,222,size=10.3,leading=13,maxh=126)
 z.para('<b>What it cannot say.</b> 128 objects have a cryptographic signature header, not independently verified. That is separate from an agent credit. Zero OpenAI/Codex/ChatGPT co-author trailers were found; this does not establish zero use. Missing trailers mean assistance is unknown. Issue-flow and backlog counts live beside the reports on page 3.',282,558,222,size=10.3,leading=13,maxh=126)

def dispatch(z):
 z.page('Bench notes & the back room');z.title('The number got smaller.<br/>The claim got better.','WASM SPIKE / AUTHOR-REPORTED RESULTS',size=30)
 z.para('Matthew\'s Wasm thread first hits missing native stubs, then gets fixed-precision workloads running. A later correction settles on <b>3.0-4.1×</b>, roughly 3.5×, for these evaluator benchmarks. Both backends use js_of_ocaml 6.2.0; Node 22; 20 iterations; matching result checksums.',M,145,222,size=11.1,leading=14.3,maxh=115)
 z.para('That is a promising result with a carefully drawn fence. The workloads are textually tiny and compute-heavy. They exclude the editor and do not solve arbitrary-precision support. The branch still contains deliberate shortcuts, including livelit removal. Keep the speedup; keep the fence.',282,145,222,size=11.1,leading=14.3,maxh=115)
 z.rect(M,272,CW,45,INK);z.text('~3.5×',M+12,280,28,'SansBold',PAPER);z.para('The evaluator, on these workloads.<br/>No measured app-wide speedup.',184,282,299,size=11.5,font='Sans',color=PAPER,leading=14)
 z.label('UNFINISHED BUSINESS / AN ORIGINAL COMIC',M,349,color=RED)
 z.image('observable-comic.png',M,372,CW)
 z.para('Fictional characters and dialogue. Generated with ImageGen for this issue.',M,536,CW,size=8.3,font='Sans',color=MUTED)
 z.para('<b>Branch postcards.</b> <font name="Mono" size="9">resizable-type-probe</font> gives tuple types a shared abbreviation budget; <font name="Mono" size="9">fix/probe-rich-depth-clamp</font> frees rich chips from a one-row clamp. No matching PR was found for either at retrieval. Small adjustments, still branch work.',M,569,CW,size=10.8,leading=14,maxh=58)
 z.para('<b>Late wire:</b> Matthew also opened Blackboard MVP: a proof-assistant kernel and editor sort. Editor statics and tactics remain future work. Draft #2525.',M,633,CW,size=9.2,leading=11.5,maxh=26)
 z.sources([('Wasm correction',pr(2490)+'#issuecomment-5534741226'),('Type budget',commit('14aa84c23c')),('Rich depth',commit('e644dcb91b')),('Blackboard #2525',pr(2525))],y=673)

def back(z):
 z.page('Before next Friday');z.title('Leave a bookmark<br/>in the unfinished parts.','THE EDITOR’S DESK',size=35)
 z.para('The first issue starts in the middle. Here are the threads we intend to recognize when they return, and the changes that would earn another visit.',M,155,CW,size=14,leading=18,maxh=57)
 z.label('01 / AFTER THE LANDING',M,225,color=GREEN);z.label('02 / UP THE STAIRCASE',282,225,color=GREEN)
 z.dropcap('Watch the Probes IV follow-ups, especially the reported recursive-ascription regression. A repaired menu or a smoother sample interaction deserves a close-up: show the troublesome action, then what now happens instead. A resolved issue is most interesting when the reader can feel the difference.',M,252,222,size=11.3,leading=14.5,maxh=145)
 z.para('Return to Modules II when a design decision changes: sharing, implicit resolution, signature ergonomics. Nine draft titles alone should not buy nine more stories next week. A small program that benefits from the new boundary would tell us more than another picture of the staircase.',282,252,222,size=11.3,leading=14.5,maxh=145)
 z.line(M,398,504,398,LINE,.6)
 z.label('03 / TWO SHORES',M,420,color=GREEN);z.label('EARLIER IN THE SEASON',282,420,color=GREEN)
 z.para('Follow both sides of the Fumola runtime contract. A change in the external runtime can matter even when Hazel itself has no new commit. Next time, try to show reuse or a clear rule for copying state. Revisit the canvas when a working preview or a new interaction earns a new picture.',M,447,222,size=11.3,leading=14.5,maxh=142)
 z.para('August 21-September 3 supplies context, not this week’s totals. Unicode support, context-menu clipboard actions, parser/probe round-trip repairs and CI restructuring had already landed. Their maintenance work is part of the ground these larger experiments stand on. We will return when there is a fresh reason to look.',282,447,222,size=11.3,leading=14.5,maxh=142)
 z.line(M,587,504,587,GREEN,1)
 note=('This edition uses ImageGen woodcut facsimiles of the three new captures. Small glyph and card details may drift; the clean edition is the reference for exact UI and syntax.' if z.treatment=='woodcut' else 'The three screenshot plates are lossless browser PNG exports, captured at 180% zoom and retained at their native resolution. Frames belong to the page layout, not the application.')
 z.para('<b>Revision 2 / the print room.</b> '+note,M,604,CW,size=9.2,leading=11.5,maxh=38)
 z.para('<b>Colophon.</b> Edited by Astra for Andrew Blinn. GitHub PRs, issues, reviews, selected diffs and branch code; harvested September 11. Reporting window: September 4-10 UTC. Mutable prose, draft flags and live views reflect retrieval. Original ImageGen art; source-linked editorial diagrams. Benchmarks are attributed, not rerun. No Slack source was used.',M,650,CW,size=7.8,font='Sans',leading=9.6,maxh=35)


for treatment,filename in [("clean","week-in-hazel-001.pdf"),("woodcut","week-in-hazel-001-woodcut.pdf")]:
 z=Zine(OUT/filename,treatment)
 for fn in [cover,lead,aftermath,modules,agent,fumola,people,stats,dispatch,back]:fn(z)
 z.save()

s=Zine(OUT/'week-in-hazel-001-style-lab.pdf')
s.page('Field notes / direction A',paper='#F1F0E3',folio=False)
s.text('WEEK IN HAZEL / ART-DIRECTION STUDY A',M,25,8,'Mono',GREEN)
s.text('Field notes',M,66,50,'SerifItalic',GREEN);s.text('from the branch garden',M,124,22,'Serif',GREEN)
s.line(M,163,504,163,GREEN,.7);s.label('SPECIMEN 001 / MODULES II',M,183,color=GREEN)
s.image('drawer-tree.png',M,215,CW,312)
s.rect(327,479,177,85,'#E0E6D4');s.para('Nine draft PRs.<br/>One growing idea.<br/><br/><b>Still under cultivation.</b>',340,491,150,size=12,font='Serif',color=GREEN,leading=15)
s.para('A quieter treatment: botanical specimen sheet, generous margins, marginal numbers, one idea at a time. The unfinished system is something to observe closely.',M,587,CW,size=15,leading=19,maxh=59)
s.text('04-10 SEP 2026  /  TWO-PAGE THEME STUDY',M,685,8,'Mono',GREEN)
s.page('Field notes / names',paper='#F1F0E3',ink=GREEN)
s.title('Names that keep<br/>their meaning.','DRAFT MODULES / EXPERIMENTAL FUMOLA',size=36)
s.label('I. A BOUNDARY',M,169,color=GREEN);s.para('A sealed module gives an abstract type a path: <b>M.T</b>. The name says where its identity comes from, even when its representation stays hidden. Modules II is still working out the rules around that boundary.',M,191,222,size=12,leading=16,maxh=113)
s.label('II. A MEMORY',282,169,color=GREEN);s.para('A Fumola livelit names a runtime and, in one form, a thunk. Reusing that name can keep an edit attached to prior state. Copying or reloading raises a different question: which history should the new object inherit?',282,191,222,size=12,leading=16,maxh=113)
s.image('fumola-scene.png',M,335,CW)
s.para('FIELD OBSERVATION 02 / Real preview, staged source. The output is (6, 42). A successful boundary crossing, not a measurement of reuse.',M,538,CW,size=8.7,font='Mono',color=GREEN,leading=11.5,maxh=36)
s.para('The shared theme is an editorial reading: a name is doing more than labeling a thing. It is keeping track of what is allowed to stay the same.',M,593,CW,size=17,font='SerifItalic',color=GREEN,leading=21,maxh=65)
s.sources([('Abstract types #2495',pr(2495)),('Fumola #2492',pr(2492)),('Runtime identity #2509',pr(2509))],y=670)
s.page('Night shift / direction B',paper='#E9E7DF',folio=False)
s.rect(0,0,W,192,INK);s.text('WEEK IN HAZEL / ART-DIRECTION STUDY B',M,25,8,'Mono',PAPER)
s.text('NIGHT',M,54,70,'SansBold',PAPER);s.text('SHIFT',171,124,70,'SansBold',PAPER)
s.label('THE MACHINES HAVE A WORKBENCH',39,226,angle=3,bg=RED,color=PAPER,size=10)
s.para('277',M,276,460,size=116,font='SansBold',leading=110)
s.para('visible Claude co-author credits<br/>among 382 commit objects',M,407,CW,size=22,font='SansBold',leading=25)
s.line(M,480,504,480,INK,3)
s.para('No, this is not the percentage<br/>of Hazel “written by AI.”',M,505,CW,size=26,font='SerifItalic',leading=29,maxh=63)
s.para('It is a footprint in the metadata. Some work leaves one; some does not. Rebases, merges and cherry-picks also leave tracks. The interesting question is what people are building with the machines.',M,600,CW,size=13.5,leading=18,maxh=60)
s.text('PHOTOCOPY ENERGY / BLACK INK / VERMILION / DEADPAN',M,690,7.5,'Mono')
s.page('Night shift / observed',paper='#E9E7DF')
s.label('DRAFT WORKSPACE / OPEN AGENT HARDENING',M,52,angle=-1,color=RED)
s.title('Somewhere to watch<br/>the edits happen.',y=83,size=33)
s.image('modular-focus.png',M,181,CW)
s.para('A thousand-line program, one definition on the desk. The rest of the document keeps supplying live context. That is the attraction of modular editors; Constellation tries to give the moving work a map.',M,382,CW,size=13,leading=17,maxh=72)
s.label('FICTION DEPARTMENT',M,474,color=RED);s.image('observable-comic.png',M,499,CW)
s.sources([('Modular editors #2469',pr(2469)),('Constellation #2505',pr(2505)),('Hardening #2427',pr(2427))],y=672)
s.save()
(ROOT/'layout-manifest.json').write_text(json.dumps(pages,indent=2))
(ROOT/'typeset-text.txt').write_text('\n\n'.join(textlog))
print('Created clean, woodcut, and style-lab PDFs in',OUT)
