import time, psutil, os, csv
from datetime import datetime
import matplotlib.pyplot as plt

print("=== Iniciando teste de stress (300x) ===")

# Arquivo CSV com timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
arquivo_csv = f"log_stress_{timestamp}.csv"

with open(arquivo_csv, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Rodada", "Hora", "PID", "Nome", "Usuário", "CPU%", "Memória%", "Energia_Estimada_W"
    ])

hora_inicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
cpu_before = psutil.cpu_percent(interval=1)
mem_before = psutil.virtual_memory().percent
t_start = time.time()

CPU_POWER_WATTS = 65  # ajuste conforme sua CPU
energia_total_acumulada = 0

rodadas_grafico = []
energia_acumulada_grafico = []
energia_por_rodada_grafico = []
cpu_medio_grafico = []

for rodada in range(1, 301):
    # Stress
    soma = sum(i**2 for i in range(10**6))

    if rodada % 50 == 0:
        hora_exec = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n--- Rodada {rodada} concluída --- Soma={soma}")

        processos = sorted(
            psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']),
            key=lambda p: p.info['cpu_percent'],
            reverse=True
        )

        with open(arquivo_csv, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            energia_rodada = 0
            cpu_total = 0

            for proc in processos[:5]:
                energia_estimada = (proc.info['cpu_percent']/100) * CPU_POWER_WATTS
                energia_rodada += energia_estimada
                cpu_total += proc.info['cpu_percent']

                writer.writerow([
                    rodada, hora_exec, proc.info['pid'], proc.info['name'],
                    proc.info['username'], proc.info['cpu_percent'],
                    round(proc.info['memory_percent'], 2),
                    round(energia_estimada, 2)
                ])

                print(f"PID={proc.info['pid']} | Nome={proc.info['name']} | "
                      f"CPU={proc.info['cpu_percent']}% | Memória={proc.info['memory_percent']:.2f}% | "
                      f"Energia={energia_estimada:.2f}W")

            energia_total_acumulada += energia_rodada
            rodadas_grafico.append(rodada)
            energia_acumulada_grafico.append(energia_total_acumulada)
            energia_por_rodada_grafico.append(energia_rodada)
            cpu_medio_grafico.append(cpu_total / 5)  # média top 5 CPU

t_end = time.time()
hora_fim = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
cpu_after = psutil.cpu_percent(interval=1)
mem_after = psutil.virtual_memory().percent

print("\n=== Resultado final ===")
print(f"Hora inicial: {hora_inicio}")
print(f"Hora final: {hora_fim}")
print(f"Tempo total: {t_end - t_start:.2f} segundos")
print(f"Uso de CPU antes: {cpu_before}% | depois: {cpu_after}%")
print(f"Uso de Memória antes: {mem_before}% | depois: {mem_after}%")
print(f"Energia total acumulada aproximada: {energia_total_acumulada:.2f}W")
print(f"\n📁 Log salvo em: {os.path.abspath(arquivo_csv)}")

# --- Gráficos ---
plt.figure(figsize=(12, 4))
plt.plot(rodadas_grafico, energia_acumulada_grafico, marker='o', color='orange')
plt.title('Energia Acumulada por Rodada')
plt.xlabel('Rodada')
plt.ylabel('Energia Acumulada (W)')
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 4))
plt.bar(rodadas_grafico, energia_por_rodada_grafico, color='skyblue')
plt.title('Energia por Rodada (não acumulada)')
plt.xlabel('Rodada')
plt.ylabel('Energia (W)')
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 4))
plt.scatter(cpu_medio_grafico, energia_por_rodada_grafico, color='green')
plt.title('Energia vs CPU Médio (top 5 processos)')
plt.xlabel('CPU Médio (%)')
plt.ylabel('Energia por Rodada (W)')
plt.grid(True)
plt.tight_layout()
plt.show()
