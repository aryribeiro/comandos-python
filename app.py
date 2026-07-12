from base64 import b64encode
from html import escape
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

import diagrama
import musica
import playground

RAIZ = Path(__file__).parent
CSV_PATH = RAIZ / "comandos.csv"
LOGO_PATH = RAIZ / "logo.png"
COLUNAS_OBRIGATORIAS = ["comando", "tipo", "categoria", "descricao"]
COMANDOS_POR_PAGINA = 25

st.set_page_config(
    page_title="Comandos Python | por Ary Ribeiro",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    /* Esconde o chrome padrão do Streamlit, mas mantém o <header> no DOM
       para preservar a seta de abrir/fechar o sidebar */
    header[data-testid="stHeader"] {
        background: transparent !important;
        box-shadow: none !important;
    }
    /* Esconde só os itens à direita do toolbar (menu, Deploy, status).
       NÃO esconder o stToolbar inteiro: é dentro dele que o Streamlit
       renderiza a seta de expandir a sidebar (stExpandSidebarButton). */
    [data-testid="stToolbarActions"],
    [data-testid="stAppDeployButton"],
    [data-testid="stMainMenu"],
    [data-testid="stStatusWidget"],
    [data-testid="stDecoration"] {
        display: none !important;
    }
    footer {display: none !important;}
    #MainMenu {display: none !important;}

    .block-container {padding-top: 1rem;}

    .app-header {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    .app-logo {width: 400px; max-width: 90%; height: auto;}
    .app-slogan {
        font-size: 1.2rem;
        color: #6b7280;
        font-weight: 500;
        margin: 1rem 0 2rem 0;
    }

    .stats-container {
        display: flex;
        justify-content: space-around;
        background: #f8fafc;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .stat-item {text-align: center;}
    .stat-number {font-size: 2rem; font-weight: bold; color: #1e3c72;}
    .stat-label {color: #6b7280; font-size: 0.9rem;}

    .command-type, .command-category, .command-nivel {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-right: 0.5rem;
    }
    .command-type {background: #e8f4fd; color: #2a5298;}
    .command-category {background: #f0f9ff; color: #1e40af;}
    .nivel-iniciante {background: #dcfce7; color: #166534;}
    .nivel-intermediario {background: #fef3c7; color: #92400e;}
    .nivel-avancado {background: #fee2e2; color: #991b1b;}

    .command-description {
        color: #4b5563;
        font-size: 1rem;
        margin-top: 0.6rem;
        line-height: 1.5;
    }

    /* A armadilha é o coração pedagógico: precisa saltar aos olhos. */
    .armadilha {
        background: #fff7ed;
        border-left: 5px solid #ea580c;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0 1.2rem 0;
        color: #7c2d12;
        line-height: 1.6;
    }
    .armadilha-titulo {
        font-weight: 700;
        color: #c2410c;
        display: block;
        margin-bottom: 0.3rem;
    }

    .diagrama-box {
        background: #fbfcfe;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 0.5rem 0.8rem;
        margin-bottom: 0.8rem;
    }
    .diagrama-box img {width: 100%; height: auto; display: block;}

    .sidebar-header {
        color: #1e3c72;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 1rem;
    }
    .no-results {text-align: center; padding: 3rem; color: #6b7280;}
    .search-info {
        background: #fef3c7;
        border: 1px solid #f59e0b;
        border-radius: 5px;
        padding: 0.8rem;
        margin-bottom: 1rem;
        color: #92400e;
    }
    .app-footer {
        text-align: center;
        color: #6b7280;
        font-size: 0.9rem;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid #e5e7eb;
    }
    .app-footer a {color: #2a5298; text-decoration: none;}
</style>
""",
    unsafe_allow_html=True,
)

CATEGORIAS = {
    "matematica": "🔢 Matemática", "string": "📝 Strings", "lista": "📋 Listas",
    "dicionario": "📚 Dicionários", "conjunto": "🔗 Conjuntos", "arquivo": "📁 Arquivos",
    "sistema": "⚙️ Sistema", "io": "💻 Entrada/Saída", "tempo": "⏰ Data/Tempo",
    "aleatorio": "🎲 Aleatório", "regex": "🔍 Regex", "json": "📊 JSON",
    "iteracao": "🔄 Iteração", "estrutura_dados": "🏗️ Estruturas de Dados",
    "funcional": "⚡ Programação Funcional", "objeto": "🎯 Objetos", "web": "🌐 Web/URLs",
    "controle": "🎛️ Controle de Fluxo", "funcao": "🔧 Funções",
    "orientacao_objeto": "🏛️ Orientação a Objetos", "excecao": "⚠️ Exceções",
    "import": "📦 Imports", "escopo": "🔐 Escopo", "debug": "🐛 Debug",
    "assincrono": "⚡ Assíncrono", "conversao": "🔄 Conversão", "sequencia": "📊 Sequências",
    "inspecao": "🔍 Inspeção", "memoria": "💾 Memória", "utilitario": "🛠️ Utilitários",
    "contexto": "📋 Context Managers", "gerador": "⚙️ Geradores", "constante": "📏 Constantes",
    "logica": "🧠 Lógica", "operador_logico": "🧮 Operadores Lógicos", "operador": "➕ Operadores",
    "aritmetico": "🔢 Aritmética", "comparacao": "⚖️ Comparação", "atribuicao": "📝 Atribuição",
    "bitwise": "🔀 Bitwise",
}

TIPOS = {
    "keyword": "🔑 Palavra-chave", "builtin_function": "⚡ Função Built-in",
    "list_method": "📋 Método de Lista", "str_method": "📝 Método de String",
    "dict_method": "📚 Método de Dicionário", "set_method": "🔗 Método de Conjunto",
    "file_method": "📁 Método de Arquivo", "operator": "➕ Operador",
    "os_module": "🖥️ Módulo OS", "sys_module": "⚙️ Módulo Sys",
    "datetime_module": "📅 Módulo DateTime", "time_module": "⏱️ Módulo Time",
    "random_module": "🎲 Módulo Random", "re_module": "🔍 Módulo RE",
    "json_module": "📊 Módulo JSON", "math_module": "🔢 Módulo Math",
    "itertools_module": "🔄 Módulo Itertools", "collections_module": "🏗️ Módulo Collections",
    "functools_module": "⚡ Módulo Functools", "copy_module": "📋 Módulo Copy",
    "urllib_module": "🌐 Módulo Urllib",
}

# Prefixo do módulo, para desambiguar homônimos: itertools.count vs count (list),
# re.compile vs compile (built-in), time.time vs datetime.time...
PREFIXOS = {
    "os_module": "os", "sys_module": "sys", "datetime_module": "datetime",
    "time_module": "time", "random_module": "random", "re_module": "re",
    "json_module": "json", "math_module": "math", "itertools_module": "itertools",
    "collections_module": "collections", "functools_module": "functools",
    "copy_module": "copy", "urllib_module": "urllib",
}

TRILHAS = {
    "primeiros_passos": "🌱 Primeiros passos",
    "fluxo": "🎛️ Decisão e repetição",
    "colecoes": "📦 Listas, dicionários e conjuntos",
    "texto": "📝 Trabalhando com texto",
    "funcoes": "🔧 Funções",
    "erros": "⚠️ Erros e exceções",
    "arquivos": "📁 Arquivos",
    "objetos": "🏛️ Objetos e memória",
    "escopo": "🔐 Escopo",
    "ferramentas": "🛠️ Ferramentas do dia a dia",
}

NIVEIS = {"iniciante": "🟢 Iniciante", "intermediario": "🟡 Intermediário", "avancado": "🔴 Avançado"}

MODO_CATALOGO = "📖 Catálogo"
MODO_ESTUDAR = "🎓 Estudar"
MODO_PLAYGROUND = "▶️ Playground"


def rotulo_categoria(categoria: str) -> str:
    return CATEGORIAS.get(categoria, categoria.replace("_", " ").title())


def rotulo_tipo(tipo: str) -> str:
    return TIPOS.get(tipo, tipo.replace("_", " ").title())


def nome_qualificado(comando: str, tipo: str) -> str:
    """`compile` do módulo re vira `re.compile` — sem isso, homônimos viram cards idênticos."""
    prefixo = PREFIXOS.get(tipo)
    return f"{prefixo}.{comando}" if prefixo else comando


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    # keep_default_na=False: sem isso o pandas converte o comando `None` em NaN
    # e ele some da base (`None` está na lista de na_values padrão).
    df = pd.read_csv(CSV_PATH, keep_default_na=False, dtype=str)

    faltando = [c for c in COLUNAS_OBRIGATORIAS if c not in df.columns]
    if faltando:
        raise ValueError(f"Colunas ausentes no CSV: {', '.join(faltando)}")

    for coluna in ("nivel", "importancia", "sintaxe", "exemplo", "saida",
                   "armadilha", "veja_tambem", "trilha", "executavel"):
        if coluna not in df.columns:
            df[coluna] = ""

    for coluna in df.columns:
        df[coluna] = df[coluna].str.strip()

    df = df[df["comando"] != ""].reset_index(drop=True)
    df["rotulo"] = [nome_qualificado(c, t) for c, t in zip(df["comando"], df["tipo"])]
    return df


@st.cache_data(show_spinner=False)
def logo_base64() -> str:
    return b64encode(LOGO_PATH.read_bytes()).decode()


@st.cache_data(show_spinner=False)
def html_playground(exemplos: list[dict]) -> str:
    return playground.construir_html(exemplos)


def render_cabecalho() -> None:
    # Logo e slogan no MESMO bloco centralizado. Com a logo em st.columns o
    # st.image encostava na borda esquerda da coluna, enquanto o slogan
    # centralizava na página: dois eixos diferentes, texto fora de prumo.
    if LOGO_PATH.exists():
        topo = f'<img class="app-logo" src="data:image/png;base64,{logo_base64()}" alt="Comandos Python">'
    else:
        topo = "<h1>🐍 Comandos Python</h1>"

    st.markdown(
        f"""
        <div class="app-header">
            {topo}
            <p class="app-slogan">Referência completa para alunos e iniciantes</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_estatisticas(df: pd.DataFrame) -> None:
    com_exemplo = int((df["exemplo"] != "").sum())
    st.markdown(
        f"""
        <div class="stats-container">
            <div class="stat-item">
                <div class="stat-number">{len(df)}</div>
                <div class="stat-label">Comandos</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{com_exemplo}</div>
                <div class="stat-label">Com exemplo executável</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{df['categoria'].nunique()}</div>
                <div class="stat-label">Categorias</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{df['tipo'].nunique()}</div>
                <div class="stat-label">Tipos</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar(df: pd.DataFrame) -> dict:
    with st.sidebar:
        st.markdown('<div class="sidebar-header">🐍 Comandos Python</div>', unsafe_allow_html=True)

        # Sempre no MESMO lugar, em todos os modos: se o player mudasse de posição
        # o Streamlit remontaria o iframe e a música cortaria no meio.
        components.html(musica.HTML, height=76)

        modo = st.radio(
            "Modo:",
            [MODO_CATALOGO, MODO_ESTUDAR, MODO_PLAYGROUND],
            key="modo",
            captions=[
                "buscar e filtrar os 363",
                "um comando por vez, a fundo",
                "rode Python no navegador",
            ],
        )

        st.markdown("---")

        if modo == MODO_PLAYGROUND:
            st.markdown("### ▶️ Playground")
            st.markdown(
                "O Python roda **dentro do seu navegador** (WebAssembly). "
                "Edite o código, quebre de propósito, veja o erro real. "
                "Nada é enviado para servidor nenhum."
            )
            return {"modo": modo}

        st.markdown('<div class="sidebar-header">🔍 Filtros e Busca</div>', unsafe_allow_html=True)

        busca = st.text_input(
            "🔍 Buscar comando:",
            placeholder="Ex: print, len, for, append...",
            help="Busca no nome do comando e na descrição",
        )

        # As opções guardam o valor original do CSV e só o rótulo é traduzido.
        # Filtrar pelo rótulo exigiria busca reversa — e falhava calado quando
        # a categoria não tinha tradução.
        categoria = st.selectbox(
            "📂 Categoria:",
            ["Todas", *sorted(df["categoria"].unique(), key=rotulo_categoria)],
            format_func=lambda c: "Todas" if c == "Todas" else rotulo_categoria(c),
        )
        tipo = st.selectbox(
            "🏷️ Tipo:",
            ["Todos", *sorted(df["tipo"].unique(), key=rotulo_tipo)],
            format_func=lambda t: "Todos" if t == "Todos" else rotulo_tipo(t),
        )
        nivel = st.selectbox(
            "📊 Nível:",
            ["Todos", *[n for n in NIVEIS if (df["nivel"] == n).any()]],
            format_func=lambda n: "Todos" if n == "Todos" else NIVEIS[n],
        )
        trilha = st.selectbox(
            "🎓 Trilha de aprendizado:",
            ["Todas", *[t for t in TRILHAS if df["trilha"].str.contains(t, regex=False).any()]],
            format_func=lambda t: "Todas" if t == "Todas" else TRILHAS[t],
            help="Um percurso temático, do básico ao avançado",
        )
        so_exemplo = st.checkbox(
            "Só com exemplo executável",
            value=(modo == MODO_ESTUDAR),
            help="Mostra apenas os comandos com exemplo, saída verificada e armadilha",
        )

        st.markdown("---")
        st.markdown("### 📚 Como usar:")
        st.markdown(
            """
            - **Catálogo**: busque e filtre a referência inteira
            - **Estudar**: veja de onde o Python tira cada nome e caia nas armadilhas
            - **Playground**: rode e edite o código de verdade
            """
        )

    return {
        "modo": modo, "busca": busca, "categoria": categoria, "tipo": tipo,
        "nivel": nivel, "trilha": trilha, "so_exemplo": so_exemplo,
    }


def aplicar_filtros(df: pd.DataFrame, f: dict) -> pd.DataFrame:
    filtrado = df

    if f["busca"]:
        # regex=False: comandos como `+`, `*` e `**` são regex inválidos
        # e derrubavam a busca com re.error.
        alvo = filtrado["comando"].str.contains(f["busca"], case=False, regex=False)
        alvo |= filtrado["descricao"].str.contains(f["busca"], case=False, regex=False)
        filtrado = filtrado[alvo]

    if f["categoria"] != "Todas":
        filtrado = filtrado[filtrado["categoria"] == f["categoria"]]
    if f["tipo"] != "Todos":
        filtrado = filtrado[filtrado["tipo"] == f["tipo"]]
    if f["nivel"] != "Todos":
        filtrado = filtrado[filtrado["nivel"] == f["nivel"]]
    if f["trilha"] != "Todas":
        filtrado = filtrado[filtrado["trilha"].str.contains(f["trilha"], regex=False)]
    if f["so_exemplo"]:
        filtrado = filtrado[filtrado["exemplo"] != ""]

    return filtrado


def badges(linha: pd.Series) -> str:
    partes = [
        f'<span class="command-type">{escape(rotulo_tipo(linha["tipo"]))}</span>',
        f'<span class="command-category">{escape(rotulo_categoria(linha["categoria"]))}</span>',
    ]
    if linha["nivel"]:
        partes.append(
            f'<span class="command-nivel nivel-{escape(linha["nivel"])}">'
            f'{escape(NIVEIS.get(linha["nivel"], linha["nivel"]))}</span>'
        )
    return "".join(partes)


def estudar_comando(rotulo: str) -> None:
    """Manda o app para o modo Estudar já no comando escolhido."""
    st.session_state.modo = MODO_ESTUDAR
    st.session_state.comando_estudo = rotulo


def render_catalogo(filtrado: pd.DataFrame) -> None:
    if filtrado.empty:
        st.markdown(
            '<div class="no-results"><h3>😔 Nenhum comando encontrado</h3>'
            "<p>Tente ajustar os filtros ou o termo de busca</p></div>",
            unsafe_allow_html=True,
        )
        return

    total_paginas = -(-len(filtrado) // COMANDOS_POR_PAGINA)  # divisão com teto
    pagina = 1

    cabecalho, seletor = st.columns([3, 1], vertical_alignment="bottom")
    with cabecalho:
        st.markdown(f"### 📋 {len(filtrado)} comando(s) encontrado(s)")
    with seletor:
        if total_paginas > 1:
            pagina = st.selectbox(
                "Página:",
                range(1, total_paginas + 1),
                format_func=lambda p: f"Página {p} de {total_paginas}",
                label_visibility="collapsed",
            )

    inicio = (pagina - 1) * COMANDOS_POR_PAGINA
    for _, linha in filtrado.iloc[inicio : inicio + COMANDOS_POR_PAGINA].iterrows():
        with st.container(border=True):
            esquerda, direita = st.columns([1, 2], vertical_alignment="center")

            with esquerda:
                # st.code traz o botão de copiar nativo, que age no navegador do usuário.
                st.code(linha["rotulo"], language="python")
                if linha["exemplo"]:
                    st.button(
                        "🎓 Estudar",
                        key=f"estudar_{linha['rotulo']}_{linha['categoria']}",
                        on_click=estudar_comando,
                        args=(linha["rotulo"],),
                        use_container_width=True,
                    )

            with direita:
                # escape(): operadores como `<`, `>` e `&` quebravam o HTML dos cards.
                st.markdown(
                    f'<div>{badges(linha)}</div>'
                    f'<div class="command-description">{escape(linha["descricao"])}</div>',
                    unsafe_allow_html=True,
                )


def render_estudar(df: pd.DataFrame, filtrado: pd.DataFrame) -> None:
    estudaveis = filtrado[filtrado["exemplo"] != ""]
    if estudaveis.empty:
        st.info(
            "Nenhum comando com exemplo bate com esses filtros. "
            "Limpe os filtros na barra lateral ou desmarque *Só com exemplo executável*."
        )
        return

    rotulos = estudaveis["rotulo"].tolist()
    atual = st.session_state.get("comando_estudo")
    indice = rotulos.index(atual) if atual in rotulos else 0

    escolhido = st.selectbox(
        f"🎓 Estudar ({len(rotulos)} comandos disponíveis):",
        rotulos,
        index=indice,
        key="seletor_estudo",
    )
    linha = estudaveis[estudaveis["rotulo"] == escolhido].iloc[0]

    st.markdown(f"## `{escolhido}`")
    st.markdown(
        f'<div>{badges(linha)}</div>'
        f'<div class="command-description">{escape(linha["descricao"])}</div>',
        unsafe_allow_html=True,
    )
    st.markdown("")

    # --- o diferencial: de onde o Python tira este nome? ---
    svg, explicacao = diagrama.render(linha["comando"], linha["tipo"])
    st.markdown("#### 🧭 De onde o Python tira isso?")
    # SVG inline não sobrevive ao Streamlit: o Markdown trata as linhas do SVG
    # como bloco de código e cospe as tags como texto, e o st.html() poda os
    # nós. Como data-URI num <img> vai como imagem — imune aos dois.
    svg_uri = b64encode(svg.encode("utf-8")).decode()
    st.markdown(
        f'<div class="diagrama-box">'
        f'<img src="data:image/svg+xml;base64,{svg_uri}" alt="Como o Python resolve {escape(linha["comando"])}">'
        f"</div>",
        unsafe_allow_html=True,
    )
    st.markdown(explicacao)

    esquerda, direita = st.columns(2)
    with esquerda:
        st.markdown("#### 📐 Sintaxe")
        st.code(linha["sintaxe"].replace("\\n", "\n"), language="python")
        st.markdown("#### 💻 Exemplo")
        st.code(linha["exemplo"], language="python")
    with direita:
        st.markdown("#### ▶️ Saída real")
        if linha["executavel"] == "1":
            st.code(linha["saida"] or "(sem saída)", language="text")
            st.caption("Saída gerada executando o exemplo — não foi escrita à mão.")
        else:
            st.info("Este exemplo não roda aqui: depende de digitação ou encerra o programa.")

        if linha["armadilha"]:
            st.markdown(
                f'<div class="armadilha"><span class="armadilha-titulo">⚠️ A armadilha</span>'
                f'{escape(linha["armadilha"])}</div>',
                unsafe_allow_html=True,
            )

    if linha["veja_tambem"]:
        relacionados = [v.strip() for v in linha["veja_tambem"].split("|") if v.strip()]
        st.markdown("#### 🔗 Veja também")
        for coluna, alvo in zip(st.columns(len(relacionados)), relacionados):
            with coluna:
                # só vira botão se o comando existir e for estudável
                destino = df[(df["comando"] == alvo) & (df["exemplo"] != "")]
                if not destino.empty:
                    st.button(
                        alvo,
                        key=f"veja_{escolhido}_{alvo}",
                        on_click=estudar_comando,
                        args=(destino.iloc[0]["rotulo"],),
                        use_container_width=True,
                    )
                else:
                    st.markdown(f"`{alvo}`")

    st.markdown("---")
    anterior, meio, proximo = st.columns([1, 2, 1])
    posicao = rotulos.index(escolhido)
    with anterior:
        if posicao > 0:
            st.button(
                f"⬅️ {rotulos[posicao - 1]}",
                on_click=estudar_comando, args=(rotulos[posicao - 1],),
                use_container_width=True,
            )
    with meio:
        st.markdown(
            f'<p style="text-align:center;color:#6b7280">{posicao + 1} de {len(rotulos)}</p>',
            unsafe_allow_html=True,
        )
    with proximo:
        if posicao < len(rotulos) - 1:
            st.button(
                f"{rotulos[posicao + 1]} ➡️",
                on_click=estudar_comando, args=(rotulos[posicao + 1],),
                use_container_width=True,
            )


def render_playground(df: pd.DataFrame) -> None:
    st.markdown("### ▶️ Playground — Python de verdade, no seu navegador")
    st.markdown(
        "Escolha um comando, **edite o código** e execute. O interpretador roda em "
        "WebAssembly dentro da sua aba: nada vai para servidor nenhum. "
        "Quebre de propósito — ver o erro real é metade do aprendizado."
    )

    com_exemplo = df[(df["exemplo"] != "") & (df["executavel"] == "1")]
    exemplos = [
        {"rotulo": f"{linha['rotulo']} — {linha['descricao']}", "codigo": linha["exemplo"]}
        for _, linha in com_exemplo.iterrows()
    ]

    # A lista é sempre a mesma: o HTML não muda entre reruns, então o Streamlit
    # não remonta o iframe e o Pyodide não recarrega os ~10 MB a cada clique.
    components.html(html_playground(exemplos), height=640, scrolling=True)


def render_rodape() -> None:
    st.markdown(
        """
        <div class="app-footer">
            Ary Ribeiro |
            <a href="https://linkedin.com/in/aryribeiro" target="_blank">linkedin.com/in/aryribeiro</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    render_cabecalho()

    try:
        df = load_data()
    except FileNotFoundError:
        st.error(f"❌ Arquivo '{CSV_PATH.name}' não encontrado na raiz do projeto!")
        st.stop()
    except (ValueError, pd.errors.ParserError) as erro:
        st.error(f"❌ Erro ao carregar '{CSV_PATH.name}': {erro}")
        st.stop()

    render_estatisticas(df)
    filtros = render_sidebar(df)

    if filtros["modo"] == MODO_PLAYGROUND:
        render_playground(df)
        render_rodape()
        return

    if filtros["busca"]:
        st.markdown(
            f'<div class="search-info">🔍 Mostrando resultados para: '
            f"<strong>{escape(filtros['busca'])}</strong></div>",  # escape(): senão o campo de busca é XSS refletido
            unsafe_allow_html=True,
        )

    filtrado = aplicar_filtros(df, filtros)

    if filtros["modo"] == MODO_ESTUDAR:
        render_estudar(df, filtrado)
    else:
        render_catalogo(filtrado)

    render_rodape()


if __name__ == "__main__":
    main()
