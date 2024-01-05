from flask import Flask, render_template, request, redirect, url_for, flash
from mundobibble import create_app
from flask_mysqldb import MySQL
import mysql.connector
from flask_login import login_user
from flask_hashing import Hashing

app = create_app()

# Configurações do banco de dados

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='labinfo',
    database='MundoLiterario'
)

hashing = Hashing(app)

# Inicialização do MySQL
mysql = MySQL()
mysql.init_app(app)

@app.route('/', methods = ['GET', 'POST'])
def home():
    cursor = db.cursor(dictionary=True)
    select = "SELECT * FROM Livro"
    cursor.execute(select)
    livros = cursor.fetchall()
    print(livros)
    
    select = "SELECT * FROM IMG"
    cursor.execute(select)
    imgs = cursor.fetchall()
    print(livros)
    print("==========")
    print(imgs)
    return render_template('index.html', livros = livros, imgs = imgs)
    
@app.route('/livro')
def livro():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Livro")
    data = cursor.fetchall()
    cursor.close()
    return render_template('index-produtos.html', livros=data)

@app.route('/autor/<name>')
def autor(name):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM autor WHERE {name}")
    data = cursor.fetchall()
    cursor.close()
    return str(data)


@app.route('/cadastro-fornecedor', methods = ['GET','POST'])
def cadastroFornecedor():
    if request.method == 'POST':
        nome = request.form['name']
        cnpj = request.form['cnpj']
        email = request.form['email']
        senha = request.form['password']
        
        hashed_password = hashing.hash_value(senha)
        hashed_password = hashed_password[:16]
        
        cursor = db.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM Fornecedor WHERE cnpj='{cnpj}'")
        check_fornecedorExiste = cursor.fetchall()
        
        if check_fornecedorExiste:
            raise Exception("Esse cnpj já está cadastrado!")
        else:
            post_fornecedor = "INSERT INTO Fornecedor (cnpj, nome, senha, email) VALUES (%s, %s, %s, %s)"
            
            tupla_fornecedorInfo = (cnpj, nome, hashed_password, email)
            
            cursor.execute(post_fornecedor, tupla_fornecedorInfo)
            cursor.close()
            db.commit()
            return render_template("abafornecedor.html")
    else:
        return render_template("fornecedor.html")

@app.route('/cadastro', methods = ['GET','POST'])
def cadastro():
    if request.method == 'POST':

        nome = request.form['name']
        email = request.form['email']
        telefone = request.form['telephone']
        senha = request.form['password']

        hashed_password = hashing.hash_value(senha)
        hashed_password = hashed_password[:16]
        
        cursor = db.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM Usuario WHERE email='{email}'")
        check_pessoa_existe = cursor.fetchall()
        
        if check_pessoa_existe:
            return ("Este email já foi cadastrado!")
        else:
            userBD = "INSERT INTO Usuario (nome, senha, email) VALUES (%s, %s, %s)"
            
            tupla_user= (nome, senha, email)
            
            cursor.execute(userBD, tupla_user)
            cursor.close()
            db.commit()
            
            cursor = db.cursor(dictionary=True)
            selectUserID = (f"SELECT UsuarioID FROM Usuario WHERE email='{email}'")
            cursor.execute(selectUserID)
            fetch_IDuser = cursor.fetchall()
            fetch_IDuser[0]['UsuarioID']
            
            telefoneBD = "INSERT INTO Telefone (Telefone1, CodUsuario) VALUES (%s, %s)"
            
            tupla_telefoneBD = (telefone, fetch_IDuser[0]['UsuarioID'])
            cursor.execute(telefoneBD, tupla_telefoneBD)
            cursor.close()
            db.commit()
            return render_template('index.html')
    else:
        return render_template('index-cadastro.html')


@app.route('/iniciar', methods = ['GET', 'POST'])
def iniciar(): 
    if request.method == ['POST']:
        user = request.form['nome']
        senha = request.form['senha']
    
        cursor = mysql.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM Usuario WHERE nome ='{user}'")
        cursor.execute(f"SELECT * FROM Usuario WHERE senha ='{senha}'")
        pessoaExiste = cursor.fetchall()

        if pessoaExiste:
            return render_template('index.html')
        else:
            flash('Usuário ou senha incorretos.')
    return render_template('index.html')

@app.route('/carrinho', methods = ['GET', 'POST'])
def carrinho():
    return render_template('index-carrinho.html')

@app.route('/cadastrarProduto', methods=['GET','POST'])
def cadastrando():
    nome = request.form['nomeLivro']
    dataDPubli = request.form['data']
    preco = request.form['preco']
    quant = request.form['quantidade']
    a = request.files['arq']

    extensao = a.filename.rsplit('.',1)[1]

    caminho = f'mundobibble/static/imgs/{nome}.{extensao}'
    a.save(caminho)
        
    caminhoBD = f'../static/imgs/{nome}.{extensao}'
        
    cursor = db.cursor(dictionary=True)

    sql = ("INSERT INTO Livro (nome, dataDPubli, preco) VALUES (%s, %s, %s)")

    tupla = (nome, dataDPubli, preco)
    cursor.execute(sql, tupla)
    cursor.close()
    db.commit()

    cursor = db.cursor(dictionary=True)
    select = (f"SELECT LivroID FROM Livro WHERE nome='{nome}'")
    cursor.execute(select)
    fetchdata = cursor.fetchall()
        
    sql = ("INSERT INTO Estoque (quantiEstoque, CodFornecedor, LivroID) VALUES (%s, %s, %s)")
        
    tupla = (int(quant), 1, fetchdata[0]['LivroID'])
    cursor.execute(sql, tupla)
        
    sql2 = ("INSERT INTO IMG (caminho, CodLivro) VALUES (%s, %s)")

    tupla2 = (caminhoBD, fetchdata[0]['LivroID'])
        
    cursor.execute(sql2, tupla2)
    cursor.close()
    db.commit()

    return render_template('abafornecedor.html')

@app.route('/buscar', methods = ['POST'])
def buscar():
    resposta = request.form['pesquisa']

    cursor = db.cursor(dictionary=True)

    select = (f"SELECT nome, preco FROM Livro WHERE nome LIKE '%{resposta}%'")
    cursor.execute(select)
    fetchdata = cursor.fetchone()
    print(fetchdata)

    cursor.reset()

    #cursor = db.cursor(dictionary=True)


    select2 = ("SELECT caminho FROM IMG INNER JOIN Livro ON CodLivro = LivroID")

    print('cheguei')
    cursor.execute(select2)
    fetchdata2 = cursor.fetchone()
    print(fetchdata2)

    if (cursor.rowcount>0):
        return render_template('index-produtos.html', busca= fetchdata)
    else:
        return render_template('index-produtos.html', busca='Item não encontrado')


if __name__ == "__main__":
    app.run(debug = True)