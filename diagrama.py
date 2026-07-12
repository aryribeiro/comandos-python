"""Diagrama "De onde o Python tira isso?" — a resolução de nomes.

O aluno acha que `len(x)` e `x.append(1)` são a mesma coisa. Não são:
`len` é um NOME, buscado na cadeia LEGB (e achado no Built-in). `append`
não está no LEGB de jeito nenhum — é ATRIBUTO do objeto. `for` não é nome
nem atributo: é SINTAXE, resolvida pelo parser antes de qualquer busca.
E `math.sqrt` só existe depois que o import põe `math` no Global.

Este módulo desenha, para cada comando, por qual dos quatro caminhos o
Python chega até ele.
"""

from html import escape

# tipo do CSV -> caminho de resolução
SINTAXE = "sintaxe"
BUILTIN = "builtin"
ATRIBUTO = "atributo"
MODULO = "modulo"

CAMINHO_POR_TIPO = {
    "keyword": SINTAXE,
    "operator": SINTAXE,
    "builtin_function": BUILTIN,
    "list_method": ATRIBUTO,
    "str_method": ATRIBUTO,
    "dict_method": ATRIBUTO,
    "set_method": ATRIBUTO,
    "file_method": ATRIBUTO,
}

# tipo -> (nome do módulo, objeto de exemplo para o método)
MODULO_POR_TIPO = {
    "os_module": "os",
    "sys_module": "sys",
    "datetime_module": "datetime",
    "time_module": "time",
    "random_module": "random",
    "re_module": "re",
    "json_module": "json",
    "math_module": "math",
    "itertools_module": "itertools",
    "collections_module": "collections",
    "functools_module": "functools",
    "copy_module": "copy",
    "urllib_module": "urllib",
}

DONO_POR_TIPO = {
    "list_method": ("list", "[1, 2]"),
    "str_method": ("str", '"texto"'),
    "dict_method": ("dict", '{"a": 1}'),
    "set_method": ("set", "{1, 2}"),
    "file_method": ("arquivo", "open(...)"),
}

AZUL, CINZA, VERDE, ROXO = "#2a5298", "#9ca3af", "#10b981", "#7c3aed"


def caminho_de(tipo: str) -> str:
    return CAMINHO_POR_TIPO.get(tipo, MODULO if tipo in MODULO_POR_TIPO else BUILTIN)


def _camada(y, rotulo, achou, nota="", cor_achou=VERDE):
    """Uma faixa da pilha LEGB.

    A faixa mais longa ("G — Global (seu arquivo, imports)") transbordava do
    retângulo: fonte menor E retângulo mais largo, porque só encolher a fonte
    deixava o texto raspando na borda.
    """
    cor = cor_achou if achou else "#e5e7eb"
    txt = "#ffffff" if achou else "#6b7280"
    marca = "✓" if achou else "✗"
    return f"""
    <rect x="30" y="{y}" width="300" height="42" rx="8" fill="{cor}"/>
    <text x="48" y="{y + 27}" font-size="13.5" font-weight="600" fill="{txt}">{marca}  {escape(rotulo)}</text>
    <text x="345" y="{y + 26}" font-size="13" fill="#6b7280">{escape(nota)}</text>
    """


def _svg(corpo, altura=300):
    # Sem indentação: o Markdown do Streamlit transforma linha com 4+ espaços
    # em bloco de código e cospe o SVG como texto na tela. Some as quebras e
    # renderize com st.html(), que não passa pelo Markdown.
    corpo = "".join(linha.strip() for linha in corpo.splitlines())
    return (
        f'<svg viewBox="0 0 700 {altura}" width="100%" height="{altura}" '
        f'xmlns="http://www.w3.org/2000/svg" font-family="system-ui, sans-serif">{corpo}</svg>'
    )


def _titulo(texto):
    return f'<text x="30" y="24" font-size="14" font-weight="700" fill="#1e3c72">{escape(texto)}</text>'


def render(comando: str, tipo: str) -> tuple[str, str]:
    """Devolve (svg, explicacao) do caminho de resolução do comando."""
    cmd = escape(comando)
    caminho = caminho_de(tipo)

    # ---------- 1. SINTAXE: nem chega a ser um nome ----------
    if caminho == SINTAXE:
        eh_operador = tipo == "operator"
        o_que = "um operador" if eh_operador else "uma palavra-chave"
        extra = (
            f'<text x="30" y="196" font-size="13" fill="#6b7280">'
            f'O Python traduz para uma chamada de método especial no objeto:</text>'
            f'<text x="30" y="220" font-size="14" font-family="monospace" fill="{ROXO}">'
            f'a {cmd} b  →  a.__add__(b)  (o "dunder" do operador)</text>'
            if eh_operador else
            f'<text x="30" y="196" font-size="13" fill="#6b7280">'
            f'Por isso não dá para usar como variável:</text>'
            f'<text x="30" y="220" font-size="14" font-family="monospace" fill="#dc2626">'
            f'{cmd} = 5   →   SyntaxError</text>'
        )
        corpo = (
            _titulo(f"'{comando}' não é um nome — é sintaxe")
            + f"""
            <rect x="30" y="44" width="380" height="52" rx="8" fill="{ROXO}"/>
            <text x="50" y="76" font-size="16" font-weight="700" fill="#fff">✓  Parser (a gramática da linguagem)</text>
            <text x="430" y="74" font-size="13" fill="#6b7280">antes de qualquer busca</text>

            <rect x="30" y="112" width="380" height="44" rx="8" fill="#f3f4f6"/>
            <text x="50" y="140" font-size="14" fill="#9ca3af">✗  LEGB — nem é consultado</text>
            {extra}
            """
        )
        exp = (
            f"**`{comando}` é {o_que}: faz parte da gramática do Python.** "
            "Não é um nome guardado em lugar nenhum — o parser já entende ao ler o código, "
            "antes de procurar qualquer variável. Por isso você não pode reatribuir nem apagar."
        )
        return _svg(corpo, 250), exp

    # ---------- 2. BUILT-IN: nome achado no último degrau do LEGB ----------
    if caminho == BUILTIN:
        corpo = (
            _titulo(f"O Python procura o nome '{comando}' de dentro para fora (LEGB)")
            + _camada(44, "L — Local (dentro da função)", False, "não achou")
            + _camada(94, "E — Enclosing (função de fora)", False, "não achou")
            + _camada(144, "G — Global (seu arquivo, imports)", False, "não achou")
            + _camada(194, "B — Built-in (vem com o Python)", True, f"achou {comando}!")
            + f'<text x="30" y="268" font-size="13" fill="#6b7280">'
            f'Está no último degrau: por isso funciona sem import — e por isso </text>'
            + f'<text x="30" y="290" font-size="13" font-family="monospace" fill="#dc2626">'
            f'{cmd} = 10</text>'
            + f'<text x="{30 + 9 * len(comando) + 45}" y="290" font-size="13" fill="#6b7280">'
            f'ofusca o original no seu arquivo inteiro.</text>'
        )
        exp = (
            f"**`{comando}` é um nome, e mora no Built-in** — o último degrau da busca LEGB. "
            "O Python olha primeiro dentro da função (Local), depois na função que a envolve "
            "(Enclosing), depois no seu arquivo (Global) e só então no Built-in. "
            f"Como está no fim da fila, qualquer variável sua chamada `{comando}` **cobre a original**."
        )
        return _svg(corpo, 310), exp

    # ---------- 3. ATRIBUTO: não está no LEGB, está no objeto ----------
    if caminho == ATRIBUTO:
        dono, exemplo_obj = DONO_POR_TIPO.get(tipo, ("objeto", "obj"))
        corpo = (
            _titulo(f"'{comando}' NÃO é um nome solto — é atributo de um objeto")
            + f"""
            <rect x="30" y="46" width="380" height="46" rx="8" fill="#f3f4f6"/>
            <text x="48" y="75" font-size="13.5" fill="#9ca3af">✗  LEGB — {cmd} não está aqui</text>

            <rect x="30" y="112" width="180" height="56" rx="8" fill="{AZUL}"/>
            <text x="48" y="137" font-size="13" fill="#dbeafe">o objeto</text>
            <text x="48" y="157" font-size="14" font-family="monospace" fill="#fff">{escape(exemplo_obj)}</text>

            <path d="M 215 140 L 275 140" stroke="{VERDE}" stroke-width="2.5" fill="none"/>
            <path d="M 275 140 l -8 -5 l 0 10 z" fill="{VERDE}"/>
            <text x="218" y="131" font-size="12" font-family="monospace" fill="{VERDE}">.{cmd}</text>

            <rect x="282" y="112" width="220" height="56" rx="8" fill="{VERDE}"/>
            <text x="300" y="137" font-size="13" fill="#d1fae5">o tipo {escape(dono)}</text>
            <text x="300" y="157" font-size="14" font-weight="700" fill="#fff">✓ achou {cmd}</text>

            <text x="30" y="200" font-size="13" fill="#6b7280">É por isso que chamar sozinho não existe:</text>
            <text x="30" y="224" font-size="14" font-family="monospace" fill="#dc2626">{cmd}(...)   →   NameError</text>
            <text x="30" y="248" font-size="14" font-family="monospace" fill="{VERDE}">{escape(exemplo_obj)}.{cmd}(...)   →   funciona</text>
            """
        )
        exp = (
            f"**`{comando}` não vive no LEGB.** Ele é um atributo do tipo `{dono}`: o Python "
            f"só o encontra a partir de um objeto, com o ponto. Por isso `{comando}(...)` sozinho "
            f"dá **NameError**, enquanto `{exemplo_obj}.{comando}(...)` funciona. "
            "Essa é a diferença entre uma *função* e um *método* — e a fonte de metade da confusão de quem começa."
        )
        return _svg(corpo, 270), exp

    # ---------- 4. MÓDULO: o import põe o nome no Global ----------
    modulo = MODULO_POR_TIPO.get(tipo, "modulo")
    corpo = (
        _titulo(f"'{comando}' mora dentro do módulo {modulo} — o import é que o traz")
        + f"""
        <rect x="30" y="46" width="380" height="44" rx="8" fill="#f3f4f6"/>
        <text x="48" y="74" font-size="13.5" fill="#9ca3af">✗  Built-in — {cmd} não vem de graça</text>

        <text x="30" y="118" font-size="14" font-family="monospace" fill="{AZUL}">import {escape(modulo)}</text>
        <path d="M 150 113 L 205 113" stroke="{AZUL}" stroke-width="2.5" fill="none"/>
        <path d="M 205 113 l -8 -5 l 0 10 z" fill="{AZUL}"/>
        <text x="214" y="118" font-size="13" fill="#6b7280">põe o nome no Global</text>

        <rect x="30" y="136" width="190" height="56" rx="8" fill="{AZUL}"/>
        <text x="48" y="161" font-size="13" fill="#dbeafe">G — Global</text>
        <text x="48" y="181" font-size="14" font-weight="700" fill="#fff">✓ {escape(modulo)}</text>

        <path d="M 225 164 L 285 164" stroke="{VERDE}" stroke-width="2.5" fill="none"/>
        <path d="M 285 164 l -8 -5 l 0 10 z" fill="{VERDE}"/>
        <text x="228" y="155" font-size="12" font-family="monospace" fill="{VERDE}">.{cmd}</text>

        <rect x="292" y="136" width="230" height="56" rx="8" fill="{VERDE}"/>
        <text x="310" y="161" font-size="13" fill="#d1fae5">o módulo {escape(modulo)}</text>
        <text x="310" y="181" font-size="14" font-weight="700" fill="#fff">✓ achou {cmd}</text>

        <text x="30" y="226" font-size="13" fill="#6b7280">Sem o import, o nome não existe no seu arquivo:</text>
        <text x="30" y="250" font-size="14" font-family="monospace" fill="#dc2626">{escape(modulo)}.{cmd}(...)   →   NameError: name '{escape(modulo)}' is not defined</text>
        """
    )
    exp = (
        f"**`{comando}` vive dentro do módulo `{modulo}`.** O `import {modulo}` não *carrega a função*: "
        f"ele coloca o nome `{modulo}` no seu Global. A partir daí o ponto busca `{comando}` **dentro** "
        f"do módulo — dois passos, iguais aos de um método. Sem o import, nem o nome `{modulo}` existe."
    )
    return _svg(corpo, 270), exp
