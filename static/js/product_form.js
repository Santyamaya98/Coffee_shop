
function updateSubtotal(productId) {
    const quantity = document.getElementById(`quantity_${productId}`).value || 0;
    const price = parseFloat(document.getElementById(`price_${productId}`).textContent);
    const subtotal = (price * quantity).toFixed(2);
    document.getElementById(`subtotal_${productId}`).textContent = subtotal;

    updateTotalPrice();
}

function updateTotalPrice() {
    const productIds = [...document.querySelectorAll('input[name^="product_"]')]
        .map(input => input.id.split('_')[1]);

    let total = 0;
    productIds.forEach(id => {
        const quantity = document.getElementById(`quantity_${id}`).value || 0;
        const price = parseFloat(document.getElementById(`price_${id}`).textContent);
        total += price * quantity;
    });

    document.getElementById('total-price').textContent = total.toFixed(2);
}

// Initial update
document.querySelectorAll('input[name^="product_"]').forEach(input => {
    input.addEventListener('input', () => {
        const productId = input.id.split('_')[1];
        updateSubtotal(productId);
    });
});
