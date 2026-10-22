"""Exercise real Bangladesh sessions using disposable QA aliases.

Test sessions are closed afterwards. Existing workshop sessions are never reset.
"""
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError
import json,getpass,secrets,datetime
ROOT=Path(__file__).resolve().parents[1]
API='https://platform-grievance-india.darrin-dookie.chatgpt.site/api/bangladesh/race'
ORIGIN='https://darrindookie-itcilo.github.io'
def call(action,body=None,token=None,method=None):
    headers={'Origin':ORIGIN}
    if token:headers['Authorization']='Bearer '+token
    if body is not None:headers['Content-Type']='application/json'
    request=Request(API+'?action='+action,data=json.dumps(body).encode() if body is not None else None,headers=headers,method=method)
    try:
        with urlopen(request,timeout=25) as r:
            data=r.read();return r.status,json.loads(data) if data else {},dict(r.headers)
    except HTTPError as e:
        data=e.read().decode(errors='replace')
        try:payload=json.loads(data)
        except json.JSONDecodeError:payload={'error':data[:300]}
        return e.code,payload,dict(e.headers)
def main():
    username=getpass.getpass('Facilitator username for live verification (hidden): ').strip()
    password=getpass.getpass('Facilitator password for live verification (hidden): ')
    status,first,_=call('login',{'username':username,'password':'intentionally-incorrect-qa'})
    if status==403 and '1010' in first.get('error',''):
        raise SystemExit('The service browser protection rejected this command-line client (HTTP 403, code 1010). This is not a passing live test. Use the normal dashboard in a browser; do not bypass the protection.')
    assert status==401,('wrong password',status)
    status,data,_=call('login',{'username':username,'password':password});del password
    assert status==200,('login',status,data)
    facilitator=data['token'];results=[];rooms=[]
    try:
        status,_,headers=call('team',method='OPTIONS');assert status==204
        assert headers.get('access-control-allow-origin',headers.get('Access-Control-Allow-Origin'))==ORIGIN
        assert call('rooms')[0]==401
        bank=json.loads((ROOT/'dist/games/bank.json').read_text())['games']
        original=json.loads((ROOT.parent/'platform-service/lib/kenya-rules.json').read_text())['dialogue']['cards']
        for i,game in enumerate([{'id':'dialogue','title':'Call It What It Is'},*bank]):
            gid=game['id'];workshop='secretariats' if i%2 else 'institutions';sector='he' if workshop=='secretariats' else 'health'
            status,data,_=call('create',{'game':gid,'workshop':workshop,'label':'QA verified · '+game['title']},facilitator)
            assert status==201,('create',gid,status,data)
            room=data['room']['code'];rooms.append(room)
            tokens=[secrets.token_hex(32),secrets.token_hex(32)];teams=[]
            for n,t in enumerate(tokens):
                status,data,_=call('join',{'game':gid,'room':room,'name':'QA Table '+str(n+1),'sector':sector},t);assert status==201,(gid,status,data);teams.append(data['team'])
            assert call('board&room='+room,token=tokens[0])[0]==401
            if gid=='dialogue':
                answers=[{'form':c['form'],'setting':c['setting'],'q3':'Consult before the decision'} for c in original]
                first={'i':0,'answers':answers[:1],'form':None,'setting':None,'screen':'reveal'}
                wrong={'i':0,'answers':[{'form':(original[0]['form']+1)%5,'setting':original[0]['setting'],'q3':''}],'form':None,'setting':None}
                final={'i':11,'answers':answers,'form':None,'setting':None,'screen':'final'};maximum=240
            else:
                answers=[{'selection':q['answer']} for q in game['questions']]
                first={'i':0,'answers':answers[:1],'screen':'reveal','score':99999}
                wrongpick=next(n for n in range(len(game['questions'][0]['options'])) if n not in game['questions'][0]['answer'])
                wrong={'i':0,'answers':[{'selection':[wrongpick]}]}
                final={'i':len(answers)-1,'answers':answers,'screen':'final'};maximum=len(answers)*10
            assert call('update',{'generation':1,'state':first},tokens[0])[0]==200
            assert call('update',{'generation':1,'state':wrong},tokens[1])[0]==200
            status,data,_=call('board&room='+room,token=facilitator);assert status==200 and len(data['teams'])==2
            a,b=data['teams'];assert a['metrics']['correct']==1 and b['metrics']['wrong']==1
            assert a['metrics']['answered']==1 and b['metrics']['answered']==1
            assert a['metrics']['score']==(20 if gid=='dialogue' else 10)
            assert 'state' not in a and 'token_hash' not in a
            status,data,_=call('update',{'generation':1,'state':final},tokens[0]);assert status==200,(gid,status,data)
            assert data['team']['metrics']['score']==maximum and data['team']['metrics']['done']
            finish=data['team']['finishedAt'];assert finish>0
            assert call('update',{'generation':1,'state':final},tokens[0])[1]['team']['finishedAt']==finish
            assert call('reset',{'room':room,'teamId':teams[0]['id']},facilitator)[0]==200
            reset=call('team',token=tokens[0])[1]['team'];assert reset['generation']==2 and reset['metrics']['score']==0 and reset['metrics']['answered']==0
            assert call('team',token=tokens[1])[1]['team']['metrics']['wrong']==1
            status,data,_=call('update',{'generation':1,'state':first},tokens[0]);assert status==409 and data['team']['generation']==2
            assert call('reset-all',{'room':room},facilitator)[0]==200
            assert call('team',token=tokens[0])[1]['team']['generation']==3
            assert call('team',token=tokens[1])[1]['team']['metrics']['wrong']==0
            assert call('close',{'room':room,'active':False},facilitator)[0]==200
            assert call('join',{'game':gid,'room':room,'name':'QA closed check','sector':sector},secrets.token_hex(32))[0]==409
            results.append({'game':gid,'workshop':workshop,'twoTeams':True,'serverScore':maximum,'progressRightWrong':True,'singleReset':True,'allReset':True,'staleUpdateRejected':True,'sessionClosed':True})
            print('Verified live: '+game['title'],flush=True)
    finally:
        for room in rooms:
            call('close',{'room':room,'active':False},facilitator)
        status,_,_=call('logout',{},facilitator)
        assert status==200
        assert call('rooms',token=facilitator)[0]==401
    result={'service':API,'checkedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'wrongPasswordRejected':True,'unauthenticatedBoardRejected':True,'corsVerified':True,'logoutRevokesAccess':True,'games':results}
    (ROOT/'verification/live-service.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'gamesVerified':len(results),'teamsVerified':len(results)*2,'facilitatorLogin':True,'logout':True}))
if __name__=='__main__':main()
