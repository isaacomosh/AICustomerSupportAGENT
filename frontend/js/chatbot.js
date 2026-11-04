(() => {
  // UI strings. Swahili is filled in; add reviewed Dholuo (luo) / Gĩkũyũ (ki) strings and they are used automatically.
  const I18N = {
    en: {hi: 'Hi! Ask me about products, delivery, payments or returns. I can also place an order for you.', ph: 'Type your question...',
         confirm: 'Confirm order', cancel: 'Cancel', total: 'Total', placed: 'Order #{id} placed', cancelled: 'Order cancelled', login: 'Log in to order',
         instock: 'In stock', outstock: 'Out of stock', viewp: 'View Product', title: 'Order placed!', view: 'View orders', keep: 'Keep shopping', no: 'Order'},
    sw: {hi: 'Habari! Uliza kuhusu bidhaa, uwasilishaji, malipo au marejesho. Naweza pia kukuwekea oda.', ph: 'Andika swali lako...',
         confirm: 'Thibitisha oda', cancel: 'Ghairi', total: 'Jumla', placed: 'Oda #{id} imewekwa', cancelled: 'Oda imeghairiwa', login: 'Ingia ili kuagiza',
         instock: 'Ipo dukani', outstock: 'Haipo dukani', viewp: 'Tazama Bidhaa', title: 'Oda imewekwa!', view: 'Tazama oda zako', keep: 'Endelea kununua', no: 'Oda'},
    luo: {}, ki: {}
  };
  const LANGS = [['en', 'English'], ['sw', 'Kiswahili'], ['luo', 'Dholuo'], ['ki', 'Gĩkũyũ']];
  let lang = 'en'; try { lang = localStorage.getItem('lang') || 'en'; } catch {}
  if (!I18N[lang]) lang = 'en';
  const t = k => (I18N[lang] || {})[k] || I18N.en[k];

  const isPage = document.body.dataset.page === 'chat';
  const panel = document.createElement('aside');
  panel.id = 'chat'; panel.setAttribute('role', isPage ? 'region' : 'dialog'); panel.setAttribute('aria-label', 'AI Assistant chat');
  panel.innerHTML = `<div class="chead"><span class="av big">${FACE}</span><div><strong>AI Assistant</strong><span class="s">Your shopping assistant</span></div>
  <span class="online"><i></i>Online</span><button type="button" class="x" aria-label="Close chat">${icon('x', 18)}</button></div>
  <div class="lbar"><label for="lang">Language</label><select id="lang">${LANGS.map(([c, n]) => `<option value="${c}">${n}</option>`).join('')}</select></div>
  <div id="log"></div>
  <form id="f"><span class="clip">${icon('clip', 20)}</span><input id="q" autocomplete="off" aria-label="Message">
  <button class="send" aria-label="Send">${icon('send', 18)}</button></form>`;
  const log = $('#log', panel), q = $('#q', panel), sel = $('#lang', panel), face = $('.av.big .face', panel);

  // the agent's reactions: idle | listen | think | happy | wow | oops
  let ft;
  const mood = (s, ms) => { clearTimeout(ft); face.dataset.s = s; if (ms) ft = setTimeout(() => face.dataset.s = 'idle', ms); };

  const md = s => esc(s).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>').replace(/^\s*[*-]\s+/gm, '• ');   // safe mini-markdown
  const clock = () => new Date().toLocaleTimeString([], {hour: 'numeric', minute: '2-digit'});
  // bot rows wrap their content in .col (bubble, time, cards) next to the avatar; user rows hold bubble + time directly
  const row = (who, inner) => {
    const r = document.createElement('div'); r.className = 'row ' + who;
    r.innerHTML = who === 'b' ? `<span class="av">${FACE}</span><div class="col">${inner}</div>` : inner;
    log.append(r); r.scrollIntoView(); return r;
  };
  const add = (text, who) => {
    const r = row(who, `<div class="m"></div><time>${clock()}</time>`), m = $('.m', r);
    if (who === 'u') m.textContent = text; else m.innerHTML = md(text);
    return m;
  };
  const productCard = p => `<a class="pc" href="product.html?id=${p.id}"><span class="pt">${thumb(p)}</span>
    <span class="pi"><strong>${esc(p.name)}</strong><span class="pp">${money(p.price)}</span>
    <span class="pstock ${p.stock ? '' : 'out'}"><i></i>${p.stock ? `${t('instock')} (${p.stock})` : t('outstock')}</span>
    <span class="pv">${t('viewp')} ${icon('arrow', 14)}</span></span></a>`;

  function orderCard(a) {
    const r = row('b', `<div class="m ocard"><ul>${a.items.map(i => `<li><span class="mini">${thumb(i)}</span>
      <span class="nm">${esc(i.name)}<small>${i.qty} × ${money(i.price)}</small></span><strong>${money(i.price * i.qty)}</strong></li>`).join('')}</ul>
      <p class="tot"><span>${t('total')}</span><span>${money(a.total)}</span></p>
      <div class="obtns"><button class="btn" data-ok>${t('confirm')}</button><button class="btn line" data-no>${t('cancel')}</button></div></div>`);
    const card = r.querySelector('.ocard');
    const done = msg => { card.querySelector('.obtns').remove(); card.append(Object.assign(document.createElement('p'), {textContent: msg, className: 'tot'})); };
    card.querySelector('[data-ok]').onclick = async () => {
      mood('think');
      const res = await api('/api/chat/confirm-order', 'POST');
      if (res.ok) {
        const m = t('placed').replace('{id}', res.d.id); done(m); updateCount(); mood('happy', 3500);
        orderSuccess(res.d, {title: t('title'), sub: `${t('no')} #${res.d.id}`, view: t('view'), keep: t('keep')});
      } else { done(res.d.error || 'Could not place order'); mood('oops', 2200); }
    };
    card.querySelector('[data-no]').onclick = async () => { await api('/api/chat/cancel-order', 'POST'); done(t('cancelled')); mood('idle'); };
  }
  function setLang(l, greet) {
    lang = l; sel.value = l; q.placeholder = t('ph');
    try { localStorage.setItem('lang', l); } catch {}
    if (greet) add(t('hi'), 'b');
  }
  sel.onchange = () => setLang(sel.value, true);

  if (isPage) { panel.classList.add('page', 'open'); $('#chatPage').append(panel); }
  else {
    const backdrop = document.createElement('div'); backdrop.id = 'backdrop';
    const fab = document.createElement('button');
    fab.className = 'fab'; fab.setAttribute('aria-label', 'Chat with us'); fab.setAttribute('aria-expanded', 'false');
    fab.innerHTML = FACE + '<span class="lbl">Chat with us</span>';
    const toggle = o => {
      panel.classList.toggle('open', o); backdrop.classList.toggle('show', o); fab.classList.toggle('open', o); fab.setAttribute('aria-expanded', o);
      if (o) { q.focus(); mood('wow', 700); }
    };
    fab.onclick = () => toggle(!panel.classList.contains('open'));
    backdrop.onclick = () => toggle(false);
    $('.x', panel).onclick = () => toggle(false);
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && panel.classList.contains('open')) toggle(false); });
    document.body.append(backdrop, panel, fab);
  }
  setLang(lang, true);

  q.addEventListener('input', () => mood(q.value ? 'listen' : 'idle'));
  q.addEventListener('blur', () => { if (face.dataset.s === 'listen') mood('idle'); });
  $('#f', panel).onsubmit = async e => {
    e.preventDefault(); const text = q.value.trim(); if (!text) return;
    q.value = ''; add(text, 'u'); const w = add('…', 'b'); mood('think');
    const r = await api('/api/chat', 'POST', {message: text, lang});
    w.innerHTML = md(r.d.reply || r.d.error || 'Something went wrong. Try again.');
    mood(r.ok ? 'happy' : 'oops', 2000);
    const a = r.d.action;
    if (!a && r.d.products && r.d.products.length) {   // product cards under the answer
      const wrap = document.createElement('div'); wrap.className = 'pcards';
      wrap.innerHTML = r.d.products.map(productCard).join(''); w.closest('.col').append(wrap); wrap.scrollIntoView({block: 'nearest'});
    }
    if (a && a.type === 'confirm_order') orderCard(a);
    if (a && a.type === 'login') row('b', `<a class="btn" href="login.html?next=${encodeURIComponent(location.pathname.split('/').pop() || 'index.html')}">${t('login')}</a>`);
  };
})();
