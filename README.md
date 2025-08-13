
# 🌡️ Pipeline de Dados Futurista com IoT e Docker

## 🚀 Visão Geral do Projeto

Este projeto demonstra a construção de um pipeline de dados completo para processar e visualizar leituras de temperatura de dispositivos IoT. Utilizando tecnologias modernas como **Docker**, **PostgreSQL** e **Python**, o objetivo é transformar dados brutos de sensores em insights acionáveis, apresentados em um dashboard interativo e com design futurista construído com **Streamlit** e **Plotly**.

O projeto segue um fluxo de trabalho (pipeline) robusto e automatizado:
1.  **Ingestão:** Lê um arquivo CSV com dados de sensores de temperatura.
2.  **Armazenamento:** Salva os dados em um banco de dados PostgreSQL executado em um contêiner Docker.
3.  **Processamento:** Cria views SQL para pré-agregar os dados e facilitar a análise.
4.  **Visualização:** Apresenta os resultados em um dashboard web interativo.

## 🛠️ Tecnologias Utilizadas

* **Python**: Linguagem principal para desenvolvimento dos scripts de ingestão e dashboard.
* **Pandas**: Para a manipulação e processamento dos dados do CSV.
* **SQLAlchemy**: Para a conexão e comunicação com o banco de dados PostgreSQL.
* **Docker**: Para gerenciar o contêiner do PostgreSQL de forma isolada e portátil.
* **PostgreSQL**: Banco de dados relacional para armazenamento dos dados.
* **Streamlit**: Framework para a construção do dashboard web de forma rápida e intuitiva.
* **Plotly Express**: Para a criação de gráficos interativos e visualmente atraentes.

## 📂 Estrutura do Projeto

.
├── data/
│   └── temperature_readings.csv
├── create_views.py
├── dashboard.py
├── drop_views.py
├── ingestao.py
└── README.md


## ⚙️ Passo a Passo para Execução

Siga os passos abaixo para configurar e executar o pipeline completo em sua máquina.

### 1. Pré-requisitos
* [**Docker**](https://docs.docker.com/get-docker/) instalado e em execução.
* [**Python 3.x**](https://www.python.org/downloads/) instalado.
* [**Git**](https://git-scm.com/downloads) instalado.

### 2. Configuração do Ambiente
1.  Clone este repositório para o seu ambiente local:
    ```bash
    git clone [URL_DO_SEU_REPOSITORIO]
    cd [pasta_do_projeto]
    ```

2.  Crie e ative um ambiente virtual Python:
    ```bash
    python -m venv venv
    # No Windows
    .\venv\Scripts\activate
    # No macOS/Linux
    source venv/bin/activate
    ```

3.  Instale as bibliotecas necessárias:
    ```bash
    pip install pandas psycopg2-binary sqlalchemy streamlit plotly
    ```

### 3. Executando o Pipeline

O pipeline deve ser executado em uma sequência específica para garantir que as dependências do banco de dados sejam respeitadas.

1.  **Rode o contêiner do PostgreSQL:**
    ```bash
    docker run --name postgres-iot -e POSTGRES_PASSWORD=SUASENHA! -p 5432:5432 -d postgres
    ```

2.  **Execute o pipeline na ordem correta:**
    ```bash
    # Primeiro, limpe as views antigas (evita erros de dependência)
    python drop_views.py

    # Segundo, ingira os dados e recrie a tabela
    python ingestao.py

    # Terceiro, crie as views para a análise
    python create_views.py

    # Por fim, inicie o dashboard
    streamlit run dashboard.py
    ```

O dashboard será aberto no seu navegador, pronto para ser explorado.

## 📊 Análise e Visualizações

O dashboard foi projetado para responder às perguntas-chave levantadas no dataset.

* **Métricas Globais:** Respondem à pergunta "Qual foi a temperatura máxima e mínima registrada?".
* **Gráfico de Linhas (Tendência):** Mostra a relação entre as temperaturas interna e externa ao longo do tempo, ajudando a identificar a tendência.
* **Box Plot (Variação):** Visualiza a variação da temperatura entre os ambientes interno e externo, identificando a dispersão dos dados.
* **Análise Mensal (Gráfico de Barras):** Responde à pergunta "Qual foi o mês mais quente/frio?" mostrando a temperatura média de cada mês.
* **Índice de Calor:** Apresenta uma tabela de referência que contextualiza os dados de temperatura com o nível de desconforto humano, transformando os dados brutos em informações úteis.

## 🖼️ Visualização do Dashboard
<img src="images/Metricas.png" alt="Métricas Globais" width="600">
<img src="images/Comparativa.png" alt="Comparativa Interno vs Externo" width="600">
<img src="images/Variacao.png" alt="Variação de Temperatura por ambiente " width="600">
<img src="images/Mensal.png" alt="Análise Mensal" width="600">

## 📚 Fonte dos Dados

Este projeto utiliza o conjunto de dados **"Temperature Readings: IoT Devices"**, disponível no Kaggle.

* **Link**: [https://www.kaggle.com/datasets/atulanandjha/temperature-readings-iot-devices](https://www.kaggle.com/datasets/atulanandjha/temperature-readings-iot-devices)

---
Feito por Joe Allan Zirn.