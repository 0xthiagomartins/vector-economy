import numpy as np
from typing import Dict, List, Tuple
import networkx as nx

class VectorialEconomicModel:
    """
    Modelo de análise econômica vetorial para avaliação de carteiras de ativos em DeFi.
    """
    
    def __init__(self):
        self.liquidity_graph = nx.DiGraph()
        self.assets = {}
        
    def add_asset(self, asset_id: str, initial_liquidity: float):
        """
        Adiciona um novo ativo ao modelo.
        
        Args:
            asset_id: Identificador único do ativo
            initial_liquidity: Liquidez inicial do ativo
        """
        self.assets[asset_id] = {
            'liquidity': initial_liquidity,
            'bargaining_power': 0.0,
            'exchange_routes': []
        }
        
    def add_liquidity_pool(self, asset_a: str, asset_b: str, liquidity: float):
        """
        Adiciona uma pool de liquidez entre dois ativos.
        
        Args:
            asset_a: Primeiro ativo
            asset_b: Segundo ativo
            liquidity: Quantidade de liquidez na pool
        """
        if asset_a not in self.assets or asset_b not in self.assets:
            raise ValueError("Ativos não encontrados no modelo")
            
        self.liquidity_graph.add_edge(asset_a, asset_b, weight=liquidity)
        self.liquidity_graph.add_edge(asset_b, asset_a, weight=liquidity)
        
    def calculate_indirect_liquidity(self, asset_a: str, asset_b: str) -> float:
        """
        Calcula a liquidez indireta entre dois ativos através de todas as rotas possíveis.
        
        Args:
            asset_a: Ativo de origem
            asset_b: Ativo de destino
            
        Returns:
            float: Liquidez indireta total
        """
        if asset_a not in self.assets or asset_b not in self.assets:
            raise ValueError("Ativos não encontrados no modelo")
            
        try:
            paths = list(nx.all_simple_paths(self.liquidity_graph, asset_a, asset_b))
            total_liquidity = 0.0
            
            for path in paths:
                path_liquidity = float('inf')
                for i in range(len(path) - 1):
                    edge_liquidity = self.liquidity_graph[path[i]][path[i+1]]['weight']
                    path_liquidity = min(path_liquidity, edge_liquidity)
                total_liquidity += path_liquidity
                
            return total_liquidity
        except nx.NetworkXNoPath:
            return 0.0
            
    def calculate_bargaining_power(self, asset_id: str) -> float:
        """
        Calcula o poder de barganha de um ativo baseado em sua liquidez e conexões.
        
        Args:
            asset_id: Identificador do ativo
            
        Returns:
            float: Poder de barganha do ativo
        """
        if asset_id not in this.assets:
            raise ValueError("Ativo não encontrado no modelo")
            
        direct_connections = len(list(this.liquidity_graph.neighbors(asset_id)))
        total_liquidity = sum(this.liquidity_graph[asset_id][neighbor]['weight'] 
                            for neighbor in this.liquidity_graph.neighbors(asset_id))
                            
        return (direct_connections * total_liquidity) / len(this.assets)
        
    def get_asset_vector(self, asset_id: str) -> np.ndarray:
        """
        Retorna o vetor representativo de um ativo.
        
        Args:
            asset_id: Identificador do ativo
            
        Returns:
            np.ndarray: Vetor [liquidez, poder_de_barganha, rotas_de_troca]
        """
        if asset_id not in this.assets:
            raise ValueError("Ativo não encontrado no modelo")
            
        bargaining_power = this.calculate_bargaining_power(asset_id)
        exchange_routes = len(list(this.liquidity_graph.neighbors(asset_id)))
        
        return np.array([
            this.assets[asset_id]['liquidity'],
            bargaining_power,
            exchange_routes
        ])
        
    def calculate_portfolio_value(self, portfolio: Dict[str, float]) -> float:
        """
        Calcula o valor total de uma carteira considerando todos os fatores.
        
        Args:
            portfolio: Dicionário com ativos e suas quantidades
            
        Returns:
            float: Valor total da carteira
        """
        total_value = 0.0
        
        for asset_id, quantity in portfolio.items():
            if asset_id not in this.assets:
                raise ValueError(f"Ativo {asset_id} não encontrado no modelo")
                
            asset_vector = this.get_asset_vector(asset_id)
            # Normalização do vetor
            normalized_vector = asset_vector / np.linalg.norm(asset_vector)
            # Cálculo do valor ponderado
            total_value += quantity * np.sum(normalized_vector)
            
        return total_value 