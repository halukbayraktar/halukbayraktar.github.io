import json,re,html,collections,sys
KONULAR=[
("anma","Anma ve Özel Günler",["özdemir bayraktar","rahmet","şehit","sehit","vefat","anıyoruz","başsağlığı","taziye","condolence","ruhu şad","mekânı cennet","mekanı cennet"]),
("spor","Spor ve Doğa",["yüzme","yüzerek","yüzücü","kulaç","maraton","marathon","triatlon","triathlon","koşu","koştu","run ","trail","ultra","babadağ","zirve","bisiklet","pedal","#bizimçocuklar","bizimcocuklar","şampiyon","euroleague","finalfour","olimpiyat","milli takım","futbol","voleybol","balık","fishing","dalış"]),
("insani","İyilik ve İnsani Yardım",["filistin","gazze","gaza","palestin","rafah","israil","israel","soykırım","genocide","deprem","earthquake","yardım","bağış","mazlum","zulüm","yetim","afrika","burkina","somali","sumud","türkiyetekyürek","tekyürek","kızılay","afad"]),
("teknofest","TEKNOFEST, T3 Vakfı ve Gençler",["teknofest","deneyap","t3vakf","t3 vakf","@t3","bilim merkez","bilim üsküdar","bilimtiran","bilim kyiv","science kyiv","yarışma","gençlerimiz","gençler","öğrenci","üniversite","1001 teknoloji","girişim merkezi","t3gm"]),
("saha","SAHA ve Savunma Sanayii",["saha","savunma sanayi","defense industry","defence industry","defence","fuar","expo","kümelen","cluster","ssb","aselsan","roketsan","tusaş","havelsan","tübitak","tubitak","sanayi"]),
("ukrayna","Ukrayna ve Dünya",["ukrayna","ukraine","kyiv","kiev","zelensk","україн","слава","azerbaycan","azerbaijan","karabağ","karabag","pakistan","kosova","bosna","srebrenitsa","arnavutluk","albania","shqip","türk dünyası","özbekistan","kazakistan","kırgız","türkmen","libya","katar","qatar","polonya","poland","italy","italya","piaggio","malezya","endonezya","japonya","kenya","suriye","syria"]),
("uzay","Uzay",["uzay","space","#iac","iac202","astronot","astronaut","roket ","rocket","uydu","satellite","yörünge","orbit","ay görevi","moon"]),
("siha","Baykar ve SİHA'lar",["tb2","tb3","akıncı","akinci","kızılelma","kizilelma","kızıl elma","siha","iha","uav","ucav","drone","dron","baykar","bayraktar","uçuş","flight","test","sivrisinek","k2","ihracat","export","motor","otonom","autonomous","yapay zeka","milliteknolojihamlesi"]),
("anma","Anma ve Özel Günler",["rahmet","şehit","sehit","başsağlığı","taziye","condolence","vefat","mekanı cennet","mekânı cennet","ruhu şad","anıyoruz","bayram","kutlu olsun","cumhuriyet","15 temmuz","zafer","kandil","ramazan","hayırlı","tebrik","çanakkale","atatürk","anneler günü","babalar günü","öğretmenler günü","yeni yıl","mübarek","özdemir bayraktar","babam","babamız","istikbal göklerdedir"]),
]
def konu(x):
    t=re.sub(r'<[^>]+>',' ',html.unescape(x.get('html',''))).lower()
    for slug,ad,ws in KONULAR:
        if any(w in t for w in ws): return slug
    return "genel"
ADLAR=dict((k,a) for k,a,_ in reversed(KONULAR)); ADLAR["genel"]="Diğer"

def uygula(kok):
    """tweets.json'daki her paylaşıma 'konu' ekler, konu sayfalarını ve _data/konular.yml'i yazar."""
    import os, collections
    yol=os.path.join(kok,"_data","tweets.json")
    d=json.load(open(yol,encoding="utf-8"))
    for x in d: x["konu"]=konu(x)
    json.dump(d,open(yol,"w",encoding="utf-8"),ensure_ascii=False,indent=0)
    c=collections.Counter(x["konu"] for x in d)
    sira=["siha","teknofest","saha","uzay","ukrayna","insani","anma","spor","genel"]
    with open(os.path.join(kok,"_data","konular.yml"),"w",encoding="utf-8") as f:
        f.write("# tools/konular.py tarafından üretilir. Anahtar kelimelerle otomatik sınıflandırma.\n")
        for k in sira:
            f.write('- slug: %s\n  ad: "%s"\n  sayi: %d\n' % (k, ADLAR[k], c.get(k,0)))
    os.makedirs(os.path.join(kok,"paylasimlar","konu"),exist_ok=True)
    for k in sira:
        open(os.path.join(kok,"paylasimlar","konu","%s.html"%k),"w",encoding="utf-8").write(
            '---\nlayout: konu\nkonu: %s\ntitle: "%s"\npermalink: /paylasimlar/konu/%s/\n---\n' % (k, ADLAR[k], k))
    return c

if __name__=='__main__':
    import os
    kok=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(uygula(kok))
