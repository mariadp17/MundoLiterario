use MundoLiterario;

#ALTER TABLE Estoque ADD CONSTRAINT fk_Livro foreign key (LivroID) references Livro(LivroID);

CREATE TABLE IMG(
	CodImg INT auto_increment NOT NULL,
	caminho VARCHAR(500) NOT NULL,
    CodLivro INT NOT NULL,
    primary key (CodImg),
    foreign key (CodLivro) references Livro(LivroID)
);
