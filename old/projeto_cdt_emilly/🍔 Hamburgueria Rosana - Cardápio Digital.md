# 🍔 Hamburgueria Rosana - Cardápio Digital

Um aplicativo web moderno para gerenciar o cardápio e pedidos da Hamburgueria Rosana, desenvolvido com Flask e JavaScript.

## 📋 Características

- ✅ Página inicial com apresentação da hamburgueria
- ✅ Cardápio dinâmico com 9 produtos
- ✅ Carrinho de compras flutuante
- ✅ Sistema de pedidos com ID único
- ✅ Design responsivo (mobile, tablet, desktop)
- ✅ API RESTful para gerenciar pedidos
- ✅ Interface intuitiva e moderna

## 🚀 Como Usar Localmente

### 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/hamburgueria-rosana.git
cd hamburgueria-rosana
```

### 2. Criar ambiente virtual
```bash
python -m venv venv
```

### 3. Ativar ambiente virtual

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Instalar dependências
```bash
pip install -r requirements.txt
```

### 5. Executar a aplicação
```bash
python app.py
```

A aplicação estará disponível em: `http://localhost:5000`

## 📁 Estrutura do Projeto

```
hamburgueria-rosana/
├── app.py                  # Arquivo principal Flask
├── requirements.txt        # Dependências Python
├── README.md              # Este arquivo
├── .gitignore             # Arquivos ignorados pelo Git
├── templates/             # Templates HTML
│   ├── index.html         # Página inicial
│   ├── menu.html          # Página do cardápio
│   ├── 404.html           # Página de erro 404
│   └── 500.html           # Página de erro 500
└── static/                # Arquivos estáticos
    ├── css/
    │   └── style.css      # Estilos da aplicação
    └── js/
        └── script.js      # JavaScript da aplicação
```

## 🔌 API Endpoints

### GET `/`
Retorna a página inicial

### GET `/menu`
Retorna a página do cardápio

### GET `/api/menu`
Retorna o cardápio em formato JSON
```json
[
  {
    "id": 1,
    "name": "Hambúrguer Clássico",
    "description": "Pão, carne, queijo, alface, tomate",
    "price": 25.00,
    "image": "..."
  }
]
```

### POST `/api/checkout`
Processa um novo pedido
```json
{
  "items": [
    {
      "id": 1,
      "name": "Hambúrguer Clássico",
      "price": 25.00,
      "quantity": 2
    }
  ],
  "total": 50.00
}
```

**Resposta:**
```json
{
  "success": true,
  "order_id": "ABC12345",
  "message": "Pedido realizado com sucesso!"
}
```

### GET `/api/orders`
Retorna todos os pedidos

### GET `/api/orders/<order_id>`
Retorna um pedido específico

### GET `/api/health`
Verifica o status do servidor

## 🎨 Design

- **Cores principais:** Laranja (#ff6b35), Bege (#f5f1e8), Marrom (#5c3d2e)
- **Tipografia:** System fonts (Segoe UI, Roboto, etc.)
- **Layout:** Responsivo e mobile-first
- **Animações:** Transições suaves e hover effects

## 📱 Compatibilidade

- ✅ Chrome/Edge (versão 90+)
- ✅ Firefox (versão 88+)
- ✅ Safari (versão 14+)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## 🚀 Deploy no Vercel

### 1. Fazer push para GitHub
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### 2. Conectar ao Vercel
1. Acesse [vercel.com](https://vercel.com)
2. Clique em "New Project"
3. Selecione seu repositório do GitHub
4. Configure as variáveis de ambiente (se necessário)
5. Clique em "Deploy"

### 3. Configurar vercel.json (opcional)
Crie um arquivo `vercel.json` na raiz do projeto:
```json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

## 🔐 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto (não faça commit):
```
FLASK_ENV=production
FLASK_DEBUG=False
```

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 👤 Autor

Desenvolvido para Hamburgueria Rosana

## 📞 Suporte

Para dúvidas ou sugestões, entre em contato com o desenvolvedor.

---

**Feito com ❤️ para os amantes de hambúrgueres** 🍔
