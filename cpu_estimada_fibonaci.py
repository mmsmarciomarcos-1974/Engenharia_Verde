import time, psutil, os, csv
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import sys
sys.set_int_max_str_digits(0)

print(f"=== Iniciando teste de Fibonacci (300x) ===")

# Função para calcular a sequência de Fibonacci até N termos
def fibonacci(n):
    seq = [0, 1]
    for _ in range(2, n):
        seq.append(seq[-1] + seq[-2])
    return seq

# --- Arquivo CSV com timestamp ---
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
arquivo_csv = f"log_fibonacci_{timestamp}.csv"

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
energia_media_processos_grafico = [[] for _ in range(5)]

cores_processos = ['purple', 'blue', 'green', 'orange', 'red']

# --- Inicializa gráficos em tempo real ---
plt.ion()
fig, axes = plt.subplots(1, 4, figsize=(24, 5))

# --- Loop principal ---
for rodada in range(1, 200):
    # Stress com Fibonacci (30 mil termos)
    fib_seq = fibonacci(30000)
    ultimo_valor = fib_seq[-1]

    if rodada % 50 == 0:
        hora_exec = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n--- Rodada {rodada} concluída --- Último Fibonacci={ultimo_valor}")

        processos = sorted(
            psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']),
            key=lambda p: p.info['cpu_percent'],
            reverse=True
        )

        with open(arquivo_csv, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            energia_rodada = 0
            cpu_total = 0

            for idx, proc in enumerate(processos[:5]):
                energia_estimada = (proc.info['cpu_percent']/100) * CPU_POWER_WATTS
                energia_rodada += energia_estimada
                cpu_total += proc.info['cpu_percent']

                energia_media_processos_grafico[idx].append(energia_estimada)

                writer.writerow([
                    rodada, hora_exec, proc.info['pid'], proc.info['name'],
                    proc.info['username'], proc.info['cpu_percent'],
                    round(proc.info['memory_percent'], 2),
                    round(energia_estimada, 2)
                ])

                print(f"PID={proc.info['pid']} | Nome={proc.info['name']} | "
                      f"CPU={proc.info['cpu_percent']}% | Memória={proc.info['memory_percent']:.2f}% | "
                      f"Energia_Estimada={energia_estimada:.2f}W")

            energia_total_acumulada += energia_rodada
            rodadas_grafico.append(rodada)
            energia_acumulada_grafico.append(energia_total_acumulada)
            energia_por_rodada_grafico.append(energia_rodada)
            cpu_medio = cpu_total / 5
            cpu_medio_grafico.append(cpu_medio)

            print(f"💡 Energia acumulada total até agora: {energia_total_acumulada:.2f}W")

            # --- Atualiza gráficos ---
            axes[0].cla()
            axes[0].plot(rodadas_grafico, energia_acumulada_grafico, marker='o', color='orange', label='Acumulada')
            z = np.polyfit(rodadas_grafico, energia_acumulada_grafico, 1)
            p = np.poly1d(z)
            axes[0].plot(rodadas_grafico, p(rodadas_grafico), "r--", label='Tendência')
            axes[0].set_title('Energia Acumulada por Rodada')
            axes[0].set_xlabel('Rodada')
            axes[0].set_ylabel('Energia Acumulada (W)')
            axes[0].grid(True)
            axes[0].legend()

            axes[1].cla()
            axes[1].bar(rodadas_grafico, energia_por_rodada_grafico, color='skyblue')
            axes[1].set_title('Energia por Rodada')
            axes[1].set_xlabel('Rodada')
            axes[1].set_ylabel('Energia (W)')
            axes[1].grid(True)

            axes[2].cla()
            axes[2].scatter(cpu_medio_grafico, energia_por_rodada_grafico, color='green')
            axes[2].set_title('Energia vs CPU Médio (top 5)')
            axes[2].set_xlabel('CPU Médio (%)')
            axes[2].set_ylabel('Energia por Rodada (W)')
            axes[2].grid(True)

            axes[3].cla()
            for idx in range(5):
                axes[3].plot(rodadas_grafico, energia_media_processos_grafico[idx], marker='o',
                             color=cores_processos[idx], label=f'Top {idx+1}')
            axes[3].set_title('Energia de cada Processo (top 5)')
            axes[3].set_xlabel('Rodada')
            axes[3].set_ylabel('Energia (W)')
            axes[3].grid(True)
            axes[3].legend()

            plt.tight_layout()
            plt.pause(0.1)

# --- Fim ---
t_end = time.time()
hora_fim = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
cpu_after = psutil.cpu_percent(interval=1)
mem_after = psutil.virtual_memory().percent

plt.ioff()
plt.show()

print(f"=== Finalizando teste de Fibonacci (300x) ===")
print("\n=== Resultado final ===")
print(f"Hora inicial: {hora_inicio}")
print(f"Hora final: {hora_fim}")
print(f"Tempo total: {t_end - t_start:.2f} segundos")
print(f"Uso de CPU antes: {cpu_before}% | depois: {cpu_after}%")
print(f"Uso de Memória antes: {mem_before}% | depois: {mem_after}%")
print(f"Energia total acumulada aproximada: {energia_total_acumulada:.2f}W")
print(f"\n📁 Log salvo em: {os.path.abspath(arquivo_csv)}")
