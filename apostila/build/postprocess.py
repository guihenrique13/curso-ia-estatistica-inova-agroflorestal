#!/usr/bin/env python3
"""Pós-processa o .docx gerado pelo pandoc:
- impede que linhas de tabela se dividam entre páginas (w:cantSplit);
- tabelas com legenda "Tabela N – ..." recebem o padrão ABNT/IBGE:
  sem linhas verticais, só 3 linhas horizontais (topo, abaixo do
  cabeçalho, fim), cabeçalho sem sombreamento;
- estilo "Fonte da tabela" (Fonte/Nota abaixo das tabelas) em 9 pt, preso à tabela;
- espaço acima dos títulos "Tabela N –" / "Figura N –";
- imagens (estilo "Figure") centralizadas e presas à fonte abaixo.
Uso: postprocess.py arquivo.docx
"""
import re, sys, zipfile, shutil, os

path = sys.argv[1]
tmp = path + '.tmp'
zin = zipfile.ZipFile(path)
zout = zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED)

ABNT_BORDERS = ('<w:tblBorders><w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
                '<w:left w:val="nil"/><w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
                '<w:right w:val="nil"/><w:insideH w:val="nil"/><w:insideV w:val="nil"/></w:tblBorders>')
HEAD_TCPR = ('<w:tcPr><w:tcBorders><w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/></w:tcBorders>'
             '<w:shd w:val="clear" w:color="auto" w:fill="auto"/></w:tcPr>')


def cant_split(xml):
    xml = re.sub(r'<w:tr>(?!<w:trPr>)', '<w:tr><w:trPr><w:cantSplit/></w:trPr>', xml)
    xml = re.sub(r'<w:tr><w:trPr>(?!<w:cantSplit/>)', '<w:tr><w:trPr><w:cantSplit/>', xml)
    return xml


def abnt_table(m):
    t = m.group(0)
    if not re.search(r'<w:tblCaption w:val="Tabela \d', t):
        return t
    t = re.sub(r'(<w:tblW [^>]*/>)', r'\1' + ABNT_BORDERS, t, count=1)
    # primeira linha (cabeçalho): borda inferior e sem sombreamento
    i = t.find('<w:tr>')
    j = t.find('</w:tr>', i)
    head = t[i:j].replace('<w:tcPr />', HEAD_TCPR).replace('<w:tcPr/>', HEAD_TCPR)
    t = t[:i] + head + t[j:]
    # mantém a tabela inteira (e a fonte/nota) na mesma página
    t = t.replace('<w:pStyle w:val="Compact" />', '<w:pStyle w:val="Compact" /><w:keepNext />')
    return t


n_abnt = 0
for item in zin.infolist():
    data = zin.read(item.filename)
    if item.filename == 'word/document.xml':
        xml = data.decode('utf-8')
        n_abnt = len(re.findall(r'<w:tblCaption w:val="Tabela \d', xml))
        xml = re.sub(r'<w:tbl>.*?</w:tbl>', abnt_table, xml, flags=re.S)
        xml = cant_split(xml)
        data = xml.encode('utf-8')
    elif item.filename == 'word/styles.xml':
        xml = data.decode('utf-8')
        xml = re.sub(r'(<w:style [^>]*w:styleId="Fontedatabela"[^>]*>.*?)(</w:style>)',
                     lambda m: re.sub(r'<w:pPr>.*?</w:pPr>|<w:rPr>.*?</w:rPr>', '', m.group(1), flags=re.S)
                     + '<w:pPr><w:keepNext/><w:spacing w:before="0" w:after="40"/></w:pPr>'
                       '<w:rPr><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>' + m.group(2),
                     xml, count=1, flags=re.S)
        # espaço antes do título das tabelas/figuras
        xml = re.sub(r'(w:styleId="TableCaption".*?<w:keepNext\s*/>)',
                     r'\1<w:spacing w:before="240" w:after="60"/>', xml, count=1, flags=re.S)
        # parágrafo da imagem (estilo "Figure"): centralizado, preso à fonte abaixo
        xml = re.sub(r'(<w:style [^>]*w:styleId="Figure"[^>]*>.*?)(</w:style>)',
                     lambda m: re.sub(r'<w:pPr>.*?</w:pPr>', '', m.group(1), flags=re.S)
                     + '<w:pPr><w:keepNext/><w:spacing w:before="0" w:after="60"/>'
                       '<w:jc w:val="center"/></w:pPr>' + m.group(2),
                     xml, count=1, flags=re.S)
        data = xml.encode('utf-8')
    zout.writestr(item, data)
zout.close(); zin.close()
shutil.move(tmp, path)
print(f'postprocess: {n_abnt} tabelas ABNT; linhas com cantSplit aplicadas')
