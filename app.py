from flask import Flask, render_template, request, redirect
from wtforms import Form
from mundobibble import create_app

app = create_app()

@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/cadastro', methods = ['GET','POST'])
def cadastro():
    if Form.validate_on_submit:
        nome = request.form.get('nome') 
        cpf = request.form.get('cpf') 
        email = request.form.get('mail') 
        endereco = request.form.get('ender')
        
        return render_template('index-cadastro.html')

@app.route('/iniciar', methods = ['GET', 'POST'])
def iniciar():
    return render_template('index-iniciar.html')

if __name__ == "__main__":
    app.run(debug = True)