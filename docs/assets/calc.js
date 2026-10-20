(function(){
  // Seller calculators (calc.py). ES5 only: this file must parse in old engines.
  function clean(v){return String(v==null?'':v).replace(/[$,\s]/g,'');}
  // junk ('abc', '1e400') counts as 0, and has() is true only for a finite number, so '.', '-', 'abc' and '1e400' still wait
  function num(v){var n=parseFloat(clean(v));return isFinite(n)?n:0;}
  function has(v){return isFinite(parseFloat(clean(v)));}
  // whole dollars with commas, never exponent text: 1e15 and up shows as 999,999,999,999,999
  function grp(n){
    var a=Math.round(Math.abs(n)),s=String(a>=1e15?999999999999999:(a||0)),o='';
    while(s.length>3){o=','+s.slice(-3)+o;s=s.slice(0,-3);}
    return s+o;
  }
  // the sign goes on only when the rounded amount is not 0: no '-$0'
  function money(n){var a=Math.round(Math.abs(n));return (n<0&&a>0?'-$':'$')+grp(a);}
  // a %/$ field: v[k] in the unit v[k+'_u'] ('pct' or 'usd', else def), as dollars of the sale price
  function amt(v,k,price,def){return (v[k+'_u']||def)==='pct'?price*num(v[k])/100:num(v[k]);}
  // the same amount in the other unit: '' when there is nothing to derive it from
  function conv(val,to,price){
    if(!has(val)||!(price>0))return '';
    var n=num(val),d;
    if(to==='usd'){d=price*n/100;return (d<0&&Math.round(-d)>0?'-':'')+grp(d);}
    // 4 decimals: a round trip keeps the seller's dollar figure (1,966 of 340,000 is 0.5782%, back to 1,966)
    // the box never gets exponent text: like grp(), 1e15 and up clamps to 999999999999999 and keeps its sign
    var p=Math.round(n/price*1e6)/1e4;
    return String(Math.abs(p)>=1e15?(p<0?-999999999999999:999999999999999):p);
  }
  function net(v){
    var price=num(v.price),held=num(v.monthly),owed=num(v.payoff)+num(v.taxes_due);
    var L={price:price,commission:amt(v,'list_pct',price,'pct')+amt(v,'buyer_pct',price,'pct'),concessions:num(v.concessions),
           repairs:num(v.repairs),closing:amt(v,'closing',price,'usd'),holding:num(v.list_months)*held,owed:owed};
    L.net=L.price-L.commission-L.concessions-L.repairs-L.closing-L.holding-owed;
    var C={price:num(v.cash),holding:num(v.cash_months)*held,owed:owed};
    C.net=C.price-C.holding-owed;
    return {list:L,cash:C,diff:L.net-C.net,listReady:has(v.price),ready:has(v.price)&&has(v.cash)};
  }
  function hold(v){
    var m=num(v.loan)+num(v.tax_year)/12+num(v.ins_year)/12+num(v.utilities)+num(v.upkeep)+num(v.hoa)+num(v.other),
        mo=Math.max(0,num(v.months));
    return {monthly:m,total:m*mo,ready:m>0,hasMonths:mo>0};
  }
  function vals(box){
    var o={},els=box.querySelectorAll('[data-k]'),i,k,u;
    for(i=0;i<els.length;i++){
      k=els[i].getAttribute('data-k');o[k]=els[i].value;
      u=els[i].getAttribute('data-u');if(u)o[k+'_u']=u;
    }
    return o;
  }
  // every match: the verdict has one diff slot per case, and the phone result bar repeats the card's head
  function txt(box,k,s){var els=box.querySelectorAll('[data-out="'+k+'"]'),i;for(i=0;i<els.length;i++)els[i].textContent=s;}
  function put(box,k,n){txt(box,k,money(n));}
  function show(box,sel,on){
    var els=box.querySelectorAll(sel),i;
    for(i=0;i<els.length;i++){if(on)els[i].removeAttribute('hidden');else els[i].setAttribute('hidden','');}
  }
  function head(box,state){show(box,'[data-head]',false);show(box,'[data-head="'+state+'"]',true);}
  function up(el,cls){
    while(el&&el.nodeType===1){if((' '+el.className+' ').indexOf(' '+cls+' ')>-1)return el;el=el.parentNode;}
    return null;
  }
  function run(box){
    var v=vals(box),r,a,d;
    if(box.getAttribute('data-calc')==='net'){
      r=net(v);
      // the verdict reads the difference in whole dollars, as shown: under $0.50 either way is 'same', never 'by $0'
      a=Math.round(Math.abs(r.diff));d=!a?0:r.diff<0?-a:a;
      show(box,'.calc-res',r.listReady);show(box,'.c',r.ready);show(box,'.calc-add',r.listReady&&!r.ready);
      show(box,'[data-case="list"]',r.ready&&d>0);show(box,'[data-case="cash"]',r.ready&&d<0);
      show(box,'[data-case="same"]',r.ready&&d===0);
      if(!r.listReady){head(box,'wait');txt(box,'head','');return;}
      head(box,!r.ready?'list':d>0?'list-more':d<0?'cash-more':'same');
      put(box,'head',r.ready?a:r.list.net);
      put(box,'l_price',r.list.price);put(box,'l_commission',-r.list.commission);put(box,'l_concessions',-r.list.concessions);
      put(box,'l_repairs',-r.list.repairs);put(box,'l_closing',-r.list.closing);put(box,'l_holding',-r.list.holding);
      put(box,'l_owed',-r.list.owed);put(box,'l_net',r.list.net);
      put(box,'c_price',r.cash.price);put(box,'c_holding',-r.cash.holding);put(box,'c_owed',-r.cash.owed);put(box,'c_net',r.cash.net);
      put(box,'diff',a);
    }else{
      r=hold(v);
      show(box,'.calc-res',r.ready);show(box,'.tot',r.hasMonths);   // no 'total $0' before months are typed
      if(!r.ready){head(box,'wait');txt(box,'head','');return;}
      head(box,r.hasMonths?'total':'month');
      put(box,'head',r.hasMonths?r.total:r.monthly);put(box,'monthly',r.monthly);put(box,'total',r.total);
    }
  }
  function addc(el,cls){if(el&&(' '+el.className+' ').indexOf(' '+cls+' ')<0)el.className+=(el.className?' ':'')+cls;}
  // the seller's own figure: the Example chip hides (CSS .fld.mine .ex), so its input stops naming it (ex-{k});
  // aria-describedby would still read the hidden chip
  function mine(f){
    var inp=f&&f.querySelector('[data-k]'),d;
    if(!inp)return;
    addc(f,'mine');
    d=(' '+(inp.getAttribute('aria-describedby')||'')+' ').replace(' ex-'+inp.getAttribute('data-k')+' ',' ').replace(/^\s+|\s+$/g,'');
    if(d)inp.setAttribute('aria-describedby',d);else inp.removeAttribute('aria-describedby');
  }
  // %/$ toggle: one stored value, in the unit shown; switching converts it with the current sale price
  function unit(box,btn){
    var g=up(btn,'unit'),f=up(btn,'fld'),inp=f&&f.querySelector('[data-k]'),to=btn.getAttribute('data-unit'),bs,i,p,price,nv;
    if(!g||!inp||inp.getAttribute('data-u')===to)return;
    p=box.querySelector('[data-k="price"]');price=p?num(p.value):0;
    // no sale price to convert with: a number keeps its unit (2.73 read as $2.73 would overstate the net)
    if(has(inp.value)&&!(price>0))return;
    nv=conv(inp.value,to,price);
    if(nv!==inp.value){
      inp.value=nv;
      if(inp.getAttribute('data-example')!==null)mine(f);   // a converted example is the seller's figure now
    }
    inp.setAttribute('data-u',to);
    bs=g.querySelectorAll('[data-unit]');
    for(i=0;i<bs.length;i++)bs[i].setAttribute('aria-pressed',bs[i]===btn?'true':'false');
    run(box);
  }
  // reduced motion: jump instead of glide (calc.js's own copy; it does not rely on site.js)
  function smoothOk(){try{return !(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches);}catch(e){return true;}}
  function wire(b){
    var bar=b.querySelector('.calc-bar');
    b.addEventListener('input',function(e){
      var t=e.target,f=t&&t.getAttribute&&t.getAttribute('data-example')!==null?up(t,'fld'):null;
      mine(f);
      run(b);
    });
    b.addEventListener('change',function(){run(b);});
    b.addEventListener('click',function(e){
      var t=e.target,btn=null,out;
      while(t&&t.nodeType===1&&t!==b){if(t.getAttribute('data-unit')){btn=t;break;}t=t.parentNode;}
      if(btn){unit(b,btn);return;}
      if(up(e.target,'calc-bar')){
        out=b.querySelector('.calc-out');
        if(out){
          out.focus({preventScroll:true});
          if(out.scrollIntoView)out.scrollIntoView({behavior:smoothOk()?'smooth':'auto',block:'start'});
        }
      }
    });
    // calc-on: the page end clears the result bar (body), and keyboard focus scrolls clear of it (html scroll-padding)
    if(bar){bar.removeAttribute('hidden');addc(document.body,'calc-on');addc(document.documentElement,'calc-on');}
    run(b);
  }
  window.CHA_CALC={net:net,hold:hold,money:money,num:num,conv:conv};
  var boxes=document.querySelectorAll?document.querySelectorAll('[data-calc]'):[],i;
  for(i=0;i<boxes.length;i++)wire(boxes[i]);
})();
