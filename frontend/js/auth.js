async function updateCount() {
  let n = '';
  if (await getUser()) { const r = await api('/api/cart'); if (r.ok) n = r.d.items.reduce((t, i) => t + i.qty, 0) || ''; }
  document.querySelectorAll('.badge').forEach(el => el.textContent = n);
}
async function requireUser() {
  const u = await getUser();
  if (!u) location.href = 'login.html?next=' + encodeURIComponent(location.pathname.split('/').pop() + location.search);
  return u;
}
function markNav(cat) { document.querySelectorAll('.cats a').forEach(a => a.classList.toggle('on', a.dataset.s === cat)); }
async function initHeader() {
  const h = $('#site-header'); if (!h) return;
  const u = await getUser();
  const file = location.pathname.split('/').pop(), listing = ['', 'index.html', 'products.html'].includes(file);
  const cat = new URLSearchParams(location.search).get('category') || 'all';
  h.innerHTML = `<a class="brand" href="index.html">Electronic</a>
  <nav class="cats" aria-label="Categories">${CATS.map(([s, n]) => `<a data-s="${s}" href="products.html${s === 'all' ? '' : '?category=' + s}">${n}</a>`).join('')}</nav>
  <nav class="right"><a href="products.html">Products</a><a href="cart.html">Cart ${icon('cart')}<span class="badge"></span></a>
  <a href="orders.html">Orders</a><a href="chat.html">Help</a>
  ${u ? `<button id="logout">Log out (${esc(u.name)})</button>` : '<a class="login" href="login.html">Log In</a>'}</nav>`;
  if (listing) markNav(cat);
  document.querySelectorAll('.cartchip').forEach(c => c.innerHTML = icon('cart', 22) + '<span class="badge"></span>');
  const lo = $('#logout');
  if (lo) lo.onclick = async () => { await api('/api/auth/logout', 'POST'); resetUser(); location.href = 'index.html'; };
  updateCount();
}
const authForm = $('#authForm');
if (authForm) authForm.onsubmit = async e => {
  e.preventDefault();
  const mode = authForm.dataset.mode;
  const body = {email: $('#email').value, password: $('#password').value};
  if (mode === 'register') body.name = $('#name').value;
  const r = await api('/api/auth/' + mode, 'POST', body);
  if (!r.ok) { $('#authErr').textContent = r.d.error || 'Something went wrong'; return; }
  resetUser();
  const next = new URLSearchParams(location.search).get('next');
  location.href = /^[\w.-]+\.html(\?[\w=&.-]*)?$/.test(next || '') ? next : 'index.html';
};
initHeader();
