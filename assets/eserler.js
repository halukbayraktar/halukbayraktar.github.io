document.querySelectorAll('.eser').forEach(b=>b.addEventListener('click',()=>document.getElementById('eser-'+b.dataset.i).showModal()));
document.querySelectorAll('.eser-detay').forEach(d=>{d.querySelector('.kapat').onclick=()=>d.close();d.addEventListener('click',e=>{if(e.target===d)d.close()})});
document.querySelectorAll('.eser-filtre button').forEach(b=>b.onclick=()=>{document.querySelectorAll('.eser-filtre button').forEach(x=>x.classList.toggle('on',x===b));const t=b.dataset.tur;document.querySelectorAll('.eser-grid .eser').forEach(c=>c.hidden=!!t&&c.dataset.tur!==t)});
