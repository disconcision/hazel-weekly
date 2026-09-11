"""Historical editions, using the approved R5 native-art/browser-text system."""
from layout import *
from datetime import datetime,timedelta

def columns(z,p,y,maxh,size=11.15):
 # Drop initials only on text that starts with ordinary prose, never split markup.
 fn=z.para if p['left'].startswith('<') else z.dropcap
 fn(p['left'],M,y,222,size=size,leading=14.1,maxh=maxh)
 z.para(p['right'],282,y,222,size=size,leading=14.1,maxh=maxh)

def box(z,x,y,w,h,title,body,fill=PALE):
 z.paper_patch(x,y,w,h,fill,fold=12)
 z.text(title,x+10,y+9,12,'SerifBold')
 z.para(body,x+10,y+28,w-20,size=8.7,font='Sans',leading=11,maxh=h-32)

def arrow(z,x,y,x2,y2):
 z.sketch_line(x,y,x2,y2,GREEN,1)
 a=math.atan2(y2-y,x2-x)
 for d in [-.45,.45]:z.sketch_line(x2,y2,x2-6*math.cos(a+d),y2-6*math.sin(a+d),GREEN,1)

def diagram(z,key):
 y=160
 if key=='startup':
  box(z,36,y,134,72,'First display','The view exists; the one-time guard allows startup.')
  box(z,198,y+7,134,72,'Startup action','Inject into the state machine; run on_startup.','#E9DEBD')
  box(z,370,y-2,134,82,'Setup effects','Observers, command palette, clipboard and initial evaluation.','#E8C7B4')
  arrow(z,172,194,194,198);arrow(z,335,198,366,194)
  z.para('After initialization, later actions continue through the model/update/view path.',M,249,CW,size=8.5,font='Sans',leading=11,maxh=15)
 elif key=='labels':
  box(z,36,y,215,80,'Name-based matching','Fully labeled components can be aligned by name. Positions alone are no longer enough.')
  box(z,282,y+7,222,80,'Positional meaning remains','Unlabeled components should keep their relative order. Mixed and duplicate cases need explicit rules.','#E9DEBD')
  z.label('PROPOSED TEST PROPERTIES / LABELED-TUPLE BRANCH',M,254,size=7.5,color=GREEN)
 elif key=='assistant':
  box(z,36,y,137,74,'Edit the program','Select structure; apply a tool-generated change.')
  box(z,199,y+6,137,74,'Check remaining errors','Repair only if needed; error-round limit: two.','#E9DEBD')
  box(z,363,y,141,74,'Name the chat','A separate summarization request after the first exchange.','#E8C7B4')
  arrow(z,176,195,195,198)
  z.label('EDIT / REPAIR PATH',36,252,size=7.5,color=GREEN);z.label('SEPARATE PURPOSE',364,252,size=7.5,color=RED)
 elif key=='indent':
  box(z,36,y,222,85,'Actual program','An unfinished construct remains unfinished. No closing token is silently inserted.')
  box(z,282,y+6,222,85,'Formatting sketch','Use the first following blank line, or segment end, as a provisional boundary.','#E9DEBD')
  arrow(z,258,204,280,204)
  z.label('A LAYOUT GUESS / NOT A PROGRAM REPAIR',M,257,size=7.5,color=GREEN)
 elif key=='elastatics':
  box(z,36,y,132,80,'Inputs','Source expression + expected type.')
  box(z,197,y+5,141,80,'Shared implementation','Check the form while building its elaboration.','#E9DEBD')
  box(z,368,y,136,80,'Outputs','Elaborated expression + its static information.','#E8C7B4')
  arrow(z,171,200,193,202);arrow(z,340,202,364,200)
  z.label('EXPECTED TYPE CAN AFFECT THE ELABORATED RESULT',M,258,size=7.5,color=GREEN)
 elif key=='pretty':
  box(z,36,y,137,79,'Segment','Delimiter nesting; pieces retain their structural identity.')
  box(z,199,y+6,137,79,'Layout document','Groups and breaks choose what fits the target width.','#E9DEBD')
  box(z,363,y,141,79,'Reassembled tiles','Line breaks added; indentation handled downstream.','#E8C7B4')
  arrow(z,176,200,195,204);arrow(z,338,204,359,200)
  z.label('A FORMATTER MUST PRESERVE GROUPING AS WELL AS SPACE',M,258,size=7.5,color=GREEN)

def cover(z,m):
 z.page('cover',folio=False)
 z.text('A SMALL MAGAZINE ABOUT A VERY LIVE LANGUAGE',M,23,8,'Mono')
 z.text('Week in',M,55,30,'SerifItalic');z.text('HAZEL',M,91,85,'SansBold')
 z.label('ISSUE '+m['id'],394,63,angle=-4,bg=RED,color=PAPER,size=10)
 z.text(m['date'],M,180,8.5,'Mono');z.text('RETROSPECTIVE',388,180,8.5,'Mono')
 z.image('cover.png',0,208,W,360)
 title=m['title'];sz=29 if len(title)>22 else 36
 tw=pdfmetrics.stringWidth(title,'SerifBold',sz)
 z.paper_patch(26,548,min(490,tw+24),57,PAPER,fold=8,grain=False)
 z.text(title,36,558,sz,'SerifBold')
 z.para(m['deck'],M,626,CW,size=16.4,leading=20,maxh=61)
 z.text('THE WEEK AS IT STOOD / MADE SEPTEMBER 2026',M,695,7.5,'Mono')

def stats(z,m,p):
 mt=json.loads((ROOT/m['slug']/'research/metrics.json').read_text())
 vals=[(mt['prs_opened'],'PRs opened'),(mt['prs_merged'],'PRs merged'),(mt['issues_opened'],'issue opened' if mt['issues_opened']==1 else 'issues opened')]
 for i,(v,label) in enumerate(vals):
  x=36+i*160;z.paper_patch(x,157,148,68,PALE,fold=12);z.text(str(v),x+12,163,32,'SerifBold',GREEN);z.text(label,x+12,202,9,'Sans')
 z.label('DAILY COMMIT OBJECTS / WEEK-END DEV GRAPH',M,245,size=8,color=INK)
 start=datetime.fromisoformat(next(v for v in selection if v['slug']==m['slug'])['start'])
 days=[(start+timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
 top=max(mt['daily'].values());base=373;scale=84/top
 for i,d in enumerate(days):
  n=mt['daily'].get(d,0);x=48+i*65;z.ink_bar(x,base-n*scale,33,n*scale,'#C3C5B9');a=mt['daily_claude_credits'].get(d,0);sig=mt['daily_signature_headers'].get(d,0);z.ink_bar(x,base-a*scale,33,a*scale,GREEN)
  if sig:z.line(x-2,base-sig*scale,x+35,base-sig*scale,RED,1.1)
  z.text(str(n),x+8,base-n*scale-15,9,'Mono');z.text(d[-2:],x+8,base+10,8,'Mono')
 z.sketch_line(M+5,base+.5,501,base+.5,LINE,.6)
 z.text('Gray: all objects  /  Green: Claude credit  /  Red tick: signature header',M,395,7.2,'Sans')
 columns(z,p,418,224,size=10.65)
 z.para(f"{mt['commits']} unique objects; {mt['nonmerge']} non-merge. UTC committer dates; reachable from {mt['period_head'][:10]}. Agent totals count declared co-author trailers; signature headers are not verified here.",M,648,CW,size=7.6,font='Sans',leading=9.5,maxh=25)

def page(z,m,p):
 z.page(p['section']);z.title(p['title'].replace('\n','<br/>'),p['kicker'],size=33)
 typ=p['type']
 if typ=='shot':
  h=z.image(p['image'],M,153,CW)
  if h>239:raise ValueError('Screenshot too tall '+m['slug'])
  cy=153+h+7
  ch=z.para(p['caption'],M,cy,CW,size=8.4,font='Sans',leading=10.8,maxh=35)
  y=cy+ch+12;columns(z,p,y,665-y,size=11.1)
 elif typ=='diagram':
  diagram(z,p['diagram']);columns(z,p,287,378,size=11.1)
 elif typ=='text':
  h=z.para(p['dek'],M,153,CW,size=13.6,leading=17.5,maxh=58)
  z.sketch_line(M,153+h+11,504,153+h+11,LINE,.6)
  y=153+h+28;columns(z,p,y,665-y,size=11.15)
 elif typ=='stats':stats(z,m,p)
 elif typ=='comic':
  z.image('comic.png',26,153,488)
  z.para(p['caption'],M,324,CW,size=8.4,font='Sans',leading=10.8,maxh=34)
  columns(z,p,367,298,size=10.9)
 links=[('#'+str(n),pr(n)) for n in p.get('sources',[])]+[('#'+str(n),issue(n)) for n in p.get('issues',[])]
 z.sources(links,y=674)

selection=json.loads((ROOT/'selection.json').read_text())
for entry in selection:
 meta=json.loads((ROOT/entry['slug']/'copy.json').read_text())
 z=Zine(OUT/f"week-in-hazel-{meta['slug']}.pdf",meta)
 cover(z,meta)
 for p in meta['pages']:page(z,meta,p)
 z.save()
(ROOT/'typeset-text.txt').write_text('\n\n'.join(textlog))
(ROOT/'pages.json').write_text(json.dumps(pages,indent=2))
LAYER.finish()
if not os.environ.get('HAZEL_ZINE_MEASURED_PASS'):
 env=dict(os.environ,HAZEL_ZINE_MEASURED_PASS='1');subprocess.run([sys.executable,__file__],check=True,env=env)
