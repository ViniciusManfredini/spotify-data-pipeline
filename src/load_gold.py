import duckdb

# 1. Conecta (ou cria) o banco de dados analítico local da camada Gold
con = duckdb.connect("data/gold/spotify_analytics.duckdb")

# 2. Tabela Dimensão (dim_musicas): consolida o catálogo único de faixas
# e aplica regra de negócio para categorizar a duração das músicas
con.execute(""" CREATE OR REPLACE TABLE dim_musicas AS SELECT DISTINCT
            track_id,
            track_name,
            artist_name,
            album_name,
            release_date,
            duration_min,
            CASE 
            WHEN duration_min < 2.5 THEN 'Curta'
            WHEN duration_min <= 4.0 THEN 'Média'
            ELSE 'Longa'
            END AS categoria_duracao

            FROM 'data/silver/spotify_tracks.parquet' """
            )


# 3. Tabela Fato (fato_reproducoes): registra a granularidade de cada evento
# individual de reprodução, convertendo o texto ISO 8601 para TIMESTAMP real
con.execute("""CREATE OR REPLACE TABLE fato_reproducoes AS SELECT 
            track_id,  
            CAST(played_at AS TIMESTAMP) AS played_at  
            FROM 'data/silver/spotify_tracks.parquet'  """
             )


# 4. Tabela Agregada (gold_resumo_artistas): cruza Fato e Dimensão (Star Schema)
# para entregar o ranking de artistas pronto para consumo em ferramentas de BI
con.execute("""CREATE OR REPLACE TABLE gold_resumo_artistas AS SELECT 
            d.artist_name,  
            COUNT(f.played_at) AS total_reproducao 
            FROM fato_reproducoes f    
            JOIN dim_musicas d 
            ON f.track_id = d.track_id
            GROUP BY d.artist_name
            ORDER BY total_reproducao DESC
              """
             )

# 5. Validação rápida das tabelas geradas no terminal e encerramento seguro da conexão
print(con.execute("SELECT * FROM dim_musicas").df())
print(con.execute("SELECT * FROM fato_reproducoes").df())
print(con.execute("SELECT * FROM gold_resumo_artistas").df())

con.close()