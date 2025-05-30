import streamlit as st
import pandas as pd
import pyperclip
from typing import List, Dict

# Configuração da página
st.set_page_config(
    page_title="Comandos Python | por Ary Ribeiro",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para design profissional
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .command-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #2a5298;
        transition: transform 0.2s;
    }
    
    .command-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .command-name {
        font-size: 1.4rem;
        font-weight: bold;
        color: #1e3c72;
        margin-bottom: 0.5rem;
    }
    
    .command-type {
        display: inline-block;
        background: #e8f4fd;
        color: #2a5298;
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-right: 0.5rem;
    }
    
    .command-category {
        display: inline-block;
        background: #f0f9ff;
        color: #1e40af;
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .command-description {
        color: #4b5563;
        font-size: 1rem;
        margin-top: 0.8rem;
        line-height: 1.5;
    }
    
    .copy-button {
        background: #10b981;
        color: white;
        border: none;
        padding: 0.4rem 0.8rem;
        border-radius: 5px;
        cursor: pointer;
        font-size: 0.8rem;
        margin-top: 0.5rem;
    }
    
    .copy-button:hover {
        background: #059669;
    }
    
    .stats-container {
        display: flex;
        justify-content: space-around;
        background: #f8fafc;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #1e3c72;
    }
    
    .stat-label {
        color: #6b7280;
        font-size: 0.9rem;
    }
    
    .sidebar-header {
        color: #1e3c72;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 1rem;
    }
    
    .no-results {
        text-align: center;
        padding: 3rem;
        color: #6b7280;
    }
    
    .search-info {
        background: #fef3c7;
        border: 1px solid #f59e0b;
        border-radius: 5px;
        padding: 0.8rem;
        margin-bottom: 1rem;
        color: #92400e;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Carrega os dados do CSV"""
    try:
        df = pd.read_csv('comandos.csv')
        return df
    except FileNotFoundError:
        st.error("❌ Arquivo 'comandos.csv' não encontrado na raiz do projeto!")
        st.stop()
    except Exception as e:
        st.error(f"❌ Erro ao carregar o arquivo: {str(e)}")
        st.stop()

def copy_to_clipboard(text: str):
    """Copia texto para área de transferência"""
    try:
        pyperclip.copy(text)
        return True
    except:
        return False

def get_category_translation():
    """Traduz categorias técnicas para nomes amigáveis"""
    return {
        'matematica': '🔢 Matemática',
        'string': '📝 Strings',
        'lista': '📋 Listas',
        'dicionario': '📚 Dicionários',
        'conjunto': '🔗 Conjuntos',
        'arquivo': '📁 Arquivos',
        'sistema': '⚙️ Sistema',
        'io': '💻 Entrada/Saída',
        'tempo': '⏰ Data/Tempo',
        'aleatorio': '🎲 Aleatório',
        'regex': '🔍 Regex',
        'json': '📊 JSON',
        'iteracao': '🔄 Iteração',
        'estrutura_dados': '🏗️ Estruturas de Dados',
        'funcional': '⚡ Programação Funcional',
        'objeto': '🎯 Objetos',
        'web': '🌐 Web/URLs',
        'controle': '🎛️ Controle de Fluxo',
        'funcao': '🔧 Funções',
        'orientacao_objeto': '🏛️ Orientação a Objetos',
        'excecao': '⚠️ Exceções',
        'import': '📦 Imports',
        'escopo': '🔐 Escopo',
        'debug': '🐛 Debug',
        'assincrono': '⚡ Assíncrono',
        'conversao': '🔄 Conversão',
        'sequencia': '📊 Sequências',
        'inspecao': '🔍 Inspeção',
        'memoria': '💾 Memória',
        'utilitario': '🛠️ Utilitários',
        'contexto': '📋 Context Managers',
        'gerador': '⚙️ Geradores',
        'constante': '📏 Constantes',
        'operador_logico': '🧮 Operadores Lógicos',
        'operador': '➕ Operadores',
        'aritmetico': '🔢 Aritmética',
        'comparacao': '⚖️ Comparação',
        'atribuicao': '📝 Atribuição',
        'bitwise': '🔀 Bitwise'
    }

def get_type_translation():
    """Traduz tipos técnicos para nomes amigáveis"""
    return {
        'keyword': '🔑 Palavra-chave',
        'builtin_function': '⚡ Função Built-in',
        'list_method': '📋 Método de Lista',
        'str_method': '📝 Método de String',
        'dict_method': '📚 Método de Dicionário',
        'set_method': '🔗 Método de Conjunto',
        'file_method': '📁 Método de Arquivo',
        'operator': '➕ Operador',
        'os_module': '🖥️ Módulo OS',
        'sys_module': '⚙️ Módulo Sys',
        'datetime_module': '📅 Módulo DateTime',
        'time_module': '⏱️ Módulo Time',
        'random_module': '🎲 Módulo Random',
        're_module': '🔍 Módulo RE',
        'json_module': '📊 Módulo JSON',
        'math_module': '🔢 Módulo Math',
        'itertools_module': '🔄 Módulo Itertools',
        'collections_module': '🏗️ Módulo Collections',
        'functools_module': '⚡ Módulo Functools',
        'copy_module': '📋 Módulo Copy',
        'urllib_module': '🌐 Módulo Urllib'
    }

def main():
    # Header principal com logo
    try:
        # Container centralizado para logo e slogan
        st.markdown("""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 2rem 0;">
        """, unsafe_allow_html=True)
        
        # Logo centralizada
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.image("logo.png", width=400)
        
        # Slogan centralizado
        st.markdown("""
            <div style="text-align: center; margin-top: 1rem; margin-bottom: 2rem;">
                <p style="font-size: 1.2rem; color: #6b7280; font-weight: 500; margin: 0;">
                    Referência completa para alunos e iniciantes
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    except FileNotFoundError:
        # Fallback caso a logo não seja encontrada
        st.markdown("""
        <div class="main-header">
            <h1>🐍 Comandos Python</h1>
            <p>Referência completa para alunos e iniciantes</p>
        </div>
        """, unsafe_allow_html=True)
        st.warning("⚠️ Logo 'logo.png' não encontrada na raiz do projeto. Usando título padrão.")
    
    # Carrega os dados
    df = load_data()
    
    # Traduções
    category_translation = get_category_translation()
    type_translation = get_type_translation()
    
    # Estatísticas
    total_commands = len(df)
    total_categories = df['categoria'].nunique()
    total_types = df['tipo'].nunique()
    
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-item">
            <div class="stat-number">{total_commands}</div>
            <div class="stat-label">Comandos</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{total_categories}</div>
            <div class="stat-label">Categorias</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{total_types}</div>
            <div class="stat-label">Tipos</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar para filtros
    with st.sidebar:
        st.markdown('<div class="sidebar-header">🔍 Filtros e Busca</div>', unsafe_allow_html=True)
        
        # Campo de busca
        search_term = st.text_input(
            "🔍 Buscar comando:",
            placeholder="Digite o nome do comando (ex: print, len, for...)",
            help="Digite parte do nome do comando para encontrá-lo rapidamente"
        )
        
        # Filtro por categoria
        categories = ['Todas'] + sorted([category_translation.get(cat, cat.title()) 
                                       for cat in df['categoria'].unique()])
        selected_category = st.selectbox(
            "📂 Filtrar por categoria:",
            categories,
            help="Escolha uma categoria para ver comandos relacionados"
        )
        
        # Filtro por tipo
        types = ['Todos'] + sorted([type_translation.get(tipo, tipo.replace('_', ' ').title()) 
                                  for tipo in df['tipo'].unique()])
        selected_type = st.selectbox(
            "🏷️ Filtrar por tipo:",
            types,
            help="Escolha um tipo específico de comando"
        )
        
        # Informações adicionais na sidebar
        st.markdown("---")
        st.markdown("### 📚 Como usar:")
        st.markdown("""
        - **Busque** digitando o nome do comando
        - **Filtre** por categoria ou tipo
        - **Copie** comandos clicando no botão 📋
        - **Explore** diferentes categorias para aprender
        """)
        st.markdown("---")
        st.markdown("""
        **Por Ary Ribeiro** | aryribeiro@gmail.com
        """)
    
    # Aplicar filtros
    filtered_df = df.copy()
    
    # Filtro de busca
    if search_term:
        filtered_df = filtered_df[
            filtered_df['comando'].str.contains(search_term, case=False, na=False)
        ]
        st.markdown(f"""
        <div class="search-info">
            🔍 Mostrando resultados para: <strong>"{search_term}"</strong>
        </div>
        """, unsafe_allow_html=True)
    
    # Filtro por categoria
    if selected_category != 'Todas':
        # Encontrar a categoria original baseada na tradução
        original_category = None
        for orig, trans in category_translation.items():
            if trans == selected_category:
                original_category = orig
                break
        if original_category:
            filtered_df = filtered_df[filtered_df['categoria'] == original_category]
    
    # Filtro por tipo
    if selected_type != 'Todos':
        # Encontrar o tipo original baseado na tradução
        original_type = None
        for orig, trans in type_translation.items():
            if trans == selected_type:
                original_type = orig
                break
        if original_type:
            filtered_df = filtered_df[filtered_df['tipo'] == original_type]
    
    # Mostrar resultados
    if len(filtered_df) == 0:
        st.markdown("""
        <div class="no-results">
            <h3>😔 Nenhum comando encontrado</h3>
            <p>Tente ajustar os filtros ou termo de busca</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"### 📋 Encontrados {len(filtered_df)} comando(s)")
        
        # Exibir comandos em cards
        for index, row in filtered_df.iterrows():
            comando = row['comando']
            tipo = row['tipo']
            categoria = row['categoria']
            descricao = row['descricao']
            
            # Traduzir tipo e categoria
            tipo_display = type_translation.get(tipo, tipo.replace('_', ' ').title())
            categoria_display = category_translation.get(categoria, categoria.title())
            
            # Card do comando
            card_html = f"""
            <div class="command-card">
                <div class="command-name">{comando}</div>
                <div>
                    <span class="command-type">{tipo_display}</span>
                    <span class="command-category">{categoria_display}</span>
                </div>
                <div class="command-description">{descricao}</div>
            </div>
            """
            
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(card_html, unsafe_allow_html=True)
            
            with col2:
                if st.button(f"📋 Copiar", key=f"copy_{index}", help="Copiar comando"):
                    if copy_to_clipboard(comando):
                        st.success("✅ Copiado!")
                    else:
                        st.error("❌ Erro ao copiar")
                        st.info(f"Comando: `{comando}`")

if __name__ == "__main__":
    main()

st.markdown("""
<style>
    .main {
        background-color: #ffffff;
        color: #333333;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    /* Esconde completamente todos os elementos da barra padrão do Streamlit */
    header {display: none !important;}
    footer {display: none !important;}
    #MainMenu {display: none !important;}
    /* Remove qualquer espaço em branco adicional */
    div[data-testid="stAppViewBlockContainer"] {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    div[data-testid="stVerticalBlock"] {
        gap: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    /* Remove quaisquer margens extras */
    .element-container {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }
</style>
""", unsafe_allow_html=True)