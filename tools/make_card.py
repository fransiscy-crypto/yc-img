import json,sys,html
from playwright.sync_api import sync_playwright
SQ=open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'make_thumb.py')).read().split("SQ='")[1].split("'\n")[0]
def page(c):
    E=html.escape
    rows="".join(f'<tr><th>{E(a)}</th><td>{E(b)}</td></tr>' for a,b in c['rows'])
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0}}.w{{width:1080px;height:1350px;background:#FBF4E6;position:relative;overflow:hidden;font-family:'Noto Sans CJK KR','Noto Sans KR','Malgun Gothic','Apple SD Gothic Neo','Noto Color Emoji','Segoe UI Emoji',sans-serif;color:#22304A}}
.tag{{position:absolute;left:72px;top:70px;background:#E8743B;color:#fff;font-size:30px;font-weight:700;padding:8px 22px;border-radius:30px}}
h1{{position:absolute;left:72px;right:72px;top:140px;margin:0;font-size:60px;font-weight:900;letter-spacing:-1.5px;line-height:1.2;word-break:keep-all}}
table{{position:absolute;left:72px;right:72px;top:310px;width:936px;border-collapse:separate;border-spacing:0 12px}}
th{{width:300px;text-align:left;vertical-align:top;font-size:31px;font-weight:800;color:#B4532A;background:#fff;padding:18px 20px;border-radius:18px 0 0 18px;word-break:keep-all}}
td{{font-size:30px;font-weight:500;line-height:1.38;background:#fff;padding:18px 24px 18px 6px;border-radius:0 18px 18px 0;word-break:keep-all}}
.note{{position:absolute;left:72px;bottom:70px;font-size:24px;color:#7A6A55;width:640px}}
.f{{position:absolute;left:72px;bottom:110px;font-size:30px;font-weight:800;color:#7A6A55}}.f b{{color:#E8743B}}
svg{{position:absolute;right:24px;bottom:-6px}}
</style></head><body><div class="w"><div class="tag">핵심 정리</div><h1>{E(c['title'])}</h1><table>{rows}</table>
<div class="f">영끌 말고 <b>영차</b></div><div class="note">※ {E(c['note'])}</div>
<svg width="200" height="200" viewBox="60 30 260 260">{SQ}</svg></div></body></html>'''
cards=json.load(open(sys.argv[1]))
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1350})
    for c in cards:
        pg.set_content(page(c)); pg.wait_for_timeout(200)
        h=pg.evaluate("document.querySelector('table').getBoundingClientRect().bottom")
        pg.screenshot(path=c['file']); print(c['file'], 'table bottom', int(h))
    b.close()
