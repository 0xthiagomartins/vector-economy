# Vector Economy

Um modelo de análise econômica vetorial para avaliação de carteiras de ativos em ambientes DeFi.

## Visão Geral

Este projeto implementa um modelo matemático para análise de valor e poder de compra de carteiras de ativos em ambientes DeFi, com foco em:

- Análise de liquidez em DEXes
- Cálculo de poder de barganha
- Avaliação de rotas de permuta diretas e indiretas
- Modelagem vetorial de valor de ativos

## Estrutura do Projeto

```
vectorial-economics/
├── data/               # Dados mockados para análise
├── notebooks/          # Jupyter notebooks com análises
├── src/               # Código fonte do projeto
│   ├── models/        # Implementações dos modelos
│   ├── utils/         # Funções utilitárias
│   └── data/          # Scripts de processamento de dados
└── requirements.txt   # Dependências do projeto
```

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual Python:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```
3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

1. Ative o ambiente virtual
2. Inicie o Jupyter Notebook:
```bash
jupyter notebook
```
3. Navegue até a pasta `notebooks/` e abra o notebook principal

## Roadmap

- [ ] Implementação do modelo base de vetores
- [ ] Análise de liquidez em DEXes
- [ ] Cálculo de rotas de permuta
- [ ] Visualização de resultados
- [ ] Documentação detalhada
