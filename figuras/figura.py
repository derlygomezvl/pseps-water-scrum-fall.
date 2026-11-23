"""Genera la Figura 1 del artículo: proceso Scrum + Cascada y seis sustituciones con veredicto PSP."""
W, H = 1600, 590
BW, BH = 215, 92          # base box
CW, CH = 215, 100         # candidate box
XS = [40, 300, 560, 820, 1080, 1340]
TOP = 62
GREY = '#c9c6bd'
TXT = '#2b2b2b'
SUB = '#666'
COL = {
    'verde': ('#e8f5e9', '#3a9a3e', '#2e7d32'),
    'amarillo': ('#fff6d6', '#d4a514', '#9a7400'),
    'rojo': ('#fdecec', '#d14343', '#c62828'),
}

out = []
a = out.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Inter">')
a('<defs>'
  '<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#b5b1a7"/></marker>'
  '<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#d14343"/></marker>'
  '</defs>')
a(f'<rect width="{W}" height="{H}" fill="white"/>')

def text(x, y, s, size=17, weight=400, fill=TXT, anchor='middle', style=''):
    a(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {style}>{s}</text>')

# Sprint region
a(f'<rect x="{XS[2]-22}" y="22" width="{XS[4]+BW-XS[2]+44}" height="{TOP+BH+20-22}" rx="12" fill="#f1f0ed" stroke="#bdbab2" stroke-dasharray="7 6" stroke-width="1.5"/>')
text(XS[2]-8, 44, 'Scrum: sprints (se repiten)', 15, 600, '#555', 'start')
text(XS[0], 44, 'Water: fase de Cascada', 15, 600, '#555', 'start')
text(XS[5], 44, 'Fall: cierre formal', 15, 600, '#555', 'start')

bases = [
    ('Elicitar Requisitos', 'Visión → SRS'),
    ('Revisión de Diseño', 'SRS → Doc. de Diseño'),
    ('Planificar Sprint', 'Backlog → Sprint Backlog'),
    ('Desarrollar Incremento', 'Sprint Backlog → Incremento'),
    ('Revisar Sprint', 'Incremento → Backlog'),
    ('Aceptación Formal', 'Incremento → Acta'),
]
for x, (n, s) in zip(XS, bases):
    a(f'<rect x="{x}" y="{TOP}" width="{BW}" height="{BH}" rx="10" fill="white" stroke="{GREY}" stroke-width="2"/>')
    text(x + BW / 2, TOP + 40, n, 18, 600)
    text(x + BW / 2, TOP + 66, s, 14.5, 400, SUB)
for i in range(5):
    x1, x2 = XS[i] + BW, XS[i + 1]
    a(f'<line x1="{x1+3}" y1="{TOP+BH/2}" x2="{x2-3}" y2="{TOP+BH/2}" stroke="#b5b1a7" stroke-width="2" marker-end="url(#ar)"/>')

# candidates: (column, row, id, l1, l2, verdict, why)
cands = [
    (0, 0, 'S5', 'Escribir Historias', 'de Usuario', 'rojo', 'NO RECOMENDABLE', 'R1 ✓   R2 ✗   R3 ✗'),
    (2, 0, 'S1', 'Planificar Sprint', '(Híbrida)', 'verde', 'RECOMENDABLE', 'R1 ✓   R2 ✓   R3 ✓'),
    (3, 0, 'S2', 'Desarrollar', 'Incremento (Híbrida)', 'rojo', 'NO RECOMENDABLE', 'R1 ✗   R2 ✓   R3 ✗'),
    (4, 0, 'S3', 'Revisar Sprint', 'con Gate Formal', 'verde', 'RECOMENDABLE', 'R1 ✓   R2 ✓   R3 ✓'),
    (4, 1, 'S6', 'Revisión Formal', 'de Requisitos', 'amarillo', 'CON PRECAUCIÓN', 'R1 ✓   R2 ✓ (0.5)   R3 ✓'),
    (4, 2, 'S4', 'Pruebas de', 'Aceptación Formal', 'rojo', 'NO RECOMENDABLE', 'R1 ✗   R2 ✗   R3 ✗'),
]
CY0, GAP = 215, 18
for col, row, sid, l1, l2, v, verdict, why in cands:
    x = XS[col]; y = CY0 + row * (CH + GAP)
    fill, stroke, dark = COL[v]
    a(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="{2.6 if v=="rojo" else 2}"/>')
    text(x + 14, y + 24, f'<tspan font-weight="700" fill="{dark}">{sid}</tspan>  {l1}', 16, 600, TXT, 'start')
    text(x + 14, y + 45, l2, 16, 600, TXT, 'start')
    text(x + 14, y + 69, verdict, 14.5, 700, dark, 'start')
    parts = []
    for tok in why.split('   '):
        r, mark = tok.split(' ', 1)
        c = '#9a7400' if '0.5' in mark else ('#2e7d32' if mark.startswith('✓') else '#c62828')
        parts.append(f'{r} <tspan fill="{c}" font-weight="800">{mark}</tspan>')
    a(f'<text x="{x+14}" y="{y+89}" font-size="15" font-weight="600" fill="{SUB}" xml:space="preserve">' + '    '.join(parts) + '</text>')

# "sustituye a" connectors (dashed, from base to first candidate)
for col in (0, 2, 3, 4):
    cx = XS[col] + BW / 2
    a(f'<line x1="{cx}" y1="{TOP+BH+2}" x2="{cx}" y2="{CY0-3}" stroke="#9e9a90" stroke-width="1.6" stroke-dasharray="5 5"/>')
text(XS[0] + BW / 2 + 8, 200, 'sustituye a', 13, 400, '#888', 'start')
for r in (1, 2):
    cx = XS[4] + CW - 22
    y1 = CY0 + (r - 1) * (CH + GAP) + CH
    a(f'<line x1="{cx}" y1="{y1}" x2="{cx}" y2="{y1+GAP}" stroke="#9e9a90" stroke-width="1.6" stroke-dasharray="4 4"/>')

# red dashed: Documento de Diseño as extra precondition of S2
x0 = XS[1] + BW / 2; x1 = XS[3] + CW / 2 + 40
a(f'<path d="M{x0},{TOP+BH+2} L{x0},198 L{x1},198 L{x1},{CY0-4}" fill="none" stroke="#d14343" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#arr)"/>')
text((x0 + XS[2]) / 2 + 40, 192, 'precondición extra', 14, 500, '#d14343')

# Legend / rule box (bottom-left)
lx, ly, lw, lh = XS[0], 345, XS[3] + BW - XS[0], 225
a(f'<rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="12" fill="#fafaf8" stroke="#dedbd3" stroke-width="1.5"/>')
text(lx + 22, ly + 34, 'PSEPS: la candidata H reemplaza a la actividad núcleo B solo si', 17, 700, TXT, 'start')
rules = [
    ('R1', 'no exige más: lo que pide H ya lo recibía B'),
    ('R2', 'no entrega menos: H cubre todo lo que entregaba B'),
    ('R3', 'conserva la invariante: ciclo de vida y principios'),
]
for i, (r, t) in enumerate(rules):
    text(lx + 22, ly + 66 + i * 26, f'<tspan font-weight="700">{r}</tspan>  {t}', 15.5, 400, TXT, 'start')
sx = lx + 22; sy = ly + 168
for i, (v, lab) in enumerate([('verde', 'Recomendable: R1–R3 con cobertura plena'), ('amarillo', 'Con precaución: cobertura 0.5 + adaptación'), ('rojo', 'No recomendable: falla alguna regla')]):
    fill, stroke, dark = COL[v]
    yy = sy + (i // 2) * 30
    xx = sx + (i % 2) * 380
    a(f'<circle cx="{xx+8}" cy="{yy-5}" r="8" fill="{stroke}"/>')
    text(xx + 24, yy, lab, 15, 500, TXT, 'start')

a('</svg>')
open(__import__('os').path.join(__import__('os').path.dirname(__file__), 'figura_psp.svg'), 'w').write('\n'.join(out))
print('ok')
