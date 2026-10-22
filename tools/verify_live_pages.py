"""Compare every live website file with the local release and check removals."""
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,datetime,subprocess,time
ROOT=Path(__file__).resolve().parents[1]
BASE='https://darrindookie-itcilo.github.io/Bangladesh-Social-Dialogue-Workshops/'
def main():
    suffix='?verify='+str(int(time.time()))
    files=[p for p in (ROOT/'dist').rglob('*') if p.is_file()]
    def check(p):
        rel=p.relative_to(ROOT/'dist').as_posix()
        with urlopen(Request(BASE+quote(rel)+suffix,headers={'Cache-Control':'no-cache'}),timeout=30) as r:
            data=r.read();assert r.status==200
        expected=p.read_bytes();assert data==expected,rel+' differs from the release'
        return {'path':rel,'status':200,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
    with ThreadPoolExecutor(max_workers=8) as pool:results=list(pool.map(check,files))
    # Paths intentionally removed from the original published version.
    old=subprocess.check_output(['git','ls-tree','-r','--name-only','ed37682c9b83ee6cf2928a6971dda90d2cdd573e','dist/'],cwd=ROOT,text=True).splitlines()
    removed=[p for p in old if not (ROOT/p).exists()]
    for path in removed:
        try:
            with urlopen(Request(BASE+quote(path[5:])+suffix,headers={'Cache-Control':'no-cache'}),timeout=20) as r:raise AssertionError(path+' still served: '+str(r.status))
        except HTTPError as e:assert e.code==404,(path,e.code)
    result={'url':BASE,'verifiedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'filesMatched':len(results),'bytesVerified':sum(r['bytes'] for r in results),'removedPaths404':removed,'files':results}
    (ROOT/'verification'/'live-pages.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='files'}))
if __name__=='__main__':main()
