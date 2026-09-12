/* Typeset text in Chromium; original PDF artwork is composited separately. */
const fs=require('fs');const path=require('path');
const runtime=process.env.HAZEL_ZINE_NODE_MODULES || process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES || '/Users/andrewblinn/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {chromium}=require(path.join(runtime,'playwright'));
const root=__dirname;const job=JSON.parse(fs.readFileSync(path.join(root,'typesetting/layout.json'),'utf8'));
const fontDir=job.fontDir;const face=(family,file,weight=400,style='normal')=>`@font-face{font-family:${family};src:url('${new URL('file://'+fontDir+'/'+file).href}');font-weight:${weight};font-style:${style}}`;
const fontCSS=face('Lib','LinLibertine_R_G.ttf')+face('Lib','LinLibertine_RB_G.ttf',700)+face('Lib','LinLibertine_RI_G.ttf',400,'italic')+face('Rubik','Rubik-Regular.ttf')+face('Rubik','Rubik-Bold.ttf',700)+face('Code','LiberationMono-Regular.ttf');
const fontStyles={Serif:'font-family:Lib',SerifBold:'font-family:Lib;font-weight:700',SerifItalic:'font-family:Lib;font-style:italic',Sans:'font-family:Rubik',SansBold:'font-family:Rubik;font-weight:700',Mono:'font-family:Code'};
const textHTML=s=>s.replace(/<b>(let f\(x\) = …|name : String|3\.0-4\.1×)<\/b>/g,'<b class="inline-code">$1</b>').replace(/&#160;|&nbsp;|\u00a0/g,' ').replace(/<link href="([^"]+)" color="([^"]+)">/g,'<a href="$1" style="color:$2">').replace(/<\/link>/g,'</a>').replace(/<font name="([^"]+)" size="([^"]+)">/g,(_,f,n)=>`<span style="${fontStyles[f]};font-size:${n}pt;hyphens:manual">`).replace(/<\/font>/g,'</span>');
const element=n=>{
 const ps=n.text.split('<br/><br/>').map((s,i)=>`<p>${n.kind==='drop'&&i===0?`<span class="initial" style="height:${n.leading*3-2}pt;line-height:${n.leading*3-3}pt">${s[0]}</span>${textHTML(s.slice(1))}`:textHTML(s)}</p>`).join('');
 return `<div id="${n.id}" class="box ${n.font==='Serif'&&n.size<=14.5?'body':'display'} ${n.styleStudy?'study':''}" style="left:${n.x}pt;top:${n.y}pt;width:${n.w}pt;font-size:${n.size}pt;line-height:${n.leading}pt;${fontStyles[n.font]};color:${n.color};--paragraph-gap:${n.styleStudy?n.leading:7}pt">${ps}</div>`;
};
(async()=>{
 const launch={headless:true};
 if(process.env.HAZEL_ZINE_BROWSER_EXECUTABLE)launch.executablePath=process.env.HAZEL_ZINE_BROWSER_EXECUTABLE;
 else launch.channel=process.env.HAZEL_ZINE_BROWSER_CHANNEL || 'chrome';
 const browser=await chromium.launch(launch);const results={engine:browser.version(),pretty:true,files:[]};
 for(const file of job.files){
  const page=await browser.newPage({viewport:{width:720,height:960},deviceScaleFactor:1});
  const html=`<!doctype html><html lang="en-US"><meta charset="utf-8"><title>${file.name} — text layer</title><style>${fontCSS}@page{size:540pt 720pt;margin:0}*{box-sizing:border-box}html,body{margin:0;padding:0;background:transparent;color:#222a23}.sheet{position:relative;width:540pt;height:720pt;break-after:page}.sheet:last-child{break-after:auto}.box{position:absolute;font-kerning:normal;font-variant-ligatures:common-ligatures}.box p{margin:0;text-wrap:pretty}.body p{hyphens:auto;hyphenate-limit-chars:8 3 3}.box p+p{margin-top:var(--paragraph-gap)}.display p{hyphens:manual}.body b,.body a{hyphens:manual}.initial{float:left;width:32pt;margin-right:5pt;margin-bottom:2pt;font:700 36pt Lib;text-align:center;color:#bb3e27;background:#dce2cc;border-bottom:.6pt solid #355b43}.inline-code{white-space:nowrap}a{color:inherit;text-decoration:none;text-decoration-thickness:.45pt;text-underline-offset:1pt}u{text-decoration:underline;text-underline-offset:1pt}</style>${Array.from({length:file.pages},(_,i)=>`<section class="sheet" data-page="${i+1}">${file.nodes.filter(n=>n.page===i+1).map(element).join('')}</section>`).join('')}</html>`;
  const htmlFile=path.join(root,'typesetting',file.name.replace('.pdf','.html'));fs.writeFileSync(htmlFile,html);
  await page.goto('file://'+htmlFile);await page.evaluate(()=>document.fonts.ready);await page.emulateMedia({media:'print'});
  const measures=await page.evaluate(()=>[...document.querySelectorAll('.box')].map(el=>{const r=el.getBoundingClientRect(),pr=el.parentElement.getBoundingClientRect();return{id:el.id,x:(r.x-pr.x)*.75,y:(r.y-pr.y)*.75,w:r.width*.75,h:r.height*.75,pretty:getComputedStyle(el.querySelector('p')).textWrap,fonts:getComputedStyle(el).fontFamily};}));
  for(const m of measures)m.key=file.nodes.find(n=>n.id===m.id).key;
  // Count paragraphs for which pretty actually changes the line distribution.
  const comparison=await page.evaluate(()=>{function lines(p){const tops=[];const walker=document.createTreeWalker(p,NodeFilter.SHOW_TEXT);let t;while(t=walker.nextNode()){if(t.parentElement.classList.contains('initial'))continue;for(let i=0;i<t.textContent.length;i++){const r=document.createRange();r.setStart(t,i);r.setEnd(t,i+1);const b=r.getBoundingClientRect();if(b.width>0)tops.push([Math.round(b.top*10)/10,Math.round(b.right*10)/10]);}}return JSON.stringify(tops)}let changed=0,total=0;for(const p of document.querySelectorAll('.body p')){const a=lines(p);p.style.textWrap='wrap';const b=lines(p);p.style.textWrap='pretty';total++;if(a!==b)changed++;}return{total,changed};});
  const errors=measures.flatMap(m=>{const n=file.nodes.find(n=>n.id===m.id);return n.maxh!=null&&m.h>n.maxh+.8?[{id:n.id,page:n.page,h:m.h,max:n.maxh,text:n.text.slice(0,90)}]:[];});
  await page.pdf({path:file.textPDF,preferCSSPageSize:true,printBackground:true,tagged:true});
  results.files.push({name:file.name,measures,comparison,errors});await page.close();
 }
 await browser.close();fs.writeFileSync(path.join(root,'typesetting/metrics.json'),JSON.stringify(results,null,2));
 console.log(JSON.stringify({engine:results.engine,files:results.files.map(f=>({name:f.name,comparison:f.comparison,overflows:f.errors}))}));
})().catch(e=>{console.error(e);process.exit(1)});
