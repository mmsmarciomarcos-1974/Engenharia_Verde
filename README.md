# 🍃 Engenharia Verde - Análise de Consumo Energético (UTFPR)

Este repositório contém os códigos-fonte em Python desenvolvidos para a disciplina de **Engenharia Verde** da UTFPR.

## 🎯 Objetivo

O principal objetivo destes scripts é analisar, medir e estimar o consumo energético (ou o uso de CPU como um proxy) de diferentes algoritmos e tarefas computacionais. A ideia é aplicar os conceitos de "Green IT" (TI Verde) para entender o impacto do software no consumo de recursos.

## 🐍 Scripts Principais

Os arquivos neste repositório são usados para executar testes e gerar visualizações:

### 1. Testes de Algoritmos

Scripts focados em medir o custo computacional de algoritmos específicos, conhecidos por sua intensidade:

* `cpu_estimada_fibonacci`: Estima o consumo de CPU/energia ao calcular a sequência de Fibonacci.
* `cpu_estimada_numeros_primos`: Estima o consumo ao encontrar números primos.

### 2. Testes Gerais e Visualização

Scripts para testes de medição de energia e para a geração de gráficos a partir dos dados coletados:

* `teste-energia.py` / `teste-energia1.py`: Scripts principais para realizar os testes de consumo energético.
* `cpu_estimada_grafico.py` (e variações): Scripts utilizados para gerar gráficos e visualizações dos resultados obtidos nos testes.

### 3. Outros

* `aula182.py`: Script de apoio ou exemplo utilizado durante a disciplina.

## 💡 Como Utilizar

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/mmsmarciomarcos-1974/Engenharia_verde.git](https://github.com/mmsmarciomarcos-1974/Engenharia_verde.git)
    cd Engenharia_verde
    ```

2.  **Instale as dependências** (Você pode precisar listar quais são, como `pandas`, `matplotlib`, `codecarbon`, etc.):
    ```bash
    pip install -r requirements.txt
    ```
    *(Nota: Se você não tiver um `requirements.txt`, pode remover esta seção ou listar as bibliotecas manualmente).*

3.  **Execute um script de teste:**
    ```bash
    python teste-energia.py
    ```

    GIT em atualização, conforme disponibilidade
