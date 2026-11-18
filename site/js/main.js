(() => {
  'use strict';

  // Carregamento inicial: aos 900ms o overlay sobe; aos 1900ms é removido. Sem animação com movimento reduzido.
  function initPreloader() {
    const el = document.getElementById('preloader');
    const html = document.documentElement;
    const fim = () => { if (el) el.remove(); html.classList.remove('carregando'); };
    if (!el) { html.classList.remove('carregando'); return; }
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches || /[?&]all\b/.test(location.search)) { fim(); return; }
    setTimeout(() => { el.classList.add('is-leaving'); html.classList.remove('carregando'); }, 900);
    setTimeout(fim, 1900);
  }

  // Menu mobile: abre/fecha, fecha ao tocar num link e com Esc
  function initMenu() {
    const burger = document.querySelector('.burger');
    const menu = document.getElementById('menu');
    if (!burger || !menu) return;
    const set = (aberto) => {
      burger.setAttribute('aria-expanded', String(aberto));
      burger.setAttribute('aria-label', aberto ? 'Fechar menu' : 'Abrir menu');
      menu.classList.toggle('is-open', aberto);
    };
    burger.addEventListener('click', () => set(burger.getAttribute('aria-expanded') !== 'true'));
    menu.addEventListener('click', (e) => { if (e.target.closest('a')) set(false); });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && burger.getAttribute('aria-expanded') === 'true') { set(false); burger.focus(); }
    });
    window.matchMedia('(min-width: 900px)').addEventListener('change', (e) => { if (e.matches) set(false); });
  }

  // Filtro do portfólio por categoria
  function initFilter() {
    const chips = [...document.querySelectorAll('.chip')];
    const reels = [...document.querySelectorAll('.reel')];
    const vazio = document.getElementById('filtro-vazio');
    chips.forEach((chip) => chip.addEventListener('click', () => {
      const f = chip.dataset.filter;
      chips.forEach((c) => {
        const on = c === chip;
        c.classList.toggle('is-on', on);
        c.setAttribute('aria-pressed', String(on));
      });
      let visiveis = 0;
      reels.forEach((r) => {
        const mostra = f === 'todos' || r.dataset.category === f;
        r.hidden = !mostra;
        if (mostra) visiveis += 1;
      });
      if (vazio) vazio.hidden = visiveis > 0;
    }));
  }

  // Modal de vídeo: toca video/<slug>.mp4 se existir; senão "Vídeo em breve"
  function initModal() {
    const dlg = document.getElementById('player');
    const area = document.getElementById('player-area');
    const titulo = document.getElementById('player-titulo');
    if (!dlg || !area || typeof dlg.showModal !== 'function') return;
    let origem = null;

    // limpeza idempotente: roda ao fechar por botão/fundo e também no evento 'close' (cobre o Esc).
    // Se o diálogo já foi reaberto, um 'close' atrasado não pode apagar o novo conteúdo.
    const limpar = () => {
      if (dlg.open) return;
      const v = area.querySelector('video');
      if (v) v.pause();
      area.replaceChildren();
      document.body.classList.remove('sem-scroll');
      if (origem) origem.focus();
    };
    const fechar = () => { if (dlg.open) dlg.close(); limpar(); };
    dlg.addEventListener('close', limpar);
    dlg.querySelector('.player__fechar').addEventListener('click', fechar);
    dlg.addEventListener('click', (e) => { if (e.target === dlg) fechar(); });

    // "Vídeo em breve": usado quando o arquivo não existe ou não pode ser reproduzido
    const mostrarBreve = () => {
      const p = document.createElement('p');
      p.className = 'player__breve';
      p.setAttribute('role', 'status');
      p.textContent = 'Vídeo em breve';
      area.replaceChildren(p);
    };

    document.querySelectorAll('.reel').forEach((card) => card.addEventListener('click', () => {
      origem = card;
      titulo.textContent = card.dataset.title || '';
      // tenta o vídeo direto; qualquer falha (404, 405, file://, HTML no lugar do mp4) cai em "em breve"
      const v = document.createElement('video');
      v.controls = true; v.playsInline = true; v.preload = 'metadata';
      v.addEventListener('error', mostrarBreve, { once: true });
      v.src = `video/${card.dataset.slug}.mp4`;
      area.replaceChildren(v);
      document.body.classList.add('sem-scroll');
      dlg.showModal();
      v.play().catch(() => {});
    }));
  }

  // Letreiro de marcas: repete a lista até cobrir a tela (senão o laço mostra vazio em telas largas).
  // Com movimento reduzido a lista fica estática e não é repetida.
  function initMarquee() {
    const faixa = document.querySelector('.marcas__faixa');
    if (!faixa) return;
    const [base, copia] = faixa.querySelectorAll('.marcas__lista');
    if (!base || !copia) return;
    const nomes = [...base.children].map((li) => li.textContent);
    const reduzido = window.matchMedia('(prefers-reduced-motion: reduce)');
    const montar = () => {
      base.replaceChildren(); copia.replaceChildren();
      const mk = () => nomes.map((n) => { const li = document.createElement('li'); li.textContent = n; return li; });
      base.append(...mk());
      let k = 1;
      if (!reduzido.matches) {
        const w = base.getBoundingClientRect().width || 1;
        k = Math.max(1, Math.ceil(window.innerWidth / w));
        for (let i = 1; i < k; i++) base.append(...mk());
      }
      copia.append(...[...base.children].map((li) => li.cloneNode(true)));
      // velocidade constante em px/s (mais calma no celular), qualquer que seja a largura da lista
      const vel = window.innerWidth < 900 ? 38 : 50;
      faixa.style.animationDuration = reduzido.matches ? '' : `${(base.getBoundingClientRect().width / vel).toFixed(2)}s`;
    };
    montar();
    let t;
    window.addEventListener('resize', () => { clearTimeout(t); t = setTimeout(montar, 200); });
    reduzido.addEventListener('change', montar);
  }

  // Entrada sutil (respeita prefers-reduced-motion via CSS)
  function initReveal() {
    const els = document.querySelectorAll('.reveal');
    // gancho de teste: ?all revela tudo e carrega as imagens (capturas automatizadas)
    if (/[?&]all\b/.test(location.search)) {
      els.forEach((e) => e.classList.add('is-in'));
      document.querySelectorAll('img[loading="lazy"]').forEach((i) => { i.loading = 'eager'; });
      return;
    }
    if (!('IntersectionObserver' in window)) { els.forEach((e) => e.classList.add('is-in')); return; }
    const io = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
    }), { threshold: 0.12 });
    els.forEach((e) => io.observe(e));
  }

  initPreloader();
  initMenu();
  initFilter();
  initModal();
  initReveal();
  initMarquee();
  window.__vc = true; // sinaliza ao head que o JS carregou (senão o conteúdo oculto por .js é revelado)
})();
