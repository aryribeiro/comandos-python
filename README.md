Obs.: caso o app esteja no modo "sleeping" (dormindo) ao entrar, basta clicar no botão que estará disponível e aguardar, para ativar o mesmo. 
![print](https://github.com/user-attachments/assets/970c11b4-0bbb-4971-a30f-43892a1317f5)

# 🐍 Comandos Python

## Descrição

"Comandos Python" é uma aplicação web interativa construída com Python e Streamlit, projetada para servir como uma referência de comandos Python, especialmente útil para alunos e iniciantes na linguagem. A aplicação permite aos usuários navegar, pesquisar e filtrar comandos Python, visualizando suas descrições, categorias e tipos de forma amigável e organizada.

🔗 **App online:** https://comandos.streamlit.app/

## ✨ Funcionalidades

* **Busca de Comandos:** Encontre comandos rapidamente pelo nome **ou pela descrição**.
* **Filtragem Avançada:** Filtre comandos por categoria (ex: Matemática, Strings, Listas) e tipo (ex: Palavra-chave, Função Built-in, Método de Lista).
* **Visualização em Cards:** Cada comando é apresentado em um card informativo com seu nome, tipo, categoria e descrição detalhada.
* **Copiar para Área de Transferência:** Passe o mouse sobre o comando e clique no ícone 📋 do bloco de código para copiá-lo.
* **Nomes Qualificados:** Comandos homônimos são exibidos com o namespace do módulo (`re.compile`, `itertools.count`, `time.time`), evitando ambiguidade.
* **Traduções Amigáveis:** Categorias e tipos técnicos são traduzidos para termos mais acessíveis, incluindo emojis para fácil identificação.
* **Estatísticas:** Visualize o número total de comandos, categorias e tipos disponíveis na base de dados.
* **Paginação:** Os resultados são exibidos em páginas de 25 comandos, mantendo a navegação fluida.
* **Interface Moderna:** Design profissional e limpo com CSS customizado para uma melhor experiência do usuário.
* **Guia Rápido:** Instruções de como usar os filtros e a busca diretamente na barra lateral.

## 🛠️ Tecnologias Utilizadas

* **Python:** Linguagem base da aplicação.
* **Streamlit:** Framework para construção da interface web interativa. A cópia de comandos usa o botão nativo do `st.code`, que age no navegador do usuário.
* **Pandas:** Para manipulação e carregamento dos dados dos comandos a partir de um arquivo CSV.

## 🚀 Configuração e Instalação

Siga os passos abaixo para executar a aplicação localmente:

1.  **Pré-requisitos:**
    * Python 3.9 ou superior instalado.
    * `pip` (gerenciador de pacotes Python).

2.  **Clone o Repositório:**
    ```bash
    git clone https://github.com/aryribeiro/comandos-python.git
    cd comandos-python
    ```

3.  **Crie e Ative um Ambiente Virtual (Recomendado):**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

4.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Estrutura de Arquivos:**
    * `app.py` — script principal da aplicação
    * `comandos.csv` — base de dados dos comandos
    * `logo.png` — logo exibida no cabeçalho (opcional; há fallback para título em texto)
    * `.streamlit/config.toml` — fixa o tema claro, que o CSS da aplicação assume

6.  **Execute a Aplicação:**
    ```bash
    streamlit run app.py
    ```
    A aplicação deverá abrir automaticamente no seu navegador padrão.

## 📊 Fonte de Dados (`comandos.csv`)

A aplicação carrega os comandos Python a partir de um arquivo chamado `comandos.csv` localizado na raiz do projeto. Este arquivo deve conter as seguintes colunas:

* `comando`: O nome do comando/função/método (ex: `print`, `len`, `append`).
* `tipo`: O tipo técnico do comando (ex: `builtin_function`, `list_method`, `keyword`).
* `categoria`: A categoria técnica do comando (ex: `io`, `sequencia`, `lista`).
* `descricao`: Uma breve descrição do que o comando faz.

**Exemplo de linha no `comandos.csv`:**
```csv
comando,tipo,categoria,descricao
print,builtin_function,io,"Imprime objetos para o fluxo de texto padrão (geralmente a tela)."
len,builtin_function,sequencia,"Retorna o número de itens em um container."
```

> ⚠️ O CSV é lido com `keep_default_na=False`. Sem isso o pandas converte o comando `None` em `NaN` e ele desaparece da base — `None` faz parte da lista de valores nulos padrão do pandas.

## 🎨 Customização

* **Adicionar Novos Comandos:** Edite o `comandos.csv` seguindo o formato acima.
* **Novas Categorias/Tipos:** Ao introduzir uma categoria ou tipo novo, adicione a tradução nos dicionários `CATEGORIAS` e `TIPOS` no `app.py`. Sem a tradução, o filtro continua funcionando, mas o rótulo cai no fallback genérico.
* **Novos Módulos:** Para que um comando de módulo apareça qualificado (ex: `math.pow`), registre o prefixo no dicionário `PREFIXOS`.
* **Estilo Visual:** O CSS fica em um único bloco `st.markdown` no topo do `app.py`.

> ⚠️ Não esconda o `<header>` do Streamlit no CSS: a seta de abrir/fechar a barra lateral é renderizada dentro dele. Esconda apenas os itens do toolbar (`stToolbarActions`, `stMainMenu`, `stStatusWidget`).

## 👤 Autor

**Ary Ribeiro** — [linkedin.com/in/aryribeiro](https://linkedin.com/in/aryribeiro)
