import os  # Módulo para interagir com o sistema, para ler as variáveis de ambientes
import json # Módulo nativo que lê e grava arquivos no formato json
from datetime import datetime # Importa a ferramente datetime para conseguirmos a data e hora exata do computador no momento da execução
from dotenv import load_dotenv # Importa a função responsável por procurar o arquivo .env na pasta do projeto e carregar o conteúdo dele para a memória do Pyhton
import spotipy  # Importa a biblioteca que facilita a comunicação com a API do Spotify
from spotipy.oauth2 import SpotifyOAuth # Importa o "porteiro" de autenticação, validando o ID e Secret, sem abrir uma janela no navegador e fazer login

# Carrega as credenciais do arquivo .env
load_dotenv()

# Autentica e inicializa o cliente da API di Spotify
auth_manager = SpotifyOAuth( scope="user-read-recently-played", 
    client_id = os.getenv("SPOTIFY_CLIENT_ID"), # Busca as chave ID 'invisível' no .env
    client_secret= os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri= os.getenv("SPOTIFY_REDIRECT_URL")
)
sp = spotipy.Spotify(auth_manager=auth_manager)

dados_brutos = sp.current_user_recently_played( 
    limit=50 # Máximo de musicas que a API entrega por busca
)

data_atual = datetime.now().strftime("%Y-%m-%d_%H-%M") # Pega a data e hora atual para distinguir o nome do arquivo quando for feita a extração

caminho_arquivo = f"data/bronze/spotify_tracks_{data_atual}.json" # Local onde o arquivo será salvo

with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
    json.dump(
        dados_brutos,
        arquivo,
        ensure_ascii=False,
        indent=4
    )
print(f"O arquivo foi salvo em {caminho_arquivo}")