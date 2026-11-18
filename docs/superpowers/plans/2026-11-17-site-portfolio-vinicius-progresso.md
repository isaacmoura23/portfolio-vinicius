# Progresso — plano: docs/superpowers/plans/2026-11-17-site-portfolio-vinicius.md
Sem git: sem worktree/commits (Ruling). Ledger neste arquivo.
Pre-flight: tarefas 2-4 compartilham index.html/styles.css/main.js; classes e funções (initMenu/initFilter/initModal) definidas no plano; sem conflitos.
Ruling: imagens em JPEG (.jpg) em vez de WebP — ffmpeg local sem encoder webp — custo se errado: peso ~20% maior.
Task 1: checker RED confirmado (site/index.html não existe); mídia e notas criadas.
Task 2-4: complete — index.html, styles.css, main.js, favicon.svg criados; checker GREEN (10 imagens, 22 refs).
Ruling: reveal só com html.js + gancho ?all para capturas — evita conteúdo invisível sem JS — custo: 1 linha de código de teste em produção.
Ruling: limpeza do modal roda também direto em fechar() (não só no evento close) — close não disparou em headless — custo: nenhum (idempotente).
Task 5: e2e em Chrome headless — 22/22 checagens PASS (filtro, modal sem vídeo, foco, menu, sem barra fixa, CTA). Página de teste removida.
Ruling: espaçamento vertical das seções reduzido (44/60 px) para casar com o design — custo: ajuste fino futuro.
Task 6: revisão independente (agente opus, contexto novo) — 0 críticos, 3 importantes, 10 menores; veredito: pronto como prévia interna.
Final: fixed links do rodapé mobile 19px→44px — T1 RED→GREEN
Final: fixed conteúdo invisível se main.js falhar (failsafe 4s + window.__vc) — página sem main.js RED→GREEN
Final: fixed checagem de vídeo por HEAD (quebrava em file:// e 405) → evento error do <video> — T3b RED→GREEN
Final: fixed corrida: 'close' atrasado limpava modal reaberto (guard dlg.open) — T4d
Final: fixed aria-labelledby no diálogo + role=status em "Vídeo em breve" — T2 RED→GREEN
Final: Ruling: og:image relativo/og:url/canonical ficam para quando houver domínio — impossível sem domínio; listado em TEXTOS-DE-EXEMPLO — custo: cartão de compartilhamento sem imagem se publicar sem trocar
Final: Ruling: autorizações de mídia/depoimentos e aviso de prévia seguem pendentes — decisão do usuário/clientes, não do código — custo: risco de uso indevido se publicar sem autorização
Final: minor (deferred): sem JS o menu mobile não abre | "Ceará" sem marcação (documentado) | nome acessível longo dos reels | #filtro-vazio não é live region | legenda "Todos os Reels em 9:16" ausente no mobile | botão do CTA desktop diz "Orçamento no WhatsApp" (design: "Pedir orçamento") | chips quebram em 2 linhas no mobile (design: linha rolável) | "·" no início das linhas da faixa de marcas | tablet 768: retratos grandes e última linha da grade com buraco | chips 40px (briefing pedia 44) | borda dos chips com contraste 1,38:1
