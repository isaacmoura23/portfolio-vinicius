// Verificador do site (sem dependências): node tools/check-site.mjs
import { existsSync, readFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..', 'site');
const file = join(root, 'index.html');
const erros = [];
const falha = (m) => erros.push(m);

if (!existsSync(file)) {
  console.error('FALHA: site/index.html não existe');
  process.exit(1);
}
const html = readFileSync(file, 'utf8');
const css = existsSync(join(root, 'css/styles.css')) ? readFileSync(join(root, 'css/styles.css'), 'utf8') : '';

// 1. recursos locais existem
const refs = [...html.matchAll(/\b(?:src|href|poster)="([^"#?]+)(?:[?#][^"]*)?"/g)].map((m) => m[1]);
for (const r of refs) {
  if (/^(https?:|mailto:|tel:|data:|#)/.test(r)) continue;
  if (!existsSync(join(root, r))) falha(`recurso local ausente: ${r}`);
}
// 2. imagens: alt e loading (exceto a primeira, do hero)
const imgs = [...html.matchAll(/<img\b[^>]*>/g)].map((m) => m[0]);
imgs.forEach((tag) => {
  const decorativa = /\balt=""/.test(tag); // ex.: logo do carregamento (aria-hidden)
  if (!decorativa && !/\balt="[^"]+"/.test(tag)) falha(`img sem alt: ${tag.slice(0, 70)}`);
  const prioritaria = /fetchpriority="high"/.test(tag) || decorativa; // hero e logo do preloader não são lazy
  if (!prioritaria && !/\bloading="lazy"/.test(tag)) falha(`img sem loading=lazy: ${tag.slice(0, 70)}`);
});
if (!html.includes('id="preloader"')) falha('carregamento inicial (#preloader) ausente');
// 3. um único h1
const h1 = (html.match(/<h1\b/g) || []).length;
if (h1 !== 1) falha(`esperado 1 <h1>, achei ${h1}`);
// 4. contato, pendências e SEO
if (!html.includes('wa.me/5585992736085')) falha('link do WhatsApp ausente');
if (/\[confirmar/i.test(html)) falha('sobrou "[confirmar" no HTML');
for (const [nome, re] of [['viewport', /<meta name="viewport"/], ['og:title', /property="og:title"/], ['ld+json', /application\/ld\+json/], ['meta description', /<meta name="description"/]])
  if (!re.test(html)) falha(`faltando: ${nome}`);
// 5. rodapé mobile definido pelo usuário: sem barra fixa
if (/position:\s*fixed/.test(css) && /barra-fixa|sticky-cta/.test(html + css)) falha('barra fixa de WhatsApp não deve existir');
// 6. modal/filtro presentes
for (const id of ['filtro-vazio', 'player']) if (!html.includes(`id="${id}"`)) falha(`id ausente: ${id}`);
if ((html.match(/class="reel"/g) || []).length !== 8) falha('esperado 8 reels');

if (erros.length) {
  console.error('FALHAS:\n - ' + erros.join('\n - '));
  process.exit(1);
}
console.log(`OK · ${imgs.length} imagens, ${refs.length} referências verificadas`);
