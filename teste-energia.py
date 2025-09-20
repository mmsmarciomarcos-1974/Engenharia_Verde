import time, psutil, os, csv
from datetime import datetime
import pyRAPL

# Configuração do pyRAPL
pyRAPL.setup()  # Inicializa o medidor
meter = pyRAPL.Measurement('stress_energy')  # Cria medição

print("=== Iniciando teste de stress (300x) com medição de energia ===")

arquivo_csv = "log_stress_energy.csv"

# Cria arquivo CSV com cabeçalho
with open(arquivo_csv, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Rodada", "Hora", "PID", "Nome", "Usuário", "CPU%", "Memória%", 
        "Energia_CPU_J", "Energia_DRAM_J", "Energia_Total_J"
    ])

hora_inicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
cpu_before = psutil.cpu_percent(interval=1)
mem_before = psutil.virtual_memory().percent
t_start = time.time()

for rodada in range(1, 301):
    # Inicia medição de energia
    meter.begin()

    # Loop de stress
    soma = sum(i**2 for i in range(10**6))

    # Finaliza medição
    meter.end()

    energia_cpu = meter.result.pkg  # Energia da CPU em Joules
    energia_dram = meter.result.dram  # Energia da RAM em Joules
    energia_total = energia_cpu + energia_dram

    if rodada % 50 == 0:
        hora_exec = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n--- Rodada {rodada} concluída ---")
        print(f"Soma = {soma}")
        print(f"Energia consumida: CPU={energia_cpu:.2f}J | DRAM={energia_dram:.2f}J | Total={energia_total:.2f}J")
        print("Processos ativos (top 5 por uso de CPU):")

        processos = sorted(
            psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']),
            key=lambda p: p.info['cpu_percent'],
            reverse=True
        )

        with open(arquivo_csv, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for proc in processos[:5]:
                linha = [
                    rodada, hora_exec, proc.info['pid'], proc.info['name'],
                    proc.info['username'], proc.info['cpu_percent'],
                    round(proc.info['memory_percent'], 2),
                    energia_cpu, energia_dram, energia_total
                ]
                writer.writerow(linha)

                print(f"PID={proc.info['pid']} | Nome={proc.info['name']} | "
                      f"Usuário={proc.info['username']} | "
                      f"CPU={proc.info['cpu_percent']}% | "
                      f"Memória={proc.info['memory_percent']:.2f}%")

t_end = time.time()
hora_fim = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
cpu_after = psutil.cpu_percent(interval=1)
mem_after = psutil.virtual_memory().percent

print("\n=== Resultado final ===")
print(f"Hora inicial: {hora_inicio}")
print(f"Hora final:   {hora_fim}")
print(f"Tempo total: {t_end - t_start:.2f} segundos")
print(f"Uso de CPU antes: {cpu_before}% | depois: {cpu_after}%")
print(f"Uso de Memória antes: {mem_before}% | depois: {mem_after}%")
print(f"\n📁 Log salvo em: {os.path.abspath(arquivo_csv)}")
