
(function(){
  var ENDPOINT = "https://services.leadconnectorhq.com/hooks/eRpXDjkyyScY5hEr424s/webhook-trigger/RkJTfvGE7v99bZynCdAE";
  var burger = document.querySelector('.burger');
  var drawer = document.getElementById('mdrawer');
  if (burger && drawer) burger.addEventListener('click', function(){
    var open = drawer.hidden;
    drawer.hidden = !open;
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  function showStep(form, n){
    form.querySelectorAll('fieldset.step').forEach(function(fs){
      fs.hidden = fs.getAttribute('data-step') !== String(n);
    });
    form.setAttribute('data-step-active', String(n));
    var meta = form.parentElement.querySelector('.step-meta b');
    if (meta) meta.textContent = String(n);
  }
  document.querySelectorAll('form.lead').forEach(function(form){
    showStep(form, 1);
    form.addEventListener('click', function(ev){
      var btn = ev.target.closest('[data-step-go]');
      if (!btn) return;
      var cur = Number(form.getAttribute('data-step-active') || '1');
      if (btn.getAttribute('data-step-go') === 'back') { showStep(form, Math.max(1, cur-1)); return; }
      var fs = form.querySelector('fieldset.step[data-step="'+cur+'"]');
      var bad = false;
      fs.querySelectorAll('input[required]').forEach(function(inp){
        if (inp.type === 'radio') {
          var any = form.querySelector('input[name="'+inp.name+'"]:checked');
          if (!any) { bad = true; inp.reportValidity && inp.reportValidity(); }
        } else if (!inp.checkValidity()) { bad = true; inp.reportValidity(); }
      });
      if (bad) return;
      showStep(form, Math.min(3, cur+1));
    });
    form.addEventListener('submit', function(ev){
      ev.preventDefault();
      if (form.querySelector('[name=website]').value) return;
      var consent = form.querySelector('[name=consent]');
      if (consent && !consent.checked) { consent.focus(); return; }
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var data = {brand:'CCT', source_page: location.pathname, language:'es',
        consent_ts: new Date().toISOString(), page_url: location.href.split('#')[0],
        page_title: document.title, referrer: document.referrer || ''};
      var vals = {};
      new FormData(form).forEach(function(v,k){
        if (k === 'website') return;
        (vals[k] = vals[k] || []).push(v);
      });
      Object.keys(vals).forEach(function(k){ data[k] = vals[k].filter(Boolean).join(', '); });
      var parts = String(data.name||'').trim().split(/\s+/);
      data.first_name = parts[0] || '';
      data.last_name = parts.slice(1).join(' ');
      data.lead_note = ['Compramos Casas TX lead (seller)',
        'CONSENT: '+(data.consent==='on'?'consent box checked, '+data.consent_ts:'not checked'),
        'Name: '+(data.name||''), 'Phone: '+(data.phone||''), 'Email: '+(data.email||''),
        'Property: '+(data.address||''), 'Listed: '+(data.listed_with_realtor||''),
        'Situation: '+(data.situation||''), 'Timeline: '+(data.timeline||''),
        'Page: '+data.page_url].join('\n');
      var btn = form.querySelector('[type=submit]');
      if (btn) btn.disabled = true;
      fetch(ENDPOINT, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(data)})
        .then(function(r){
          if (!r.ok) throw new Error('bad');
          var to = data.listed_with_realtor === 'yes' ? '/gracias-listada' : '/gracias';
          location.href = to;
        })
        .catch(function(){
          if (btn) btn.disabled = false;
          form.classList.add('hide');
          var p = form.parentElement.querySelector('.panel.err');
          if (p) p.classList.remove('hide');
        });
    });
  });
})();
