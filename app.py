from flask import Flask, render_template, request, redirect, url_for, flash
from mundobibble import create_app
from flask_mysqldb import MySQL

from flask_login import login_user

app = create_app()

# Configurações do banco de dados
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'labinfo'
app.config['MYSQL_DB'] = 'MundoLiterario'

# Inicialização do MySQL
mysql = MySQL()
mysql.init_app(app)

@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/livro')
def livro():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM livro")
    data = cursor.fetchall()
    cursor.close()
    return str(data)

@app.route('/autor/<name>')
def autor(name):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM autor WHERE {name}")
    data = cursor.fetchall()
    cursor.close()
    return str(data)

def formulario():
    return render_template('index-cadastro.html')


@app.route('/cadastro', methods = ['GET','POST'])
def cadastro():
    nome = request.form['nome'] 
    cpf = request.form['cpf'] 
    mail = request.form['mail'] 
    ender = request.form['ender']

    cur = mysql.connection.cursor()

    # Executar o comando SQL para inserir os dados na tabela usuário
    cur.execute("INSERT INTO Usuario (nome, email, senha) VALUES (%s, %s, %s)", (nome, mail, ender))

    # Commit para salvar as mudanças no banco de dados
    mysql.connection.commit()

    # Fechar o cursor
    cur.close()


    return render_template("index-cadastro.html", nome = nome, cpf = cpf, mail = mail, ender = ender, form = form)


@app.route('/iniciar', methods = ['GET', 'POST'])
def iniciar():
    form = LoginForm()
    if form.validate_on_submit():
        user = user.query.filter_by(username = form.user.name.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Seja bem-vindo!')
            return redirect(url_for('/'))
        else:
            flash('Usuario ou senha invalidos.')
    return render_template('index-iniciar.html', form = form)

@app.route('/carrinho', methods = ['GET', 'POST'])
def carrinho():
    return render_template('index-carrinho.html')

if __name__ == "__main__":
    app.run(debug = True)