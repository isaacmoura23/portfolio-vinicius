# Site de portfólio do Vinicius — plano de implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (modo nativo escolhido) para executar tarefa a tarefa. Passos usam `- [ ]`.

**Goal:** Construir o site de página única do Vinicius, fiel ao design aprovado, em HTML/CSS/JS puros.

**Architecture:** `site/index.html` (conteúdo estático semântico) + `site/css/styles.css` (tokens em `:root`, mobile-first) + `site/js/main.js` (menu, filtro, modal de vídeo). Mídia em `site/img/` e `site/video/` com nomes fixos por "slug". Verificação por script Node sem dependências (`tools/check-site.mjs`) mais conferência visual no Chrome contra `design/figcraft/previews-img/`.

**Tech Stack:** HTML5, CSS3 (custom properties, grid, clamp), JS ES2020 sem build, Node 26 para o checker, ffmpeg para webp, Montserrat + Inter (Google Fonts).

**Spec:** `docs/superpowers/specs/2026-11-17-site-portfolio-vinicius-design.md`

## Global Constraints
- Local: `portifolio_Vinicios/site/`. Sem framework, sem build, sem backend, sem deploy.
- Paleta (de `design/figcraft/build_img.py`): bg `#0B0B0C`, surf `#17171A`, line `#2A2A2E`, text `#F4EFE9`, muted `#A39B92`, brand `#8A5A3B`, accent `#C98A54`, ink `#0B0B0C`.
- Títulos: Montserrat 800 em caixa-alta; corpo: Inter. Botões em pílula, accent com texto ink.
- WhatsApp: `https://wa.me/5585992736085?text=Ol%C3%A1%20Vinicius%2C%20quero%20um%20or%C3%A7amento%20de%20v%C3%ADdeo.`
- Instagram: `https://www.instagram.com/viniciuscapture/`; Threads: `https://www.threads.net/@viniciuscapture`.
- Mobile 390 px é referência; desktop 1440 px; breakpoint principal 900 px.
- Rodapé mobile = decisão do usuário: **sem barra fixa**; botão "Orçamento no WhatsApp" dentro do card do CTA (281×56 em 342 de card); abaixo, rodapé em texto centralizado.
- Textos fictícios marcados `<!-- EXEMPLO -->` e listados em `site/TEXTOS-DE-EXEMPLO.md`. Aviso "PRÉVIA INTERNA · textos de exemplo fictícios" no rodapé.
- Mídia de terceiros é placeholder; aviso visível "capas sem autorização de uso" só em `TEXTOS-DE-EXEMPLO.md`/README, não no layout.

## Review Focus
- Reel sem `video/<slug>.mp4`: modal mostra "Vídeo em breve" e não quebra.
- Modal: Esc fecha, foco volta ao cartão, vídeo pausa ao fechar, scroll do body travado.
- Filtro "Todos" restaura os 8; categoria sem item não deixa grade vazia sem aviso.
- Menu mobile: abre/fecha com teclado, fecha ao tocar num link.
- Imagem faltando: o checker falha (nenhum `src` apontando para arquivo inexistente).

---

### Task 1: Checker + estrutura + mídia
**Files:** Create `tools/check-site.mjs`, `site/img/*.webp`, `site/video/LEIA-ME.txt`, `site/TEXTOS-DE-EXEMPLO.md`.
**Interfaces:** Produces `node tools/check-site.mjs` → exit 0 se: `site/index.html` existe; todo `src`/`href` local existe; todo `<img>` tem `alt` e `loading` (exceto o do hero); há exatamente 1 `<h1>`; contém `wa.me/5585992736085`; não contém `[confirmar`; contém `<meta name="viewport"`, `og:title`, `application/ld+json`.
- [ ] Escrever o checker acima; rodar: deve falhar ("site/index.html não existe").
- [ ] Converter `design/figcraft/assets/{biolab,inove,glow,farmacia,mamute,dm,oticas,erica,retrato-hero,retrato-sobre}.png` em `site/img/<mesmo-nome>.webp` (`ffmpeg -quality 85`).
- [ ] Criar `site/video/LEIA-ME.txt` explicando: soltar `<slug>.mp4` (biolab, inove, glow, farmacia, mamute, dm, oticas, erica).
- [ ] Criar `site/TEXTOS-DE-EXEMPLO.md` listando os fictícios: 3 descrições de serviço, linha de experiência (Sobre), e-mail e "Ceará" do rodapé, descrições das 6 etapas; e o aviso de mídia sem autorização.

### Task 2: Base — head, tokens, topo e hero
**Files:** Create `site/index.html`, `site/css/styles.css`, `site/js/main.js`, `site/favicon.svg`.
**Interfaces:** Produces classes `.container`, `.btn`, `.btn--primary`, `.btn--ghost`, `.eyebrow`, `.section-title`, `.card`; `main.js` exporta nada (IIFE) e define `initMenu()`.
- [ ] `<head>`: title "Vinicius Capture | Videomaker e creator mobile no Ceará", description, canonical omitida, OG (title, description, image `img/retrato-hero.webp`), `ld+json` `ProfessionalService` (name, url Instagram, telephone `+5585992736085`).
- [ ] Header com logo "VINICIUS CAPTURE", nav (Serviços, Portfólio, Processo, Sobre) + botão "Orçamento"; hambúrguer `<button aria-expanded aria-controls="menu">` abaixo de 900 px; `initMenu()` alterna, fecha no clique de link e no Esc.
- [ ] Hero: eyebrow "Videomaker & creator mobile · Ceará", `<h1>` "Vídeos que dão presença e autoridade à sua marca.", subtítulo, botões "Pedir orçamento no WhatsApp" e "Ver portfólio" (`#portfolio`), retrato `retrato-hero.webp` (sem lazy, `fetchpriority="high"`).
- [ ] Rodar checker (ainda falha por seções ausentes é aceitável; falhas de head devem sumir).

### Task 3: Marcas, serviços e portfólio
**Files:** Modify `site/index.html`, `site/css/styles.css`, `site/js/main.js`.
**Interfaces:** Produces `initFilter()` e `initModal()`; cartões `<button class="reel" data-category="saude|varejo|eventos|alimentacao" data-slug="biolab">`.
- [ ] Faixa "Marcas atendidas": BioLab · Inove Odontologia · Farmácia Albuquerque · Glow Makeup · Óticas Ver Prime.
- [ ] Serviços (3 cards numerados, textos do design, linhas fictícias com `<!-- EXEMPLO -->`).
- [ ] Portfólio: chips Todos/Saúde/Varejo/Eventos/Alimentação (`role="tablist"` simples com `aria-pressed`); 8 reels 9:16 na ordem BioLab(saude), Inove·Dra. Erica Moraes(saude), Glow Makeup(eventos), Farmácia Albuquerque(eventos), Pizzaria do Mamute(alimentacao), DM Multimarcas(varejo), Óticas Ver Prime(varejo), Inove·procedimentos(saude); degradê inferior e legenda; ícone de play.
- [ ] `initFilter()`: filtra por `data-category`; mostra `#filtro-vazio` se 0 itens.
- [ ] `initModal()`: abre `<dialog>`; testa `video/<slug>.mp4` com `fetch(..., {method:'HEAD'})`; se existe, `<video controls playsinline>`, senão texto "Vídeo em breve"; Esc/botão fechar; pausa o vídeo; devolve foco ao cartão.

### Task 4: Processo, sobre, prova social, CTA e rodapé
**Files:** Modify `site/index.html`, `site/css/styles.css`.
- [ ] Processo: 6 etapas (Briefing, Roteiro, Captação, Edição, Revisão, Entrega) com as descrições de `design/figcraft/build_img.py` (`STEP_DESC`).
- [ ] Sobre: `retrato-sobre.webp`, título "Percepção, autoridade e marca", texto do post DVZ6fHVkbUm, linha de experiência (EXEMPLO).
- [ ] Prova social: 3 `<blockquote>` com `QUOTES` de `build_img.py` e a nota "Comentários públicos no Instagram do Vinicius · autorização dos autores pendente".
- [ ] CTA: card brand com "Vamos tirar suas ideias do papel?" e botão de WhatsApp dentro (mobile 281×56 centralizado).
- [ ] Rodapé: divisória, links Instagram/WhatsApp/Threads, "© 2026 Vinicius Capture · Ceará · contato@viniciuscapture.com.br", "PRÉVIA INTERNA · textos de exemplo fictícios".
- [ ] Rodar `node tools/check-site.mjs`: deve passar (exit 0).

### Task 5: Acabamento e verificação visual
**Files:** Modify `site/css/styles.css`, `site/js/main.js`.
- [ ] Animação de entrada sutil (opacity/translate por IntersectionObserver), desativada com `prefers-reduced-motion`.
- [ ] `focus-visible` com contorno accent em todos os interativos; contraste ≥ AA.
- [ ] Servir `python3 -m http.server 8765 --directory site` e comparar no Chrome 390/768/1440 com `design/figcraft/previews-img/04…png` e `05…png`; corrigir diferenças visíveis.
- [ ] Testes manuais do Review Focus (modal sem vídeo, Esc, filtro vazio, menu por teclado).

### Task 6: Revisão independente
- [ ] Despachar um agente revisor (somente leitura) para: responsividade, acessibilidade, links, SEO, aderência ao spec. Corrigir o que for confirmado; reportar o resto.

## Self-review
Cobertura do spec: seções (T2–T4), filtro/modal (T3), SEO (T2), mídia por nomes fixos (T1), textos de exemplo (T1/T4), rodapé do usuário (Global Constraints + T4), revisão com agente (T6). Nomes consistentes: `initMenu`, `initFilter`, `initModal`, slugs iguais em img/video.
