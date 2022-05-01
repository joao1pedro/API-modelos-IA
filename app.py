from flask import Flask, jsonify, request
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


@app.route('/modelo', methods=['GET','POST'])
def create_modelo():
    """Cadastra um novo modelo no banco de dados."""
    if request.method == 'POST':
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


@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_modelo(id):
    """Deleta o modelo da base de dados."""
    dados = Modelo.query.get(id)
    db.session.delete(dados)
    db.session.commit()

    return jsonify(
        {"message": "Deletado"}
    ), 204


@app.before_first_request
def create_table():
    """Cria a tabela do banco de dados caso não exista"""
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
