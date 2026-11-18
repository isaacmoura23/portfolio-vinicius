# Site de portfólio do Vinicius (@viniciuscapture) — design

Data: 2026-11-17 · Status: aprovado pelo usuário em 2026-11-17 ("pode sim")

## Intenção
Transformar o design aprovado no FigCraft (`design/figcraft/vinicius-portfolio-imagens.figcraft`, quadros 04 desktop e 05 mobile, com as edições manuais do usuário) em um site real de página única. Objetivo do visitante: pedir orçamento pelo WhatsApp. Público: pequenos e médios negócios locais do Ceará.

## Metas
- Fidelidade ao design aprovado (paleta, tipografia, seções, textos, ordem).
- Mobile-first, rápido, acessível (WCAG AA), SEO básico.
- Trocar mídia (capas e vídeos) apenas soltando arquivos nas pastas, sem mexer no código.

## Não-metas
- Backend, formulário com envio, CMS, painel.
- Publicar ou fazer deploy (o usuário decide depois).
- Next.js ou frameworks.

## Anti-metas (falhas mesmo que funcione)
- Publicar imagens/vídeos de terceiros sem autorização como se fossem finais.
- Textos fictícios sem marcação, parecendo fatos do Vinicius.
- Quebrar o layout do rodapé mobile que o usuário definiu (botão dentro do card do CTA, sem barra fixa).

## Restrições
- Sem etapa de build: HTML, CSS e JS puros, como os outros sites do usuário (grow, Bellezza, AlfaFit). Local: `portifolio_Vinicios/site/`.
- Capas atuais são capturas de tela de baixa resolução (≈540 px) em `design/figcraft/assets/`; só servem de placeholder.
- Fonte dos títulos: Montserrat ExtraBold; corpo: Inter (Google Fonts ou local).

## Abordagens consideradas
1. **HTML/CSS/JS puros** (escolhida): casa com o padrão do usuário, zero build, deploy direto no Vercel. Custo: sem componentes reutilizáveis.
2. Next.js 15 + Tailwind + Framer Motion (sugerida pela skill de Instagram): componentização e animações prontas, mas exige build, node_modules e foge do padrão dos outros sites.
3. Artefato único HTML: rápido, mas não vira projeto organizado com pastas de mídia.

## Design
Seções, em ordem: topo com menu (hambúrguer no mobile) → hero (título, subtítulo, 2 botões, retrato) → marcas atendidas → serviços (3 cards) → portfólio (filtro Todos/Saúde/Varejo/Eventos/Alimentação + 8 Reels 9:16) → processo (6 etapas com descrição) → sobre (retrato + texto + linha de experiência) → prova social (3 comentários reais, autorização pendente) → CTA final (botão dentro do card) → rodapé (Instagram, WhatsApp, Threads, copyright, aviso de prévia).

Comportamento:
- Filtro do portfólio por categoria (JS simples).
- Reel abre em modal com `<video>` se `video/<slug>.mp4` existir; senão mostra "vídeo em breve".
- Botões de WhatsApp: `https://wa.me/5585992736085?text=...` (mensagem pronta).
- Imagens com `loading="lazy"`, `alt` descritivo, `prefers-reduced-motion` respeitado.
- SEO: title, description, Open Graph, schema.org (`ProfessionalService`), H1 único.

Mídia: `site/img/` (retratos e capas) e `site/video/` com nomes fixos (ex.: `biolab.mp4`). Placeholders copiados de `design/figcraft/assets/`.

Textos de exemplo (fictícios) ficam marcados com `<!-- EXEMPLO -->` e listados em `site/TEXTOS-DE-EXEMPLO.md` para troca antes de publicar.

## Deixado para o construtor
Detalhes de espaçamento exatos (seguir os valores do design), animações sutis de entrada, estrutura de CSS (variáveis em `:root`), favicon.

## Verificação
Revisão independente por agente (responsividade 390/768/1440, contraste, foco de teclado, links) e conferência visual contra as prévias em `design/figcraft/previews-img/`.
