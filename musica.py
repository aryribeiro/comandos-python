"""Trilha sonora de estudo.

Duas restrições reais moldam este arquivo:

1. **O áudio precisa sobreviver aos reruns.** Um `st.audio` é re-renderizado a
   cada interação do Streamlit — trocar um filtro reiniciaria a música do zero.
   Por isso o player vive num components.html cujo HTML é uma CONSTANTE: o
   Streamlit não remonta o iframe, e a faixa continua tocando por cima de
   qualquer rerun.

2. **Nenhum navegador toca áudio sozinho.** A política de autoplay bloqueia som
   sem um gesto do usuário; um `autoplay` no <audio> seria silenciosamente
   ignorado. Então há um botão de play explícito — que é também a saída elegante:
   ninguém leva um susto sonoro ao abrir o app.

E uma armadilha do próprio Streamlit: o `AppStaticFileHandler` só devolve o
Content-Type correto para uma allowlist de extensões (imagem, fonte, pdf, xml,
json). **`.mp3` não está nela**: o arquivo sai como `text/plain` + `nosniff`.
O Chrome ainda assim toca (sniffa o conteúdo de mídia), mas apostar nisso em
todo navegador seria irresponsável. Por isso o áudio não vem de um `src`: o JS
faz `fetch` dos bytes e monta um Blob declarando `audio/mpeg` por conta própria
— o fetch ignora o Content-Type do servidor, e o Blob nasce com o tipo certo.

Continua preguiçoso: os ~8 MB só são baixados quando alguém aperta o play.
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

<audio id="audio" loop></audio>

<script>
  const audio  = document.getElementById("audio");
  const botao  = document.getElementById("tocar");
  const vol    = document.getElementById("vol");
  const rotulo = document.getElementById("rotulo");

  audio.volume = vol.value / 100;
  vol.addEventListener("input", () => {{ audio.volume = vol.value / 100; }});

  let pronto = false;

  async function prepararFaixa() {{
    // O Streamlit serve .mp3 como text/plain (extensão fora da allowlist dele).
    // Buscar os bytes e montar o Blob com o tipo certo evita depender de o
    // navegador "adivinhar" o formato — o fetch ignora o Content-Type.
    if (pronto) return true;
    rotulo.textContent = "carregando a trilha...";
    try {{
      const r = await fetch("{FAIXA}");
      if (!r.ok) throw new Error(r.status);
      const blob = new Blob([await r.arrayBuffer()], {{ type: "audio/mpeg" }});
      audio.src = URL.createObjectURL(blob);
      pronto = true;
      return true;
    }} catch (e) {{
      rotulo.textContent = "trilha indisponível";
      return false;
    }}
  }}

  botao.addEventListener("click", async () => {{
    if (!audio.paused) {{
      audio.pause();
      botao.innerHTML = "&#9654;";
      botao.classList.remove("tocando");
      rotulo.textContent = "Trilha de estudo";
      return;
    }}

    botao.disabled = true;
    const ok = await prepararFaixa();
    botao.disabled = false;
    if (!ok) return;

    try {{
      await audio.play();          // só é permitido por vir de um clique
    }} catch (e) {{
      rotulo.textContent = "não foi possível tocar";
      return;
    }}
    botao.innerHTML = "&#10074;&#10074;";
    botao.classList.add("tocando");
    rotulo.textContent = "tocando...";
  }});
</script>
"""
