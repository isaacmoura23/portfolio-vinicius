"""Versão 2 — portfólio do Vinicius (@viniciuscapture) no estilo "menu de jogo" da referência:
capa, perfil, mosaico de projetos e contato, em telas 16:9 (1600x900).
Nada da referência foi copiado (fotos, nome, marca): só a estrutura e o clima visual.
Fotos e vídeos do Vinicius e de clientes são placeholders até haver autorização."""
import json, math
from pathlib import Path

OUT = Path(__file__).parent
C = dict(bg='#02050B', navy='#06182B', glow='#0C4C7C', glow2='#1A78B8', pill='#A9D1F5',
         text='#E8EDF3', muted='#8FA0B3', line='#1B2D42', brand='#8A5A3B', accent='#C98A54',
         ink='#02050B', warn='#E5736B')
D = 'DIN Condensed'   # títulos (fonte de sistema do Mac; na implementação: Bebas Neue/Anton)
B = 'Inter'
steps = [{'command': 'file.rename', 'params': {'name': 'Vinicius Capture — portfólio v2 (menu de jogo)'}}]


def _add(params):
    alias = f'n{len(steps)}'
    steps.append({'command': 'node.create', 'params': params, 'as': alias})
    return alias


def box(kind, name, x, y, w, h, parent=None, **props):
    p = dict(type=kind, name=name, x=x, y=y, width=w, height=h, props=props)
    if parent:
        p['parent'] = {'$ref': parent}
    return _add(p)


def rect(name, x, y, w, h, fill, parent, r=0, stroke=None, **extra):
    pr = dict(cornerRadius=r, **extra)
    if isinstance(fill, dict):
        pr['fills'] = [fill]
    else:
        pr['fill'] = fill
    if stroke:
        pr.update(stroke=stroke, strokeWeight=1)
    return box('rectangle', name, x, y, w, h, parent, **pr)


def grad(a, b, kind='radialGradient'):
    return {'type': kind, 'stops': [a, b]}


def txt(value, x, y, w, size=16, parent=None, color=None, font=B, style='Regular',
        align='left', ls=0, lh=1.3, height=None):
    cpl = max(1, int(w / (size * (0.42 if font == D else 0.5))))
    lines = sum(max(1, math.ceil(len(s) / cpl)) for s in value.split('\n'))
    h = height or math.ceil(lines * size * lh) + 4
    params = dict(type='text', name=value.replace('\n', ' ')[:50], x=x, y=y, width=w, height=h,
                  text=value, props=dict(fontFamily=font, fontSize=size, fontStyle=style,
                  fill=color or C['text'], lineHeight=f'{int(lh*100)}%', textAlign=align,
                  textAutoResize='none', letterSpacing=ls))
    if parent:
        params['parent'] = {'$ref': parent}
    _add(params)
    return h


def head(value, x, y, w, size, p, color=None, align='left', ls=1):
    return txt(value.upper(), x, y, w, size, p, color or C['text'], D, 'Bold', align, ls, lh=1.0)


def frame(name, x, w=1600, h=900):
    f = box('frame', name, x, 0, w, h, fill=C['bg'], clip=True)
    return f


def glow(p, cx, cy, r, a=C['glow'], b=C['bg']):
    rect('brilho azul', cx - r, cy - r, 2 * r, 2 * r, grad(a, b), p, r)


def tabs(p, active):
    for i, n in enumerate(['PERFIL', 'PROJETOS', 'CONTATO']):
        x = 600 + i * 140
        on = i == active
        if on:
            rect('aba ativa', x, 56, 120, 34, C['pill'], p, 17)
        txt(n, x, 64, 120, 13, p, C['ink'] if on else C['muted'], B, 'Medium', 'center', 1, height=20)


def mono(p, x=70, y=50):
    txt('VC', x, y, 90, 54, p, C['text'], D, 'Bold', ls=2, lh=1.0, height=60)


def note(p, text='Estudo visual · fotos e vídeos são placeholders, sujeitos a autorização'):
    txt(text, 70, 860, 900, 11, p, C['muted'], height=16)


# ─────────────── 01 · Capa ───────────────
f1 = frame('01 — Capa · 1600x900', 0)
glow(f1, 800, 760, 760)
mono(f1, 130, 110)
rect('forma do retrato', 0, 330, 560, 340, grad(C['accent'], C['brand'], 'linearGradient'), f1, [0, 170, 170, 0])
rect('retrato (placeholder)', 90, 355, 330, 290, C['navy'], f1, 24, C['line'])
txt('RETRATO DE ESTÚDIO\nsubstituir pelo original\n(direitos do fotógrafo)', 90, 478, 330, 13, f1, C['muted'], B, 'Medium', 'center')
head('Portfólio', 600, 300, 760, 210, f1, '#D5D9DF', ls=0)
head('2026', 1330, 330, 240, 112, f1, C['text'], ls=0)
rect('quadradinho', 746, 580, 14, 14, C['text'], f1)
txt('VIDEOMAKER & CREATOR MOBILE', 770, 576, 420, 17, f1, C['text'], B, 'Medium', ls=1, height=22)
for i, n in enumerate(['INICIAR', 'PROJETOS', 'CONTATO']):
    txt(n, 650, 690 + i * 46, 300, 17, f1, C['text'], B, 'Medium', 'center', 2, height=24)
note(f1)

# ─────────────── 02 · Perfil ───────────────
f2 = frame('02 — Perfil · 1600x900', 1700)
glow(f2, 380, 560, 340)
glow(f2, 1500, 100, 380, '#0A2F4F')
tabs(f2, 0)
mono(f2)
txt('OLÁ, EU SOU', 140, 150, 400, 24, f2, C['muted'], B, 'Regular', ls=2, height=30)
head('Vinicius', 140, 184, 400, 70, f2)
rect('retrato (placeholder)', 160, 290, 440, 540, grad(C['accent'], C['brand'], 'linearGradient'), f2, 28)
txt('RETRATO\nsubstituir pelo original', 160, 520, 440, 13, f2, C['text'], B, 'Medium', 'center')
head('Sobre mim', 760, 140, 700, 46, f2)
txt('Videomaker e creator mobile. Conteúdo que conecta marcas, pessoas e histórias. Cada vídeo nasce com intenção, estratégia e responsabilidade: eu capto, dirijo, roteirizo, edito, reviso e entrego.',
    760, 198, 720, 18, f2, C['text'], lh=1.5)
head('Ferramentas', 760, 330, 500, 34, f2)
for i in range(6):
    x = 760 + i * 92
    on = i == 0
    rect('ferramenta', x, 384, 74, 74, C['text'] if on else 'none', f2, 18, None if on else C['line'])
    txt('CapCut' if on else '+', x, 408 if on else 405, 74, 14 if on else 22, f2, C['ink'] if on else C['muted'], B, 'SemiBold', 'center', height=24)
txt('Só o CapCut foi citado pelo Vinicius. [confirmar: demais ferramentas]', 760, 468, 700, 12, f2, C['warn'], height=18)
head('Serviços', 760, 520, 340, 34, f2)
for i, s in enumerate(['Cobertura de eventos', 'Institucionais', 'Reels e conteúdo']):
    txt('•  ' + s, 760, 566 + i * 30, 340, 17, f2, C['text'], height=24)
head('Clientes', 1130, 520, 340, 34, f2)
for i, s in enumerate(['BioLab', 'Inove Odontologia', 'Farmácia Albuquerque', 'Glow Makeup']):
    txt('•  ' + s, 1130, 566 + i * 30, 340, 17, f2, C['text'], height=24)
txt('[confirmar: autorização de cada cliente]', 1130, 690, 380, 12, f2, C['warn'], height=18)
head('Região', 760, 740, 340, 34, f2)
txt('Ocara · Quixeramobim · Beberibe · Aracoiaba [confirmar]', 760, 786, 700, 17, f2, C['text'], height=24)
note(f2)

# ─────────────── 03 · Projetos ───────────────
f3 = frame('03 — Projetos · 1600x900', 3400)
glow(f3, 120, 80, 420, '#0A3A60')
glow(f3, 1560, 760, 420, '#0A3A60')
tabs(f3, 1)
mono(f3)
head('Recap de projetos 2026', 400, 126, 800, 76, f3, '#C9CED6', 'center', 0)
rect('aviso', 1130, 164, 200, 30, 'none', f3, 15, C['warn'])
txt('AUTORIZAÇÃO PENDENTE', 1130, 171, 200, 10, f3, C['warn'], B, 'SemiBold', 'center', 1, height=16)
tiles = [(190, 250, 200, 355, 'BioLab · Ocara', 'Saúde · institucional'),
         (410, 250, 320, 170, 'Inove · Dra. Erica Moraes', 'Saúde · texto em tela'),
         (750, 250, 320, 170, 'Inove · procedimentos', 'Saúde · procedimento'),
         (1090, 250, 320, 170, 'Glow Makeup', '1 ano · evento'),
         (410, 440, 205, 365, 'Farmácia Albuquerque', 'Inauguração'),
         (635, 440, 205, 365, 'Pizzaria do Mamute', 'Gastronomia'),
         (860, 440, 205, 365, 'DM Multimarcas', 'Varejo'),
         (1085, 440, 325, 175, 'Óticas Ver Prime', 'Varejo · atendimento'),
         (190, 625, 200, 180, 'Reel · bom produto', 'Autoridade'),
         (1085, 635, 325, 170, 'Card · "Não é caro…"', 'Argumento de preço')]
for (x, y, w, h, n, s) in tiles:
    rect(n, x, y, w, h, grad('#0F4A78', '#050B14', 'linearGradient'), f3, 10, C['line'])
    box('ellipse', 'play', x + 14, y + 14, 26, 26, f3, fill=C['accent'], opacity=.9)
    txt('▶', x + 14, y + 19, 26, 10, f3, C['ink'], B, 'Bold', 'center', height=16)
    txt(n, x + 14, y + h - 52, w - 28, 12, f3, C['text'], B, 'SemiBold', height=34)
    txt(s, x + 14, y + h - 22, w - 28, 10, f3, C['muted'], height=14)
note(f3, 'Capas e vídeos entram após autorização de cada cliente · estudo visual')

# ─────────────── 04 · Contato ───────────────
f4 = frame('04 — Contato · 1600x900', 5100)
glow(f4, 800, 880, 700, '#0A2F4F')
tabs(f4, 2)
mono(f4)
head('Contato', 540, 170, 400, 56, f4, '#C9CED6')
txt('[confirmar: o WhatsApp é o número comercial?]', 540, 560, 420, 12, f4, C['warn'], height=18)
rect('retrato circular (placeholder)', 150, 240, 340, 340, grad(C['accent'], C['brand'], 'linearGradient'), f4, 170)
txt('RETRATO', 150, 396, 340, 13, f4, C['text'], B, 'Medium', 'center', height=18)
txt('VINICIUS', 150, 600, 340, 20, f4, C['text'], D, 'Bold', 'center', 2, height=26)
txt('Videomaker & Creator Mobile', 150, 630, 340, 13, f4, C['muted'], height=18)
socials = [('IG', 'Instagram', '@viniciuscapture'), ('WA', 'WhatsApp', '(85) 99273-6085'),
           ('TH', 'Threads', '@viniciuscapture')]
for i, (ic, net, handle) in enumerate(socials):
    x = 540 + i * 36
    y = 270 + i * 90
    rect(net, x, y, 56, 56, C['text'], f4, 28)
    txt(ic, x, y + 18, 56, 15, f4, C['ink'], B, 'Bold', 'center', height=20)
    txt(net.upper(), x + 76, y + 6, 330, 14, f4, C['muted'], B, 'Medium', ls=1.5, height=18)
    txt(handle, x + 76, y + 28, 380, 16, f4, C['text'], B, 'SemiBold', height=22)
head('Obrigado', 1000, 230, 560, 150, f4, '#C9CED6', ls=0)
head('2026', 1000, 380, 560, 150, f4, '#8F98A5', ls=0)
rect('botão WhatsApp', 1000, 600, 440, 60, C['accent'], f4, 30)
txt('PEDIR ORÇAMENTO NO WHATSAPP', 1000, 619, 440, 15, f4, C['ink'], B, 'Bold', 'center', 1, height=22)
note(f4)

(OUT / 'portfolio-v2.commands.json').write_text(json.dumps(steps, ensure_ascii=False, indent=1))
print(len(steps), 'comandos')
