from flask import Flask
from database import init_db
from config import DATABASE_URL  # Importe a URL do banco de dados do config.py

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SECRET_KEY'] = 'chave_secreta'  # Chave secreta para flash messages

# Inicializa o banco de dados
init_db()

# Importa as rotas
from routes import routes
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)