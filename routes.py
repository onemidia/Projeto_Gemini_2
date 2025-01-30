import os
import csv
import json
from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for, current_app
from models import Produto
from database import get_db
from sqlalchemy.orm import Session
from werkzeug.utils import secure_filename

routes = Blueprint("routes", __name__)

# ... (resto do seu código)

@routes.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        arquivo = None  # Defina arquivo como None aqui

        if 'file' not in request.files:
            flash('Nenhum arquivo enviado', 'error')
            return redirect(request.url)

        arquivo = request.files['file'] # Move a definição para cá
        if arquivo.filename == '':
            flash('Nenhum arquivo selecionado', 'error')
            return redirect(request.url)
        
        if arquivo and allowed_file(arquivo.filename): # Agora arquivo está sempre definido
            # ... (resto do seu código para processar o arquivo)

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