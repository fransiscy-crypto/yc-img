# -*- coding: utf-8 -*-
"""한 주 묶음 만들기
usage: python3 tools/make_week.py posts.json w1019 out.html
posts.json: {"week": "...", "posts": [{id,date,date_iso,time,type,category,titles[3],tags[5],check,sources,
             thumb_title,thumb_cat,card:{title,rows:[[라벨,값],...],note},points:[{emoji,big,cap},{...}],body}]}
결과: <repo>/<folder>/ 에 그림 생성(d1.png, d1_card.png, d1_p1.png, d1_p2.png …) + 도우미 HTML
"""
import json, os, subprocess, sys, tempfile, time
T = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(T)
src, folder, out_html = sys.argv[1:4]
d = json.load(open(src)); od = os.path.join(R, folder); os.makedirs(od, exist_ok=True)
tmp = tempfile.mkdtemp()
th = [{"title": p["thumb_title"], "category": p["thumb_cat"], "file": os.path.join(od, p["id"] + ".png")} for p in d["posts"]]
cd = [dict(p["card"], file=os.path.join(od, p["id"] + "_card.png")) for p in d["posts"]]
pt = {p["id"]: p["points"] for p in d["posts"]}
for name, obj in (("th", th), ("cd", cd), ("pt", pt)):
    json.dump(obj, open(os.path.join(tmp, name + ".json"), "w"), ensure_ascii=False)
py = sys.executable
subprocess.run([py, os.path.join(T, "make_thumb.py"), os.path.join(tmp, "th.json")], check=True)
subprocess.run([py, os.path.join(T, "make_card.py"), os.path.join(tmp, "cd.json")], check=True)
subprocess.run([py, os.path.join(T, "make_point.py"), os.path.join(tmp, "pt.json"), od], check=True)
env = dict(os.environ, IMG_VER=str(int(time.time())), IMG_BASE=f"https://raw.githubusercontent.com/fransiscy-crypto/yc-img/main/{folder}/")
subprocess.run([py, os.path.join(T, "build_helper.py"), src, od, out_html, os.path.join(tmp, "pkg")], check=True, env=env)
print("done:", od, out_html)
