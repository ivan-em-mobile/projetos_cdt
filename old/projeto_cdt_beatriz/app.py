'''
🍔 HAMBURGUERIA ROSANA - BACKEND EM PYTHON (FLASK)
'''

from flask import Flask, render_template, request, jsonify
from datetime import datetime
import random
import string

app = Flask(__name__)

# Armazenar pedidos em memória (Lista global para simular uma base de dados provisória)
orders = []

def generate_order_id():
    """Gera um ID único alfanumérico de 8 caracteres para o pedido"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# ==========================================================================
# 📌 ROTAS DAS PÁGINAS (HTML)
# ==========================================================================

@app.route('/')
def index():
    """Página inicial do site (Apresentação e Benefícios)"""
    return render_template('index.html')

@app.route('/menu')
def menu():
    """Página do cardápio para os clientes escolherem os hambúrgueres"""
    return render_template('menu.html')

@app.route('/admin')
def admin():
    """Página de Administração para gerir e exportar os pedidos recebidos"""
    return render_template('admin.html')


# ==========================================================================
# 📌 ROTAS DA API (JSON)
# ==========================================================================

@app.route('/api/menu', methods=['GET'])
def api_menu():
    """API que retorna os itens do cardápio em formato JSON"""
    menu_items = [
        {
            'id': 1,
            'name': 'Hambúrguer Clássico',
            'description': 'Pão, carne, queijo, alface, tomate',
            'price': 25.00,
            'image': 'https://images.unsplash.com/photo-1610970878459-a0e464d7592b?w=400&h=300&fit=crop'
        },
        {
            'id': 2,
            'name': 'Hambúrguer Duplo',
            'description': 'Pão, 2 carnes, 2 queijos, bacon',
            'price': 35.00,
            'image': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400&h=300&fit=crop'
        },
        {
            'id': 3,
            'name': 'X-Bacon Premium',
            'description': 'Carne, bacon crocante, cebola caramelizada',
            'price': 40.00,
            'image': 'https://images.unsplash.com/photo-1553979459-d2229ba7433b?w=400&h=300&fit=crop'
        },
        {
            'id': 4,
            'name': 'Torta Holandesa',
            'description': 'Deliciosa torta de chocolate com creme e biscoito',
            'price': 30.00,
            'image': 'https://images.unsplash.com/photo-1571115177098-24ec42ed204d?w=400&h=300&fit=crop'
        },
        {
            'id': 5,
            'name': 'X-Tudo',
            'description': 'Carne, bacon, ovo, queijo, alface, tomate',
            'price': 45.00,
            'image': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400&h=300&fit=crop'
        },
        {
            'id': 6,
            'name': 'Cheeseburger',
            'description': 'Carne suculenta com 2 queijos derretidos',
            'price': 28.00,
            'image': 'https://images.unsplash.com/photo-1603064752734-4c48eff53d05?w=400&h=300&fit=crop'
        },
        {
            'id': 7,
            'name': 'Batata Frita',
            'description': 'Porção crocante com sal grosso',
            'price': 10.00,
            'image': 'https://images.unsplash.com/photo-1541592106381-b31e9677c0e5?w=400&h=300&fit=crop'
        },
        {
            'id': 8,
            'name': 'Refrigerante',
            'description': 'Lata 350ml - Coca, Guaraná, Sprite',
            'price': 7.00,
            'image': 'https://plus.unsplash.com/premium_photo-1725075086631-b21a5642918b?w=400&h=300&fit=crop'
        },
        {
            'id': 9,
            'name': 'Suco Natural',
            'description': 'Laranja, melancia ou morango',
            'price': 8.00,
            'image': 'https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=400&h=300&fit=crop'
        }
    ]
    return jsonify(menu_items)

@app.route('/api/checkout', methods=['POST'])
def api_checkout():
    """API para receber dados do carrinho, criar o pedido e guardar em memória"""
    try:
        data = request.get_json()
        
        # Validar dados recebidos do JavaScript
        if not data or 'items' not in data or 'total' not in data:
            return jsonify({'success': False, 'message': 'Dados inválidos'}), 400
        
        # Gerar o ID único do pedido
        order_id = generate_order_id()
        
        # Criar a estrutura do objeto do pedido
        order = {
            'order_id': order_id,
            'items': data['items'],
            'total': data['total'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'Recebido'
        }
        
        # Armazenar o pedido na lista global
        orders.append(order)
        
        # Print do pedido no terminal do Python (para monitoramento em tempo real)
        print(f"\n{'='*60}")
        print(f"🍔 NOVO PEDIDO RECEBIDO")
        print(f"{'='*60}")
        print(f"ID do Pedido: {order_id}")
        print(f"Data/Hora: {order['timestamp']}")
        print(f"Itens:")
        for item in data['items']:
            print(f"  - {item['name']} (x{item['quantity']}) - R$ {item['price'] * item['quantity']:.2f}")
        print(f"Total: R$ {data['total']:.2f}")
        print(f"{'='*60}\n")
        
        return jsonify({
            'success': True,
            'order_id': order_id,
            'message': 'Pedido realizado com sucesso!'
        })
    
    except Exception as e:
        print(f"❌ Erro ao processar pedido: {str(e)}")
        return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500

@app.route('/api/orders', methods=['GET'])
def api_get_orders():
    """API utilizada pela página admin para retornar todos os pedidos cadastrados"""
    return jsonify(orders)

@app.route('/api/orders/<order_id>', methods=['GET'])
def api_get_order(order_id):
    """API para consultar um pedido específico pelo seu ID exclusivo"""
    order = next((o for o in orders if o['order_id'] == order_id), None)
    
    if not order:
        return jsonify({'success': False, 'message': 'Pedido não encontrado'}), 404
    
    return jsonify({'success': True, 'order': order})

@app.route('/api/health', methods=['GET'])
def api_health():
    """Verificar a saúde e conectividade da aplicação"""
    return jsonify({'status': 'ok', 'message': 'Servidor funcionando normalmente'})


# ==========================================================================
# 📌 TRATAMENTO DE ERROS CUSTOMIZADOS (PÁGINAS)
# ==========================================================================

@app.errorhandler(404)
def not_found(error):
    """Tratamento de página não encontrada (Erro 404)"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Tratamento de erro interno no servidor (Erro 500)"""
    return render_template('500.html'), 500


# ==========================================================================
# 📌 INICIALIZAÇÃO DO SERVIDOR FLASK
# ==========================================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🍔 HAMBURGUERIA ROSANA - SERVIDOR INICIADO COM SUCESSO")
    print("="*60)
    print("Acesse o Cardápio em: http://localhost:5000/menu")
    print("Acesse o Painel Admin em: http://localhost:5000/admin")
    print("="*60 + "\n")
    
    # Executa o Flask na porta 5000 em modo debug (reinicia ao salvar o código)
    app.run(debug=True, host='0.0.0.0', port=5000)