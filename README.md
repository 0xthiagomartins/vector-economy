# Economia Vetorial

Este projeto implementa um modelo de análise econômica vetorial para avaliação de carteiras de ativos em ambientes DeFi (Finanças Descentralizadas). O modelo considera diversos fatores como liquidez, trocas diretas e indiretas, poder de barganha, e suporta múltiplas moedas e ativos.

## Estrutura do Projeto

```
.
├── src/
│   ├── models/
│   │   └── vector_model.py     # Implementação do modelo vetorial
│   └── utils/
│       └── data_generator.py   # Gerador de dados mockados
├── notebooks/
│   └── demo.py                 # Script de demonstração
└── README.md
```

## Requisitos

- Python 3.8+
- NumPy
- Pandas
- Matplotlib
- Seaborn
- NetworkX

Instale as dependências usando:

```bash
pip install numpy pandas matplotlib seaborn networkx
```

## Executando a Demonstração

Para executar a demonstração do modelo:

```bash
python notebooks/demo.py
```

A demonstração irá:
1. Gerar dados mockados de ativos e pools de liquidez
2. Inicializar o modelo vetorial
3. Visualizar o grafo de liquidez
4. Analisar liquidez indireta entre pares de ativos
5. Encontrar e analisar rotas de swap
6. Calcular vetores de permutas
7. Analisar poder de barganha
8. Avaliar carteiras de exemplo

Os resultados serão exibidos no terminal e gráficos serão salvos como arquivos PNG:
- `liquidity_graph.png`: Visualização do grafo de liquidez
- `exchange_vectors.png`: Gráfico dos vetores de permutas
- `bargaining_power.png`: Gráfico do poder de barganha
- `asset_vectors.png`: Visualização dos vetores de ativos

## Componentes do Modelo

### Vetor de Permutas
O vetor de permutas (exchange vector) de um ativo é composto por:
- Permutas diretas: número de pools de liquidez diretas
- Permutas indiretas: número de rotas de swap indiretas
- Eficiência: média das taxas efetivas das rotas
- Diversidade: variedade de ativos alcançáveis

### Liquidez Indireta
O modelo calcula a liquidez indireta entre pares de ativos considerando:
- Rotas de swap disponíveis
- Taxas de swap acumuladas
- Slippage em cada pool
- Profundidade das pools

### Poder de Barganha
O poder de barganha de um ativo é calculado com base em:
- Liquidez total (direta e indireta)
- Volume de negociação
- Número de rotas de swap
- Utilidade e confiança do ativo

## Próximos Passos

- [ ] Integração com dados reais de DEXes
- [ ] Otimização de carteiras usando o modelo vetorial
- [ ] Análise de risco e volatilidade
- [ ] Interface web para visualização e análise
- [ ] Backtesting com dados históricos

## Contribuindo

Contribuições são bem-vindas! Por favor, sinta-se à vontade para abrir issues ou enviar pull requests.
