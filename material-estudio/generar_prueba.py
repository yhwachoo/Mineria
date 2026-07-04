# -*- coding: utf-8 -*-
"""Genera dos PDF: la Prueba (enunciado) y el Solucionario, para el curso
Minería de Datos. Cubre: PCA, Análisis Factorial, Árboles de decisión,
Ensembles (bagging/RF/AdaBoost), Redes Bayesianas/Naive Bayes, SVM y validación.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable, KeepTogether, PageBreak)
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

# ---------------------------------------------------------------- paleta
NAVY   = colors.HexColor('#14304d')   # azul profundo (banners, encabezados)
BLUE   = colors.HexColor('#2d6cdf')   # azul de acento
INK    = colors.HexColor('#1f2d3d')   # texto principal
MUTED  = colors.HexColor('#5b6675')   # texto secundario
LM = RM = 1.8 * cm
CONTENT_W = letter[0] - LM - RM       # ancho útil de la página

# colores de cada tipo de tarjeta: (fondo, barra de acento, color de texto)
PAL = {
    'recuerda': (colors.HexColor('#e9f1fc'), colors.HexColor('#2d6cdf'), colors.HexColor('#173a6b')),
    'intui':    (colors.HexColor('#efeafa'), colors.HexColor('#6c4dd6'), colors.HexColor('#352258')),
    'porque':   (colors.HexColor('#fbf3e0'), colors.HexColor('#e0a21a'), colors.HexColor('#6b4a05')),
    'result':   (colors.HexColor('#e7f6ec'), colors.HexColor('#2ba84a'), colors.HexColor('#16532a')),
    'interp':   (colors.HexColor('#eef1f5'), colors.HexColor('#97a1b0'), colors.HexColor('#3c4654')),
    'sol':      (colors.HexColor('#f4f6f9'), colors.HexColor('#14304d'), colors.HexColor('#26323f')),
}

# ---------------------------------------------------------------- estilos
styles = getSampleStyleSheet()
S = {}
# encabezado / banner
S['banner_u'] = ParagraphStyle('banner_u', parent=styles['Normal'], fontSize=8.5,
                               alignment=TA_CENTER, textColor=colors.HexColor('#c7d6ec'),
                               leading=11, spaceAfter=1)
S['banner_t'] = ParagraphStyle('banner_t', parent=styles['Title'], fontSize=18,
                               alignment=TA_CENTER, textColor=colors.white, leading=21,
                               spaceBefore=1, spaceAfter=2)
S['banner_s'] = ParagraphStyle('banner_s', parent=styles['Normal'], fontSize=9.5,
                               alignment=TA_CENTER, textColor=colors.HexColor('#dce6f5'),
                               leading=12)
S['sub'] = ParagraphStyle('sub', parent=styles['Normal'], fontSize=10,
                          alignment=TA_CENTER, textColor=MUTED)
# títulos de sección (banner ancho)
S['seccion'] = ParagraphStyle('seccion', parent=styles['Heading2'], fontSize=12,
                              spaceBefore=14, spaceAfter=6, leading=16, leftIndent=4,
                              textColor=colors.white, backColor=NAVY, borderPadding=(5, 6, 5, 6))
# texto base
S['preg'] = ParagraphStyle('preg', parent=styles['Normal'], fontSize=10.5,
                           leading=15, spaceBefore=6, spaceAfter=2, textColor=INK,
                           alignment=TA_JUSTIFY)
S['body'] = ParagraphStyle('body', parent=styles['Normal'], fontSize=10.5,
                           leading=15, spaceBefore=7, spaceAfter=3, alignment=TA_JUSTIFY,
                           leftIndent=2, textColor=NAVY)
S['nota'] = ParagraphStyle('nota', parent=styles['Normal'], fontSize=9,
                           leading=12.5, textColor=MUTED)
S['paso'] = ParagraphStyle('paso', parent=styles['Normal'], fontSize=10,
                           leading=14, spaceBefore=2, spaceAfter=3, alignment=TA_JUSTIFY,
                           leftIndent=20, textColor=INK)
# estilos internos de las tarjetas (sin fondo; el fondo lo pone la Table)
S['recuerda'] = ParagraphStyle('recuerda', parent=styles['Normal'], fontSize=9.5,
                               leading=13.5, alignment=TA_JUSTIFY, textColor=PAL['recuerda'][2])
S['intui'] = ParagraphStyle('intui', parent=styles['Normal'], fontSize=9.6,
                            leading=13.8, alignment=TA_JUSTIFY, textColor=PAL['intui'][2])
S['porque'] = ParagraphStyle('porque', parent=styles['Normal'], fontSize=9.3,
                             leading=12.8, alignment=TA_JUSTIFY, textColor=PAL['porque'][2])
S['result'] = ParagraphStyle('result', parent=styles['Normal'], fontSize=10,
                             leading=14, alignment=TA_JUSTIFY, textColor=PAL['result'][2])
S['interp'] = ParagraphStyle('interp', parent=styles['Normal'], fontSize=9.5,
                             leading=13.2, alignment=TA_JUSTIFY, textColor=PAL['interp'][2])
S['solinner'] = ParagraphStyle('solinner', parent=styles['Normal'], fontSize=10,
                               leading=14, alignment=TA_JUSTIFY, textColor=PAL['sol'][2])
S['sol'] = ParagraphStyle('sol', parent=styles['Normal'], fontSize=10,
                          leading=14, alignment=TA_JUSTIFY, textColor=PAL['sol'][2],
                          backColor=PAL['sol'][0], borderPadding=(7, 9, 7, 9),
                          spaceBefore=3, spaceAfter=4, leftIndent=4, rightIndent=2)
# encabezado de pregunta (chip)
S['item'] = ParagraphStyle('item', parent=styles['Normal'], fontSize=11,
                           leading=14, textColor=NAVY, fontName='Helvetica-Bold')
# celdas de tablas de datos
S['cell'] = ParagraphStyle('cell', parent=styles['Normal'], fontSize=9.5,
                           leading=12, alignment=TA_CENTER, textColor=INK)
S['cellL'] = ParagraphStyle('cellL', parent=styles['Normal'], fontSize=9.5,
                            leading=12, textColor=INK)
S['cellH'] = ParagraphStyle('cellH', parent=styles['Normal'], fontSize=9.5,
                            leading=12, alignment=TA_CENTER, textColor=colors.white,
                            fontName='Helvetica-Bold')

def P(t, st='preg'):
    return Paragraph(t, S[st])

def _box(text, kind, style_key=None):
    """Tarjeta con barra de color a la izquierda."""
    bg, accent, _ = PAL[kind]
    inner = Paragraph(text, S[style_key or kind])
    t = Table([[inner]], colWidths=[CONTENT_W], hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg),
        ('LINEBEFORE', (0, 0), (-1, -1), 3.2, accent),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
    ]))
    return t

def sol(t):
    return _box(t, 'sol', 'solinner')

def conc(t):
    """Respuesta conceptual (tarjeta neutra)."""
    return _box(t, 'sol', 'solinner')

def tbl(data, colw=None, header=True):
    data = [list(r) for r in data]
    if header and data:
        # Reescribe la fila de encabezado en blanco/negrita para que se lea
        # sobre el fondo azul (el color del Paragraph original anularía el blanco).
        fila = []
        for c in data[0]:
            txt = getattr(c, 'text', None) if isinstance(c, Paragraph) else str(c)
            fila.append(Paragraph(txt if txt is not None else '', S['cellH']))
        data[0] = fila
    t = Table(data, colWidths=colw, hAlign='LEFT')
    cmds = [
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#c7ced8')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f6fa')]),
    ]
    if header:
        cmds += [('BACKGROUND', (0, 0), (-1, 0), NAVY)]
    t.setStyle(TableStyle(cmds))
    return t

def hr():
    return HRFlowable(width='100%', thickness=0.7, color=colors.HexColor('#cdd5df'),
                      spaceBefore=4, spaceAfter=4)

def item(t):
    inner = Paragraph(t, S['item'])
    tb = Table([[inner]], colWidths=[CONTENT_W], hAlign='LEFT')
    tb.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e7eef7')),
        ('LINEBEFORE', (0, 0), (-1, -1), 4, BLUE),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    return KeepTogether([Spacer(1, 6), tb, Spacer(1, 2)])

def recuerda(t):
    return _box('<font color="#1b4fa0"><b>&#128161; Recuerda.</b></font> ' + t, 'recuerda')

def paso(n, t):
    return Paragraph('<font color="#2d6cdf"><b>Paso %s.</b></font> %s' % (n, t), S['paso'])

def res(t):
    return _box('<font color="#1f7a34"><b>&#10003; Resultado.</b></font> ' + t, 'result')

def interp(t):
    return _box('<font color="#5b6675"><b><i>Interpretación.</i></b></font> ' + t, 'interp')

def porque(t):
    return _box('<font color="#9a6a00"><b>&#8627; &iquest;Por qu&eacute;?</b></font> ' + t, 'porque')

def intui(t):
    return _box('<font color="#5a3aa8"><b>&#9733; Idea clave.</b></font> ' + t, 'intui')

# ----------------------------------------------------- datos compartidos
def encabezado(flow, solucionario=False, subtitulo='Minería de Datos &nbsp;&bull;&nbsp; Clasificación y Reducción de Dimensionalidad'):
    titulo = 'SOLUCIONARIO' if solucionario else 'Prueba de Cátedra'
    banner_inner = [
        Paragraph('UNIVERSIDAD TECNOLÓGICA METROPOLITANA', S['banner_u']),
        Paragraph(titulo, S['banner_t']),
        Paragraph(subtitulo, S['banner_s']),
    ]
    banner = Table([[banner_inner]], colWidths=[CONTENT_W], hAlign='LEFT')
    banner.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), NAVY),
        ('LINEBELOW', (0, 0), (-1, -1), 3, BLUE),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    flow.append(banner)
    flow.append(Spacer(1, 8))
    if not solucionario:
        meta = Table([
            ['Nombre:', '__________________________________', 'Fecha:', '____ / ____ / ______'],
            ['Carrera:', '__________________________________', 'Puntaje:', '______ / 100  pts'],
        ], colWidths=[1.6*cm, 8.0*cm, 1.6*cm, 5.0*cm])
        meta.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 9.5),
            ('TEXTCOLOR', (0, 0), (-1, -1), INK),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('LINEBELOW', (1, 0), (1, 0), 0.6, colors.HexColor('#c7ced8')),
            ('LINEBELOW', (3, 0), (3, 0), 0.6, colors.HexColor('#c7ced8')),
            ('LINEBELOW', (1, 1), (1, 1), 0.6, colors.HexColor('#c7ced8')),
            ('LINEBELOW', (3, 1), (3, 1), 0.6, colors.HexColor('#c7ced8')),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        flow.append(meta)
        flow.append(Spacer(1, 6))
        instr = ('<font color="#14304d"><b>&#9432; Instrucciones.</b></font> Tiempo: 120 minutos. Prueba individual, '
                 'a lápiz y papel. Se permite calculadora y una hoja de fórmulas manuscrita. Justifique todo desarrollo: '
                 'una respuesta sin procedimiento no recibe puntaje. Use 4 decimales cuando sea necesario. '
                 '<b>Valores útiles:</b> log<sub>2</sub>(3)=1.585, log<sub>2</sub>(5)=2.322, ln(2)=0.693, '
                 'ln(3)=1.099, e<sup>-1</sup>=0.3679, &#8730;2=1.414.')
        flow.append(_box(instr, 'recuerda', 'recuerda'))
    flow.append(Spacer(1, 2))

# ============================================================ CONTENIDO
def construir(flow, sols):
    """sols=True incluye soluciones."""

    # ---------- Sección I: PCA
    flow.append(Paragraph('Sección I — Análisis de Componentes Principales (PCA) &nbsp;[14 pts]', S['seccion']))
    flow.append(P('<b>1.</b> Sea un conjunto de datos con dos variables estandarizadas cuya '
                  'matriz de covarianzas (= correlaciones) es:'))
    flow.append(P('&nbsp;&nbsp;&nbsp;&nbsp;&Sigma; = [ [4, 2], [2, 4] ]', 'body'))
    flow.append(P('<b>(a)</b> [4 pts] Calcule los valores propios (autovalores) de &Sigma;.'))
    flow.append(P('<b>(b)</b> [3 pts] Obtenga el vector propio asociado al mayor autovalor (la primera componente principal).'))
    flow.append(P('<b>(c)</b> [3 pts] ¿Qué proporción de la varianza total explica la primera componente principal?'))
    flow.append(P('<b>(d)</b> [4 pts] Explique brevemente la diferencia conceptual entre PCA y el Análisis Factorial '
                  'en cuanto a qué busca explicar cada técnica.'))
    if sols:
        flow.append(sol('<b>(a)</b> Autovalores: det(&Sigma; &minus; &lambda;I) = (4&minus;&lambda;)<sup>2</sup> &minus; 2<sup>2</sup> = 0 '
                        '&rArr; (4&minus;&lambda;) = &plusmn;2 &rArr; <b>&lambda;<sub>1</sub> = 6, &lambda;<sub>2</sub> = 2</b>.'))
        flow.append(sol('<b>(b)</b> Para &lambda;<sub>1</sub>=6: (4&minus;6)v<sub>1</sub> + 2v<sub>2</sub> = 0 &rArr; &minus;2v<sub>1</sub>+2v<sub>2</sub>=0 '
                        '&rArr; v<sub>1</sub>=v<sub>2</sub>. Normalizado: <b>v<sub>1</sub> = (1/&#8730;2)(1, 1) &asymp; (0.707, 0.707)</b>.'))
        flow.append(sol('<b>(c)</b> Varianza total = traza = &lambda;<sub>1</sub>+&lambda;<sub>2</sub> = 6+2 = 8. '
                        'Proporción PC1 = 6/8 = <b>0.75 (75%)</b>.'))
        flow.append(sol('<b>(d)</b> PCA realiza transformaciones ortogonales de las variables originales maximizando la '
                        '<b>varianza</b> de las nuevas variables (busca recoger toda la varianza). El Análisis Factorial busca '
                        'explicar la <b>estructura de covarianzas/correlaciones</b> entre las variables mediante factores latentes '
                        'comunes, separando varianza común (comunalidad) de varianza específica.'))

    # ---------- Sección II: Análisis Factorial
    flow.append(Paragraph('Sección II — Análisis Factorial &nbsp;[16 pts]', S['seccion']))
    flow.append(P('<b>2.</b> Tras un Análisis Factorial por máxima verosimilitud (rotación varimax) sobre 3 variables '
                  'observadas, se obtuvo la siguiente matriz de pesos (cargas) factoriales para 2 factores:'))
    flow.append(tbl([
        [P('Variable', 'cell'), P('Factor 1 (&lambda;<sub>i1</sub>)', 'cell'), P('Factor 2 (&lambda;<sub>i2</sub>)', 'cell')],
        [P('X1', 'cell'), P('0.80', 'cell'), P('0.10', 'cell')],
        [P('X2', 'cell'), P('0.70', 'cell'), P('0.30', 'cell')],
        [P('X3', 'cell'), P('0.20', 'cell'), P('0.90', 'cell')],
    ], colw=[3*cm, 3.5*cm, 3.5*cm]))
    flow.append(Spacer(1, 3))
    flow.append(P('<b>(a)</b> [6 pts] Calcule la comunalidad h<sup>2</sup><sub>i</sub> y la varianza específica '
                  '&psi;<sub>i</sub> de cada variable (suponga variables estandarizadas, varianza total = 1).'))
    flow.append(P('<b>(b)</b> [3 pts] Calcule la suma de cargas al cuadrado (SS loadings) del Factor 1 y diga qué '
                  'proporción de la varianza total (de las 3 variables) explica ese factor.'))
    flow.append(P('<b>(c)</b> [4 pts] Para decidir si los datos son adecuados para el Análisis Factorial se reportó: '
                  'determinante de la matriz de correlaciones = 7.9&times;10<sup>-7</sup>, KMO = 0.794 y test de '
                  'esfericidad de Bartlett con p &lt; 0.001. Interprete cada uno y concluya.'))
    flow.append(P('<b>(d)</b> [3 pts] ¿Qué busca lograr la rotación varimax sobre la matriz de cargas?'))
    if sols:
        flow.append(sol('<b>(a)</b> h<sup>2</sup><sub>i</sub> = &Sigma;<sub>j</sub> &lambda;<sup>2</sup><sub>ij</sub> &nbsp;y&nbsp; &psi;<sub>i</sub> = 1 &minus; h<sup>2</sup><sub>i</sub>:'))
        flow.append(sol('X1: h<sup>2</sup> = 0.80<sup>2</sup>+0.10<sup>2</sup> = 0.64+0.01 = <b>0.65</b>; &psi; = <b>0.35</b>.'))
        flow.append(sol('X2: h<sup>2</sup> = 0.70<sup>2</sup>+0.30<sup>2</sup> = 0.49+0.09 = <b>0.58</b>; &psi; = <b>0.42</b>.'))
        flow.append(sol('X3: h<sup>2</sup> = 0.20<sup>2</sup>+0.90<sup>2</sup> = 0.04+0.81 = <b>0.85</b>; &psi; = <b>0.15</b>.'))
        flow.append(sol('<b>(b)</b> SS(F1) = 0.80<sup>2</sup>+0.70<sup>2</sup>+0.20<sup>2</sup> = 0.64+0.49+0.04 = <b>1.17</b>. '
                        'Proporción = 1.17/3 = <b>0.39 (39%)</b>.'))
        flow.append(sol('<b>(c)</b> Determinante muy bajo (&asymp;0) &rArr; existen intercorrelaciones altas entre variables, '
                        'favorable. KMO=0.794 está entre 0.5 y 1 &rArr; adecuación muestral aceptable/buena. Bartlett con '
                        'p&lt;0.001 &rArr; se rechaza H<sub>0</sub> (las variables NO están incorrelacionadas en la población). '
                        '<b>Conclusión: es pertinente aplicar Análisis Factorial.</b>'))
        flow.append(sol('<b>(d)</b> Busca una <b>estructura simple</b>: que cada factor tenga unas pocas cargas altas y muchas '
                        'casi nulas, redistribuyendo la varianza para facilitar la interpretación de los factores '
                        '(rotación ortogonal &rArr; las cargas siguen siendo correlaciones factor-variable).'))

    # ---------- Sección III: Árboles de decisión
    flow.append(Paragraph('Sección III — Árboles de Decisión &nbsp;[22 pts]', S['seccion']))
    flow.append(P('<b>3.</b> Un banco quiere predecir si un cliente <b>paga</b> el crédito (Sí/No). Se dispone de '
                  '8 clientes con dos atributos binarios:'))
    flow.append(tbl([
        [P('Cliente', 'cell'), P('Tiene casa', 'cell'), P('Ingreso alto', 'cell'), P('Paga crédito', 'cell')],
        [P('1', 'cell'), P('Sí', 'cell'), P('Sí', 'cell'), P('Sí', 'cell')],
        [P('2', 'cell'), P('Sí', 'cell'), P('Sí', 'cell'), P('Sí', 'cell')],
        [P('3', 'cell'), P('Sí', 'cell'), P('Sí', 'cell'), P('Sí', 'cell')],
        [P('4', 'cell'), P('Sí', 'cell'), P('No', 'cell'), P('Sí', 'cell')],
        [P('5', 'cell'), P('Sí', 'cell'), P('Sí', 'cell'), P('No', 'cell')],
        [P('6', 'cell'), P('No', 'cell'), P('No', 'cell'), P('No', 'cell')],
        [P('7', 'cell'), P('No', 'cell'), P('No', 'cell'), P('No', 'cell')],
        [P('8', 'cell'), P('No', 'cell'), P('No', 'cell'), P('No', 'cell')],
    ], colw=[2*cm, 2.6*cm, 2.6*cm, 2.8*cm]))
    flow.append(Spacer(1, 3))
    flow.append(P('<b>(a)</b> [6 pts] Para el nodo raíz, calcule los tres criterios de impureza: índice de Gini, '
                  'entropía y error de clasificación.'))
    flow.append(P('<b>(b)</b> [8 pts] Considere dividir por cada atributo. Calcule el Gini ponderado (Gini split) de la '
                  'división por "Tiene casa" y por "Ingreso alto". ¿Cuál atributo conviene elegir como nodo inicial y por qué?'))
    flow.append(P('<b>(c)</b> [5 pts] Para el atributo elegido en (b), calcule la ganancia de información usando entropía.'))
    flow.append(P('<b>(d)</b> [3 pts] Mencione un criterio de parada (¿cuándo dejar de dividir?) y explique brevemente '
                  'qué hace la poda (pruning) en CART.'))
    if sols:
        flow.append(sol('<b>(a)</b> Raíz: 4 "Sí" y 4 "No" (p=0.5 cada clase). '
                        'Gini = 1 &minus; (0.5<sup>2</sup>+0.5<sup>2</sup>) = <b>0.5</b>. '
                        'Entropía = &minus;(0.5·log<sub>2</sub>0.5 + 0.5·log<sub>2</sub>0.5) = <b>1.0</b>. '
                        'Error = 1 &minus; max(0.5,0.5) = <b>0.5</b>.'))
        flow.append(sol('<b>(b) Tiene casa:</b> rama Sí = {1,2,3,4,5} &rarr; 4 Sí / 1 No, Gini = 1&minus;((4/5)<sup>2</sup>+(1/5)<sup>2</sup>) '
                        '= 1&minus;(0.64+0.04) = 0.32. Rama No = {6,7,8} &rarr; 0 Sí / 3 No, Gini = 0 (puro). '
                        'Gini split = (5/8)(0.32) + (3/8)(0) = <b>0.20</b>.'))
        flow.append(sol('<b>Ingreso alto:</b> rama Sí = {1,2,3,5} &rarr; 3 Sí / 1 No, Gini = 1&minus;((3/4)<sup>2</sup>+(1/4)<sup>2</sup>) = 0.375. '
                        'Rama No = {4,6,7,8} &rarr; 1 Sí / 3 No, Gini = 0.375. '
                        'Gini split = (4/8)(0.375)+(4/8)(0.375) = <b>0.375</b>.'))
        flow.append(sol('Se elige <b>"Tiene casa"</b> porque su Gini split (0.20) es menor que el de "Ingreso alto" (0.375), '
                        'es decir produce nodos más puros (mayor reducción de impureza: 0.5&minus;0.20 = 0.30 vs 0.5&minus;0.375 = 0.125).'))
        flow.append(sol('<b>(c)</b> Entropía rama Sí (4/1): &minus;((4/5)log<sub>2</sub>(4/5)+(1/5)log<sub>2</sub>(1/5)) '
                        '= &minus;(0.8·(&minus;0.3219)+0.2·(&minus;2.3219)) = 0.7219. Rama No: entropía = 0. '
                        'Entropía ponderada = (5/8)(0.7219)+(3/8)(0) = 0.4512. '
                        'Ganancia = 1.0 &minus; 0.4512 = <b>0.5488</b>.'))
        flow.append(sol('<b>(d)</b> Criterio de parada: todos los registros del nodo son de la misma clase (nodo puro), '
                        'o no quedan atributos, o se alcanza una profundidad/mínimo de registros. La poda elimina ramas que '
                        'aportan poca capacidad predictiva (reduce sobreajuste), reemplazando subárboles por hojas cuando '
                        'no empeora —o mejora— el error estimado sobre validación.'))

    # ---------- Sección IV: Ensembles
    flow.append(Paragraph('Sección IV — Métodos de Consenso y Potenciación &nbsp;[14 pts]', S['seccion']))
    flow.append(P('<b>4.</b> Sobre métodos de ensemble:'))
    flow.append(P('<b>(a)</b> [4 pts] En <b>bagging</b>, cada muestra bootstrap se obtiene con reemplazo y del mismo '
                  'tamaño n que los datos originales. Para n = 10, calcule la probabilidad de que un individuo dado '
                  '<b>sí</b> sea seleccionado en una muestra bootstrap. ¿A qué valor converge cuando n &rarr; &infin;?'))
    flow.append(P('<b>(b)</b> [4 pts] En <b>AdaBoost.M1</b>, un clasificador débil obtiene un error ponderado '
                  '&epsilon; = 0.25. Calcule el peso &alpha; del clasificador, con &alpha; = &frac12;·ln((1&minus;&epsilon;)/&epsilon;).'))
    flow.append(P('<b>(c)</b> [3 pts] ¿Qué es un Bosque Aleatorio (Random Forest) y en qué se diferencia del bagging clásico?'))
    flow.append(P('<b>(d)</b> [3 pts] Explique la diferencia esencial entre bagging y boosting (potenciación).'))
    if sols:
        flow.append(sol('<b>(a)</b> P(no seleccionado) = (1&minus;1/n)<sup>n</sup> = (1&minus;0.1)<sup>10</sup> = 0.9<sup>10</sup> = 0.3487. '
                        'P(seleccionado) = 1 &minus; 0.3487 = <b>0.6513</b>. Cuando n&rarr;&infin;, (1&minus;1/n)<sup>n</sup>&rarr;e<sup>-1</sup>, '
                        'luego P(seleccionado) &rarr; 1&minus;e<sup>-1</sup> = <b>0.632</b> (&asymp;63.2%).'))
        flow.append(sol('<b>(b)</b> &alpha; = &frac12;·ln((1&minus;0.25)/0.25) = &frac12;·ln(0.75/0.25) = &frac12;·ln(3) '
                        '= &frac12;·(1.099) = <b>0.5493</b>.'))
        flow.append(sol('<b>(c)</b> Random Forest es el caso del método de consenso (bagging) en que <b>todos los '
                        'clasificadores son árboles</b>; además, en cada división se considera solo un subconjunto aleatorio '
                        'de atributos, lo que decorrelaciona los árboles y reduce la varianza del consenso.'))
        flow.append(sol('<b>(d)</b> Bagging entrena modelos en paralelo sobre muestras bootstrap independientes y combina '
                        'por voto/promedio (reduce varianza). Boosting entrena modelos en secuencia, aumentando el peso de '
                        'los individuos mal clasificados en cada iteración y ponderando cada modelo (reduce sesgo); '
                        'AdaBoost.M1 está pensado para clasificación binaria.'))

    # ---------- Sección V: Redes Bayesianas / Naive Bayes
    flow.append(Paragraph('Sección V — Redes Bayesianas y Naive Bayes &nbsp;[16 pts]', S['seccion']))
    flow.append(P('<b>5.</b> Teorema de Bayes. Una prueba para detectar una condición tiene sensibilidad '
                  'P(+|enfermo) = 0.99 y la probabilidad de falso positivo es P(+|sano) = 0.05. La prevalencia es '
                  'P(enfermo) = 0.01.'))
    flow.append(P('<b>(a)</b> [6 pts] Si una persona da positivo, calcule la probabilidad de que esté realmente enferma, '
                  'P(enfermo | +), usando el teorema de la probabilidad total y el de Bayes.'))
    flow.append(P('<b>6.</b> Clasificador Naive Bayes. A partir de la siguiente tabla de entrenamiento (10 clientes) '
                  'clasifique a un nuevo cliente con Edad = Joven e Ingreso = Alto.'))
    flow.append(tbl([
        [P('Compra', 'cell'), P('N° casos', 'cell'), P('Edad=Joven', 'cell'), P('Edad=Mayor', 'cell'), P('Ingreso=Alto', 'cell'), P('Ingreso=Bajo', 'cell')],
        [P('Sí', 'cell'), P('6', 'cell'), P('4', 'cell'), P('2', 'cell'), P('4', 'cell'), P('2', 'cell')],
        [P('No', 'cell'), P('4', 'cell'), P('1', 'cell'), P('3', 'cell'), P('1', 'cell'), P('3', 'cell')],
    ], colw=[1.8*cm, 1.8*cm, 2.4*cm, 2.4*cm, 2.5*cm, 2.5*cm]))
    flow.append(Spacer(1, 3))
    flow.append(P('<b>(b)</b> [7 pts] Calcule las probabilidades a posteriori (sin normalizar y normalizadas) y entregue '
                  'la clase predicha.'))
    flow.append(P('<b>(c)</b> [3 pts] ¿Por qué el clasificador se llama "naive" (ingenuo)? ¿Qué supuesto hace?'))
    if sols:
        flow.append(sol('<b>5(a)</b> Probabilidad total: P(+) = P(+|enf)P(enf) + P(+|sano)P(sano) '
                        '= 0.99·0.01 + 0.05·0.99 = 0.0099 + 0.0495 = 0.0594. '
                        'Bayes: P(enf|+) = (0.99·0.01)/0.0594 = 0.0099/0.0594 = <b>0.1667 (&asymp;16.7%)</b>.'))
        flow.append(sol('<b>6(b)</b> Priori: P(Sí)=6/10=0.6, P(No)=4/10=0.4. '
                        'Verosimilitudes: P(Joven|Sí)=4/6=0.6667, P(Alto|Sí)=4/6=0.6667; '
                        'P(Joven|No)=1/4=0.25, P(Alto|No)=1/4=0.25.'))
        flow.append(sol('Posteriori &prop; Sí: 0.6·0.6667·0.6667 = <b>0.2667</b>; &nbsp; No: 0.4·0.25·0.25 = <b>0.0250</b>.'))
        flow.append(sol('Normalizando: P(Sí|x) = 0.2667/(0.2667+0.0250) = 0.2667/0.2917 = <b>0.9143</b>; '
                        'P(No|x) = <b>0.0857</b>. <b>Se clasifica como "Compra = Sí".</b>'))
        flow.append(sol('<b>6(c)</b> Se asume <b>independencia condicional</b> de los atributos dada la clase, '
                        'P(x<sub>1</sub>,x<sub>2</sub>|C)=P(x<sub>1</sub>|C)P(x<sub>2</sub>|C). Es un supuesto "ingenuo" '
                        'porque rara vez se cumple del todo, pero simplifica el cálculo y suele funcionar bien.'))

    # ---------- Sección VI: SVM y Validación
    flow.append(Paragraph('Sección VI — Máquinas de Soporte Vectorial y Validación &nbsp;[18 pts]', S['seccion']))
    flow.append(P('<b>7.</b> Considere un problema 1-D linealmente separable con dos puntos de soporte: '
                  'un ejemplo de clase +1 en x = +1 y uno de clase &minus;1 en x = &minus;1. El clasificador es '
                  'f(x) = w·x + b, con condiciones de soporte w·x+b = +1 y w·x+b = &minus;1.'))
    flow.append(P('<b>(a)</b> [6 pts] Determine w y b, la frontera de decisión y el ancho del margen (2/||w||).'))
    flow.append(P('<b>(b)</b> [4 pts] Explique qué son los <b>vectores de soporte</b> y por qué la SVM busca el margen '
                  'máximo. ¿Para qué sirve un <b>kernel</b> cuando los datos no son linealmente separables?'))
    flow.append(P('<b>8.</b> Validación.'))
    flow.append(P('<b>(c)</b> [5 pts] Explique en qué consiste la validación cruzada de k iteraciones (k-fold cross '
                  'validation) y por qué se prefiere a una única partición train/test.'))
    flow.append(P('<b>(d)</b> [3 pts] Un modelo evaluado con 5-fold CV obtuvo exactitudes de 0.80, 0.85, 0.90, 0.75 y '
                  '0.80. Calcule la exactitud media estimada.'))
    if sols:
        flow.append(sol('<b>7(a)</b> De w·1+b = +1 y w·(&minus;1)+b = &minus;1. Sumando: 2b = 0 &rArr; <b>b = 0</b>. '
                        'Restando: 2w = 2 &rArr; <b>w = 1</b>. Frontera: w·x+b = 0 &rArr; <b>x = 0</b>. '
                        'Margen = 2/||w|| = 2/1 = <b>2</b> (distancia 1 a cada lado).'))
        flow.append(sol('<b>7(b)</b> Los vectores de soporte son los ejemplos más cercanos a la frontera (los que están '
                        'sobre los márgenes); determinan por completo el hiperplano. Se maximiza el margen porque un margen '
                        'mayor mejora la generalización (menor riesgo de error en datos nuevos). El kernel proyecta '
                        'implícitamente los datos a un espacio de mayor dimensión donde sí son linealmente separables, sin '
                        'calcular explícitamente esa transformación (truco del kernel).'))
        flow.append(sol('<b>8(c)</b> Se divide el conjunto en k subconjuntos (folds) de tamaño similar; se entrena con '
                        'k&minus;1 folds y se evalúa con el restante, repitiendo k veces de modo que cada fold sirva una vez '
                        'como test. La métrica final es el promedio de las k evaluaciones. Se prefiere a un solo train/test '
                        'porque usa todos los datos para entrenar y validar, reduce la dependencia de una partición '
                        'particular y da una estimación más estable y menos sesgada del desempeño.'))
        flow.append(sol('<b>8(d)</b> Media = (0.80+0.85+0.90+0.75+0.80)/5 = 4.10/5 = <b>0.82 (82%)</b>.'))

    if not sols:
        flow.append(Spacer(1, 8))
        flow.append(hr())
        flow.append(Paragraph('Fin de la prueba. Revise sus respuestas antes de entregar.', S['nota']))

# ==================================================== SOLUCIONARIO DETALLADO
def construir_solucionario(flow):
    intro = ('Este solucionario muestra, para cada pregunta, la <b>fórmula</b> que se aplica, el '
             '<b>paso a paso</b> del cálculo y la <b>interpretación</b> del resultado. La idea es que '
             'puedas reproducir el razonamiento, no solo verificar la respuesta final.')
    flow.append(Paragraph(intro, S['nota']))
    flow.append(hr())

    # ===== Sección I: PCA
    flow.append(Paragraph('Sección I — Análisis de Componentes Principales (PCA)', S['seccion']))
    flow.append(item('Pregunta 1 — Matriz de covarianzas &Sigma; = [[4, 2], [2, 4]]'))
    flow.append(intui('Imagina una nube de puntos en 2D. PCA busca el <b>eje</b> a lo largo del cual la nube se '
                      'estira más (donde hay más varianza). Ese eje es la 1ª componente principal. Matemáticamente, '
                      'estirar la nube = la matriz de covarianzas &Sigma; "empuja" más fuerte en esa dirección. '
                      'Una dirección que &Sigma; solo <b>estira pero no gira</b> se llama vector propio, y cuánto la '
                      'estira es su valor propio &lambda;. Por eso todo PCA se reduce a buscar vectores y valores propios.'))
    flow.append(recuerda('Un <b>vector propio</b> v de &Sigma; cumple &Sigma;v = &lambda;v: al multiplicarlo por &Sigma; '
                         'queda apuntando en la misma dirección, escalado por el <b>valor propio</b> &lambda; (la varianza '
                         'capturada en esa dirección). Se hallan resolviendo det(&Sigma; &minus; &lambda;I) = 0.'))

    flow.append(Paragraph('<b>(a) Valores propios</b>', S['body']))
    flow.append(paso(1, 'Partimos de la definición &Sigma;v = &lambda;v y la pasamos todo a un lado: '
                        '&Sigma;v &minus; &lambda;v = 0. Para poder factorizar v escribimos &lambda;v = &lambda;Iv '
                        '(donde I es la identidad), y queda (&Sigma; &minus; &lambda;I)v = 0.'))
    flow.append(porque('No se puede restar un número (&lambda;) a una matriz (&Sigma;) directamente: la resta de matrices '
                       'exige el mismo tamaño. Por eso multiplicamos &lambda; por la identidad I = [[1,0],[0,1]], que '
                       'convierte &lambda; en la matriz &lambda;I = [[&lambda;,0],[0,&lambda;]]. Restar &lambda;I solo afecta '
                       'a la <b>diagonal</b> de &Sigma;.'))
    flow.append(paso(2, 'Buscamos v &ne; 0 (una dirección real, no el origen). El sistema (&Sigma; &minus; &lambda;I)v = 0 '
                        'solo tiene soluciones distintas de cero si la matriz NO es invertible, y eso ocurre cuando su '
                        'determinante es 0. De ahí la condición det(&Sigma; &minus; &lambda;I) = 0.'))
    flow.append(porque('Si det &ne; 0 la matriz tendría inversa y la única solución sería v = 0 (la solución trivial), '
                       'que no representa ninguna dirección. Forzar det = 0 es exactamente lo que permite que exista una '
                       'dirección no nula que &Sigma; solo estira.'))
    flow.append(paso(3, 'Construimos &Sigma; &minus; &lambda;I restando &lambda; a cada elemento de la diagonal de &Sigma;: '
                        'de [[4, 2], [2, 4]] obtenemos [[4&minus;&lambda;, 2], [2, 4&minus;&lambda;]].'))
    flow.append(paso(4, 'Calculamos su determinante. Para una 2&times;2 [[a,b],[c,d]] el determinante es a·d &minus; b·c. '
                        'Aquí a=d=(4&minus;&lambda;) y b=c=2: det = (4&minus;&lambda;)(4&minus;&lambda;) &minus; (2)(2) '
                        '= (4&minus;&lambda;)<sup>2</sup> &minus; 4.'))
    flow.append(paso(5, 'Igualamos a 0 y despejamos: (4&minus;&lambda;)<sup>2</sup> &minus; 4 = 0 '
                        '&rArr; (4&minus;&lambda;)<sup>2</sup> = 4 &rArr; 4&minus;&lambda; = &plusmn;2. '
                        'Si 4&minus;&lambda;=+2 &rArr; &lambda;=2; si 4&minus;&lambda;=&minus;2 &rArr; &lambda;=6.'))
    flow.append(res('&lambda;<sub>1</sub> = 6 (el mayor) y &lambda;<sub>2</sub> = 2.'))
    flow.append(interp('Hay dos direcciones especiales: en una la nube se estira con varianza 6 y en la otra con varianza 2. '
                       'La de varianza 6 será la 1ª componente principal por capturar más información.'))

    flow.append(Paragraph('<b>(b) Vector propio de &lambda;<sub>1</sub> = 6 (1ª componente principal)</b>', S['body']))
    flow.append(paso(1, 'Sustituimos el valor propio mayor (&lambda;=6) en (&Sigma; &minus; &lambda;I)v = 0 para hallar SU '
                        'dirección: &Sigma; &minus; 6I = [[4&minus;6, 2], [2, 4&minus;6]] = [[&minus;2, 2], [2, &minus;2]].'))
    flow.append(porque('Cada valor propio tiene su propia dirección. Como queremos la 1ª componente (la de mayor varianza), '
                       'usamos &lambda;=6. Si usáramos &lambda;=2 obtendríamos la 2ª componente.'))
    flow.append(paso(2, 'La matriz multiplicada por v = (v<sub>1</sub>, v<sub>2</sub>) da el sistema. La 1ª fila dice: '
                        '&minus;2·v<sub>1</sub> + 2·v<sub>2</sub> = 0 &rArr; v<sub>1</sub> = v<sub>2</sub>.'))
    flow.append(porque('La 2ª fila (2v<sub>1</sub> &minus; 2v<sub>2</sub> = 0) entrega la misma información. Esto es '
                       'esperable: como forzamos det = 0, las dos filas son "dependientes" y solo fijan la <b>dirección</b> '
                       '(v<sub>1</sub>=v<sub>2</sub>), no la longitud del vector.'))
    flow.append(paso(3, 'Cualquier vector con v<sub>1</sub>=v<sub>2</sub> sirve; el más simple es (1, 1). '
                        'Lo <b>normalizamos</b> (lo dejamos de largo 1) dividiéndolo por su norma '
                        '&#8730;(1<sup>2</sup>+1<sup>2</sup>) = &#8730;2.'))
    flow.append(porque('Se normaliza por convención: una componente principal indica solo una <b>dirección</b>, así que se '
                       'le da longitud 1 para que las "cargas" sean comparables y la proyección conserve la escala correcta.'))
    flow.append(res('v<sub>1</sub> = (1/&#8730;2)(1, 1) &asymp; (0.707, 0.707).'))
    flow.append(interp('La 1ª componente apunta a 45°: es esencialmente el <b>promedio</b> de las dos variables. Tiene '
                       'sentido, porque ambas están correlacionadas positivamente (covarianza 2 &gt; 0): cuando una sube, '
                       'la otra también, y la dirección de máximo estiramiento es la diagonal.'))

    flow.append(Paragraph('<b>(c) Proporción de varianza explicada por PC1</b>', S['body']))
    flow.append(paso(1, 'La varianza total de los datos es la suma de las varianzas de cada variable, que son los elementos '
                        'de la diagonal de &Sigma;: 4 + 4 = 8. Esa suma se llama <b>traza</b>.'))
    flow.append(paso(2, 'Un teorema clave de PCA dice que la traza también es igual a la suma de los valores propios: '
                        '6 + 2 = 8. &#10003; Coincide, lo que confirma que &lambda;<sub>1</sub> y &lambda;<sub>2</sub> '
                        'reparten toda la varianza.'))
    flow.append(porque('Cada valor propio ES la varianza capturada por su componente. Por eso "varianza explicada por una '
                       'componente" = su &lambda;, y la fracción es ese &lambda; dividido por el total de varianza (la traza).'))
    flow.append(paso(3, 'Proporción PC1 = &lambda;<sub>1</sub> / (&lambda;<sub>1</sub>+&lambda;<sub>2</sub>) = 6/8 = 0.75.'))
    flow.append(res('La 1ª componente explica el <b>75%</b> de la varianza total; la 2ª, el 25% restante.'))
    flow.append(interp('Si quisiéramos reducir de 2 dimensiones a 1, nos quedaríamos con PC1 y conservaríamos el 75% de la '
                       'información, descartando solo el 25%. Ese es el criterio típico para decidir cuántas componentes mantener.'))

    flow.append(Paragraph('<b>(d) PCA vs Análisis Factorial</b>', S['body']))
    flow.append(Paragraph('<b>PCA</b> hace transformaciones <b>ortogonales</b> de las variables originales y busca '
                          'maximizar la <b>varianza</b>; intenta recoger <i>toda</i> la varianza observada (es descriptivo, '
                          'sin modelo de error). El <b>Análisis Factorial</b> postula <b>factores latentes</b> (no '
                          'observables, como "inteligencia") que <i>causan</i> las variables medidas, y se centra en explicar '
                          'la <b>estructura de covarianzas/correlaciones</b>, separando la varianza en parte <b>común</b> '
                          '(comunalidad) y parte <b>específica</b> de cada variable. En una frase: <b>PCA resume varianza; '
                          'el Factorial explica por qué las variables correlacionan.</b>', S['sol']))

    # ===== Sección II: Factorial
    flow.append(Paragraph('Sección II — Análisis Factorial', S['seccion']))
    flow.append(item('Pregunta 2 — Cargas factoriales (2 factores, varimax)'))
    flow.append(intui('Una "carga" &lambda;<sub>ij</sub> es la correlación entre la variable X<sub>i</sub> y el factor j. '
                      'Como en estadística el <b>cuadrado de una correlación</b> es la proporción de varianza que una '
                      'variable comparte con otra, &lambda;<sup>2</sup><sub>ij</sub> es la fracción de la varianza de '
                      'X<sub>i</sub> explicada por el factor j. Sumando sobre todos los factores obtenemos cuánta de su '
                      'varianza explican los factores en conjunto.'))
    flow.append(recuerda('Con variables estandarizadas (varianza total = 1), la varianza de cada variable se descompone en '
                         '<b>comunalidad</b> h<sup>2</sup><sub>i</sub> = &Sigma;<sub>j</sub> &lambda;<sup>2</sup><sub>ij</sub> '
                         '(lo que explican los factores comunes) + <b>varianza específica</b> &psi;<sub>i</sub> (lo propio de '
                         'la variable). Por tanto &psi;<sub>i</sub> = 1 &minus; h<sup>2</sup><sub>i</sub>.'))

    flow.append(Paragraph('<b>(a) Comunalidades y varianzas específicas</b>', S['body']))
    flow.append(paso(1, 'Para cada variable tomamos su FILA de cargas y sumamos los cuadrados (eso es la comunalidad). '
                        'Luego restamos de 1 para obtener la varianza específica.'))
    flow.append(porque('Sumamos a lo largo de la fila porque queremos el aporte de <i>todos los factores</i> a UNA variable. '
                       'Elevamos al cuadrado porque la varianza compartida es la correlación al cuadrado, no la correlación.'))
    flow.append(paso(2, 'X1: h<sup>2</sup> = 0.80<sup>2</sup> + 0.10<sup>2</sup> = 0.64 + 0.01 = 0.65 '
                        '&rArr; &psi; = 1 &minus; 0.65 = 0.35.'))
    flow.append(paso(3, 'X2: h<sup>2</sup> = 0.70<sup>2</sup> + 0.30<sup>2</sup> = 0.49 + 0.09 = 0.58 '
                        '&rArr; &psi; = 1 &minus; 0.58 = 0.42.'))
    flow.append(paso(4, 'X3: h<sup>2</sup> = 0.20<sup>2</sup> + 0.90<sup>2</sup> = 0.04 + 0.81 = 0.85 '
                        '&rArr; &psi; = 1 &minus; 0.85 = 0.15.'))
    flow.append(res('h<sup>2</sup> = (0.65, 0.58, 0.85) y &psi; = (0.35, 0.42, 0.15).'))
    flow.append(interp('X3 es la mejor representada por los factores (85% de su varianza es común; casi todo lo explica el '
                       'Factor 2). X2 es la peor representada (solo 58%): tiene mucha varianza específica, propia.'))

    flow.append(Paragraph('<b>(b) SS loadings del Factor 1 y su proporción de varianza</b>', S['body']))
    flow.append(paso(1, 'Ahora tomamos la COLUMNA de un factor y sumamos los cuadrados de sus cargas. Eso mide cuánta '
                        'varianza, sumada sobre TODAS las variables, explica ese factor.'))
    flow.append(porque('En (a) sumábamos por fila (aporte de los factores a una variable); aquí sumamos por columna '
                       '(aporte de un factor a todas las variables). Es la misma tabla leída en el otro sentido.'))
    flow.append(paso(2, 'SS(F1) = 0.80<sup>2</sup> + 0.70<sup>2</sup> + 0.20<sup>2</sup> = 0.64 + 0.49 + 0.04 = 1.17.'))
    flow.append(paso(3, 'La varianza total de las 3 variables estandarizadas es 3 (cada una aporta 1). La proporción '
                        'explicada por el Factor 1 es SS(F1)/3 = 1.17/3 = 0.39.'))
    flow.append(res('SS(F1) = 1.17 &rArr; el Factor 1 explica el <b>39%</b> de la varianza total.'))
    flow.append(interp('Es análogo a la "proporción de varianza" de PCA, pero aquí solo cuenta la varianza <i>común</i>. '
                       'Un factor que explica 39% es importante; sirve para decidir cuántos factores conservar.'))

    flow.append(Paragraph('<b>(c) ¿Son los datos adecuados para Factorial?</b>', S['body']))
    flow.append(paso(1, '<b>Determinante de la matriz de correlaciones &asymp; 0</b> (7.9&times;10<sup>-7</sup>).'))
    flow.append(porque('El determinante mide cuán "independientes" son las variables. Si fueran perfectamente '
                       'incorrelacionadas, la matriz de correlación sería la identidad y su determinante valdría 1. Un '
                       'determinante casi 0 indica fuertes intercorrelaciones &rArr; hay estructura común que factorizar. '
                       'Favorable.'))
    flow.append(paso(2, '<b>KMO = 0.794</b>. Se recomienda continuar si está entre 0.5 y 1; 0.794 es "bueno". Favorable.'))
    flow.append(porque('El KMO compara las correlaciones simples con las parciales: si las variables comparten factores '
                       'comunes, las correlaciones parciales (quitando el efecto de las demás) son pequeñas y el KMO sube '
                       'hacia 1. Un KMO alto = la muestra es adecuada para extraer factores.'))
    flow.append(paso(3, '<b>Test de esfericidad de Bartlett, p &lt; 0.001</b>. Como p &lt; 0.05 se <b>rechaza</b> H<sub>0</sub>.'))
    flow.append(porque('H<sub>0</sub> afirma "la matriz de correlación es la identidad" (variables incorrelacionadas en la '
                       'población). Un p muy pequeño dice que ese escenario es improbable &rArr; sí existe correlación real, '
                       'condición necesaria para el análisis factorial. Favorable.'))
    flow.append(res('Los tres indicadores coinciden &rArr; <b>es pertinente aplicar Análisis Factorial.</b>'))

    flow.append(Paragraph('<b>(d) ¿Qué busca la rotación varimax?</b>', S['body']))
    flow.append(Paragraph('Busca una <b>estructura simple</b>: redistribuye la varianza entre los factores para que cada '
                          'factor tenga <b>pocas cargas altas y muchas casi nulas</b>. Así cada variable se asocia '
                          'claramente a un factor y la interpretación se vuelve obvia (de otro modo las cargas quedan '
                          '"repartidas" y ningún factor es interpretable). Al ser una rotación <b>ortogonal</b>, los factores '
                          'siguen siendo independientes y las cargas siguen siendo correlaciones factor-variable; solo '
                          'cambiamos el "ángulo de los ejes" para ver mejor los grupos.', S['sol']))

    # ===== Sección III: Árboles
    flow.append(Paragraph('Sección III — Árboles de Decisión', S['seccion']))
    flow.append(item('Pregunta 3 — Predecir si el cliente paga el crédito'))
    flow.append(intui('Un árbol va partiendo los datos para llegar a grupos lo más "puros" posible (idealmente, cada hoja '
                      'con una sola clase). Para medir cuán mezclado está un grupo usamos un <b>índice de impureza</b>. '
                      'Cuanto más puro un nodo, menor impureza. El árbol elige la división que más reduce la impureza.'))
    flow.append(recuerda('Con p<sub>k</sub> = proporción de la clase k en el nodo: '
                         '<b>Gini</b> = 1 &minus; &Sigma; p<sub>k</sub><sup>2</sup>; &nbsp; '
                         '<b>Entropía</b> = &minus;&Sigma; p<sub>k</sub> log<sub>2</sub> p<sub>k</sub>; &nbsp; '
                         '<b>Error</b> = 1 &minus; max(p<sub>k</sub>). La impureza de una división es el <b>promedio '
                         'ponderado</b> por el tamaño de cada rama; la <b>ganancia</b> = impureza del padre &minus; impureza '
                         'ponderada de los hijos. Mejor división = menor impureza ponderada (= mayor ganancia).'))

    flow.append(Paragraph('<b>(a) Impureza del nodo raíz</b>', S['body']))
    flow.append(paso(1, 'Contamos clases en la raíz: de 8 clientes, 4 pagan "Sí" y 4 "No" &rArr; p(Sí)=4/8=0.5, p(No)=0.5.'))
    flow.append(paso(2, 'Gini = 1 &minus; (0.5<sup>2</sup> + 0.5<sup>2</sup>) = 1 &minus; (0.25 + 0.25) = 0.5.'))
    flow.append(porque('El Gini es la probabilidad de equivocarse si etiquetáramos un caso al azar según las proporciones '
                       'del nodo. Con 50/50 esa probabilidad es máxima (0.5): es el nodo más "confuso" posible.'))
    flow.append(paso(3, 'Entropía = &minus;(0.5·log<sub>2</sub>0.5 + 0.5·log<sub>2</sub>0.5). Como log<sub>2</sub>0.5 = &minus;1: '
                        '= &minus;(0.5·(&minus;1) + 0.5·(&minus;1)) = 1.'))
    flow.append(porque('La entropía mide la "incertidumbre" en bits. Con dos clases igualmente probables necesitamos '
                       'exactamente 1 bit para describir el resultado: máxima incertidumbre.'))
    flow.append(paso(4, 'Error = 1 &minus; max(0.5, 0.5) = 1 &minus; 0.5 = 0.5.'))
    flow.append(res('Gini = 0.5, Entropía = 1.0, Error = 0.5 (máxima impureza: clases perfectamente mezcladas 50/50).'))

    flow.append(Paragraph('<b>(b) Gini split de cada atributo y elección</b>', S['body']))
    flow.append(paso(1, '<u>Atributo "Tiene casa".</u> Separamos los 8 clientes según el valor del atributo y calculamos '
                        'el Gini de cada rama. Rama "Sí" = {1,2,3,4,5}: 4 pagan, 1 no &rArr; '
                        'Gini = 1 &minus; ((4/5)<sup>2</sup> + (1/5)<sup>2</sup>) = 1 &minus; (0.64 + 0.04) = 0.32.'))
    flow.append(paso(2, 'Rama "No" = {6,7,8}: 0 pagan, 3 no &rArr; nodo <b>puro</b> &rArr; Gini = 1 &minus; (0<sup>2</sup>+1<sup>2</sup>) = 0.'))
    flow.append(paso(3, 'Combinamos las ramas con un <b>promedio ponderado</b> por cuántos clientes tiene cada una: '
                        'Gini split = (5/8)·0.32 + (3/8)·0 = 0.20.'))
    flow.append(porque('Ponderamos por tamaño porque una rama con muchos casos debe pesar más en la impureza total que una '
                       'con pocos. Una rama pequeña y sucia "ensucia" menos el conjunto que una grande y sucia.'))
    flow.append(paso(4, '<u>Atributo "Ingreso alto".</u> Rama "Sí" = {1,2,3,5}: 3 pagan, 1 no &rArr; '
                        'Gini = 1 &minus; ((3/4)<sup>2</sup>+(1/4)<sup>2</sup>) = 0.375. '
                        'Rama "No" = {4,6,7,8}: 1 paga, 3 no &rArr; Gini = 0.375.'))
    flow.append(paso(5, 'Gini split = (4/8)·0.375 + (4/8)·0.375 = 0.375.'))
    flow.append(res('Tiene casa: 0.20 (ganancia 0.5&minus;0.20 = 0.30). Ingreso alto: 0.375 (ganancia 0.125). '
                    '&rArr; Se elige <b>"Tiene casa"</b> por menor impureza / mayor ganancia.'))
    flow.append(interp('"Tiene casa" deja una rama 100% pura (todos los que no tienen casa, no pagan), por eso reduce mucho '
                       'más la impureza. Es la variable que el algoritmo CART pondría en la raíz del árbol.'))

    flow.append(Paragraph('<b>(c) Ganancia de información (entropía) de "Tiene casa"</b>', S['body']))
    flow.append(paso(1, 'Calculamos la entropía de cada rama. Rama "Sí" (4 pagan, 1 no): p = (0.8, 0.2). '
                        'Entropía = &minus;(0.8·log<sub>2</sub>0.8 + 0.2·log<sub>2</sub>0.2).'))
    flow.append(paso(2, 'Con log<sub>2</sub>0.8 = &minus;0.3219 y log<sub>2</sub>0.2 = &minus;2.3219: '
                        '= &minus;(0.8·(&minus;0.3219) + 0.2·(&minus;2.3219)) = &minus;(&minus;0.2575 &minus; 0.4644) = 0.7219.'))
    flow.append(paso(3, 'Rama "No" (0 pagan, 3 no): nodo puro &rArr; entropía = 0.'))
    flow.append(paso(4, 'Entropía ponderada de la división = (5/8)·0.7219 + (3/8)·0 = 0.4512.'))
    flow.append(paso(5, 'Ganancia = entropía del padre &minus; entropía ponderada = 1.0 &minus; 0.4512 = 0.5488.'))
    flow.append(porque('La "ganancia de información" es cuánta incertidumbre eliminamos al dividir. Pasamos de 1 bit de '
                       'incertidumbre a solo 0.4512: la división nos "informó" 0.5488 bits sobre la clase.'))
    flow.append(res('Ganancia de información = 0.5488 bits (coincide con la conclusión de (b): es una buena división).'))

    flow.append(Paragraph('<b>(d) Criterio de parada y poda</b>', S['body']))
    flow.append(Paragraph('<b>Parada (cuándo dejar de dividir):</b> cuando el nodo es puro (todos de la misma clase), '
                          'cuando no quedan atributos, o cuando se alcanza un límite preestablecido (profundidad máxima, '
                          'mínimo de registros por hoja, ganancia mínima exigida). <b>Poda (pruning) en CART:</b> tras '
                          'construir el árbol completo (que suele sobreajustar), se recorren las ramas y se reemplazan por '
                          'hojas aquellos subárboles que aportan poca capacidad predictiva, siempre que ello no aumente '
                          '—o incluso reduzca— el error estimado en un conjunto de <b>validación</b>. Sirve para combatir '
                          'el <b>sobreajuste</b> y obtener un árbol más simple y generalizable.', S['sol']))

    # ===== Sección IV: Ensembles
    flow.append(Paragraph('Sección IV — Métodos de Consenso y Potenciación', S['seccion']))
    flow.append(item('Pregunta 4 — Bagging, AdaBoost, Random Forest'))

    flow.append(Paragraph('<b>(a) Probabilidad de ser seleccionado en un bootstrap (n = 10)</b>', S['body']))
    flow.append(intui('"Con reemplazo" significa que cada vez que sacamos un dato, lo devolvemos antes de sacar el '
                      'siguiente; por eso un mismo individuo puede salir varias veces o ninguna. Queremos saber qué tan '
                      'probable es que un individuo concreto aparezca al menos una vez en la muestra.'))
    flow.append(recuerda('Una muestra bootstrap saca n elementos <b>con reemplazo</b>. En cada extracción, un individuo '
                         'tiene probabilidad 1/n de salir, luego (1&minus;1/n) de NO salir. Como las n extracciones son '
                         'independientes, P(no salir nunca) = (1&minus;1/n)<sup>n</sup>.'))
    flow.append(paso(1, 'P(no salir en UNA extracción) = 1 &minus; 1/10 = 0.9.'))
    flow.append(paso(2, 'P(no salir en las 10 extracciones) = 0.9 multiplicado por sí mismo 10 veces = 0.9<sup>10</sup> = 0.3487.'))
    flow.append(porque('Multiplicamos las 10 probabilidades porque las extracciones son <b>independientes</b> (al haber '
                       'reemplazo, cada extracción no afecta a las demás). Multiplicar probabilidades de eventos '
                       'independientes da la probabilidad de que ocurran todos.'))
    flow.append(paso(3, 'Pasamos al complemento: P(salir al menos una vez) = 1 &minus; P(no salir nunca) = 1 &minus; 0.3487 = 0.6513.'))
    flow.append(porque('Es más fácil calcular "no salir nunca" (un solo caso) que "salir 1, 2, 3... veces" (muchos casos). '
                       'Por eso usamos la regla del complemento: P(al menos una) = 1 &minus; P(ninguna).'))
    flow.append(paso(4, 'Cuando n&rarr;&infin;, el límite (1&minus;1/n)<sup>n</sup> &rarr; e<sup>-1</sup> = 0.3679, '
                        'luego P(seleccionado) &rarr; 1 &minus; 0.3679 = 0.632.'))
    flow.append(res('Para n=10, P &asymp; 0.6513; en el límite, &asymp; 0.632 (el conocido <b>63.2%</b>).'))
    flow.append(interp('Por eso cada modelo del bagging ve, en promedio, ~63% de los datos distintos; el ~37% restante '
                       '(datos "out-of-bag") sirve para estimar el error sin necesidad de un conjunto de test aparte.'))

    flow.append(Paragraph('<b>(b) Peso &alpha; en AdaBoost.M1 (&epsilon; = 0.25)</b>', S['body']))
    flow.append(recuerda('AdaBoost combina muchos clasificadores débiles. A cada uno le da un peso '
                         '&alpha; = &frac12;·ln((1&minus;&epsilon;)/&epsilon;), donde &epsilon; es su error ponderado. '
                         'Ese &alpha; mide cuánto "vale el voto" de ese clasificador en la decisión final.'))
    flow.append(paso(1, 'Sustituimos &epsilon; = 0.25: &alpha; = &frac12;·ln((1 &minus; 0.25)/0.25) = &frac12;·ln(0.75/0.25).'))
    flow.append(paso(2, 'Calculamos el cociente: 0.75/0.25 = 3 &rArr; &alpha; = &frac12;·ln(3).'))
    flow.append(paso(3, 'Con ln(3) = 1.099: &alpha; = 0.5 · 1.099 = 0.5493.'))
    flow.append(res('&alpha; = 0.5493.'))
    flow.append(porque('La fórmula está diseñada para que un buen clasificador pese mucho y uno malo casi nada: si '
                       '&epsilon;=0.5 (acierta como lanzar una moneda) &rArr; ln(1)=0 &rArr; &alpha;=0 (voto nulo); si '
                       '&epsilon;&rarr;0 (casi perfecto) &rArr; &alpha;&rarr;&infin; (voto enorme). El cociente '
                       '(1&minus;&epsilon;)/&epsilon; es la razón aciertos/errores, y el logaritmo la convierte en un peso.'))
    flow.append(interp('&alpha;=0.5493 es un peso moderado: el clasificador es claramente mejor que el azar, así que su voto '
                       'cuenta, pero no domina por sí solo la decisión del comité.'))

    flow.append(Paragraph('<b>(c) Random Forest</b>', S['body']))
    flow.append(Paragraph('Es el método de consenso (bagging) en el que <b>todos los clasificadores base son árboles</b>. '
                          'Su diferencia con el bagging clásico: en cada división de cada árbol se considera solo un '
                          '<b>subconjunto aleatorio de atributos</b> (no todos). Esto evita que todos los árboles usen '
                          'siempre la misma variable "fuerte", los hace más distintos entre sí ("decorrelacionados") y, al '
                          'promediar árboles diversos, se reduce aún más la <b>varianza</b> del modelo final.', S['sol']))
    flow.append(Paragraph('<b>(d) Bagging vs Boosting</b>', S['body']))
    flow.append(Paragraph('<b>Bagging:</b> entrena los modelos <b>en paralelo</b>, cada uno sobre una muestra bootstrap '
                          'independiente, y los combina por voto/promedio. Ataca principalmente la <b>varianza</b> (estabiliza '
                          'modelos inestables). <b>Boosting:</b> entrena los modelos <b>en secuencia</b>; en cada paso '
                          'aumenta el peso de los individuos mal clasificados para que el siguiente modelo se concentre en '
                          'ellos, y pondera cada modelo según su acierto. Ataca principalmente el <b>sesgo</b> (mejora un '
                          'modelo débil paso a paso). AdaBoost.M1, en particular, está pensado para clasificación binaria.', S['sol']))

    # ===== Sección V: Bayes
    flow.append(Paragraph('Sección V — Redes Bayesianas y Naive Bayes', S['seccion']))
    flow.append(item('Pregunta 5 — Teorema de Bayes (prueba diagnóstica)'))
    flow.append(intui('Nos dan P(positivo | enfermo) pero queremos lo contrario: P(enfermo | positivo). El teorema de '
                      'Bayes sirve justamente para "dar vuelta" una probabilidad condicional. La clave es que la respuesta '
                      'depende mucho de qué tan rara es la enfermedad (la "prevalencia").'))
    flow.append(recuerda('Probabilidad total: P(+) = P(+|enf)·P(enf) + P(+|sano)·P(sano) (todas las formas de dar positivo). '
                         'Bayes: P(enf|+) = P(+|enf)·P(enf) / P(+).'))
    flow.append(paso(1, 'Anotamos los datos: P(+|enf) = 0.99, P(+|sano) = 0.05, P(enf) = 0.01 y por tanto '
                        'P(sano) = 1 &minus; 0.01 = 0.99.'))
    flow.append(paso(2, 'Calculamos los <b>positivos verdaderos</b> (enfermos que dan positivo): '
                        'P(+|enf)·P(enf) = 0.99·0.01 = 0.0099.'))
    flow.append(paso(3, 'Calculamos los <b>falsos positivos</b> (sanos que dan positivo): '
                        'P(+|sano)·P(sano) = 0.05·0.99 = 0.0495.'))
    flow.append(paso(4, 'Sumamos para obtener TODOS los positivos: P(+) = 0.0099 + 0.0495 = 0.0594.'))
    flow.append(porque('El denominador de Bayes es la probabilidad total de positivo porque preguntamos "de TODOS los que '
                       'dan positivo, ¿qué fracción está enferma?". Hay que contar tanto los positivos verdaderos como los '
                       'falsos para tener el universo completo de positivos.'))
    flow.append(paso(5, 'Aplicamos Bayes: P(enf|+) = positivos verdaderos / todos los positivos = 0.0099 / 0.0594 = 0.1667.'))
    flow.append(res('P(enfermo | positivo) = 0.1667 &asymp; <b>16.7%</b>.'))
    flow.append(interp('Aunque la prueba parece excelente (99% de sensibilidad), como la enfermedad es muy rara (1%), la '
                       'mayoría de los positivos provienen de la enorme masa de personas sanas. Por eso solo ~1 de cada 6 '
                       'positivos está realmente enfermo. Es la "paradoja de la prueba": la prevalencia importa tanto como '
                       'la sensibilidad.'))

    flow.append(item('Pregunta 6 — Clasificador Naive Bayes'))
    flow.append(intui('Para clasificar un caso nuevo, Naive Bayes calcula, para cada clase, qué tan "verosímil" es que esa '
                      'clase haya generado los atributos observados, multiplicado por qué tan frecuente es la clase. Gana la '
                      'clase con mayor producto.'))
    flow.append(recuerda('Naive Bayes elige la clase C que maximiza P(C)·&Pi;<sub>i</sub> P(x<sub>i</sub>|C). P(C) es la '
                         '<b>priori</b> (frecuencia de la clase). Cada P(x<sub>i</sub>|C) = (casos con ese atributo dentro de '
                         'la clase)/(total de la clase). Al final se <b>normaliza</b> dividiendo por la suma de los productos.'))
    flow.append(Paragraph('<b>(b) Clasificar al cliente Edad=Joven, Ingreso=Alto</b>', S['body']))
    flow.append(paso(1, 'Prioris (frecuencia de cada clase): P(Sí) = 6/10 = 0.6; P(No) = 4/10 = 0.4.'))
    flow.append(paso(2, 'Verosimilitudes de la clase Sí (usando las filas de la tabla): P(Joven|Sí) = 4/6 = 0.6667; '
                        'P(Alto|Sí) = 4/6 = 0.6667.'))
    flow.append(paso(3, 'Verosimilitudes de la clase No: P(Joven|No) = 1/4 = 0.25; P(Alto|No) = 1/4 = 0.25.'))
    flow.append(paso(4, 'Score Sí = P(Sí)·P(Joven|Sí)·P(Alto|Sí) = 0.6 · 0.6667 · 0.6667 = 0.2667.'))
    flow.append(paso(5, 'Score No = P(No)·P(Joven|No)·P(Alto|No) = 0.4 · 0.25 · 0.25 = 0.0250.'))
    flow.append(porque('Multiplicamos las verosimilitudes (no las sumamos) por el supuesto de <b>independencia '
                       'condicional</b>: dada la clase, asumimos que los atributos ocurren de forma independiente, y la '
                       'probabilidad conjunta de eventos independientes es el producto de sus probabilidades.'))
    flow.append(paso(6, 'Normalizamos para que sumen 1: suma = 0.2667 + 0.0250 = 0.2917 &rArr; '
                        'P(Sí|x) = 0.2667/0.2917 = 0.9143; P(No|x) = 0.0250/0.2917 = 0.0857.'))
    flow.append(porque('Los "scores" no son probabilidades reales porque omitimos el denominador P(x), igual para ambas '
                       'clases. Dividir cada uno por su suma recupera probabilidades que suman 1, sin cambiar cuál es mayor.'))
    flow.append(res('P(Sí|x) = 0.9143 &gt; P(No|x) = 0.0857 &rArr; se clasifica como <b>"Compra = Sí"</b>.'))
    flow.append(Paragraph('<b>(c) ¿Por qué "naive" (ingenuo)?</b>', S['body']))
    flow.append(Paragraph('Porque asume <b>independencia condicional</b> de los atributos dada la clase: '
                          'P(x<sub>1</sub>, x<sub>2</sub> | C) = P(x<sub>1</sub>|C)·P(x<sub>2</sub>|C). Ese supuesto es '
                          '"ingenuo" porque en la práctica los atributos casi siempre están relacionados (p. ej. edad e '
                          'ingreso). Sin embargo, simplifica enormemente el cálculo —evita estimar probabilidades conjuntas '
                          'complejas— y aun así el clasificador suele funcionar muy bien.', S['sol']))

    # ===== Sección VI: SVM y validación
    flow.append(Paragraph('Sección VI — Máquinas de Soporte Vectorial y Validación', S['seccion']))
    flow.append(item('Pregunta 7 — SVM lineal en 1-D'))
    flow.append(intui('Entre todas las fronteras que separan dos clases, la SVM elige la que deja el mayor "pasillo" vacío '
                      'entre ambas (el margen). Los puntos que tocan los bordes de ese pasillo son los vectores de soporte y '
                      'cumplen, por convención, f(x) = +1 y f(x) = &minus;1. Con esas dos ecuaciones podemos despejar la recta.'))
    flow.append(recuerda('La SVM busca el hiperplano f(x) = w·x + b que separa las clases con el <b>mayor margen</b>. Los '
                         'vectores de soporte cumplen w·x+b = +1 (clase +) y w·x+b = &minus;1 (clase &minus;). El ancho del '
                         'margen es 2/||w||.'))
    flow.append(Paragraph('<b>(a) Hallar w, b, frontera y margen</b>', S['body']))
    flow.append(paso(1, 'Escribimos las dos condiciones de soporte con los datos. Para x=+1 (clase +): w·(1) + b = +1. '
                        'Para x=&minus;1 (clase &minus;): w·(&minus;1) + b = &minus;1. Es un sistema de 2 ecuaciones, 2 incógnitas.'))
    flow.append(paso(2, 'Para eliminar w, <b>sumamos</b> ambas ecuaciones: (w + b) + (&minus;w + b) = 1 + (&minus;1). '
                        'El w se cancela: 2b = 0 &rArr; b = 0.'))
    flow.append(porque('Sumar las ecuaciones cancela w porque aparecen como +w y &minus;w. Es la técnica de eliminación '
                       'para sistemas lineales: combinamos las ecuaciones para que una incógnita desaparezca.'))
    flow.append(paso(3, 'Para eliminar b, <b>restamos</b> la segunda de la primera: (w + b) &minus; (&minus;w + b) = 1 &minus; (&minus;1). '
                        'El b se cancela: 2w = 2 &rArr; w = 1.'))
    flow.append(paso(4, 'La frontera de decisión es donde f(x)=0: w·x + b = 0 &rArr; 1·x + 0 = 0 &rArr; x = 0 '
                        '(el punto medio entre +1 y &minus;1, justo lo esperado).'))
    flow.append(paso(5, 'Ancho del margen = 2/||w|| = 2/|1| = 2 (es decir, 1 unidad de distancia a cada lado de la frontera).'))
    flow.append(porque('El margen es 2/||w|| porque las dos rectas de soporte (f=+1 y f=&minus;1) están separadas por una '
                       'diferencia de 2 en f, y al traducir esa diferencia de "valor de la función" a "distancia real" se '
                       'divide por la magnitud de w. Maximizar el margen equivale a minimizar ||w||.'))
    flow.append(res('w = 1, b = 0, frontera en x = 0, margen = 2.'))

    flow.append(Paragraph('<b>(b) Vectores de soporte, margen máximo y kernel</b>', S['body']))
    flow.append(Paragraph('<b>Vectores de soporte:</b> son los ejemplos más cercanos a la frontera, los que quedan justo '
                          'sobre los bordes del margen. Determinan por completo el hiperplano: si moviéramos los demás puntos '
                          '(sin que crucen el margen) la solución no cambiaría. <b>Por qué margen máximo:</b> entre todos los '
                          'hiperplanos que separan las clases, el de mayor margen deja más "colchón" ante datos nuevos, por lo '
                          'que <b>generaliza</b> mejor y reduce el error esperado. <b>Kernel:</b> cuando los datos no son '
                          'linealmente separables, un kernel los proyecta <i>implícitamente</i> a un espacio de mayor dimensión '
                          'donde sí lo son, calculando los productos internos en ese espacio sin construir explícitamente la '
                          'transformación (el "truco del kernel"). Así una frontera curva en el espacio original equivale a un '
                          'hiperplano recto en el espacio transformado.', S['sol']))

    flow.append(item('Pregunta 8 — Validación'))
    flow.append(Paragraph('<b>(c) Validación cruzada de k iteraciones (k-fold)</b>', S['body']))
    flow.append(Paragraph('Se divide el conjunto en k partes (folds) de tamaño similar. Se repite k veces: en cada iteración '
                          'se entrena con k&minus;1 folds y se evalúa con el fold restante, de modo que cada fold sea '
                          'exactamente una vez el conjunto de prueba. La métrica final es el <b>promedio</b> de las k '
                          'evaluaciones. Se prefiere a una única partición train/test porque: (1) <b>usa todos los datos</b> '
                          'tanto para entrenar como para validar; (2) <b>no depende</b> de una partición concreta que pudo '
                          'salir "fácil" o "difícil" por azar; (3) entrega una estimación más <b>estable y menos sesgada</b> '
                          'del desempeño real, además de una idea de su variabilidad.', S['sol']))
    flow.append(Paragraph('<b>(d) Exactitud media (5-fold)</b>', S['body']))
    flow.append(paso(1, 'Sumamos las exactitudes de los 5 folds: 0.80 + 0.85 + 0.90 + 0.75 + 0.80 = 4.10.'))
    flow.append(paso(2, 'Dividimos por el número de folds (5): 4.10 / 5 = 0.82.'))
    flow.append(porque('La métrica de k-fold es el promedio de los folds porque cada fold dio una estimación parcial del '
                       'desempeño; promediarlas resume el rendimiento global del modelo en todo el conjunto.'))
    flow.append(res('Exactitud media estimada = 0.82 = <b>82%</b>.'))

    flow.append(Spacer(1, 6))
    flow.append(hr())
    flow.append(Paragraph('Fin del solucionario.', S['nota']))


# ==================================================== PRUEBA 2 — MÓDULO IV
def _tabla_churn():
    return tbl([
        [P('Cliente', 'cell'), P('Contrato', 'cell'), P('Soporte técnico', 'cell'), P('Churn (se fuga)', 'cell')],
        [P('1', 'cell'), P('Mensual', 'cell'), P('Sí', 'cell'), P('Sí', 'cell')],
        [P('2', 'cell'), P('Mensual', 'cell'), P('No', 'cell'), P('Sí', 'cell')],
        [P('3', 'cell'), P('Mensual', 'cell'), P('No', 'cell'), P('Sí', 'cell')],
        [P('4', 'cell'), P('Mensual', 'cell'), P('No', 'cell'), P('Sí', 'cell')],
        [P('5', 'cell'), P('Mensual', 'cell'), P('Sí', 'cell'), P('No', 'cell')],
        [P('6', 'cell'), P('Anual', 'cell'), P('Sí', 'cell'), P('No', 'cell')],
        [P('7', 'cell'), P('Anual', 'cell'), P('Sí', 'cell'), P('No', 'cell')],
        [P('8', 'cell'), P('Anual', 'cell'), P('Sí', 'cell'), P('No', 'cell')],
        [P('9', 'cell'), P('Anual', 'cell'), P('No', 'cell'), P('No', 'cell')],
        [P('10', 'cell'), P('Anual', 'cell'), P('No', 'cell'), P('No', 'cell')],
    ], colw=[2*cm, 2.8*cm, 3.2*cm, 3.2*cm])

def _tabla_naive():
    return tbl([
        [P('Aprueba', 'cell'), P('N° casos', 'cell'), P('Asiste=Sí', 'cell'), P('Asiste=No', 'cell'), P('Estudia=Sí', 'cell'), P('Estudia=No', 'cell')],
        [P('Sí', 'cell'), P('6', 'cell'), P('5', 'cell'), P('1', 'cell'), P('4', 'cell'), P('2', 'cell')],
        [P('No', 'cell'), P('4', 'cell'), P('1', 'cell'), P('3', 'cell'), P('1', 'cell'), P('3', 'cell')],
    ], colw=[1.9*cm, 1.9*cm, 2.3*cm, 2.3*cm, 2.4*cm, 2.4*cm])

def _tabla_confusion():
    return tbl([
        [P('', 'cell'), P('Predicho: Churn Sí', 'cell'), P('Predicho: Churn No', 'cell')],
        [P('Real: Churn Sí', 'cellL'), P('VP = 40', 'cell'), P('FN = 10', 'cell')],
        [P('Real: Churn No', 'cellL'), P('FP = 20', 'cell'), P('VN = 30', 'cell')],
    ], colw=[4.2*cm, 4.6*cm, 4.6*cm])

def construir2(flow, sols=False):
    """Enunciado de la Prueba 2 (Módulo IV)."""
    # ---------- Sección I: Árboles
    flow.append(Paragraph('Sección I — Árboles de Decisión &nbsp;[30 pts]', S['seccion']))
    flow.append(P('<b>1.</b> Una empresa de telecomunicaciones quiere predecir la <b>fuga de clientes (churn)</b>. '
                  'Dispone de 10 clientes con dos atributos binarios:'))
    flow.append(_tabla_churn())
    flow.append(Spacer(1, 3))
    flow.append(P('<b>Datos útiles:</b> log<sub>2</sub>(0.4)=&minus;1.3219, log<sub>2</sub>(0.6)=&minus;0.7370, '
                  'log<sub>2</sub>(0.8)=&minus;0.3219, log<sub>2</sub>(0.2)=&minus;2.3219.', 'nota'))
    flow.append(P('<b>(a)</b> [9 pts] Para el nodo raíz, calcule los tres criterios de impureza: índice de Gini, '
                  'entropía y error de clasificación.'))
    flow.append(P('<b>(b)</b> [10 pts] Calcule el Gini ponderado (Gini split) de la división por "Contrato" y por '
                  '"Soporte técnico". ¿Cuál atributo conviene como nodo raíz y por qué?'))
    flow.append(P('<b>(c)</b> [7 pts] Para el atributo elegido en (b), calcule la ganancia de información (entropía).'))
    flow.append(P('<b>(d)</b> [4 pts] Describa brevemente el algoritmo de Hunt y explique, según sus resultados, '
                  'por qué se selecciona ese atributo como raíz.'))

    # ---------- Sección II: Ensembles
    flow.append(Paragraph('Sección II — Métodos de Consenso y Potenciación &nbsp;[18 pts]', S['seccion']))
    flow.append(P('<b>2.</b> Sobre métodos de ensemble:'))
    flow.append(P('<b>(a)</b> [5 pts] En <b>bagging</b>, con n = 5 datos, calcule la probabilidad de que un individuo '
                  'dado <b>sí</b> sea seleccionado en una muestra bootstrap. ¿A qué valor converge cuando n &rarr; &infin;? '
                  '(Use 0.8<sup>5</sup> = 0.3277, e<sup>-1</sup> = 0.3679.)'))
    flow.append(P('<b>(b)</b> [5 pts] En <b>AdaBoost.M1</b>, un clasificador débil tiene error &epsilon; = 0.20. '
                  'Calcule su peso &alpha; = &frac12;·ln((1&minus;&epsilon;)/&epsilon;). (Use ln(4) = 1.3863.)'))
    flow.append(P('<b>(c)</b> [4 pts] ¿Qué es un Bosque Aleatorio (Random Forest) y por qué usa un subconjunto '
                  'aleatorio de atributos en cada división?'))
    flow.append(P('<b>(d)</b> [4 pts] Explique la diferencia esencial entre bagging y boosting (potenciación).'))

    # ---------- Sección III: Bayes
    flow.append(Paragraph('Sección III — Redes Bayesianas y Naive Bayes &nbsp;[22 pts]', S['seccion']))
    flow.append(P('<b>3.</b> Un banco usa un score para detectar morosos. Se sabe: P(moroso) = 0.10, '
                  'P(score alto | moroso) = 0.80 y P(score alto | no moroso) = 0.20.'))
    flow.append(P('<b>(a)</b> [8 pts] Si un cliente obtiene score alto, calcule P(moroso | score alto) usando el '
                  'teorema de la probabilidad total y el de Bayes.'))
    flow.append(P('<b>4.</b> Clasificador Naive Bayes. Con la siguiente tabla de entrenamiento (10 estudiantes), '
                  'clasifique a uno nuevo con Asiste = Sí y Estudia = Sí.'))
    flow.append(_tabla_naive())
    flow.append(Spacer(1, 3))
    flow.append(P('<b>(b)</b> [11 pts] Calcule las probabilidades a posteriori (sin normalizar y normalizadas) y '
                  'entregue la clase predicha.'))
    flow.append(P('<b>(c)</b> [3 pts] ¿Por qué el clasificador se llama "naive" (ingenuo)?'))

    # ---------- Sección IV: SVM
    flow.append(Paragraph('Sección IV — Máquinas de Soporte Vectorial &nbsp;[16 pts]', S['seccion']))
    flow.append(P('<b>5.</b> Problema 1-D linealmente separable con dos vectores de soporte: un ejemplo de clase '
                  '+1 en x = 4 y uno de clase &minus;1 en x = 2. El clasificador es f(x) = w·x + b, con condiciones '
                  'de soporte w·x+b = +1 y w·x+b = &minus;1.'))
    flow.append(P('<b>(a)</b> [8 pts] Determine w y b, la frontera de decisión y el ancho del margen (2/||w||).'))
    flow.append(P('<b>(b)</b> [8 pts] Explique qué son los vectores de soporte, por qué la SVM busca el margen máximo '
                  'y para qué sirve un kernel cuando los datos no son linealmente separables.'))

    # ---------- Sección V: Evaluación
    flow.append(Paragraph('Sección V — Evaluación de Modelos y Validación &nbsp;[14 pts]', S['seccion']))
    flow.append(P('<b>6.</b> Un modelo de churn se evaluó sobre 100 clientes (clase positiva = "Churn Sí"), '
                  'obteniendo la siguiente matriz de confusión:'))
    flow.append(_tabla_confusion())
    flow.append(Spacer(1, 3))
    flow.append(P('<b>(a)</b> [8 pts] Calcule exactitud (accuracy), precisión (precision), exhaustividad (recall) y '
                  'F1. (Recuerde: Exactitud = (VP+VN)/total; Precisión = VP/(VP+FP); Recall = VP/(VP+FN); '
                  'F1 = 2·P·R/(P+R).)'))
    flow.append(P('<b>(b)</b> [3 pts] Explique en qué consiste la validación cruzada de k iteraciones (k-fold) y por '
                  'qué se prefiere a una única partición train/test.'))
    flow.append(P('<b>(c)</b> [3 pts] Un modelo evaluado con 4-fold CV obtuvo exactitudes de 0.78, 0.82, 0.80 y 0.84. '
                  'Calcule la exactitud media estimada.'))

    flow.append(Spacer(1, 8))
    flow.append(hr())
    flow.append(Paragraph('Fin de la prueba. Revise sus respuestas antes de entregar.', S['nota']))


def construir2_solucionario(flow):
    intro = ('Solucionario de la Prueba del Módulo IV. Para cada pregunta se indica la <b>fórmula</b>, el '
             '<b>paso a paso</b> y la <b>interpretación</b> del resultado.')
    flow.append(Paragraph(intro, S['nota']))
    flow.append(hr())

    # ===== Sección I: Árboles
    flow.append(Paragraph('Sección I — Árboles de Decisión', S['seccion']))
    flow.append(item('Pregunta 1 — Predicción de fuga de clientes (churn)'))
    flow.append(_tabla_churn())
    flow.append(Spacer(1, 4))
    flow.append(intui('El árbol divide a los clientes buscando grupos lo más "puros" posible (idealmente, cada hoja '
                      'con un solo tipo: todos churn o todos no-churn). La impureza mide cuán mezclado está un nodo; '
                      'el árbol elige la división que más la reduce.'))
    flow.append(recuerda('Con p<sub>k</sub> = proporción de la clase k: <b>Gini</b> = 1 &minus; &Sigma; p<sub>k</sub><sup>2</sup>; '
                         '<b>Entropía</b> = &minus;&Sigma; p<sub>k</sub> log<sub>2</sub> p<sub>k</sub>; '
                         '<b>Error</b> = 1 &minus; max(p<sub>k</sub>). Impureza de un split = promedio ponderado por el '
                         'tamaño de las ramas; ganancia = impureza del padre &minus; impureza ponderada.'))

    flow.append(Paragraph('<b>(a) Impureza del nodo raíz</b>', S['body']))
    flow.append(paso(1, 'Contamos clases en la raíz: de 10 clientes, 4 se fugan (Sí) y 6 no (No) &rArr; '
                        'p(Sí) = 4/10 = 0.4 y p(No) = 6/10 = 0.6.'))
    flow.append(paso(2, 'Gini = 1 &minus; (0.4<sup>2</sup> + 0.6<sup>2</sup>) = 1 &minus; (0.16 + 0.36) = 0.48.'))
    flow.append(paso(3, 'Entropía = &minus;(0.4·log<sub>2</sub>0.4 + 0.6·log<sub>2</sub>0.6) '
                        '= &minus;(0.4·(&minus;1.3219) + 0.6·(&minus;0.7370)) = &minus;(&minus;0.5288 &minus; 0.4422) = 0.9710.'))
    flow.append(paso(4, 'Error = 1 &minus; max(0.4, 0.6) = 1 &minus; 0.6 = 0.40.'))
    flow.append(res('Gini = 0.48, Entropía = 0.9710, Error = 0.40.'))

    flow.append(Paragraph('<b>(b) Gini split de cada atributo y elección</b>', S['body']))
    flow.append(paso(1, '<u>Contrato.</u> Rama "Mensual" = {1,2,3,4,5}: 4 churn, 1 no &rArr; '
                        'Gini = 1 &minus; ((4/5)<sup>2</sup>+(1/5)<sup>2</sup>) = 1 &minus; (0.64+0.04) = 0.32.'))
    flow.append(paso(2, 'Rama "Anual" = {6,7,8,9,10}: 0 churn, 5 no &rArr; nodo <b>puro</b> &rArr; Gini = 0.'))
    flow.append(paso(3, 'Gini split (Contrato) = (5/10)·0.32 + (5/10)·0 = 0.16.'))
    flow.append(paso(4, '<u>Soporte técnico.</u> Rama "Sí" = {1,5,6,7,8}: 1 churn, 4 no &rArr; Gini = 0.32. '
                        'Rama "No" = {2,3,4,9,10}: 3 churn, 2 no &rArr; '
                        'Gini = 1 &minus; ((3/5)<sup>2</sup>+(2/5)<sup>2</sup>) = 1 &minus; (0.36+0.16) = 0.48.'))
    flow.append(paso(5, 'Gini split (Soporte) = (5/10)·0.32 + (5/10)·0.48 = 0.16 + 0.24 = 0.40.'))
    flow.append(res('Contrato: 0.16 (ganancia 0.48&minus;0.16 = 0.32). Soporte: 0.40 (ganancia 0.08). '
                    '&rArr; Se elige <b>"Contrato"</b>.'))
    flow.append(interp('"Contrato" deja una rama 100% pura (todos los de contrato Anual se quedan), por eso reduce mucho '
                       'más la impureza. Sería la variable raíz del árbol.'))

    flow.append(Paragraph('<b>(c) Ganancia de información (entropía) de "Contrato"</b>', S['body']))
    flow.append(paso(1, 'Entropía rama "Mensual" (4 churn, 1 no): p = (0.8, 0.2). '
                        '= &minus;(0.8·(&minus;0.3219) + 0.2·(&minus;2.3219)) = &minus;(&minus;0.2575 &minus; 0.4644) = 0.7219.'))
    flow.append(paso(2, 'Entropía rama "Anual" (pura): 0.'))
    flow.append(paso(3, 'Entropía ponderada = (5/10)·0.7219 + (5/10)·0 = 0.3610.'))
    flow.append(paso(4, 'Ganancia = entropía del padre &minus; ponderada = 0.9710 &minus; 0.3610 = 0.6100.'))
    flow.append(res('Ganancia de información = 0.6100 bits.'))

    flow.append(Paragraph('<b>(d) Algoritmo de Hunt y elección de la raíz</b>', S['body']))
    flow.append(conc('El <b>algoritmo de Hunt</b> construye el árbol de forma <b>recursiva</b>: (1) si todos los registros '
                     'de un nodo son de la misma clase, se crea una hoja; (2) si hay mezcla, se elige el atributo que '
                     'mejor separa las clases (el de menor impureza ponderada / mayor ganancia), se divide el nodo según '
                     'ese atributo y se repite el procedimiento en cada rama. Aquí se selecciona <b>Contrato</b> como raíz '
                     'porque tiene el menor Gini split (0.16 frente a 0.40) y la mayor ganancia, dejando además una rama '
                     'completamente pura (Anual &rarr; ningún churn).'))

    # ===== Sección II: Ensembles
    flow.append(Paragraph('Sección II — Métodos de Consenso y Potenciación', S['seccion']))
    flow.append(item('Pregunta 2 — Bagging, AdaBoost, Random Forest'))

    flow.append(Paragraph('<b>(a) Probabilidad de ser seleccionado (n = 5)</b>', S['body']))
    flow.append(recuerda('Una muestra bootstrap saca n elementos con reemplazo. P(no salir nunca) = (1&minus;1/n)<sup>n</sup>; '
                         'P(salir al menos una vez) = 1 &minus; (1&minus;1/n)<sup>n</sup>.'))
    flow.append(paso(1, 'P(no salir en una extracción) = 1 &minus; 1/5 = 0.8.'))
    flow.append(paso(2, 'P(no salir en las 5) = 0.8<sup>5</sup> = 0.3277.'))
    flow.append(paso(3, 'P(seleccionado) = 1 &minus; 0.3277 = 0.6723.'))
    flow.append(paso(4, 'Cuando n&rarr;&infin;: (1&minus;1/n)<sup>n</sup> &rarr; e<sup>-1</sup> = 0.3679 &rArr; '
                        'P &rarr; 1 &minus; 0.3679 = 0.632.'))
    flow.append(res('Para n=5, P &asymp; 0.6723; en el límite, &asymp; 0.632 (63.2%).'))
    flow.append(interp('Con n pequeño la probabilidad es algo mayor que 0.632, pero conforme crece n se acerca a ese '
                       'valor; por eso se dice que cada bootstrap contiene ~63% de los datos.'))

    flow.append(Paragraph('<b>(b) Peso &alpha; en AdaBoost.M1 (&epsilon; = 0.20)</b>', S['body']))
    flow.append(recuerda('&alpha; = &frac12;·ln((1&minus;&epsilon;)/&epsilon;): pesa más cuanto menor es el error &epsilon;.'))
    flow.append(paso(1, '&alpha; = &frac12;·ln((1 &minus; 0.20)/0.20) = &frac12;·ln(0.8/0.2) = &frac12;·ln(4).'))
    flow.append(paso(2, 'ln(4) = 1.3863 &rArr; &alpha; = 0.5 · 1.3863 = 0.6931.'))
    flow.append(res('&alpha; = 0.6931.'))
    flow.append(interp('Es mayor que el del ejercicio con &epsilon;=0.25 (0.5493): a menor error, mayor peso del voto. '
                       'Si &epsilon; fuera 0.5, &alpha; sería 0 (voto inútil).'))

    flow.append(Paragraph('<b>(c) Random Forest</b>', S['body']))
    flow.append(conc('Es <b>bagging con árboles</b>: todos los clasificadores base son árboles de decisión. Además, en '
                     'cada división considera solo un <b>subconjunto aleatorio de atributos</b> (no todos). Así evita que '
                     'todos los árboles usen siempre la misma variable dominante, los vuelve más distintos entre sí '
                     '(decorrelacionados) y, al promediarlos, reduce más la <b>varianza</b> del modelo.'))
    flow.append(Paragraph('<b>(d) Bagging vs Boosting</b>', S['body']))
    flow.append(conc('<b>Bagging:</b> modelos en <b>paralelo</b> sobre bootstraps independientes, combinados por '
                     'voto/promedio; ataca la <b>varianza</b>. <b>Boosting:</b> modelos en <b>secuencia</b>; cada paso '
                     'sube el peso de los mal clasificados para que el siguiente se enfoque en ellos, y pondera cada '
                     'modelo; ataca el <b>sesgo</b>.'))

    # ===== Sección III: Bayes
    flow.append(Paragraph('Sección III — Redes Bayesianas y Naive Bayes', S['seccion']))
    flow.append(item('Pregunta 3 — Teorema de Bayes (score de morosidad)'))
    flow.append(intui('Nos dan P(score alto | moroso) pero queremos lo contrario: P(moroso | score alto). Bayes "da '
                      'vuelta" la condicional, y el denominador es la probabilidad total de tener score alto.'))
    flow.append(recuerda('P(score alto) = P(sa|mor)·P(mor) + P(sa|no mor)·P(no mor). '
                         'Bayes: P(mor|sa) = P(sa|mor)·P(mor) / P(score alto).'))
    flow.append(paso(1, 'Datos: P(sa|mor)=0.80, P(sa|no mor)=0.20, P(mor)=0.10 &rArr; P(no mor)=0.90.'))
    flow.append(paso(2, 'Morosos con score alto: 0.80·0.10 = 0.08.'))
    flow.append(paso(3, 'No morosos con score alto (falsas alarmas): 0.20·0.90 = 0.18.'))
    flow.append(paso(4, 'Probabilidad total de score alto: 0.08 + 0.18 = 0.26.'))
    flow.append(paso(5, 'Bayes: P(mor|sa) = 0.08 / 0.26 = 0.3077.'))
    flow.append(res('P(moroso | score alto) = 0.3077 &asymp; 30.8%.'))
    flow.append(interp('Aunque el score "marca" al 80% de los morosos, como los morosos son pocos (10%), una buena parte '
                       'de los score-alto son en realidad no morosos. Por eso solo ~31% de los marcados son morosos reales.'))

    flow.append(item('Pregunta 4 — Clasificador Naive Bayes'))
    flow.append(recuerda('Se elige la clase C que maximiza P(C)·&Pi;<sub>i</sub> P(x<sub>i</sub>|C). P(C) = frecuencia '
                         'de la clase; P(x<sub>i</sub>|C) = casos con ese atributo dentro de la clase / total de la clase. '
                         'Al final se normaliza dividiendo por la suma de los productos.'))
    flow.append(Paragraph('<b>(b) Clasificar a Asiste = Sí, Estudia = Sí</b>', S['body']))
    flow.append(paso(1, 'Prioris: P(Sí) = 6/10 = 0.6; P(No) = 4/10 = 0.4.'))
    flow.append(paso(2, 'Verosimilitudes clase Sí: P(Asiste=Sí|Sí) = 5/6 = 0.8333; P(Estudia=Sí|Sí) = 4/6 = 0.6667.'))
    flow.append(paso(3, 'Verosimilitudes clase No: P(Asiste=Sí|No) = 1/4 = 0.25; P(Estudia=Sí|No) = 1/4 = 0.25.'))
    flow.append(paso(4, 'Score Sí = 0.6 · 0.8333 · 0.6667 = 0.3333.'))
    flow.append(paso(5, 'Score No = 0.4 · 0.25 · 0.25 = 0.0250.'))
    flow.append(paso(6, 'Normalizamos: suma = 0.3333 + 0.0250 = 0.3583 &rArr; '
                        'P(Sí|x) = 0.3333/0.3583 = 0.9302; P(No|x) = 0.0250/0.3583 = 0.0698.'))
    flow.append(res('P(Sí|x) = 0.9302 &gt; P(No|x) = 0.0698 &rArr; se clasifica como <b>"Aprueba = Sí"</b>.'))
    flow.append(Paragraph('<b>(c) ¿Por qué "naive"?</b>', S['body']))
    flow.append(conc('Porque asume <b>independencia condicional</b> de los atributos dada la clase: '
                     'P(Asiste, Estudia | C) = P(Asiste|C)·P(Estudia|C). Es "ingenuo" porque los atributos suelen estar '
                     'relacionados, pero simplifica el cálculo y suele funcionar muy bien.'))

    # ===== Sección IV: SVM
    flow.append(Paragraph('Sección IV — Máquinas de Soporte Vectorial', S['seccion']))
    flow.append(item('Pregunta 5 — SVM lineal en 1-D'))
    flow.append(intui('La SVM elige la frontera que deja el mayor "pasillo" (margen) entre las clases. Los puntos que '
                      'tocan los bordes del pasillo son los vectores de soporte y cumplen f(x) = +1 y f(x) = &minus;1.'))
    flow.append(recuerda('Vectores de soporte: w·x+b = +1 (clase +) y w·x+b = &minus;1 (clase &minus;). '
                         'Margen = 2/||w||.'))
    flow.append(Paragraph('<b>(a) Hallar w, b, frontera y margen</b>', S['body']))
    flow.append(paso(1, 'Condiciones de soporte con los datos: para x=4 (clase +): 4w + b = +1. '
                        'Para x=2 (clase &minus;): 2w + b = &minus;1.'))
    flow.append(paso(2, '<b>Restamos</b> la segunda de la primera para eliminar b: (4w+b) &minus; (2w+b) = 1 &minus; (&minus;1) '
                        '&rArr; 2w = 2 &rArr; w = 1.'))
    flow.append(paso(3, 'Sustituimos w=1 en 4w+b=1: 4 + b = 1 &rArr; b = &minus;3.'))
    flow.append(paso(4, 'Frontera: w·x+b = 0 &rArr; x &minus; 3 = 0 &rArr; x = 3 (punto medio entre 2 y 4).'))
    flow.append(paso(5, 'Margen = 2/||w|| = 2/|1| = 2 (1 unidad a cada lado de la frontera).'))
    flow.append(res('w = 1, b = &minus;3, frontera en x = 3, margen = 2.'))

    flow.append(Paragraph('<b>(b) Vectores de soporte, margen máximo y kernel</b>', S['body']))
    flow.append(conc('<b>Vectores de soporte:</b> los ejemplos más cercanos a la frontera (sobre los bordes del margen); '
                     'determinan por completo el hiperplano (mover los demás no lo cambia). <b>Margen máximo:</b> entre '
                     'todas las fronteras que separan las clases, la de mayor margen <b>generaliza</b> mejor (más colchón '
                     'ante datos nuevos). <b>Kernel:</b> si los datos no son linealmente separables, proyecta '
                     'implícitamente a un espacio de mayor dimensión donde sí lo son, sin construir esa transformación '
                     'explícitamente ("truco del kernel").'))

    # ===== Sección V: Evaluación
    flow.append(Paragraph('Sección V — Evaluación de Modelos y Validación', S['seccion']))
    flow.append(item('Pregunta 6 — Matriz de confusión y validación'))
    flow.append(_tabla_confusion())
    flow.append(Spacer(1, 4))
    flow.append(intui('La matriz de confusión cruza lo real con lo predicho. VP/VN son los aciertos; FP es "falsa alarma" '
                      '(predijo churn y no era) y FN es "se nos escapó" (no predijo churn y sí era). Las métricas resumen '
                      'estos cuatro números desde distintos ángulos.'))
    flow.append(recuerda('Exactitud = (VP+VN)/total; Precisión = VP/(VP+FP); Recall (exhaustividad) = VP/(VP+FN); '
                         'F1 = 2·P·R/(P+R).'))
    flow.append(Paragraph('<b>(a) Cálculo de métricas</b>', S['body']))
    flow.append(paso(1, 'Datos: VP=40, FN=10, FP=20, VN=30; total = 40+10+20+30 = 100.'))
    flow.append(paso(2, 'Exactitud = (40+30)/100 = 70/100 = 0.70.'))
    flow.append(paso(3, 'Precisión = 40/(40+20) = 40/60 = 0.6667.'))
    flow.append(porque('La precisión mira "de los que predije como churn, ¿cuántos lo eran?": por eso el denominador es '
                       'VP+FP (todos los predichos positivos).'))
    flow.append(paso(4, 'Recall = 40/(40+10) = 40/50 = 0.80.'))
    flow.append(porque('El recall mira "de los churn reales, ¿cuántos detecté?": por eso el denominador es VP+FN '
                       '(todos los positivos reales).'))
    flow.append(paso(5, 'F1 = 2·(0.6667·0.80)/(0.6667+0.80) = 2·0.5333/1.4667 = 1.0667/1.4667 = 0.7273.'))
    flow.append(res('Exactitud = 0.70; Precisión = 0.6667; Recall = 0.80; F1 = 0.7273.'))
    flow.append(interp('El modelo detecta bien a los que se fugan (recall 0.80) pero con varias falsas alarmas '
                       '(precisión 0.67). El F1 (0.73) resume ese equilibrio en un solo número.'))

    flow.append(Paragraph('<b>(b) Validación cruzada k-fold</b>', S['body']))
    flow.append(conc('Se divide el conjunto en k partes (folds). Se repite k veces: se entrena con k&minus;1 folds y se '
                     'evalúa con el restante, de modo que cada fold sea una vez el de prueba; la métrica final es el '
                     '<b>promedio</b> de las k evaluaciones. Se prefiere a un único train/test porque usa todos los datos '
                     'para entrenar y validar, no depende de una partición afortunada y da una estimación más estable.'))
    flow.append(Paragraph('<b>(c) Exactitud media (4-fold)</b>', S['body']))
    flow.append(paso(1, 'Sumamos los 4 folds: 0.78 + 0.82 + 0.80 + 0.84 = 3.24.'))
    flow.append(paso(2, 'Dividimos por 4: 3.24 / 4 = 0.81.'))
    flow.append(res('Exactitud media estimada = 0.81 = 81%.'))

    flow.append(Spacer(1, 6))
    flow.append(hr())
    flow.append(Paragraph('Fin del solucionario.', S['nota']))


# ============================== PRUEBA 3 — PCA/FACTORIAL + ÁRBOLES
def _tabla_fac3():
    return tbl([
        [P('Variable', 'cell'), P('Factor 1 (&lambda;<sub>i1</sub>)', 'cell'), P('Factor 2 (&lambda;<sub>i2</sub>)', 'cell')],
        [P('X1', 'cell'), P('0.85', 'cell'), P('0.15', 'cell')],
        [P('X2', 'cell'), P('0.10', 'cell'), P('0.80', 'cell')],
        [P('X3', 'cell'), P('0.75', 'cell'), P('0.25', 'cell')],
        [P('X4', 'cell'), P('0.20', 'cell'), P('0.70', 'cell')],
    ], colw=[3.2*cm, 3.6*cm, 3.6*cm])

def _tabla_arbol3():
    return tbl([
        [P('Solicitante', 'cell'), P('Empleo estable', 'cell'), P('Garantía', 'cell'), P('Aprueba préstamo', 'cell')],
        [P('1', 'cell'), P('Sí', 'cell'), P('Sí', 'cell'), P('Sí', 'cell')],
        [P('2', 'cell'), P('Sí', 'cell'), P('Sí', 'cell'), P('Sí', 'cell')],
        [P('3', 'cell'), P('Sí', 'cell'), P('Sí', 'cell'), P('Sí', 'cell')],
        [P('4', 'cell'), P('Sí', 'cell'), P('Sí', 'cell'), P('Sí', 'cell')],
        [P('5', 'cell'), P('Sí', 'cell'), P('No', 'cell'), P('Sí', 'cell')],
        [P('6', 'cell'), P('No', 'cell'), P('Sí', 'cell'), P('Sí', 'cell')],
        [P('7', 'cell'), P('Sí', 'cell'), P('No', 'cell'), P('No', 'cell')],
        [P('8', 'cell'), P('No', 'cell'), P('No', 'cell'), P('No', 'cell')],
        [P('9', 'cell'), P('No', 'cell'), P('No', 'cell'), P('No', 'cell')],
        [P('10', 'cell'), P('No', 'cell'), P('No', 'cell'), P('No', 'cell')],
    ], colw=[2.6*cm, 3*cm, 2.6*cm, 3.4*cm])

def construir3(flow, sols=False):
    """Enunciado de la Prueba 3 (PCA/Factorial + Árboles)."""
    # ---------- Sección I: PCA
    flow.append(Paragraph('Sección I — Análisis de Componentes Principales (PCA) &nbsp;[25 pts]', S['seccion']))
    flow.append(P('<b>1.</b> Un conjunto de datos con dos variables estandarizadas tiene la siguiente matriz de '
                  'covarianzas:'))
    flow.append(P('&nbsp;&nbsp;&nbsp;&nbsp;&Sigma; = [ [6, 2], [2, 3] ]', 'body'))
    flow.append(P('<b>(a)</b> [6 pts] Calcule los valores propios (autovalores) de &Sigma;.'))
    flow.append(P('<b>(b)</b> [6 pts] Obtenga el vector propio (normalizado) asociado al mayor autovalor.'))
    flow.append(P('<b>(c)</b> [6 pts] ¿Qué proporción de la varianza total explica la 1ª componente? Si se desea '
                  'conservar al menos el 75% de la varianza, ¿cuántas componentes hay que retener?'))
    flow.append(P('<b>(d)</b> [7 pts] Explique qué representa un valor propio en PCA y por qué conviene estandarizar '
                  'las variables antes del análisis.'))

    # ---------- Sección II: Factorial
    flow.append(Paragraph('Sección II — Análisis Factorial &nbsp;[35 pts]', S['seccion']))
    flow.append(P('<b>2.</b> Un Análisis Factorial por máxima verosimilitud (rotación varimax) sobre 4 variables '
                  'estandarizadas entregó la siguiente matriz de cargas para 2 factores:'))
    flow.append(_tabla_fac3())
    flow.append(Spacer(1, 3))
    flow.append(P('<b>(a)</b> [8 pts] Calcule la comunalidad h<sup>2</sup><sub>i</sub> y la varianza específica '
                  '&psi;<sub>i</sub> de cada variable.'))
    flow.append(P('<b>(b)</b> [8 pts] Calcule la suma de cargas al cuadrado (SS loadings) de cada factor, su '
                  'proporción de varianza y la varianza acumulada.'))
    flow.append(P('<b>(c)</b> [5 pts] Interprete: ¿qué variables define principalmente cada factor?'))
    flow.append(P('<b>(d)</b> [8 pts] Para evaluar la adecuación se reportó: determinante de la matriz de '
                  'correlaciones muy bajo, KMO = 0.68 y test de Bartlett con p &lt; 0.001. Interprete cada indicador '
                  'y concluya si procede el análisis.'))
    flow.append(P('<b>(e)</b> [6 pts] ¿Qué busca la rotación varimax y por qué facilita la interpretación?'))

    # ---------- Sección III: Árboles
    flow.append(Paragraph('Sección III — Árboles de Decisión &nbsp;[40 pts]', S['seccion']))
    flow.append(P('<b>3.</b> Un banco quiere predecir si <b>aprueba un préstamo</b> (Sí/No). Dispone de 10 '
                  'solicitantes con dos atributos binarios:'))
    flow.append(_tabla_arbol3())
    flow.append(Spacer(1, 3))
    flow.append(P('<b>Datos útiles:</b> log<sub>2</sub>(0.4)=&minus;1.3219, log<sub>2</sub>(0.6)=&minus;0.7370, '
                  'log<sub>2</sub>(0.8)=&minus;0.3219, log<sub>2</sub>(0.2)=&minus;2.3219.', 'nota'))
    flow.append(P('<b>(a)</b> [10 pts] Para el nodo raíz, calcule el índice de Gini, la entropía y el error de '
                  'clasificación.'))
    flow.append(P('<b>(b)</b> [14 pts] Calcule el Gini split de la división por "Empleo estable" y por "Garantía". '
                  '¿Cuál atributo conviene como raíz y por qué?'))
    flow.append(P('<b>(c)</b> [8 pts] Para el atributo elegido en (b), calcule la ganancia de información (entropía).'))
    flow.append(P('<b>(d)</b> [8 pts] Indique un criterio de parada del árbol y explique brevemente qué hace la poda '
                  '(pruning) y para qué sirve.'))

    flow.append(Spacer(1, 8))
    flow.append(hr())
    flow.append(Paragraph('Fin de la prueba. Revise sus respuestas antes de entregar.', S['nota']))


def construir3_solucionario(flow):
    intro = ('Solucionario de la Prueba de PCA / Análisis Factorial y Árboles. Para cada pregunta se indica la '
             '<b>fórmula</b>, el <b>paso a paso</b> y la <b>interpretación</b>.')
    flow.append(Paragraph(intro, S['nota']))
    flow.append(hr())

    # ===== Sección I: PCA
    flow.append(Paragraph('Sección I — Análisis de Componentes Principales (PCA)', S['seccion']))
    flow.append(item('Pregunta 1 — Matriz de covarianzas &Sigma; = [[6, 2], [2, 3]]'))
    flow.append(intui('PCA busca las direcciones donde la nube de puntos se estira más (mayor varianza). Esas '
                      'direcciones son los vectores propios de &Sigma;, y cuánto se estira en cada una es su valor '
                      'propio &lambda;.'))
    flow.append(recuerda('Los valores propios se obtienen de det(&Sigma; &minus; &lambda;I) = 0; el vector propio de '
                         'cada &lambda; se obtiene resolviendo (&Sigma; &minus; &lambda;I)v = 0. La varianza total es '
                         'la traza (suma de la diagonal) = suma de los valores propios.'))

    flow.append(Paragraph('<b>(a) Valores propios</b>', S['body']))
    flow.append(paso(1, '&Sigma; &minus; &lambda;I = [[6&minus;&lambda;, 2], [2, 3&minus;&lambda;]] (se resta &lambda; a la diagonal).'))
    flow.append(paso(2, 'Determinante = (6&minus;&lambda;)(3&minus;&lambda;) &minus; (2)(2). Desarrollamos: '
                        '(6&minus;&lambda;)(3&minus;&lambda;) = 18 &minus; 9&lambda; + &lambda;<sup>2</sup>, y restamos 4 '
                        '&rArr; &lambda;<sup>2</sup> &minus; 9&lambda; + 14 = 0.'))
    flow.append(paso(3, 'Resolvemos la cuadrática: &lambda; = (9 &plusmn; &#8730;(81 &minus; 56))/2 = (9 &plusmn; &#8730;25)/2 '
                        '= (9 &plusmn; 5)/2 &rArr; &lambda; = 7 ó &lambda; = 2.'))
    flow.append(res('&lambda;<sub>1</sub> = 7 (el mayor) y &lambda;<sub>2</sub> = 2.'))

    flow.append(Paragraph('<b>(b) Vector propio de &lambda;<sub>1</sub> = 7</b>', S['body']))
    flow.append(paso(1, 'Sustituimos &lambda;=7: &Sigma; &minus; 7I = [[6&minus;7, 2], [2, 3&minus;7]] = [[&minus;1, 2], [2, &minus;4]].'))
    flow.append(paso(2, '1ª fila: &minus;1·v<sub>1</sub> + 2·v<sub>2</sub> = 0 &rArr; v<sub>1</sub> = 2·v<sub>2</sub>. '
                        'Un vector que cumple esto es (2, 1).'))
    flow.append(paso(3, 'Normalizamos dividiendo por su norma &#8730;(2<sup>2</sup>+1<sup>2</sup>) = &#8730;5 = 2.2361.'))
    flow.append(res('v<sub>1</sub> = (1/&#8730;5)(2, 1) &asymp; (0.894, 0.447).'))
    flow.append(interp('La 1ª componente pesa más sobre la variable de mayor varianza (la primera, con varianza 6).'))

    flow.append(Paragraph('<b>(c) Proporción de varianza y nº de componentes</b>', S['body']))
    flow.append(paso(1, 'Varianza total = traza = 6 + 3 = 9 (= 7 + 2, los valores propios). &#10003;'))
    flow.append(paso(2, 'Proporción PC1 = &lambda;<sub>1</sub>/total = 7/9 = 0.7778 = 77.8%.'))
    flow.append(paso(3, 'Como 77.8% &ge; 75% ya con la 1ª componente, basta retener <b>una</b> componente.'))
    flow.append(res('PC1 explica 77.8% &rArr; se conserva 1 componente para superar el 75%.'))

    flow.append(Paragraph('<b>(d) Significado del valor propio y estandarización</b>', S['body']))
    flow.append(conc('Un <b>valor propio</b> es la <b>varianza capturada</b> por su componente; por eso se ordenan de '
                     'mayor a menor y se eligen los primeros (los más informativos). Conviene <b>estandarizar</b> antes '
                     'porque PCA se basa en la varianza: si una variable está en unidades grandes (p. ej. ingresos en '
                     'pesos) dominaría la primera componente solo por su escala, no por su importancia real. '
                     'Estandarizando, todas parten con varianza 1 y compiten en igualdad de condiciones.'))

    # ===== Sección II: Factorial
    flow.append(Paragraph('Sección II — Análisis Factorial', S['seccion']))
    flow.append(item('Pregunta 2 — Cargas factoriales (4 variables, 2 factores)'))
    flow.append(_tabla_fac3())
    flow.append(Spacer(1, 4))
    flow.append(intui('Una carga &lambda;<sub>ij</sub> es la correlación entre la variable i y el factor j. Su cuadrado '
                      'es la proporción de varianza de esa variable explicada por el factor.'))
    flow.append(recuerda('Comunalidad h<sup>2</sup><sub>i</sub> = &Sigma;<sub>j</sub> &lambda;<sup>2</sup><sub>ij</sub> '
                         '(suma por FILA); &psi;<sub>i</sub> = 1 &minus; h<sup>2</sup><sub>i</sub>. SS loadings de un '
                         'factor = suma de cuadrados por COLUMNA; su proporción = SS / nº de variables.'))

    flow.append(Paragraph('<b>(a) Comunalidades y varianzas específicas</b>', S['body']))
    flow.append(paso(1, 'Sumamos los cuadrados de cada fila y restamos de 1:'))
    flow.append(paso(2, 'X1: h<sup>2</sup> = 0.85<sup>2</sup>+0.15<sup>2</sup> = 0.7225+0.0225 = 0.745 &rArr; &psi; = 0.255.'))
    flow.append(paso(3, 'X2: h<sup>2</sup> = 0.10<sup>2</sup>+0.80<sup>2</sup> = 0.01+0.64 = 0.65 &rArr; &psi; = 0.35.'))
    flow.append(paso(4, 'X3: h<sup>2</sup> = 0.75<sup>2</sup>+0.25<sup>2</sup> = 0.5625+0.0625 = 0.625 &rArr; &psi; = 0.375.'))
    flow.append(paso(5, 'X4: h<sup>2</sup> = 0.20<sup>2</sup>+0.70<sup>2</sup> = 0.04+0.49 = 0.53 &rArr; &psi; = 0.47.'))
    flow.append(res('h<sup>2</sup> = (0.745, 0.65, 0.625, 0.53); &psi; = (0.255, 0.35, 0.375, 0.47).'))

    flow.append(Paragraph('<b>(b) SS loadings, proporción y acumulada</b>', S['body']))
    flow.append(paso(1, 'SS(F1) = 0.85<sup>2</sup>+0.10<sup>2</sup>+0.75<sup>2</sup>+0.20<sup>2</sup> '
                        '= 0.7225+0.01+0.5625+0.04 = 1.335.'))
    flow.append(paso(2, 'SS(F2) = 0.15<sup>2</sup>+0.80<sup>2</sup>+0.25<sup>2</sup>+0.70<sup>2</sup> '
                        '= 0.0225+0.64+0.0625+0.49 = 1.215.'))
    flow.append(paso(3, 'Proporciones (sobre 4 variables): F1 = 1.335/4 = 0.3338 (33.4%); F2 = 1.215/4 = 0.3038 (30.4%).'))
    flow.append(paso(4, 'Acumulada = (1.335+1.215)/4 = 2.55/4 = 0.6375 (63.75%).'))
    flow.append(res('F1 explica 33.4%, F2 explica 30.4%; juntos 63.75% de la varianza total.'))

    flow.append(Paragraph('<b>(c) Interpretación de los factores</b>', S['body']))
    flow.append(conc('<b>Factor 1</b> tiene cargas altas en <b>X1 (0.85)</b> y <b>X3 (0.75)</b>, y bajas en X2 y X4: '
                     'representa lo que comparten X1 y X3. <b>Factor 2</b> tiene cargas altas en <b>X2 (0.80)</b> y '
                     '<b>X4 (0.70)</b>: representa lo común a X2 y X4. Hay, entonces, dos grupos de variables claramente '
                     'separados, justo lo que busca una buena solución factorial rotada.'))

    flow.append(Paragraph('<b>(d) Adecuación de los datos</b>', S['body']))
    flow.append(paso(1, '<b>Determinante muy bajo</b> (&asymp; 0): indica fuertes intercorrelaciones entre variables. '
                        'Favorable (si fuera &asymp; 1 las variables serían independientes y no habría factores).'))
    flow.append(paso(2, '<b>KMO = 0.68</b>: está entre 0.5 y 1, así que es aceptable (calidad "mediana", no excelente, '
                        'pero suficiente para continuar).'))
    flow.append(paso(3, '<b>Bartlett p &lt; 0.001</b>: se rechaza H<sub>0</sub> ("variables incorrelacionadas") &rArr; '
                        'sí existe correlación poblacional. Favorable.'))
    flow.append(res('Los tres indicadores son favorables &rArr; <b>procede el Análisis Factorial</b> (con la salvedad de '
                    'que el KMO es solo aceptable).'))

    flow.append(Paragraph('<b>(e) Rotación varimax</b>', S['body']))
    flow.append(conc('Busca una <b>estructura simple</b>: que cada factor tenga pocas cargas altas y muchas casi nulas. '
                     'Así cada variable se asocia claramente a un factor (como ocurre aquí: X1,X3 con F1 y X2,X4 con F2) '
                     'y la interpretación es directa. Al ser ortogonal, los factores siguen siendo independientes y las '
                     'cargas siguen siendo correlaciones factor-variable.'))

    # ===== Sección III: Árboles
    flow.append(Paragraph('Sección III — Árboles de Decisión', S['seccion']))
    flow.append(item('Pregunta 3 — Aprobación de préstamos'))
    flow.append(_tabla_arbol3())
    flow.append(Spacer(1, 4))
    flow.append(intui('El árbol divide a los solicitantes buscando grupos lo más puros posible. La impureza mide cuán '
                      'mezcladas están las clases; se elige la división que más la reduce.'))
    flow.append(recuerda('Con p<sub>k</sub> = proporción de la clase k: <b>Gini</b> = 1 &minus; &Sigma; p<sub>k</sub><sup>2</sup>; '
                         '<b>Entropía</b> = &minus;&Sigma; p<sub>k</sub> log<sub>2</sub> p<sub>k</sub>; '
                         '<b>Error</b> = 1 &minus; max(p<sub>k</sub>). Impureza de un split = promedio ponderado por '
                         'tamaño de las ramas; ganancia = impureza del padre &minus; impureza ponderada.'))

    flow.append(Paragraph('<b>(a) Impureza del nodo raíz</b>', S['body']))
    flow.append(paso(1, 'De 10 solicitantes, 6 aprueban (Sí) y 4 no (No) &rArr; p(Sí)=6/10=0.6, p(No)=0.4.'))
    flow.append(paso(2, 'Gini = 1 &minus; (0.6<sup>2</sup>+0.4<sup>2</sup>) = 1 &minus; (0.36+0.16) = 0.48.'))
    flow.append(paso(3, 'Entropía = &minus;(0.6·(&minus;0.7370) + 0.4·(&minus;1.3219)) = &minus;(&minus;0.4422 &minus; 0.5288) = 0.9710.'))
    flow.append(paso(4, 'Error = 1 &minus; max(0.6, 0.4) = 0.40.'))
    flow.append(res('Gini = 0.48, Entropía = 0.9710, Error = 0.40.'))

    flow.append(Paragraph('<b>(b) Gini split de cada atributo y elección</b>', S['body']))
    flow.append(paso(1, '<u>Empleo estable.</u> Rama "Sí" = {1,2,3,4,5,7}: 5 aprueban, 1 no &rArr; '
                        'Gini = 1 &minus; ((5/6)<sup>2</sup>+(1/6)<sup>2</sup>) = 1 &minus; (0.6944+0.0278) = 0.2778.'))
    flow.append(paso(2, 'Rama "No" = {6,8,9,10}: 1 aprueba, 3 no &rArr; '
                        'Gini = 1 &minus; ((1/4)<sup>2</sup>+(3/4)<sup>2</sup>) = 1 &minus; (0.0625+0.5625) = 0.375.'))
    flow.append(paso(3, 'Gini split (Empleo) = (6/10)·0.2778 + (4/10)·0.375 = 0.1667 + 0.15 = 0.3167.'))
    flow.append(paso(4, '<u>Garantía.</u> Rama "Sí" = {1,2,3,4,6}: 5 aprueban, 0 no &rArr; nodo <b>puro</b> &rArr; Gini = 0.'))
    flow.append(paso(5, 'Rama "No" = {5,7,8,9,10}: 1 aprueba, 4 no &rArr; '
                        'Gini = 1 &minus; ((1/5)<sup>2</sup>+(4/5)<sup>2</sup>) = 1 &minus; (0.04+0.64) = 0.32.'))
    flow.append(paso(6, 'Gini split (Garantía) = (5/10)·0 + (5/10)·0.32 = 0.16.'))
    flow.append(res('Empleo: 0.3167 (ganancia 0.1633). Garantía: 0.16 (ganancia 0.32). &rArr; Se elige <b>"Garantía"</b>.'))
    flow.append(interp('"Garantía" deja una rama 100% pura (todos los que dan garantía son aprobados), por eso reduce '
                       'mucho más la impureza y sería la raíz del árbol.'))

    flow.append(Paragraph('<b>(c) Ganancia de información (entropía) de "Garantía"</b>', S['body']))
    flow.append(paso(1, 'Rama "Sí" (pura): entropía = 0.'))
    flow.append(paso(2, 'Rama "No" (1 aprueba, 4 no): p = (0.2, 0.8). '
                        '= &minus;(0.2·(&minus;2.3219) + 0.8·(&minus;0.3219)) = &minus;(&minus;0.4644 &minus; 0.2575) = 0.7219.'))
    flow.append(paso(3, 'Entropía ponderada = (5/10)·0 + (5/10)·0.7219 = 0.3610.'))
    flow.append(paso(4, 'Ganancia = 0.9710 &minus; 0.3610 = 0.6100.'))
    flow.append(res('Ganancia de información = 0.6100 bits.'))

    flow.append(Paragraph('<b>(d) Criterio de parada y poda</b>', S['body']))
    flow.append(conc('<b>Parada:</b> se deja de dividir cuando el nodo es puro (todos de la misma clase), no quedan '
                     'atributos, o se alcanza un límite (profundidad máxima, mínimo de registros por hoja, ganancia '
                     'mínima). <b>Poda (pruning):</b> tras construir el árbol completo se reemplazan por hojas los '
                     'subárboles que aportan poca capacidad predictiva, siempre que no aumente el error en un conjunto '
                     'de validación. Sirve para reducir el <b>sobreajuste</b> y obtener un árbol más simple y generalizable.'))

    flow.append(Spacer(1, 6))
    flow.append(hr())
    flow.append(Paragraph('Fin del solucionario.', S['nota']))


# ============================================================ BUILD
def _decorate(canvas, doc):
    """Banda superior de color y pie con número de página en cada hoja."""
    canvas.saveState()
    w, h = letter
    # banda superior full-bleed
    canvas.setFillColor(NAVY)
    canvas.rect(0, h - 9, w, 9, fill=1, stroke=0)
    canvas.setFillColor(BLUE)
    canvas.rect(0, h - 12, w, 3, fill=1, stroke=0)
    # pie de página
    canvas.setStrokeColor(colors.HexColor('#cdd5df'))
    canvas.setLineWidth(0.6)
    canvas.line(LM, 1.25 * cm, w - RM, 1.25 * cm)
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(MUTED)
    kind = getattr(doc, '_kind', '')
    canvas.drawString(LM, 0.95 * cm, 'Minería de Datos · UTEM · %s' % kind)
    canvas.drawRightString(w - RM, 0.95 * cm, 'Página %d' % canvas.getPageNumber())
    canvas.restoreState()

SUB_PRUEBA1 = 'Minería de Datos &nbsp;&bull;&nbsp; Clasificación y Reducción de Dimensionalidad'
SUB_MOD4 = 'Minería de Datos &nbsp;&bull;&nbsp; Módulo IV: Modelamiento'
SUB_PCA_ARB = 'Minería de Datos &nbsp;&bull;&nbsp; PCA, Análisis Factorial y Árboles de Decisión'

def build(path, solucionario, enun_fn, sol_fn, subtitulo=SUB_PRUEBA1):
    doc = SimpleDocTemplate(path, pagesize=letter,
                            topMargin=1.55*cm, bottomMargin=1.7*cm,
                            leftMargin=LM, rightMargin=RM,
                            title=('Solucionario' if solucionario else 'Prueba') + ' - Minería de Datos')
    doc._kind = 'Solucionario' if solucionario else 'Prueba'
    flow = []
    encabezado(flow, solucionario, subtitulo)
    if solucionario:
        sol_fn(flow)
    else:
        enun_fn(flow)
    # Cada sección comienza en una hoja nueva (salvo la primera), para que
    # ninguna sección quede mezclada con otra en la misma página.
    processed = []
    seen_section = False
    for f in flow:
        st = getattr(f, 'style', None)
        if st is not None and getattr(st, 'name', '') == 'seccion':
            if seen_section:
                processed.append(PageBreak())
            seen_section = True
        processed.append(f)
    doc.build(processed, onFirstPage=_decorate, onLaterPages=_decorate)
    print('OK ->', path)

if __name__ == '__main__':
    # Prueba 1 — temario completo (PCA, Factorial, Árboles, Ensembles, Bayes, SVM, Validación)
    build('D:/Downloads/Prueba_MineriaDatos.pdf', False,
          lambda f: construir(f, sols=False), construir_solucionario, SUB_PRUEBA1)
    build('D:/Downloads/Solucionario_MineriaDatos.pdf', True,
          lambda f: construir(f, sols=False), construir_solucionario, SUB_PRUEBA1)
    # Prueba 2 — Módulo IV: Modelamiento (Árboles, Ensembles, Bayes, SVM, Evaluación)
    build('D:/Downloads/Prueba_Modulo4.pdf', False,
          lambda f: construir2(f, sols=False), construir2_solucionario, SUB_MOD4)
    build('D:/Downloads/Solucionario_Modulo4.pdf', True,
          lambda f: construir2(f, sols=False), construir2_solucionario, SUB_MOD4)
    # Prueba 3 — PCA / Análisis Factorial + Árboles de Decisión
    build('D:/Downloads/Prueba_PCA_Factorial_Arboles.pdf', False,
          lambda f: construir3(f, sols=False), construir3_solucionario, SUB_PCA_ARB)
    build('D:/Downloads/Solucionario_PCA_Factorial_Arboles.pdf', True,
          lambda f: construir3(f, sols=False), construir3_solucionario, SUB_PCA_ARB)
