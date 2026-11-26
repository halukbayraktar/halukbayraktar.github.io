(function(){
  const S=document.querySelector('.ani-defteri');if(!S)return;
  const OZET=S.dataset.mod==='ozet';
  const K={taziye:{url:'/ozdemir-bayraktar/ani-defteri/taziye.json',kaynak:'<a class="src" href="https://baykartech.com/tr/taziye-mesajlari/" target="_blank" rel="noopener">Kaynak: Baykar taziye defteri ↗</a>'},
           youtube:{url:'/ozdemir-bayraktar/ani-defteri/youtube.json',kaynak:'<a class="src" href="https://www.youtube.com/watch?v=pwqI5OOc5EA" target="_blank" rel="noopener">Kaynak: YouTube belgeseli ↗</a>'}};
  const KONU=[['h','Hatıralar'],['v','Vatan ve milli teknoloji'],['i','Örnek ve ilham'],['b','Belgesel üzerine'],['a','Aileye başsağlığı'],['w','Dünyadan mesajlar'],['d','Dua ve rahmet']];
  const $=q=>S.querySelector(q),L=$('.mesajlar'),ara=$('.ad-ara'),sira=$('.ad-sira'),daha=$('.ad-daha'),bilgi=$('.ad-bilgi'),konuK=$('.ad-konu');
  const veri={},ADIM=40;let k='taziye',konu='',goster=ADIM;
  const tr=s=>(s||'').toLocaleLowerCase('tr');
  const esc=s=>(s||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const gun=t=>(t||'').split(' ').slice(0,3).join(' ');
  const say=n=>n.toLocaleString('tr');
  async function yukle(x){if(!veri[x]){try{veri[x]=await (await fetch(K[x].url)).json()}catch(e){veri[x]=[]}const s=$('[data-say="'+x+'"]');if(s)s.textContent=say(veri[x].length);const t=document.querySelector('[data-toplam]');if(t&&veri.taziye&&veri.youtube)t.textContent=say(veri.taziye.length+veri.youtube.length)}return veri[x]}
  function konular(){if(!konuK)return;const a=veri[k]||[];
    konuK.innerHTML='<button type="button" data-c=""'+(konu?'':' class="on"')+'>Tümü <span>'+say(a.length)+'</span></button>'+KONU.map(([c,ad])=>{const n=a.filter(x=>(x.k||'').includes(c)).length;return n?'<button type="button" data-c="'+c+'"'+(konu===c?' class="on"':'')+'>'+ad+' <span>'+say(n)+'</span></button>':''}).join('');
    konuK.querySelectorAll('button').forEach(b=>b.onclick=()=>{konu=b.dataset.c;goster=ADIM;konular();ciz()})}
  function ciz(){
    let a=veri[k]||[];
    if(OZET){a=a.slice(-10).reverse()}else{
      const q=tr(ara.value.trim());
      if(konu)a=a.filter(x=>(x.k||'').includes(konu));
      if(q)a=a.filter(x=>tr(x.n).includes(q)||tr(x.m).includes(q));
      if(sira.value==='yeni')a=a.slice().reverse();
      bilgi.textContent=(q||konu)?say(a.length)+' mesaj':'';}
    let h='',onceki='';
    a.slice(0,OZET?10:goster).forEach(x=>{const g=k==='taziye'?gun(x.t):'';if(g&&g!==onceki){h+='<h3 class="gun">'+esc(g)+'</h3>';onceki=g}
      h+='<figure class="mesaj"><blockquote>'+esc(x.m).replace(/\n/g,'<br>')+'</blockquote><figcaption><b>'+esc(x.n)+'</b><time>'+esc(k==='taziye'?(x.t||'').split(' ').pop():x.t)+'</time></figcaption></figure>'});
    L.innerHTML=h||'<p class="ad-bos">Sonuç yok.</p>';if(daha)daha.hidden=OZET||a.length<=goster;
    $('.ad-kaynak').innerHTML=K[k].kaynak;
  }
  async function sec(x){k=x;konu='';goster=ADIM;S.querySelectorAll('.ad-sekme button').forEach(b=>b.classList.toggle('on',b.dataset.k===x));await yukle(x);konular();ciz()}
  S.querySelectorAll('.ad-sekme button').forEach(b=>b.onclick=()=>sec(b.dataset.k));
  if(!OZET){let z;ara.oninput=()=>{clearTimeout(z);z=setTimeout(()=>{goster=ADIM;ciz()},200)};sira.onchange=()=>{goster=ADIM;ciz()};daha.onclick=()=>{goster+=ADIM*2;ciz()}}
  sec('taziye');yukle('youtube');
})();
