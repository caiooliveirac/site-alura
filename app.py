from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
    

class Jogo:
    def __init__(self, nome, categoria, console) -> None:
        self.nome = nome
        self.categoria = categoria
        self.console = console

jogo1 = Jogo('Super Mario','Acao','SNES')
jogo2 = Jogo('Pokemon Gold','RPG','GBA')
lista = [jogo1,jogo2]

@app.route('/')
def index():
    return render_template('lista.html',titulo='Jogos',jogos=lista)

@app.route('/novo')
def novo():
    return render_template('novo.html',titulo='Novo Jogo')

@app.route('/criar')
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    return redirect('/')


app.run()