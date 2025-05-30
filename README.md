Obs.: caso o app esteja no modo "sleeping" (dormindo) ao entrar, basta clicar no botão que estará disponível e aguardar, para ativar o mesmo. 
![print](https://github.com/user-attachments/assets/970c11b4-0bbb-4971-a30f-43892a1317f5)

# 🐍 Comandos Python - Referência Interativa

## Descrição

"Comandos Python" é uma aplicação web interativa construída com Python e Streamlit, projetada para servir como uma referência de comandos Python, especialmente útil para alunos e iniciantes na linguagem. A aplicação permite aos usuários navegar, pesquisar e filtrar comandos Python, visualizando suas descrições, categorias e tipos de forma amigável e organizada.

## ✨ Funcionalidades

* **Busca de Comandos:** Encontre comandos rapidamente digitando seus nomes.
* **Filtragem Avançada:** Filtre comandos por categoria (ex: Matemática, Strings, Listas) e tipo (ex: Palavra-chave, Função Built-in, Método de Lista).
* **Visualização em Cards:** Cada comando é apresentado em um card informativo com seu nome, tipo, categoria e descrição detalhada.
* **Copiar para Área de Transferência:** Copie facilmente o nome do comando com um clique no botão "📋 Copiar".
* **Traduções Amigáveis:** Categorias e tipos técnicos são traduzidos para termos mais acessíveis, incluindo emojis para fácil identificação.
* **Estatísticas:** Visualize o número total de comandos, categorias e tipos disponíveis na base de dados.
* **Interface Moderna:** Design profissional e limpo com CSS customizado para uma melhor experiência do usuário.
* **Guia Rápido:** Instruções de como usar os filtros e a busca diretamente na barra lateral.
* **Logo Customizada:** Exibe uma logo da aplicação no cabeçalho (requer `logo.png`).

## 🛠️ Tecnologias Utilizadas

* **Python:** Linguagem base da aplicação.
* **Streamlit:** Framework para construção da interface web interativa.
* **Pandas:** Para manipulação e carregamento dos dados dos comandos a partir de um arquivo CSV.
* **Pyperclip:** Para a funcionalidade de copiar para a área de transferências.

## 🚀 Configuração e Instalação

Siga os passos abaixo para executar a aplicação localmente:

1.  **Pré-requisitos:**
    * Python 3.7 ou superior instalado.
    * `pip` (gerenciador de pacotes Python).

2.  **Clone o Repositório (Exemplo):**
    ```bash
    git clone [https://github.com/aryribeiro/comandos-python.git](https://github.com/aryribeiro/comandos-python.git)
    cd comandos-python-app
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
    Crie um arquivo `requirements.txt` com o seguinte conteúdo:
    ```txt
    streamlit
    pandas
    pyperclip
    ```
    Em seguida, instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Estrutura de Arquivos Necessária:**
    Certifique-se de que os seguintes arquivos estejam na raiz do projeto:
    * `app.py` (o script principal da aplicação)
    * `comandos.csv` (o arquivo CSV contendo os dados dos comandos)
    * `logo.png` (arquivo de imagem para o logo da aplicação, opcional mas recomendado para a experiência completa)

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

**Customização**

    Adicionar Novos Comandos: Para adicionar mais comandos, edite o arquivo comandos.csv seguindo o formato especificado.
    Novas Categorias/Tipos: Se adicionar comandos com novas categorias ou tipos técnicos, atualize os dicionários get_category_translation() e get_type_translation() no arquivo app.py para incluir traduções amigáveis e emojis correspondentes.
    Estilo Visual: Modifique o CSS dentro das seções st.markdown("""<style>...</style>""") no arquivo app.py para alterar a aparência da aplicação.

👤 Autor

#### Ary Ribeiro 📧 aryribeiro@gmail.com
