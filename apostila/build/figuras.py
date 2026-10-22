#!/usr/bin/env python3
"""Gera as figuras da apostila (PNG, 300 dpi, 16 cm de largura) em apostila/figuras/.

Estilo ABNT: preto e branco/tons de cinza, sem 3D, sem título dentro da
imagem (o título vai na legenda, acima da figura), eixos com unidade,
vírgula decimal (formatador próprio, não depende do locale) e fonte serifada.

As médias são recalculadas dos CSVs em dados/ e conferidas com os valores
publicados nas tabelas da apostila (2 casas decimais); qualquer diferença
interrompe o script.

Uso: python3 apostila/build/figuras.py
Requisitos: matplotlib, pandas, numpy.
"""
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd

BUILD = Path(__file__).resolve().parent
APOST = BUILD.parent
DADOS = APOST.parent / 'dados'
OUT = APOST / 'figuras'
OUT.mkdir(exist_ok=True)

CM = 1 / 2.54
LARG = 16 * CM
DPI = 300

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['DejaVu Serif'],
    'font.size': 10,
    'axes.labelsize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'axes.edgecolor': 'black',
    'axes.linewidth': 0.8,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'xtick.color': 'black',
    'ytick.color': 'black',
    'axes.unicode_minus': False,
    'savefig.dpi': DPI,
    'savefig.facecolor': 'white',
    'figure.facecolor': 'white',
    'legend.frameon': False,
})


def br(x, casas=None):
    """Número no padrão brasileiro: vírgula decimal, ponto de milhar."""
    if casas is None:
        s = f'{x:g}' if abs(x) < 1e6 else f'{x:.0f}'
        if 'e' in s:
            s = f'{x:.6f}'.rstrip('0').rstrip('.')
        inteiro, _, dec = s.partition('.')
    else:
        s = f'{x:.{casas}f}'
        inteiro, _, dec = s.partition('.')
    sinal = '−' if inteiro.startswith('-') else ''
    inteiro = inteiro.lstrip('-')
    inteiro = f'{int(inteiro):,}'.replace(',', '.')
    return sinal + inteiro + (',' + dec if dec else '')


FMT = FuncFormatter(lambda x, pos: br(round(x, 6)))


def salvar(fig, nome):
    fig.savefig(OUT / nome, dpi=DPI)
    plt.close(fig)
    print('  ', OUT / nome)


def conferir(nome, calculado, esperado, casas=2):
    tol = 0.5 * 10 ** -casas + 1e-9
    for k, v in esperado.items():
        c = calculado[k]
        if abs(c - v) > tol:   # igual a 2 casas (meio arredondado para cima)
            raise SystemExit(f'{nome}: média de {k} = {c:.4f}, esperado {v}')
    print(f'{nome}: médias conferem com a apostila')


def barras_letras(df, col_trat, col_y, ordem, rotulos, letras, esperado, ylabel,
                  nome, casas, ymax=None, xlabel=None):
    m = df.groupby(col_trat)[col_y].mean()
    conferir(nome, m, esperado)
    vals = [m[k] for k in ordem]
    fig, ax = plt.subplots(figsize=(LARG, 8.5 * CM))
    x = np.arange(len(ordem))
    ax.bar(x, vals, width=0.6, color='0.75', edgecolor='black', linewidth=0.8)
    topo = ymax or max(vals) * 1.15
    for xi, v, l in zip(x, vals, letras):
        ax.text(xi, v + topo * 0.015, f'{br(v, casas)} {l}', ha='center', va='bottom', fontsize=9)
    ax.set_xticks(x, rotulos)
    ax.set_ylim(0, topo)
    ax.set_ylabel(ylabel)
    if xlabel:
        ax.set_xlabel(xlabel)
    ax.yaxis.set_major_formatter(FMT)
    fig.tight_layout()
    salvar(fig, nome)


def fig_dic_mudas():
    df = pd.read_csv(DADOS / 'dic_mudas.csv')
    ordem = ['composto_organico', 'terra_esterco', 'comercial', 'terra', 'terra_areia']
    esperado = dict(zip(ordem, [37.40, 36.35, 33.23, 26.48, 24.98]))
    # 33,225 e 24,975 arredondam para cima nas tabelas (ExpDes.pt): tolerância de 0,005
    barras_letras(df, 'substrato', 'altura_cm', ordem,
                  ['Composto\norgânico', 'Terra +\nesterco', 'Comercial', 'Terra', 'Terra +\nareia'],
                  ['a', 'a', 'a', 'b', 'b'], esperado, 'Altura das mudas (cm)',
                  'fig_dic_mudas.png', 2, ymax=45, xlabel='Substrato')


def fig_dbc_milho():
    df = pd.read_csv(DADOS / 'dbc_milho.csv')
    ordem = ['Hibrido_comercial', 'BRS_Gorutuba', 'BRS_Caimbe', 'AL_Bandeirante', 'Crioulo_local']
    m = df.groupby('cultivar')['produtividade_kg_ha'].mean()
    esperado = dict(zip(ordem, [6147, 6130, 5213, 4974, 4291]))
    for k, v in esperado.items():   # tabela publicada com 0 casas
        if round(m[k]) != v:
            raise SystemExit(f'milho: {k} = {m[k]:.2f}, esperado {v}')
    esperado = {k: m[k] for k in ordem}
    barras_letras(df, 'cultivar', 'produtividade_kg_ha', ordem,
                  ['Híbrido\ncomercial', 'BRS\nGorutuba', 'BRS\nCaimbé', 'AL\nBandeirante', 'Crioulo\nlocal'],
                  ['a', 'a', 'b', 'b', 'c'], esperado, 'Produtividade de grãos (kg ha⁻¹)',
                  'fig_dbc_milho.png', 0, ymax=7200, xlabel='Cultivar')


def fig_fatorial():
    df = pd.read_csv(DADOS / 'fatorial_adubacao.csv')
    m = df.groupby(['especie', 'adubacao'])['massa_seca_g'].mean()
    niveis = ['sem_adubo', 'organico', 'mineral']
    esperado = {
        'angico': [16.03, 26.03, 23.43],
        'aroeira': [15.48, 17.13, 15.58],
        'mogno_africano': [20.23, 28.33, 33.60],
    }
    especies = sorted(df['especie'].unique())
    alvo = {}
    for e in especies:
        chave = 'mogno_africano' if e.startswith('mogno') else e
        for n, v in zip(niveis, esperado[chave]):
            alvo[(e, n)] = v
    conferir('fig_fatorial.png', m, alvo)
    estilos = {
        'angico': ('o', '-', 'Angico'),
        'aroeira': ('s', '--', 'Aroeira'),
    }
    fig, ax = plt.subplots(figsize=(LARG, 8.5 * CM))
    x = np.arange(3)
    for e in especies:
        mk, ls, nome = estilos.get(e, ('^', ':', 'Mogno-africano'))
        ax.plot(x, [m[(e, n)] for n in niveis], marker=mk, linestyle=ls, color='black',
                markerfacecolor='white' if mk == 's' else 'black', markersize=6, linewidth=1.2,
                label=nome)
    ax.set_xticks(x, ['Sem adubo', 'Orgânico', 'Mineral'])
    ax.set_xlim(-0.3, 2.3)
    ax.set_ylim(10, 36)
    ax.set_xlabel('Adubação')
    ax.set_ylabel('Massa seca das mudas (g)')
    ax.yaxis.set_major_formatter(FMT)
    ax.legend(title='Espécie', loc='upper left', title_fontsize=9)
    fig.tight_layout()
    salvar(fig, 'fig_fatorial.png')


def fig_cafe():
    df = pd.read_csv(DADOS / 'parcela_sub_cafe_sombra.csv')
    m = df.groupby(['cultivar', 'sombreamento_pct'])['produtividade_sc_ha'].mean()
    somb = [0, 30, 50]
    cults = ['Arara', 'Catuai_144', 'Topazio']
    nomes = ['Arara', 'Catuaí 144', 'Topázio']
    esperado = {'Arara': [33.15, 35.75, 36.98], 'Catuai_144': [31.05, 34.63, 32.28],
                'Topazio': [25.45, 32.48, 29.50]}
    letras = {'Arara': ['a', 'a', 'a'], 'Catuai_144': ['a', 'ab', 'b'], 'Topazio': ['b', 'b', 'c']}
    conferir('fig_cafe.png', m, {(c, s): v for c in cults for s, v in zip(somb, esperado[c])})
    cores = ['white', '0.65', '0.25']
    fig, ax = plt.subplots(figsize=(LARG, 8.5 * CM))
    x = np.arange(3)
    w = 0.26
    for i, (c, nome) in enumerate(zip(cults, nomes)):
        vals = [m[(c, s)] for s in somb]
        pos = x + (i - 1) * w
        ax.bar(pos, vals, width=w, color=cores[i], edgecolor='black',
               linewidth=0.8, label=nome)
        for p, v, l in zip(pos, vals, letras[c]):
            ax.text(p, v + 0.5, l, ha='center', va='bottom', fontsize=9)
    ax.set_xticks(x, ['0 %', '30 %', '50 %'])
    ax.set_xlabel('Sombreamento (%)')
    ax.set_ylabel('Produtividade (sc ha⁻¹)')
    ax.set_ylim(0, 50)
    ax.yaxis.set_major_formatter(FMT)
    ax.legend(loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.03))
    fig.tight_layout()
    salvar(fig, 'fig_cafe.png')


def fig_doses():
    df = pd.read_csv(DADOS / 'doses_nitrogenio.csv')
    m = df.groupby('dose_n_kg_ha')['volume_m3_ha'].mean()
    print('   médias por dose:', ', '.join(f'{d:g} → {v:.3f}' for d, v in m.items()))
    conferir('fig_doses.png', m, {0: 41.4, 50: 50.4, 100: 56.0, 150: 60.8, 200: 59.0},
             casas=1)   # Tabela 10 tem 1 casa decimal
    b0, b1, b2 = 41.1586, 0.21921, -0.00063929
    # confere a equação com um ajuste quadrático às médias
    c2, c1, c0 = np.polyfit(m.index.values, m.values, 2)
    assert abs(c0 - b0) < 1e-3 and abs(c1 - b1) < 1e-4 and abs(c2 - b2) < 1e-7, (c0, c1, c2)
    pred = b0 + b1 * m.index.values + b2 * m.index.values ** 2
    r2 = 1 - ((m.values - pred) ** 2).sum() / ((m.values - m.values.mean()) ** 2).sum()
    dmet = -b1 / (2 * b2)
    ymax = b0 + b1 * dmet + b2 * dmet ** 2
    print(f'   R² (médias) = {r2:.4f}; DMET = {dmet:.1f}; ŷmax = {ymax:.2f}')
    xs = np.linspace(0, 200, 300)
    fig, ax = plt.subplots(figsize=(LARG, 9 * CM))
    ax.plot(xs, b0 + b1 * xs + b2 * xs ** 2, color='black', linewidth=1.2, label='Curva ajustada')
    ax.plot(m.index, m.values, 'o', color='black', markersize=6, label='Médias observadas')
    ax.axvline(dmet, color='black', linestyle='--', linewidth=0.9)
    ax.annotate(f'DMET = {br(dmet, 1)} kg ha⁻¹', xy=(dmet, 47), xytext=(-6, 0),
                textcoords='offset points', ha='right', va='center', fontsize=9)
    ax.text(8, 61.5, f'ŷ = {br(b0, 4)} + {br(b1, 5)}x − {br(-b2, 8)}x²\nR² = {br(r2, 2)}',
            ha='left', va='top', fontsize=9)
    ax.set_xlim(-5, 210)
    ax.set_ylim(38, 64)
    ax.set_xticks([0, 50, 100, 150, 200])
    ax.set_xlabel('Dose de N (kg ha⁻¹)')
    ax.set_ylabel('Volume de madeira (m³ ha⁻¹)')
    ax.xaxis.set_major_formatter(FMT)
    ax.yaxis.set_major_formatter(FMT)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 0.0))
    fig.tight_layout()
    salvar(fig, 'fig_doses.png')


def fig_pragas():
    df = pd.read_csv(DADOS / 'dic_contagem_pragas.csv')
    ordem = ['convencional', 'pousio', 'saf_simples', 'saf_biodiverso']
    g = df.groupby('manejo')['insetos_praga']
    conferir('fig_pragas.png', g.mean(), dict(zip(ordem, [21.17, 13.83, 9.83, 2.50])))
    v = g.var()
    for k, e in zip(ordem, [97.4, 18.6, 31.4, 4.3]):
        assert abs(v[k] - e) < 0.05, (k, v[k])
    fig, ax = plt.subplots(figsize=(LARG, 9 * CM))
    dados = [df.loc[df.manejo == k, 'insetos_praga'].values for k in ordem]
    ax.boxplot(dados, widths=0.5, patch_artist=True,
               boxprops=dict(facecolor='0.85', edgecolor='black', linewidth=0.8),
               medianprops=dict(color='black', linewidth=1.4),
               whiskerprops=dict(color='black', linewidth=0.8),
               capprops=dict(color='black', linewidth=0.8),
               flierprops=dict(marker='o', markerfacecolor='white', markeredgecolor='black', markersize=5))
    rng = np.random.default_rng(1)
    for i, d in enumerate(dados, start=1):
        ax.plot(i + rng.uniform(-0.09, 0.09, len(d)), d, '.', color='black', markersize=4, alpha=0.8)
        ax.plot(i, d.mean(), marker='D', color='white', markeredgecolor='black', markersize=5)
    ax.set_xticks(range(1, 5), [f'{n}\n(s² = {br(v[k], 1)})' for n, k in
                                zip(['Convencional', 'Pousio', 'SAF simples', 'SAF biodiverso'], ordem)])
    ax.set_xlabel('Manejo')
    ax.set_ylabel('Insetos-praga por armadilha (nº)')
    ax.set_ylim(-1, 35)
    ax.yaxis.set_major_formatter(FMT)
    ax.plot([], [], 'D', color='white', markeredgecolor='black', markersize=5, label='Média')
    ax.plot([], [], '.', color='black', label='Armadilha')
    ax.legend(loc='upper right')
    fig.tight_layout()
    salvar(fig, 'fig_pragas.png')


def fig_copilot():
    """Figura motivadora (Cap. 1): experimento de Peng et al. (2023), arXiv:2302.06590.

    Valores publicados no artigo (não há CSV): tempo médio de quem concluiu a
    tarefa, 71,17 min (com Copilot, n = 45) e 160,89 min (sem, n = 50); redução de
    55,8 %; ganho estimado pelos próprios participantes, 35 % em média.
    """
    com, sem = 71.17, 160.89
    reducao = (sem - com) / sem * 100
    assert abs(reducao - 55.8) < 0.05, reducao   # confere com o artigo
    estimado, real = 35.0, 55.8
    fig, (a, b) = plt.subplots(2, 1, figsize=(LARG, 9.5 * CM))
    # (a) tempo médio
    y = [1, 0]
    a.barh(y, [sem, com], height=0.5, color=['white', '0.45'], edgecolor='black', linewidth=0.8)
    a.set_yticks(y, ['Sem IA', 'Com IA (Copilot)'])
    for yi, v in zip(y, [sem, com]):
        a.text(v + 2, yi, f'{br(v, 1)} min', va='center', ha='left', fontsize=9)
    a.annotate('', xy=(com, 0.5), xytext=(sem, 0.5),
               arrowprops=dict(arrowstyle='->', color='black', linewidth=0.9))
    a.text((com + sem) / 2, 0.5, f'−{br(reducao, 1)} %', ha='center', va='center', fontsize=9,
           fontweight='bold', bbox=dict(facecolor='white', edgecolor='none', pad=1.5))
    a.set_xlim(0, 200)
    a.set_ylim(-0.5, 1.5)
    a.set_xlabel('Tempo médio para concluir a tarefa (min)')
    a.xaxis.set_major_formatter(FMT)
    # (b) ganho estimado × real
    b.barh(y, [estimado, real], height=0.5, color=['white', '0.45'], edgecolor='black', linewidth=0.8)
    b.set_yticks(y, ['Ganho estimado\npelos participantes', 'Ganho real medido'])
    for yi, v in zip(y, [estimado, real]):
        b.text(v + 0.6, yi, f'{br(v)} %', va='center', ha='left', fontsize=9)
    b.set_xlim(0, 70)
    b.set_ylim(-0.5, 1.5)
    b.set_xlabel('Ganho de produtividade (%)')
    b.xaxis.set_major_formatter(FMT)
    for ax, letra in ((a, '(a)'), (b, '(b)')):
        ax.text(-0.02, 1.08, letra, transform=ax.transAxes, ha='right', va='bottom',
                fontsize=10, fontweight='bold')
    fig.tight_layout(h_pad=1.5)
    salvar(fig, 'fig_copilot.png')


if __name__ == '__main__':
    print('figuras ->', OUT)
    fig_dic_mudas()
    fig_dbc_milho()
    fig_fatorial()
    fig_cafe()
    fig_doses()
    fig_pragas()
    fig_copilot()
