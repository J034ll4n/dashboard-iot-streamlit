from sqlalchemy import create_engine, text

# 1. Configuração do Banco de Dados
db_string = "postgresql://postgres:Joe102030!@localhost:5432/postgres"
engine = create_engine(db_string)

# 2. Comandos SQL para DROPAR as views
sql_drop_views = """
DROP VIEW IF EXISTS avg_temp_por_dispositivo CASCADE;
DROP VIEW IF EXISTS leituras_por_hora CASCADE;
DROP VIEW IF EXISTS temp_max_min_por_dia CASCADE;
DROP VIEW IF EXISTS temp_por_local_dia CASCADE;
DROP VIEW IF EXISTS avg_temp_por_local CASCADE;
"""

def drop_views():
    """Conecta ao banco de dados e apaga todas as views."""
    try:
        print("Conectando ao banco de dados e apagando views...")
        with engine.begin() as connection:
            connection.execute(text(sql_drop_views))
        print("Todas as views foram apagadas com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    drop_views()