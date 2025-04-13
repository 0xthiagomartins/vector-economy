"""
Demonstração do Modelo de Economia Vetorial

Este script demonstra a utilização do modelo de análise econômica vetorial
para avaliação de carteiras de ativos em ambientes DeFi.
"""

import sys
sys.path.append('..')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from src.models.vector_model import VectorialEconomicModel, SwapRoute
from src.utils.data_generator import MockDataGenerator

def main():
    # 1. Geração de Dados Mockados
    print("1. Gerando dados mockados...")
    data_generator = MockDataGenerator(num_assets=10)
    
    # Gera dados de liquidez
    liquidity_data = data_generator.generate_liquidity_data()
    print("\nDados de Liquidez:")
    print(liquidity_data.head())
    
    # Gera dados de mercado
    market_data = data_generator.generate_market_data()
    print("\nDados de Mercado:")
    print(market_data.head())
    
    # 2. Inicialização do Modelo
    print("\n2. Inicializando o modelo...")
    model = VectorialEconomicModel()
    
    # Adiciona os ativos
    for _, row in market_data.iterrows():
        model.add_asset(row['asset'], row['liquidity_score'] * 1000000)
        # Adiciona outros atributos
        model.assets[row['asset']]['volume'] = row['volume_24h']
        model.assets[row['asset']]['price_impact'] = 1 - row['liquidity_score']
        model.assets[row['asset']]['utility'] = np.random.uniform(0.1, 0.9)
        model.assets[row['asset']]['confidence'] = np.random.uniform(0.1, 0.9)
    
    # Adiciona as pools de liquidez
    for _, row in liquidity_data.iterrows():
        swap_fee = np.random.uniform(0.001, 0.005)
        slippage_model = np.random.choice(['linear', 'quadratic', 'constant'])
        
        model.add_liquidity_pool(
            row['token_a'],
            row['token_b'],
            row['liquidity'],
            swap_fee=swap_fee,
            slippage_model=slippage_model
        )
    
    # 3. Visualização do Grafo de Liquidez
    print("\n3. Visualizando o grafo de liquidez...")
    G = model.liquidity_graph
    pos = nx.spring_layout(G, seed=42)
    
    plt.figure(figsize=(12, 10))
    nx.draw(G, pos, with_labels=True, node_color='lightblue',
            node_size=1000, font_size=10, font_weight='bold',
            edge_color='gray', width=1, alpha=0.7)
    
    edge_labels = {(u, v): f"{G[u][v]['weight']:.0f}" for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    plt.title('Grafo de Liquidez')
    plt.tight_layout()
    plt.savefig('liquidity_graph.png')
    plt.close()
    
    # 4. Análise de Liquidez Indireta
    print("\n4. Analisando liquidez indireta...")
    pairs = [
        (market_data.iloc[0]['asset'], market_data.iloc[-1]['asset']),
        (market_data.iloc[1]['asset'], market_data.iloc[-2]['asset']),
        (market_data.iloc[2]['asset'], market_data.iloc[-3]['asset'])
    ]
    
    for asset_a, asset_b in pairs:
        indirect_liquidity = model.calculate_indirect_liquidity(asset_a, asset_b)
        print(f"Liquidez indireta entre {asset_a} e {asset_b}: {indirect_liquidity:,.2f}")
    
    # 5. Análise de Rotas de Swap
    print("\n5. Analisando rotas de swap...")
    swap_pairs = [
        (market_data.iloc[0]['asset'], market_data.iloc[-1]['asset'], 1000),
        (market_data.iloc[1]['asset'], market_data.iloc[-2]['asset'], 5000),
        (market_data.iloc[2]['asset'], market_data.iloc[-3]['asset'], 10000)
    ]
    
    for asset_a, asset_b, amount in swap_pairs:
        route = model.find_best_swap_route(asset_a, asset_b, amount)
        
        if route:
            print(f"\nMelhor rota de {asset_a} para {asset_b} (quantidade: {amount}):")
            print(f"  Caminho: {' -> '.join(route.path)}")
            print(f"  Custo total: {route.total_cost:.4f}")
            print(f"  Taxa efetiva: {route.effective_rate:.4f}")
            print(f"  Liquidez: {route.liquidity:.2f}")
        else:
            print(f"\nNenhuma rota encontrada de {asset_a} para {asset_b} (quantidade: {amount})")
    
    # 6. Análise de Eficiência de Rotas
    print("\n6. Analisando eficiência de rotas...")
    asset_a = market_data.iloc[0]['asset']
    asset_b = market_data.iloc[-1]['asset']
    amount = 5000
    
    route_analysis = model.analyze_route_efficiency(asset_a, asset_b, amount)
    
    print(f"Rotas mais eficientes de {asset_a} para {asset_b} (quantidade: {amount}):")
    for i, route in enumerate(route_analysis['most_efficient'], 1):
        print(f"\n{i}. {' -> '.join(route.path)}")
        print(f"   Taxa efetiva: {route.effective_rate:.4f}")
        print(f"   Liquidez: {route.liquidity:.2f}")
    
    # 7. Análise do Vetor de Permutas
    print("\n7. Analisando vetores de permutas...")
    exchange_vectors = {}
    for asset in market_data['asset']:
        exchange_vectors[asset] = model.calculate_exchange_vector(asset)
    
    exchange_data = []
    for asset, vector in exchange_vectors.items():
        exchange_data.append({
            'asset': asset,
            'permutas_diretas': vector[0],
            'permutas_indiretas': vector[1],
            'eficiencia': vector[2],
            'diversidade': vector[3]
        })
    
    exchange_df = pd.DataFrame(exchange_data)
    print("\nVetores de Permutas:")
    print(exchange_df)
    
    plt.figure(figsize=(12, 6))
    exchange_df.set_index('asset').plot(kind='bar', width=0.8)
    plt.title('Vetores de Permutas por Ativo')
    plt.ylabel('Valor')
    plt.xlabel('Ativo')
    plt.legend(title='Componente')
    plt.tight_layout()
    plt.savefig('exchange_vectors.png')
    plt.close()
    
    # 8. Análise de Poder de Barganha
    print("\n8. Analisando poder de barganha...")
    bargaining_powers = {}
    for asset in market_data['asset']:
        bargaining_powers[asset] = model.calculate_bargaining_power(asset)
    
    plt.figure(figsize=(12, 6))
    plt.bar(bargaining_powers.keys(), bargaining_powers.values())
    plt.title('Poder de Barganha por Ativo')
    plt.xticks(rotation=45)
    plt.ylabel('Poder de Barganha')
    plt.tight_layout()
    plt.savefig('bargaining_power.png')
    plt.close()
    
    # 9. Análise de Carteiras
    print("\n9. Analisando carteiras...")
    portfolios = data_generator.generate_portfolio_data(num_portfolios=3)
    
    for i, portfolio in enumerate(portfolios, 1):
        value = model.calculate_portfolio_value(portfolio)
        print(f"\nCarteira {i}:")
        print("Composição:")
        for asset, amount in portfolio.items():
            print(f"  {asset}: {amount:,.2f}")
        print(f"Valor total: {value:,.2f}")
    
    # 10. Visualização dos Vetores de Ativos
    print("\n10. Visualizando vetores de ativos...")
    selected_assets = market_data['asset'].iloc[:3].tolist()
    
    asset_vectors = {}
    for asset in selected_assets:
        asset_vectors[asset] = model.get_asset_vector(asset)
    
    vector_data = []
    for asset, vector in asset_vectors.items():
        vector_data.append({
            'asset': asset,
            'liquidez': vector[0],
            'volume': vector[1],
            'impacto_preco': vector[2],
            'permutas': vector[3],
            'utilidade': vector[4],
            'confianca': vector[5]
        })
    
    vector_df = pd.DataFrame(vector_data)
    print("\nVetores de Ativos:")
    print(vector_df)
    
    plt.figure(figsize=(12, 6))
    vector_df.set_index('asset').plot(kind='bar', width=0.8)
    plt.title('Vetores de Ativos')
    plt.ylabel('Valor')
    plt.xlabel('Ativo')
    plt.legend(title='Componente')
    plt.tight_layout()
    plt.savefig('asset_vectors.png')
    plt.close()

if __name__ == '__main__':
    main() 