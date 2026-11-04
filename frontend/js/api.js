const $ = (s, r = document) => r.querySelector(s);
const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const money = n => '$' + Number(n).toFixed(2);
async function api(url, method = 'GET', body) {
  try {
    const r = await fetch(url, {method, headers: {'Content-Type': 'application/json'}, body: body && JSON.stringify(body)});
    let d = {}; try { d = await r.json(); } catch {}
    return {ok: r.ok, status: r.status, d};
  } catch { return {ok: false, status: 0, d: {error: 'Connection lost. Try again.'}}; }
}
function toast(t) {
  let el = $('#toast');
  if (!el) { el = document.createElement('div'); el.id = 'toast'; el.setAttribute('role', 'status'); document.body.append(el); }
  el.textContent = t; el.classList.add('show');
  clearTimeout(toast.t); toast.t = setTimeout(() => el.classList.remove('show'), 2200);
}
let _u;
const getUser = () => _u || (_u = api('/api/auth/me').then(r => r.d.user || null));
const resetUser = () => { _u = null; };

const CATS = [['all','All'],['smart-watch','Smart Watch'],['vr-headsets','VR Headsets'],['controllers','Controllers']];
const ICONS = {
  x:'<path d="M18 6 6 18M6 6l12 12"/>',
  cart:'<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h3l2.7 12.4a1 1 0 0 0 1 .8h8.8a1 1 0 0 0 1-.8L20 8H6"/>',
  arrow:'<path d="M5 12h14M13 6l6 6-6 6"/>',
  clip:'<path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48"/>',
  send:'<path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/>',
  chat:'<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/><circle cx="8" cy="12" r=".9"/><circle cx="12" cy="12" r=".9"/><circle cx="16" cy="12" r=".9"/>'};
const icon = (n, size = 16) => `<svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICONS[n]}</svg>`;
const FACE = `<svg class="face" viewBox="139 130 258 271" aria-hidden="true"><path class="blob" d="M235.1,352.4C214.1,346.8 197.9,329.8 192.4,307.6C190.4,299.4 186.1,292.8 180.0,288.2C161.6,274.5 153.7,260.0 153.6,239.5C153.5,212.1 169.4,192.1 198.5,183.1C209.8,179.7 215.5,176.0 220.1,169.3C231.2,153.2 248.6,144.0 268.0,144.0C287.0,144.0 301.7,151.4 314.1,167.0C320.9,175.7 326.9,180.4 333.5,182.1C366.0,191.0 382.7,210.7 382.4,240.0C382.2,260.1 374.3,274.6 356.1,288.2C349.8,292.9 345.6,299.6 343.5,308.1C338.2,329.8 321.4,347.1 300.5,352.5C292.2,354.6 243.1,354.6 235.1,352.4z"/><g class="eyes"><rect class="eye l" x="230" y="220" width="19" height="58" rx="9.5"/><rect class="eye r" x="287" y="220" width="19" height="58" rx="9.5"/></g><g class="mouths" stroke-width="19"><line class="mouth m-idle" x1="239.5" y1="377.5" x2="296.5" y2="377.5"/><path class="mouth m-smile" d="M239.5,360.4 Q268.0,415.12 296.5,360.4"/><path class="mouth m-sad" d="M239.5,394.6 Q268.0,339.88 296.5,394.6"/><ellipse class="mouth m-o" cx="268.0" cy="377.5" rx="18.05" ry="21.849999999999998" stroke="none"/></g></svg>`;
const thumb = p => p.image ? `<img src="${esc(p.image)}" alt="" loading="lazy">` : (p.emoji || '');

/* Jetpack success pop. o = order {id,total}; L = optional labels + onClose callback. */
function orderSuccess(o, L = {}) {
  const calm = matchMedia('(prefers-reduced-motion:reduce)').matches;
  const ov = document.createElement('div');
  ov.className = 'ok-overlay'; ov.setAttribute('role', 'dialog'); ov.setAttribute('aria-modal', 'true'); ov.setAttribute('aria-label', L.title || 'Order placed');
  ov.innerHTML = `<div class="ok-wrap">
    <div class="jet fly"><i class="tank l"></i><i class="tank r"></i><div class="fl l"></div><div class="fl r"></div>
      ${[0, 1, 2, 3, 4, 5].map(i => `<b class="puff" style="--d:${i * .15}s;--x:${(i % 2 ? 1 : -1) * (6 + i * 4)}px"></b>`).join('')}
      <div class="head">${FACE.replace('class="face"', 'class="face" data-s="wow"')}</div></div>
    <div class="ok-card"><svg class="tick" viewBox="0 0 52 52" aria-hidden="true"><circle cx="26" cy="26" r="25"/><path d="M15 27l8 8 14-16"/></svg>
      <h2>${esc(L.title || 'Order placed!')}</h2><p class="ok-sub">${esc(L.sub || 'Order #' + o.id)}</p><p class="ok-sum">${money(o.total)}</p>
      <div class="ok-btns"><a class="btn" href="orders.html">${esc(L.view || 'View orders')}</a><button class="btn line" data-close>${esc(L.keep || 'Keep shopping')}</button></div></div></div>`;
  if (!calm) {
    const colors = ['#2563eb', '#22c55e', '#f59e0b', '#ec4899', '#06b6d4'], r = (a, b) => a + Math.random() * (b - a);
    for (let i = 0; i < 36; i++) {
      const c = document.createElement('i'); c.className = 'cf';
      c.style.cssText = `--x:${r(-170, 170)}px;--y:${r(160, 420)}px;--r:${r(-540, 540)}deg;--c:${colors[i % 5]};--d:${r(0, .3)}s`;
      ov.append(c);
    }
  }
  const jet = $('.jet', ov), face = $('.face', ov), done = $('[data-close]', ov);
  const close = () => { document.removeEventListener('keydown', onKey); ov.remove(); if (L.onClose) L.onClose(); };
  const onKey = e => { if (e.key === 'Escape') close(); };
  done.onclick = close; ov.onclick = e => { if (e.target === ov) close(); };
  document.addEventListener('keydown', onKey);
  document.body.append(ov);
  setTimeout(() => { jet.classList.remove('fly'); face.dataset.s = 'happy'; }, calm ? 0 : 1300);   // engines throttle down, agent smiles
  setTimeout(() => done.focus(), calm ? 50 : 1700);
}
