import json
import glob
import pandas as pd
from datetime import datetime

# 1. Mapeia e ordena cronologicamente todos os snapshots JSON da camada Bronze
arquivos_bronze = sorted(glob.glob("data/bronze/*.json"))

lista_musicas = []

# 2. Consolidação incremental: percorre todos os arquivos históricos capturados
for caminho in arquivos_bronze:
    with open(caminho, "r", encoding="utf-8") as arquivo:
        dados_brutos = json.load(arquivo)
        # 3. Desaninha (flattening) a estrutura JSON da API do Spotify para formato tabular
        for itens in dados_brutos["items"]:
            musica = {
                "track_id"     : itens["track"]["id"],
                "track_name"   : itens["track"]["name"],
                "artist_name"  : itens["track"]["artists"][0]["name"],
                "album_name"   : itens["track"]["album"]["name"],
                "release_date" : itens["track"]["album"]["release_date"],
                "duration_ms"  : itens["track"]["duration_ms"],
                "popularity"   : itens["track"].get("popularity"),
                "played_at"    : itens["played_at"]
            }
            lista_musicas.append(musica)

# 4. Transformações, enriquecimento e controle de qualidade no DataFrame
df = pd.DataFrame(lista_musicas)

# Converte a duração de milissegundos para minutos com 2 casas decimais
df['duration_min'] = (df['duration_ms'] / 60000).round(2)

# Deduplicação por chave composta: mantém replays da mesma música em horários distintos,
# mas elimina eventos repetidos capturados em extrações sobrepostas
df = df.drop_duplicates(subset=["track_id", "played_at"])

# Adiciona metadado de auditoria indicando quando o registro foi processado
df['processed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 5. Persiste a camada Silver em formato colunar Parquet (sem o índice do Pandas)
df.to_parquet("data/silver/spotify_tracks.parquet", index=False)

print(f" O arquivo foi salvo")