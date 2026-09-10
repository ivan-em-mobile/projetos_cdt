let cart = [];

// Carregar menu quando a página carrega
document.addEventListener('DOMContentLoaded', function() {
    loadMenu();
    updateCart();

    const modal = document.getElementById('cart-modal');
    if (modal) {
        modal.addEventListener('click', function(event) {
            if (event.target === this) {
                toggleCart();
            }
        });
    }
});

// Carregar menu da API
function loadMenu() {
    const menuContainer = document.getElementById('menu-items');
    if (!menuContainer) return;

    fetch('/api/menu')
        .then(response => response.json())
        .then(data => {
            menuContainer.innerHTML = '';
            data.forEach(item => {
                const menuItem = document.createElement('div');
                menuItem.className = 'menu-item';
                menuItem.innerHTML = `
                    <img src="${item.image}" alt="${item.name}" class="menu-item-image" onerror="this.src='https://via.placeholder.com/400x300?text=${encodeURIComponent(item.name)}'">
                    <div class="menu-item-content">
                        <div class="menu-item-name">${item.name}</div>
                        <div class="menu-item-description">${item.description}</div>
                        <div class="menu-item-footer">
                            <div class="menu-item-price">R$ ${item.price.toFixed(2)}</div>
                            <button class="menu-item-btn" onclick="addToCart(${item.id}, '${item.name}', ${item.price})">+</button>
                        </div>
                    </div>
                `;
                menuContainer.appendChild(menuItem);
            });
        })
        .catch(error => {
            console.error('Erro ao carregar menu:', error);
            menuContainer.innerHTML = '<p>Erro ao carregar o cardápio</p>';
        });
}

// Adicionar ao carrinho
function addToCart(itemId, itemName, itemPrice) {
    const cartItem = cart.find(i => i.id === itemId);

    if (cartItem) {
        cartItem.quantity++;
    } else {
        cart.push({
            id: itemId,
            name: itemName,
            price: itemPrice,
            quantity: 1
        });
    }

    updateCart();
}

// Remover do carrinho
function removeFromCart(itemId) {
    cart = cart.filter(i => i.id !== itemId);
    updateCart();
}

// Atualizar carrinho
function updateCart() {
    const cartCount = document.getElementById('cart-count');
    const cartItemsList = document.getElementById('cart-items-list');
    const totalAmount = document.getElementById('total-amount');
    const checkoutBtn = document.getElementById('checkout-btn');

    if (!cartCount) return;

    // Contar itens
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.textContent = totalItems;

    // Renderizar itens
    if (cart.length === 0) {
        cartItemsList.innerHTML = '<p class="empty-message">Seu carrinho está vazio</p>';
        if (checkoutBtn) checkoutBtn.style.display = 'none';
    } else {
        cartItemsList.innerHTML = cart.map(item => `
            <div class="cart-item">
                <div class="cart-item-info">
                    <div class="cart-item-name">${item.name}</div>
                    <div class="cart-item-qty">Quantidade: ${item.quantity}</div>
                </div>
                <div class="cart-item-price">R$ ${(item.price * item.quantity).toFixed(2)}</div>
                <button class="cart-item-remove" onclick="removeFromCart(${item.id})">✕</button>
            </div>
        `).join('');
        if (checkoutBtn) checkoutBtn.style.display = 'block';
    }

    // Calcular total
    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    if (totalAmount) totalAmount.textContent = total.toFixed(2);
}

// Alternar carrinho
function toggleCart() {
    const modal = document.getElementById('cart-modal');
    if (modal) {
        modal.classList.toggle('show');
    }
}

// Finalizar pedido
function checkout() {
    if (cart.length === 0) {
        alert('Seu carrinho está vazio!');
        return;
    }

    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    const itemsList = cart.map(item => `${item.name} (x${item.quantity})`).join(', ');

    fetch('/api/checkout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            items: cart,
            total: total
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`✅ Pedido realizado com sucesso!\n\nItens: ${itemsList}\nTotal: R$ ${total.toFixed(2)}\n\nNúmero do pedido: ${data.order_id}`);
            cart = [];
            updateCart();
            toggleCart();
        } else {
            alert('Erro ao processar o pedido. Tente novamente.');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao conectar com o servidor.');
    });
}
