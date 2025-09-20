import time, psutil, os, csv
from datetime import datetime
import matplotlib.pyplot as plt

print("=== Iniciando teste de stress (300x) ===")

# Data e hora atual para nome do arquivo
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
arquivo_csv = f"log_stress_{timestamp}.csv"

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

CPU_POWER_WATTS = 65  # ajuste conforme a sua CPU
energia_total_acumulada = 0

# Para gráfico
rodadas_grafico = []
energia_grafico = []

for rodada in range(1, 301):
    # Loop de stress
    soma = sum(i**2 for i in range(10**6))

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
            energia_rodada = 0

            for proc in processos[:5]:
                energia_estimada = (proc.info['cpu_percent']/100) * CPU_POWER_WATTS
                energia_rodada += energia_estimada

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

            energia_total_acumulada += energia_rodada
            print(f"💡 Energia acumulada aproximada até agora: {energia_total_acumulada:.2f}W")

            # Para gráfico
            rodadas_grafico.append(rodada)
            energia_grafico.append(energia_total_acumulada)

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
print(f"Energia total acumulada aproximada: {energia_total_acumulada:.2f}W")
print(f"\n📁 Log salvo em: {os.path.abspath(arquivo_csv)}")

# --- Gráfico da energia acumulada ---
plt.figure(figsize=(10, 5))
plt.plot(rodadas_grafico, energia_grafico, marker='o', color='orange')
plt.title('Energia Estimada Acumulada por Rodada')
plt.xlabel('Rodada')
plt.ylabel('Energia Acumulada (W)')
plt.grid(True)
plt.tight_layout()
plt.show()
