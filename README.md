# halukbayraktar.github.io

Haluk Bayraktar'ın kişisel sitesi. Jekyll + GitHub Pages.

- Ana sayfa: `index.html`, tasarım `assets/site.css`, şablon `_layouts/default.html`
- Paylaşımlar: `_data/tweets.json` (X arşivinden) + `_data/yazilar.yml` (makale, röportaj; elle eklenir)
- Görevler: `_data/gorevler.yml`
- `/kamara/` ayrı bir sayfadır, bu yapıdan bağımsızdır.

## X arşivini güncellemek

1. X'ten yeni arşivi indir ve aç.
2. Görselleri 800px JPEG olarak `paylasimlar/img/<tweetid>-<ad>.jpg` adıyla koy.
3. `python3 tools/twitter_ice_aktar.py <arşiv>/data`

## Aylık yeni tweet'ler

Her ay Chrome'da x.com/haluk açılır, yeni paylaşımlar toplanıp
`python3 tools/yeni_tweetler_ekle.py yeni.json` ile eklenir. Yeni görseller X'in sunucusundan gösterilir.

## İletişim formu

Bana Ulaşın formu Web3Forms ile çalışır (`iletisim/index.html`, `access_key` alanı). Anahtar herkese açık olacak şekilde tasarlanmıştır; mesajlar hesaba bağlı e-postaya gider.
