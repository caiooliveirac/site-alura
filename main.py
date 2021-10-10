from flask import Flask, render_template, request, redirect, session, flash
import pymysql.cursors
from ambiente import Hash, jovem1, pares
from time import sleep

app = Flask(__name__)
app.secret_key = "senhasecretasamu192"

db = pymysql.connect(host=jovem1.host, user=jovem1.user, password=jovem1.password, db="samu",cursorclass=pymysql.cursors.DictCursor)

class Unidade:
    def __init__(self,nome,vermelha,verde,ortopedista,cirurgiao,radiografia):
        self.nome = nome
        self.vermelha = vermelha
        self.verde = verde
        self.ortopedista = ortopedista
        self.cirurgiao = cirurgiao
        self.radiografia = radiografia

@app.route('/')
def ola():
    cursor = db.cursor()
    cursor.execute("SELECT *,CONCAT(TIMESTAMPDIFF(MINUTE,atualizou,NOW()),' minutos') as `atualizado_ha` from samu.unidades WHERE unidade LIKE '%UPA%' ORDER BY unidade")
    data = cursor.fetchall()
    cursor1 = db.cursor()
    cursor1.execute("SELECT *,CONCAT(TIMESTAMPDIFF(MINUTE,atualizou,NOW()),' minutos') as `atualizado_ha` from samu.unidades WHERE unidade NOT LIKE '%UPA%'")
    data1 = cursor1.fetchall()
    cursor2 = db.cursor()
    cursor2.execute("SELECT *,CONCAT(TIMESTAMPDIFF(MINUTE,atualizou,NOW()),' minutos') as atualizado_ha FROM samu.hospitais ORDER BY unidade")
    data2 = cursor2.fetchall()
    cursor3 = db.cursor()
    cursor3.execute("SELECT *,CONCAT(TIMESTAMPDIFF(MINUTE,atualizou,NOW()),' minutos') as atualizado_ha FROM samu.psiquiatricos ORDER BY unidade")
    data3 = cursor3.fetchall()
    cursor4 = db.cursor()
    cursor4.execute("SELECT *,CONCAT(TIMESTAMPDIFF(MINUTE,atualizou,NOW()),' minutos') as atualizado_ha FROM samu.maternidades ORDER BY unidade")
    data4 = cursor4.fetchall()
    return render_template('lista.html',titulo='PAs',unidades=data,pas=data1,hospitais=data2,psiquiatricos=data3,maternidades=data4)
        
@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login')
    else:
        return render_template('novo.html',titulo='Atualize Pronto Atendimento')

@app.route('/criar',methods=['POST'])
def criar():
    if request.method == "POST":
        details = request.form
        restricao =0
        verde = 0
        ortopedista =0
        cirurgiao = 0
        rx = 0
        nome = details['nome']
        if details.get('restricao'):
            restricao = details['restricao']
        if details.get('verde'):
            verde = details['verde']
        if details.get('ortopedista'):
            ortopedista = details['ortopedista']
        if details.get('cirurgiao'):
            cirurgiao = details['cirurgiao']
        if details.get('rx'):
            rx = details['rx']
        cursor = db.cursor()
        sql = f"INSERT INTO samu.unidades(idunidades,unidade,restricao,verde,ortopedista,cirurgiao,rx) VALUES (DEFAULT,'{nome}',{restricao},{verde},{ortopedista},{cirurgiao},{rx})"
        cursor.execute(sql)
        db.commit()
        cursor.close()
    return redirect('/')

@app.route('/novohosp')
def novohosp():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login')
    else:
        return render_template('novohosp.html',titulo='Atualize Hospital')

@app.route('/criarhosp',methods=['POST'])
def criarhosp():
    if request.method == "POST":
        details = request.form
        chefe = 0
        contato = 0 
        equipe = 0
        vermelha = 0        
        nome = details['nome']
        if details.get('chefe'):
            chefe = details['chefe']
        if details.get('contato'):
            contato = details['contato']
        if details.get('equipe'):
            equipe = details['equipe']
        if details.get('vermelha'):
            vermelha = details['vermelha']
        cursor = db.cursor()
        sql = f"INSERT INTO samu.hospitais(id,unidade,chefe,contato,equipe,vermelha) VALUES (DEFAULT,'{nome}','{chefe}','{contato}','{equipe}','{vermelha}')"
        cursor.execute(sql)
        db.commit()
        cursor.close()
    return redirect('/')

@app.route('/novopsiq')
def novopsiq():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login')
    else:
        return render_template('novopsiq.html',titulo='Atualize Unidade Psiquiátrica')

@app.route('/criarpsiq',methods=['POST'])
def criarpsiq():
    if request.method == "POST":
        details = request.form
        #contato, lotacao = "Não informado"      
        nome = details['nome']
        if details.get('contato'):
            contato = details['contato']
        if details.get('lotacao'):
            lotacao = details['lotacao']
        cursor = db.cursor()
        sql = f"INSERT INTO samu.psiquiatricos(idunidades,unidade,contato,lotacao) VALUES (DEFAULT,'{nome}','{contato}','{lotacao}')"
        cursor.execute(sql)
        db.commit()
        cursor.close()
    return redirect('/')

@app.route('/novomaternidade')
def novomaternidade():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login')
    else:
        return render_template('novomaternidade.html',titulo='Atualize Maternidade')

@app.route('/criarmaternidade',methods=['POST'])
def criarmaternidade():
    if request.method == "POST":
        details = request.form
        contato = 0
        equipe = 0
        lotacao = 0
        nome = details['nome']
        if details.get('contato'):
            contato = details['contato']
        if details.get('equipe'):
            equipe = details['equipe']
        if details.get('lotacao'):
            lotacao = details['lotacao']
        cursor = db.cursor()
        sql = f"INSERT INTO samu.maternidades(idunidades,unidade,contato,equipe,lotacao) VALUES (DEFAULT,'{nome}','{contato}','{equipe}','{lotacao}')"
        cursor.execute(sql)
        db.commit()
        cursor.close()
    return redirect('/')

@app.route('/login')
def login():
    return render_template('login.html',titulo='Login')

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
    if request.method == 'POST':
        session['usuario_logado'] = None
        flash('Nenhum usuário logado.')
        return redirect('/')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html',titulo='Cadastro')

@app.route('/cadastrar',methods=['GET','POST'])
def cadastrar():
    novo_usuario = request.form['login']
    nova_senha = request.form['senha']
    pares[novo_usuario] = nova_senha
    return redirect('/login')

app.run(debug=True)
