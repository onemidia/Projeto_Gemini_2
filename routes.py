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
        if 'file' not in request.files:
            flash('Nenhum arquivo enviado', 'error')
            return redirect(request.url)
        arquivo = request.files['file']
        if arquivo.filename == '':
            flash('Nenhum arquivo selecionado', 'error')
            return redirect(request.url)
        if arquivo and allowed_file(arquivo.filename):
            filename = secure_filename(arquivo.filename)
            try:
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                arquivo.save(os.path.join(UPLOAD_FOLDER, filename))

                # Converter TXT para JSON e salvar no banco de dados
                with open(os.path.join(UPLOAD_FOLDER, filename), 'r') as file:
                    reader = csv.reader(file, delimiter=';')
                    produtos = []
                    db: Session = next(get_db())  # Obtém a sessão do banco de dados
                    # Limpa a tabela antes de inserir novos dados
                    db.query(Produto).delete()
                    db.commit()
                    for row in reader:
                        try:
                            id_produto = int(row[0])
                            descricao = row[1]
                            valor = float(row[2])
                            unidade = row[3]
                            produto = Produto(id=id_produto, codigo=id_produto, descricao=descricao, valor=valor, unidade=unidade)
                            db.add(produto)
                            produtos.append(produto)
                        except ValueError:
                            flash('Erro ao processar linha do arquivo TXT. Verifique o formato.', 'error')
                            db.rollback()  # Cancela as alterações em caso de erro
                            break  # Interrompe o loop em caso de erro
                    if not produtos:
                      return redirect(request.url)
                    db.commit()
                    flash('Arquivo TXT enviado e dados atualizados com sucesso!', 'success')
                    return redirect(url_for('index'))
            except Exception as e:
                flash(f'Erro ao processar arquivo: {e}', 'error')
                return redirect(request.url)
        else:
            flash('Tipo de arquivo não permitido', 'error')
            return redirect(request.url)
    return render_template('index.html')

@routes.route('/produtos', methods=['GET'])
def get_produtos():
    db: Session = next(get_db())  # Obtém a sessão do banco de dados
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