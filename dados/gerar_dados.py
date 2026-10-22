"""Gera os conjuntos de dados fictícios do curso "IA para Estatística Experimental".

Todos os dados são simulados (seed fixa) com efeitos realistas para exemplos
agroflorestais. Formato longo: 1 linha = 1 parcela (unidade experimental).
Uso: python gerar_dados.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

rng = np.random.default_rng(2026)
PASTA = Path(__file__).parent


def salvar(df, nome):
    df.to_csv(PASTA / f"{nome}.csv", index=False)
    df.to_excel(PASTA / f"{nome}.xlsx", index=False)


# 1) DIC: substratos na produção de mudas de ipê-amarelo (altura aos 120 dias)
substratos = {"terra": 28.0, "terra_esterco": 36.0, "comercial": 34.0,
              "composto_organico": 39.0, "terra_areia": 25.0}
linhas = []
for trat, media in substratos.items():
    for rep in range(1, 5):
        alt = media + rng.normal(0, 2.6)
        diam = 0.12 * alt + rng.normal(0, 0.35)
        linhas.append({"substrato": trat, "repeticao": rep,
                       "altura_cm": round(alt, 1), "diametro_mm": round(diam, 2)})
salvar(pd.DataFrame(linhas), "dic_mudas")

# 2) DBC: cultivares de milho em aleias de gliricídia, blocos = faixas de declive
cultivares = {"BRS_Caimbe": 5200, "AL_Bandeirante": 4800, "BRS_Gorutuba": 5600,
              "Crioulo_local": 4300, "Hibrido_comercial": 6100}
efeito_bloco = {1: 350, 2: 120, 3: -150, 4: -320}
linhas = []
for cult, media in cultivares.items():
    for bloco, eb in efeito_bloco.items():
        prod = media + eb + rng.normal(0, 260)
        linhas.append({"bloco": bloco, "cultivar": cult,
                       "produtividade_kg_ha": round(prod)})
salvar(pd.DataFrame(linhas), "dbc_milho")

# 3) Fatorial 3x3 em DIC: adubação x espécie florestal (massa seca aos 6 meses)
especies = {"angico": 0, "aroeira": -4, "mogno_africano": 3}
adubos = {"sem_adubo": 18, "organico": 26, "mineral": 25}
# interação: mogno responde mais ao mineral, aroeira quase não responde
interacao = {("mogno_africano", "mineral"): 6, ("aroeira", "organico"): -5,
             ("aroeira", "mineral"): -6}
linhas = []
for esp, ee in especies.items():
    for adu, ea in adubos.items():
        for rep in range(1, 5):
            ms = ea + ee + interacao.get((esp, adu), 0) + rng.normal(0, 1.8)
            linhas.append({"especie": esp, "adubacao": adu, "repeticao": rep,
                           "massa_seca_g": round(ms, 1)})
salvar(pd.DataFrame(linhas), "fatorial_adubacao")

# 4) Parcela subdividida em DBC: sombreamento (parcela) x cultivar de café (subparcela)
sombras = {0: 0, 30: 2.5, 50: 1.0}
cafes = {"Catuai_144": 30, "Arara": 32, "Topazio": 28}
inter_sc = {(50, "Arara"): 3.0, (0, "Topazio"): -2.5}
linhas = []
for bloco in range(1, 5):
    eb = rng.normal(0, 1.5)
    for sombra, es in sombras.items():
        erro_parcela = rng.normal(0, 1.4)  # erro (a)
        for cafe, ec in cafes.items():
            prod = ec + es + eb + inter_sc.get((sombra, cafe), 0) + erro_parcela + rng.normal(0, 1.1)
            linhas.append({"bloco": bloco, "sombreamento_pct": sombra, "cultivar": cafe,
                           "produtividade_sc_ha": round(prod, 1)})
salvar(pd.DataFrame(linhas), "parcela_sub_cafe_sombra")

# 5) Regressão: doses de N em cobertura no eucalipto em ILPF (resposta quadrática)
linhas = []
for dose in [0, 50, 100, 150, 200]:
    for rep in range(1, 5):
        vol = 42 + 0.22 * dose - 0.00072 * dose ** 2 + rng.normal(0, 2.2)
        linhas.append({"dose_n_kg_ha": dose, "repeticao": rep, "volume_m3_ha": round(vol, 1)})
salvar(pd.DataFrame(linhas), "doses_nitrogenio")

# 6) DIC com contagem (viola pressupostos): insetos por armadilha em 4 manejos de SAF
manejos = {"convencional": 22, "saf_simples": 9, "saf_biodiverso": 4, "pousio": 12}
linhas = []
for man, lam in manejos.items():
    for rep in range(1, 7):
        linhas.append({"manejo": man, "repeticao": rep,
                       "insetos_praga": int(rng.negative_binomial(3, 3 / (3 + lam)))})
salvar(pd.DataFrame(linhas), "dic_contagem_pragas")

# 7) Planilha de campo "bagunçada" (formato largo, nomes ruins) para exercício de organização
dic = pd.read_csv(PASTA / "dic_mudas.csv")
largo = dic.pivot(index="substrato", columns="repeticao", values="altura_cm").reset_index()
largo.columns = ["Substrato usado", "Rep 1 (cm)", "Rep 2 (cm)", "Rep 3 (cm)", "Rep 4 (cm)"]
largo["Substrato usado"] = ["comercial ", "Composto Orgânico", "Terra", "terra + areia", "Terra c/ esterco"]
largo = largo.astype(str).apply(lambda col: col.str.replace(".", ",", regex=False))
largo.loc[1, "Rep 3 (cm)"] = "perdida"
largo.to_excel(PASTA / "planilha_campo_baguncada.xlsx", index=False)

print("Arquivos gerados em", PASTA)
