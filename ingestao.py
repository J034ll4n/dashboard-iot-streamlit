import pandas as pd
from sqlalchemy import create_engine, text
import os

# 1. Configuração do Banco de Dados
db_string = "postgresql://postgres:Joe102030!@localhost:5432/postgres"
engine = create_engine(db_string)

# 2. Caminho do Arquivo
file_path = os.path.join("data", "temperature_readings.csv")

# 3. Lógica de Ingestão de Dados
def ingest_data():
    """
    Lê o arquivo CSV, processa os dados e os insere no PostgreSQL.
    """
    try:
        print("Lendo o arquivo CSV...")
        df = pd.read_csv(file_path)

        print("Ajustando os nomes das colunas...")
        column_mapping = {
            'room_id/id': 'device_id',
            'noted_date': 'timestamp',
            'temp': 'temperature',
            'out/in': 'location'  # Agora incluímos e renomeamos a coluna 'out/in'
        }
        df.rename(columns=column_mapping, inplace=True)
        
        # Agora incluímos a coluna 'location' na seleção
        df = df[['device_id', 'timestamp', 'temperature', 'location']]

        print("Convertendo a coluna de timestamp...")
        df['timestamp'] = pd.to_datetime(df['timestamp'], format="%d-%m-%Y %H:%M")

        with engine.connect() as connection:
            print("Conectando ao banco de dados e inserindo os dados...")
            df.to_sql('temperature_readings', con=connection, if_exists='replace', index=False)
            print("Dados inseridos com sucesso na tabela 'temperature_readings'.")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        print("Certifique-se de ter baixado o arquivo do Kaggle e colocado na pasta 'data'.")
    except Exception as e:
        print(f"Ocorreu um erro durante a ingestão dos dados: {e}")

# 4. Executa a função
if __name__ == "__main__":
    ingest_data()