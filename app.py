import os
from dotenv import load_dotenv
from flask import Flask
from database import init_db
from config import DATABASE_URL

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SECRET_KEY'] = SECRET_KEY

# Inicializa o banco de dados
init_db()

# Importa e registra as rotas
from routes import routes
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)