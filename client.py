from flask import Flask, render_template, request, redirect, flash, url_for
import requests
import secrets

app = Flask(__name__)

secret = secrets.token_urlsafe(32)
app.secret_key = secret

headers = {'Content-Type': "application/json", 'Accept': "application/json"}

@app.route('/')
def index():
    response = requests.get('http://127.0.0.1:5000/modelo', headers=headers)
    if response.status_code == 200:
        modelos = response.json()
        return render_template('index.html', modelos=modelos)

@app.route('/create', methods=['POST'])
def create():
    nome = request.form['nome']
    descricao = request.form['descricao']

    requests.post('http://127.0.0.1:5000/modelo', json={'nome':nome, 'descricao': descricao}, headers=headers)

    flash("Modelo adicionado com sucesso!")

    return redirect(url_for('index'))

@app.route('/update', methods=['GET','POST'])
def update():
    if request.method == "POST":
        id = request.form['id']

        nome = request.form['nome']
        descricao = request.form['descricao']

        link = 'http://127.0.0.1:5000/modelo/{0}'.format(id)

        requests.put(link, json={'nome':nome, 'descricao': descricao}, headers=headers)

        flash("Modelo editado com sucesso!")
        
        return redirect(url_for('index'))
    else:
        redirect(url_for('delete'))


@app.route('/delete', methods=['GET','POST'])
def delete(id):
    if request.method == "POST":

        link = 'http://127.0.0.1:5000/modelo/{0}'.format(id)

        requests.delete(link, headers=headers)

        flash("Modelo Deletado com Sucesso.")

        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(port=3000)