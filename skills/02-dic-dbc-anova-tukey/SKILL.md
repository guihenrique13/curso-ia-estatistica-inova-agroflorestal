---
name: dic-dbc-anova-tukey
description: Analisa experimentos com um fator em DIC (inteiramente casualizado) ou DBC (blocos casualizados) - confere a planilha, testa pressupostos, faz ANOVA, calcula CV% e compara médias por Tukey. Use quando o usuário enviar dados de um experimento com um único fator qualitativo (substratos, cultivares, manejos, espécies) e pedir ANOVA, teste de médias ou "qual tratamento foi melhor".
---

# DIC e DBC: ANOVA + Tukey

## Quando usar
Um único fator **qualitativo** (tipos de substrato, cultivares, manejos), com ou sem blocos. Se o fator for quantitativo (doses), use a skill 04-regressao-doses. Se houver dois fatores, use a 03.

## Antes de analisar, pergunte
1. Delineamento: DIC ou DBC? (Havia blocos? Qual coluna indica o bloco?)
2. Qual coluna é a variável resposta e qual a unidade?
3. Qual coluna é o tratamento e quantos níveis tem?
4. Quantas repetições (ou blocos)? Está balanceado?
5. O fator é qualitativo ou quantitativo?

## Passo a passo
1. **Conferir a estrutura**: nº de linhas = tratamentos × repetições; contar repetições por tratamento; checar grafias diferentes, vazios e vírgula decimal. Bloco deve ser tratado como **fator** (não número).
2. **Modelo**: DIC: resposta ~ tratamento. DBC: resposta ~ tratamento + bloco.
3. **Pressupostos** (nos resíduos do modelo):
   - Normalidade: Shapiro-Wilk (p > 0,05 = normal).
   - Homogeneidade: Bartlett (sensível à não normalidade) ou Levene (mais robusto).
4. **ANOVA**: F e valor-p do tratamento. Em DBC, informe também o bloco (se significativo, o uso de blocos foi útil).
5. **CV%** = 100 × √QMres / média geral. Referência de campo: < 10% baixo, 10–20% médio, 20–30% alto, > 30% muito alto (depende da variável; contagens costumam ser altas).
6. Se F significativo (p < 0,05): **Tukey a 5%**. Se não significativo: "as médias não diferem", sem letras diferentes.
7. Se pressuposto falhar: transformar (√(x + 0,5) para contagens; log(x + 1) para dados assimétricos) e refazer, ou usar **Kruskal-Wallis** (DIC) / **Friedman** (DBC). Apresente as médias originais e diga que a análise foi feita nos dados transformados.

## Exemplos resolvidos (para conferência)
**DIC – substratos × altura de mudas de ipê** (dic_mudas.csv, 5 substratos × 4 rep.): F = 34,57; p < 0,001; GL res = 15; CV = 6,1%; Shapiro p = 0,81; Bartlett p = 0,09. Tukey: composto_organico 37,40 a; terra_esterco 36,35 a; comercial 33,23 a; terra 26,48 b; terra_areia 24,98 b.

**DBC – cultivares de milho em aleias** (dbc_milho.csv, 5 cultivares × 4 blocos): F = 34,69; p < 0,001; bloco p = 0,004; CV = 5,04%. Tukey (kg/ha): Hibrido_comercial 6147 a; BRS_Gorutuba 6130 a; BRS_Caimbe 5213 b; AL_Bandeirante 4974 b; Crioulo_local 4291 c.

**Pressuposto violado – pragas por manejo** (dic_contagem_pragas.csv): Bartlett p = 0,02 (variâncias heterogêneas), CV = 52%. Com √(x + 0,5): Bartlett p = 0,50, CV = 25%; saf_biodiverso teve menos pragas (c) que convencional (a). Kruskal-Wallis: χ² = 15,2; p = 0,0017.

## Código de referência
R (ExpDes.pt):
```r
library(ExpDes.pt)
d <- read.csv("dic_mudas.csv")
dic(d$substrato, d$altura_cm, quali = TRUE, mcomp = "tukey", sigF = 0.05)
d2 <- read.csv("dbc_milho.csv")
dbc(d2$cultivar, d2$bloco, d2$produtividade_kg_ha, quali = TRUE, mcomp = "tukey")
# pressuposto violado
p <- read.csv("dic_contagem_pragas.csv")
dic(p$manejo, sqrt(p$insetos_praga + 0.5), quali = TRUE)
kruskal.test(insetos_praga ~ manejo, data = p)
# DBC não paramétrico: friedman.test(y ~ trat | bloco, data = d)
```
Python (statsmodels + scipy):
```python
import pandas as pd, statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from scipy import stats
d = pd.read_csv("dbc_milho.csv")
m = smf.ols("produtividade_kg_ha ~ C(cultivar) + C(bloco)", data=d).fit()
print(anova_lm(m))
print(stats.shapiro(m.resid))
grupos = [g["produtividade_kg_ha"].astype(float) for _, g in d.groupby("cultivar")]
print(stats.bartlett(*grupos), stats.levene(*grupos))
cv = 100 * (m.mse_resid ** 0.5) / d["produtividade_kg_ha"].mean()
print(f"CV = {cv:.2f}%")
# Tukey com o QM do resíduo do modelo (vale para DIC e DBC)
med = d.groupby("cultivar")["produtividade_kg_ha"].mean().sort_values(ascending=False)
r = d["bloco"].nunique()   # repetições por tratamento
q = stats.studentized_range.ppf(0.95, len(med), m.df_resid)
dms = q * (m.mse_resid / r) ** 0.5
print(med); print(f"DMS Tukey = {dms:.1f}")
```
Duas médias diferem se a diferença entre elas for maior que a DMS (diferença mínima significativa); monte as letras a partir disso. Evite `pairwise_tukeyhsd` em DBC: ele ignora os blocos e muda o resultado (no milho, AL_Bandeirante × Crioulo_local deixa de diferir).

## Formato da resposta
1. Dados conferidos (tratamentos, repetições, problemas encontrados).
2. Pressupostos: teste, valor-p, conclusão.
3. Valores-p e conclusão em linguagem simples.
4. **Tabelas e figura no padrão ABNT** (siga a skill 05: título acima, só 3 traços horizontais, Fonte e Nota abaixo, vírgula decimal; versão Markdown no chat + versão para exportar ao Docs):
   - Tabela 1 – ANOVA: FV | GL | SQ | QM | F (Bloco no DBC; Resíduo; Total; CV (%)), com **, * ou ns.
   - Tabela 2 – médias em ordem decrescente com letras. Ex.: `Composto orgânico | 37,40 a` … `Terra + areia | 24,98 b`; Nota: "Médias seguidas pela mesma letra na coluna não diferem entre si pelo teste de Tukey a 5 % de probabilidade."
   - Figura 1 – barras em cinza (média ± erro padrão) com as letras acima; eixo "Altura (cm)".
5. Parágrafo citando as tabelas: ex. "Conforme a Tabela 2, mudas em composto orgânico, terra + esterco e substrato comercial cresceram igualmente e cerca de 10 cm a mais que em terra pura".

## Regras de segurança
- Nunca invente dados, médias ou valores-p.
- Execute o código sempre que possível e mostre-o. Se não executou, diga claramente e entregue o código.
- Avise quando um pressuposto falhar e proponha transformação ou Kruskal-Wallis/Friedman.
- Não aplique Tukey quando F não for significativo, nem em fator quantitativo.
- Explique em linguagem simples (valor-p, CV, letras).
