# Textos e mídias provisórios (trocar antes de publicar)

## Textos fictícios (marcados com `<!-- EXEMPLO -->` no `index.html`)
- Serviços: as 3 linhas de detalhe (prazo de entrega, escopo, pacotes mensais).
- Sobre: "Mais de 6 anos criando conteúdo audiovisual. Formação em Comunicação Social e cursos de roteiro e edição."
- Etapas do processo: as 6 descrições curtas.
- Rodapé: e-mail `contato@viniciuscapture.com.br` e a cidade/estado "Ceará".
- Aviso "PRÉVIA INTERNA · textos de exemplo fictícios" (remover ao publicar).

## A confirmar com o Vinicius
- O WhatsApp (85) 99273-6085 é o número comercial?
- Quais clientes autorizam aparecer (nomes, capas, vídeos e logos)?
- Preços/pacotes, anos de experiência, formação e região atendida.

## Mídia
- As capas em `img/` são capturas de tela de baixa resolução (~540 px) de Reels do Instagram do Vinicius e de clientes, **sem autorização de uso**. São só para testar o layout.
- Os retratos vêm de posts do perfil (retrato do hero: fotografia de @samuelsanfotografo; direitos a confirmar).
- Substitua por arquivos originais mantendo os nomes (`img/<slug>.jpg`, `video/<slug>.mp4`).

## Depoimentos
- Os 3 textos da seção "O que dizem" são comentários públicos do Instagram (@mayborges16, @olicelmaoliveira.farma, @prof.robertalsousa). Peça autorização aos autores.

## Antes de publicar (pendências técnicas)
- Definir o domínio e então trocar `og:image` por URL absoluta (ex.: `https://SEU-DOMINIO/img/retrato-hero.jpg`) e acrescentar `og:url`, `<link rel="canonical">` e a `url` do JSON-LD. Sem isso o cartão de compartilhamento (WhatsApp/Facebook) sai sem imagem.
- "Ceará" aparece sem marcação no `<title>`, no texto do hero e no JSON-LD (`areaServed`), além do rodapé: confirmar a região atendida.
- Remover o aviso "PRÉVIA INTERNA" do rodapé e os comentários `<!-- EXEMPLO -->`.
- Substituir capas e retratos por arquivos originais autorizados (hoje são capturas de terceiros, sem autorização) e pedir autorização dos autores dos 3 comentários.
