"""Playground: Python de verdade rodando NO NAVEGADOR do aluno (Pyodide/WebAssembly).

Duas decisões que sustentam este arquivo:

1. O iframe é AUTOCONTIDO — o seletor de comando e todos os exemplos vivem
   dentro dele. O HTML entregue ao components.html nunca muda entre reruns,
   então o Streamlit não remonta o iframe e o Pyodide (~10 MB) não recarrega.
   Se o código dependesse de um widget do Streamlit, cada troca de comando
   torraria o interpretador inteiro de novo.

2. O Pyodide só é baixado no PRIMEIRO clique em Executar. Quem nunca abre o
   playground não paga nada.

Como tudo roda no navegador, não há execução de código no servidor.
"""

import json

PYODIDE = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js"


def construir_html(exemplos: list[dict]) -> str:
    """exemplos: [{'rotulo': 'print', 'codigo': '...'}, ...]"""
    dados = json.dumps(exemplos, ensure_ascii=False)

    return f"""
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; font-family: system-ui, sans-serif; color: #1f2937; }}
  .pg {{ border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px; background: #fff; }}
  .linha {{ display: flex; gap: 10px; align-items: center; margin-bottom: 12px; flex-wrap: wrap; }}
  select {{
    flex: 1; min-width: 180px; padding: 9px 12px; border: 1px solid #d1d5db;
    border-radius: 8px; font-size: 14px; background: #fff; color: #1f2937;
  }}
  button {{
    padding: 9px 18px; border: none; border-radius: 8px; background: #10b981;
    color: #fff; font-size: 14px; font-weight: 600; cursor: pointer; white-space: nowrap;
  }}
  button:hover:not(:disabled) {{ background: #059669; }}
  button:disabled {{ background: #9ca3af; cursor: wait; }}
  #reset {{ background: #6b7280; }}
  #reset:hover:not(:disabled) {{ background: #4b5563; }}
  textarea {{
    width: 100%; min-height: 190px; padding: 12px; border: 1px solid #d1d5db;
    border-radius: 8px; font-family: ui-monospace, "Cascadia Code", Consolas, monospace;
    font-size: 13.5px; line-height: 1.55; resize: vertical; color: #1f2937; background: #f9fafb;
  }}
  .rot {{ font-size: 12px; font-weight: 600; color: #6b7280; margin: 12px 0 6px; text-transform: uppercase; letter-spacing: .04em; }}
  pre {{
    margin: 0; padding: 12px; min-height: 76px; max-height: 240px; overflow: auto;
    background: #0f172a; color: #e2e8f0; border-radius: 8px;
    font-family: ui-monospace, Consolas, monospace; font-size: 13.5px;
    line-height: 1.55; white-space: pre-wrap; word-break: break-word;
  }}
  pre.erro {{ color: #fca5a5; }}
  .dica {{ font-size: 12.5px; color: #6b7280; margin-top: 10px; }}
</style>

<div class="pg">
  <div class="linha">
    <select id="sel"></select>
    <button id="run">▶ Executar</button>
    <button id="reset">↺ Restaurar</button>
  </div>

  <textarea id="cod" spellcheck="false"></textarea>

  <div class="rot">Saída</div>
  <pre id="out">Clique em ▶ Executar. Na primeira vez o Python leva alguns segundos para carregar no seu navegador — depois é instantâneo.</pre>

  <div class="dica">
    ✏️ O código é seu: edite, quebre, teste hipóteses. Roda no <strong>seu navegador</strong>
    (Pyodide/WebAssembly) — nada é enviado para servidor nenhum.
  </div>
</div>

<script src="{PYODIDE}"></script>
<script>
  const EXEMPLOS = {dados};
  const sel  = document.getElementById("sel");
  const cod  = document.getElementById("cod");
  const out  = document.getElementById("out");
  const run  = document.getElementById("run");
  const reset = document.getElementById("reset");

  EXEMPLOS.forEach((e, i) => {{
    const o = document.createElement("option");
    o.value = i;
    o.textContent = e.rotulo;
    sel.appendChild(o);
  }});

  const carregar = () => {{ cod.value = EXEMPLOS[sel.value].codigo; }};
  sel.addEventListener("change", carregar);
  reset.addEventListener("click", carregar);
  carregar();

  let pyodide = null;

  async function garantirPython() {{
    if (pyodide) return pyodide;
    out.className = "";
    out.textContent = "carregando o Python no navegador (só desta vez)...";
    pyodide = await loadPyodide();
    return pyodide;
  }}

  run.addEventListener("click", async () => {{
    run.disabled = true;
    const original = run.textContent;
    run.textContent = "executando...";
    try {{
      const py = await garantirPython();
      let buffer = "";
      py.setStdout({{ batched: (s) => {{ buffer += s + "\\n"; }} }});
      py.setStderr({{ batched: (s) => {{ buffer += s + "\\n"; }} }});
      await py.runPythonAsync(cod.value);
      out.className = "";
      out.textContent = buffer.trimEnd() || "(o código rodou, mas não imprimiu nada — use print())";
    }} catch (err) {{
      out.className = "erro";
      // a mensagem do Pyodide traz o traceback inteiro; a última linha é o que importa
      const linhas = String(err.message || err).trimEnd().split("\\n");
      out.textContent = linhas.slice(-12).join("\\n");
    }} finally {{
      run.disabled = false;
      run.textContent = original;
    }}
  }});
</script>
"""
