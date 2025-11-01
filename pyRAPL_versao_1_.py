import time
import os
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Importa a biblioteca pyRAPL
try:
    from pyRAPL import setup, measure, Result
except ImportError:
    print("Erro: Biblioteca pyRAPL não encontrada.")
    print("Por favor, instale com: pip install pyRAPL pandas matplotlib")
    exit()

# --- Configuração do Experimento ---
NUM_EXECUCOES = 40       # N=X execuções (conforme documento)
DUMMY_CSV_PATH = "dados_pessoas_ficticias.csv"
DUMMY_CSV_ROWS = 10000   # Volume de dados para a tarefa

# --- Tarefa 1: Implementação "Python Puro" ---
@measure(domains=['pkg'])
def tarefa_python_puro(csv_path):
    """
    Executa a Tarefa 1: Ler CSV com 'csv', iterar e 'imprimir'.
    O 'print' foi comentado para não poluir o console 40x.
    """
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # print(f"Puro: {row['id']}, {row['nome']}")
            pass # Apenas iteramos para simular a carga

# --- Tarefa 2: Implementação "Pandas" ---
@measure(domains=['pkg'])
def tarefa_pandas(csv_path):
    """
    Executa a Tarefa 2: Ler CSV com 'pandas', iterar e 'imprimir'.
    O 'print' foi comentado.
    """
    df = pd.read_csv(csv_path)
    for index, row in df.iterrows():
        # print(f"Pandas: {row['id']}, {row['nome']}")
        pass # Apenas iteramos para simular a carga

# --- Tarefa 3: Medição de Baseline (Overhead) ---
@measure(domains=['pkg'])
def tarefa_overhead():
    """
    Executa uma tarefa nula para medir o custo (overhead)
    da própria ferramenta pyRAPL e do script.
    """
    pass

# --- Função Utilitária ---
def create_dummy_csv(filepath, num_rows):
    """
    Cria um arquivo CSV fictício para o experimento.
    """
    print(f"Gerando arquivo de dados fictício em: {filepath} ({num_rows} linhas)")
    with open(filepath, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "nome", "email"])
        for i in range(1, num_rows + 1):
            writer.writerow([i, f"Pessoa {i}", f"pessoa{i}@email.com"])

# --- Orquestrador Principal do Experimento ---
if __name__ == "__main__":
    
    # 1. Configura o pyRAPL
    try:
        setup(domains=['pkg'])
    except Exception as e:
        print(f"\nERRO AO INICIAR O pyRAPL: {e}")
        print("Isso geralmente acontece por falta de permissão (rode com 'sudo')")
        print("ou hardware incompatível (ex: VM ou CPU não-Intel sem RAPL).")
        exit()

    # 2. Gera os dados de entrada
    create_dummy_csv(DUMMY_CSV_PATH, DUMMY_CSV_ROWS)

    # 3. Inicializa listas para coletar os dados
    resultados_puro = []    # (energia_j, tempo_s)
    resultados_pandas = []  # (energia_j, tempo_s)
    resultados_overhead = []# (energia_j)

    print(f"\nIniciando orquestração: {NUM_EXECUCOES} execuções de cada tarefa...")
    
    # 4. Loop de Execução (N=X)
    for i in range(NUM_EXECUCOES):
        print(f"Iniciando execução {i+1}/{NUM_EXECUCOES}...")
        
        # Mede Overhead
        res_oh = tarefa_overhead()
        resultados_overhead.append(res_oh.energy('pkg') / 1_000_000) # uJ para J

        # Mede Python Puro
        res_puro = tarefa_python_puro(DUMMY_CSV_PATH)
        energia_j_puro = res_puro.energy('pkg') / 1_000_000
        tempo_s_puro = res_puro.duration / 1_000_000 # us para s
        resultados_puro.append((energia_j_puro, tempo_s_puro))

        # Mede Pandas
        res_pandas = tarefa_pandas(DUMMY_CSV_PATH)
        energia_j_pandas = res_pandas.energy('pkg') / 1_000_000
        tempo_s_pandas = res_pandas.duration / 1_000_000
        resultados_pandas.append((energia_j_pandas, tempo_s_pandas))

    print("\nExecuções concluídas. Gerando análise e artefatos...")

    # 5. Análise dos Resultados
    
    # Calcula médias de energia (em Joules)
    energia_puro_raw = [r[0] for r in resultados_puro]
    energia_pandas_raw = [r[0] for r in resultados_pandas]
    
    avg_overhead_j = np.mean(resultados_overhead)
    # Subtrai o overhead para isolar o consumo real da tarefa
    avg_puro_j = np.mean(energia_puro_raw) - avg_overhead_j
    avg_pandas_j = np.mean(energia_pandas_raw) - avg_overhead_j
    
    # Calcula médias de tempo (em Segundos)
    tempo_puro_s = [r[1] for r in resultados_puro]
    tempo_pandas_s = [r[1] for r in resultados_pandas]
    avg_puro_s = np.mean(tempo_puro_s)
    avg_pandas_s = np.mean(tempo_pandas_s)

    # 6. Gerar Artefatos (Saídas do Documento)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # --- Artefato 1: Tabela de Resultados (impresso no console) ---
    print("\n---")
    print("## 4. Resultados da Execução (Dados Finais)")
    print(f"(Baseado em N={NUM_EXECUCOES} execuções)")
    print(f"Baseline de Overhead (custo do script): {avg_overhead_j:.4f} J por medição\n")
    
    print("| Implementação | Consumo Médio de Energia (J) | Tempo Médio de Execução (s) |")
    print("| :--- | :--- | :--- |")
    print(f"| Python Puro   | {avg_puro_j:.4f} J               | {avg_puro_s:.4f} s                |")
    print(f"| Pandas        | {avg_pandas_j:.4f} J               | {avg_pandas_s:.4f} s                |")
    print("---\n")

    # --- Artefato 2: Log de Dados Brutos (CSV) ---
    csv_log_path = f"log_resultados_brutos_{timestamp}.csv"
    with open(csv_log_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "Execucao_N", 
            "Energia_Puro_J_raw", "Tempo_Puro_s", 
            "Energia_Pandas_J_raw", "Tempo_Pandas_s", 
            "Energia_Overhead_J"
        ])
        for i in range(NUM_EXECUCOES):
            writer.writerow([
                i+1, 
                energia_puro_raw[i], tempo_puro_s[i],
                energia_pandas_raw[i], tempo_pandas_s[i],
                resultados_overhead[i]
            ])
    print(f"✅ Dados brutos salvos em: {os.path.abspath(csv_log_path)}")

    # --- Artefato 3: Gráfico Comparativo (PNG) ---
    # (Um boxplot é tecnicamente mais adequado para mostrar a variação)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Gráfico de Energia (com overhead subtraído)
    energia_puro_corrigida = [e - avg_overhead_j for e in energia_puro_raw]
    energia_pandas_corrigida = [e - avg_overhead_j for e in energia_pandas_raw]
    
    ax1.boxplot([energia_puro_corrigida, energia_pandas_corrigida], 
                labels=['Python Puro', 'Pandas'])
    ax1.set_title(f'Consumo de Energia (N={NUM_EXECUCOES} execuções)')
    ax1.set_ylabel('Energia Corrigida (Joules)')
    ax1.grid(True, linestyle='--', alpha=0.6)

    # Gráfico de Tempo
    ax2.boxplot([tempo_puro_s, tempo_pandas_s], 
                labels=['Python Puro', 'Pandas'])
    ax2.set_title(f'Tempo de Execução (N={NUM_EXECUCOES} execuções)')
    ax2.set_ylabel('Tempo (Segundos)')
    ax2.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    grafico_path = f"grafico_comparativo_{timestamp}.png"
    plt.savefig(grafico_path)
    print(f"✅ Gráfico comparativo salvo em: {os.path.abspath(grafico_path)}")
    print("\nExperimento concluído com sucesso.")