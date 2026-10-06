from app import create_app

# Cria a instância do aplicativo Flask usando a factory function
app = create_app()

if __name__ == '__main__':
    # Roda o servidor local de testes
    app.run(debug=True)
