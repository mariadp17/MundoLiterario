from flask import Flask, render_template, request, redirect
from wtforms import Form
from mundobibble import create_app

app = create_app()

@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/cadastro', methods = ['GET','POST'])
def cadastro():
    nome = request.form.get('nome') 
    cpf = request.form.get('cpf') 
    mail = request.form.get('mail') 
    ender = request.form.get('ender')
    
    return render_template('index-cadastro.html', nome = nome, cpf = cpf, mail = mail, ender = ender)

@app.route('/iniciar', methods = ['GET', 'POST'])
def iniciar():
    return render_template('index-iniciar.html')

@app.route('/carrinho', methods = ['GET', 'POST'])
def carrinho():
    return render_template('index-carrinho.html')

if __name__ == "__main__":
    app.run(debug = True)