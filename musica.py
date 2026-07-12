"""Trilha sonora de estudo.

O caminho aqui foi decidido por um case que já funciona em produção: o
**aws-game**, que toca vários mp3 no Streamlit Cloud. Ele embute o áudio como
**data URI em base64** dentro do components.html:

    new Audio('data:audio/mp3;base64,' + dados)

Eu havia inventado uma alternativa — servir o mp3 de `/app/static/` com
`enableStaticServing` — e ela **não funciona no Cloud**: a rota devolve um 303
para o portão de autenticação (`share.streamlit.io/-/auth/app`), então o
navegador recebe HTML de redirect em vez de áudio. Some-se a isso que o
`AppStaticFileHandler` nem serve .mp3 com o Content-Type correto (a allowlist
dele só cobre imagem, fonte, pdf, xml e json).

O base64 resolve os dois problemas de uma vez e ainda mata um terceiro: como o
áudio já está na memória quando o aluno clica, **não há download durante o
clique** — logo não há risco de a janela de *user activation* do navegador
expirar e o play ser bloqueado (era esse o bug do "não foi possível tocar").

Preço: o base64 infla ~37%. Por isso o som.mp3 foi reencodado para 96 kbps mono
sem capa embutida — 4,0 MB em vez de 7,8 MB (os 5min52s originais estão
inteiros). Música de fundo a 35% de volume não precisa de 185 kbps estéreo.

E o player vive num components.html de HTML **constante**: assim o Streamlit não
remonta o iframe a cada rerun, e a faixa não reinicia quando o aluno mexe num
filtro.
"""

import json


def construir_html(audio_base64: str) -> str:
    # json.dumps escapa a string do base64 com segurança dentro do JS.
    dados = json.dumps(f"data:audio/mp3;base64,{audio_base64}")

    return f"""
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

<script>
  // Igual ao aws-game: o audio nasce de um data URI, sem depender de rota
  // nenhuma do servidor e sem baixar nada na hora do clique.
  const audio  = new Audio({dados});
  audio.loop = true;

  const botao  = document.getElementById("tocar");
  const vol    = document.getElementById("vol");
  const rotulo = document.getElementById("rotulo");

  audio.volume = vol.value / 100;
  vol.addEventListener("input", () => {{ audio.volume = vol.value / 100; }});

  botao.addEventListener("click", () => {{
    if (!audio.paused) {{
      audio.pause();
      botao.innerHTML = "&#9654;";
      botao.classList.remove("tocando");
      rotulo.textContent = "Trilha de estudo";
      return;
    }}

    // Sem await antes do play: ele precisa sair no mesmo tique do clique,
    // senão o navegador bloqueia o áudio por falta de gesto do usuário.
    audio.play().then(() => {{
      botao.innerHTML = "&#10074;&#10074;";
      botao.classList.add("tocando");
      rotulo.textContent = "tocando...";
    }}).catch(() => {{
      rotulo.textContent = "não foi possível tocar";
    }});
  }});
</script>
"""
