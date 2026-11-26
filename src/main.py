import subprocess
import time
import sys


# Executa um script individual do pipeline, garantindo o uso do interpretador ativo e interrompendo a
# execução caso ocorra qualquer erro.
def executar_etapa(nome_etapa, caminho_script): 
    print(f"\n --- Iniciando: {nome_etapa} ---") 
    # sys.executable assegura que os subprocessos rodem dentro do mesmo .venv
    subprocess.run([sys.executable, caminho_script], check=True)

if __name__ == "__main__":

    # Registra o timestamp inicial para medir a performance total do pipeline
    inicio = time.time()

    # Orquestração sequencial das camadas Bronze -> Silver -> Gold
    executar_etapa("1. Extração (Bronze)", "src/extract.py")
    executar_etapa("2. Transformação (Silver)", "src/transform.py")
    executar_etapa("3. Carga Analitica (Gold)", "src/load_gold.py")

    # Calcula e exibe o tempo total de execução de ponta a ponta
    tempo_total = round(time.time() - inicio, 2)

    print(f" O Pipeline conclui com sucesso em {tempo_total} segundos")