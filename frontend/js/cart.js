(async () => {
  if (!(await requireUser())) return;
  const draw = c => {
    const items = c.items || [];
    $('#cart').innerHTML = items.length
      ? items.map(i => `<div class="line-item"><span class="li"><span class="mini">${thumb(i)}</span>${esc(i.name)} × ${i.qty}</span>
        <span>${money(i.price * i.qty)} <button class="rm" data-id="${i.product_id}">Remove</button></span></div>`).join('')
        + `<div class="total"><span>Total</span><span>${money(c.total)}</span></div>
        <div class="actions"><a class="btn" href="checkout.html">Checkout</a><a class="btn line" href="products.html">Keep shopping</a></div>`
      : '<p class="muted">Your cart is empty. <a href="products.html">Browse products</a></p>';
    updateCount();
  };
  draw((await api('/api/cart')).d);
  $('#cart').onclick = async e => {
    const b = e.target.closest('.rm'); if (!b) return;
    draw((await api('/api/cart/' + b.dataset.id, 'DELETE')).d);
  };
})();
