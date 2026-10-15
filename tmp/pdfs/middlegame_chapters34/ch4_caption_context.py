import ast, json
from pathlib import Path

HERE=Path(__file__).parent
tree=ast.parse((HERE/'build_chapter_four_illustrated.py').read_text(encoding='utf-8'))
figs=None
for node in tree.body:
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='FIGURES' for t in node.targets):
        figs=ast.literal_eval(node.value)
assert figs
for i,(pg,n,x,y,label) in enumerate(figs,1):
    blocks=json.loads((HERE/'source'/f'page-{pg:03d}-ocr.json').read_text(encoding='utf-8'))
    side=[b for b in blocks if (b['x']<780)==(x<780) and b['bottom'] <= y+10]
    side.sort(key=lambda b:(b['y'],b['x']))
    ctx=' | '.join(b['text'].replace('\n',' ') for b in side[-8:])
    print(f'{i:02d} p{pg} x{x} y{y} :: {ctx}')
