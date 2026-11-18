"""PRÉVIA do portfólio do Vinicius com imagens reais (capas dos Reels e retratos do perfil público).
Uso interno para avaliar o layout. Sem autorização de uso: NÃO publicar."""
import json, math
from pathlib import Path
ASSETS = Path(__file__).parent / 'assets'

OUT = Path(__file__).parent
C = dict(bg='#0B0B0C', surf='#17171A', line='#2A2A2E', text='#F4EFE9', muted='#A39B92',
         brand='#8A5A3B', accent='#C98A54', green='#34D058', white='#FFFFFF', ink='#0B0B0C')
H = 'Montserrat'   # títulos (substituto embutido de Anton/Bebas Neue)
B = 'Inter'        # corpo
steps = [{'command': 'file.rename', 'params': {'name': 'Vinicius Capture — portfólio (prévia com imagens)'}}]


def _add(params):
    alias = f'n{len(steps)}'
    steps.append({'command': 'node.create', 'params': params, 'as': alias})
    return alias


def box(kind, name, x, y, w, h, parent=None, **props):
    p = dict(type=kind, name=name, x=x, y=y, width=w, height=h, props=props)
    if parent:
        p['parent'] = {'$ref': parent}
    return _add(p)


def rect(name, x, y, w, h, fill, parent, r=0, stroke=None):
    pr = dict(cornerRadius=r)
    if isinstance(fill, dict):
        pr['fills'] = [fill]
    else:
        pr['fill'] = fill
    if stroke:
        pr.update(stroke=stroke, strokeWeight=1)
    return box('rectangle', name, x, y, w, h, parent, **pr)


def txt(value, x, y, w, size=16, parent=None, color=None, font=B, style='Regular',
        align='left', ls=0, lh=1.35, height=None):
    cpl = max(1, int(w / (size * 0.5)))
    lines = sum(max(1, math.ceil(len(s) / cpl)) for s in value.split('\n'))
    h = height or math.ceil(lines * size * lh) + 4
    params = dict(type='text', name=value.replace('\n', ' ')[:60], x=x, y=y, width=w, height=h,
                  text=value, props=dict(fontFamily=font, fontSize=size, fontStyle=style,
                  fill=color or C['text'], lineHeight=f'{int(lh*100)}%', textAlign=align,
                  textAutoResize='none', letterSpacing=ls))
    if parent:
        params['parent'] = {'$ref': parent}
    _add(params)
    return h


def frame(name, x, w, h, fill=None):
    return box('frame', name, x, 0, w, h, fill=fill or C['bg'], clip=True)


def title(value, x, y, w, size, p, color=None, align='left'):
    return txt(value.upper(), x, y, w, size, p, color, H, 'ExtraBold', align, lh=1.05)


def label(value, x, y, w, p, color=None):
    return txt(value.upper(), x, y, w, 11, p, color or C['accent'], B, 'SemiBold', ls=2, lh=1.2)


def button(text, x, y, w, p, primary=True, h=56):
    rect(text, x, y, w, h, C['accent'] if primary else 'none', p, h / 2, None if primary else C['accent'])
    txt(text, x, y + (h - 18) / 2, w, 15, p, C['ink'] if primary else C['accent'], B, 'SemiBold', 'center', height=20)


def photo(alias, fname):
    steps.append({'command': 'image.replace', 'params': {'ids': [{'$ref': alias}], 'index': 0,
                  'path': str((ASSETS / fname).resolve())}})


def scrim(x, y, w, h, p, r=0):
    rect('degradê legenda', x, y, w, h, {'type': 'linearGradient', 'stops': ['#02050B00', '#02050BEE'], 'from': [0.5, 0], 'to': [0.5, 1]}, p, r)


def placeholder(name, x, y, w, h, p, caption, sub=None, r=14, img=None):
    a = rect(name, x, y, w, h, C['surf'], p, r, C['line'])
    if img:
        photo(a, img)
        scrim(x, y + h * .55, w, h * .45, p, r)
    txt(caption, x + 16, y + h - 74, w - 32, 13, p, C['text'], B, 'SemiBold', height=36)
    if sub:
        txt(sub, x + 16, y + h - 34, w - 32, 11, p, C['muted'], height=18)
    box('ellipse', 'ícone play', x + w / 2 - 22, y + h / 2 - 40, 44, 44, p, fill=C['accent'], opacity=.9)
    txt('▶', x + w / 2 - 22, y + h / 2 - 30, 44, 18, p, C['ink'], B, 'Bold', 'center', height=24)


NAV = ['Serviços', 'Portfólio', 'Processo', 'Sobre']
REELS = [('BioLab · Ocara', 'Saúde · institucional', '135 curtidas', 'biolab.png'),
         ('Inove · Dra. Erica Moraes', 'Saúde · texto em tela', 'Reel de clínica', 'inove.png'),
         ('Glow Makeup', '1 ano · evento', 'Cobertura', 'glow.png'),
         ('Farmácia Albuquerque', 'Inauguração · evento', 'Cobertura', 'farmacia.png'),
         ('Pizzaria do Mamute', 'Gastronomia · produto', 'Reel', 'mamute.png'),
         ('DM Multimarcas', 'Varejo · humor', 'Reel', 'dm.png'),
         ('Óticas Ver Prime', 'Varejo · atendimento', 'Reel', 'oticas.png'),
         ('Inove · procedimentos', 'Saúde · procedimento', 'Reel de clínica', 'erica.png')]
SERV = [('Cobertura de eventos', 'Seu evento contado do começo ao fim, do making of ao resultado.', 'Entrega em até 7 dias · vídeo principal + cortes para Reels'),
        ('Vídeos institucionais', 'Vídeos que apresentam sua empresa com profissionalismo.', 'Roteiro, captação e edição · vídeos de 30 s a 2 min'),
        ('Reels e conteúdo', 'Conteúdo curto, pensado com intenção, para vender e marcar presença.', 'Pacotes mensais com 4, 8 ou 12 vídeos')]
STEPS = ['Briefing', 'Roteiro', 'Captação', 'Edição', 'Revisão', 'Entrega']
STEP_DESC = ['Entendo o objetivo e o público da sua marca.', 'Penso a ideia e o roteiro antes de ligar a câmera.',
             'Capto com cuidado nos detalhes.', 'Edito com ritmo e identidade.',
             'Reviso cada detalhe com você.', 'Entrego pronto para publicar.']
QUOTES = [('"Atencioso, caprichoso. Ele coloca empenho e cuidado em cada produção."', '@mayborges16'),
          ('"Muito competente, trabalhos impecáveis! Parabéns pela dedicação."', '@olicelmaoliveira.farma'),
          ('"Ver a sua entrega no trabalho como videomaker e o ser humano incrível que você é me enche de alegria."', '@prof.robertalsousa')]
QUOTE_NOTE = 'Comentários públicos no Instagram do Vinicius · autorização dos autores pendente'

# ───────────────────────── 01 · Briefing ─────────────────────────
f1 = frame('01 — Briefing e evidências · 1440', 0, 1440, 1560)
label('Briefing · @viniciuscapture · 16/11/2026', 96, 80, 700, f1)
title('Do Instagram\nao portfólio web', 96, 112, 900, 64, f1)
txt('Vinicius, Videomaker & Creator Mobile. Atende negócios locais do interior do Ceará com cobertura de eventos, institucionais e Reels. Objetivo recomendado: portfólio de página única que leve ao orçamento no WhatsApp.',
    96, 268, 780, 20, f1, C['muted'])
cols = [('CONFIRMADO NO PERFIL', C['green'], ['Videomaker & Creator Mobile', 'Cobertura de eventos | Institucionais | Reels', 'Conteúdo que conecta marcas, pessoas e histórias', 'Orçamento no WhatsApp: wa.me/5585992736085', '110 posts · 1.773 seguidores', 'Edita com CapCut, grava no celular']),
        ('INFERÊNCIA', C['accent'], ['Público: pequenos e médios negócios locais', 'Região: Ocara, Quixeramobim, Beberibe, Aracoiaba', 'Base em Fortaleza (localização de 2 posts)', 'Posicionamento: autoridade e construção de marca']),
        ('A CONFIRMAR', '#E5736B', ['Preços e pacotes', 'Anos de experiência e formação', 'Autorização de uso por cliente', 'Direitos dos retratos (@samuelsanfotografo)', 'WhatsApp é o número comercial?', 'Arquivos originais dos vídeos'])]
for i, (t, col, items) in enumerate(cols):
    x = 96 + i * 424
    rect(t, x, 420, 400, 440, C['surf'], f1, 16, C['line'])
    label(t, x + 28, 448, 340, f1, col)
    y = 490
    for it in items:
        y += txt('•  ' + it, x + 28, y, 344, 15, f1, C['text']) + 12
label('Base da análise', 96, 920, 600, f1)
txt('Perfil: 110 posts. Examinados: 48 itens da grade (legenda e capa) e 5 abertos (post fixado, 2 posts de imagem, 2 Reels).\nNão analisados: stories (visualizar deixa o nome na lista de quem viu), destaques (não encontrados) e carrosséis (nenhum identificado na amostra). Reels vistos só por capa e legenda.',
    96, 952, 1100, 15, f1, C['muted'])
label('Pendências essenciais', 96, 1090, 600, f1)
pend = ['O WhatsApp da bio é o número comercial?', 'Quais clientes autorizam aparecer e quais Reels são os melhores?',
        'Existem preços, pacotes ou processo de contratação para publicar?', 'Qual a cidade-base e a região atendida?',
        'Há fotos e vídeos originais em alta resolução?', 'Anos de experiência, formação e equipamentos podem ser citados?']
y = 1124
for i, q in enumerate(pend):
    y += txt(f'{i+1}.  {q}', 96, y, 1100, 15, f1) + 10
txt('Este arquivo é só o briefing. A prévia com imagens está no quadro 04 e no 05.', 96, 1450, 1100, 12, f1, C['muted'])

# ───────────────────────── 02 · Design system ─────────────────────────
f2 = frame('02 — Design system · 1440', 1540, 1440, 1700)
label('Design system', 96, 80, 400, f2)
title('Cores, tipografia\ne voz', 96, 112, 900, 64, f2)
txt('Valores estimados a olho a partir dos retratos de estúdio e dos cards preto e branco do perfil. Não foram medidos com ferramenta.', 96, 260, 900, 16, f2, C['muted'])
label('Paleta', 96, 340, 300, f2)
pal = [('Fundo', C['bg'], 'Preto das roupas e cards'), ('Superfície', C['surf'], 'Apoio ao fundo'), ('Texto', C['text'], 'Branco quente dos cards'),
       ('Marca', C['brand'], 'Marrom/caramelo dos retratos'), ('Destaque CTA', C['accent'], 'Cobre claro derivado da marca'), ('Acento', C['green'], 'Verde das legendas em tela')]
for i, (n, hx, why) in enumerate(pal):
    x = 96 + i * 208
    rect(n, x, 376, 192, 150, hx, f2, 14, C['line'])
    txt(n, x, 540, 192, 16, f2, C['text'], B, 'SemiBold', height=22)
    txt(hx, x, 566, 192, 14, f2, C['accent'], B, 'Medium', height=20)
    txt(why, x, 590, 192, 12, f2, C['muted'])
txt('Contraste: texto #F4EFE9 sobre #0B0B0C passa AA com folga. Botão #C98A54 com texto #0B0B0C: verificar na implementação. Verde só em detalhes pequenos.', 96, 690, 1200, 14, f2, C['muted'])
label('Tipografia', 96, 770, 300, f2)
rect('amostra títulos', 96, 806, 640, 330, C['surf'], f2, 16, C['line'])
txt('TÍTULOS', 128, 830, 300, 11, f2, C['accent'], B, 'SemiBold', ls=2)
title('Presença e\nautoridade', 128, 862, 580, 56, f2)
txt('Montserrat ExtraBold · caixa-alta · 56/60\nSubstituto embutido do FigCraft. Na implementação: Anton ou Bebas Neue.', 128, 1030, 580, 13, f2, C['muted'])
rect('amostra corpo', 764, 806, 580, 330, C['surf'], f2, 16, C['line'])
txt('CORPO', 796, 830, 300, 11, f2, C['accent'], B, 'SemiBold', ls=2)
txt('Não trabalho apenas com vídeos. Trabalho com percepção, autoridade e construção de marca. Cada conteúdo nasce com intenção, estratégia e responsabilidade.', 796, 862, 520, 20, f2)
txt('Inter · 16 a 20 / 150%\nRótulos: Inter SemiBold, caixa-alta, 11 com 2 de espaçamento.', 796, 1030, 520, 13, f2, C['muted'])
label('Tom de voz', 96, 1190, 300, f2)
tones = [('Direto e confiante', '"Nada é aleatório, nada é só para preencher feed."'),
         ('Estratégico', '"Imagem como ativo estratégico."'),
         ('Humano e agradecido', '"Continue plantando. Eu ainda estou nessa construção."')]
for i, (t, q) in enumerate(tones):
    x = 96 + i * 424
    rect(t, x, 1226, 400, 170, C['surf'], f2, 16, C['line'])
    txt(t, x + 28, 1250, 344, 18, f2, C['text'], B, 'SemiBold', height=26)
    txt(q, x + 28, 1292, 344, 15, f2, C['muted'])
label('Componentes', 96, 1450, 300, f2)
button('Pedir orçamento no WhatsApp', 96, 1490, 330, f2)
button('Ver portfólio', 450, 1490, 200, f2, primary=False)
for i, chip in enumerate(['Todos', 'Saúde', 'Varejo', 'Eventos', 'Alimentação']):
    rect(chip, 690 + i * 118, 1498, 106, 40, C['accent'] if i == 0 else 'none', f2, 20, None if i == 0 else C['line'])
    txt(chip, 690 + i * 118, 1508, 106, 13, f2, C['ink'] if i == 0 else C['text'], B, 'Medium', 'center', height=20)

# ───────────────────────── 03 · Inventário ─────────────────────────
f3 = frame('03 — Inventário de conteúdo · 1440', 3080, 1440, 1500)
label('Inventário de conteúdo', 96, 80, 500, f3)
title('O que entra\nno portfólio', 96, 112, 900, 64, f3)
txt('Candidatos por engajamento e variedade. Todo item de cliente depende de autorização.', 96, 260, 900, 16, f3, C['muted'])
label('Reels de clientes', 96, 330, 400, f3)
inv = [('BioLab (Ocara)', 'DejfA-eu-2H', '135 curtidas · 8 coment.', 'Institucional de saúde'),
       ('Inove Odontologia', 'DdjAR3Hh4lu · DZ8VXc6Bczk', 'Dra. Erica Moraes · 2 Reels', 'Atendimento e procedimentos'),
       ('JR Autos e Motopeças', 'DaamiUYt5Wu', 'Reel institucional', 'Marco da empresa'),
       ('Farmácia Albuquerque', 'Dasoj06Ob-h', 'Inauguração', 'Cobertura de evento'),
       ('Glow Makeup', 'DfxDWrGBZcA', '1 ano da marca', 'Evento com retrato'),
       ('Pizzaria do Mamute', 'Da2mrqcRJ6N', 'Gastronomia', 'Produto'),
       ('DM Multimarcas', 'Derld3pJ7xs · DdeqHYDtvJv', 'Varejo', 'Mostra versatilidade e humor'),
       ('Óticas Ver Prime', 'DfK_CU3JptW', 'Varejo', 'Dia de atendimento')]
for i, (n, code, stat, why) in enumerate(inv):
    x = 96 + (i % 4) * 316
    y = 366 + (i // 4) * 180
    rect(n, x, y, 300, 160, C['surf'], f3, 14, C['line'])
    txt(n, x + 20, y + 18, 260, 16, f3, C['text'], B, 'SemiBold', height=22)
    txt(why, x + 20, y + 50, 260, 13, f3, C['muted'])
    txt(stat, x + 20, y + 98, 260, 13, f3, C['accent'], B, 'Medium', height=18)
    txt('reel/' + code, x + 20, y + 122, 260, 11, f3, C['muted'], height=16)
label('Marca pessoal e autoridade', 96, 760, 500, f3)
pers = [('Reel "Não basta ter um bom produto"', 'DeK5LhlRXyH', '90 curtidas · 89 coment.', 'Maior engajamento. Autoridade.'),
        ('Reel "Como videomaker mobile…"', 'DeSZ6UoPoEK', '69 curtidas · 57 coment.', 'Seção Sobre.'),
        ('Post "Alguns enxergam uma câmera…"', 'DVZ6fHVkbUm', '52 curtidas', 'Retrato marrom + posicionamento.'),
        ('Post fixado "LEIA ISSO"', 'DdBpNVFRrcW', '66 curtidas · 71 coment.', 'Trajetória e processo. Foto de @samuelsanfotografo.'),
        ('Card "Não é caro pagar pelo serviço…"', 'De0WzP6RTLe', '54 curtidas', 'Argumento de preço. Estilo P&B.')]
for i, (n, code, stat, why) in enumerate(pers):
    x = 96 + (i % 3) * 424
    y = 796 + (i // 3) * 190
    rect(n, x, y, 400, 170, C['surf'], f3, 14, C['line'])
    txt(n, x + 20, y + 18, 360, 15, f3, C['text'], B, 'SemiBold', height=22)
    txt(why, x + 20, y + 58, 360, 13, f3, C['muted'])
    txt(stat, x + 20, y + 108, 360, 13, f3, C['accent'], B, 'Medium', height=18)
    txt(('reel/' if n.startswith('Reel') else 'p/') + code, x + 20, y + 134, 360, 11, f3, C['muted'], height=16)
label('Materiais e pendências de autorização', 96, 1200, 600, f3)
mats = [('Retratos do Vinicius', 'Hero e Sobre', 'Direitos do fotógrafo e original em alta'), ('Reels de clientes', 'Portfólio', 'Autorização de cada cliente'),
        ('Logos dos clientes', 'Faixa de marcas', 'Autorização e arquivo oficial'), ('Comentários elogiosos', 'Prova social', 'Autorização de cada autor')]
for i, (a, b, c) in enumerate(mats):
    y = 1236 + i * 52
    txt(a, 96, y, 300, 14, f3, C['text'], B, 'SemiBold', height=20)
    txt(b, 420, y, 300, 14, f3, C['muted'], height=20)
    txt(c, 760, y, 560, 14, f3, '#E5736B', height=20)
    rect('linha', 96, y + 32, 1248, 1, C['line'], f3)

# ───────────────────────── 04 · Home desktop ─────────────────────────
d = frame('04 — Home desktop · 1440', 4620, 1440, 4740)
txt('VINICIUS CAPTURE', 96, 36, 260, 15, d, C['text'], H, 'ExtraBold', ls=1.5, height=24)
for i, n in enumerate(NAV):
    txt(n, 700 + i * 110, 38, 100, 14, d, C['muted'], height=20)
button('Orçamento', 1136, 22, 208, d, h=48)
label('Videomaker & creator mobile · Ceará', 96, 170, 700, d)
title('Vídeos que dão\npresença e\nautoridade\nà sua marca.', 96, 206, 760, 76, d)
txt('Conteúdo que conecta marcas, pessoas e histórias. Cobertura de eventos, institucionais e Reels.', 96, 548, 560, 20, d, C['muted'])
button('Pedir orçamento no WhatsApp', 96, 640, 340, d)
button('Ver portfólio', 460, 640, 200, d, primary=False)
photo(rect('retrato', 880, 130, 464, 580, C['brand'], d, 24), 'retrato-hero.png')
rect('faixa marcas', 0, 800, 1440, 120, C['surf'], d)
label('Marcas atendidas · confirmar autorização', 96, 826, 700, d, C['muted'])
txt('BioLab   ·   Inove Odontologia   ·   Farmácia Albuquerque   ·   Glow Makeup   ·   Óticas Ver Prime', 96, 864, 1250, 15, d, C['text'], B, 'Medium', height=22)
label('Serviços', 96, 1020, 300, d)
title('O que eu faço', 96, 1050, 800, 52, d)
for i, (t, desc, pend) in enumerate(SERV):
    x = 96 + i * 424
    rect(t, x, 1160, 400, 300, C['surf'], d, 18, C['line'])
    txt(f'0{i+1}', x + 32, 1190, 100, 14, d, C['accent'], H, 'ExtraBold')
    txt(t, x + 32, 1232, 340, 24, d, C['text'], H, 'Bold', height=36)
    txt(desc, x + 32, 1290, 336, 16, d, C['muted'])
    txt(pend, x + 32, 1396, 336, 13, d, C['accent'], height=40)
label('Portfólio', 96, 1580, 300, d)
title('Trabalhos recentes', 96, 1610, 900, 52, d)
for i, chip in enumerate(['Todos', 'Saúde', 'Varejo', 'Eventos', 'Alimentação']):
    rect(chip, 96 + i * 118, 1700, 106, 40, C['accent'] if i == 0 else 'none', d, 20, None if i == 0 else C['line'])
    txt(chip, 96 + i * 118, 1710, 106, 13, d, C['ink'] if i == 0 else C['text'], B, 'Medium', 'center', height=20)
for i, (n, seg, st, im) in enumerate(REELS):
    x = 96 + (i % 4) * 318
    y = 1780 + (i // 4) * 480
    placeholder(n, x, y, 300, 460, d, n, seg, img=im)
txt('PRÉVIA INTERNA · capas dos Reels do perfil público do Vinicius e de clientes, sem autorização de uso. Não publicar.', 96, 2760, 800, 12, d, C['muted'])
label('Processo', 96, 2860, 300, d)
title('Do briefing à entrega', 96, 2890, 1000, 52, d)
for i, s in enumerate(STEPS):
    x = 96 + i * 210
    rect(s, x, 2990, 190, 150, C['surf'], d, 14, C['line'])
    txt(f'0{i+1}', x + 22, 3012, 100, 13, d, C['accent'], H, 'ExtraBold')
    txt(s, x + 22, 3058, 150, 18, d, C['text'], H, 'Bold', height=26)
    txt(STEP_DESC[i], x + 22, 3092, 150, 12, d, C['muted'], height=40)
photo(rect('retrato sobre', 96, 3260, 480, 560, C['brand'], d, 24), 'retrato-sobre.png')
label('Sobre', 640, 3290, 300, d)
title('Percepção, autoridade\ne marca', 640, 3322, 704, 44, d)
txt('Alguns enxergam uma câmera. Eu enxergo posicionamento. Cada conteúdo que produzo nasce com intenção, estratégia e responsabilidade: estudo, direção e clareza de objetivo antes mesmo de ligar a câmera.', 640, 3470, 660, 18, d, C['muted'])
txt('Mais de 6 anos criando conteúdo audiovisual. Formação em Comunicação Social e cursos de roteiro e edição.', 640, 3640, 660, 16, d, C['text'], lh=1.5)
label('Prova social', 96, 3900, 300, d)
title('O que dizem', 96, 3930, 900, 52, d)
for i, (q, who) in enumerate(QUOTES):
    x = 96 + i * 424
    rect('depoimento', x, 4020, 400, 230, C['surf'], d, 18, C['line'])
    txt('\u201c', x + 28, 4030, 40, 56, d, C['accent'], B, 'Bold', height=60)
    txt(q.strip('"'), x + 28, 4084, 344, 16, d, C['text'], lh=1.45)
    txt(who, x + 28, 4210, 344, 13, d, C['accent'], B, 'SemiBold', height=20)
txt(QUOTE_NOTE, 96, 4264, 900, 11, d, C['muted'], height=16)
rect('cta final', 96, 4340, 1248, 260, C['brand'], d, 28)
title('Vamos tirar suas ideias do papel?', 140, 4380, 760, 44, d)
txt('Orçamento direto no WhatsApp.', 140, 4504, 500, 18, d, C['text'], height=26)
button('Pedir orçamento', 1040, 4442, 260, d)
rect('divisória rodapé', 96, 4640, 1248, 1, C['line'], d)
txt('Instagram @viniciuscapture     ·     WhatsApp (85) 99273-6085     ·     Threads @viniciuscapture', 96, 4660, 1000, 14, d, C['text'], height=20)
txt('© 2026 Vinicius Capture · Ceará · contato@viniciuscapture.com.br', 96, 4698, 700, 11, d, C['muted'], height=16)
txt('PRÉVIA INTERNA · textos de exemplo fictícios', 944, 4698, 400, 11, d, C['muted'], align='right', height=16)

# ───────────────────────── 05 · Home mobile ─────────────────────────
IMG = 'photo' in globals()
m = frame('05 — Home mobile · 390', 6160, 390, 4440)


def sec_head(lab, ttl, y, size=30):
    label(lab, 24, y, 300, m)
    return 30 + title(ttl, 24, y + 28, 342, size, m)


def portrait(name, x, y, w, h, fname, r=20):
    a = rect(name, x, y, w, h, C['brand'], m, r)
    if IMG:
        photo(a, fname)
    else:
        txt('RETRATO (placeholder)', x, y + h - 40, w, 11, m, C['text'], B, 'Medium', 'center', height=16)


# topo e menu
txt('VINICIUS CAPTURE', 24, 28, 240, 13, m, C['text'], H, 'ExtraBold', ls=1.2, height=20)
for k in range(3):
    rect('menu', 336, 30 + k * 8, 30, 2, C['text'], m, 1)
# hero
label('Videomaker & creator mobile · Ceará', 24, 100, 340, m)
title('Vídeos que dão\npresença e\nautoridade\nà sua marca.', 24, 130, 342, 34, m)
txt('Conteúdo que conecta marcas, pessoas e histórias. Cobertura de eventos, institucionais e Reels.', 24, 290, 342, 16, m, C['muted'])
button('Pedir orçamento no WhatsApp', 24, 372, 342, m, h=52)
button('Ver portfólio', 24, 436, 342, m, primary=False, h=52)
portrait('retrato', 24, 512, 342, 330, 'retrato-hero.png')
# marcas
rect('faixa marcas', 0, 872, 390, 150, C['surf'], m)
label('Marcas atendidas', 24, 896, 300, m, C['muted'])
txt('BioLab  ·  Inove Odontologia\nFarmácia Albuquerque  ·  Glow Makeup\nÓticas Ver Prime', 24, 928, 342, 15, m, C['text'], B, 'Medium', lh=1.6)
# serviços
y = 1064 + sec_head('Serviços', 'O que eu faço', 1064)
y += 10
for i, (t, desc, pend) in enumerate(SERV):
    rect(t, 24, y, 342, 168, C['surf'], m, 14, C['line'])
    txt(f'0{i+1}', 44, y + 16, 60, 12, m, C['accent'], H, 'ExtraBold', height=16)
    txt(t, 44, y + 40, 300, 18, m, C['text'], H, 'Bold', height=26)
    txt(desc, 44, y + 74, 302, 13, m, C['muted'])
    txt(pend, 44, y + 122, 302, 12, m, C['accent'], height=34)
    y += 184
# portfólio
y += 20
y += sec_head('Portfólio', 'Trabalhos\nrecentes', y)
y += 8
for i, chip in enumerate(['Todos', 'Saúde', 'Varejo', 'Eventos']):
    rect(chip, 24 + i * 86, y, 78, 34, C['accent'] if i == 0 else 'none', m, 17, None if i == 0 else C['line'])
    txt(chip, 24 + i * 86, y + 8, 78, 12, m, C['ink'] if i == 0 else C['text'], B, 'Medium', 'center', height=18)
txt('+', 24 + 4 * 86, y + 6, 22, 16, m, C['muted'], B, 'Medium', height=20)
y += 56
for i, r in enumerate(REELS):
    kw = {'img': r[3]} if len(r) > 3 else {}
    placeholder(r[0], 24 + (i % 2) * 175, y + (i // 2) * 290, 167, 274, m, r[0], r[1], 12, **kw)
y += 4 * 290 + 4
txt('Todos os Reels em 9:16 · toque para assistir', 24, y, 342, 11, m, C['muted'], align='center', height=16)
y += 56
# processo
y += sec_head('Processo', 'Do briefing\nà entrega', y)
y += 8
for i, s in enumerate(STEPS):
    x = 24 + (i % 2) * 175
    yy = y + (i // 2) * 128
    rect(s, x, yy, 167, 116, C['surf'], m, 12, C['line'])
    txt(f'0{i+1}', x + 16, yy + 12, 60, 11, m, C['accent'], H, 'ExtraBold', height=16)
    txt(s, x + 16, yy + 34, 140, 15, m, C['text'], H, 'Bold', height=22)
    txt(STEP_DESC[i], x + 16, yy + 62, 140, 11, m, C['muted'], height=44)
y += 3 * 128 + 44
# sobre
portrait('retrato sobre', 24, y, 342, 340, 'retrato-sobre.png')
y += 340 + 30
y += sec_head('Sobre', 'Percepção,\nautoridade\ne marca', y, 28)
y += 10
y += txt('Alguns enxergam uma câmera. Eu enxergo posicionamento. Cada conteúdo nasce com intenção, estratégia e responsabilidade: estudo, direção e clareza de objetivo antes mesmo de ligar a câmera.', 24, y, 342, 15, m, C['muted'], lh=1.5) + 14
y += txt('Mais de 6 anos criando conteúdo audiovisual. Formação em Comunicação Social e cursos de roteiro e edição.', 24, y, 342, 14, m, C['text'], lh=1.5) + 44
y += sec_head('Prova social', 'O que dizem', y)
y += 8
for q, who in QUOTES:
    rect('depoimento', 24, y, 342, 134, C['surf'], m, 14, C['line'])
    txt(q, 44, y + 20, 302, 14, m, C['text'], lh=1.45)
    txt(who, 44, y + 100, 302, 12, m, C['accent'], B, 'SemiBold', height=18)
    y += 150
y += txt(QUOTE_NOTE, 24, y, 342, 10, m, C['muted'], lh=1.4) + 40
# CTA e rodapé
rect('cta', 24, y, 342, 170, C['brand'], m, 22)
title('Vamos tirar suas\nideias do papel?', 44, y + 24, 302, 28, m)
button('Orçamento no WhatsApp', 54.5, y + 100, 281, m)
y += 170 + 26
txt('Instagram @viniciuscapture\nWhatsApp (85) 99273-6085\n© 2026 Vinicius Capture · Ceará\ncontato@viniciuscapture.com.br', 24, y, 342, 11, m, C['muted'], align='center', lh=1.6)
y += 80
txt('PRÉVIA INTERNA · textos de exemplo fictícios', 24, y, 342, 9, m, C['muted'], align='center', ls=.6, height=14)
y += 40
m_h = y + 110

steps_h = [st for st in steps if st.get('command') == 'node.create' and st['params'].get('name', '').startswith('05 — Home mobile')]
for st in steps_h:
    st['params']['height'] = m_h
(OUT / 'portfolio-img.commands.json').write_text(json.dumps(steps, ensure_ascii=False, indent=1))
print(len(steps), 'comandos')
