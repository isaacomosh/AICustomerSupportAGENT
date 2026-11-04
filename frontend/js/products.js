async function addToCart(id) {
  if (!(await getUser())) { location.href = 'login.html?next=' + encodeURIComponent(location.pathname.split('/').pop() + location.search); return; }
  const r = await api('/api/cart', 'POST', {product_id: id});
  if (r.ok) { toast('Added to cart'); updateCount(); } else toast(r.d.error || 'Could not add item');
}
const cardHtml = p => `<article class="card"><a class="tile" href="product.html?id=${p.id}" aria-hidden="true" tabindex="-1">${thumb(p)}</a>
  <div class="info"><h3>${esc(p.name)}</h3><p class="price">${money(p.price)}</p>
  <p class="stock ${p.stock ? '' : 'out'}"><i></i>${p.stock ? 'In stock' : 'Out of stock'}</p>
  <div class="foot"><a class="more" href="product.html?id=${p.id}">Details ${icon('arrow', 14)}</a>
  <button class="add" data-id="${p.id}" ${p.stock ? '' : 'disabled'}>${icon('cart', 14)} Add to cart</button></div></div></article>`;

if ($('#tabs')) {
  let cat = new URLSearchParams(location.search).get('category') || 'all', all = [];
  $('#tabs').innerHTML = CATS.map(([s, n]) => `<button class="chip" role="tab" data-s="${s}" aria-selected="${s === cat}">${n}</button>`).join('');
  const draw = () => {
    const q = ($('#search')?.value || '').toLowerCase();
    const list = all.filter(p => p.name.toLowerCase().includes(q));
    $('#grid').innerHTML = list.length ? list.map(cardHtml).join('') : '<p class="muted">No products found. Try another category.</p>';
  };
  const load = async () => { all = (await api('/api/products?category=' + cat)).d; if (!Array.isArray(all)) all = []; draw(); };
  $('#tabs').onclick = e => {
    const b = e.target.closest('button'); if (!b) return;
    cat = b.dataset.s;
    document.querySelectorAll('#tabs button').forEach(x => x.setAttribute('aria-selected', x === b));
    history.replaceState(null, '', cat === 'all' ? location.pathname : '?category=' + cat);
    markNav(cat); load();
  };
  $('#grid').onclick = e => { const b = e.target.closest('.add'); if (b) addToCart(+b.dataset.id); };
  $('#search')?.addEventListener('input', draw);
  load();
}
if ($('#detail')) (async () => {
  const id = new URLSearchParams(location.search).get('id');
  const r = await api('/api/products/' + encodeURIComponent(id));
  if (!r.ok) { $('#detail').innerHTML = '<p class="muted">Product not found. <a href="products.html">Back to products</a></p>'; return; }
  const p = r.d; document.title = p.name + ' · Electronic';
  $('#detail').innerHTML = `<div class="big">${p.image ? `<img src="${esc(p.image)}" alt="${esc(p.name)}">` : p.emoji}</div><div><h1>${esc(p.name)}</h1>
  <p class="price">${money(p.price)}</p><p>${esc(p.description)}</p>
  <p class="stock ${p.stock ? '' : 'out'}"><i></i>${p.stock ? p.stock + ' in stock' : 'Out of stock'}</p>
  <div class="actions"><button class="btn" id="add" ${p.stock ? '' : 'disabled'}>Add to cart</button>
  <a class="btn line" href="products.html?category=${esc(p.category)}">Back</a></div></div>`;
  $('#add').onclick = () => addToCart(p.id);
})();
