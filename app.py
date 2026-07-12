from base64 import b64encode
from html import escape
from pathlib import Path

import pandas as pd
import streamlit as st

CSV_PATH = Path(__file__).parent / "comandos.csv"
LOGO_PATH = Path(__file__).parent / "logo.png"
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
    .app-logo {
        width: 400px;
        max-width: 90%;
        height: auto;
    }
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

    .command-type, .command-category {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-right: 0.5rem;
    }
    .command-type {background: #e8f4fd; color: #2a5298;}
    .command-category {background: #f0f9ff; color: #1e40af;}

    .command-description {
        color: #4b5563;
        font-size: 1rem;
        margin-top: 0.6rem;
        line-height: 1.5;
    }

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
    "matematica": "🔢 Matemática",
    "string": "📝 Strings",
    "lista": "📋 Listas",
    "dicionario": "📚 Dicionários",
    "conjunto": "🔗 Conjuntos",
    "arquivo": "📁 Arquivos",
    "sistema": "⚙️ Sistema",
    "io": "💻 Entrada/Saída",
    "tempo": "⏰ Data/Tempo",
    "aleatorio": "🎲 Aleatório",
    "regex": "🔍 Regex",
    "json": "📊 JSON",
    "iteracao": "🔄 Iteração",
    "estrutura_dados": "🏗️ Estruturas de Dados",
    "funcional": "⚡ Programação Funcional",
    "objeto": "🎯 Objetos",
    "web": "🌐 Web/URLs",
    "controle": "🎛️ Controle de Fluxo",
    "funcao": "🔧 Funções",
    "orientacao_objeto": "🏛️ Orientação a Objetos",
    "excecao": "⚠️ Exceções",
    "import": "📦 Imports",
    "escopo": "🔐 Escopo",
    "debug": "🐛 Debug",
    "assincrono": "⚡ Assíncrono",
    "conversao": "🔄 Conversão",
    "sequencia": "📊 Sequências",
    "inspecao": "🔍 Inspeção",
    "memoria": "💾 Memória",
    "utilitario": "🛠️ Utilitários",
    "contexto": "📋 Context Managers",
    "gerador": "⚙️ Geradores",
    "constante": "📏 Constantes",
    "logica": "🧠 Lógica",
    "operador_logico": "🧮 Operadores Lógicos",
    "operador": "➕ Operadores",
    "aritmetico": "🔢 Aritmética",
    "comparacao": "⚖️ Comparação",
    "atribuicao": "📝 Atribuição",
    "bitwise": "🔀 Bitwise",
}

TIPOS = {
    "keyword": "🔑 Palavra-chave",
    "builtin_function": "⚡ Função Built-in",
    "list_method": "📋 Método de Lista",
    "str_method": "📝 Método de String",
    "dict_method": "📚 Método de Dicionário",
    "set_method": "🔗 Método de Conjunto",
    "file_method": "📁 Método de Arquivo",
    "operator": "➕ Operador",
    "os_module": "🖥️ Módulo OS",
    "sys_module": "⚙️ Módulo Sys",
    "datetime_module": "📅 Módulo DateTime",
    "time_module": "⏱️ Módulo Time",
    "random_module": "🎲 Módulo Random",
    "re_module": "🔍 Módulo RE",
    "json_module": "📊 Módulo JSON",
    "math_module": "🔢 Módulo Math",
    "itertools_module": "🔄 Módulo Itertools",
    "collections_module": "🏗️ Módulo Collections",
    "functools_module": "⚡ Módulo Functools",
    "copy_module": "📋 Módulo Copy",
    "urllib_module": "🌐 Módulo Urllib",
}

# Prefixo do módulo, para desambiguar homônimos: itertools.count vs count (list),
# re.compile vs compile (built-in), time.time vs datetime.time...
PREFIXOS = {
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


def rotulo_categoria(categoria: str) -> str:
    return CATEGORIAS.get(categoria, categoria.replace("_", " ").title())


def rotulo_tipo(tipo: str) -> str:
    return TIPOS.get(tipo, tipo.replace("_", " ").title())


def nome_qualificado(comando: str, tipo: str) -> str:
    """`compile` do módulo re vira `re.compile` — sem isso, homônimos viram cards idênticos."""
    prefixo = PREFIXOS.get(tipo)
    return f"{prefixo}.{comando}" if prefixo else comando


@st.cache_data
def load_data() -> pd.DataFrame:
    # keep_default_na=False: sem isso o pandas converte o comando `None` em NaN
    # e ele some da base (`None` está na lista de na_values padrão).
    df = pd.read_csv(CSV_PATH, keep_default_na=False, dtype=str)

    faltando = [c for c in COLUNAS_OBRIGATORIAS if c not in df.columns]
    if faltando:
        raise ValueError(f"Colunas ausentes no CSV: {', '.join(faltando)}")

    for coluna in COLUNAS_OBRIGATORIAS:
        df[coluna] = df[coluna].str.strip()

    return df[df["comando"] != ""].reset_index(drop=True)


@st.cache_data
def logo_base64() -> str:
    return b64encode(LOGO_PATH.read_bytes()).decode()


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
    st.markdown(
        f"""
        <div class="stats-container">
            <div class="stat-item">
                <div class="stat-number">{len(df)}</div>
                <div class="stat-label">Comandos</div>
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


def render_filtros(df: pd.DataFrame) -> tuple[str, str, str]:
    with st.sidebar:
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
            "📂 Filtrar por categoria:",
            ["Todas", *sorted(df["categoria"].unique(), key=rotulo_categoria)],
            format_func=lambda c: "Todas" if c == "Todas" else rotulo_categoria(c),
            help="Escolha uma categoria para ver comandos relacionados",
        )

        tipo = st.selectbox(
            "🏷️ Filtrar por tipo:",
            ["Todos", *sorted(df["tipo"].unique(), key=rotulo_tipo)],
            format_func=lambda t: "Todos" if t == "Todos" else rotulo_tipo(t),
            help="Escolha um tipo específico de comando",
        )

        st.markdown("---")
        st.markdown("### 📚 Como usar:")
        st.markdown(
            """
            - **Busque** pelo nome do comando ou pela descrição
            - **Filtre** por categoria ou tipo
            - **Copie** passando o mouse sobre o comando e clicando em 📋
            - **Explore** as categorias para aprender
            """
        )

    return busca, categoria, tipo


def aplicar_filtros(df: pd.DataFrame, busca: str, categoria: str, tipo: str) -> pd.DataFrame:
    filtrado = df

    if busca:
        # regex=False: comandos como `+`, `*` e `**` são regex inválidos
        # e derrubavam a busca com re.error.
        alvo = filtrado["comando"].str.contains(busca, case=False, regex=False)
        alvo |= filtrado["descricao"].str.contains(busca, case=False, regex=False)
        filtrado = filtrado[alvo]

    if categoria != "Todas":
        filtrado = filtrado[filtrado["categoria"] == categoria]

    if tipo != "Todos":
        filtrado = filtrado[filtrado["tipo"] == tipo]

    return filtrado


def render_card(linha: pd.Series) -> None:
    with st.container(border=True):
        esquerda, direita = st.columns([1, 2], vertical_alignment="center")

        with esquerda:
            # st.code traz o botão de copiar nativo, que age no navegador do usuário.
            st.code(nome_qualificado(linha["comando"], linha["tipo"]), language="python")

        with direita:
            # escape(): operadores como `<`, `>` e `&` quebravam o HTML dos cards.
            st.markdown(
                f"""
                <div>
                    <span class="command-type">{escape(rotulo_tipo(linha['tipo']))}</span>
                    <span class="command-category">{escape(rotulo_categoria(linha['categoria']))}</span>
                </div>
                <div class="command-description">{escape(linha['descricao'])}</div>
                """,
                unsafe_allow_html=True,
            )


def render_resultados(filtrado: pd.DataFrame) -> None:
    if filtrado.empty:
        st.markdown(
            """
            <div class="no-results">
                <h3>😔 Nenhum comando encontrado</h3>
                <p>Tente ajustar os filtros ou o termo de busca</p>
            </div>
            """,
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
        render_card(linha)


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
    busca, categoria, tipo = render_filtros(df)

    if busca:
        st.markdown(
            f'<div class="search-info">🔍 Mostrando resultados para: '
            f"<strong>{escape(busca)}</strong></div>",  # escape(): sem isso, o campo de busca era XSS refletido
            unsafe_allow_html=True,
        )

    render_resultados(aplicar_filtros(df, busca, categoria, tipo))
    render_rodape()


if __name__ == "__main__":
    main()
