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
* `leitura-consumo-p`: Leitura de um arquivo no formato CSV que tem dados de consumo energético e ao mesmo tempo mede o seu consumo, contendo os pacotes Python.
* `leitura-consumo-m`: Leitura de um arquivo no formato CSV que tem dados de consumo energético e ao mesmo tempo mede o seu consumo, via código-fonte sem pacotes auxiliares.
* `gerador_massa`: Gera dados ficticios dos programas acima (Leitura-consumo-p e Leitura-consumo-m), utilizando o pacote Faker, protegendo dados sensiveis, pensando na LGPD.


### 2. Testes Gerais e Visualização

Scripts para testes de medição de energia e para a geração de gráficos a partir dos dados coletados:

* `teste-energia.py` / `teste-energia1.py`: Scripts principais para realizar os testes de consumo energético.
* `cpu_estimada_grafico.py` (e variações): Scripts utilizados para gerar gráficos e visualizações dos resultados obtidos nos testes.

### 3. Outros

* `aula182.py`: Programa aleatorio de exemplo, NÃO necessariamente relacionado a Disciplina.


    GIT em atualização, conforme disponibilidade
