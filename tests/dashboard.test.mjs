import assert from 'node:assert/strict';
import test from 'node:test';
import {readFile} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {webcrypto,createHash} from 'node:crypto';
import {JSDOM,VirtualConsole} from 'jsdom';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..'),dist=path.join(root,'dist');
const base='https://darrindookie-itcilo.github.io/Bangladesh-Social-Dialogue-Workshops/';
const pause=()=>new Promise(r=>setTimeout(r,10));
async function until(fn,message){for(let i=0;i<500;i++){if(fn())return;await pause();}throw new Error(message);}
async function dom(page='index.html',hash='',api){
  const errors=[],downloads=[],vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e.message));
  const d=new JSDOM(await readFile(path.join(dist,page.split('?')[0]),'utf8'),{url:base+page+hash,runScripts:'outside-only',pretendToBeVisual:true,virtualConsole:vc});
  const w=d.window;Object.defineProperty(w,'crypto',{value:webcrypto});w.TextEncoder=TextEncoder;w.TextDecoder=TextDecoder;w.Blob=Blob;
  w.HTMLElement.prototype.scrollIntoView=function(){};w.scrollTo=()=>{};w.confirm=()=>true;w.alert=()=>{};
  w.HTMLDialogElement.prototype.showModal=function(){this.open=true;};w.HTMLDialogElement.prototype.close=function(){this.open=false;};
  const blobs=new Map();w.URL.createObjectURL=blob=>{const id='blob:qa-'+blobs.size;blobs.set(id,blob);return id;};w.URL.revokeObjectURL=()=>{};
  w.HTMLAnchorElement.prototype.click=function(){if(this.download)downloads.push({name:this.download,blob:blobs.get(this.href),href:this.href});};
  w.fetch=async(url,options={})=>{const u=new URL(String(url),w.location.href);if(u.origin.includes('chatgpt.site')){
      if(api)return api(u,options);
      const action=u.searchParams.get('action');return new Response(JSON.stringify(action==='login'?{token:'bdf_fixture',expiresAt:Date.now()+5400000,serverNow:Date.now()}:action==='rooms'?{rooms:[],serverNow:Date.now()}:{ok:true,serverNow:Date.now()}));
    }
    const local=path.resolve(dist,decodeURIComponent(u.pathname.replace('/Bangladesh-Social-Dialogue-Workshops/','')));assert(local.startsWith(dist+path.sep));try{return new Response(await readFile(local));}catch{return new Response('Not found',{status:404});}};
  const evaluate=async file=>w.eval(await readFile(path.join(dist,file),'utf8'));
  return{d,w,errors,downloads,evaluate,close:()=>d.window.close()};
}
async function app(hash,api){const t=await dom('index.html',hash,api);for(const f of ['data.js','game-catalog.js','facilitator-live.js','app.js'])await t.evaluate(f);return t;}
async function route(t,hash){t.w.location.hash=hash;await until(()=>t.w.document.title.includes(hash.split('?')[0]==='programme'?(hash.includes('secretariats')?'Secretariat':'Tripartite'):hash.startsWith('activities')?'Activity':hash.startsWith('games')?'games':hash.startsWith('notebook')?'notebook':'Facilitator'),'route did not render');await pause();}
const submit=form=>form.dispatchEvent(new form.ownerDocument.defaultView.Event('submit',{bubbles:true,cancelable:true}));
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');

test('both programmes follow the attached agendas, including the external Tuesday morning meeting',async()=>{const t=await app('#programme?w=institutions&day=1');try{const D=t.w.BANGLADESH;assert.deepEqual(Array.from(D.workshops,w=>w.days.flatMap(d=>d.items).filter(s=>s.session).length),[12,10]);
  for(const w of D.workshops)for(const day of w.days){t.w.location.hash=`programme?w=${w.id}&day=${day.number}`;await pause();assert.equal(t.w.document.querySelectorAll('article.session').length,day.items.filter(s=>s.session).length);assert(t.w.document.querySelector('.daily-games a'));assert(!t.w.document.querySelector('main').textContent.includes('Rev.1'));}
  t.w.location.hash='programme?w=institutions&day=2';await pause();assert.match(t.w.document.querySelector('.external-meeting').textContent,/09:00.*12:30/);assert.match(t.w.document.querySelector('.external-meeting').textContent,/no course session/);assert.equal(t.w.document.querySelector('article.session .session-time small').textContent,'Session 5');assert.deepEqual(t.errors,[]);
}finally{t.close();}});
test('every session offers current activity files and both workshop packs use the separate agendas',async()=>{const t=await app('#activities?w=institutions');try{const D=t.w.BANGLADESH;assert.equal(D.activities.length,19);assert.equal(D.activities.filter(a=>a.workshop==='institutions').length,13);assert.equal(t.w.document.querySelectorAll('.resource-card').length,13);
  for(const w of D.workshops)for(const s of w.days.flatMap(d=>d.items).filter(s=>s.session)){t.w.location.hash=`activities?w=${w.id}&session=${s.session}`;await pause();assert.equal(t.w.document.querySelectorAll('[data-preview]').length,s.handouts.length);assert(s.handouts.length>0);}
  t.w.document.querySelector('[data-preview]').click();assert(t.w.document.querySelector('#document-viewer').open);assert(t.w.document.querySelector('#document-body').textContent.length>100);t.w.document.querySelector('[data-close-dialog]').click();assert(!t.w.document.querySelector('#document-viewer').open);
  for(const row of D.activities)assert.equal((await readFile(path.join(dist,row.file))).subarray(0,2).toString(),'PK');
  assert.deepEqual(t.errors,[]);
}finally{t.close();}});
test('facilitator rejects a wrong password, unlocks 22 sessions and both reserve sheets, downloads exact bytes, and locks on sign-out',async()=>{const t=await app('#facilitator?w=institutions');try{let form=t.w.document.querySelector('#facilitator-login');form.elements.username.value=process.env.BD_TEST_USERNAME;form.elements.password.value='intentionally-wrong';submit(form);await until(()=>!form.querySelector('button').disabled,'wrong-password response');assert.match(t.w.document.querySelector('#login-error').textContent,/not recognized/);assert.equal(t.w.document.querySelectorAll('[data-unlock-file]').length,0);
  assert(process.env.BD_TEST_PASSWORD,'Run npm test to enter the facilitator password securely.');form.elements.password.value=process.env.BD_TEST_PASSWORD;submit(form);await until(()=>!!t.w.document.querySelector('[data-lock]'),'facilitator did not unlock');assert.equal(t.w.document.querySelectorAll('.trainer-row').length,14);assert.equal(t.w.document.querySelectorAll('.reserve-row').length,2);
  const expected=JSON.parse(await readFile(path.join(root,'verification/materials.json'),'utf8'));
  for(const wid of ['institutions','secretariats']){t.w.location.hash=`facilitator?tab=materials&w=${wid}`;await pause();const buttons=Array.from(t.w.document.querySelectorAll('[data-unlock-file]'));assert.equal(buttons.length,wid==='institutions'?26:20);
    for(const b of buttons){const n=t.downloads.length;b.click();await until(()=>t.downloads.length>n,'protected download failed');const row=expected.find(r=>r.path===b.dataset.unlockFile),bytes=Buffer.from(await t.downloads.at(-1).blob.arrayBuffer());assert.equal(hash(bytes),row.sha256);}
    t.w.document.querySelector('[data-script]').click();assert(t.w.document.querySelector('#document-body').textContent.length>100);t.w.document.querySelector('[data-close-dialog]').click();}
  assert.equal(t.downloads.length,46);t.w.document.querySelector('[data-lock]').click();assert(t.w.document.querySelector('#facilitator-login'));assert.equal(t.w.document.querySelector('#document-body').textContent,'');assert(!Object.keys(t.w.localStorage).some(k=>t.w.localStorage.getItem(k).includes(process.env.BD_TEST_PASSWORD)));assert.deepEqual(t.errors,[]);
}finally{t.close();}});
test('facilitator live controls send one create request after reconnecting and render progress, right/wrong, points and reset controls',async()=>{let creates=0,resets=0;const r={code:'ABCDEFGH',workshop:'institutions',game:'rapport',label:'QA UI session',active:1};const team={id:'test-id',name:'Table A',generation:1,startedAt:Date.now(),finishedAt:0,updatedAt:Date.now(),metrics:{step:2,steps:6,stepName:'Reframe · Question 2',answered:1,correct:1,wrong:0,score:10,max:60,done:false}};
  const t=await app('#facilitator?tab=live&w=institutions',(u,o)=>{const action=u.searchParams.get('action');if(action==='create')creates++;if(action==='reset'||action==='reset-all')resets++;return new Response(JSON.stringify({serverNow:Date.now(),...(action==='login'?{token:'bdf_fixture',expiresAt:Date.now()+5400000}:action==='rooms'?{rooms:[]}:action==='create'?{room:r}:action==='board'?{room:r,teams:[team]}:{ok:true})}));});try{const f=t.w.document.querySelector('#facilitator-login');f.elements.username.value=process.env.BD_TEST_USERNAME;f.elements.password.value=process.env.BD_TEST_PASSWORD;submit(f);await until(()=>t.w.document.querySelector('#create-session'),'live board unavailable');
    t.w.BDLive.mount();t.w.BDLive.mount();const create=t.w.document.querySelector('#create-session');create.querySelector('button').click();await until(()=>creates===1&&t.w.document.querySelector('.session-code'),'session create failed or duplicated');t.w.document.querySelector('[data-board=refresh]').click();await until(()=>!!t.w.document.querySelector('[data-reset-team]'),'team progress did not render');const text=t.w.document.querySelector('#live-team-table').textContent;assert.match(text,/Reframe · Question 2/);assert.match(text,/10/);assert(t.w.document.querySelector('[data-board=reset-all]'));t.w.document.querySelector('[data-reset-team]').click();await until(()=>resets===1&&t.w.document.querySelector('#board-notice').textContent.includes('Reset saved'),'team reset not completed');assert.deepEqual(t.errors,[]);
  }finally{t.close();}});
test('all six workshop challenges complete all 40 decision rounds with exact scores and exportable results',async()=>{const bank=JSON.parse(await readFile(path.join(dist,'games/bank.json'),'utf8'));
  for(const g of bank.games){const t=await dom('games/challenges/index.html?game='+g.id+'&w=secretariats');try{await t.evaluate('race.js');await t.evaluate('games/challenges/challenge.js');const form=t.w.document.querySelector('#setup');assert(form);form.elements.team.value='QA practice';submit(form);await until(()=>!!t.w.document.querySelector('#lock'),'game did not start');
    for(const q of g.questions){if(q.kind==='order'){let order=Array.from(t.w.document.querySelectorAll('.order-row span'),row=>q.options.indexOf(row.textContent));assert.notDeepEqual(order,q.answer,'a sequencing round must need a decision');for(let target=0;target<q.answer.length;target++){let current=order.indexOf(q.answer[target]);while(current>target){t.w.document.querySelector(`[data-move="${current}"][data-delta="-1"]`).click();[order[current-1],order[current]]=[order[current],order[current-1]];current--;}}}else for(const n of q.answer)t.w.document.querySelector(`[data-choice="${n}"]`).click();assert(!t.w.document.querySelector('#lock').disabled);t.w.document.querySelector('#lock').click();assert.match(t.w.document.querySelector('.feedback').textContent,/Good call/);t.w.document.querySelector('#next').click();}
    assert.match(t.w.document.querySelector('.results-number').textContent,new RegExp(String(g.questions.length*10)));t.w.document.querySelector('#export').click();assert.equal(JSON.parse(await t.downloads[0].blob.text()).right,g.questions.length);assert.deepEqual(t.errors,[]);
  }finally{t.close();}}
});
test('game desk lists seven games and notebooks remain separate across workshops',async()=>{const t=await app('#games?w=institutions');try{assert.equal(t.w.document.querySelectorAll('.game-card').length,6);assert.equal(t.w.document.querySelectorAll('.daily-games').length,4);t.w.location.hash='notebook?w=institutions';await pause();let input=t.w.document.querySelector('[data-note=reflection]');input.value='Institution reflection';input.dispatchEvent(new t.w.Event('input',{bubbles:true}));t.w.location.hash='notebook?w=secretariats';await pause();assert.equal(t.w.document.querySelector('[data-note=reflection]').value,'');t.w.location.hash='notebook?w=institutions';await pause();assert.equal(t.w.document.querySelector('[data-note=reflection]').value,'Institution reflection');assert.deepEqual(t.errors,[]);}finally{t.close();}});
test('a different team alias gets an independent live token while the same alias resumes its team',async()=>{
  const seen=[],t=await dom('games/challenges/index.html','',async(u,o)=>{const b=JSON.parse(o.body),bearer=o.headers.Authorization;seen.push(bearer);return new Response(JSON.stringify({serverNow:Date.now(),team:{id:bearer,name:b.name,sector:b.sector,room:b.room,generation:1,revision:0,startedAt:Date.now(),finishedAt:0,state:{}}}));});
  try{await t.evaluate('race.js');const C=t.w.NaivashaRace.RaceConnection;
    const a=new C('rapport');await a.join({room:'ABCDEFGH',name:'Table A',sector:'health'});
    const resume=new C('rapport');await resume.join({room:'ABCDEFGH',name:'Table A',sector:'health'});
    const b=new C('rapport');await b.join({room:'ABCDEFGH',name:'Table B',sector:'health'});
    assert.equal(seen[0],seen[1]);assert.notEqual(seen[0],seen[2]);a.stop();resume.stop();b.stop();assert.deepEqual(t.errors,[]);
  }finally{t.close();}
});

test('handout search finds text and session topics while preserving the workshop and session filters',async()=>{
  for(const wid of ['institutions','secretariats']){const t=await app('#activities?w='+wid);try{
    const search=t.w.document.querySelector('#activity-search');
    for(const term of ['evidence','minutes','wage','budget','action plan']){search.value=term;search.dispatchEvent(new t.w.Event('input',{bubbles:true}));assert(t.w.document.querySelectorAll('.resource-card').length>0,wid+' search missed '+term);}
    search.value='no-such-handout-xyz';search.dispatchEvent(new t.w.Event('input',{bubbles:true}));assert.equal(t.w.document.querySelectorAll('.resource-card').length,0);assert(t.w.document.querySelector('[data-clear-filters]'));t.w.document.querySelector('[data-clear-filters]').click();await pause();assert(t.w.document.querySelectorAll('.resource-card').length>0);assert.deepEqual(t.errors,[]);
  }finally{t.close();}}
});
test('live join rejects ambiguous code characters and explains a network failure with a practice fallback',async()=>{
  const t=await dom('games/challenges/index.html','',()=>{throw new TypeError('Failed to fetch');});
  try{await t.evaluate('race.js');const c=new t.w.NaivashaRace.RaceConnection('rapport');
    await assert.rejects(c.join({room:'ABCD01GH',name:'QA table'}),/digits 2–9/);
    await assert.rejects(c.join({room:'ABCDEFGH',name:'QA table'}),/practice mode/);assert(!c.message.includes('Failed to fetch'));c.stop();
  }finally{t.close();}
});
test('all handouts, corrected agendas and participant packs match the recorded integrity hashes',async()=>{
  const records=JSON.parse(await readFile(path.join(root,'verification/materials.json'),'utf8'));
  for(const row of records.filter(r=>!r.path.startsWith('protected/')))assert.equal(hash(await readFile(path.join(dist,row.path))),row.sha256,row.path);
});
test('Bangladesh dialogue scenarios preserve every server-scored classification and both acceptable alternatives',async()=>{
  const t=await dom('games/dialogue/index.html');try{await t.evaluate('race.js');await t.evaluate('games/dialogue/live.js');
    const html=await readFile(path.join(dist,'games/dialogue/index.html'),'utf8'),inline=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(m=>m[1]).filter(Boolean);for(const code of inline)t.w.eval(code);
    const rules=JSON.parse(await readFile(path.join(root,'../platform-service/lib/kenya-rules.json'),'utf8')).dialogue.cards;
    const cards=JSON.parse(html.match(/var CARDS = (\[[\s\S]*?\n\]);/)[1]);assert.equal(cards.length,12);for(let i=0;i<12;i++){const c=cards[i],r=rules[i];assert.equal(c.form,r.form);assert.equal(c.setting,r.setting);assert.equal(c.altForm,r.altForm);assert.equal(c.altSetting,r.altSetting);assert(!/county|university|ward manager|hospital board|Cabinet Secretary/i.test(c.text));}
    assert.equal(cards.filter(c=>c.arguable).length,2);assert.deepEqual(t.errors,[]);
  }finally{t.close();}
});
