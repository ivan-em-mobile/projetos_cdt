// 🛒 Estado global da aplicação
let cart = [];

// 🚀 Inicialização do sistema consoante a página atual
document.addEventListener('DOMContentLoaded', function() {
    // Inicializa funções da página do cardápio se os elementos existirem
    if (document.getElementById('menu-items')) {
        loadMenu();
        updateCart();
    }

    // Inicializa funções da página admin se a tabela existir
    if (document.getElementById('admin-orders-list')) {
        loadAdminOrders();
    }

    // Configura o fecho do modal do carrinho ao clicar fora dele
    const modal = document.getElementById('cart-modal');
    if (modal) {
        modal.addEventListener('click', function(event) {
            if (event.target === this) {
                toggleCart();
            }
        });
    }
});

/**
 * 1. CARREGAR O CARDÁPIO COMPLETO DA API (Página do Cliente)
 */
function loadMenu() {
    const menuContainer = document.getElementById('menu-items');
    if (!menuContainer) return;

    fetch('/api/menu')
        .then(response => response.json())
        .then(data => {
            // Limpa o container para evitar duplicações ou loops
            menuContainer.innerHTML = '';
            
            data.forEach(item => {
                const menuItem = document.createElement('div');
                menuItem.className = 'menu-item';
                menuItem.innerHTML = `
                    <img src="${item.image}" alt="${item.name}" class="menu-item-image" onerror="this.src='https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400'">
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

/**
 * 2. ADICIONAR AO CARRINHO
 */
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

/**
 * 3. REMOVER DO CARRINHO
 */
function removeFromCart(itemId) {
    cart = cart.filter(i => i.id !== itemId);
    updateCart();
}

/**
 * 4. ATUALIZAR INTERFACE DO CARRINHO
 */
function updateCart() {
    const cartCount = document.getElementById('cart-count');
    const cartItemsList = document.getElementById('cart-items-list');
    const totalAmount = document.getElementById('total-amount');
    const checkoutBtn = document.getElementById('checkout-btn');

    if (!cartCount) return;

    // Atualiza a bolha de contagem do carrinho flutuante
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.textContent = totalItems;

    // Renderiza a lista de itens dentro do modal
    if (cart.length === 0) {
        if (cartItemsList) cartItemsList.innerHTML = '<p class="empty-message">Seu carrinho está vazio</p>';
        if (checkoutBtn) checkoutBtn.style.display = 'none';
    } else {
        if (cartItemsList) {
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
        }
        if (checkoutBtn) checkoutBtn.style.display = 'block';
    }

    // Calcula o valor total em dinheiro
    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    if (totalAmount) totalAmount.textContent = total.toFixed(2);
}

/**
 * 5. ALTERNAR MODAL DO CARRINHO
 */
function toggleCart() {
    const modal = document.getElementById('cart-modal');
    if (modal) {
        modal.classList.toggle('show');
    }
}

/**
 * 6. FINALIZAR PEDIDO (CHECKOUT)
 */
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

/**
 * 7. CARREGAR PEDIDOS NA TELA DE ADMINISTRAÇÃO
 */
function loadAdminOrders() {
    const ordersContainer = document.getElementById('admin-orders-list');
    if (!ordersContainer) return;

    fetch('/api/orders')
        .then(response => response.json())
        .then(orders => {
            ordersContainer.innerHTML = '';

            if (orders.length === 0) {
                ordersContainer.innerHTML = `
                    <tr>
                        <td colspan="5" style="text-align: center; color: #999; padding: 40px;">Nenhum pedido recebido até ao momento.</td>
                    </tr>`;
                return;
            }

            // Inverte para exibir os pedidos mais recentes no topo da tabela
            orders.reverse().forEach(order => {
                const itemsFormatted = order.items.map(item => `${item.name} (x${item.quantity})`).join('<br>');
                
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td class="col-id">${order.order_id}</td>
                    <td style="color: #718096;">${order.timestamp}</td>
                    <td style="line-height: 1.5;">${itemsFormatted}</td>
                    <td class="col-total">R$ ${order.total.toFixed(2)}</td>
                    <td><span class="badge-status">${order.status}</span></td>
                `;
                ordersContainer.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Erro ao carregar dados do administrador:', error);
            ordersContainer.innerHTML = `<tr><td colspan="5" style="text-align: center; color: red; padding: 40px;">Erro ao carregar os dados dos pedidos.</td></tr>`;
        });
}

/**
 * 8. EXPORTAR TODOS OS PEDIDOS EM FORMATO JSON
 */
function exportarPedidosJSON() {
    fetch('/api/orders')
        .then(response => response.json())
        .then(orders => {
            if (orders.length === 0) {
                alert('⚠️ Não existem pedidos registados para exportar!');
                return;
            }

            // Converte a lista para string JSON estruturada
            const jsonString = JSON.stringify(orders, null, 4);
            const blob = new Blob([jsonString], { type: 'application/json' });
            const url = window.URL.createObjectURL(blob);
            
            // Link temporário para simular o download automático
            const downloadLink = document.createElement('a');
            downloadLink.href = url;
            downloadLink.download = `pedidos_rosana_${new Date().toISOString().slice(0,10)}.json`;
            
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);
            window.URL.revokeObjectURL(url);
        })
        .catch(error => {
            console.error('Erro na exportação:', error);
            alert('Não foi possível exportar os pedidos.');
        });
}