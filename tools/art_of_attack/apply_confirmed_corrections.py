"""Apply the user's recorded corrections to the first five chapters only."""
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[2]
FOLDER=ROOT/'translations/art_of_attack/translation'
SPECIFIC={
 'IN-3': [('局面思想','局面棋思想')],
 'IN-4': [('对局面认识的加深','对局面棋理解的加深'),('准确的局面走法','准确的局面棋走法')],
 'IN-8': [('局面技术','局面棋技术')],
 'IN-12': [('正常的局面走法','正常的局面棋走法')],
 'IN-15': [('选择局面走法','选择局面棋走法')],
 'IN-40': [('直到当时仍被接受','直到本书写作时仍被接受')],
 'IN-43': [('进攻方的局面优势','进攻方在局面棋方面的优势')],
 'IN-45': [('局面技术','局面棋技术')],
 'CH1-19': [('拒绝王翼弃兵','王翼弃兵拒弃兵变例')],
 'CH1-121': [('拒绝后翼弃兵','后翼弃兵拒弃兵变例')],
 'CH1-133': [('子力优势和局面优势','子力优势和局面棋方面的优势')],
 'CH2-41': [('位置上的不利','局面棋方面的不利')],
 'CH2-197': [('位置上的错误','局面棋方面的错误')],
 'CH2-224': [('位置型风格','局面棋风格')],
 'CH2-226': [('接受王翼弃兵','王翼弃兵接受弃兵变例')],
 'CH3-10': [('动态意义与位置意义','动态意义与局面棋意义')],
 'CH3-11': [('动态或位置的角度','动态或局面棋的角度')],
 'CH3-13': [('位置性的走法','局面棋走法'),('持久的位置特征','持久的局面棋特征')],
 'CH3-67': [('位置性的阵形','局面棋阵形')],
 'CH3-70': [('纯粹的位置调动','纯粹的局面棋调动')],
 'CH3-71': [('主要位置原则','主要局面棋原则')],
 'CH3-114': [('位置性弃子','局面棋弃子'),('位置战','局面棋')],
 'CH5-64': [('拒后翼弃兵','后翼弃兵拒弃兵变例')],
 'CH5-302': [('局面战','局面棋'),('其原因在于局面本身','其原因在于局面棋的特点')],
 'CH5-389': [('局面计划','局面棋计划')],
}
GENERAL=[('经典弃象','古典弃象'),('菲利多尔','菲利道尔'),('菲利多','菲利道尔'),('纳伊多夫','纳道尔夫'),
         ('埃文斯弃兵','伊文斯弃兵'),('蒙目车轮战','盲棋车轮战')]


def main():
    changes=[]
    for stem in ['front_preface','introduction','ch01','ch02','ch03','ch04','ch05']:
        path=FOLDER/f'{stem}_v1.md'
        raw=path.read_bytes()
        ending='\r\n' if b'\r\n' in raw else '\n'
        old=raw.decode('utf-8').replace('\r\n','\n')
        pieces=re.split(r'(?m)(?=^## )',old)
        for i,block in enumerate(pieces):
            if not block.startswith('## '):continue
            sid=block[3:].split('|',1)[0].strip()
            pairs=GENERAL+SPECIFIC.get(sid,[])
            lines=block.splitlines(keepends=True)
            for j,line in enumerate(lines):
                if not line.startswith(('ZH: ','FIG: ')):continue
                before=line
                for a,b in pairs:line=line.replace(a,b)
                if line!=before:
                    changes.append({'segment':sid,'file':path.name,'before':before.strip(),'after':line.strip()})
                    lines[j]=line
            pieces[i]=''.join(lines)
        revised=''.join(pieces)
        if revised!=old:path.write_bytes(revised.replace('\n',ending).encode('utf-8'))
    report=FOLDER/'confirmed_corrections_applied_20261016.json'
    # Preserve the first audit log on a no-op rerun.
    if changes:report.write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'changed_fields':len(changes),'report':str(report)},ensure_ascii=False))


if __name__=='__main__':main()
