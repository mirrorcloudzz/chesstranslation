"""Compare the language-reviewed authoritative sources with the v2 snapshot.

This is a structural regression check, not an automated language evaluator.
"""
import hashlib
import json
import re
from build_complete_proofs import NAMES, DEST
from build_opening_proofs import PROJECT, ROOT, parse_file

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

# Every exception below was checked directly against the original scan.
APPROVED_ENGLISH={
    'CH10-105':[("1 1...c4'?",'11... c4?')],
    'CH10-239':[('(otherwise 3... Bf8 3... Rg7','(otherwise 3... Bf8!) 3... Rg7')],
    'CH10-318':[('Qxd1 !','Qxd1!')],
    'CH10-405':[('Ne5 !','Ne5!')],
    'CH10-56':[("without the black 1 pawn on b5. Qukovié's", "without the black pawn on b5. Vuković's")],
    'CH10-76':[('I1...Ne8','11... Ne8')],
    'CH10-101':[('I I Ne5','11. Ne5')],
    'CH10-119':[('planning . Qd6','planning ...Qd6'),('because of Qxf5','because of ...Qxf5')],
    'CH10-250':[('threatening7 Rh3','threatening 7. Rh3')],
    'CH11-390':[('I ...Ne4! ! ,','1... Ne4!,')],
}

def main():
    folder=PROJECT/'translation'
    reasons={}
    for path in folder.glob('language_review_*_20261018.json'):
        if path.name=='language_review_complete_20261018.json':continue
        log=json.loads(path.read_text(encoding='utf-8'))
        records=log if isinstance(log,list) else log.get('changes',[])
        for record in records:
            field=record.get('field','zh').lower()
            field={'translation':'zh','english':'text','en':'text','caption':'caption_zh'}.get(field,field)
            reasons.setdefault((record['id'],field),[]).append({'log':path.name,'reason':record['reason']})
    old=json.loads((folder/'segments_complete_v2.json').read_text(encoding='utf-8'))
    current=[s for stem,*_ in NAMES for s in parse_file(stem)]
    assert [s['segment_id'] for s in old]==[s['segment_id'] for s in current]
    changes=[];errors=[];transcription=[]
    protected=['text','section','page','page_end','kind','figure_id','note_anchor']
    san=re.compile(r'(?<![A-Za-z])(?:[KQRBN][a-h1-8]?[a-h1-8]?x?[a-h][1-8](?:=[QRBN])?[+#]?[!?]*|[a-h]x?[a-h]?[1-8](?:=[QRBN])?[+#]?[!?]*|O-O(?:-O)?[+#]?[!?]*)(?![A-Za-z])')
    for before,after in zip(old,current):
        sid=before['segment_id']
        for field in protected:
            if before.get(field)!=after.get(field):
                if field=='text' and sid in APPROVED_ENGLISH:
                    expected=before[field]
                    for original,corrected in APPROVED_ENGLISH[sid]:
                        assert expected.count(original)==1,sid
                        expected=expected.replace(original,corrected)
                    if after[field]==expected:
                        entry={'segment':sid,'section':after['section'],'page':after['page'],
                               'field':field,'before':before[field],'after':after[field],
                               'reason':'Original scan independently checked; OCR/typography correction only'}
                        changes.append(entry);transcription.append(entry)
                    else:errors.append({'segment':sid,'field':field,'reason':'not the specifically approved transcription correction'})
                else:errors.append({'segment':sid,'field':field})
        for field in ['zh','caption_zh']:
            if before.get(field)!=after.get(field):
                b=before.get(field,'');a=after.get(field,'')
                changes.append({'segment':sid,'section':after['section'],'page':after['page'],
                                'field':field,'before':b,'after':a})
                if san.findall(b)!=san.findall(a):
                    # This explanation deliberately repeats the target f7;
                    # it adds a coordinate mention, not a chess move.
                    coordinate_explanation=(sid=='CH5-219' and field=='zh' and
                        a=='现在由象来攻击f7，效果与上面变化中由后攻击f7同样好。')
                    if not coordinate_explanation:errors.append({'segment':sid,'field':field,'reason':'SAN tokens changed'})
        if before['kind']=='moves' and before['zh']!=after['zh']:
            errors.append({'segment':sid,'reason':'pure moves block changed'})
    historical=json.loads((folder/'proof_manifest_complete_v2.json').read_text(encoding='utf-8'))
    historical_ok=all(digest(ROOT/m['path'])==m['sha256'] for m in historical)
    if not historical_ok:errors.append({'reason':'historical v2 PDF changed'})
    counts={stem:sum(s['section']==stem for s in current) for stem,*_ in NAMES}
    for change in changes:
        change['review_reasons']=reasons.get((change['segment'],change['field']),[])
        if not change['review_reasons']:errors.append({'segment':change['segment'],'field':change['field'],'reason':'change lacks an individual review record'})
    result={'date':'2026-10-18','baseline':'segments_complete_v2.json',
            'scope':'Structural comparison only; human EN/ZH language reading is documented in the separate chapter review notes.',
            'sections':counts,'units':len(current),'changed_units':len({x['segment'] for x in changes}),
            'changed_fields':len(changes),'historical_v2_pdf_hashes_match':historical_ok,
            'protected_fields':protected,'scan_verified_english_exceptions':transcription,'errors':errors,'changes':changes,
            'source_sha256':{stem:digest(folder/f'{stem}_v1.md') for stem,*_ in NAMES}}
    (folder/'language_review_complete_20261018.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ['changes','source_sha256','scan_verified_english_exceptions']},ensure_ascii=False,indent=2))
    return 1 if errors else 0

if __name__=='__main__':
    raise SystemExit(main())
