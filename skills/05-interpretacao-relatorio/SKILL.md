---
name: interpretacao-relatorio
description: Transforma resultados estatísticos (ANOVA, Tukey, desdobramento, regressão) em texto de resultados e discussão para relatório técnico, TCC ou artigo, com tabelas e figuras no padrão ABNT/IBGE prontas para colar, descrição da metodologia estatística e declaração de uso de IA. Use para redigir resultados, montar tabela/figura ABNT ou citar o uso de IA.
---

# Interpretação, Redação e Tabelas ABNT

## Quando usar
Análise já feita (por esta IA, R ou SISVAR) e o usuário quer texto, tabela ou figura para relatório, TCC ou artigo. Vale também ao final de TODA análise (skills 02–04): tabelas e figuras saem sempre no padrão abaixo.

## Antes de redigir, pergunte
1. Delineamento, tratamentos, repetições; variáveis e unidades; local e época (para o título).
2. Onde estão os resultados? (Peça a saída ou rode a análise; **não escreva números de memória**.)
3. Destino e norma (ABNT ou a da revista, que prevalece).

## Passo a passo
1. **Conferir a saída**: ANOVA, pressupostos, CV%, Tukey ou regressão. Faltou algo: rode ou peça.
2. **Metodologia estatística** (1 parágrafo): delineamento, tratamentos e repetições, pressupostos, ANOVA, Tukey ou regressão, 5 % de significância, software e pacote.
3. **Tabelas e figuras ABNT** (seção abaixo).
4. **Resultados**: efeito, diferenças com números e tamanho prático (cm, kg/ha, %). Interação significativa: descreva o desdobramento.
5. **Discussão**: porquê agronômico; só literatura **que o usuário fornecer**. **Limitações**: pressupostos, transformação, CV alto, um local/ano.
6. **Declaração de uso de IA**.

## Formatação ABNT de tabelas e figuras
Base: ABNT NBR 14724 e Normas de Apresentação Tabular do IBGE (1993).
- **Acima**: "Tabela N – Título" (o quê, onde, quando). Gráfico: "Figura N – Título". Numeração sequencial, separada para tabelas e figuras.
- Só **3 traços horizontais**: topo, sob o cabeçalho e base. Sem traços verticais, laterais abertas, sem traços no corpo.
- **Abaixo**: "Fonte: elaborada pelo autor (2026)." (ou a origem dos dados); depois "Nota:"/legenda. Fonte e notas em letra menor (10).
- Vírgula decimal; mesmo nº de casas na coluna; unidade no cabeçalho: "Altura (cm)".
- Significância, explicada na nota: ** significativo a 1 %; * significativo a 5 %; ns não significativo.
- **ANOVA**: FV | GL | SQ | QM | F, com Resíduo, Total e CV (%). Parcela subdividida: Erro (a), Erro (b), CV1 (%) e CV2 (%).
- **Médias**: tratamento | média (unidade) com letras. Nota: "Médias seguidas pela mesma letra na coluna não diferem entre si pelo teste de Tukey a 5 % de probabilidade."
- **Interação significativa** (fatorial, parcela subdividida): dupla entrada; minúsculas comparam na coluna, maiúsculas na linha, e a nota diz isso.
- **Regressão**: ŷ = b0 + b1x + b2x², R² e, se quadrática, DMET; figura com médias observadas (pontos) e curva ajustada.
- **Figuras**: título acima e fonte abaixo (fora da imagem), eixos com título e unidade, sem 3D, legível em preto e branco (tons de cinza, marcadores distintos).

### Exemplo completo (dic_mudas)
(─ = posição dos 3 traços horizontais)
```
Tabela 1 – Análise de variância da altura de mudas de ipê-amarelo
           em cinco substratos, em viveiro, aos 120 dias
──────────────────────────────────────────────
FV            GL        SQ        QM         F
──────────────────────────────────────────────
Substrato      4    515,85    128,96   34,57**
Resíduo       15     55,95      3,73
Total         19    571,81
CV (%)                6,10
──────────────────────────────────────────────
Fonte: elaborada pelo autor (2026).
Nota: ** significativo a 1 % de probabilidade pelo teste F.

Tabela 2 – Altura média de mudas de ipê-amarelo em cinco substratos,
           em viveiro, aos 120 dias
────────────────────────────────
Substrato            Altura (cm)
────────────────────────────────
Composto orgânico        37,40 a
Terra + esterco          36,35 a
Comercial                33,23 a
Terra                    26,48 b
Terra + areia            24,98 b
────────────────────────────────
Fonte: elaborada pelo autor (2026).
Nota: Médias seguidas pela mesma letra na coluna não diferem
entre si pelo teste de Tukey a 5 % de probabilidade.
```
Parágrafo pronto: "Conforme a Tabela 1, o substrato influenciou a altura das mudas (F = 34,57; p < 0,01). Composto orgânico, terra + esterco e substrato comercial proporcionaram as maiores alturas (33,23 a 37,40 cm; Tabela 2), cerca de 10 cm acima de terra e terra + areia. O CV de 6,10 % indica boa precisão experimental."

### Entrega no Gemini (cada tabela duas vezes)
1. **No chat**: tabela Markdown, título acima e Fonte/Nota abaixo como texto (o chat desenha todas as bordas).
2. **Versão ABNT**: oriente exportar a resposta para o Google Docs (Compartilhar e exportar → Exportar para Documentos) ou gerar no Canvas. No Docs/Word: tire todas as bordas (0 pt) e aplique borda superior e inferior na linha do cabeçalho e borda inferior na última linha.
3. Opcional: texto CSV (separador ";") para colar no Planilhas.
4. Diga a sequência ("Tabela 1: ANOVA; Tabela 2: médias; Figura 1: barras") e ofereça o parágrafo que as cita.

Figura em Python (execute e mostre o código):
```python
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
s = ["Composto\norgânico","Terra +\nesterco","Comercial","Terra","Terra +\nareia"]
m = [37.40, 36.35, 33.23, 26.48, 24.98]; l = ["a","a","a","b","b"]
fig, ax = plt.subplots()
ax.bar(s, m, color="0.7", edgecolor="black")
for i, (v, t) in enumerate(zip(m, l)):
    ax.text(i, v + 0.5, t, ha="center")
ax.set_xlabel("Substrato"); ax.set_ylabel("Altura (cm)")
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}".replace(".", ",")))
fig.tight_layout(); fig.savefig("figura1.png", dpi=300)
```

## Formato da resposta
1. Metodologia estatística. 2. Tabelas ABNT (ANOVA + médias ou regressão), nas duas versões. 3. Figura ABNT e código. 4. Numeração e parágrafo de resultados citando "Tabela N"/"Figura N". 5. Ideias para a discussão (sem inventar citações). 6. Declaração de uso de IA.

## Como citar o uso de IA
- Na metodologia: ferramenta, data e finalidade. Modelo: "As análises estatísticas foram realizadas em Python (statsmodels) no Gemini (Google, acesso em [data]); os resultados foram conferidos pelos autores, que assumem total responsabilidade pelo conteúdo."
- Referência (ABNT, adaptar): GOOGLE. **Gemini**. Versão [x]. [S. l.]: Google, [ano]. Disponível em: https://gemini.google.com. Acesso em: [dia mês ano].
- Cite o software dos cálculos (Python/statsmodels, R/ExpDes.pt). IA não é autora; confira as regras da instituição.

## Regras de segurança
- Nunca invente dados, resultados, valores-p ou referências.
- Só números da saída da análise; sem saída, rode o código (e mostre-o) ou peça. Se não rodou, diga.
- Pressuposto violado: informe a transformação ou o teste usado.
- Não exagere: "não diferiram" não significa "são iguais"; um local/ano não generaliza.
