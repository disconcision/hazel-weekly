"""Reflow the finished zines for the personal-site archive; PDFs remain unchanged."""
from pathlib import Path
from datetime import datetime, timedelta
from html import escape, unescape
import json, re, shutil, sys
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DEST = Path(sys.argv[1]).resolve()
PILOT = json.loads((ROOT/'web/pilot-content.json').read_text())
AI_DISCLOSURE = 'All content is fully AI-generated from the Hazel Git repository and GitHub data.'
AI_DETAILS = 'Reporting, writing and illustrations are all AI-produced.'

def clean(s):
    s = re.sub(r'<link href="([^"]+)"[^>]*>', r'<a href="\1">', s).replace('</link>', '</a>')
    s = re.sub(r'<font[^>]*>', '', s).replace('</font>', '')
    return s

def plain(s):
    return unescape(re.sub('<[^>]+>', ' ', s)).strip()

def prose(s, cls='prose'):
    return '<div class="'+cls+'">'+''.join('<p>'+p+'</p>' for p in re.split(r'<br\s*/?><br\s*/?>', clean(s)))+'</div>'

def asset(slug, src):
    dst = DEST/'assets'/slug/src.name
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists(): shutil.copy2(src, dst)
    return '../../assets/'+slug+'/'+src.name

def figure(slug, src, caption, narrow=False):
    url=asset(slug, src)
    w,h=Image.open(src).size
    return '<figure'+(' class="narrow"' if narrow else '')+'><a href="'+url+'" aria-label="Open image at full resolution"><img loading="lazy" decoding="async" src="'+url+'" width="'+str(w)+'" height="'+str(h)+'" alt="'+escape(plain(caption),quote=True)+'"></a><figcaption>'+clean(caption)+'</figcaption></figure>'

def sources(links):
    return '<nav class="sources" aria-label="Article sources"><span>Sources</span>'+''.join('<a href="'+escape(url,quote=True)+'">'+escape(label)+'</a>' for label,url in links)+'</nav>' if links else ''

def slips(items, stats=False):
    return '<div class="'+('stat-grid' if stats else 'flow'+(' two' if len(items)==2 else ''))+'">'+''.join('<div class="paper-slip"><strong>'+clean(str(title))+'</strong><p>'+clean(body)+'</p></div>' for title,body in items)+'</div>'

def chart(rows, caption, signature=True):
    top=max(r[1] for r in rows) or 1
    bars=[]
    for day,total,credit,sig in rows:
        height=total/top*100
        bars.append('<div class="day"><span class="bar-count">'+str(total)+'</span><div class="bar-space"><div class="bar-total" style="height:'+str(height)+'%"><div class="bar-credit" style="height:'+str(credit/total*100 if total else 0)+'%"></div></div>'+('<span class="bar-signature" style="bottom:'+str(sig/top*100)+'%"></span>' if sig else '')+'</div><span class="bar-date">'+day[-2:]+'</span></div>')
    legend='Gray: all commit objects · Green: Claude co-author credit'+(' · Red tick: signature header' if signature else '')
    table='<details class="data"><summary>Daily counts as a table</summary><div class="table-wrap"><table><caption>Daily commit objects, UTC</caption><thead><tr><th scope="col">Date</th><th scope="col">All</th><th scope="col">Claude credit</th>'+('<th scope="col">Signature header</th>' if signature else '')+'</tr></thead><tbody>'+''.join('<tr><th scope="row">'+d+'</th><td>'+str(t)+'</td><td>'+str(c)+'</td>'+('<td>'+str(s)+'</td>' if signature else '')+'</tr>' for d,t,c,s in rows)+'</tbody></table></div></details>'
    return '<figure class="chart"><div class="bars" aria-hidden="true">'+''.join(bars)+'</div><figcaption>'+caption+'<br>'+legend+'</figcaption></figure>'+table

def article(key, section, title, kicker, body):
    if not re.fullmatch(r'[a-z][a-z0-9-]*', key):
        raise ValueError('Section anchors must be stable lowercase URL slugs: '+key)
    heading=clean(title).replace('<br/>',' ').replace('\n',' ')
    permalink='<a class="section-link" href="#'+key+'" title="Link to this section">'+heading+'<span class="section-link-mark" aria-hidden="true">#</span></a>'
    return '<section class="article" id="'+key+'" aria-labelledby="'+key+'-title"><p class="eyebrow">'+escape(section)+'</p><p class="eyebrow article-kicker">'+escape(kicker)+'</p><h2 id="'+key+'-title">'+permalink+'</h2>'+body+'</section>'

def page(slug, issue_id, title, date, deck, sections, retrospective=False, cover_src=None, cover_alt=None):
    keys=[key for key,_,_ in sections]
    if len(keys)!=len(set(keys)):
        raise ValueError('Duplicate section anchors in issue '+slug)
    dest=DEST/'issues'/slug
    dest.mkdir(parents=True, exist_ok=True)
    contents=''.join('<li><a href="#'+key+'">'+escape(plain(heading))+'</a></li>' for key,heading,_ in sections)
    notice='<aside class="ai-notice" aria-label="AI disclosure"><strong>'+AI_DISCLOSURE+'</strong><span>'+AI_DETAILS+'</span></aside>'
    cover_src=Path(cover_src) if cover_src else (ROOT/'assets/drawer-tree.png' if slug=='001' else ROOT/'back-issues'/slug/'assets/cover.png')
    cover_url=asset(slug,cover_src)
    cover_width,cover_height=Image.open(cover_src).size
    cover_alts={'001':'A tree growing from an open cabinet of drawers.','neg019':'Two paper feeds meet at a printing press.','neg060':'A pen and a mechanical pencil arm share a drafting desk.','neg100':'A bonsai tree with its roots connected to a new support.'}
    cover='<figure class="cover-leader"><a href="../../assets/covers/'+slug+'.png" aria-label="View the full printed cover of Issue '+issue_id+'"><img src="'+cover_url+'" width="'+str(cover_width)+'" height="'+str(cover_height)+'" fetchpriority="high" alt="Cover illustration: '+escape(cover_alt or cover_alts[slug],quote=True)+'"></a></figure>'
    html='''<!doctype html>
<html lang="en-US"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex"><meta name="description" content="'''+escape(deck,quote=True)+'''"><title>'''+escape(title)+' · Issue '+issue_id+''' · Week in Hazel</title><link rel="icon" href="../../assets/favicon.svg"><link rel="stylesheet" href="../../style.css"></head>
<body class="reader"><a class="skip-link" href="#reading">Skip to articles</a><div class="wrap"><header class="reader-top"><a class="brand" href="../../">Week in Hazel</a><a href="../../pdfs/week-in-hazel-'''+slug+'''.pdf">Read the PDF ↗</a></header>'''+notice+'''
<main id="reading"><div class="reader-hero">'''+cover+'''<header class="reader-title"><div class="reader-meta"><p class="eyebrow">Issue '''+issue_id+(' · Retrospective' if retrospective else ' · Pilot issue')+'''</p><p class="dates">'''+date+'''</p></div><div><h1>'''+escape(title)+'''</h1><p class="summary">'''+escape(deck)+'''</p></div></header></div>
<details class="contents"><summary>In this issue</summary><ol>'''+contents+'''</ol></details>'''+''.join(s[2] for s in sections)+'''</main><div class="reading-end"><a href="../../">← All issues</a></div><footer class="site-footer"><p>A small digest for the hazelnut community.</p><p>'''+('Retrospective edition · Produced September 2026' if retrospective else 'Issue '+issue_id+' · '+date)+'''</p></footer></div></body></html>'''
    (dest/'index.html').write_text(html)

def build_pilot():
    sections=[]
    for key,nodes in PILOT.items():
        get=lambda i: nodes[i]['args'][0]
        p=lambda i: prose(get(i))
        heading=lambda i: '<h3>'+clean(get(i)).replace('<br/>',' ')+'</h3>'
        eyebrow=lambda i: '<p class="eyebrow">'+escape(get(i))+'</p>'
        def shot(i,j):
            name=get(i)
            if name!='observable-comic.png': name=name.replace('.png','-woodcut.png')
            return figure('001',ROOT/'assets'/name,get(j),key=='constellation')
        if key=='lead': body=shot(2,3)+p(4)+p(5)
        elif key=='aftermath':
            body=prose(get(2),'intro')+eyebrow(3)+heading(5)+p(7)+eyebrow(4)+heading(6)+p(8)+eyebrow(9)+p(10)+p(11)+slips([(get(i),get(i+1)) for i in [12,14,16]],True)+prose(get(18),'note')
        elif key=='modules':
            body=prose(get(2),'intro')+eyebrow(3)+slips([(get(i)+' · '+get(i+1),get(i+2)+'<br>'+get(i+3)) for i in [4,8,12]])+p(16)+p(17)
        elif key in ['agent','fumola']: body=shot(2,3)+p(4)+p(5)+prose(get(6),'prose callout')
        elif key=='constellation': body=shot(2,3)+p(4)+p(5)+eyebrow(6)+p(7)+p(8)
        elif key=='people':
            body=''.join(heading(i)+'<p class="handle">'+escape(get(i+1))+'</p>'+p(i+2) for i in [2,5,8,11])+eyebrow(14)+heading(15)+p(16)+p(17)
        elif key=='stats':
            mt=json.loads((ROOT/'research/metrics.json').read_text())
            rows=[(d,v['total'],v['claude'],0) for d,v in mt['daily'].items()]
            body=slips([(get(i),get(i+1)) for i in [2,4,6,8]],True)+prose(get(10),'note')+eyebrow(11)+slips([(get(12),get(13))])+chart(rows,get(14),False)+p(31)+p(32)
        elif key=='dispatch': body=p(2)+p(3)+slips([(get(4),get(5))])+eyebrow(6)+shot(7,8)+p(9)+p(10)
        elif key=='back':
            body=prose(get(2),'intro')+''.join(eyebrow(label)+heading(h)+p(text) for label,h,text in [(3,5,7),(4,6,8),(9,11,13),(10,12,14)])+prose(get(15).replace('Screenshots are illustrated reproductions; the clean edition preserves exact UI.','Screenshots are illustrated reproductions.'),'credits')
        else: raise ValueError(key)
        body+=''.join(sources(n['args'][0]) for n in nodes if n['type']=='sources')
        title=nodes[1]['args'][0]
        sections.append((key,title,article(key,get(0),title,nodes[1]['args'][1],body)))
    page('001','001','The cabinet is open.','September 4–10, 2026','Probes IV reaches dev. Modules II tests new boundaries. Constellation becomes an editor. Fumola connects two runtimes.',sections)

DIAGRAMS={
 'startup': [('First display','The view exists; the one-time guard allows startup.'),('Startup action','Inject into the state machine; run on_startup.'),('Setup effects','Observers, command palette, clipboard and initial evaluation.')],
 'labels': [('Name-based matching','Fully labeled components can be aligned by name. Positions alone are no longer enough.'),('Positional meaning remains','Unlabeled components should keep their relative order. Mixed and duplicate cases need explicit rules.')],
 'assistant': [('Edit the program','Select structure; apply a tool-generated change.'),('Check remaining errors','Repair only if needed; error-round limit: two.'),('Name the chat','A separate summarization request after the first exchange.')],
 'indent': [('Actual program','An unfinished construct remains unfinished. No closing token is silently inserted.'),('Formatting sketch','Use the first following blank line, or segment end, as a provisional boundary.')],
 'elastatics': [('Inputs','Source expression + expected type.'),('Shared implementation','Check the form while building its elaboration.'),('Outputs','Elaborated expression + its static information.')],
 'pretty': [('Segment','Delimiter nesting; pieces retain their structural identity.'),('Layout document','Groups and breaks choose what fits the target width.'),('Reassembled tiles','Line breaks added; indentation handled downstream.')],
}
DIAGRAM_NOTES={
 'startup':'After initialization, later actions continue through the model/update/view path.',
 'labels':'Proposed test properties / labeled-tuple branch',
 'assistant':'Edit / repair path. Naming the chat is a separate purpose.',
 'indent':'A layout guess / not a program repair',
 'elastatics':'Expected type can affect the elaborated result',
 'pretty':'A formatter must preserve grouping as well as space',
}

def build_retrospectives():
    selection=json.loads((ROOT/'back-issues/selection.json').read_text())
    for entry in selection:
        slug=entry['slug']; base=ROOT/'back-issues'/slug
        meta=json.loads((base/'copy.json').read_text())
        sections=[]
        for i,p in enumerate(meta['pages']):
            body=''; typ=p['type']
            if typ=='diagram':
                body=slips(DIAGRAMS[p['diagram']])+prose(DIAGRAM_NOTES[p['diagram']],'note')
            elif typ in ['shot','comic']:
                body=figure(slug,base/'assets'/p.get('image','comic.png'),p['caption'])
            elif typ=='text': body=prose(p['dek'],'intro')
            elif typ=='stats':
                mt=json.loads((base/'research/metrics.json').read_text())
                body=slips([(mt['prs_opened'],'PRs opened'),(mt['prs_merged'],'PRs merged'),(mt['issues_opened'],'issues opened')],True)
                start=datetime.fromisoformat(entry['start'])
                days=[(start+timedelta(days=d)).strftime('%Y-%m-%d') for d in range(7)]
                rows=[(d,mt['daily'].get(d,0),mt['daily_claude_credits'].get(d,0),mt['daily_signature_headers'].get(d,0)) for d in days]
                body+=chart(rows,'Daily commit objects / week-end dev graph')
            else: raise ValueError(typ)
            body+=prose(p['left'])+prose(p['right'])
            if typ=='stats':
                body+=prose(f"{mt['commits']} unique objects; {mt['nonmerge']} non-merge. UTC committer dates; reachable from {mt['period_head'][:10]}. Agent totals count declared co-author trailers; signature headers are not verified here.",'note')
            body+=sources([('#'+str(n),'https://github.com/hazelgrove/hazel/pull/'+str(n)) for n in p.get('sources',[])]+[('#'+str(n),'https://github.com/hazelgrove/hazel/issues/'+str(n)) for n in p.get('issues',[])])
            key='article-'+str(i+1)
            sections.append((key,p['title'],article(key,p['section'],p['title'],p['kicker'],body)))
        dates={'neg019':'April 17–23, 2026','neg060':'July 4–10, 2025','neg100':'September 27–October 3, 2024'}
        page(slug,meta['id'],meta['title'],dates[slug],meta['deck'],sections,True)

if __name__=='__main__':
    build_pilot()
    build_retrospectives()
    print('Built four HTML editions in', DEST/'issues')
