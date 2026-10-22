"""Monta e executa notebooks/analise_exemplos.ipynb."""
import copy
import sys
from pathlib import Path

import nbformat as nbf
from nbclient import NotebookClient

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "notebooks" / "analise_exemplos.ipynb"

cells = []


def md(t):
    cells.append(nbf.v4.new_markdown_cell(t.strip("\n")))


def code(t, tags=None):
    c = nbf.v4.new_code_cell(t.strip("\n"))
    if tags:
        c.metadata["tags"] = tags
    cells.append(c)


# ---------------------------------------------------------------- abertura
md(r"""
# IA para Estatística Experimental: análises de exemplo em Python

**Curso Inova Agroflorestal (UFVJM)**: notebook de demonstração para o Google Colab.

Este notebook mostra **o código que a IA escreve "por trás"** quando você pede uma análise ao Gemini. Você **não precisa saber programar** para acompanhar: cada bloco de código vem antes de uma explicação **"O que este código faz"**.

**Como usar no Colab**
1. Clique em uma célula de código e aperte **Shift + Enter** para rodá-la (ou no botão ▶ à esquerda).
2. Rode as células **em ordem**, de cima para baixo.
3. Se algo der erro, leia a mensagem. Muitas vezes é só um arquivo que não foi carregado.

**Conjuntos de dados usados** (todos fictícios, simulados para o curso):

| Arquivo | Delineamento | Pergunta |
|---|---|---|
| `dic_mudas.csv` | DIC | Qual substrato produz mudas de ipê mais altas? |
| `dbc_milho.csv` | DBC | Qual cultivar de milho rende mais em aleias de gliricídia? |
| `fatorial_adubacao.csv` | Fatorial 3×3 em DIC | Espécie florestal × tipo de adubação: há interação? |
| `parcela_sub_cafe_sombra.csv` | Parcelas subdivididas em DBC | Sombreamento (parcela) × cultivar de café (subparcela) |
| `doses_nitrogenio.csv` | DIC com doses (regressão) | Qual a dose de N de máxima eficiência no eucalipto? |
| `dic_contagem_pragas.csv` | DIC com contagens | O que fazer quando os pressupostos da ANOVA falham? |

> Os resultados deste notebook foram conferidos com o R (pacote `ExpDes.pt`). Veja a seção **Conferência com o gabarito do R** no final.
""")

md(r"""
## 0. Preparação

### 0.1 Carregar as "caixas de ferramentas" (bibliotecas)

**O que este código faz:** o Python sozinho não sabe fazer ANOVA. Aqui "abrimos as caixas de ferramentas" que já vêm instaladas no Colab:
- `pandas`: lê e organiza tabelas (como uma planilha);
- `scipy`: testes estatísticos (Shapiro-Wilk, Bartlett, Levene, Kruskal-Wallis);
- `statsmodels`: ANOVA, regressão e Tukey;
- `matplotlib`: gráficos.
""")

code(r"""
import io
import os
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import studentized_range
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.multicomp import pairwise_tukeyhsd

pd.set_option("display.precision", 4)
plt.rcParams["figure.dpi"] = 100
print("Bibliotecas carregadas!")
""")

md(r"""
### 0.2 Como carregar os dados (3 jeitos)

**O que este código faz:** cria uma função `carregar("nome_do_arquivo")` que busca a planilha em três lugares, nesta ordem:

1. **Upload do seu computador** (só no Colab): mude `USAR_UPLOAD = True`. Ao rodar cada análise, vai aparecer um botão **"Escolher arquivos"**. Aceita `.csv` ou `.xlsx`.
2. **Pasta local**: se o arquivo já estiver na pasta `dados/` (ou se você arrastou o arquivo para o painel 📁 **Arquivos** à esquerda do Colab, que fica em `/content`).
3. **Endereço na internet (URL)**: se não houver upload nem arquivo local, os dados são baixados automaticamente do repositório do curso no GitHub (`URL_BASE`). Se você copiar os arquivos para outro repositório, troque `URL_BASE` pelo endereço "raw" da sua pasta `dados/`.

> Dica: o jeito mais simples no Colab é clicar no ícone de pasta 📁 à esquerda e **arrastar os arquivos CSV para lá**.
""")

code(r"""
# ---- AJUSTE AQUI, se precisar ----
USAR_UPLOAD = False   # True = abre a janela "Escolher arquivos" (somente no Colab)
URL_BASE = "https://raw.githubusercontent.com/guihenrique13/curso-ia-estatistica-inova-agroflorestal/main/dados/"  # endereço "raw" da pasta dados/ do repositório do curso
PASTAS_LOCAIS = ["dados", "../dados", "/content/dados", "/content"]
# -----------------------------------

EM_COLAB = "google.colab" in sys.modules


def carregar(nome):
    # 1) upload manual (Colab)
    if EM_COLAB and USAR_UPLOAD:
        from google.colab import files
        print(f"Escolha o arquivo '{nome}.csv' (ou .xlsx) no seu computador:")
        enviado = files.upload()
        nome_arquivo = list(enviado)[0]
        conteudo = io.BytesIO(enviado[nome_arquivo])
        if nome_arquivo.lower().endswith(".xlsx"):
            return pd.read_excel(conteudo)
        return pd.read_csv(conteudo)
    # 2) pasta local
    for pasta in PASTAS_LOCAIS:
        for ext in (".csv", ".xlsx"):
            caminho = os.path.join(pasta, nome + ext)
            if os.path.exists(caminho):
                print("Lido de:", caminho)
                return pd.read_csv(caminho) if ext == ".csv" else pd.read_excel(caminho)
    # 3) internet
    print("Lendo da internet:", URL_BASE + nome + ".csv")
    return pd.read_csv(URL_BASE + nome + ".csv")


print("Rodando no Colab?", EM_COLAB)
""")

md(r"""
### 0.3 Funções de apoio (o "molde" de cada análise)

**O que este código faz:** em vez de repetir as mesmas contas seis vezes, criamos pequenas "receitas" reaproveitáveis:

- `quadro_anova(modelo)`: monta o **quadro da ANOVA** no formato que aparece nos livros e no `ExpDes.pt` (GL, SQ, QM, Fc, Pr>Fc).
- `cv(modelo, y)`: **coeficiente de variação** (CV% = raiz do QM do resíduo ÷ média geral × 100). Mede a precisão do experimento.
- `pressupostos(modelo, dados, resposta, tratamento)`: testa **normalidade dos resíduos** (Shapiro-Wilk) e **homogeneidade das variâncias** (Bartlett e Levene). Regra prática: **p > 0,05 = pressuposto OK**.
- `tukey_letras(...)`: teste de **Tukey** com as **letras** (médias com a mesma letra não diferem). Ele recebe o QM do resíduo e o GL **do modelo correto** (importante no DBC, fatorial e parcela subdividida).
""")

code(r"""
def quadro_anova(modelo):
    t = sm.stats.anova_lm(modelo, typ=1)
    t = t.rename(columns={"df": "GL", "sum_sq": "SQ", "mean_sq": "QM", "F": "Fc", "PR(>F)": "Pr>Fc"})
    t.index = [i.replace("C(", "").replace(")", "") for i in t.index]
    t = t.rename(index={"Residual": "Resíduo"})
    t.loc["Total"] = [t["GL"].sum(), t["SQ"].sum(), np.nan, np.nan, np.nan]
    return t


def cv(modelo, y):
    return 100 * np.sqrt(modelo.mse_resid) / np.mean(y)


def pressupostos(modelo, dados, resposta, tratamento):
    sw = stats.shapiro(modelo.resid)
    grupos = [g[resposta].to_numpy(dtype=float) for _, g in dados.groupby(tratamento)]
    bt = stats.bartlett(*grupos)
    lv = stats.levene(*grupos, center="median")
    ok = lambda p: "OK (p > 0,05)" if p > 0.05 else "VIOLADO (p <= 0,05)"
    print(f"Normalidade dos resíduos (Shapiro-Wilk): W = {sw.statistic:.4f}, p = {sw.pvalue:.4f}  -> {ok(sw.pvalue)}")
    print(f"Homogeneidade (Bartlett):                K2 = {bt.statistic:.4f}, p = {bt.pvalue:.4f}  -> {ok(bt.pvalue)}")
    print(f"Homogeneidade (Levene, mediana):         W = {lv.statistic:.4f}, p = {lv.pvalue:.4f}  -> {ok(lv.pvalue)}")
    return sw.pvalue, bt.pvalue, lv.pvalue


def tukey_letras(dados, resposta, tratamento, qme, gl_residuo, alfa=0.05):
    medias = dados.groupby(tratamento)[resposta].mean().sort_values(ascending=False)
    n = dados.groupby(tratamento)[resposta].count().min()   # repetições por tratamento
    k = len(medias)
    q = studentized_range.ppf(1 - alfa, k, gl_residuo)
    dms = q * np.sqrt(qme / n)                               # diferença mínima significativa
    m = medias.values
    letras, faixas, ultimo = [""] * k, [], -1
    for i in range(k):
        j = i
        while j + 1 < k and (m[i] - m[j + 1]) < dms:
            j += 1
        if j > ultimo:
            faixas.append((i, j))
            ultimo = j
    for f, (i, j) in enumerate(faixas):
        for t in range(i, j + 1):
            letras[t] += "abcdefghij"[f]
    print(f"Tukey a {alfa:.0%}: DMS = {dms:.4f} (q = {q:.3f}, QM resíduo = {qme:.4f}, GL = {gl_residuo:g}, n = {n})")
    return pd.DataFrame({"Média": m.round(3), "Grupo": letras}, index=medias.index)


# aqui guardamos os números principais para conferir com o R no final
conferir = {}
""")

# ---------------------------------------------------------------- 1 DIC
md(r"""
---
## 1. DIC: substratos para mudas de ipê-amarelo

**Experimento:** 5 substratos × 4 repetições, em delineamento inteiramente casualizado (DIC), no viveiro. Resposta: altura da muda aos 120 dias (cm).

**Modelo:** altura = média geral + efeito do substrato + erro.

### 1.1 Carregar e olhar os dados
**O que este código faz:** lê a planilha e mostra as primeiras linhas e a média por substrato. Sempre olhe os dados antes de analisar!
""")
code(r"""
mudas = carregar("dic_mudas")
display(mudas.head())
print(mudas.groupby("substrato")["altura_cm"].agg(["count", "mean", "std"]).round(2))
""")
md(r"""
### 1.2 ANOVA e CV
**O que este código faz:** ajusta o modelo `altura_cm ~ C(substrato)` (o `C()` diz ao Python que substrato é uma **categoria**, não um número) e monta o quadro da ANOVA.

**Como ler:** se **Pr>Fc < 0,05**, pelo menos um substrato difere dos outros.
""")
code(r"""
mod_mudas = smf.ols("altura_cm ~ C(substrato)", data=mudas).fit()
tab = quadro_anova(mod_mudas)
display(tab)
cv_mudas = cv(mod_mudas, mudas["altura_cm"])
print(f"CV = {cv_mudas:.2f} %")
conferir["1 DIC: F substrato"] = tab.loc["substrato", "Fc"]
conferir["1 DIC: p substrato"] = tab.loc["substrato", "Pr>Fc"]
conferir["1 DIC: CV %"] = cv_mudas
""")
md(r"""
### 1.3 Pressupostos
**O que este código faz:** a ANOVA só é confiável se (1) os resíduos forem aproximadamente **normais** e (2) os tratamentos tiverem **variâncias parecidas**. Os testes abaixo verificam isso.
""")
code(r"""
sw, bt, lv = pressupostos(mod_mudas, mudas, "altura_cm", "substrato")
conferir["1 DIC: Shapiro p"] = sw
conferir["1 DIC: Bartlett p"] = bt
""")
md(r"""
### 1.4 Teste de Tukey
**O que este código faz:** compara todos os pares de substratos. Primeiro com a função pronta do `statsmodels` (`pairwise_tukeyhsd`, coluna `reject = True` quer dizer "diferem"), depois em forma de **letras**, como nos artigos.

> No DIC, as duas formas dão o mesmo resultado. Em DBC/fatorial **não**: `pairwise_tukeyhsd` ignora os blocos e usa o erro errado. Por isso usamos `tukey_letras` com o QM do resíduo da ANOVA.
""")
code(r"""
print(pairwise_tukeyhsd(mudas["altura_cm"], mudas["substrato"], alpha=0.05))
letras_mudas = tukey_letras(mudas, "altura_cm", "substrato", mod_mudas.mse_resid, mod_mudas.df_resid)
display(letras_mudas)
""")
md(r"""
### 1.5 Gráfico
**O que este código faz:** gráfico de barras com a média de cada substrato, o desvio padrão (barrinha preta) e as letras do Tukey em cima.
""")
code(r"""
resumo = mudas.groupby("substrato")["altura_cm"].agg(["mean", "std"]).loc[letras_mudas.index]
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(resumo.index, resumo["mean"], yerr=resumo["std"], capsize=4, color="#5b8c5a")
for i, (nome, linha) in enumerate(resumo.iterrows()):
    ax.text(i, linha["mean"] + linha["std"] + 0.5, letras_mudas.loc[nome, "Grupo"], ha="center", fontsize=12)
ax.set_ylabel("Altura aos 120 dias (cm)")
ax.set_title("Mudas de ipê-amarelo por substrato (Tukey 5%)")
plt.xticks(rotation=20)
plt.tight_layout()
plt.show()
""")
md(r"""
**Interpretação:** composto orgânico, terra + esterco e substrato comercial formam o grupo "a" (mudas mais altas); terra pura e terra + areia ficam no grupo "b". CV de 6,1% indica **boa precisão**.
""")

# ---------------------------------------------------------------- 2 DBC
md(r"""
---
## 2. DBC: cultivares de milho em aleias de gliricídia

**Experimento:** 5 cultivares × 4 blocos (os blocos são faixas do terreno com declives diferentes). Resposta: produtividade de grãos (kg/ha).

**Por que blocos?** O terreno não é uniforme. Cada bloco tem **todas** as cultivares, e o modelo "desconta" a diferença entre blocos do erro, o que deixa o teste mais sensível.

**Modelo:** produtividade = média + efeito da cultivar + efeito do bloco + erro.
""")
code(r"""
milho = carregar("dbc_milho")
display(milho.head())
print(milho.pivot(index="cultivar", columns="bloco", values="produtividade_kg_ha"))
""")
md(r"""
### 2.1 ANOVA e CV
**O que este código faz:** igual ao DIC, mas agora o modelo tem `+ C(bloco)`.
""")
code(r"""
mod_milho = smf.ols("produtividade_kg_ha ~ C(cultivar) + C(bloco)", data=milho).fit()
tab = quadro_anova(mod_milho)
display(tab)
cv_milho = cv(mod_milho, milho["produtividade_kg_ha"])
print(f"CV = {cv_milho:.2f} %")
conferir["2 DBC: F cultivar"] = tab.loc["cultivar", "Fc"]
conferir["2 DBC: p cultivar"] = tab.loc["cultivar", "Pr>Fc"]
conferir["2 DBC: F bloco"] = tab.loc["bloco", "Fc"]
conferir["2 DBC: CV %"] = cv_milho
""")
md(r"""
### 2.2 Pressupostos
> Observação: o `ExpDes.pt` usa, no DBC, o teste de O'Neill-Mathews para homogeneidade. Aqui mostramos Bartlett e Levene, que são os mais comuns. A conclusão é a mesma (variâncias homogêneas).
""")
code(r"""
sw, bt, lv = pressupostos(mod_milho, milho, "produtividade_kg_ha", "cultivar")
conferir["2 DBC: Shapiro p"] = sw
""")
md(r"""
### 2.3 Tukey (com o erro do DBC)
**O que este código faz:** Tukey usando o **QM do resíduo e o GL da ANOVA do DBC** (12 GL), e não o erro de uma ANOVA simples.
""")
code(r"""
letras_milho = tukey_letras(milho, "produtividade_kg_ha", "cultivar", mod_milho.mse_resid, mod_milho.df_resid)
display(letras_milho)
""")
md(r"""
### 2.4 Gráfico
**O que este código faz:** mostra a produtividade de cada cultivar **em cada bloco** (pontos ligados por linha). Se as linhas andam "juntas", o efeito do bloco é parecido para todas as cultivares.
""")
code(r"""
fig, ax = plt.subplots(figsize=(7, 4))
for cult in letras_milho.index:
    sub = milho[milho["cultivar"] == cult].sort_values("bloco")
    ax.plot(sub["bloco"], sub["produtividade_kg_ha"], marker="o",
            label=f"{cult} ({letras_milho.loc[cult, 'Grupo']})")
ax.set_xticks([1, 2, 3, 4])
ax.set_xlabel("Bloco (faixa de declive)")
ax.set_ylabel("Produtividade (kg/ha)")
ax.set_title("Milho em aleias: cultivares por bloco (letras = Tukey 5%)")
ax.legend(fontsize=8)
plt.tight_layout()
plt.show()
""")
md(r"""
**Interpretação:** Híbrido comercial e BRS Gorutuba são os mais produtivos (grupo "a"); o milho crioulo fica sozinho no grupo "c". O efeito de bloco também foi significativo, o que mostra que **usar blocos valeu a pena**.
""")

# ---------------------------------------------------------------- 3 Fatorial
md(r"""
---
## 3. Fatorial 3×3 em DIC: espécie florestal × adubação

**Experimento:** 3 espécies (angico, aroeira, mogno-africano) × 3 adubações (sem adubo, orgânico, mineral) × 4 repetições = 36 vasos. Resposta: massa seca aos 6 meses (g).

**A grande pergunta do fatorial é a INTERAÇÃO:** o efeito da adubação **depende** da espécie? Se a interação for significativa, não dá para falar "o melhor adubo" de forma geral. É preciso fazer o **desdobramento** (analisar um fator **dentro** de cada nível do outro).
""")
code(r"""
fat = carregar("fatorial_adubacao")
display(fat.head())
print(fat.pivot_table(index="especie", columns="adubacao", values="massa_seca_g", aggfunc="mean").round(2))
""")
md(r"""
### 3.1 ANOVA com interação e CV
**O que este código faz:** `C(especie) * C(adubacao)` inclui os dois efeitos principais **e** a interação `especie:adubacao`.
""")
code(r"""
mod_fat = smf.ols("massa_seca_g ~ C(especie) * C(adubacao)", data=fat).fit()
tab = quadro_anova(mod_fat)
display(tab)
cv_fat = cv(mod_fat, fat["massa_seca_g"])
print(f"CV = {cv_fat:.2f} %")
QME_fat, GL_fat = mod_fat.mse_resid, mod_fat.df_resid
conferir["3 Fatorial: F especie"] = tab.loc["especie", "Fc"]
conferir["3 Fatorial: F adubacao"] = tab.loc["adubacao", "Fc"]
conferir["3 Fatorial: F interacao"] = tab.loc["especie:adubacao", "Fc"]
conferir["3 Fatorial: p interacao"] = tab.loc["especie:adubacao", "Pr>Fc"]
conferir["3 Fatorial: CV %"] = cv_fat
""")
md(r"""
### 3.2 Pressupostos
""")
code(r"""
fat["tratamento"] = fat["especie"] + " | " + fat["adubacao"]
sw, bt, lv = pressupostos(mod_fat, fat, "massa_seca_g", "tratamento")
conferir["3 Fatorial: Shapiro p"] = sw
""")
md(r"""
### 3.3 Gráfico de interação
**O que este código faz:** uma linha por espécie. **Linhas paralelas = sem interação. Linhas que se cruzam ou abrem = interação.** Aqui o mogno dispara com adubo mineral, enquanto a aroeira quase não responde.
""")
code(r"""
ordem_adubo = ["sem_adubo", "organico", "mineral"]
medias_fat = fat.groupby(["especie", "adubacao"])["massa_seca_g"].mean().unstack()[ordem_adubo]
fig, ax = plt.subplots(figsize=(7, 4))
for esp, linha in medias_fat.iterrows():
    ax.plot(ordem_adubo, linha.values, marker="o", linewidth=2, label=esp)
ax.set_xlabel("Adubação")
ax.set_ylabel("Massa seca (g)")
ax.set_title("Interação espécie × adubação")
ax.legend(title="Espécie")
plt.tight_layout()
plt.show()
""")
md(r"""
### 3.4 Desdobramento da interação
**O que este código faz:** como a interação foi significativa, para **cada nível de um fator** fazemos uma "mini-ANOVA" do outro fator, sempre usando o **QM do resíduo da ANOVA completa** (27 GL). Se o F do desdobramento for significativo, aplicamos Tukey naquele nível.

Conta da soma de quadrados dentro de um nível: SQ = n × Σ (média da combinação − média do nível)², com n = 4 repetições.
""")
code(r"""
def desdobrar(dados, resposta, fator, dentro, qme, gl, alfa=0.05):
    linhas = []
    for nivel, sub in dados.groupby(dentro):
        medias = sub.groupby(fator)[resposta].mean()
        n = sub.groupby(fator)[resposta].count().iloc[0]
        sq = n * ((medias - sub[resposta].mean()) ** 2).sum()
        glf = len(medias) - 1
        F = (sq / glf) / qme
        p = stats.f.sf(F, glf, gl)
        linhas.append({"Fonte": f"{fator} dentro de {dentro} = {nivel}", "GL": glf, "SQ": sq,
                       "QM": sq / glf, "Fc": F, "Pr>Fc": p})
    tabela = pd.DataFrame(linhas).set_index("Fonte")
    display(tabela.round(4))
    for (nivel, sub), p in zip(dados.groupby(dentro), tabela["Pr>Fc"]):
        print(f"\n>> {fator} dentro de {dentro} = {nivel}")
        if p < alfa:
            display(tukey_letras(sub, resposta, fator, qme, gl, alfa))
        else:
            print("   F não significativo: as médias são estatisticamente iguais.")
            print(sub.groupby(fator)[resposta].mean().round(3).to_string())
    return tabela


print("=== Espécie dentro de cada adubação ===")
d1 = desdobrar(fat, "massa_seca_g", "especie", "adubacao", QME_fat, GL_fat)
""")
code(r"""
print("=== Adubação dentro de cada espécie ===")
d2 = desdobrar(fat, "massa_seca_g", "adubacao", "especie", QME_fat, GL_fat)
conferir["3 Fatorial: F esp. d/ mineral"] = d1.loc["especie dentro de adubacao = mineral", "Fc"]
conferir["3 Fatorial: F adub. d/ aroeira"] = d2.loc["adubacao dentro de especie = aroeira", "Fc"]
conferir["3 Fatorial: p adub. d/ aroeira"] = d2.loc["adubacao dentro de especie = aroeira", "Pr>Fc"]
""")
md(r"""
**Interpretação:** o mogno-africano é a espécie que mais acumula massa em todas as adubações e responde **mais ao adubo mineral** (a > b > c). O angico responde igualmente ao orgânico e ao mineral. A **aroeira não responde à adubação** (p = 0,385). Por isso uma recomendação única de adubo estaria errada.
""")

# ---------------------------------------------------------------- 4 Parcela subdividida
md(r"""
---
## 4. Parcelas subdivididas em DBC: sombreamento × cultivar de café

**Experimento:** 4 blocos. Em cada bloco, 3 **parcelas** recebem um nível de sombreamento por árvores (0, 30 e 50%). Cada parcela é dividida em 3 **subparcelas** com as cultivares de café (Catuaí 144, Arara, Topázio). Resposta: produtividade (sacas/ha).

**Por que é diferente do fatorial comum?** O sombreamento é aplicado em áreas grandes (não dá para sombrear uma linha só de café). Então existem **dois erros**:
- **Erro (a)** = bloco × sombreamento → usado para testar **sombreamento** (e bloco). Tem só 6 GL!
- **Erro (b)** = resíduo → usado para testar **cultivar** e a **interação**.

> Erro comum (inclusive de IAs!): analisar como fatorial simples e testar o sombreamento com o resíduo. Isso dá um F inflado e conclusões erradas.
""")
code(r"""
cafe = carregar("parcela_sub_cafe_sombra")
cafe["sombreamento_pct"] = cafe["sombreamento_pct"].astype(str)   # tratar como categoria
display(cafe.head())
print(cafe.pivot_table(index="sombreamento_pct", columns="cultivar", values="produtividade_sc_ha", aggfunc="mean").round(2))
""")
md(r"""
### 4.1 ANOVA com os dois erros (cálculo manual)
**O que este código faz:**
1. Ajusta um modelo com todos os termos, incluindo `bloco:sombreamento` (que é o erro a).
2. Pega as somas de quadrados desse quadro.
3. **Refaz os testes F**: sombreamento e bloco divididos pelo QM do **erro (a)**; cultivar e interação divididos pelo QM do **erro (b)**.
4. Calcula dois CVs: CV 1 (parcelas, erro a) e CV 2 (subparcelas, erro b).
""")
code(r"""
mod_cafe = smf.ols("produtividade_sc_ha ~ C(bloco) + C(sombreamento_pct) + C(bloco):C(sombreamento_pct)"
                   " + C(cultivar) + C(sombreamento_pct):C(cultivar)", data=cafe).fit()
bruto = sm.stats.anova_lm(mod_cafe, typ=1)
gl, sq = bruto["df"], bruto["sum_sq"]
nomes = {"C(bloco)": "Bloco", "C(sombreamento_pct)": "Sombreamento", "C(bloco):C(sombreamento_pct)": "Erro a",
         "C(cultivar)": "Cultivar", "C(sombreamento_pct):C(cultivar)": "Sombreamento x Cultivar", "Residual": "Erro b"}
gl, sq = gl.rename(nomes), sq.rename(nomes)
qm = sq / gl
QMa, GLa, QMb, GLb = qm["Erro a"], gl["Erro a"], qm["Erro b"], gl["Erro b"]

linhas = []
for fonte, erro in [("Sombreamento", "a"), ("Bloco", "a"), ("Erro a", None),
                    ("Cultivar", "b"), ("Sombreamento x Cultivar", "b"), ("Erro b", None)]:
    if erro is None:
        F = p = np.nan
    else:
        qme, gle = (QMa, GLa) if erro == "a" else (QMb, GLb)
        F = qm[fonte] / qme
        p = stats.f.sf(F, gl[fonte], gle)
    linhas.append({"Fonte": fonte, "GL": gl[fonte], "SQ": sq[fonte], "QM": qm[fonte], "Fc": F, "Pr>Fc": p,
                   "Testado contra": {"a": "Erro a", "b": "Erro b", None: ""}[erro]})
linhas.append({"Fonte": "Total", "GL": gl.sum(), "SQ": sq.sum(), "QM": np.nan, "Fc": np.nan, "Pr>Fc": np.nan, "Testado contra": ""})
tab_cafe = pd.DataFrame(linhas).set_index("Fonte")
display(tab_cafe.round(4))

media_geral = cafe["produtividade_sc_ha"].mean()
cv1, cv2 = 100 * np.sqrt(QMa) / media_geral, 100 * np.sqrt(QMb) / media_geral
print(f"CV 1 (parcelas, erro a)    = {cv1:.2f} %")
print(f"CV 2 (subparcelas, erro b) = {cv2:.2f} %")

conferir["4 Subdividida: F sombreamento"] = tab_cafe.loc["Sombreamento", "Fc"]
conferir["4 Subdividida: p sombreamento"] = tab_cafe.loc["Sombreamento", "Pr>Fc"]
conferir["4 Subdividida: F bloco"] = tab_cafe.loc["Bloco", "Fc"]
conferir["4 Subdividida: F cultivar"] = tab_cafe.loc["Cultivar", "Fc"]
conferir["4 Subdividida: F interacao"] = tab_cafe.loc["Sombreamento x Cultivar", "Fc"]
conferir["4 Subdividida: p interacao"] = tab_cafe.loc["Sombreamento x Cultivar", "Pr>Fc"]
conferir["4 Subdividida: CV1 %"] = cv1
conferir["4 Subdividida: CV2 %"] = cv2
""")
md(r"""
**Para comparar:** se tivéssemos (erradamente) testado o sombreamento contra o erro b, o F seria muito maior. Veja:
""")
code(r"""
F_errado = qm["Sombreamento"] / QMb
print(f"F do sombreamento com erro ERRADO (erro b): {F_errado:.2f}  p = {stats.f.sf(F_errado, 2, GLb):.2e}")
print(f"F do sombreamento com erro CERTO (erro a):  {tab_cafe.loc['Sombreamento', 'Fc']:.2f}  p = {tab_cafe.loc['Sombreamento', 'Pr>Fc']:.4f}")
""")
md(r"""
### 4.2 (Alternativa) Modelo misto
**O que este código faz:** outra forma moderna de analisar parcela subdividida é o **modelo misto**, em que a parcela (bloco × sombreamento) entra como **efeito aleatório**. O teste de Wald conjunto para o sombreamento deve concordar em linhas gerais com o cálculo manual (com dados balanceados, os F dos efeitos de subparcela coincidem).
""")
code(r"""
cafe["parcela"] = cafe["bloco"].astype(str) + "_" + cafe["sombreamento_pct"]
misto = smf.mixedlm("produtividade_sc_ha ~ C(bloco) + C(sombreamento_pct) * C(cultivar)",
                    data=cafe, groups=cafe["parcela"]).fit(reml=True)
print(f"Variância entre parcelas (erro a, componente): {misto.cov_re.iloc[0, 0]:.3f}")
print(f"Variância residual (erro b):                   {misto.scale:.3f}")
print(f"Conferência: (QM erro a - QM erro b) / 3 = {(QMa - QMb) / 3:.3f}  |  QM erro b = {QMb:.3f}")
""")
md(r"""
### 4.3 Desdobramento da interação
**O que este código faz:**
- **Cultivar dentro de cada sombreamento:** usa o **erro b** (18 GL), com a mesma função `desdobrar` do fatorial.
- **Sombreamento dentro de cada cultivar:** mistura parcelas diferentes, então usa um **erro combinado** = (QMa + (c − 1)·QMb) / c, onde c = 3 cultivares, com GL calculado pela fórmula de **Satterthwaite**. É exatamente o que o `ExpDes.pt` faz.
""")
code(r"""
print("=== Cultivar dentro de cada sombreamento (erro b) ===")
d_cult = desdobrar(cafe, "produtividade_sc_ha", "cultivar", "sombreamento_pct", QMb, GLb)
""")
code(r"""
c = cafe["cultivar"].nunique()
QM_comb = (QMa + (c - 1) * QMb) / c
GL_comb = (QMa + (c - 1) * QMb) ** 2 / (QMa ** 2 / GLa + ((c - 1) * QMb) ** 2 / GLb)
print(f"Erro combinado: QM = {QM_comb:.4f}, GL (Satterthwaite) = {GL_comb:.3f}\n")
print("=== Sombreamento dentro de cada cultivar (erro combinado) ===")
d_somb = desdobrar(cafe, "produtividade_sc_ha", "sombreamento_pct", "cultivar", QM_comb, GL_comb)
conferir["4 Subdividida: F somb. d/ Topazio"] = d_somb.loc["sombreamento_pct dentro de cultivar = Topazio", "Fc"]
conferir["4 Subdividida: F cult. d/ 30%"] = d_cult.loc["cultivar dentro de sombreamento_pct = 30", "Fc"]
""")
md(r"""
> Como o sombreamento é **quantitativo** (0, 30, 50%), o `ExpDes.pt` ajusta uma regressão para a Topázio em vez do Tukey. Com apenas 3 níveis, o mais honesto é descrever a tendência: a Topázio produz mais com sombra.

### 4.4 Gráfico
""")
code(r"""
ordem_s = ["0", "30", "50"]
medias_cafe = cafe.groupby(["cultivar", "sombreamento_pct"])["produtividade_sc_ha"].mean().unstack()[ordem_s]
fig, ax = plt.subplots(figsize=(7, 4))
for cult, linha in medias_cafe.iterrows():
    ax.plot([0, 30, 50], linha.values, marker="o", linewidth=2, label=cult)
ax.set_xticks([0, 30, 50])
ax.set_xlabel("Sombreamento (%)")
ax.set_ylabel("Produtividade (sc/ha)")
ax.set_title("Café sombreado: interação sombreamento × cultivar")
ax.legend(title="Cultivar")
plt.tight_layout()
plt.show()
""")
md(r"""
**Interpretação:** o sombreamento tem efeito significativo (p = 0,032, testado corretamente com o erro a). A interação é significativa: a **Arara** é sempre a melhor ou empatada, e a **Topázio** é a mais prejudicada a pleno sol, melhorando com sombra.
""")

# ---------------------------------------------------------------- 5 Doses
md(r"""
---
## 5. Regressão: doses de nitrogênio no eucalipto (ILPF)

**Experimento:** 5 doses de N em cobertura (0, 50, 100, 150, 200 kg/ha) × 4 repetições em DIC. Resposta: volume de madeira (m³/ha).

**Por que regressão e não Tukey?** Dose é um número. Perguntar "a dose 100 difere da 150?" desperdiça informação. O certo é ajustar uma **curva** e achar a **dose de máxima eficiência técnica (MET)**.

Modelo quadrático: volume = b0 + b1·dose + b2·dose². Se b2 < 0, a curva tem um ponto máximo em **MET = −b1 / (2·b2)**.
""")
code(r"""
doses = carregar("doses_nitrogenio")
display(doses.head())
print(doses.groupby("dose_n_kg_ha")["volume_m3_ha"].mean().round(2))
""")
md(r"""
### 5.1 ANOVA (dose como categoria), pressupostos e CV
""")
code(r"""
mod_dose_cat = smf.ols("volume_m3_ha ~ C(dose_n_kg_ha)", data=doses).fit()
tab = quadro_anova(mod_dose_cat)
display(tab)
cv_dose = cv(mod_dose_cat, doses["volume_m3_ha"])
print(f"CV = {cv_dose:.2f} %")
sw, bt, lv = pressupostos(mod_dose_cat, doses, "volume_m3_ha", "dose_n_kg_ha")
QME_d, GL_d, SQ_trat = mod_dose_cat.mse_resid, mod_dose_cat.df_resid, tab.iloc[0]["SQ"]
conferir["5 Doses: F tratamento"] = tab.iloc[0]["Fc"]
conferir["5 Doses: CV %"] = cv_dose
""")
md(r"""
### 5.2 Regressões linear e quadrática
**O que este código faz:** ajusta as duas curvas, decompõe a soma de quadrados dos tratamentos em **efeito linear**, **efeito quadrático** e **desvios da regressão**, e testa cada parte com o QM do resíduo da ANOVA (como no `ExpDes.pt`/SISVAR).

- O **R²** é calculado sobre as **médias** das doses (SQ da regressão ÷ SQ de tratamentos), como no `ExpDes.pt`.
- **Desvios não significativos** = a curva explica bem as médias.
""")
code(r"""
lin = smf.ols("volume_m3_ha ~ dose_n_kg_ha", data=doses).fit()
quad = smf.ols("volume_m3_ha ~ dose_n_kg_ha + I(dose_n_kg_ha**2)", data=doses).fit()
print("Linear:     ", lin.params.round(5).to_dict())
print("Quadrático: ", quad.params.round(6).to_dict())

sq_lin = lin.ess
sq_quad = quad.ess - lin.ess
sq_desv = SQ_trat - quad.ess
decomp = pd.DataFrame({
    "GL": [1, 1, 2, GL_d],
    "SQ": [sq_lin, sq_quad, sq_desv, QME_d * GL_d],
}, index=["Efeito linear", "Efeito quadrático", "Desvios da regressão", "Resíduo"])
decomp["QM"] = decomp["SQ"] / decomp["GL"]
decomp["Fc"] = decomp["QM"] / QME_d
decomp["Pr>Fc"] = stats.f.sf(decomp["Fc"], decomp["GL"], GL_d)
decomp.loc["Resíduo", ["Fc", "Pr>Fc"]] = np.nan
display(decomp.round(4))

r2_lin, r2_quad = sq_lin / SQ_trat, quad.ess / SQ_trat
b0, b1, b2 = quad.params
MET = -b1 / (2 * b2)
vol_max = b0 + b1 * MET + b2 * MET ** 2
print(f"R² linear = {r2_lin:.4f} | R² quadrático = {r2_quad:.4f}")
print(f"Equação: volume = {b0:.4f} + {b1:.5f}·dose {b2:+.7f}·dose²")
print(f"Dose de máxima eficiência técnica (MET) = {MET:.1f} kg/ha de N  ->  volume estimado = {vol_max:.1f} m³/ha")

conferir["5 Doses: F efeito linear"] = decomp.loc["Efeito linear", "Fc"]
conferir["5 Doses: F efeito quadratico"] = decomp.loc["Efeito quadrático", "Fc"]
conferir["5 Doses: R2 quadratico"] = r2_quad
conferir["5 Doses: b1"] = b1
conferir["5 Doses: MET kg/ha"] = MET
""")
md(r"""
### 5.3 Gráfico
**O que este código faz:** pontos = parcelas; quadrados = médias; linha = curva quadrática; tracejado = dose de máxima eficiência.
""")
code(r"""
x = np.linspace(0, 200, 200)
medias_d = doses.groupby("dose_n_kg_ha")["volume_m3_ha"].mean()
fig, ax = plt.subplots(figsize=(7, 4))
ax.scatter(doses["dose_n_kg_ha"], doses["volume_m3_ha"], alpha=0.5, label="Parcelas")
ax.scatter(medias_d.index, medias_d.values, marker="s", s=60, color="black", label="Médias")
ax.plot(x, b0 + b1 * x + b2 * x ** 2, color="#c0392b", label=f"Quadrática (R² = {r2_quad:.3f})")
ax.axvline(MET, linestyle="--", color="gray")
ax.text(MET - 3, ax.get_ylim()[0] + 1, f"MET = {MET:.0f} kg/ha", ha="right")
ax.set_xlabel("Dose de N (kg/ha)")
ax.set_ylabel("Volume (m³/ha)")
ax.set_title("Eucalipto em ILPF: resposta a doses de nitrogênio")
ax.legend()
plt.tight_layout()
plt.show()
""")
md(r"""
**Interpretação:** o efeito quadrático é significativo e os desvios não são, então a parábola descreve bem a resposta (R² = 0,99). A produção máxima ocorre por volta de **171 kg/ha de N**. Lembre que a **dose econômica** costuma ser menor que a MET, pois depende do preço do adubo e da madeira.
""")

# ---------------------------------------------------------------- 6 Pragas
md(r"""
---
## 6. Contagem de pragas: quando os pressupostos falham

**Experimento:** 4 manejos (convencional, SAF simples, SAF biodiverso, pousio) × 6 armadilhas em DIC. Resposta: número de insetos-praga por armadilha.

**Por que este exemplo?** Dados de **contagem** quase nunca são normais e, onde a média é maior, a variação também é maior. Isso viola a **homogeneidade das variâncias**. Vamos ver: (1) a falha, (2) a correção por **transformação raiz(x + 0,5)** e (3) a alternativa **não paramétrica** (Kruskal-Wallis).
""")
code(r"""
pragas = carregar("dic_contagem_pragas")
display(pragas.head())
print(pragas.groupby("manejo")["insetos_praga"].agg(["mean", "var"]).round(2))
print("\nRepare: a variância cresce junto com a média (típico de contagens).")
""")
md(r"""
### 6.1 ANOVA nos dados originais: veja o diagnóstico
""")
code(r"""
mod_pragas = smf.ols("insetos_praga ~ C(manejo)", data=pragas).fit()
tab = quadro_anova(mod_pragas)
display(tab)
cv_pragas = cv(mod_pragas, pragas["insetos_praga"])
print(f"CV = {cv_pragas:.2f} %   <- muito alto!")
sw, bt, lv = pressupostos(mod_pragas, pragas, "insetos_praga", "manejo")
conferir["6 Pragas: F original"] = tab.loc["manejo", "Fc"]
conferir["6 Pragas: CV original %"] = cv_pragas
conferir["6 Pragas: Bartlett p original"] = bt
""")
md(r"""
**Diagnóstico:** o teste de Bartlett deu p < 0,05, então **as variâncias não são homogêneas** e o CV passa de 50%. A ANOVA "crua" não é confiável.

### 6.2 Transformação raiz(x + 0,5)
**O que este código faz:** cria uma nova coluna com a raiz quadrada da contagem + 0,5 (o 0,5 evita problemas com zeros), refaz ANOVA, pressupostos, CV e Tukey nessa escala.
""")
code(r"""
pragas["raiz"] = np.sqrt(pragas["insetos_praga"] + 0.5)
mod_raiz = smf.ols("raiz ~ C(manejo)", data=pragas).fit()
tab = quadro_anova(mod_raiz)
display(tab)
cv_raiz = cv(mod_raiz, pragas["raiz"])
print(f"CV = {cv_raiz:.2f} %")
sw, bt, lv = pressupostos(mod_raiz, pragas, "raiz", "manejo")
print()
print(pairwise_tukeyhsd(pragas["raiz"], pragas["manejo"], alpha=0.05))
display(tukey_letras(pragas, "raiz", "manejo", mod_raiz.mse_resid, mod_raiz.df_resid))
conferir["6 Pragas: F raiz"] = tab.loc["manejo", "Fc"]
conferir["6 Pragas: CV raiz %"] = cv_raiz
conferir["6 Pragas: Bartlett p raiz"] = bt
""")
md(r"""
### 6.3 Alternativa não paramétrica: Kruskal-Wallis
**O que este código faz:** o Kruskal-Wallis compara os manejos usando a **ordem (posto)** dos valores, sem exigir normalidade nem variâncias iguais.
""")
code(r"""
grupos = [g["insetos_praga"].to_numpy(dtype=float) for _, g in pragas.groupby("manejo")]
kw = stats.kruskal(*grupos)
print(f"Kruskal-Wallis: H = {kw.statistic:.3f}, GL = {len(grupos) - 1}, p = {kw.pvalue:.6f}")
conferir["6 Pragas: Kruskal H"] = kw.statistic
conferir["6 Pragas: Kruskal p"] = kw.pvalue
""")
md(r"""
### 6.4 Gráfico: antes e depois da transformação
""")
code(r"""
ordem_m = ["convencional", "pousio", "saf_simples", "saf_biodiverso"]
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].boxplot([pragas.loc[pragas.manejo == m, "insetos_praga"] for m in ordem_m])
axes[0].set_title("Original: caixas de tamanhos muito diferentes")
axes[0].set_ylabel("Insetos-praga por armadilha")
axes[1].boxplot([pragas.loc[pragas.manejo == m, "raiz"] for m in ordem_m])
axes[1].set_title("Raiz(x + 0,5): variação mais parecida")
axes[1].set_ylabel("raiz(insetos + 0,5)")
for ax in axes:
    ax.set_xticks(range(1, 5), ordem_m, rotation=20)
plt.tight_layout()
plt.show()
""")
md(r"""
**Interpretação:** depois da transformação, os pressupostos passam a ser atendidos e o efeito dos manejos fica ainda mais claro. O **SAF biodiverso** tem significativamente menos pragas que todos os outros manejos, e o convencional tem mais que o SAF simples. O Kruskal-Wallis chega à mesma conclusão (p ≈ 0,002). Ao apresentar, mostre as **médias originais** (insetos/armadilha) com as letras obtidas na escala transformada.

> Uma alternativa mais avançada para contagens é o **modelo linear generalizado (GLM) Poisson ou binomial negativo**. Vale pedir à IA que explique quando usar.
""")

# ---------------------------------------------------------------- Conferência
md(r"""
---
## 7. Conferência com o gabarito do R (`ExpDes.pt`)

**O que este código faz:** compara os números calculados aqui em Python com os obtidos no R (arquivo `dados/gabarito_resultados.txt`, gerado por `notebooks/analise_exemplos.R`). **É exatamente isso que você deve fazer com qualquer resultado de IA: conferir com uma fonte confiável.**

Pequenas diferenças na 3ª ou 4ª casa decimal vêm de arredondamento na impressão do R (ex.: o R mostra o p do DBC como 0.0000017; o valor exato é 1,66 × 10⁻⁶).
""")
code(r"""
gabarito_R = {
    "1 DIC: F substrato": 34.573, "1 DIC: p substrato": 2.0868e-07, "1 DIC: CV %": 6.1,
    "1 DIC: Shapiro p": 0.8071113, "1 DIC: Bartlett p": 0.09455033,
    "2 DBC: F cultivar": 34.686, "2 DBC: p cultivar": 0.0000017, "2 DBC: F bloco": 7.731,
    "2 DBC: CV %": 5.04, "2 DBC: Shapiro p": 0.313313,
    "3 Fatorial: F especie": 111.098, "3 Fatorial: F adubacao": 53.064, "3 Fatorial: F interacao": 15.714,
    "3 Fatorial: p interacao": 9.3204e-07, "3 Fatorial: CV %": 8.55, "3 Fatorial: Shapiro p": 0.4999856,
    "3 Fatorial: F esp. d/ mineral": 94.3217, "3 Fatorial: F adub. d/ aroeira": 0.9883,
    "3 Fatorial: p adub. d/ aroeira": 0.3853,
    "4 Subdividida: F sombreamento": 6.477, "4 Subdividida: p sombreamento": 0.031721,
    "4 Subdividida: F bloco": 4.376, "4 Subdividida: F cultivar": 78.611,
    "4 Subdividida: F interacao": 5.968, "4 Subdividida: p interacao": 0.003075,
    "4 Subdividida: CV1 %": 9.472102, "4 Subdividida: CV2 %": 3.724808,
    "4 Subdividida: F somb. d/ Topazio": 12.128865, "4 Subdividida: F cult. d/ 30%": 7.622929,
    "5 Doses: F tratamento": 32.55, "5 Doses: CV %": 5.14, "5 Doses: F efeito linear": 110.27,
    "5 Doses: F efeito quadratico": 18.9, "5 Doses: R2 quadratico": 0.992103, "5 Doses: b1": 0.2192,
    "5 Doses: MET kg/ha": 171.4,
    "6 Pragas: F original": 9.6159, "6 Pragas: CV original %": 52.03, "6 Pragas: Bartlett p original": 0.01982546,
    "6 Pragas: F raiz": 13.662, "6 Pragas: CV raiz %": 25.14, "6 Pragas: Bartlett p raiz": 0.4970718,
    "6 Pragas: Kruskal H": 15.201, "6 Pragas: Kruskal p": 0.001653,
}
comp = pd.DataFrame({"Python": pd.Series(conferir), "R (gabarito)": pd.Series(gabarito_R)})
comp["Diferença relativa %"] = 100 * (comp["Python"] - comp["R (gabarito)"]).abs() / comp["R (gabarito)"].abs()
# critério: diferença relativa < 1% OU diferença absoluta < 1e-6 (p-valores minúsculos que o R imprime arredondados)
comp["Bate?"] = np.where((comp["Diferença relativa %"] < 1) | ((comp["Python"] - comp["R (gabarito)"]).abs() < 1e-6), "sim", "NÃO")
with pd.option_context("display.float_format", "{:.6g}".format):
    display(comp)
print(f"\n{(comp['Bate?'] == 'sim').sum()} de {len(comp)} valores conferem com o R.")
""")

# ---------------------------------------------------------------- R opcional
md(r"""
---
## 8. (Opcional) A mesma análise em R, dentro do Colab

**O que este código faz:** o Colab também roda **R** dentro de um notebook Python, pela ponte `rpy2`. A primeira célula ativa a ponte; a segunda (que começa com `%%R`) é **código R puro**, usando o pacote `ExpDes.pt`, padrão em agronomia no Brasil.

> Essas células **não** foram executadas na preparação deste material. No Colab, a instalação do `ExpDes.pt` leva alguns minutos. Os dados precisam estar na pasta `dados/` ou em `/content` (ajuste o caminho).
""")
code(r"""
# Ativa a "ponte" Python -> R (o rpy2 já vem instalado no Colab)
%load_ext rpy2.ipython
""", tags=["nao-executar"])
code(r"""
%%R
if (!requireNamespace("ExpDes.pt", quietly = TRUE)) install.packages("ExpDes.pt")
library(ExpDes.pt)

pasta <- if (dir.exists("dados")) "dados" else if (dir.exists("../dados")) "../dados" else "/content"
ler <- function(nome) read.csv(file.path(pasta, paste0(nome, ".csv")))

# DIC: substratos de mudas
d <- ler("dic_mudas")
dic(d$substrato, d$altura_cm, quali = TRUE, mcomp = "tukey")

# Fatorial com desdobramento automático
d <- ler("fatorial_adubacao")
fat2.dic(d$especie, d$adubacao, d$massa_seca_g, quali = c(TRUE, TRUE),
         mcomp = "tukey", fac.names = c("Especie", "Adubacao"))

# Parcela subdividida (erro a e erro b automáticos)
d <- ler("parcela_sub_cafe_sombra")
psub2.dbc(d$sombreamento_pct, d$cultivar, d$bloco, d$produtividade_sc_ha,
          quali = c(FALSE, TRUE), mcomp = "tukey", fac.names = c("Sombreamento", "Cultivar"))
""", tags=["nao-executar"])

# ---------------------------------------------------------------- Gemini
md(r"""
---
## 9. Peça ao Gemini no Colab (Data Science Agent)

No Colab, clique no botão **Gemini** (✦, no canto inferior ou superior direito) e escreva o pedido em português. O **Data Science Agent** cria as células de código, executa e explica. **Antes**, carregue o arquivo no painel 📁 Arquivos. Depois, **confira** os números com este notebook (seção 7).

Copie e cole um dos pedidos abaixo:

**1. DIC (mudas)**
```
Você é um estatístico experimental da área agroflorestal. Carregue o arquivo dic_mudas.csv. É um experimento em DIC com 5 substratos (coluna substrato) e 4 repetições; a variável resposta é altura_cm. Faça: (1) ANOVA com quadro completo (GL, SQ, QM, F, p); (2) teste de Shapiro-Wilk nos resíduos e Bartlett para homogeneidade; (3) CV%; (4) teste de Tukey a 5% com letras; (5) gráfico de barras com as letras. Explique os resultados em português simples, como para um produtor rural.
```

**2. DBC (milho)**
```
Carregue dbc_milho.csv. É um experimento em blocos casualizados (DBC): 5 cultivares (coluna cultivar) em 4 blocos (coluna bloco); resposta produtividade_kg_ha. Faça a ANOVA incluindo o efeito de bloco, verifique os pressupostos, calcule o CV% e aplique Tukey a 5% usando o quadrado médio do resíduo da ANOVA do DBC (não use um Tukey que ignore os blocos). Mostre o código e diga se valeu a pena usar blocos.
```

**3. Fatorial com desdobramento**
```
Carregue fatorial_adubacao.csv: fatorial 3x3 em DIC, fatores especie e adubacao, 4 repetições, resposta massa_seca_g. Faça a ANOVA com interação. Se a interação for significativa a 5%, faça o desdobramento: espécie dentro de cada adubação e adubação dentro de cada espécie, usando o QM do resíduo da ANOVA completa, com Tukey nos casos significativos. Faça um gráfico de interação e interprete.
```

**4. Parcela subdividida**
```
Carregue parcela_sub_cafe_sombra.csv. É um experimento em parcelas subdivididas em DBC: parcela = sombreamento_pct (0, 30, 50%), subparcela = cultivar de café, 4 blocos, resposta produtividade_sc_ha. Faça a ANOVA com dois erros: erro (a) = bloco x sombreamento para testar sombreamento e bloco; erro (b) = resíduo para cultivar e interação. Mostre o CV da parcela e da subparcela. Não analise como fatorial simples. Depois desdobre a interação e faça um gráfico.
```

**5. Regressão de doses**
```
Carregue doses_nitrogenio.csv: doses de N (dose_n_kg_ha = 0, 50, 100, 150, 200) em DIC com 4 repetições; resposta volume_m3_ha. Como a dose é quantitativa, NÃO use Tukey. Faça a ANOVA, ajuste regressões linear e quadrática, teste os efeitos linear, quadrático e os desvios da regressão com o QM do resíduo, informe o R², a equação e a dose de máxima eficiência técnica (MET = -b1/(2*b2)). Faça o gráfico com a curva e a MET marcada.
```

**6. Pressupostos violados (contagens)**
```
Carregue dic_contagem_pragas.csv: DIC com 4 manejos (coluna manejo) e 6 repetições; resposta insetos_praga (contagem). Faça a ANOVA e teste os pressupostos (Shapiro-Wilk e Bartlett). Se algum pressuposto falhar, explique por que isso é comum em contagens, aplique a transformação raiz(x + 0,5) e refaça a análise com Tukey, e rode também o teste de Kruskal-Wallis. Compare as conclusões e faça boxplots antes e depois da transformação.
```

> **Checklist depois da resposta da IA:** o GL do resíduo está certo? Ela usou o erro certo (bloco, erro a)? Mostrou o CV? Testou pressupostos? Os números batem com o gabarito? Peça sempre: *"mostre o código que você usou"*.
""")

nb = nbf.v4.new_notebook()
nb.cells = cells
nb.metadata = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python"},
    "colab": {"provenance": [], "toc_visible": True},
}

# ---- execução: pula células marcadas "nao-executar"
exec_nb = copy.deepcopy(nb)
pulos = [i for i, c in enumerate(exec_nb.cells) if "nao-executar" in c.metadata.get("tags", [])]
for i in pulos:
    exec_nb.cells[i].source = "pass  # célula R: não executada aqui"
client = NotebookClient(exec_nb, timeout=600, kernel_name="python3",
                        resources={"metadata": {"path": str(RAIZ / "notebooks")}})
client.execute()
for i, (c_orig, c_exec) in enumerate(zip(nb.cells, exec_nb.cells)):
    if c_orig.cell_type == "code" and i not in pulos:
        c_orig.outputs = c_exec.outputs
        c_orig.execution_count = c_exec.execution_count
nbf.write(nb, SAIDA)
print("Notebook salvo em", SAIDA)
