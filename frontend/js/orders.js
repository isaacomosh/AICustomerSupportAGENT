(async () => {
  if (!(await requireUser())) return;
  const placed = new URLSearchParams(location.search).get('placed');
  if (/^\d+$/.test(placed || '')) toast('Order #' + placed + ' placed');
  const r = await api('/api/orders');
  $('#orders').innerHTML = (r.ok && r.d.length) ? r.d.map(o => `<div class="order"><h3><span>Order #${o.id}</span><span>${esc(o.status)}</span></h3>
    ${o.items.map(i => `<div class="line-item"><span>${esc(i.name)} × ${i.qty}</span><span>${money(i.price * i.qty)}</span></div>`).join('')}
    <div class="total"><span>Total</span><span>${money(o.total)}</span></div></div>`).join('')
    : '<p class="muted">No orders yet. <a href="products.html">Browse products</a></p>';
})();
