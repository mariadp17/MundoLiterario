from flask import Flask, render_template, request, redirect, url_for, flash
from mundobibble import create_app
from flask_mysqldb import MySQL
import mysql.connector
from flask_login import login_user
from flask_hashing import Hashing

app = create_app()

# Configurações do banco de dados
db = mysql.connector.connect(host = 'localhost', user = 'root', password = 'labinfo', database = 'MundoLiterario')

hashing = Hashing(app)

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


@app.route('/cadastro', methods = ['GET','POST'])
def cadastro():
    if request.method == 'POST':

        nome = request.form['name']
        email = request.form['email']
        telefone = request.form['telephone']
        senha = request.form['password']

        #dando hashing na senha, hashing de 16 caracteres
        hashed_password = hashing.hash_value(senha)
        hashed_password = hashed_password[:16]
        
        #checando se o email já está cadastrado
        cursor = db.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM Usuario WHERE email='{email}'")
        check_pessoa_existe = cursor.fetchall()
        
        if check_pessoa_existe:
            return ("Este email já foi cadastrado!")
        else:
            # dando post no banco com as informações do cliente
            userBD = "INSERT INTO Usuario (nome, senha, email) VALUES (%s, %s, %s)"
            
            tupla_user= (nome, senha, email)
            
            cursor.execute(userBD, tupla_user)
            cursor.close()
            db.commit()
            
            # criando outro cursor para pegar o id_cliente que acabou de ser adicionado para adicionar o telefone do mesmo
            cursor = db.cursor(dictionary=True)
            selectUserID = (f"SELECT UsuarioID FROM Usuario WHERE email='{email}'")
            cursor.execute(selectUserID)
            fetch_cpf = cursor.fetchall()
            fetch_cpf[0]['UsuarioID']
            
            telefoneBD = "INSERT INTO Telefone (Telefone1, CodUsuario) VALUES (%s, %s)"
            
            tupla_telefoneBD = (fetch_cpf[0]['UsuarioID'], telefone)
            cursor.execute(telefoneBD, tupla_telefoneBD)
            cursor.close()
            db.commit()
            return redirect('/')
    else:
        return render_template('index-cadastro.html')


@app.route('/iniciar', methods = ['GET', 'POST'])
def iniciar(): 
    if request.methods == ['POST']:
        user = request.form['nome']
        senha = request.form['senha']
    
        cursor = mysql.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM Usuario WHERE nome ='{user}'")
        cursor.execute(f"SELECT * FROM Usuario WHERE senha ='{senha}'")
        pessoaExiste = cursor.fetchall()

        if pessoaExiste:
            login_user(user)
            flash('Login bem-sucedido!')
            return redirect(url_for('/'))
        else:
            flash('Usuário ou senha incorretos.')

    return render_template('index-iniciar.html')

@app.route('/carrinho', methods = ['GET', 'POST'])
def carrinho():
    return render_template('index-carrinho.html')

if __name__ == "__main__":
    app.run(debug = True)