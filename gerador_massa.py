import csv
import random
import time # Para medir o tempo de execução

NOME_ARQUIVO = 'massa_dados_600k.csv'
NUMERO_DE_REGISTROS = 600_000

def gerar_codigo_idef_rapido():
    """Gera um CPF mascarado aleatório no formato ***.XXX.XXX-**"""
    # É mais rápido gerar os números de uma vez
    meio = f"{random.randint(100000, 999999)}"
    return f"***.{meio[:3]}.{meio[3:]}-**"

def gerar_telefone_rapido():
    """Gera um telefone celular fictício"""
    ddd = random.randint(11, 99)
    prefixo = f"9{random.randint(8000, 9999)}"
    sufixo = random.randint(1000, 9999)
    return f"({ddd}) {prefixo}-{sufixo}"

# --- Início da Execução ---
print(f"Iniciando a geração de {NUMERO_DE_REGISTROS:,} registros...")
print(f"Isso pode levar alguns segundos. Salvando em '{NOME_ARQUIVO}'...")

# Registra o tempo de início
start_time = time.time()

try:
    with open(NOME_ARQUIVO, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # 1. Escreve o cabeçalho
        writer.writerow(['nome', 'sobrenome', 'codigo-idef', 'telefone', 'email'])
        
        # 2. Gera os registros em um loop otimizado
        for i in range(1, NUMERO_DE_REGISTROS + 1):
            
            # Gera dados únicos baseados no contador (i)
            nome = f"Nome{i}"
            sobrenome = f"Sobrenome{i}"
            email = f"usuario{i}@emailficticio.com"
            
            # Gera dados aleatórios
            codigo_idef = gerar_codigo_idef_rapido()
            telefone = gerar_telefone_rapido()
            
            # Escreve a linha no CSV
            writer.writerow([nome, sobrenome, codigo_idef, telefone, email])
            
            # Mostra o progresso a cada 100.000 registros
            if i % 100_000 == 0:
                print(f"  ... {i:,} registros gerados.")

    # Registra o tempo de fim
    end_time = time.time()
    
    # 3. Relatório Final
    print("\n" + "="*40)
    print(f"[SUCESSO] Arquivo '{NOME_ARQUIVO}' gerado!")
    print(f"Total de Registros: {NUMERO_DE_REGISTROS:,}")
    print(f"Tempo total de execução: {end_time - start_time:.2f} segundos")
    print("="*40)

except IOError as e:
    print(f"Erro de permissão ao escrever o arquivo: {e}")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")