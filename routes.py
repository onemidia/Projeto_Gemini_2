import os
import csv
import json
from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for, current_app
from models import Produto
from database import get_db
from sqlalchemy.orm import Session
from werkzeug.utils import secure_filename

routes = Blueprint("routes", __name__)

# Configurações
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt'}

# Função para verificar se o arquivo tem uma extensão permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@routes.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        arquivo = None  # Inicializa arquivo como None
        filename = None  # Inicializa filename como None

        if 'file' not in request.files:
            flash('Nenhum arquivo enviado', 'error')
            return redirect(request.url)

        arquivo = request.files['file']
        if arquivo.filename == '':
            flash('Nenhum arquivo selecionado', 'error')
            return redirect(request.url)

        if arquivo and allowed_file(arquivo.filename):
            filename = secure_filename(arquivo.filename)  # Define filename aqui
            try:
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                arquivo.save(os.path.join(UPLOAD_FOLDER, filename))

                # ... (resto do código para processar o arquivo)

            except Exception as e:
                flash(f'Erro ao processar arquivo: {e}', 'error')
                return redirect(request.url)

        else:
            flash('Tipo de arquivo não permitido', 'error')
            return redirect(request.url)

    return render_template('index.html')

@routes.route('/produtos', methods=['GET'])
def get_produtos():
    with next(get_db()) as db:  # Use o bloco with aqui
        produtos = db.query(Produto).all()
        produtos_json = [
            {
                'id': produto.id,
                'codigo': produto.codigo,
                'descricao': produto.descricao,
                'valor': produto.valor,
                'unidade': produto.unidade
            } for produto in produtos
        ]
        return jsonify(produtos_json)