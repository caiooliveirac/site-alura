import os
from flask import Flask, render_template, request, redirect, session, flash

app = Flask(__name__)
app.secret_key = "senhasecreta"

class Telaini:
    def __init__(self,nome,categoria):
        self.nome = nome
        self.categoria = categoria

jogo1 = Telaini('Caio','MSFS')
jogo2 = Telaini('Iolanda','Violao')
jogos = [jogo1,jogo2]

@app.route('/')
def ola():
    return render_template('lista.html',titulo='Lista',jogos=jogos)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login')
    else:
        return render_template('novo.html',titulo='Cadastre')

@app.route('/criar',methods=['POST'])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    jogo = Telaini(nome, categoria)
    jogos.append(jogo)
    return redirect('/')

@app.route('/login')
def login():
    return render_template('login.html',titulo='Login')

pares = {'Caio':'25161515','Iolanda':'ca251094'}

@app.route('/autenticar',methods=['POST'])
def autenticar():
    usuario = request.form['login']
    tentativa_login = pares.get(usuario)
    if request.form['senha'] == tentativa_login:
        session['usuario_logado'] = request.form['login']
        flash(session['usuario_logado']+' (online)')
        return redirect('/')
    else:
        flash('Não foi possível realizar login. Tenta novamente!')
        return redirect('/login')

@app.route('/logout',methods=['POST'])
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado.')
    return redirect('/')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html',titulo='Cadastro')

@app.route('/cadastrar',methods=['POST'])
def cadastrar():
    novo_usuario = request.form['login']
    nova_senha = request.form['senha']
    pares[novo_usuario] = nova_senha
    return redirect('/login')

app.run(debug=True)
