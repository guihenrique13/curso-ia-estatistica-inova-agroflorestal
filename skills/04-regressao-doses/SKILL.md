---
name: regressao-doses
description: Analisa fatores quantitativos (doses de adubo, níveis de sombreamento, espaçamentos, idades) por regressão das médias - modelo linear ou quadrático, R², significância dos coeficientes e dose de máxima eficiência técnica. Use quando os tratamentos forem números com ordem e o usuário pedir ANOVA, "melhor dose", curva de resposta ou Tukey em doses.
---

# Regressão para Doses e Níveis Quantitativos

## Quando usar
O fator é **quantitativo**: doses de N (0, 50, 100, 150, 200 kg/ha), % de sombra, espaçamento, idade. Aqui **não se usa Tukey**: a pergunta não é "qual dose difere de qual", e sim "como a resposta muda conforme a dose" e "qual a dose ótima". Tukey em doses perde a informação da ordem e pode apontar como iguais doses vizinhas que fazem parte de uma tendência clara.

## Antes de analisar, pergunte
1. Delineamento (DIC ou DBC) e se há blocos.
2. Variável resposta e unidade.
3. Níveis do fator e unidade (kg/ha, %, m). Há testemunha (dose 0)?
4. Número de repetições por nível.
5. Há outro fator junto (fatorial)? Se sim, combine com a skill 03.

## Passo a passo
1. **Conferir dados**: a coluna da dose deve ser numérica; contar repetições por dose. Ideal ≥ 4 níveis.
2. **ANOVA** com a dose como fator (para obter o QM do resíduo), pressupostos (Shapiro-Wilk, Bartlett/Levene) e CV%.
3. Se F de tratamentos for significativo, **ajustar regressão** nas médias (desdobrando a SQ de tratamentos):
   - Linear: ŷ = b0 + b1·x
   - Quadrático: ŷ = b0 + b1·x + b2·x²
4. **Escolher o modelo**: o de maior grau com coeficiente significativo (p < 0,05), **desvio de regressão não significativo** e sentido biológico. Não suba para cúbico só para aumentar o R².
5. **R²** (da regressão nas médias) = SQ da regressão / SQ de tratamentos: quanto da variação entre doses o modelo explica.
6. Quadrático com b2 < 0 (curva com ponto máximo): **dose de máxima eficiência técnica (DMET)** = −b1 / (2·b2). A resposta máxima é ŷ(DMET). Só é válida se estiver dentro do intervalo testado; fora dele, não extrapole.
7. Opcional: máxima eficiência econômica (MEE) usa preços do insumo e do produto; é sempre menor que a DMET.

## Exemplo resolvido (para conferência)
**Doses de N × volume de eucalipto em ILPF (m³/ha)** (doses_nitrogenio.csv, DIC, 5 doses × 4 rep.):
- ANOVA: F = 32,55; p < 0,001; GL res = 15; CV = 5,14%; Shapiro p = 0,57; Bartlett p = 0,56.
- Médias: 0 → 41,35; 50 → 50,38; 100 → 55,98; 150 → 60,75; 200 → 59,00.
- Linear: R² = 0,85, mas desvio de regressão significativo (p = 0,005) → inadequado.
- Quadrático: ŷ = 41,1586 + 0,21921·x − 0,00063929·x²; b2 significativo (p < 0,001); desvio não significativo (p = 0,61); **R² = 0,99** → modelo escolhido.
- Cúbico: b3 não significativo (p = 0,49) → descartado.
- **DMET = −0,21921 / (2 × −0,00063929) ≈ 171,4 kg/ha de N**, com volume estimado de ≈ 59,9 m³/ha.
Atenção: use os coeficientes com várias casas decimais; arredondar b2 para −0,0006 muda a DMET para ≈ 183.

## Código de referência
R (ExpDes.pt):
```r
library(ExpDes.pt)
d <- read.csv("doses_nitrogenio.csv")
dic(d$dose_n_kg_ha, d$volume_m3_ha, quali = FALSE)   # ANOVA + regressões
m <- lm(volume_m3_ha ~ dose_n_kg_ha + I(dose_n_kg_ha^2), data = d)
b <- coef(m)
met <- -b[2] / (2 * b[3])
met; predict(m, data.frame(dose_n_kg_ha = met))
```
Python (statsmodels):
```python
import pandas as pd, statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
d = pd.read_csv("doses_nitrogenio.csv")
print(anova_lm(smf.ols("volume_m3_ha ~ C(dose_n_kg_ha)", data=d).fit()))
lin = smf.ols("volume_m3_ha ~ dose_n_kg_ha", data=d).fit()
qua = smf.ols("volume_m3_ha ~ dose_n_kg_ha + I(dose_n_kg_ha**2)", data=d).fit()
print(qua.summary())
b0, b1, b2 = qua.params
met = -b1 / (2 * b2)
print(f"DMET = {met:.1f} kg/ha; y max = {b0 + b1*met + b2*met**2:.2f}")
```
Obs.: o R² de `qua.summary()` usa as parcelas individuais e é menor que o R² nas médias do ExpDes.pt (0,99). Informe qual foi usado. Os valores-p dos coeficientes também podem diferir um pouco, porque o ExpDes.pt testa com o QM do resíduo da ANOVA.

## Formato da resposta
1. Dados conferidos (doses, repetições).
2. Pressupostos; modelo escolhido e justificativa em uma frase.
3. **Tabelas e figura ABNT** (skill 05: título acima, 3 traços horizontais, Fonte e Nota abaixo; Markdown no chat + versão para o Docs):
   - ANOVA: FV | GL | SQ | QM | F (**, *, ns), com Resíduo, Total e CV (%); pode incluir as linhas Efeito linear, Efeito quadrático e Desvios de regressão.
   - Regressão: Modelo | Equação | R² | DMET. Ex.: `Quadrático | ŷ = 41,1586 + 0,21921x − 0,00063929x² | 0,99 | 171,4 kg/ha`.
   - Figura: médias observadas como pontos (± erro padrão) + curva ajustada em preto, equação e R² no gráfico, linha tracejada na DMET; eixos "Dose de N (kg/ha)" e "Volume (m³/ha)".
4. DMET (se quadrático com máximo) e resposta máxima estimada.
5. Parágrafo citando tabela e figura: ex. "Conforme a Figura 1, o volume de madeira aumentou com o N até cerca de 171 kg/ha; acima disso não houve ganho."

## Regras de segurança
- Nunca use Tukey como análise principal de fator quantitativo.
- Nunca invente coeficientes ou R²; rode o código e mostre-o, ou avise que não rodou.
- Não extrapole a curva além das doses testadas.
- Com só 3 níveis, a quadrática passa exatamente pelas médias (R² = 1): avise que isso não prova o modelo.
- Pressuposto violado: avise e sugira transformação (log, √x) antes da regressão.
- Explique R², DMET e "desvio de regressão" em linguagem simples.
