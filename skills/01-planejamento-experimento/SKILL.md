---
name: planejamento-experimento
description: Ajuda a planejar experimentos agroflorestais antes de ir a campo ou ao viveiro - escolher entre DIC, DBC, fatorial e parcela subdividida, definir número de repetições, sortear o croqui casualizado e montar a planilha de coleta. Use quando o usuário disser que vai montar, desenhar ou instalar um experimento, ou perguntar quantas repetições usar.
---

# Planejamento de Experimentos

## Quando usar
O experimento ainda não foi instalado, ou o usuário quer revisar o desenho antes de coletar dados. Um bom planejamento evita análises impossíveis depois.

## Antes de analisar, pergunte
1. Qual a pergunta da pesquisa? (ex.: "Qual substrato produz mudas de ipê mais altas?")
2. Quais os tratamentos? São um fator ou mais de um? Cada fator é **qualitativo** (tipos) ou **quantitativo** (doses, % de sombra)?
3. Qual a variável resposta e a unidade? (altura cm, produtividade sc/ha)
4. O local é **homogêneo** (viveiro, casa de vegetação) ou **heterogêneo** (declive, mancha de solo, borda de mata, idade do SAF)?
5. Quantas parcelas cabem (área, mudas, mão de obra)?
6. Algum fator é difícil de aplicar em parcelas pequenas (sombreamento, irrigação, preparo de solo)?

## Passo a passo
### 1. Escolher o delineamento
| Situação | Delineamento |
|---|---|
| Ambiente homogêneo (viveiro, bancada) | **DIC** (inteiramente casualizado) |
| Há uma fonte de variação conhecida no campo (declive, solo, linha de árvores) | **DBC** (blocos casualizados): cada bloco recebe todos os tratamentos |
| Dois ou mais fatores e interesse na interação (espécie × adubação) | **Fatorial** (em DIC ou DBC) |
| Um fator exige parcelas grandes (sombra, irrigação) e outro cabe em parcelas menores (cultivar) | **Parcela subdividida**: fator difícil na parcela, fator fácil na subparcela |

Blocos devem ser formados **perpendiculares** ao gradiente (ex.: faixas em nível no declive).

### 2. Número de repetições
Regra prática: o **GL do resíduo deve ser ≥ 10–12**.
- DIC: GL resíduo = t × (r − 1)
- DBC: GL resíduo = (t − 1) × (r − 1)
- Fatorial DIC a × b: GL resíduo = a × b × (r − 1)
(t = nº de tratamentos, r = repetições ou blocos)

Exemplos: 5 substratos em DIC com 4 repetições → 5 × 3 = 15 ✔. 5 cultivares em DBC com 4 blocos → 4 × 3 = 12 ✔. 3 tratamentos em DBC com 3 blocos → 2 × 2 = 4 ✘ (aumente para 6–7 blocos). Nunca use menos de 3 repetições. Se a variável varia muito (contagem de pragas, sobrevivência), use mais.

### 3. Croqui casualizado
Sorteie a posição dos tratamentos (nunca escolha "a olho").
- DIC: sorteio de todas as parcelas juntas.
- DBC: sorteio separado **dentro de cada bloco**.
- Parcela subdividida: sorteia o fator da parcela no bloco e depois o da subparcela dentro de cada parcela.
Mostre o croqui como tabela (linhas = blocos, colunas = posições) e numere as parcelas.

### 4. Planilha modelo (formato longo: 1 linha = 1 parcela)
| parcela | bloco | especie | adubacao | repeticao | altura_cm | obs |
|---|---|---|---|---|---|---|
| 1 | 1 | angico | organico | 1 | | |
| 2 | 1 | aroeira | sem_adubo | 1 | | |

Regras: nomes de colunas sem acento e sem espaço (use _), unidade no nome (altura_cm), um tipo de dado por coluna, mesma grafia sempre ("organico", não "Orgânico"), célula vazia para dado perdido (não 0), ponto decimal ao salvar CSV.

## Código de referência
R (agricolae) para sortear o croqui:
```r
library(agricolae)
trt <- c("terra", "terra_areia", "terra_esterco", "composto_organico", "comercial")
dic <- design.crd(trt, r = 4, seed = 123)$book      # DIC
dbc <- design.rcbd(trt, r = 4, seed = 123)$book     # DBC (r = blocos)
sombra <- c("0", "30", "50"); cultivar <- c("Arara", "Catuai_144", "Topazio")
ps  <- design.split(sombra, cultivar, r = 4, design = "rcbd", seed = 123)$book
write.csv(dbc, "croqui_dbc.csv", row.names = FALSE)
```
Python:
```python
import random, pandas as pd
random.seed(123)
trt = ["terra","terra_areia","terra_esterco","composto_organico","comercial"]
linhas = []
for b in range(1, 5):
    ordem = random.sample(trt, len(trt))
    for pos, t in enumerate(ordem, 1):
        linhas.append({"bloco": b, "posicao": pos, "tratamento": t})
pd.DataFrame(linhas).to_csv("croqui_dbc.csv", index=False)
```

## Formato da resposta
1. Delineamento recomendado e o porquê (2–3 frases).
2. Tabela de tratamentos e cálculo do GL do resíduo.
3. Croqui sorteado (tabela) + a semente usada para repetir o sorteio.
4. Planilha modelo pronta para copiar.
5. Como será a análise depois (ex.: "ANOVA em DBC + Tukey"; "regressão para as doses").
6. Lista de cuidados para o campo.

## Erros comuns (avise o usuário)
- **Pseudorrepetição**: medir 10 plantas da mesma parcela não são 10 repetições; a repetição é a parcela (use a média das plantas).
- Tratamentos lado a lado sem sorteio (ex.: todas as testemunhas na borda).
- Blocos com tamanhos diferentes ou faltando tratamento.
- Poucas repetições (GL resíduo < 10).
- Doses sem testemunha (dose 0) ou com só 2–3 níveis: para regressão use ≥ 4 níveis.
- Sem bordadura entre parcelas (efeito de vizinhança, sombra de árvores do SAF).
- Mudar o protocolo no meio do experimento sem anotar.

## Regras de segurança
- Não invente dados de área ou de variabilidade; pergunte.
- Se executar o sorteio, mostre o código e a semente; se não puder executar, diga isso e entregue o código.
- Explique cada termo (bloco, parcela, repetição) em linguagem simples.
- Quando houver dúvida séria de desenho, recomende validar com um(a) estatístico(a) ou orientador(a).
