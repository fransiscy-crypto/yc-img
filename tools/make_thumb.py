import json,sys,html
from playwright.sync_api import sync_playwright
SQ='<g><path d="M196 236 C 300 236, 312 112, 250 72 C 206 46, 168 86, 200 112 C 226 132, 236 168, 196 206 Z" fill="#C97A3F"/><ellipse cx="125" cy="262" rx="20" ry="10" fill="#B86C36"/><ellipse cx="175" cy="262" rx="20" ry="10" fill="#B86C36"/><ellipse cx="150" cy="196" rx="62" ry="68" fill="#E0935A"/><ellipse cx="150" cy="212" rx="40" ry="46" fill="#FBE3C8"/><path d="M106 80 Q 96 34 132 60 Z" fill="#E0935A"/><path d="M194 80 Q 204 34 168 60 Z" fill="#E0935A"/><circle cx="150" cy="118" r="56" fill="#E0935A"/><ellipse cx="150" cy="138" rx="30" ry="20" fill="#FBE3C8"/><circle cx="129" cy="114" r="7" fill="#2B2B3A"/><circle cx="171" cy="114" r="7" fill="#2B2B3A"/><circle cx="131" cy="111" r="2.2" fill="#fff"/><circle cx="173" cy="111" r="2.2" fill="#fff"/><ellipse cx="150" cy="130" rx="6" ry="4.5" fill="#6B3E22"/><path d="M142 139 q 4 6 8 0 q 4 6 8 0" stroke="#6B3E22" stroke-width="3.5" fill="none" stroke-linecap="round"/><ellipse cx="113" cy="134" rx="10" ry="7" fill="#F29A8E" opacity=".65"/><ellipse cx="187" cy="134" rx="10" ry="7" fill="#F29A8E" opacity=".65"/><ellipse cx="150" cy="206" rx="22" ry="25" fill="#F2C14E" stroke="#C9952A" stroke-width="3"/><ellipse cx="150" cy="185" rx="27" ry="12" fill="#8A5A35"/><rect x="147" y="168" width="6" height="10" rx="3" fill="#6B3E22"/><ellipse cx="124" cy="204" rx="11" ry="15" fill="#E0935A" transform="rotate(-20 124 204)"/><ellipse cx="176" cy="204" rx="11" ry="15" fill="#E0935A" transform="rotate(20 176 204)"/></g>'
def page(title,cat):
    t=html.escape(title); c=html.escape(cat)
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0}}.w{{width:1080px;height:1080px;background:#FBF4E6;position:relative;overflow:hidden;font-family:'Noto Sans CJK KR',sans-serif}}
.tag{{position:absolute;left:80px;top:90px;background:#E8743B;color:#fff;font-size:34px;font-weight:700;padding:10px 26px;border-radius:40px}}
.t{{position:absolute;left:80px;right:80px;top:190px;font-size:88px;font-weight:900;line-height:1.22;color:#22304A;letter-spacing:-2px;word-break:keep-all}}
.f{{position:absolute;left:80px;bottom:80px;font-size:36px;font-weight:700;color:#7A6A55}}.f b{{color:#E8743B}}
.hill{{position:absolute;left:0;bottom:0}}
</style></head><body><div class="w"><div class="tag">{c}</div><div class="t">{t}</div>
<svg class="hill" width="1080" height="1080" viewBox="0 0 1080 1080"><path d="M0 1080 L0 1000 Q 600 980 1080 820 L1080 1080 Z" fill="#CFE3C6"/>
<g transform="translate(640 600) scale(1.45)">{SQ}</g></svg>
<div class="f">영끌 말고 <b>영차</b></div></div></body></html>'''
items=json.load(open(sys.argv[1]))
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1080})
    for it in items:
        pg.set_content(page(it['title'],it['category'])); pg.wait_for_timeout(200)
        pg.screenshot(path=it['file']); print(it['file'])
    b.close()
