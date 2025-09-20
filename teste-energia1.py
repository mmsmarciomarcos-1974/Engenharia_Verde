import time, psutil, os, csv
from datetime import datetime

print(f"=== Iniciando teste de stress (3000x) ===")

arquivo_csv = "log_stress_estimada.csv"

# Cria arquivo CSV com cabeçalho
with open(arquivo_csv, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Rodada", "Hora", "PID", "Nome", "Usuário", "CPU%", "Memória%", "Energia_Estimada_W"
    ])

hora_inicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
cpu_before = psutil.cpu_percent(interval=1)
mem_before = psutil.virtual_memory().percent
t_start = time.time()

# Fator de energia aproximado (W por % de CPU)
CPU_POWER_WATTS = 65  # ajuste para sua CPU

for rodada in range(1, 3001):
    # Loop de stress
    soma = sum(i**2 for i in range(10**6))

    # A cada 50 rodadas
    if rodada % 50 == 0:
        hora_exec = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n--- Rodada {rodada} concluída ---")
        print(f"Soma = {soma}")
        
        processos = sorted(
            psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']),
            key=lambda p: p.info['cpu_percent'],
            reverse=True
        )

        with open(arquivo_csv, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for proc in processos[:5]:
                energia_estimada = (proc.info['cpu_percent']/100) * CPU_POWER_WATTS
                linha = [
                    rodada, hora_exec, proc.info['pid'], proc.info['name'],
                    proc.info['username'], proc.info['cpu_percent'],
                    round(proc.info['memory_percent'], 2),
                    round(energia_estimada, 2)
                ]
                writer.writerow(linha)

                print(f"PID={proc.info['pid']} | Nome={proc.info['name']} | "
                      f"Usuário={proc.info['username']} | "
                      f"CPU={proc.info['cpu_percent']}% | "
                      f"Memória={proc.info['memory_percent']:.2f}% | "
                      f"Energia Estimada={energia_estimada:.2f}W")

t_end = time.time()
hora_fim = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
cpu_after = psutil.cpu_percent(interval=1)
mem_after = psutil.virtual_memory().percent

print(f"=== Iniciando teste de stress (3000x) ===")
print("\n=== Resultado final ===")
print(f"Hora inicial: {hora_inicio}")
print(f"Hora final:   {hora_fim}")
print(f"Tempo total: {t_end - t_start:.2f} segundos")
print(f"Uso de CPU antes: {cpu_before}% | depois: {cpu_after}%")
print(f"Uso de Memória antes: {mem_before}% | depois: {mem_after}%")
print(f"\n📁 Log salvo em: {os.path.abspath(arquivo_csv)}")
