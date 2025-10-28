import pandas as pd
import os
import random
from datetime import datetime, timedelta
from codecarbon import track_emissions  # Importa a biblioteca de medição

#NOME_ARQUIVO_CSV = 'dados_consumo_grande.csv'
NOME_ARQUIVO_CSV = 'massa_dados_600k.csv'
# ---------------------------------------------------------------------
# FUNÇÃO 1: GERAR UMA CARGA DE TRABALHO (CSV GRANDE)
# Vamos medir quanta energia gastamos para gerar esses dados.
# ---------------------------------------------------------------------
@track_emissions(project_name="geracao_csv_verde")
def gerar_csv_grande(linhas=1_000_000):
    """
    Gera um arquivo CSV grande para simular uma carga de trabalho real.
    """
    print(f"[+] Gerando arquivo '{NOME_ARQUIVO_CSV}' com {linhas:,} linhas...")
    dispositivos = ['servidor_01', 'servidor_02', 'ar_cond_01', 'iluminacao_bloco_A', 'workstation_dev']
    data_inicial = datetime(2025, 1, 1)
    
    # 'w' (write) para criar o arquivo
    with open(NOME_ARQUIVO_CSV, 'w', newline='', encoding='utf-8') as f:
        # Escreve o cabeçalho
        f.write("timestamp,id_dispositivo,consumo_Wh\n")
        
        # Gera as linhas de dados
        for i in range(linhas):
            ts = data_inicial + timedelta(hours=i)
            disp = random.choice(dispositivos)
            consumo = random.randint(50, 3000) # Consumo aleatório
            f.write(f"{ts},{disp},{consumo}\n")
            
    print("[+] Arquivo CSV grande gerado com sucesso.")

# ---------------------------------------------------------------------
# FUNÇÃO 2: ANÁLISE DE DADOS (NOSSO SCRIPT ORIGINAL)
# Vamos medir quanta energia gastamos para analisar os dados.
# ---------------------------------------------------------------------
@track_emissions(project_name="analise_csv_verde")
def analisar_consumo_energetico(caminho_csv):
    """
    Lê um CSV de consumo de energia e realiza uma análise 
    focada em Engenharia Verde.
    """
    try:
        print(f"\n--- Iniciando Análise de Eficiência Energética ---")
        
        # Etapa 1: Leitura do arquivo CSV (esta é a parte mais pesada)
        print(f"Lendo e processando o arquivo '{caminho_csv}'...")
        df = pd.read_csv(caminho_csv, parse_dates=['timestamp'])

        # Etapa 2: Cálculo do Consumo Total
        consumo_total_wh = df['consumo_Wh'].sum()
        consumo_total_kwh = consumo_total_wh / 1000
        
        print(f"\n[+] Consumo Total Registrado: {consumo_total_kwh:,.2f} kWh")

        # Etapa 3: Identificar Principais Consumidores
        print("Analisando consumo por dispositivo...")
        consumo_por_dispositivo = df.groupby('id_dispositivo')['consumo_Wh'].sum().sort_values(ascending=False)
        
        print("\n[+] Consumo por Dispositivo (Wh):")
        print(consumo_por_dispositivo.head()) # .head() para não poluir
        
        dispositivo_maior_consumo = consumo_por_dispositivo.idxmax()
        print(f"  -> ALERTA: O maior consumidor é '{dispositivo_maior_consumo}'")

        print("\n--- Análise Concluída ---")
        return df

    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em '{caminho_csv}'")
        return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return None

# --- Execução Principal do Script ---
if __name__ == "__main__":
    
    # 1. Gera o arquivo grande (apenas se ele não existir)
    if not os.path.exists(NOME_ARQUIVO_CSV):
        gerar_csv_grande()
    
    # 2. Executa a análise (será medida pelo CodeCarbon)
    analisar_consumo_energetico(NOME_ARQUIVO_CSV)