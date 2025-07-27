# Relatórios de Progresso – Iniciação Científica

## Objetivos

- Projeto vinculado ao Centro de Pesquisa em Biologia de Bactérias e Bacteriófagos (CEPID B3) da Universidade de São Paulo.
- Registrar decisões, testes, problemas e aprendizados durante o desenvolvimento do projeto.
- Manter um histórico para acompanhamento pelo orientador e autoavaliação.
- Organizar e garantir a reprodutibilidade dos experimentos e tarefas realizadas durante o desenvolvimento do projeto.

## Sobre o projeto
Este projeto propõe, inicialmente, que as técnicas computacionais relacionadas à pLMs, em especial, o uso de embeddings de nucleotídeos, podem ser utilizadas para um melhor entendimento da taxonomia de bacteriófagos. Para delimitar o escopo da pesquisa a algo que seja adequado a um projeto de iniciação científica, é proposto a construção de um modelo de regressão que utilize embeddings gerados por pLMs a partir de sequências de nucleotídeos para estimar a razão dN/dS sem a necessidade de algoritmos de alinhamento ou de técnicas não escaláveis ou custosas. 
A hipótese central é que embeddings de pLMs retêm informações suficientes sobre restrições evolutivas, conforme especulado por Marquet et al. (2021, p. 1642), e podem, portanto, ser utilizados para prever o dN/dS. A escolha do dN/dS como variável-alvo se justifica uma vez que essa métrica resume taxas evolutivas e permite identificar genes que possivelmente passaram por seleção adaptativa (Jeffares et al., 2015, p. 66). Aplicada ao contexto dos bacteriófagos, supõe-se que dN/dS pode contribuir para esclarecer padrões de evolução entre os genes virais, o que pode auxiliar na compreensão da organização taxonômica desses vírus.

## Objetivo do projeto
Seja $K = (K_1, K_2, \ldots, K_n)$ uma sequência de nucleotídeos de comprimento $n$, codificando uma proteína $P$. Seja $\phi(K_i) \in \mathbb{R}^d$ a representação vetorial do $i$-ésimo nucleotídeo $K_i$, obtida por um modelo de linguagem para proteínas (pLM), e seja $\phi^*(K) \in \mathbb{R}^d$ uma função de agregação que combina as representações $\phi(K_1), \ldots, \phi(K_n)$ em uma única representação vetorial da sequência completa.

Deseja-se estimar a razão entre substituições não-sinônimas e sinônimas associadas a $K$, denotada por $\left(\frac{d_N}{d_S}\right)_K$, por meio de uma função

$$
f: \mathbb{R}^d \rightarrow \mathbb{R}_{\geq 0}
$$

tal que:

$$
f(\phi^*(K)) = \left(\frac{d_N}{d_S}\right)_K + \varepsilon
$$

onde $\varepsilon \in \mathbb{R}$ representa o erro de aproximação da estimativa.

## Arvore de diretórios
.
├── README.md # Descrição geral do repositório
├── Setups/
│   └── config.txt # Informações relativas aos computadores utilizados
├── Relatórios/
│   └── relatórios_%date.md # Relatórios de progresso (YYYY-MM-DD.md)
└── Scripts/
    ├── .py
    ├── .ipynb
    └── .sh
  
