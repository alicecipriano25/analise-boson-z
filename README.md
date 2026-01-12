# Análise Estatística - Limites de Exclusão do $Z'$

Este repositório contém os dados e scripts utilizados para a análise estatística e definição de limites de exclusão para um bóson elétricamente neutro $Z'$, utilizando dados de sinal e de ruído de fundo correspondentes ao espectro de massa invariante do par elétron-pósitron publicado pelo experimento ATLAS para colisões próton–próton a uma energia de centro de massa de $\sqrt{s}=13$ TeV durante o Run 2 do Grande Colisor de Hádrons, com luminosidade integrada de $139 \,\textnormal{fb}^{-1}$. A análise faz parte da monografia "Busca por um bóson neutro utilizando dados do experimento ATLAS/LHC".

**Obs.:** Durante o desenvolvimento do trabalho, a constante de acoplamento entre o $Z'$ e os férmions foi definida como $\eta$. Após o fim da análise, ela passou a ser definida como $g'$, para não haver confusão com a pseudorapidez.

## Conteúdo do Repositório

### 1. Dados (`all_binning_normalized_with_bkg.csv`)
Arquivo CSV contendo os histogramas de massa invariante utilizados na análise. As colunas incluem:
* **Mass (GeV):** Centro do bin de massa.
* **Background:** Estimativa do fundo esperado de acordo com processos do Modelo Padrão.
* **Data:** Dados observados.
* **mass_zprime_...:** Distribuições de sinal para diferentes massas de $Z'$ e diferentes acoplamentos ($\eta = 0.01$ e $\eta = 0.03$).

### 2. Scripts de Processamento (`.py`)
Os scripts realizam o cálculo do limite de exclusão usando a biblioteca `pyhf`. Eles estão divididos por faixas de massa e acoplamento para otimização do tempo de processamento:

* `adjust_scan_test_01_...`: Scripts para o acoplamento $\eta = 0.01$.
* `adjust_scan_test_03_...`: Scripts para o acoplamento $\eta = 0.03$.

## Metodologia

A análise utiliza o motor estatístico `pyhf` para realizar testes de hipótese baseados em um modelo de fundo não correlacionado (`uncorrelated_background`). 

### Pseudo-experimentos (Toys)
Para cada ponto de massa, foram realizados 500 pseudo-experimentos para determinar as distribuições da estatística de teste. 
* **Otimização de Amplitudes:** Foram utilizados limites (bounds) de busca de sinal distintos para diferentes massas. Essa escolha foi baseada em testes prévios, garantindo que o intervalo de variação do parâmetro de intensidade de sinal ($\mu$) fosse adequado para capturar o limite de 95% de C.L. em cada região.

### Pré-requisitos
São necessárias as seguintes bibliotecas instaladas:
```bash
pip install numpy pandas pyhf
