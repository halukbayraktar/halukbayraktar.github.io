#!/usr/bin/env python3
"""Tarayıcıdan toplanan yeni tweet'leri _data/tweets.json'a ekler.

Kullanım: python3 tools/yeni_tweetler_ekle.py yeni.json
yeni.json: [{"id": "...", "date": "2026-11-30T10:00:00.000Z", "text": "...",
             "media": ["G1abc..."], "fmt": ["jpg"], "video": false}, ...]
Görseller X'in sunucusundan gösterilir (pbs.twimg.com), indirilmez.
Zaten olan id'ler atlanır. Yeni bir yıl gelirse yıl sayfası oluşturulur.
"""
import json, os, sys, html, re, datetime

KULLANICI = "haluk"
kok = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
yol = os.path.join(kok, "_data", "tweets.json")
mevcut = json.load(open(yol, encoding="utf-8"))
idler = {k["id"] for k in mevcut}

def metin_html(t):
    out = html.escape(t.strip())
    out = re.sub(r"(https?://[^\s<]+)", r'<a href="\1">\1</a>', out)
    return out.replace("\n", "<br>")

eklenen = 0
for t in json.load(open(sys.argv[1], encoding="utf-8")):
    if t["id"] in idler or (not t.get("text") and not t.get("media")):
        continue
    d = datetime.datetime.fromisoformat(t["date"].replace("Z", "+00:00"))
    fmts = t.get("fmt") or []
    imgs = ["https://pbs.twimg.com/media/%s?format=%s&name=medium" % (m, fmts[i] if i < len(fmts) else "jpg")
            for i, m in enumerate(t.get("media", []))][:4]
    mevcut.append({
        "id": t["id"], "date": d.strftime("%Y-%m-%d %H:%M"), "year": d.year,
        "html": metin_html(t.get("text", "")), "images": imgs, "video": bool(t.get("video")),
        "url": "https://x.com/%s/status/%s" % (KULLANICI, t["id"]), "type": "paylasim",
    })
    idler.add(t["id"]); eklenen += 1
    sayfa = os.path.join(kok, "paylasimlar", "%d.html" % d.year)
    if not os.path.exists(sayfa):
        open(sayfa, "w", encoding="utf-8").write(
            "---\nlayout: yil\nyear: %d\ntitle: Paylaşımlar · %d\npermalink: /paylasimlar/%d/\n---\n" % (d.year, d.year, d.year))

mevcut.sort(key=lambda k: k["date"], reverse=True)
json.dump(mevcut, open(yol, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(eklenen, "yeni paylaşım eklendi")
