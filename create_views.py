from sqlalchemy import create_engine, text

db_string = "postgresql://postgres:Joe102030!@localhost:5432/postgres"
engine = create_engine(db_string)

sql_commands = """
DROP VIEW IF EXISTS avg_temp_por_dispositivo CASCADE;
DROP VIEW IF EXISTS leituras_por_hora CASCADE;
DROP VIEW IF EXISTS temp_max_min_por_dia CASCADE;
DROP VIEW IF EXISTS temp_por_local_dia CASCADE;
DROP VIEW IF EXISTS avg_temp_por_local CASCADE;
DROP VIEW IF EXISTS temp_com_status CASCADE;
DROP VIEW IF EXISTS avg_temp_por_mes CASCADE;

CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
SELECT device_id, AVG(temperature) AS avg_temp
FROM temperature_readings
GROUP BY device_id;

CREATE OR REPLACE VIEW leituras_por_hora AS
SELECT EXTRACT(HOUR FROM timestamp) AS hora, COUNT(*) AS contagem
FROM temperature_readings
GROUP BY hora
ORDER BY hora;

CREATE OR REPLACE VIEW temp_max_min_por_dia AS
SELECT DATE(timestamp) AS data, MAX(temperature) AS temp_max, MIN(temperature) AS temp_min
FROM temperature_readings
GROUP BY data
ORDER BY data;

CREATE OR REPLACE VIEW temp_por_local_dia AS
SELECT
    DATE(timestamp) AS data,
    location,
    AVG(temperature) AS avg_temp_diaria,
    MAX(temperature) AS max_temp_diaria,
    MIN(temperature) AS min_temp_diaria
FROM temperature_readings
GROUP BY data, location
ORDER BY data, location;

CREATE OR REPLACE VIEW avg_temp_por_local AS
SELECT location, AVG(temperature) AS avg_temp_geral
FROM temperature_readings
GROUP BY location;

CREATE OR REPLACE VIEW temp_com_status AS
SELECT
    device_id,
    timestamp,
    temperature,
    CASE
        WHEN temperature >= 54 THEN 'Perigo Extremo'
        WHEN temperature >= 41 THEN 'Perigo'
        WHEN temperature >= 32 THEN 'Cautela Extrema'
        WHEN temperature >= 27 THEN 'Cautela'
        ELSE 'Normal'
    END AS status
FROM temperature_readings;

-- NOVA VIEW: Média de temperatura por mês
CREATE OR REPLACE VIEW avg_temp_por_mes AS
SELECT
    EXTRACT(MONTH FROM timestamp) AS mes,
    AVG(temperature) AS avg_temp
FROM temperature_readings
GROUP BY mes
ORDER BY mes;
"""

def create_views():
    try:
        print("Conectando ao banco de dados, excluindo e recriando as views...")
        with engine.begin() as connection:
            connection.execute(text(sql_commands))
        print("Views SQL criadas com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro ao criar as views: {e}")

if __name__ == "__main__":
    create_views()