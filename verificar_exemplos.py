"""Guarda de regressão do conteúdo: executa todo exemplo do CSV e confere a saída.

A promessa do app é que a saída mostrada ao aluno é a saída REAL do Python —
nunca um texto escrito à mão. Este script é o que sustenta essa promessa: ele
roda cada exemplo num subprocesso isolado e compara o stdout com a coluna
`saida` do comandos.csv.

    python verificar_exemplos.py

Sai com código 1 se algum exemplo quebrar ou divergir. Rode depois de mexer
no CSV: uma saída que não bate significa que a documentação está mentindo.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

CSV = Path(__file__).parent / "comandos.csv"
TIMEOUT = 20


def executar(codigo: str) -> tuple[bool, str]:
    # Diretório temporário: os exemplos de arquivo (open/write) escrevem em disco.
    with tempfile.TemporaryDirectory() as tmp:
        script = Path(tmp) / "exemplo.py"
        script.write_text(codigo, encoding="utf-8")
        try:
            p = subprocess.run(
                [sys.executable, str(script)],
                capture_output=True, text=True, encoding="utf-8",
                cwd=tmp, timeout=TIMEOUT,
            )
        except subprocess.TimeoutExpired:
            return False, f"TIMEOUT: não terminou em {TIMEOUT}s"
    if p.returncode != 0:
        erro = (p.stderr or "").strip().splitlines()
        return False, erro[-1] if erro else "erro sem mensagem"
    return True, (p.stdout or "").rstrip("\n")


def main() -> int:
    df = pd.read_csv(CSV, keep_default_na=False, dtype=str)
    alvos = df[(df["exemplo"] != "") & (df["executavel"] == "1")]

    quebrados, divergentes, ok = [], [], 0

    for _, linha in alvos.iterrows():
        nome = f"{linha['comando']} ({linha['tipo']})"
        rodou, saida = executar(linha["exemplo"])
        if not rodou:
            quebrados.append((nome, saida))
        elif saida.strip() != linha["saida"].strip():
            divergentes.append((nome, linha["saida"], saida))
        else:
            ok += 1

    print(f"exemplos conferidos : {len(alvos)}")
    print(f"saída bate          : {ok}")
    print(f"quebrados           : {len(quebrados)}")
    print(f"saída divergente    : {len(divergentes)}")

    for nome, erro in quebrados:
        print(f"\n[QUEBROU] {nome}\n  {erro}")
    for nome, gravada, real in divergentes:
        print(f"\n[DIVERGIU] {nome}")
        print(f"  no CSV : {gravada!r}")
        print(f"  real   : {real!r}")

    if quebrados or divergentes:
        print("\nO CSV está mentindo para o aluno. Corrija antes de publicar.")
        return 1

    print("\nTodo exemplo roda e a saída publicada é a saída real.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
