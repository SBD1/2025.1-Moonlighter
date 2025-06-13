import psycopg2
import os

# EXECUÇÃO DA CONEXÃO COM O BANCO DE DADOS POSTGRESQL DO DOCKER:
def connect_to_db():
    try:
        connection = psycopg2.connect(
            dbname=os.getenv('DB_NAME', 'moonlighter'),
            user=os.getenv('DB_USER', 'moonlighter'),
            password=os.getenv('DB_PASSWORD', 'moonlighter'),
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432')
        )
        return connection
    except Exception as e:
        print(f"Erro na Tentantiva de conexão com o Banco PostgreSQL: {e}")
        return None