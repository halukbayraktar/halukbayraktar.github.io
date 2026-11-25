#!/usr/bin/env python3
"""X (Twitter) arşivinden siteye paylaşımları aktarır.

Kullanım: python3 tools/twitter_ice_aktar.py <arşiv>/data
Üretir: _data/tweets.json ve paylasimlar/<yıl>.html sayfaları.
Görseller paylasimlar/img/<tweetid>-<ad>.jpg olarak beklenir.
Yalnızca kendi paylaşımlar ve kendine yanıt (seri) alınır; RT ve başkalarına yanıtlar alınmaz.
"""
import json, os, sys, html, re, datetime

KULLANICI = "haluk"
data = sys.argv[1]
kok = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def yukle(ad):
    p = os.path.join(data, ad)
    if not os.path.exists(p):
        return []
    s = open(p, encoding="utf-8").read()
    return json.loads(s[s.index("=") + 1:])

tweets = [x["tweet"] for x in yukle("tweets.js")]
notlar = {}
for n in yukle("note-tweet.js"):
    n = n["noteTweet"]
    notlar[n["createdAt"][:19]] = n["core"]

def tarih(t):
    return datetime.datetime.strptime(t["created_at"], "%a %b %d %H:%M:%S %z %Y")

def metin(t):
    txt = t["full_text"]
    ent = t.get("entities", {})
    urls = ent.get("urls", [])
    dt = tarih(t).strftime("%Y-%m-%dT%H:%M:%S")
    nt = notlar.get(dt)
    if nt and len(nt.get("text", "")) > len(txt) - 30:
        txt = nt["text"]
        urls = nt.get("urls", [])
    # medya linklerini kaldır
    for m in t.get("extended_entities", {}).get("media", []):
        txt = txt.replace(m.get("url", "@@"), "")
    txt = html.unescape(txt).strip()
    out = html.escape(txt)
    for u in urls:
        short = u.get("url")
        if not short:
            continue
        exp = u.get("expanded_url") or short
        disp = u.get("display_url") or exp
        out = out.replace(html.escape(short), '<a href="%s">%s</a>' % (html.escape(exp, True), html.escape(disp)))
    return out.replace("\n", "<br>")

def gorseller(t):
    g = []
    for m in t.get("extended_entities", {}).get("media", [])[:4]:
        ad = t["id_str"] + "-" + m["media_url_https"].split("/")[-1].rsplit(".", 1)[0] + ".jpg"
        if os.path.exists(os.path.join(kok, "paylasimlar", "img", ad)):
            g.append("/paylasimlar/img/" + ad)
    return g

def video_mu(t):
    return any(m.get("type") in ("video", "animated_gif") for m in t.get("extended_entities", {}).get("media", []))

kendi = {t["id_str"]: t for t in tweets if not t["full_text"].startswith("RT @")}
ana = {}
seri = {}
for t in sorted(kendi.values(), key=tarih):
    r = t.get("in_reply_to_status_id_str")
    if not r:
        ana[t["id_str"]] = t
    elif (t.get("in_reply_to_screen_name") or "").lower() == KULLANICI:
        kok_id = r
        while kok_id in seri:
            kok_id = seri[kok_id]
        seri[t["id_str"]] = kok_id

devam = {}
for tid, kid in seri.items():
    if kid in ana:
        devam.setdefault(kid, []).append(kendi[tid])

kayitlar = []
for tid, t in ana.items():
    d = tarih(t)
    parcalar = [t] + sorted(devam.get(tid, []), key=tarih)
    kayitlar.append({
        "id": tid,
        "date": d.strftime("%Y-%m-%d %H:%M"),
        "year": d.year,
        "html": "<br><br>".join(metin(p) for p in parcalar),
        "images": [g for p in parcalar for g in gorseller(p)][:4],
        "video": any(video_mu(p) for p in parcalar),
        "url": "https://x.com/%s/status/%s" % (KULLANICI, tid),
        "type": "paylasim",
    })
kayitlar.sort(key=lambda k: k["date"], reverse=True)
json.dump(kayitlar, open(os.path.join(kok, "_data", "tweets.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)

yillar = sorted({k["year"] for k in kayitlar}, reverse=True)
for y in yillar:
    with open(os.path.join(kok, "paylasimlar", "%d.html" % y), "w", encoding="utf-8") as f:
        f.write("---\nlayout: yil\nyear: %d\ntitle: Paylaşımlar · %d\npermalink: /paylasimlar/%d/\n---\n" % (y, y, y))
print(len(kayitlar), "paylaşım,", len(yillar), "yıl")
