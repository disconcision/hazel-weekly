import json,subprocess,re,collections,datetime,argparse
from pathlib import Path
ap=argparse.ArgumentParser(description='Count SHA-distinct commits reachable from the captured remote branch tips.')
ap.add_argument('--research',type=Path,default=Path(__file__).parent/'research')
ap.add_argument('--start',default='2026-09-04T00:00:00Z')
ap.add_argument('--end',default='2026-09-11T00:00:00Z')
args=ap.parse_args(); P=args.research; START=args.start; END=args.end
for value in (START,END):
 if not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z',value):raise SystemExit('use UTC timestamps YYYY-MM-DDTHH:MM:SSZ')
start_dt=datetime.datetime.fromisoformat(START.replace('Z','+00:00')); end_dt=datetime.datetime.fromisoformat(END.replace('Z','+00:00'))
if START>=END: raise SystemExit('start must precede end; use UTC timestamps YYYY-MM-DDTHH:MM:SSZ')
inside=lambda t: bool(t) and START<=t<END
branches=sum(json.load(open(P/'branches-pages.json')),[])
shas=list(dict.fromkeys(b['commit']['sha'] for b in branches))
raw=subprocess.check_output(['git','log',*shas,'--since-as-filter='+START,'--until='+END,'--format=%H%x1f%P%x1f%aN%x1f%aI%x1f%cI%x1f%B%x1e'],text=True)
commits=[]
for part in raw.split('\x1e'):
 if not part.strip():continue
 sha,parents,author,ad,cd,body=part.strip().split('\x1f',5)
 t=datetime.datetime.fromisoformat(cd).astimezone(datetime.timezone.utc).isoformat().replace('+00:00','Z')
 if not inside(t):continue
 header=subprocess.check_output(['git','cat-file','commit',sha],text=True).split('\n\n',1)[0]
 commits.append(dict(sha=sha,parents=parents.split(),author=author,author_date=ad,committer_date=t,body=body,claude_credit=bool(re.search(r'(?im)^Co-authored-by:.*(?:claude|anthropic)',body)),openai_credit=bool(re.search(r'(?im)^Co-authored-by:.*(?:codex|openai|chatgpt)',body)),signature_present='\ngpgsig ' in header))
prs=[json.load(open(f))[0] for f in P.glob('pr-*.json') if re.fullmatch(r'pr-\d+\.json',f.name)]; issues=sum(json.load(open(P/'issues-pages.json')),[])
new=[p for p in prs if inside(p['created_at'])]; merged=[p for p in prs if inside(p['merged_at'])]
aliases={'disconcision':'Andrew Blinn','andrew blinn':'Andrew Blinn','cyrus-':'Cyrus Omar','Cyrus Omar':'Cyrus Omar'}
authors=collections.Counter(aliases.get(c['author'],c['author']) for c in commits)
day_dates=[]; day=start_dt.replace(hour=0,minute=0,second=0)
while day<end_dt:
 day_dates.append(day.date().isoformat());day+=datetime.timedelta(days=1)
days={d:dict(total=sum(c['committer_date'][:10]==d for c in commits),claude=sum(c['committer_date'][:10]==d and c['claude_credit'] for c in commits)) for d in day_dates}
nonmerge=[c for c in commits if len(c['parents'])<2]
active_refs=[]
for b in branches:
 cd=subprocess.check_output(['git','show','-s','--format=%cI',b['commit']['sha']],text=True).strip(); cd=datetime.datetime.fromisoformat(cd).astimezone(datetime.timezone.utc).isoformat().replace('+00:00','Z')
 if inside(cd): active_refs.append(b['name'])
metrics=dict(window_start=START,window_end_exclusive=END,repository='hazelgrove/hazel',default_branch='dev',default_head=next(b['commit']['sha'] for b in branches if b['name']=='dev'),current_remote_branches=len(branches),refs_with_tip_committer_date_in_week=len(active_refs),recent_tip_refs=active_refs,new_prs=len(new),new_prs_draft_at_retrieval=sum(p['draft'] for p in new),merged_prs=len(merged),merged_to_dev=sum(p['base']['ref']=='dev' for p in merged),merged_to_feature_branches=sum(p['base']['ref']!='dev' for p in merged),new_issues=sum('pull_request' not in x and inside(x['created_at']) for x in issues),closed_issues=sum('pull_request' not in x and inside(x['closed_at']) for x in issues),unique_commit_objects=len(commits),nonmerge_commit_objects=len(nonmerge),merge_commit_objects=len(commits)-len(nonmerge),claude_coauthor_credit=sum(c['claude_credit'] for c in commits),nonmerge_claude_credit=sum(c['claude_credit'] for c in nonmerge),openai_coauthor_credit=sum(c['openai_credit'] for c in commits),cryptographic_signature_present=sum(c['signature_present'] for c in commits),authors=authors,daily=days,merged=[{'number':p['number'],'title':p['title'],'base':p['base']['ref']} for p in merged])
(P/'metrics.json').write_text(json.dumps(metrics,indent=2));(P/'branch-commits.json').write_text(json.dumps(commits,indent=2));print(json.dumps(metrics,indent=2))
