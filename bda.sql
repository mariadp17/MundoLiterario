CREATE DATABASE MundoLiterario;

USE MundoLiterario;

CREATE TABLE Usuario(
UsuarioID INT auto_increment NOT NULL,
nome VARCHAR(100) NOT NULL,
senha VARCHAR(45) NOT NULL,
email VARCHAR(100) NOT NULL,
primary key (UsuarioID)
);

CREATE TABLE Fornecedor(
FornecedorID INT auto_increment NOT NULL,
cnpj VARCHAR(45) NOT NULL,
nome VARCHAR(100) NOT NULL,
senha VARCHAR(45) NOT NULL,
email VARCHAR(100) NOT NULL,
primary key (FornecedorID)
);

CREATE TABLE Endereco(
EnderecoID INT auto_increment NOT NULL,
estado VARCHAR(50) NOT NULL,
cidade VARCHAR(50) NOT NULL,
bairro VARCHAR(45) NOT NULL,
rua VARCHAR(45) NOT NULL,
numeroDaCasa VARCHAR(4),
CodUsuario INT,
CodFornecedor INT,
primary key (EnderecoID),
foreign key (CodUsuario) references Usuario(UsuarioID),
foreign key (CodFornecedor) references Fornecedor(FornecedorID)
);

CREATE TABLE Telefone(
TelefoneID INT auto_increment NOT NULL,
Telefone1 VARCHAR(20) NOT NULL,
Telefone2 VARCHAR(20), 
CodUsuario INT,
CodFornecedor INT,
primary key (TelefoneID),
foreign key (CodUsuario) references Usuario(UsuarioID),
foreign key (CodFornecedor) references Fornecedor(FornecedorID)
);

CREATE TABLE Editora(
EditoraID INT auto_increment NOT NULL,
nome VARCHAR(45) NOT NULL,
email VARCHAR(100) NOT NULL,
telefone VARCHAR(20) NOT NULL,
primary key (EditoraID)
);

CREATE TABLE Autor(
AutorID INT auto_increment NOT NULL,
nome VARCHAR(45) NOT NULL,
primary key (AutorID)
);

CREATE TABLE Categoria(
CategoriaID INT auto_increment NOT NULL,
nome VARCHAR(50) NOT NULL,
primary key (CategoriaID)
);

CREATE TABLE Estoque(
EstoqueID INT auto_increment NOT NULL,
quantiEstoque INT NOT NULL,
CodFornecedor INT,
primary key (EstoqueID),
foreign key (CodFornecedor) references Fornecedor(FornecedorID)
);

CREATE TABLE Livro(
LivroID INT auto_increment NOT NULL,
nome VARCHAR(50) NOT NULL,
dataDPubli INT NOT NULL,
preco INT NOT NULL,
CodAutor INT,
CodEditora INT,
CodCategoria INT,
primary key (LivroID),
foreign key (CodAutor) references Autor(AutorID),
foreign key (CodEditora) references Editora(EditoraID),
foreign key (CodCategoria) references Categoria(CategoriaID)
);

CREATE TABLE Carrinho(
CarrinhoID INT auto_increment NOT NULL,
CodUsuario INT,
primary key (CarrinhoID),
foreign key (CodUsuario) references Usuario(UsuarioID)
);

CREATE TABLE CarrinhoHasPedido(
quantidade INT NOT NULL,
valor FLOAT NOT NULL,
CodLivro INT,
CodCarrinhoID INT,
foreign key (CodLivro) references Livro(LivroID),
foreign key (CodCarrinhoID) references Carrinho(CarrinhoID)
);

CREATE TABLE Compras(
CompraID INT auto_increment NOT NULL,
dataCompra DATE NOT NULL,
CodCarrinhoID INT,
primary key (CompraID),
foreign key (CodCarrinhoID) references Carrinho(CarrinhoID)
);