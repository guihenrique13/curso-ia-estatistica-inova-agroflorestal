---
name: fatorial-parcela-subdividida
description: Analisa experimentos com dois fatores - fatorial (em DIC ou DBC) e parcela subdividida - testando a interação, fazendo o desdobramento quando ela é significativa e usando corretamente os dois erros (erro a e erro b) da parcela subdividida. Use quando os dados tiverem dois fatores cruzados, como espécie × adubação ou sombreamento × cultivar de café.
---

# Fatorial e Parcela Subdividida

## Quando usar
Dois fatores combinados (todas as combinações presentes). **Fatorial**: todas as combinações sorteadas nas parcelas da mesma forma. **Parcela subdividida**: um fator na parcela grande (ex.: % de sombra) e outro na subparcela (ex.: cultivar).

## Antes de analisar, pergunte
1. Delineamento base: DIC ou DBC? É fatorial ou parcela subdividida? (Qual fator foi aplicado em parcelas maiores?)
2. Variável resposta e unidade.
3. Fatores e níveis (ex.: 3 espécies × 3 adubações).
4. Repetições ou blocos.
5. Cada fator é qualitativo (Tukey) ou quantitativo (regressão)?

## Passo a passo
1. **Conferir a estrutura**: nº de linhas = a × b × r; cada combinação com o mesmo nº de repetições; bloco como fator.
2. **Pressupostos** nos resíduos (Shapiro-Wilk; Bartlett/Levene entre as combinações).
3. **ANOVA** com: fator A, fator B, **interação A×B**, resíduo. CV%.
4. **Olhe primeiro a interação A×B**:
   - **Não significativa**: os fatores agem de forma independente. Interprete cada efeito principal (Tukey para qualitativo, regressão para quantitativo).
   - **Significativa**: o efeito de um fator **depende** do nível do outro. **Desdobre** antes de qualquer conclusão: compare A dentro de cada nível de B, e B dentro de cada nível de A. Não interprete os efeitos principais isolados.
5. **Parcela subdividida – dois erros**:
   - **Erro a** (bloco × fator da parcela): testa o fator da parcela.
   - **Erro b** (resíduo): testa o fator da subparcela e a interação.
   - Há dois CVs (CV1 da parcela, CV2 da subparcela). O erro a tem poucos GL e costuma ser maior, por isso o fator da parcela é testado com menos precisão.
   - No desdobramento, comparar a subparcela dentro da parcela usa o erro b; comparar a parcela dentro da subparcela usa um **erro combinado** (Satterthwaite), que o ExpDes.pt calcula sozinho.
6. Fator quantitativo com 3 níveis: a quadrática passa exatamente pelas 3 médias (R² = 1); diga que isso não é "ajuste perfeito", e sim falta de pontos.

## Exemplos resolvidos (para conferência)
**Fatorial 3×3 em DIC – espécie × adubação, massa seca (g)** (fatorial_adubacao.csv, 4 rep.): interação F = 15,71; p < 0,001 → desdobrar. CV = 8,55%; GL res = 27; Shapiro p = 0,50.
| Espécie | mineral | organico | sem_adubo |
|---|---|---|---|
| mogno_africano | 33,60 aA | 28,33 aB | 20,23 aC |
| angico | 23,43 bA | 26,03 aA | 16,03 bB |
| aroeira | 15,58 cA | 17,13 bA | 15,48 bA |
Minúsculas: espécies na coluna; maiúsculas: adubações na linha (Tukey 5%). A aroeira não respondeu à adubação (p = 0,39).

**Parcela subdividida em DBC – sombreamento (parcela: 0, 30, 50%) × cultivar de café (subparcela), sc/ha** (parcela_sub_cafe_sombra.csv, 4 blocos): sombreamento F = 6,48; p = 0,032 (erro a, GL 6); cultivar F = 78,6; p < 0,001 e interação F = 5,97; p = 0,003 (erro b, GL 18). CV1 = 9,47%; CV2 = 3,72%. Cultivar dentro de sombra (Tukey): 0% Arara 33,15 a, Catuai_144 31,05 a, Topazio 25,45 b; 30% Arara 35,75 a, Catuai_144 34,63 ab, Topazio 32,48 b; 50% Arara 36,98 a, Catuai_144 32,28 b, Topazio 29,50 c. Sombra dentro de cultivar: só Topazio respondeu (p = 0,002), com melhor produção perto de 30% de sombra.

## Código de referência
R (ExpDes.pt):
```r
library(ExpDes.pt)
d <- read.csv("fatorial_adubacao.csv")
fat2.dic(d$especie, d$adubacao, d$massa_seca_g, quali = c(TRUE, TRUE),
         mcomp = "tukey", fac.names = c("Especie", "Adubacao"))
# fatorial em DBC: fat2.dbc(f1, f2, bloco, resp, ...)
s <- read.csv("parcela_sub_cafe_sombra.csv")
psub2.dbc(s$sombreamento_pct, s$cultivar, s$bloco, s$produtividade_sc_ha,
          quali = c(FALSE, TRUE), mcomp = "tukey",
          fac.names = c("Sombreamento", "Cultivar"))
```
O ExpDes.pt desdobra automaticamente quando a interação é significativa.

Python (statsmodels):
```python
import pandas as pd, statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from scipy import stats
d = pd.read_csv("fatorial_adubacao.csv")
m = smf.ols("massa_seca_g ~ C(especie) * C(adubacao)", data=d).fit()
print(anova_lm(m, typ=2))
# parcela subdividida: erro a = bloco x sombra
s = pd.read_csv("parcela_sub_cafe_sombra.csv")
f = ("produtividade_sc_ha ~ C(bloco) + C(sombreamento_pct) + "
     "C(bloco):C(sombreamento_pct) + C(cultivar) + C(sombreamento_pct):C(cultivar)")
t = anova_lm(smf.ols(f, data=s).fit())
ea = t.loc["C(bloco):C(sombreamento_pct)"]
Fs = t.loc["C(sombreamento_pct)", "mean_sq"] / ea["mean_sq"]
p = stats.f.sf(Fs, t.loc["C(sombreamento_pct)", "df"], ea["df"])
print(t); print("Sombreamento (erro a): F =", round(Fs, 2), "p =", round(p, 4))
```
A tabela padrão do Python testa tudo contra o erro b; o F correto do fator da parcela é o calculado com o erro a (linha acima). Para o desdobramento com Tukey, prefira o R.

## Formato da resposta
1. Dados conferidos (combinações e repetições).
2. Pressupostos.
3. Decisão sobre a interação, em uma frase.
4. **Tabelas e figura ABNT** (skill 05: título acima, 3 traços horizontais, Fonte e Nota abaixo; Markdown no chat + versão para o Docs):
   - ANOVA: FV | GL | SQ | QM | F (**, *, ns); no split-plot, Erro (a), Erro (b), CV1 (%) e CV2 (%).
   - Interação significativa: dupla entrada. Ex.: `Mogno-africano | 33,60 aA | 28,33 aB | 20,23 aC`; Nota: "Médias seguidas pela mesma letra minúscula na coluna e maiúscula na linha não diferem entre si pelo teste de Tukey a 5 % de probabilidade." Sem interação: médias de cada fator.
   - Figura: barras agrupadas em tons de cinza, ou linhas por nível se um fator é quantitativo.
5. Parágrafo citando a tabela: ex. "Conforme a Tabela 2, a resposta à adubação depende da espécie: o mogno-africano responde muito ao adubo mineral, enquanto a aroeira não responde."

## Regras de segurança
- Nunca invente dados ou resultados; execute e mostre o código, ou avise que não executou.
- Com interação significativa, não conclua sobre efeitos principais sem desdobrar.
- Em parcela subdividida, nunca teste o fator da parcela com o erro b.
- Pressuposto violado: avise e sugira transformação (√x, log) ou análise não paramétrica por combinação.
- Fator quantitativo: regressão, não Tukey.
- Linguagem simples; explique "interação" com exemplo do campo.
