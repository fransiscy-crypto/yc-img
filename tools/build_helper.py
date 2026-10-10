# -*- coding: utf-8 -*-
"""posts.json -> (1) 미리보기/수동 도우미 HTML  (2) 자동 입력 프로그램용 원고 패키지
usage: python3 build6.py posts.json imgdir out_html macro_dir
본문 표기: [그림:card|p1|p2]  !! 강조  * 글머리  > 인용 묶음  Q./A.  ※ 작은글씨  URL줄
헤더: '## ' 또는 【 / ▍ / 📅 📌 ❌ ✅ 로 시작하는 짧은 한 줄
"""
import json, base64, html, sys, re, os, random, shutil
src, imgdir, out_html, mdir = sys.argv[1:5]
IMG_BASE = os.environ.get("IMG_BASE", "")  # 예: https://cdn.jsdelivr.net/gh/아이디/저장소@main/week1012/
d = json.load(open(src))
E = lambda s: html.escape(s, quote=False)
NUM = re.compile(r"((?:약 |최대 |연 |월 |한 달 )?(?:\d+억\s?\d[\d,]*(?:만|천)(?:\s?원)?|\d[\d,\.]*(?:\s?(?:%p|%|만 원|억 원|천 원|원|건|만 건|억|만)))(?:\s?(?:~|→)\s?\d[\d,\.]*(?:\s?(?:%p|%|만 원|억 원|원|만|억))?)?)")
HEAD = re.compile(r"^(## |【|▍|📅|📌|❌ 오해|✅ )")

# 글마다 다른 서식 세트 (주차+글번호로 고정 시드 → 매주 조합이 바뀜)
HL = ["#FFF1A8", "#D3F9D8", "#FFE3E3", "#D0EBFF", "#FFE8CC", "#E5DBFF"]
NUMC = ["#D9480F", "#1971C2", "#C2255C", "#2B8A3E", None, None]
BUL = ["• ", "✔ ", "▪ ", "☑️ ", "👉 ", "· "]
HC = ["#22304A", "#E8743B", "#1864AB", "#5F3DC4", "#2B8A3E", "#C92A2A"]
HSIZE = [24, 24, 28]

def style_for(pid):
    r = random.Random(d["week"] + pid)
    return dict(hl=r.choice(HL), num=r.choice(NUMC), bul=r.choice(BUL), hc=r.choice(HC), hs=r.choice(HSIZE),
                qemo=r.choice(["🙋", "💭", "🤔", "❓"]))

GAP = "<p><br></p>"
BLANK = "<p><br></p>"

def P(inner, extra=""):
    return f'<p style="line-height:1.85;background-color:transparent;{extra}"><span style="font-size:16px;background-color:transparent">{inner}</span></p>'

def render(body, S):
    numfx = (lambda s: NUM.sub(lambda m: f'<b><span style="color:{S["num"]}">{m.group(1)}</span></b>', s)) if S["num"] else (lambda s: NUM.sub(lambda m: f'<b>{m.group(1)}</b>', s))
    blocks = []  # ("h", html, text) | ("img", key)
    for p in [x.strip() for x in body.split("\n\n") if x.strip()]:
        m = re.match(r"^\[그림:(\w+)\]$", p)
        if m: blocks.append(("img", m.group(1))); continue
        if "\n" not in p and HEAD.match(p) and len(p) < 50:
            t = p[3:] if p.startswith("## ") else p
            pre = (S["qemo"] + " ") if p.startswith("## ") and t.endswith("?") else ""
            blocks.append(("h", f'<p style="line-height:1.6"><span style="font-size:{S["hs"]}px;color:{S["hc"]};background-color:transparent"><b>{pre}{E(t)}</b></span></p>', pre + t)); continue
        if p.startswith(">"):
            lines = [l.lstrip("> ").strip() for l in p.split("\n")]
            inner = "<br>".join(numfx(E(l)) for l in lines)
            blocks.append(("h", P(inner, f"border-left:4px solid {S['hc']};padding:6px 0 6px 14px;background:#F8F9FA"), "\n".join(lines))); continue
        if p.startswith("!! "):
            t = p[3:]
            blocks.append(("h", P(f'<span style="background-color:{S["hl"]}"><b>{numfx(E(t))}</b></span>'), t)); continue
        if p.startswith("* "):
            ls = [l[2:].strip() for l in p.split("\n")]
            blocks.append(("h", "".join(P(S["bul"] + numfx(E(l))) for l in ls), "\n".join(S["bul"] + l for l in ls))); continue
        if p.startswith("Q.") and "\nA." in p:
            q, a = p.split("\nA.", 1)
            blocks.append(("h", P(f'<b>{E(q)}</b><br>A.{numfx(E(a))}'), f"{q}\nA.{a}")); continue
        if p.startswith("※"):
            blocks.append(("h", f'<p style="font-size:13px;color:#888;line-height:1.7">{E(p)}</p>', p)); continue
        if re.match(r"^https?://\S+$", p):
            blocks.append(("h", f'<p style="font-size:14px"><a href="{E(p)}">{E(p)}</a></p>', p)); continue
        m = re.match(r"^(STEP \d+\.)(.*)$", p, re.S)
        if m:
            blocks.append(("h", P(f'<b style="color:{S["hc"]}">{E(m.group(1))}</b>{numfx(E(m.group(2)))}'), p)); continue
        blocks.append(("h", P(numfx(E(p))), p))
    # 연속 텍스트 블록 묶기
    segs = []
    for b in blocks:
        if b[0] == "img": segs.append({"t": "img", "k": b[1]})
        else:
            if segs and segs[-1]["t"] == "html": segs[-1]["html"] += GAP + b[1]; segs[-1]["text"] += "\n\n" + b[2]
            else: segs.append({"t": "html", "html": GAP + b[1] + "", "text": b[2]})
    return segs

def b64(p): return "data:image/png;base64," + base64.b64encode(open(p, "rb").read()).decode()
arr = lambda x: x if isinstance(x, list) else [s for s in str(x or "").replace(",", "\n").split("\n") if s.strip()]

os.makedirs(os.path.join(mdir, "img"), exist_ok=True)
H, M = [], []
for p in d["posts"]:
    pid = p["id"]; S = style_for(pid)
    segs = [{"t": "img", "k": "thumb"}] + render(p["body"], S)
    files = {"thumb": f"{pid}.png", "card": f"{pid}_card.png", "p1": f"{pid}_p1.png", "p2": f"{pid}_p2.png"}
    n = 0; prev = ""; plain = []; mseg = []
    for s in segs:
        if s["t"] == "img":
            n += 1; fn = files[s["k"]]
            shutil.copy(os.path.join(imgdir, fn), os.path.join(mdir, "img", fn))
            s["src"] = (IMG_BASE + fn) if IMG_BASE else b64(os.path.join(imgdir, fn)); s["n"] = n
            prev += f'<div class="im" data-n="{n}"><span>그림 {n} · 클릭하면 복사</span><p style="text-align:center"><img src="{s["src"]}" style="max-width:100%;width:640px"></p></div>'
            plain.append(f"[그림 {n}]")
            mseg.append({"type": "image", "file": "img/" + fn})
        else:
            prev += s["html"]; plain.append(s["text"])
            mseg.append({"type": "html", "html": s["html"], "text": s["text"]})
    tags = arr(p["tags"])
    date_iso = p.get("date_iso") or ("2026-" + re.sub(r"[^\d/]", "", p["date"]).replace("/", "-").zfill(5))
    H.append({k: p[k] for k in ("id", "date", "time", "type", "category", "titles")} | {"tags": tags, "check": arr(p.get("check")), "sources": arr(p.get("sources")), "prev": prev, "plain": "\n\n".join(plain), "nimg": n, "len": len(p["body"])})
    M.append({"id": pid, "date": p["date"], "date_iso": date_iso, "time": p["time"], "category": p["category"], "title": p["titles"][0], "titles": p["titles"], "tags": tags, "segments": mseg})
json.dump({"week": d["week"], "posts": M}, open(os.path.join(mdir, "posts.json"), "w"), ensure_ascii=False, indent=1)
tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.environ.get("TPL","helper_tpl.html"))).read()
open(out_html, "w").write(tpl.replace("__VER__", d["week"]).replace("__DATA__", json.dumps({"week": d["week"], "posts": H}, ensure_ascii=False)))
print("ok", out_html, mdir)
