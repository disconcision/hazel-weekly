#!/usr/bin/env python3
"""Build the unpublished Issue -058 PDF and readable HTML edition."""
from __future__ import annotations

import html
import json
import math
import os
import random
import re
import shutil
from pathlib import Path

from PIL import Image
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
OUT = REPO / "output" / "pdf"
WEB = ROOT / "web"
ASSETS = ROOT / "assets"
W, H, M = 540, 720, 36
CW = W - 2 * M
PAPER, INK, GREEN, RED = "#F3EBDD", "#222A23", "#355B43", "#BB3E27"
MOSS, GOLD, PALE, LINE = "#708B63", "#D0A648", "#DCE2CC", "#B6B9A7"


def find_font(filename: str) -> Path:
    explicit = os.environ.get("HAZEL_ZINE_FONT_DIR")
    candidates = []
    if explicit:
        candidates.append(Path(explicit) / filename)
    runtime = os.environ.get("CODEX_PRIMARY_RUNTIME_ROOT")
    if runtime:
        candidates.extend(Path(runtime).rglob(filename))
    candidates.extend(Path("/opt/codex/runtimes/codex-primary-runtime").rglob(filename))
    for path in candidates:
        if path.is_file():
            return path
    raise FileNotFoundError(f"Font not found: {filename}; set HAZEL_ZINE_FONT_DIR")


for name, filename in [
    ("Serif", "LinLibertine_R_G.ttf"),
    ("SerifBold", "LinLibertine_RB_G.ttf"),
    ("SerifItalic", "LinLibertine_RI_G.ttf"),
    ("Sans", "Rubik-Regular.ttf"),
    ("SansBold", "Rubik-Bold.ttf"),
    ("Mono", "LiberationMono-Regular.ttf"),
]:
    pdfmetrics.registerFont(TTFont(name, str(find_font(filename))))

pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="SerifBold", italic="SerifItalic")
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="SansBold")


def rich(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\$hole|\^\^probe\(1 \+ 1\)|\$==|==\.|assoc_opt", lambda m: f'<font name="Mono">{m.group(0)}</font>', text)
    return text


class Zine:
    def __init__(self, path: Path, meta: dict):
        self.path = path
        self.meta = meta
        self.c = canvas.Canvas(str(path), pagesize=(W, H), pageCompression=1)
        self.c.setTitle(f"Week in Hazel | Issue {meta['id']} | {meta['title']}")
        self.c.setAuthor("Astra (AI editor); ImageGen (illustrations)")
        self.page_number = 0
        self.qa = []

    def rect(self, x, y, w, h, fill, stroke=None, lw=.5):
        self.c.setFillColor(HexColor(fill)); self.c.setStrokeColor(HexColor(stroke or fill)); self.c.setLineWidth(lw)
        self.c.rect(x, H-y-h, w, h, fill=1, stroke=int(stroke is not None))

    def line(self, x1, y1, x2, y2, color=INK, lw=.7):
        self.c.setStrokeColor(HexColor(color)); self.c.setLineWidth(lw); self.c.line(x1, H-y1, x2, H-y2)

    def text(self, value, x, y, size=10, font="Serif", color=INK):
        self.c.setFont(font, size); self.c.setFillColor(HexColor(color)); self.c.drawString(x, H-y-size*.78, value)

    def para(self, value, x, y, w, size=10.4, leading=13.1, font="Serif", color=INK, maxh=None):
        style = ParagraphStyle("p", fontName=font, fontSize=size, leading=leading, textColor=HexColor(color), alignment=TA_LEFT, spaceAfter=0, splitLongWords=False)
        p = Paragraph(value, style); _, height = p.wrap(w, H)
        if maxh is not None and height > maxh + .2:
            raise ValueError(f"Page {self.page_number} paragraph overflow: {height:.1f}>{maxh:.1f}: {value[:80]}")
        p.drawOn(self.c, x, H-y-height)
        return height

    def paper_patch(self, x, y, w, h, fill=PALE):
        rng = random.Random(int(x*37+y*53+w*7+h*11))
        pts = []
        for i in range(13):
            t=i/12; pts.append((x+w*t, y+rng.uniform(-2.2,2.2)))
        for i in range(1,5): pts.append((x+w+rng.uniform(-2.1,2.1),y+h*i/4))
        for i in range(13):
            t=1-i/12; pts.append((x+w*t,y+h+rng.uniform(-2.2,2.2)))
        for i in range(1,5): pts.append((x+rng.uniform(-2.1,2.1),y+h*(1-i/5)))
        self.c.saveState(); self.c.setFillColor(HexColor(INK)); self.c.setFillAlpha(.10)
        for off, col, alpha in [(1.3, INK, .10), (0, fill, 1)]:
            self.c.setFillColor(HexColor(col)); self.c.setFillAlpha(alpha); path=self.c.beginPath(); path.moveTo(pts[0][0]+off,H-(pts[0][1]+off))
            for px,py in pts[1:]: path.lineTo(px+off,H-(py+off))
            path.close(); self.c.drawPath(path,fill=1,stroke=0)
        self.c.restoreState()

    def page(self, section, folio=True):
        if self.page_number: self.c.showPage()
        self.page_number += 1; self.rect(0,0,W,H,PAPER)
        rng=random.Random(500+self.page_number); self.c.setFillColor(HexColor(INK)); self.c.setFillAlpha(.045)
        for _ in range(900):
            x=rng.random()*W; y=rng.random()*H; self.c.circle(x,y,rng.uniform(.08,.27),fill=1,stroke=0)
        self.c.setFillAlpha(1)
        if folio:
            self.text("WEEK IN HAZEL",M,20,7.3,"Mono"); self.text(section.upper(),260,20,7.3,"Mono")
            self.line(M,36,W-M,36); self.line(M,H-29,W-M,H-29)
            self.text(f"{self.meta['id']}  /  {self.meta['date']}",M,H-20,7,"Mono")
            self.text(f"{self.page_number:02d}",W-M-12,H-20,7,"Mono")

    def title(self, page):
        self.text(page["kicker"],M,50,7.8,"Mono",RED)
        return self.para(page["title"],M,69,CW,31,31,"SerifBold",maxh=66)

    def image(self, filename, x, y, w, h=None):
        path=ASSETS/filename; im=Image.open(path); assert im.format=="PNG"
        iw,ih=im.size; h=h or w*ih/iw; self.c.drawImage(str(path),x,H-y-h,width=w,height=h,mask="auto",preserveAspectRatio=True)
        return h

    def sources(self, page, y=672):
        links=[]
        for n in page.get("sources",[]): links.append((f"PR #{n}",f"https://github.com/hazelgrove/hazel/pull/{n}"))
        for n in page.get("issues",[]): links.append((f"issue #{n}",f"https://github.com/hazelgrove/hazel/issues/{n}"))
        line="  /  ".join(f'<a href="{u}" color="{GREEN}"><u>{t}</u></a>' for t,u in links)
        self.para(line,M,y,CW,7.4,9,"Sans",maxh=22)

    def draw_columns(self, paras, y, max_y=660, size=10.35, leading=13.05):
        cols=[[],[]]; heights=[0,0]
        for raw in paras:
            formatted=rich(raw)
            style=ParagraphStyle("measure",fontName="Serif",fontSize=size,leading=leading,spaceAfter=0,splitLongWords=False)
            p=Paragraph(formatted,style); _,h=p.wrap(222,H); h+=7
            idx=0 if heights[0]<=heights[1] else 1; cols[idx].append((formatted,h)); heights[idx]+=h
        for idx, items in enumerate(cols):
            yy=y; x=M+idx*246
            for formatted,h in items:
                actual=self.para(formatted,x,yy,222,size,leading,"Serif",maxh=max_y-yy); yy+=actual+7
            if yy>max_y+1: raise ValueError(f"Page {self.page_number} column overflow: {yy:.1f}>{max_y}")

    def save(self):
        self.c.save()


def draw_cover(z: Zine, meta: dict):
    z.page("cover",folio=False)
    z.text("A SMALL MAGAZINE ABOUT A VERY LIVE LANGUAGE",M,23,8,"Mono")
    z.text("Week in",M,54,29,"SerifItalic"); z.text("HAZEL",M,90,83,"SansBold")
    z.paper_patch(396,58,105,27,RED); z.text("ISSUE -058",408,67,10,"Mono",PAPER)
    z.text(meta["date"],M,180,8.5,"Mono"); z.text("RETROSPECTIVE",388,180,8.5,"Mono")
    z.image("cover.png",0,208,W,360)
    z.paper_patch(25,548,480,56,PAPER); z.para(meta["title"],36,558,466,30,31,"SerifBold",maxh=47)
    z.para(meta["deck"],M,622,CW,14.2,17.1,"Serif",maxh=60)
    z.text("THE WEEK AS IT STOOD / MADE SEPTEMBER 2026",M,696,7.4,"Mono")


def draw_lead(z: Zine, page: dict):
    z.page(page["section"]); z.title(page)
    z.para(page["dek"],M,136,CW,13.5,17,"Serif",maxh=42)
    y=198
    boxes=[(M,104,"ZIPPER","unfinished tiles"),(220,104,"LOCAL","next edit"),(380,124,"GLOBAL","display list")]
    for x,w,t,b in boxes:
        z.paper_patch(x,y,w,60,PALE); z.text(t,x+10,y+10,11,"SerifBold"); z.text(b,x+10,y+32,8.2,"Sans")
    z.line(143,228,216,228,GREEN,1.1); z.line(324,228,376,228,GREEN,1.1)
    z.text("derive",164,214,7.1,"Mono",RED); z.text("derive",334,214,7.1,"Mono",RED)
    z.draw_columns(page["body"],287,660,10.25,12.85); z.sources(page)


def draw_shot(z: Zine, page: dict, tall=False):
    z.page(page["section"]); z.title(page)
    if tall:
        ih=z.image(page["image"],M,139,210)
        z.para(page["caption"],M,145+ih,210,7.5,9.2,"Sans",maxh=60)
        y=139; x=282; yy=y
        for raw in page["body"]:
            h=z.para(rich(raw),x,yy,222,10.3,13,"Serif",maxh=660-yy); yy+=h+8
        if yy>660: raise ValueError("Tall-shot copy overflow")
    else:
        ih=z.image(page["image"],M,139,CW)
        z.para(page["caption"],M,145+ih,CW,7.7,9.4,"Sans",maxh=40)
        z.draw_columns(page["body"],190+ih,660,10.25,12.85)
    z.sources(page)


def draw_text(z: Zine, page: dict, code=False):
    z.page(page["section"]); z.title(page)
    y=138
    if page.get("dek"):
        h=z.para(page["dek"],M,y,CW,13.2,16.5,"Serif",maxh=45); y+=h+18
    if code:
        z.paper_patch(M,y,CW,98,"#E6DDC4")
        yy=y+12
        for line in page["code"].splitlines():
            z.text(line,M+13,yy,9,"Mono",GREEN if line.startswith("^^") else INK); yy+=15
        y+=116
    z.draw_columns(page["body"],y,660,10.35,13.05); z.sources(page)


def draw_stats(z: Zine, page: dict, metrics: dict):
    z.page(page["section"]); z.title(page)
    vals=[(metrics["prs_opened"],"PRs opened"),(metrics["prs_merged"],"PRs merged"),(metrics["issues_opened"],"issues opened")]
    for i,(v,label) in enumerate(vals):
        x=M+i*160; z.paper_patch(x,142,148,64,PALE); z.text(str(v),x+12,150,29,"SerifBold",GREEN); z.text(label,x+12,183,8.5,"Sans")
    z.text("DAILY COMMIT OBJECTS / WEEK-END DEV GRAPH",M,229,7.7,"Mono",RED)
    daily=metrics["daily"]; top=max(daily.values()); base=365
    for i,(day,count) in enumerate(sorted(daily.items())):
        x=49+i*65; h=104*count/top; z.rect(x,base-h,33,h,"#C3C5B9")
        if metrics["daily_signature_headers"].get(day):
            sig=metrics["daily_signature_headers"][day]; sh=104*sig/top; z.line(x-2,base-sh,x+35,base-sh,RED,1.1)
        z.text(str(count),x+9,base-h-14,8.5,"Mono"); z.text(day[-2:],x+9,base+9,8,"Mono")
    z.line(M,base+.5,W-M,base+.5,LINE,.6)
    z.text("Gray: all objects / red tick: objects with signature headers",M,387,7.2,"Sans")
    z.draw_columns(page["body"],414,658,10.25,12.85); z.sources(page)


def draw_comic(z: Zine, page: dict):
    z.page(page["section"]); z.title(page)
    ih=z.image(page["image"],26,139,488)
    z.para(page["caption"],M,146+ih,CW,7.7,9.4,"Sans",maxh=32)
    z.draw_columns(page["body"],184+ih,660,10.15,12.75); z.sources(page)


def build_html(meta: dict):
    WEB.mkdir(parents=True,exist_ok=True); web_assets=WEB/"assets"; web_assets.mkdir(exist_ok=True)
    for name in ["cover.png","comic.png","unused-variable-warnings-stamp.png","backpack-scrollbar-regression-stamp.png"]:
        shutil.copy2(ASSETS/name,web_assets/name)
    for name in ["unused-variable-warnings.png","backpack-scrollbar-regression.png"]:
        shutil.copy2(ASSETS/"originals"/name,web_assets/("original-"+name))
    sections=[]
    for i,page in enumerate(meta["pages"],2):
        image_html=""
        if page.get("image"):
            image_html=f'<figure><img src="assets/{page["image"]}" alt="{html.escape(page["caption"])}"><figcaption>{html.escape(page["caption"])}</figcaption></figure>'
        if page.get("code"):
            image_html += f'<pre>{html.escape(page["code"])}</pre>'
        body="".join(f"<p>{html.escape(p)}</p>" for p in page["body"])
        links=[]
        for n in page.get("sources",[]): links.append(f'<a href="https://github.com/hazelgrove/hazel/pull/{n}">PR #{n}</a>')
        for n in page.get("issues",[]): links.append(f'<a href="https://github.com/hazelgrove/hazel/issues/{n}">issue #{n}</a>')
        sections.append(f'<section><div class="kicker">{html.escape(page["kicker"])}</div><h2>{html.escape(page["title"])}</h2>{image_html}<div class="copy">{body}</div><p class="sources">{" / ".join(links)}</p></section>')
    doc=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Week in Hazel - Issue {meta['id']}</title><style>
@font-face{{font-family:Lib;src:local("Linux Libertine")}}:root{{--paper:#f3ebdd;--ink:#222a23;--green:#355b43;--red:#bb3e27}}*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:19px/1.55 Georgia,Lib,serif}}main{{max-width:980px;margin:auto;padding:24px 36px 80px}}.disclosure{{background:var(--red);color:white;padding:15px 20px;font:700 15px/1.35 system-ui;margin-bottom:28px}}.disclosure span{{display:block;font-weight:400}}.cover{{width:100%;display:block;margin:0 0 26px}}h1{{font-size:64px;line-height:.96;margin:.12em 0}}.deck{{font-size:25px;line-height:1.3;max-width:820px}}.meta,.kicker,.sources{{font:13px/1.4 ui-monospace,monospace;letter-spacing:.04em;text-transform:uppercase}}.kicker{{color:var(--red)}}section{{border-top:1px solid #9ba08f;padding:42px 0}}h2{{font-size:42px;line-height:1.03;margin:.25em 0 .6em}}.copy{{columns:2;column-gap:40px}}p{{margin:0 0 1em}}figure{{margin:20px 0 30px}}figure img{{display:block;max-width:100%;max-height:760px;margin:auto}}figcaption{{font:14px/1.4 system-ui;margin-top:8px}}pre{{overflow:auto;background:#e6ddc4;padding:18px;color:var(--green);font-size:15px}}a{{color:var(--green)}}@media(max-width:720px){{main{{padding:15px 18px 60px}}h1{{font-size:44px}}h2{{font-size:34px}}.copy{{columns:1}}}}
</style></head><body><main><div class="disclosure">All content is fully AI-generated from the Hazel Git repository and GitHub data.<span>Reporting, writing and illustrations are all AI-produced.</span></div><img class="cover" src="assets/cover.png" alt="A traveler crosses syntax tiles with missing delimiters in a translucent backpack"><div class="meta">Week in Hazel / Issue {meta['id']} / {meta['date']} / Retrospective / Unpublished cloud trial</div><h1>{html.escape(meta['title'])}</h1><p class="deck">{html.escape(meta['deck'])}</p>{''.join(sections)}<p class="meta">A small digest for the hazelnut community. Historical cutoff head 790b84e568197eb668591c4b05903aaeb6de20a9.</p></main></body></html>'''
    (WEB/"index.html").write_text(doc)


def main():
    meta=json.loads((ROOT/"copy.json").read_text()); metrics=json.loads((ROOT/"research/metrics.json").read_text())
    OUT.mkdir(parents=True,exist_ok=True); path=OUT/"week-in-hazel-neg058.pdf"
    z=Zine(path,meta); draw_cover(z,meta)
    draw_lead(z,meta["pages"][0]); draw_shot(z,meta["pages"][1],tall=True)
    draw_text(z,meta["pages"][2],code=True); draw_shot(z,meta["pages"][3],tall=False)
    draw_text(z,meta["pages"][4]); draw_stats(z,meta["pages"][5],metrics); draw_comic(z,meta["pages"][6]); z.save()
    build_html(meta); shutil.copy2(path,WEB/path.name)
    print(json.dumps({"pdf":str(path),"html":str(WEB/"index.html"),"pages":z.page_number}))


if __name__=="__main__": main()
