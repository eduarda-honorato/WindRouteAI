# WindRouteAI

O **WindRouteAI** é um sistema para **planejamento de rotas de manutenção técnica em parques eólicos**, utilizando **algoritmos de busca não ponderada**. Ele permite visualizar o melhor caminho entre turbinas eólicas em um grafo, mostrando a sequência de passos e o custo do percurso.

---

# Requisitos

- Python 3.8+  
- Navegador web (Chrome, Firefox, Edge ou Safari)  
- Biblioteca Flask  

Instale as dependências com:

```bash
pip install flask
```

---

# Como executar

1. Clone ou baixe o repositório.
2. Descompacte os arquivos em uma pasta de sua preferência.
3. Abra o terminal na pasta do projeto.
4. Execute o comando:

```bash
python app.py
```

5. No navegador, acesse:

http://127.0.0.1:5000

A página inicial do **WindRouteAI** será exibida com o menu principal.

---

# Navegação básica

- Na página inicial, clique em "Algoritmos de busca não ponderada" ou "Algoritmos de busca ponderada" para acessar a ferramenta de otimização de rotas.
- Para voltar à página inicial a qualquer momento, clique no nome do programa "WindRouteAI" no canto superior esquerdo.

---

# Como usar a ferramenta

1. Definição do problema
    - No campo Início, escolha uma turbina da lista.
    - No campo Objetivo, escolha uma turbina da lista.
    - No campo Métodos na página "Algoritmos de busca não ponderada", selecione um dos algoritmos:
        > Amplitude
        > Profundidade
        > Profundidade Limitada
        > Aprofundamento Iterativo
        > Bidirecional
    - No campo Métodos na página "Algoritmos de busca ponderada", selecione um dos algoritmos:
        > Custo Uniforme
        > Greedy
        > A-Estrela
        > AIA-Estrela
    - Clique em Executar para visualizar o caminho.

2. Interpretação dos resultados
    - Caminho gerado no grafo
    - Caminho em lista de turbinas
    - Custo do percurso (para os métodos de busca ponderada)
    - Número de passos
    - Caso não exista solução nos métodos Profundidade Limitada (lim=6) ou Aprofundamento Iterativo (lim_max=9), será exibido:
        "Nenhum caminho encontrado"

---

# Exemplo de uso

1. Escolha o ponto de partida: **T3** ou **T20**
2. Escolha o ponto de partida: **T16** ou **T8**
3. Selecione um método na lista.
4. Clique em Executar.
5. Analise os resultados obtidos. 

---

# Contato e suporte

Desenvolvido por Maria Eduarda Honorato e Matheus Jardim