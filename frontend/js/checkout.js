(async () => {
  if (!(await requireUser())) return;
  const c = (await api('/api/cart')).d, items = c.items || [];
  if (!items.length) { $('#summary').innerHTML = '<p class="muted">Your cart is empty. <a href="products.html">Browse products</a></p>'; $('#place').hidden = true; return; }
  $('#summary').innerHTML = items.map(i => `<div class="line-item"><span class="li"><span class="mini">${thumb(i)}</span>${esc(i.name)} × ${i.qty}</span><span>${money(i.price * i.qty)}</span></div>`).join('')
    + `<div class="total"><span>Total</span><span>${money(c.total)}</span></div>`;
  $('#place').onclick = async () => {
    $('#place').disabled = true;
    const r = await api('/api/orders', 'POST');
    if (!r.ok) { $('#orderErr').textContent = r.d.error || 'Could not place order'; $('#place').disabled = false; return; }
    updateCount();
    orderSuccess(r.d, {onClose: () => location.href = 'orders.html?placed=' + r.d.id});
  };
})();
