from flask import Flask, jsonify, redirect, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
import secrets

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

secret = secrets.token_urlsafe(32)

app.secret_key = secret


class Modelo(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return self.nome

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_nome(cls, nome):
        return cls.query.filter_by(nome=nome).first()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class ModeloSchema(Schema):
    id = fields.Integer()
    nome = fields.String()
    descricao = fields.String()


@app.route('/modelo', methods=['GET'])
def get_all_modelos():
    """Retorna todos os modelos de IA cadastrados na base de dados."""
    modelos = Modelo.get_all()
    serializer = ModeloSchema(many=True)
    dados = serializer.dump(modelos)
    return jsonify(
        dados
    )


@app.route('/modelo', methods=['POST'])
def create_modelo():
    """Cadastra um novo modelo no banco de dados."""
    content_type = request.headers.get('Content-Type')

    if (content_type == 'application/json'):
        dados = request.get_json()

        novo_modelo = Modelo(
            nome=dados.get('nome'),
            descricao=dados.get('descricao')
        )

        novo_modelo.save()

        serializer = ModeloSchema()

        dados = serializer.dump(novo_modelo)

        return jsonify(
            dados
        ), 201
    elif (content_type == 'application/x-www-form-urlencoded'):
        nome = request.form['nome']
        descricao = request.form['descricao']

        novo_modelo = Modelo(nome=nome, descricao=descricao)
        novo_modelo.save()

        flash("Modelo adicionado com sucesso!")

        return redirect(url_for('index'))


@app.route('/modelo/<string:nome>', methods=['GET'])
def get_modelo_by_nome(nome):
    """Retorna nome e descrição de um determinado modelo passado seu nome como parâmetro."""
    modelo = Modelo.get_by_nome(nome)

    serializer = ModeloSchema()

    dados = serializer.dump(modelo)

    return jsonify(
        dados
    ), 200


@app.route('/modelo/<int:id>', methods=['GET'])
def get_modelo_by_id(id):
    """Retorna nome e descrição de um determinado modelo passado seu id como parâmetro."""
    modelo = Modelo.get_by_id(id)

    serializer = ModeloSchema()

    dados = serializer.dump(modelo)

    return jsonify(
        dados
    ), 200


@app.route('/modelo/<int:id>', methods=['PUT'])
def update_modelo(id):
    """Edita os campos de um modelo (nome, descrição)."""
    modelo = Modelo.get_by_id(id)

    dados = request.get_json()

    modelo.nome = dados.get('nome')
    modelo.descricao = dados.get('descricao')

    db.session.commit()

    serializer = ModeloSchema()

    dados = serializer.dump(modelo)

    return jsonify(
        dados
    ), 200


@app.route('/modelo/<int:id>', methods=['DELETE'])
def delete_modelo(id):
    """Deleta o modelo da base de dados."""
    modelo = Modelo.get_by_id(id)

    modelo.delete()

    return jsonify(
        {"message": "Deletado"}
    ), 204


@app.before_first_request
def create_table():
    db.create_all()


@app.route('/')
def index():
    modelos = Modelo.get_all()
    return render_template('index.html', modelos=modelos)


@app.route('/update', methods=['GET', 'POST'])
def update():
    if (request.method == 'POST'):
        dados = Modelo.query.get(request.form.get('id'))

        dados.nome = request.form['nome']
        dados.descricao = request.form['descricao']

        db.session.commit()
        flash("Modelo editado com sucesso!")

        return redirect(url_for('index'))


@app.route('/delete/<int:id>/', methods=['GET', 'POST'])
def delete(id):
    dados = Modelo.query.get(id)
    db.session.delete(dados)
    db.session.commit()
    flash("Modelo Deletado com Sucesso.")

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
