# 🎵 Spotify Data Pipeline — Arquitetura Medallion

Pipeline completo (end-to-end) de Engenharia de Dados desenvolvido com Python, Spotipy (OAuth 2.0), Pandas, Apache Parquet e DuckDB. O projeto extrai o histórico pessoal de músicas tocadas recentemente na API do Spotify, consolida os eventos de forma incremental e modela um Data Warehouse analítico em formato Star Schema.

## 🏗️ Arquitetura (Medallion)

* **Camada Bronze (`src/extract.py`):** Realiza a autenticação via OAuth 2.0 (escopo `user-read-recently-played`), extrai as últimas 50 reproduções e salva arquivos JSON brutos com carimbo de data e hora em `data/bronze/`.
* **Camada Silver (`src/transform.py`):** Lê de forma incremental todos os arquivos JSON históricos da Bronze, desaninha as estruturas de faixas e artistas, aplica extração resiliente a mudanças de esquema (`.get()`), remove duplicidades usando chave composta (`track_id` + `played_at`) e salva os dados tratados em formato colunar **Parquet** em `data/silver/`.
* **Camada Gold (`src/load_gold.py`):** Consulta os arquivos Parquet diretamente via SQL no **DuckDB** para construir uma Modelagem Dimensional (**Star Schema**) e visões analíticas:
  * `dim_musicas`: Tabela dimensão com o catálogo único de faixas e classificação de duração (`Curta`, `Média`, `Longa`).
  * `fato_reproducoes`: Tabela fato registrando cada evento individual de reprodução (`track_id`, `played_at`).
  * `gold_resumo_artistas`: Tabela agregada com o ranking de artistas por total de reproduções.
* **Orquestração (`src/main.py`):** Ponto único de entrada que executa `extract -> transform -> load_gold` em sequência, medindo o tempo de processamento e interrompendo o fluxo em caso de falha.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Ingestão:** Spotipy (Spotify Web API / OAuth 2.0)
* **Processamento e Armazenamento:** Pandas, PyArrow, Apache Parquet, JSON
* **Banco Analítico e Modelagem:** DuckDB, SQL (Star Schema)

## 🚀 Como Executar o Projeto

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/ViniciusManfredini/spotify-data-pipeline.git
   cd spotify-data-pipeline
    ``` 
2. **Crie e ative o ambiente virtual**
    ```bash
    python -m venv .venv
    # Windows:
    .\.venv\Scripts\activate
    # Linux/macOS:
    source .venv/bin/activate
    ```

3. **Instale as dependências**
     ```bash
    pip install -r requirements.txt
     ```

4. **Configure as variáveis** 
    Crie um arquivo .env na raiz do projeto com as credenciais do seu app no Spotify Developer:
     ```bash
    SPOTIPY_CLIENT_ID=seu_client_id
    SPOTIPY_CLIENT_SECRET=seu_client_secret
    SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
     ```

5. **Execute o pipeline completo** 
     ```bash
    python src/main.py
     ```