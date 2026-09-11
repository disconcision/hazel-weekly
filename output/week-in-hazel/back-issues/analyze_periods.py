"""Reproduce cutoff-dev metrics from local git and saved GitHub responses."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import subprocess,json,re
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
def git(*args):return subprocess.check_output(['git','-C',str(REPO),*args]).decode()
def utc(s):return datetime.fromisoformat(s.replace('Z','+00:00')).astimezone(timezone.utc)
def flatten(x):
 if isinstance(x,list):
  for v in x:yield from flatten(v)
 else:yield x
for e in json.loads((ROOT/'selection.json').read_text()):
 start,end=utc(e['start']),utc(e['end']);r=ROOT/e['slug']/'research'
 rows=[]
 # Explicit Python date filter avoids git --since traversal pruning on unusual histories.
 for line in git('log',e['head'],'--format=%H%x09%cI%x09%an%x09%P%x09%s').splitlines():
  parts=line.split('\t',4)
  if start<=utc(parts[1])<end:rows.append(parts)
 (r/'period-dev-commits.tsv').write_text('\n'.join('\t'.join(v) for v in rows)+'\n')
 daily=Counter();signed=Counter();agent_daily=Counter();authors=Counter();agent={k:[] for k in ['claude','copilot','openai','codex','chatgpt']};sigshas=[]
 for sha,when,author,parents,subject in rows:
  d=utc(when).date().isoformat();daily[d]+=1;authors[author]+=1
  raw=git('cat-file','commit',sha);header,body=raw.split('\n\n',1)
  if re.search(r'^gpgsig(?:-sha256)? ',header,re.M):signed[d]+=1;sigshas.append(sha)
  trailers='\n'.join(v for v in body.splitlines() if re.match(r'(?i)^co-authored-by:',v))
  for k in agent:
   if re.search(r'(?i)\b'+k+r'\b',trailers):agent[k].append(sha)
  if sha in agent['claude']:agent_daily[d]+=1
 prs=list(flatten(json.loads((r/'week-pr-metadata.json').read_text())))
 opened=[p for p in prs if start<=utc(p['created_at'])<end]
 merged=[p for p in prs if p.get('merged_at') and start<=utc(p['merged_at'])<end]
 issues=json.loads((r/'issues-opened.json').read_text())[0]['items']
 m=dict(period_head=e['head'],commits=len(rows),nonmerge=sum(len(v[3].split())<=1 for v in rows),merges=sum(len(v[3].split())>1 for v in rows),authors=dict(authors),daily=dict(sorted(daily.items())),daily_signature_headers=dict(sorted(signed.items())),daily_claude_credits=dict(sorted(agent_daily.items())),agent_credit_objects={k:len(v) for k,v in agent.items()},agent_credit_shas=agent,signature_headers=len(sigshas),signature_header_shas=sigshas,prs_opened=len(opened),prs_merged=len(merged),dev_merges=sum(p['base']['ref']=='dev' for p in merged),feature_merges=[{'number':p['number'],'base':p['base']['ref']} for p in merged if p['base']['ref']!='dev'],issues_opened=len(issues),scope='UTC committer dates inside week, reachable from historical week-end dev head; signature presence only; exact Co-authored-by trailers')
 (r/'metrics.json').write_text(json.dumps(m,indent=2)+'\n');print(e['id'],len(rows),len(opened),len(merged),len(issues),m['agent_credit_objects'])
