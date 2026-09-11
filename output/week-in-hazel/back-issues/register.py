"""Register verified retrospective editions without advancing the current cutoff."""
from pathlib import Path
from datetime import datetime,timezone
import json,re
from PIL import Image
R=Path(__file__).resolve().parent;kit=R.parent;now=datetime.now(timezone.utc).isoformat()
checks={x['issue']:x for x in json.loads((R/'verification.json').read_text())['pdf_checks']}
issues=json.loads((kit/'issues.json').read_text());images=json.loads((kit/'image-ledger.json').read_text())
for old in issues:
 if old['id']=='001':old.setdefault('number',1)
for e in json.loads((R/'selection.json').read_text()):
 m=json.loads((R/e['slug']/'copy.json').read_text());qa=checks[e['id']];topics=[]
 for n,p in enumerate(m['pages'],2):
  if p['type']=='comic':continue
  topics.append({'key':e['slug']+'-'+re.sub('[^a-z0-9]+','-',p['section'].lower()).strip('-'),'role':'lead' if n==2 else 'feature','page':n,'new_angle':p['title'].replace('\n',' '),'github_numbers':p.get('sources',[])+p.get('issues',[]),'return_trigger':'Return on a substantive later change; consult reporting dates, not retrospective production date.'})
 record={'id':e['id'],'number':e['number'],'title':m['title'],'start_utc':e['start'],'end_exclusive_utc':e['end'],'artifact':'../pdf/'+qa['file'],'status':'ready','edition':'retrospective','produced_utc':now,'revision':1,'historical_dev_head':e['head'],'pages':qa['pages'],'extracted_words':qa['words'],'topics':topics,'images':[e['slug']+'-'+s for s in ['cover','screenshot','comic']],'reporting_credits':{'editor':'Astra (AI editor and reporter)','illustrations':'ImageGen'},'production_guide':'back-issues/README.md','source_directory':'back-issues/'+e['slug']+'/research','next_issue_end_exclusive_utc':None}
 issues=[x for x in issues if x['id']!=e['id']];issues.append(record)
 for kind in ['cover','screenshot','comic']:
  id=e['slug']+'-'+kind;f=R/e['slug']/'assets'/(kind+'.png');images=[x for x in images if x['id']!=id]
  images.append({'id':id,'issue':e['id'],'number':e['number'],'kind':'authentic historical-build screenshot' if kind=='screenshot' else 'generated illustration','concept':m['pages'][next(i for i,p in enumerate(m['pages']) if p['type']=='shot')]['caption'] if kind=='screenshot' else (m['title'] if kind=='cover' else m['pages'][-1]['caption']),'path':str(f.relative_to(kit)),'created_utc':now,'reporting_start_utc':e['start'],'historical_head':e['head'] if kind=='screenshot' else None,'prompt':None if kind=='screenshot' else 'back-issues/'+('ART-PROMPTS.json' if kind=='cover' else 'COMIC-PROMPTS.json'),'cleanup':'back-issues/COMIC-CLEANUP.md' if kind=='comic' else None,'pixel_dimensions':list(Image.open(f).size),'reuse_rule':'Retrospective visual. Avoid repeating the same program or comic premise; return for a new behavior or an explicitly labeled historical comparison.'})
 # Full source index keeps long links and provenance out of article columns.
 lines=[f"# Issue {e['id']} sources",'',f"Reporting window: {e['start']} to {e['end']} (exclusive).",f"Historical dev head: [{e['head']}](https://github.com/hazelgrove/hazel/commit/{e['head']}).",'', 'GitHub records retrieved September 11, 2026. Article readiness uses dated merge/open events, pre-cutoff comments and period code. Current PR descriptions are mutable and were not treated as a historical snapshot.','']
 for n,p in enumerate(m['pages'],2):
  lines.extend([f"## Page {n}: {p['title'].replace(chr(10),' ')}",''])
  for num in p.get('sources',[]):lines.append(f"- [PR #{num}](https://github.com/hazelgrove/hazel/pull/{num}) — `research/pr-{num}.json`; related `comments-`, `reviews-`, `review-comments-` files.")
  for num in p.get('issues',[]):lines.append(f"- [Issue #{num}](https://github.com/hazelgrove/hazel/issues/{num}) — `research/issues-opened.json`.")
  lines.append('')
 lines.extend(['## Reproducible evidence','', '- `research/metrics.json` and `period-dev-commits.tsv`: period-head graph and counts.', '- `research/build-provenance.json` and `screenshot-program.hz`: exact revision and staged UI program.', '- `../analyze_periods.py`: git-object and trailer analysis.', '- `../README.md`: limitations, selection rationale and process findings.', '', 'The comic and cover are original generated fiction, not archival images or developer portraits. Their premises are explained on the last page and their prompts are retained in the kit.'])
 (R/e['slug']/'SOURCES.md').write_text('\n'.join(lines)+'\n')
# Newest reporting week first preserves the current pilot at the head of the ledger.
issues.sort(key=lambda x:x['start_utc'],reverse=True)
(kit/'issues.json').write_text(json.dumps(issues,indent=2,ensure_ascii=False)+'\n');(kit/'image-ledger.json').write_text(json.dumps(images,indent=2,ensure_ascii=False)+'\n')
print('Registered',len(checks),'back issues. Current weekly cutoff remains',next(x for x in issues if x['id']=='001')['next_issue_end_exclusive_utc'])
