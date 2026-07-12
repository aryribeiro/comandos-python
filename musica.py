"""Trilha sonora de estudo.

Três restrições reais moldam este arquivo:

1. **O áudio precisa sobreviver aos reruns.** Um `st.audio` é re-renderizado a
   cada interação do Streamlit — trocar um filtro reiniciaria a música do zero.
   Por isso o player vive num components.html cujo HTML é uma CONSTANTE: o
   Streamlit não remonta o iframe, e a faixa continua tocando por cima de
   qualquer rerun.

2. **`play()` tem que ser chamado NO clique, sem await antes.** O navegador só
   libera áudio dentro de uma janela curta de *user activation* (~5s) após o
   gesto. A primeira versão daqui fazia `await fetch(8 MB)` e só então chamava
   `play()`: em localhost o download era instantâneo e passava, mas em produção
   a janela expirava no meio do download e o play era bloqueado — o usuário via
   "não foi possível tocar". Agora o play é síncrono e o navegador TRANSMITE o
   arquivo progressivamente, em vez de baixá-lo inteiro antes de começar.

3. **O Streamlit serve .mp3 como text/plain.** A allowlist do
   `AppStaticFileHandler` só cobre imagem, fonte, pdf, xml e json; o resto sai
   como texto puro com `nosniff`. O Chrome ainda assim toca (sniffa o container
   de mídia), então o caminho normal é o `src` direto. Se algum navegador
   recusar o formato, o `catch` cai para um fallback que busca os bytes e monta
   um Blob `audio/mpeg` — aí o tipo é declarado por nós e não há o que adivinhar.

Nada de autoplay: além de ser bloqueado sem gesto, ninguém merece um susto
sonoro ao abrir o app.
"""

FAIXA = "/app/static/som.mp3"

HTML = f"""
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; font-family: system-ui, sans-serif; }}
  .player {{
    display: flex; align-items: center; gap: 10px;
    padding: 10px 12px; border: 1px solid #e5e7eb;
    border-radius: 10px; background: #f8fafc;
  }}
  #tocar {{
    width: 38px; height: 38px; flex: 0 0 38px; padding: 0;
    border: none; border-radius: 50%; background: #2a5298; color: #fff;
    font-size: 15px; cursor: pointer; line-height: 1;
  }}
  #tocar:hover {{ background: #1e3c72; }}
  #tocar.tocando {{ background: #10b981; }}
  .col {{ flex: 1; min-width: 0; }}
  #rotulo {{
    font-size: 12px; color: #6b7280; font-weight: 600;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }}
  input[type=range] {{ width: 100%; accent-color: #2a5298; height: 16px; }}
</style>

<div class="player">
  <button id="tocar" title="Tocar a trilha de estudo">&#9654;</button>
  <div class="col">
    <div id="rotulo">Trilha de estudo</div>
    <input type="range" id="vol" min="0" max="100" value="35" title="Volume">
  </div>
</div>

<!-- preload="none": quem nunca aperta o play não baixa nada. -->
<audio id="audio" loop preload="none" src="{FAIXA}"></audio>

<script>
  const audio  = document.getElementById("audio");
  const botao  = document.getElementById("tocar");
  const vol    = document.getElementById("vol");
  const rotulo = document.getElementById("rotulo");

  audio.volume = vol.value / 100;
  vol.addEventListener("input", () => {{ audio.volume = vol.value / 100; }});

  let tentouBlob = false;

  function tocando() {{
    botao.innerHTML = "&#10074;&#10074;";
    botao.classList.add("tocando");
    rotulo.textContent = "tocando...";
  }}

  function parado(msg) {{
    botao.innerHTML = "&#9654;";
    botao.classList.remove("tocando");
    rotulo.textContent = msg || "Trilha de estudo";
  }}

  async function viaBlob() {{
    // Só se o navegador recusar o text/plain que o Streamlit devolve:
    // buscamos os bytes e declaramos audio/mpeg por conta própria.
    const r = await fetch("{FAIXA}");
    if (!r.ok) throw new Error(r.status);
    const blob = new Blob([await r.arrayBuffer()], {{ type: "audio/mpeg" }});
    audio.src = URL.createObjectURL(blob);
  }}

  botao.addEventListener("click", () => {{
    if (!audio.paused) {{
      audio.pause();
      parado();
      return;
    }}

    rotulo.textContent = "iniciando...";

    // SEM await aqui: o play precisa sair no mesmo tique do clique, senão a
    // permissão de áudio do navegador expira e ele bloqueia.
    audio.play().then(tocando).catch(async (erro) => {{
      if (tentouBlob) {{
        parado("não foi possível tocar");
        return;
      }}
      tentouBlob = true;

      // Formato recusado: refaz a faixa como Blob e tenta de novo.
      rotulo.textContent = "preparando a trilha...";
      try {{
        await viaBlob();
      }} catch (e) {{
        parado("trilha indisponível");
        return;
      }}
      // Esta segunda tentativa pode cair fora da janela de permissão —
      // se cair, pedimos o clique de novo em vez de fingir que deu certo.
      audio.play().then(tocando).catch(() => parado("toque no play novamente"));
    }});
  }});
</script>
"""
