(function(){
  var d=document.querySelector('.vdlg');
  if(d&&d.showModal){
    var vi=d.querySelector('video'),p=d.querySelector('p');
    document.addEventListener('click',function(e){
      var a=e.target.closest('a.vid[data-mp4]');if(!a)return;
      e.preventDefault();vi.src=a.dataset.mp4;vi.poster=a.dataset.poster;
      p.textContent=a.querySelector('b').textContent;d.showModal();vi.play().catch(function(){});
    });
    function kapat(){vi.pause();vi.removeAttribute('src');vi.load();d.close();}
    d.querySelector('.kapat').addEventListener('click',kapat);
    d.addEventListener('click',function(e){if(e.target===d)kapat();});
    d.addEventListener('cancel',function(){vi.pause();vi.removeAttribute('src');vi.load();});
  }
  var k=document.querySelector('.vkonu');if(!k)return;
  k.addEventListener('click',function(e){
    var b=e.target.closest('button');if(!b)return;
    k.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x===b);});
    var s=b.dataset.k;
    document.querySelectorAll('#gorsel a.vid').forEach(function(a){
      a.hidden=!!s&&(' '+a.dataset.konu+' ').indexOf(' '+s+' ')<0;
    });
  });
})();
