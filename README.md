Obs.: caso o app esteja no modo "sleeping" (dormindo) ao entrar, basta clicar no botão que estará disponível e aguardar, para ativar o mesmo. 
![print](https://github.com/user-attachments/assets/970c11b4-0bbb-4971-a30f-43892a1317f5)

# 🐍 Comandos Python

Referência de comandos Python para alunos e iniciantes — **que executa o que ensina**.

🔗 **App online:** https://comandos.streamlit.app/

## O que faz este app diferente

A maioria das referências te mostra *o que* um comando faz. Esta responde três perguntas que os alunos erram e quase ninguém ensina:

**1. De onde o Python tira esse nome?**
`len(x)` e `x.append(1)` *parecem* a mesma coisa — e não são. `len` é um **nome**, procurado na cadeia LEGB (Local → Enclosing → Global → Built-in). `append` **não está no LEGB**: é um **atributo** do objeto. `for` não é nome nem atributo — é **sintaxe**, resolvida pelo parser. E `math.sqrt` só existe depois que o `import` põe `math` no Global.

Cada comando ganha um diagrama do seu caminho de resolução. É isso que explica, de uma vez, por que `append(x)` sozinho dá `NameError` e por que `len` funciona sem importar nada.

**2. Qual é a armadilha?**
Cada comando do núcleo traz a pegadinha clássica em destaque. `round(2.5)` é **2**, não 3. `'banana'.strip('ba')` vira **`'nan'`**. `lista.sort()` devolve **None**. `all([])` é **True**. São os erros que o aluno vai cometer — melhor cometer aqui.

**3. E se eu mudar o código?**
O **Playground** roda Python de verdade dentro do navegador (Pyodide/WebAssembly). O aluno edita, quebra de propósito e vê o erro real. Nada é executado no servidor.

## ✅ As saídas não são escritas à mão

Toda saída publicada foi gerada **executando o exemplo**. O [verificar_exemplos.py](verificar_exemplos.py) roda os 93 exemplos executáveis num subprocesso isolado e compara o stdout com a coluna `saida` do CSV:

```bash
python verificar_exemplos.py
```

Ele sai com erro se algum exemplo quebrar ou divergir — ou seja, se o app estiver mentindo para o aluno. Rode sempre depois de mexer no CSV.

## ✨ Funcionalidades

* **📖 Catálogo** — busca (no nome *e* na descrição) e filtros por categoria, tipo, nível e trilha, sobre os 363 comandos.
* **🎓 Estudar** — um comando por vez: diagrama de resolução, sintaxe, exemplo, saída verificada, armadilha, veja-também e navegação anterior/próximo.
* **▶️ Playground** — edite e execute Python no seu navegador, sem servidor.
* **Trilhas de aprendizado** — percursos temáticos, dos primeiros passos às ferramentas do dia a dia.
* **Níveis** — iniciante, intermediário e avançado.
* **Nomes qualificados** — homônimos aparecem com o namespace (`re.compile`, `itertools.count`, `time.time`), em vez de virarem cards idênticos.
* **Copiar** — botão nativo do `st.code`, que age no navegador de quem acessa.
* **Trilha sonora** — música de fundo opcional para estudar, com play/pause e volume.

## 🛠️ Tecnologias

* **Streamlit** — interface. A cópia usa o botão nativo do `st.code`.
* **Pandas** — carga do CSV.
* **Pyodide** — CPython compilado para WebAssembly, rodando no navegador do aluno.
* **SVG** — os diagramas de resolução de nomes, gerados em Python.

## 🚀 Rodando localmente

```bash
git clone https://github.com/aryribeiro/comandos-python.git
cd comandos-python
python -m venv venv && venv\Scripts\activate      # Windows
pip install -r requirements.txt
streamlit run app.py
```

## 📁 Estrutura

| Arquivo | Papel |
|---|---|
| [app.py](app.py) | Interface: catálogo, modo estudar e playground |
| [diagrama.py](diagrama.py) | Gera o SVG "de onde o Python tira isso?" |
| [playground.py](playground.py) | O iframe autocontido do Pyodide |
| [musica.py](musica.py) | Player da trilha sonora |
| [verificar_exemplos.py](verificar_exemplos.py) | Executa os exemplos e confere a saída |
| [comandos.csv](comandos.csv) | A base: 363 comandos, 95 com conteúdo de ensino |
| `static/som.mp3` | Trilha sonora (servida sob demanda) |

## 📊 A base (`comandos.csv`)

| Coluna | Conteúdo |
|---|---|
| `comando`, `tipo`, `categoria`, `descricao` | o verbete (todos os 363) |
| `nivel`, `importancia`, `trilha` | classificação pedagógica |
| `sintaxe`, `exemplo`, `saida` | a lição — `saida` é **gerada por execução** |
| `armadilha` | a pegadinha clássica |
| `veja_tambem` | comandos relacionados (separados por `\|`) |
| `executavel` | `0` quando o exemplo não roda aqui (pede digitação, encerra o processo) |

## 🎨 Customização

* **Novos comandos:** edite o `comandos.csv` e rode o `verificar_exemplos.py`.
* **Novas categorias/tipos:** adicione a tradução em `CATEGORIAS` / `TIPOS` no `app.py`. Sem a tradução o filtro continua funcionando — só o rótulo cai no fallback.
* **Novos módulos:** registre o prefixo em `PREFIXOS` (para sair `math.pow`) e em `MODULO_POR_TIPO` no `diagrama.py`.

### Três armadilhas do Streamlit que este código já pagou

1. **Não esconda o `<header>`.** A seta de abrir/fechar a barra lateral é renderizada dentro dele: escondê-lo deixa o usuário de celular sem busca e sem filtros. Esconda só os itens do toolbar.
2. **SVG inline não sobrevive ao `st.markdown`.** O Markdown trata linha indentada como bloco de código e cospe as tags como texto na tela. Os diagramas vão como data-URI num `<img>`.
3. **O CSV precisa de `keep_default_na=False`.** Sem isso o pandas converte o comando `None` em `NaN` e ele **some da base** — `None` faz parte da lista de nulos padrão do pandas.

## 👤 Autor

**Ary Ribeiro** — [linkedin.com/in/aryribeiro](https://linkedin.com/in/aryribeiro)
