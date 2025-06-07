# database/db.py

import sqlite3
import os

DATABASE_FILE = 'invest_platform.sqlite' # Nome do seu arquivo de banco de dados SQLite
SCHEMA_FILE = os.path.join(os.path.dirname(__file__), 'schema.sql') # Caminho para o schema.sql

def get_db_connection():
    """
    Estabelece e retorna uma conexão com o banco de dados SQLite.
    Cria o arquivo de banco de dados se não existir.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row # Permite acessar colunas como dicionário (row['column_name'])
    return conn

def init_db():
    """
    Inicializa o banco de dados, criando as tabelas conforme definido em schema.sql.
    """
    print(f"Inicializando banco de dados em: {DATABASE_FILE}")
    conn = get_db_connection()
    cursor = conn.cursor()

    with open(SCHEMA_FILE, 'r') as f:
        schema = f.read()

    cursor.executescript(schema)
    conn.commit()
    conn.close()
    print("Banco de dados inicializado com sucesso!")

def execute_query(query, params=()):
    """
    Executa uma consulta SQL genérica (INSERT, UPDATE, DELETE) no banco de dados.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid # Retorna o ID da última linha inserida, útil para INSERT
    except sqlite3.Error as e:
        print(f"Erro ao executar query: {e}")
        conn.rollback() # Desfaz a operação em caso de erro
        return None
    finally:
        conn.close()

def fetch_all(query, params=()):
    """
    Executa uma consulta SQL e retorna todas as linhas como objetos Row.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao buscar todos: {e}")
        return []
    finally:
        conn.close()

def fetch_one(query, params=()):
    """
    Executa uma consulta SQL e retorna a primeira linha como um objeto Row.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Erro ao buscar um: {e}")
        return None
    finally:
        conn.close()

# Exemplo de uso (pode ser removido depois ou movido para um script de teste)
if __name__ == '__main__':
    # Este bloco será executado apenas quando você rodar 'python db.py' diretamente
    # CUIDADO: Rodar init_db() recria as tabelas (apagando dados existentes, se houver)
    # Para o MVP, é útil para resetar o banco de dados.

    # Você pode querer comentar ou adicionar uma confirmação para esta linha em produção
    init_db()

    # Exemplo: Adicionar um usuário
    user_id = execute_query("INSERT INTO users (username) VALUES (?)", ("TesteUser",))
    if user_id:
        print(f"Usuário 'TesteUser' adicionado com ID: {user_id}")

    # Exemplo: Buscar usuários
    users = fetch_all("SELECT * FROM users")
    print("\nUsuários no DB:")
    for user in users:
        print(f"ID: {user['id']}, Username: {user['username']}")

    # Exemplo: Adicionar um ativo
    asset_id = execute_query("INSERT INTO assets (ticker, name, sector) VALUES (?, ?, ?)",
                             ("XPTO11.SA", "Fundo XPTO", "Fundos Imobiliários"))
    if asset_id:
        print(f"Ativo 'XPTO11.SA' adicionado com ID: {asset_id}")

    # Exemplo: Buscar um ativo
    xpto = fetch_one("SELECT * FROM assets WHERE ticker = ?", ("XPTO11.SA",))
    if xpto:
        print(f"\nAtivo encontrado: {xpto['name']} ({xpto['ticker']})")
