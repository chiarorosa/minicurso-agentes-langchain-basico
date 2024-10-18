import os
import random
import re
import sqlite3
import time

import requests
from bs4 import BeautifulSoup

# URLs base para a paginação e para os livros
URL_BASE = "https://books.toscrape.com/catalogue/page-{}.html"
URL_BOOK = "https://books.toscrape.com/catalogue/{}"


class DatabaseCreator:
    """
    Classe responsável pela criação do banco de dados e das tabelas necessárias.
    """

    def __init__(self, db_name="books.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        """Estabelece a conexão com o banco de dados SQLite."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        """Cria as tabelas 'livros' e 'movimentacoes' se não existirem."""
        # Criando a tabela 'livros' se ainda não existir
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT,
                preco REAL,
                em_estoque TEXT,
                genero TEXT,
                avaliacao TEXT,
                descricao TEXT
            )
            """
        )

        # Criando a tabela 'movimentacoes' se ainda não existir
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS movimentacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                livro_id INTEGER,
                quantidade INTEGER,
                data_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                tipo_movimentacao TEXT,
                FOREIGN KEY(livro_id) REFERENCES livros(id)
            )
            """
        )
        self.conn.commit()

    def close_connection(self):
        """Fecha a conexão com o banco de dados."""
        if self.conn:
            self.conn.close()


class DatabaseHandler:
    """
    Classe responsável por manipular o banco de dados, incluindo inserções e consultas.
    """

    def __init__(self, db_name="books.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def salvar_livro(self, livro):
        """
        Salva um livro na tabela 'livros' e registra uma movimentação de entrada.

        Args:
            livro (dict): Dicionário contendo os detalhes do livro.
        """
        self.cursor.execute(
            """
            INSERT INTO livros (titulo, preco, em_estoque, genero, avaliacao, descricao)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                livro["titulo"],
                livro["preco"],
                livro["em_estoque"],
                livro["genero"],
                livro["avaliacao"],
                livro["descricao"],
            ),
        )
        self.conn.commit()
        livro_id = self.cursor.lastrowid

        # Inserindo movimentação de entrada
        self.cursor.execute(
            """
            INSERT INTO movimentacoes (livro_id, quantidade, tipo_movimentacao)
            VALUES (?, ?, ?)
            """,
            (livro_id, livro["quantitativo"], "entrada"),
        )
        self.conn.commit()

    def obter_todos_ids_livros(self):
        """Retorna uma lista com todos os IDs de livros na tabela 'livros'."""
        self.cursor.execute("SELECT id FROM livros")
        return [row[0] for row in self.cursor.fetchall()]

    def calcular_estoque_atual(self, livro_id):
        """
        Calcula o estoque atual de um livro com base nas movimentações.

        Args:
            livro_id (int): ID do livro.

        Returns:
            int: Quantidade atual em estoque.
        """
        self.cursor.execute(
            """
            SELECT
                (SELECT COALESCE(SUM(quantidade), 0) FROM movimentacoes WHERE livro_id = ? AND tipo_movimentacao = 'entrada') -
                (SELECT COALESCE(SUM(quantidade), 0) FROM movimentacoes WHERE livro_id = ? AND tipo_movimentacao = 'saida')
            """,
            (livro_id, livro_id),
        )
        resultado = self.cursor.fetchone()
        return resultado[0] if resultado else 0

    def registrar_saida(self, livro_id, quantidade_saida):
        """
        Registra uma movimentação de saída para um livro.

        Args:
            livro_id (int): ID do livro.
            quantidade_saida (int): Quantidade a ser retirada do estoque.
        """
        self.cursor.execute(
            """
            INSERT INTO movimentacoes (livro_id, quantidade, tipo_movimentacao)
            VALUES (?, ?, ?)
            """,
            (livro_id, quantidade_saida, "saida"),
        )
        self.conn.commit()

    def close_connection(self):
        """Fecha a conexão com o banco de dados."""
        if self.conn:
            self.conn.close()


def obter_detalhes_do_livro(produto):
    """
    Obtém os detalhes de um livro a partir do elemento HTML do produto.

    Args:
        produto (bs4.element.Tag): Elemento HTML que representa o produto.

    Returns:
        dict or None: Dicionário com os detalhes do livro ou None em caso de erro.
    """
    try:
        livro_url = URL_BOOK.format(produto.select("a")[0]["href"])
        livro_page = requests.get(livro_url)
        soup_livro = BeautifulSoup(livro_page.text, "lxml")

        titulo = soup_livro.select(".product_main h1")[0].text
        preco = soup_livro.select(".price_color")[0].text.split("£")[1]
        estoque_str = soup_livro.select(".instock.availability")[0].text.strip()
        avaliacao = soup_livro.select(".star-rating")[0]["class"][1]
        genero = soup_livro.select(".breadcrumb li")[2].text.strip()

        # Separando "Em estoque" e "Quantitativo"
        if "In stock" in estoque_str:
            em_estoque = "Sim"
            match = re.search(r"\((\d+) available\)", estoque_str)
            if match:
                quantitativo = int(match.group(1))
            else:
                quantitativo = 0
        else:
            em_estoque = "Não"
            quantitativo = 0

        # Checando se a descrição existe
        descricao_elem = soup_livro.select("#product_description ~ p")
        if descricao_elem:
            descricao = descricao_elem[0].text
        else:
            descricao = "Descrição não disponível"

        return {
            "titulo": titulo,
            "preco": float(preco),
            "em_estoque": em_estoque,
            "quantitativo": quantitativo,
            "genero": genero,
            "avaliacao": avaliacao,
            "descricao": descricao,
        }
    except Exception as e:
        print(f"Erro ao obter detalhes do livro: {e}")
        return None


def main():
    # Inicializar e criar o banco de dados
    db_creator = DatabaseCreator()
    db_creator.connect()
    db_creator.create_tables()
    db_creator.close_connection()

    # Inicializar o manipulador do banco de dados
    db_handler = DatabaseHandler()

    # Loop para pegar todos os livros
    livros = []
    for i in range(1, 51):  # Ajuste conforme necessário
        try:
            resultado = requests.get(URL_BASE.format(i))
            resultado.raise_for_status()
        except requests.RequestException as e:
            print(f"Erro ao acessar a página {i}: {e}")
            continue

        soup = BeautifulSoup(resultado.text, "lxml")
        produtos = soup.select(".product_pod")

        for produto in produtos:
            livro = obter_detalhes_do_livro(produto)
            if livro:
                livros.append(livro)
                db_handler.salvar_livro(livro)
                print(f"Livro salvo: {livro['titulo']}")

            # Aguardar um tempo para evitar sobrecarregar o servidor
            time.sleep(0.3)  # 300ms

    print(f"Total de livros coletados e salvos: {len(livros)}")

    # -----------------------------------------------------------------------
    # Gerando saídas aleatórias para 100 livros
    # -----------------------------------------------------------------------

    # Obter todos os IDs de livros disponíveis
    livro_ids = db_handler.obter_todos_ids_livros()

    # Verificar se há pelo menos 100 livros
    quantidade_selecionada = min(100, len(livro_ids))
    if quantidade_selecionada == 0:
        print("Nenhum livro disponível para gerar movimentações de saída.")
    else:
        # Selecionar 100 IDs de livros aleatórios
        livro_ids_selecionados = random.sample(livro_ids, quantidade_selecionada)

        for livro_id in livro_ids_selecionados:
            estoque_atual = db_handler.calcular_estoque_atual(livro_id)

            if estoque_atual > 0:
                # Gerar uma quantidade de saída aleatória que não exceda o estoque atual
                quantidade_saida = random.randint(1, estoque_atual)

                # Inserir movimentação de saída
                db_handler.registrar_saida(livro_id, quantidade_saida)
                print(f"Saída registrada para o livro ID {livro_id}: {quantidade_saida} unidades")
            else:
                print(f"O livro ID {livro_id} não possui estoque disponível para saída.")

    # Fechar a conexão com o banco de dados
    db_handler.close_connection()


if __name__ == "__main__":
    main()
