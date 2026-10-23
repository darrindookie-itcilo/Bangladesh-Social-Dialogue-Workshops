"""Refresh the published training set from the October 22 attachments.

The password is read from the terminal and never written to source or metadata.
Original Office documents are copied/reconstructed byte for byte. ZIP agendas
are deliberately excluded. Facilitator documents and reserve sheets are encrypted.
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from io import BytesIO
from lxml import etree as E
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64, getpass, hashlib, html, json, os, re, shutil

ROOT = Path(__file__).resolve().parents[1]
UPLOAD = ROOT.parent / 'upload'
DIST = ROOT / 'dist'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W = '{' + NS['w'] + '}'

def text(node):
    return ''.join(t.text or '' for t in node.iter(W + 't')).strip()

def paragraphs(node):
    return [text(p) for p in node.findall('./w:p', NS) if text(p)]

def xml(blob):
    with ZipFile(BytesIO(blob)) as z:
        return E.fromstring(z.read('word/document.xml'))

def as_html(blob):
    body = xml(blob).find('w:body', NS)
    def paragraph(p):
        value = text(p)
        if not value:
            return ''
        style = p.find('./w:pPr/w:pStyle', NS)
        name = style.get(W + 'val', '') if style is not None else ''
        tag = 'h3' if 'Heading' in name or name in ('Title', 'Subtitle') else 'p'
        return f'<{tag}>{html.escape(value)}</{tag}>'
    def table(t):
        rows = []
        for i, tr in enumerate(t.findall('./w:tr', NS)):
            cells = []
            for tc in tr.findall('./w:tc', NS):
                span = tc.find('./w:tcPr/w:gridSpan', NS)
                attr = f' colspan="{int(span.get(W+"val"))}"' if span is not None else ''
                tag = 'th' if i == 0 else 'td'
                cells.append(f'<{tag}{attr}>' + ''.join(paragraph(p) for p in tc.findall('./w:p', NS)) + f'</{tag}>')
            rows.append('<tr>' + ''.join(cells) + '</tr>')
        return '<div class="table-scroll"><table>' + ''.join(rows) + '</table></div>'
    return ''.join(paragraph(n) if n.tag == W+'p' else table(n) if n.tag == W+'tbl' else '' for n in body)

def agenda(blob, code, start):
    from datetime import date, timedelta
    r = xml(blob)
    tables = r.findall('./w:body/w:tbl', NS)
    meta = {text(cells[0]): text(cells[1]) for tr in tables[0].findall('./w:tr', NS) if len(cells := tr.findall('./w:tc',NS)) == 2}
    days, session = [], 0
    for tr in tables[1].findall('./w:tr', NS)[1:]:
        cells = tr.findall('./w:tc', NS)
        if len(cells) == 1:
            ps = paragraphs(cells[0])
            days.append({'number': len(days)+1, 'date': (date.fromisoformat(start)+timedelta(days=len(days))).isoformat(), 'label': ps[0], 'theme': ' '.join(ps[1:]), 'items': []})
            continue
        ps = paragraphs(cells[1])
        item = {'time': text(cells[0]), 'title': ps[0]}
        external = 'no course session' in ps[0].lower()
        topics = [re.sub(r'^•\s*', '', p) for p in ps[1:]]
        if topics and not external:
            session += 1
            item.update(session=session, id=f'{code}-r3-s{session}', topics=topics, handouts=[])
        elif external:
            item.update(external=True, topics=topics)
        days[-1]['items'].append(item)
    return days, meta

class Store:
    def __init__(self, key):
        self.aes = AESGCM(key)
        self.parts = [bytearray()]
        self.blocks = {}
    def encrypt(self, value):
        iv = os.urandom(12)
        return b'BD26' + iv + self.aes.encrypt(iv, value, None)
    def block(self, value):
        ident = hashlib.sha256(value).digest()
        if ident in self.blocks:
            return self.blocks[ident]
        if len(self.parts[-1])+len(value)>190000:
            self.parts.append(bytearray())
        ref = [f'p{len(self.parts)-1:04}.enc', len(self.parts[-1]), len(value)]
        self.parts[-1].extend(value)
        self.blocks[ident] = ref
        return ref
    def recipe(self, value, office=False):
        boundaries = [0, len(value)]
        if office:
            with ZipFile(BytesIO(value)) as z:
                boundaries = sorted({0, len(value), z.start_dir, *(x.header_offset for x in z.infolist())})
        refs = []
        for left, right in zip(boundaries, boundaries[1:]):
            for pos in range(left, right, 180000):
                refs.append(self.block(value[pos:min(pos+180000, right)]))
        return self.encrypt(b'BDREC1\n'+json.dumps({'size':len(value),'parts':refs},separators=(',',':')).encode())

def main():
    old = json.loads((DIST/'data.js').read_text().split('=',1)[1].strip().rstrip(';'))
    password = getpass.getpass('Facilitator password (hidden): ')
    username = input('Facilitator username: ').strip().lower()
    salt = os.urandom(32)
    key = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=600000).derive((username+'\0'+password).encode())
    del password
    store = Store(key)
    protected, recipes, verified, activities = [], {}, [], []
    for w in old['workshops']:
        code = w['code']
        rev = 'Rev.3' if code=='A3519987' else 'Rev.3.1'
        source_agenda = next(UPLOAD.glob(f'{code}_Agenda_*_{rev}.docx'))
        data = source_agenda.read_bytes()
        w['days'], meta = agenda(data,code,w['start'])
        w.update(participants=meta['Participants'],outputs=meta['Expected outputs'],revision=rev,durationLabel='4 calendar days · Tuesday afternoon only · final half day' if code=='A3519987' else '2½ days · final half day')
        w['duration'] = 3 if code=='A3519987' else 2.5
        target = DIST/'downloads'/code
        if target.exists():
            shutil.rmtree(target)
        target.mkdir(parents=True)
        agenda_name = source_agenda.name
        (target/agenda_name).write_bytes(data)
        w['agenda'] = f'downloads/{code}/{agenda_name}'
        w['pack'] = f'downloads/{code}/{code}_Participant_Handouts_2026-10-22.zip'
        verified.append({'path':w['agenda'],'sha256':hashlib.sha256(data).hexdigest(),'kind':'agenda','source':source_agenda.name})
        bundle = {agenda_name: data}
        archive = next(UPLOAD.glob(f'{code}_Complete_Materials(2).zip'))
        with ZipFile(archive) as z:
            for name in sorted(z.namelist()):
                base = Path(name).name
                reserve = bool(re.match(code+r'_R[12]_',base))
                if '/Exercise_Handouts/' in name and base.endswith('.docx') and not reserve:
                    blob = z.read(name)
                    (target/base).write_bytes(blob)
                    bundle[base] = blob
                    number = re.search(r'_H([\d.]+)_',base).group(1)
                    session = int(number.split('.')[0])
                    ss = [5,6] if code=='A3519987' and session==5 else [10,11] if code=='A3519987' and session==10 else list(range(1,11)) if code=='A3519988' and session==6 else [session]
                    aid = code+'-h'+number
                    ps = paragraphs(xml(blob).find('w:body',NS))
                    row = {'id':aid,'workshop':w['id'],'code':code,'number':number,'title':ps[1] if len(ps)>1 else base,'file':f'downloads/{code}/{base}','html':as_html(blob),'sessions':ss,'description':'Eight reusable secretariat templates, including the annual budget template.' if code=='A3519988' and session==6 else 'Participant exercise · revised 22 October 2026 · editable Word document'}
                    activities.append(row)
                    for day in w['days']:
                        for s in day['items']:
                            if s.get('session') in ss:
                                s['handouts'].append(aid)
                    verified.append({'path':row['file'],'sha256':hashlib.sha256(blob).hexdigest(),'kind':'handout','source':name})
                elif (('/Slide_Decks/' in name and base.endswith('.pptx')) or ('/Trainer_Scripts/' in name and base.endswith('.docx')) or reserve):
                    blob = z.read(name)
                    session = 0 if reserve else int(re.search(r'_S(\d+)_',base).group(1))
                    kind = 'reserve' if reserve else 'slides' if base.endswith('.pptx') else 'script'
                    path = 'protected/'+base+'.enc'
                    row = {'id':f'{code}-r3-s{session}','workshop':w['id'],'session':session,'kind':kind,'name':base,'file':path,'sha256':hashlib.sha256(blob).hexdigest()}
                    if kind=='slides':
                        with ZipFile(BytesIO(blob)) as p:
                            row['slides'] = sum(bool(re.fullmatch(r'ppt/slides/slide\d+\.xml',n)) for n in p.namelist())
                    else:
                        row['html']=as_html(blob)
                    protected.append(row)
                    recipes[path] = base64.b64encode(store.recipe(blob,office=True)).decode()
                    verified.append({'path':path,'sha256':row['sha256'],'kind':kind,'source':name})
        with ZipFile(DIST/w['pack'],'w',ZIP_DEFLATED) as out:
            for name, blob in sorted(bundle.items()):
                out.writestr(name,blob)
        verified.append({'path':w['pack'],'sha256':hashlib.sha256((DIST/w['pack']).read_bytes()).hexdigest(),'kind':'pack','entries':sorted(bundle)})
    assert [sum('session' in s for d in w['days'] for s in d['items']) for w in old['workshops']] == [12,10]
    assert len(activities)==19 and len(protected)==46
    pdir=DIST/'protected'
    shutil.rmtree(pdir)
    (pdir/'parts').mkdir(parents=True)
    (pdir/'manifest.enc').write_bytes(store.recipe(json.dumps(protected,separators=(',',':')).encode()))
    (pdir/'recipes.enc').write_bytes(store.encrypt(json.dumps(recipes,separators=(',',':')).encode()))
    for i, part in enumerate(store.parts):
        (pdir/'parts'/f'p{i:04}.enc').write_bytes(store.encrypt(bytes(part)))
    (pdir/'kdf.json').write_text(json.dumps({'salt':base64.b64encode(salt).decode(),'iterations':600000,'hash':'SHA-256','format':'BD26'}))
    activities.sort(key=lambda a:(a['code'],float(a['number'])))
    old['activities']=activities
    old['updated']='22 October 2026'
    (DIST/'data.js').write_text('window.BANGLADESH = '+json.dumps(old,separators=(',',':'),ensure_ascii=False)+';\n')
    (ROOT/'verification').mkdir(exist_ok=True)
    (ROOT/'verification'/'materials.json').write_text(json.dumps(verified,indent=2))
    from review_agendas import main as review_agendas
    review_agendas()
    print(json.dumps({'sessions':[12,10],'participantHandouts':len(activities),'protectedFiles':len(protected),'encryptedParts':len(store.parts),'encryptedBytes':sum(p.stat().st_size for p in pdir.rglob('*') if p.is_file())}))

if __name__=='__main__':
    main()
