"""Read-only GitHub harvest for Week in Hazel. Requires an authenticated gh CLI."""
import json, subprocess, concurrent.futures, argparse, datetime
from pathlib import Path
ap=argparse.ArgumentParser(); ap.add_argument('--since',default='2026-08-21T00:00:00Z'); ap.add_argument('--until',default='2026-09-11T00:00:00Z'); ap.add_argument('--out',default=str(Path(__file__).parent/'research')); args=ap.parse_args()
P=Path(args.out); P.mkdir(parents=True,exist_ok=True)
def api(endpoint):
 return json.loads(subprocess.check_output(['gh','api',endpoint,'--paginate','--slurp']))
def save(name,data): (P/name).write_text(json.dumps(data,indent=2))
def flat(data): return sum(data,[])
if not (P/'issues-pages.json').exists(): save('issues-pages.json',api(f'repos/hazelgrove/hazel/issues?state=all&since={args.since}&per_page=100&sort=updated&direction=desc'))
for name,endpoint in [
 ('branches-pages.json','repos/hazelgrove/hazel/branches?per_page=100'),
 ('dev-commits-pages.json',f'repos/hazelgrove/hazel/commits?sha=dev&since={args.since}&until={args.until}&per_page=100'),
 ('events-pages.json','repos/hazelgrove/hazel/events?per_page=100')]:
 if not (P/name).exists(): save(name,api(endpoint))
issues=flat(json.loads((P/'issues-pages.json').read_text()))
prs=[x for x in issues if 'pull_request' in x]
jobs=[]
for x in prs:
 n=x['number']; jobs.extend([(f'pr-{n}.json',f'repos/hazelgrove/hazel/pulls/{n}'),(f'reviews-{n}.json',f'repos/hazelgrove/hazel/pulls/{n}/reviews?per_page=100')])
for x in issues:
 if x['comments']: jobs.append((f'comments-{x["number"]}.json',f'repos/hazelgrove/hazel/issues/{x["number"]}/comments?per_page=100'))
def run(job):
 name,url=job
 if (P/name).exists():return
 save(name,api(url))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
 for i,_ in enumerate(ex.map(run,jobs)):
  if i%30==0:print('harvested',i,'of',len(jobs),flush=True)
print('Finished',len(prs),'PR details and review sets;',len(issues),'issue/PR records',flush=True)

save('harvest-manifest.json',dict(repository='hazelgrove/hazel',context_since=args.since,event_cutoff_exclusive=args.until,completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),issue_and_pr_records=len(issues),pr_details=len(prs),note='Mutable prose/status reflect retrieval; cached files are not overwritten. Use a fresh output directory per issue.'))
