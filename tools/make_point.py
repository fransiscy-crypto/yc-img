import json,html,os,sys
from playwright.sync_api import sync_playwright
SQ=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'make_thumb.py')).read().split("SQ='")[1].split("'\n")[0]
pts=json.load(open(sys.argv[1])); OUT=sys.argv[2] if len(sys.argv)>2 else '.'
def page(p):
    E=html.escape
    cap=E(p['cap']).replace('\n','<br>')
    big=E(p['big']); fs=104 if len(p['big'])<=10 else (84 if len(p['big'])<=16 else 66)
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0}}.w{{width:1080px;height:720px;background:#FBF4E6;position:relative;overflow:hidden;font-family:'Noto Sans CJK KR','Noto Color Emoji',sans-serif;color:#22304A}}
.box{{position:absolute;left:60px;right:60px;top:60px;bottom:60px;background:#fff;border-radius:36px;border:4px solid #F3D9BF}}
.e{{position:absolute;left:110px;top:105px;font-size:72px}}
.big{{position:absolute;left:110px;right:110px;top:215px;font-size:{fs}px;font-weight:900;color:#E8743B;letter-spacing:-2px;line-height:1.1;word-break:keep-all}}
.cap{{position:absolute;left:110px;right:300px;top:{215+fs*1.1+40}px;font-size:36px;font-weight:600;line-height:1.45;color:#4A5568;word-break:keep-all}}
.f{{position:absolute;left:110px;bottom:100px;font-size:26px;font-weight:800;color:#B9AC98}}.f b{{color:#E8743B}}
svg{{position:absolute;right:70px;bottom:62px}}
</style></head><body><div class="w"><div class="box"></div><div class="e">{p['emoji']}</div><div class="big">{big}</div><div class="cap">{cap}</div>
<div class="f">영끌 말고 <b>영차</b></div><svg width="190" height="190" viewBox="60 30 260 260">{SQ}</svg></div></body></html>'''
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':720})
    for pid,lst in pts.items():
        for i,p in enumerate(lst,1):
            pg.set_content(page(p)); pg.wait_for_timeout(250)
            pg.screenshot(path=os.path.join(OUT,f'{pid}_p{i}.png'))
    b.close()
print('ok')
