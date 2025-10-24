# Retificação do Desenho Proposto 
- Este documento contém retificações sobre o modelo proposto no relatório do dia 13 de Agosto.

## Objetivo do Modelo
- **Problema encontrado:** o modelo usado (Evo2) é um autoregressor, o que implica que ele produz as representações vetorias sequencialmente em uma única direção. Embora funcione para modelos generativos, a natureza do projeto demanda o conhecimento global da estrutura da sequência codificanete sob análise.
- **Solução proposta:** gerar os embeddings a partir das duas direções do gene. 

### Proposta:
- Seja $G$ um gene composto por $k$ nucleotídeos:

$$
G = \\{ n_1, n_2, \ldots, n_k \\}
$$

- Seja $\mathbb{F}(G) \in \mathbb{R}^d$ a representação vetorial de $G$, obtida por um modelo de linguagem treinado em nucleotídeos.
- Seja $\mathbb{I}(G) \in \mathbb{R}^d$ a representação vetorial do complementar reverso de G (obtido da mesma forma).
- Seja $\mathbb{C}(\mathbb{F}(G), \mathbb{I}(G)) \in \mathbb{R}^{m\times2}$ a função que concatena ambas as representações.
- Seja o conjunto de códons de $G$ definido como:

$$
C = \\{ (n_1, n_2, n_3), (n_4, n_5, n_6), \ldots, (n_{k-2}, n_{k-1}, n_k) \\}
$$

- Seja $\mathbb{B}$ uma função que estima a probabilidade de a taxa de substituições não sinônimas ($\beta$) exceder a taxa de substituições sinônimas ($\alpha$), dado um códon $c_i \in C$ e um conjunto $O$ de genes ortólogos a $G$:

$$
\mathbb{B}(c_i \mid (G, O)) = P(\alpha_i < \beta_i) + \varepsilon_i = P\left[ \left(\frac{dN}{dS}\right)_{c_i} < 1 \\,\middle| (G, O) \right] + \varepsilon_i,
\quad \quad \text{Onde $\varepsilon_i$ é o erro da estimativa para o i-ésimo códon.}$$

- O objetivo do modelo é encontrar uma função $f: \mathbb{R}^d \to \mathbb{R}^m$ que, dada a representação vetorial $\mathbb{V}(G)$, produza as estimativas de $\mathbb{B}(c_i \mid G, O)$ para todos os $m$ códons de $G$:

$$
f(\mathbb{C}(\mathbb{F}(G), \mathbb{R}(G))) = \left[ P(\alpha_1 < \beta_1) + \varepsilon_1^* , \\, \ldots, \\, P(\alpha_m < \beta_m) + \varepsilon_m^* \right], \quad \quad \text{Onde $\varepsilon_i^*$ é o novo erro da estimativa}
$$

- Adicionalmente, busca-se a função $f$ que minimize a soma dos erros:

$$
\min_{f} \sum_{i=1}^m |\varepsilon_i^*|
$$

## Embeddings
- **Suposição**: embeddings de proteína codificam informações evolutivas.
- Serão gerados por uma fonte:
    - Evo2 7B base
- Já existem justificativas que favorecem a representação da camada 26.
