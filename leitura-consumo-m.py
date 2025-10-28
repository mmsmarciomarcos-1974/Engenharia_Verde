import csv
import os
import random
from datetime import datetime, timedelta
import time  # Módulo embutido para medir o tempo
import tracemalloc # Módulo embutido para medir a memória

#NOME_ARQUIVO_CSV = 'dados_consumo_grande.csv'
NOME_ARQUIVO_CSV = 'massa_dados_600k.csv'
LINHAS_PARA_GERAR = 1_000_000 # 1 milhão de linhas

# ---------------------------------------------------------------------
# FUNÇÃO 1: GERAR UMA CARGA DE TRABALHO (CSV GRANDE)
# (Usando o módulo 'csv' embutido)
# ---------------------------------------------------------------------
def gerar_csv_grande():
    """
    Gera um arquivo CSV grande para simular uma carga de trabalho real.
    """
    print(f"[+] Gerando arquivo '{NOME_ARQUIVO_CSV}' com {LINHAS_PARA_GERAR:,} linhas...")
    dispositivos = ['servidor_01', 'servidor_02', 'ar_cond_01', 'iluminacao_bloco_A', 'workstation_dev']
    data_inicial = datetime(2025, 1, 1)
    
    try:
        with open(NOME_ARQUIVO_CSV, 'w', newline='', encoding='utf-8') as f:
            # Cria um "escritor" CSV
            writer = csv.writer(f)
            
            # Escreve o cabeçalho
            writer.writerow(["timestamp", "id_dispositivo", "consumo_Wh"])
            
            # Gera as linhas de dados
            for i in range(LINHAS_PARA_GERAR):
                ts = data_inicial + timedelta(hours=i)
                disp = random.choice(dispositivos)
                consumo = random.randint(50, 3000)
                writer.writerow([ts, disp, consumo])
                
        print("[+] Arquivo CSV grande gerado com sucesso.")
        
    except IOError as e:
        print(f"Erro ao escrever o arquivo: {e}")

# ---------------------------------------------------------------------
# FUNÇÃO 2: ANÁLISE DE DADOS (CÓDIGO PURO)
# (Usando o módulo 'csv' embutido e dicionários)
# ---------------------------------------------------------------------
def analisar_consumo_energetico_puro(caminho_csv):
    """
    Lê um CSV de consumo de energia e realiza uma análise 
    focada em Engenharia Verde, usando apenas código Python puro.
    """
    print(f"\n--- Iniciando Análise Pura (sem Pandas) ---")
    
    try:
        with open(caminho_csv, 'r', encoding='utf-8') as f:
            # Cria um "leitor" CSV
            leitor = csv.reader(f)
            
            # Pula o cabeçalho
            cabeçalho = next(leitor)
            
            # Variáveis para armazenar nossos resultados
            consumo_total_wh = 0
            consumo_por_dispositivo = {} # Dicionário para agrupar
            pico_consumo_wh = 0
            linha_pico = []

            print("Processando linhas do CSV...")
            
            # Itera linha por linha (eficiente em memória!)
            for linha in leitor:
                # O leitor CSV retorna uma lista de strings
                dispositivo = linha[1]
                consumo = int(linha[2]) # Converte string para inteiro

                # Etapa 2: Cálculo do Consumo Total
                consumo_total_wh += consumo

                # Etapa 3: Identificar Principais Consumidores
                # Adiciona ao dicionário, somando se já existir
                consumo_por_dispositivo[dispositivo] = consumo_por_dispositivo.get(dispositivo, 0) + consumo
                
                # Etapa 4: Identificar Pico de Consumo
                if consumo > pico_consumo_wh:
                    pico_consumo_wh = consumo
                    linha_pico = linha

            # --- Análise Concluída ---
            print("\n[+] Análise Concluída.")

            # Exibindo resultados
            consumo_total_kwh = consumo_total_wh / 1000
            print(f"[+] Consumo Total Registrado: {consumo_total_kwh:,.2f} kWh")

            # Encontra o dispositivo com maior consumo no dicionário
            dispositivo_maior_consumo = max(consumo_por_dispositivo, key=consumo_por_dispositivo.get)
            print(f"[+] ALERTA: O maior consumidor é '{dispositivo_maior_consumo}'")
            # print("Consumo por Dispositivo (Wh):", consumo_por_dispositivo) # (Opcional)

            print("\n[+] Pico de Consumo Individual Registrado:")
            print(f"  -> Dispositivo: {linha_pico[1]}")
            print(f"  -> Horário: {linha_pico[0]}")
            print(f"  -> Consumo: {pico_consumo_wh} Wh")

    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em '{caminho_csv}'")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

# --- Execução Principal do Script ---
if __name__ == "__main__":
    
    # 1. Gera o arquivo grande (apenas se ele não existir)
    if not os.path.exists(NOME_ARQUIVO_CSV):
        gerar_csv_grande(LINHAS_PARA_GERAR)
    
    # 2. Executa a análise, medindo o desempenho
    
    print("\n========================================================")
    print("      MEDINDO DESEMPENHO DA ANÁLISE EM CÓDIGO PURO      ")
    print("========================================================")

    # Inicia o monitoramento de memória
    tracemalloc.start()

    # Registra o tempo de início
    start_time = time.perf_counter()

    # *** EXECUTA A FUNÇÃO DE ANÁLISE ***
    analisar_consumo_energetico_puro(NOME_ARQUIVO_CSV)

    # Registra o tempo de fim
    end_time = time.perf_counter()
    
    # Pega os dados de memória (atual e pico)
    memoria_atual, memoria_pico = tracemalloc.get_traced_memory()
    
    # Para o monitoramento de memória
    tracemalloc.stop()

    # --- RELATÓRIO DE ENGENHARIA VERDE ---
    print("\n--- Relatório de Recursos (Engenharia Verde) ---")
    print(f"Tempo de Execução (CPU): {end_time - start_time:.4f} segundos")
    print(f"Pico de Uso de Memória (RAM): {memoria_pico / 1024**2:.2f} MB")
    print("========================================================")