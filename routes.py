from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, validators
from models import Produto
from database import get_db
from sqlalchemy.orm import Session
from werkzeug.utils import secure_filename
import csv
import logging

# Configuração do logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

# Blueprint para organizar as rotas
main = Blueprint('main', __name__)

# Formulário de upload com validação
class UploadForm(FlaskForm):
    file = FileField('Arquivo', validators=[DataRequired()])
    submit = SubmitField('Enviar')

# Limita o tamanho máximo do arquivo (ajuste conforme necessário)
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

@main.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename):
            if file.content_length > MAX_CONTENT_LENGTH:
                flash('Arquivo muito grande. O tamanho máximo permitido é de 16MB.', 'error')
                return redirect(url_for('index'))

            filename = secure_filename(file.filename)
            try:
                with open(os.path.join(UPLOAD_FOLDER, filename), 'r') as csvfile:
                    reader = csv.reader(csvfile, delimiter=';')
                    # Pula o cabeçalho (se houver)
                    next(reader, None)

                    with next(get_db()) as db:
                        db.query(Produto).delete()
                        db.commit()

                        for row in reader:
                            try:
                                id_produto, descricao, valor, unidade = row
                                produto = Produto(id=id_produto, codigo=id_produto, descricao=descricao, valor=float(valor), unidade=unidade)
                                db.add(produto)
                            except (ValueError, IndexError) as e:
                                logging.error(f"Erro ao processar linha {row}: {e}")
                                flash('Erro ao processar linha do arquivo. Verifique o formato.', 'error')
                                db.rollback()
                                break

                        db.commit()
                        flash('Arquivo TXT enviado e dados atualizados com sucesso!', 'success')
            except Exception as e:
                logging.error(f"Erro geral: {e}")
                flash('Ocorreu um erro inesperado. Verifique o log para mais detalhes.', 'error')

    return render_template('index.html', form=form)

# ... (outras rotas)

@routes.route('/produtos', methods=['GET'])
def get_produtos():
    with next(get_db()) as db:
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