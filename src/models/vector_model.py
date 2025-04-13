import numpy as np
from typing import Dict, List, Tuple, Optional
import networkx as nx
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class SwapRoute:
    """Representa uma rota de swap entre dois ativos."""
    path: List[str]
    total_cost: float
    effective_rate: float
    liquidity: float

class VectorialEconomicModel:
    """
    Modelo de análise econômica vetorial para avaliação de carteiras de ativos em DeFi.
    """
    
    def __init__(self):
        # Grafo direcionado para representar as pools de liquidez
        self.liquidity_graph = nx.DiGraph()
        # Dicionário para armazenar informações dos ativos
        self.assets = {}
        # Cache para rotas de swap
        self.route_cache = {}
        
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
            'exchange_routes': [],
            'volume': 0.0,
            'price_impact': 0.0,
            'utility': 0.0,
            'confidence': 0.0
        }
        
    def add_liquidity_pool(self, asset_a: str, asset_b: str, liquidity: float, 
                          swap_fee: float = 0.003, slippage_model: str = 'linear'):
        """
        Adiciona uma pool de liquidez entre dois ativos.
        
        Args:
            asset_a: Primeiro ativo
            asset_b: Segundo ativo
            liquidity: Quantidade de liquidez na pool
            swap_fee: Taxa de swap da pool (padrão: 0.3%)
            slippage_model: Modelo de slippage ('linear', 'quadratic', 'constant')
        """
        if asset_a not in self.assets or asset_b not in self.assets:
            raise ValueError("Ativos não encontrados no modelo")
            
        # Adiciona arestas em ambas as direções
        self.liquidity_graph.add_edge(asset_a, asset_b, 
                                     weight=liquidity, 
                                     swap_fee=swap_fee,
                                     slippage_model=slippage_model)
        self.liquidity_graph.add_edge(asset_b, asset_a, 
                                     weight=liquidity, 
                                     swap_fee=swap_fee,
                                     slippage_model=slippage_model)
        
        # Atualiza as rotas de troca para ambos os ativos
        if asset_b not in self.assets[asset_a]['exchange_routes']:
            self.assets[asset_a]['exchange_routes'].append(asset_b)
        if asset_a not in self.assets[asset_b]['exchange_routes']:
            self.assets[asset_b]['exchange_routes'].append(asset_a)
            
        # Limpa o cache de rotas
        self.route_cache = {}
        
    def calculate_slippage(self, asset_a: str, asset_b: str, amount: float) -> float:
        """
        Calcula o slippage para uma troca entre dois ativos.
        
        Args:
            asset_a: Ativo de origem
            asset_b: Ativo de destino
            amount: Quantidade a ser trocada
            
        Returns:
            float: Slippage estimado
        """
        if asset_a not in self.assets or asset_b not in self.assets:
            raise ValueError("Ativos não encontrados no modelo")
            
        if not self.liquidity_graph.has_edge(asset_a, asset_b):
            return float('inf')  # Sem liquidez direta
            
        liquidity = self.liquidity_graph[asset_a][asset_b]['weight']
        slippage_model = self.liquidity_graph[asset_a][asset_b]['slippage_model']
        
        # Diferentes modelos de slippage
        if slippage_model == 'linear':
            return (amount / liquidity) * 0.5  # Modelo linear simples
        elif slippage_model == 'quadratic':
            return (amount / liquidity) ** 2  # Modelo quadrático
        elif slippage_model == 'constant':
            return 0.01  # Slippage constante de 1%
        else:
            return 0.0  # Sem slippage
            
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
            
        # Verifica se existe liquidez direta
        if self.liquidity_graph.has_edge(asset_a, asset_b):
            return self.liquidity_graph[asset_a][asset_b]['weight']
            
        try:
            # Encontra todas as rotas possíveis
            paths = list(nx.all_simple_paths(self.liquidity_graph, asset_a, asset_b))
            total_liquidity = 0.0
            
            for path in paths:
                # A liquidez da rota é o mínimo de liquidez entre as arestas
                path_liquidity = float('inf')
                for i in range(len(path) - 1):
                    edge_liquidity = self.liquidity_graph[path[i]][path[i+1]]['weight']
                    path_liquidity = min(path_liquidity, edge_liquidity)
                total_liquidity += path_liquidity
                
            return total_liquidity
        except nx.NetworkXNoPath:
            return 0.0
            
    def find_best_swap_route(self, asset_a: str, asset_b: str, amount: float) -> Optional[SwapRoute]:
        """
        Encontra a melhor rota de swap entre dois ativos.
        
        Args:
            asset_a: Ativo de origem
            asset_b: Ativo de destino
            amount: Quantidade a ser trocada
            
        Returns:
            Optional[SwapRoute]: A melhor rota de swap ou None se não existir rota
        """
        if asset_a not in self.assets or asset_b not in self.assets:
            raise ValueError("Ativos não encontrados no modelo")
            
        # Verifica o cache
        cache_key = f"{asset_a}_{asset_b}_{amount}"
        if cache_key in self.route_cache:
            return self.route_cache[cache_key]
            
        # Verifica se existe rota direta
        if self.liquidity_graph.has_edge(asset_a, asset_b):
            liquidity = self.liquidity_graph[asset_a][asset_b]['weight']
            swap_fee = self.liquidity_graph[asset_a][asset_b]['swap_fee']
            slippage = self.calculate_slippage(asset_a, asset_b, amount)
            
            if amount <= liquidity:
                total_cost = swap_fee + slippage
                route = SwapRoute(
                    path=[asset_a, asset_b],
                    total_cost=total_cost,
                    effective_rate=total_cost,
                    liquidity=liquidity
                )
                self.route_cache[cache_key] = route
                return route
                
        # Encontra a melhor rota indireta usando Dijkstra modificado
        try:
            # Inicializa estruturas de dados
            costs = {node: float('inf') for node in self.liquidity_graph.nodes()}
            costs[asset_a] = 0
            predecessors = {node: None for node in self.liquidity_graph.nodes()}
            visited = set()
            
            # Algoritmo de Dijkstra modificado
            while len(visited) < len(self.liquidity_graph.nodes()):
                # Encontra o vértice não visitado com menor custo
                current = min((node for node in self.liquidity_graph.nodes() if node not in visited), 
                             key=lambda x: costs[x])
                
                if current == asset_b:
                    break
                    
                visited.add(current)
                
                # Atualiza os custos para os vizinhos
                for neighbor in self.liquidity_graph.neighbors(current):
                    if neighbor in visited:
                        continue
                        
                    # Calcula o custo de swap
                    liquidity = self.liquidity_graph[current][neighbor]['weight']
                    swap_fee = self.liquidity_graph[current][neighbor]['swap_fee']
                    
                    # Se a quantidade é maior que a liquidez, o custo é infinito
                    if amount > liquidity:
                        edge_cost = float('inf')
                    else:
                        slippage = self.calculate_slippage(current, neighbor, amount)
                        edge_cost = swap_fee + slippage
                        
                    new_cost = costs[current] + edge_cost
                    if new_cost < costs[neighbor]:
                        costs[neighbor] = new_cost
                        predecessors[neighbor] = current
                        
            # Reconstrói a rota
            if costs[asset_b] == float('inf'):
                self.route_cache[cache_key] = None
                return None
                
            path = []
            current = asset_b
            while current is not None:
                path.insert(0, current)
                current = predecessors[current]
                
            # Calcula a liquidez efetiva da rota
            route_liquidity = float('inf')
            for i in range(len(path) - 1):
                edge_liquidity = self.liquidity_graph[path[i]][path[i+1]]['weight']
                route_liquidity = min(route_liquidity, edge_liquidity)
                
            # Calcula a taxa efetiva
            effective_rate = self.calculate_effective_rate(path, amount)
            
            route = SwapRoute(
                path=path,
                total_cost=costs[asset_b],
                effective_rate=effective_rate,
                liquidity=route_liquidity
            )
            
            self.route_cache[cache_key] = route
            return route
            
        except Exception as e:
            print(f"Erro ao encontrar rota: {e}")
            return None
            
    def calculate_effective_rate(self, path: List[str], amount: float) -> float:
        """
        Calcula a taxa efetiva de swap em uma rota.
        
        Args:
            path: Lista de ativos na rota
            amount: Quantidade inicial a ser trocada
            
        Returns:
            float: Taxa efetiva total
        """
        total_rate = 0.0
        current_amount = amount
        
        for i in range(len(path) - 1):
            asset_a = path[i]
            asset_b = path[i+1]
            
            swap_fee = self.liquidity_graph[asset_a][asset_b]['swap_fee']
            slippage = self.calculate_slippage(asset_a, asset_b, current_amount)
            
            total_rate += swap_fee + slippage
            
            # Atualiza a quantidade para o próximo hop
            current_amount = current_amount * (1 - swap_fee - slippage)
            
        return total_rate
        
    def calculate_bargaining_power(self, asset_id: str) -> float:
        """
        Calcula o poder de barganha de um ativo baseado em sua liquidez e conexões.
        
        Args:
            asset_id: Identificador do ativo
            
        Returns:
            float: Poder de barganha do ativo
        """
        if asset_id not in self.assets:
            raise ValueError("Ativo não encontrado no modelo")
            
        direct_connections = len(list(self.liquidity_graph.neighbors(asset_id)))
        total_liquidity = sum(self.liquidity_graph[asset_id][neighbor]['weight'] 
                            for neighbor in self.liquidity_graph.neighbors(asset_id))
                            
        return (direct_connections * total_liquidity) / len(self.assets)
        
    def calculate_exchange_vector(self, asset_id: str) -> np.ndarray:
        """
        Calcula o vetor de permutas para um ativo.
        
        Args:
            asset_id: Identificador do ativo
            
        Returns:
            np.ndarray: Vetor de permutas [permutas_diretas, permutas_indiretas, eficiência, diversidade]
        """
        if asset_id not in self.assets:
            raise ValueError("Ativo não encontrado no modelo")
            
        # Número de permutas diretas
        direct_exchanges = len(self.assets[asset_id]['exchange_routes'])
        
        # Número de permutas indiretas (através de um intermediário)
        indirect_exchanges = 0
        for neighbor in self.liquidity_graph.neighbors(asset_id):
            for second_neighbor in self.liquidity_graph.neighbors(neighbor):
                if second_neighbor != asset_id and second_neighbor not in self.assets[asset_id]['exchange_routes']:
                    indirect_exchanges += 1
                    
        # Eficiência das rotas (média das taxas de swap)
        route_efficiency = 0.0
        if direct_exchanges > 0:
            efficiencies = []
            for neighbor in self.liquidity_graph.neighbors(asset_id):
                swap_fee = self.liquidity_graph[asset_id][neighbor]['swap_fee']
                efficiencies.append(1 - swap_fee)  # Quanto menor a taxa, maior a eficiência
            route_efficiency = sum(efficiencies) / len(efficiencies)
            
        # Diversidade de destinos (entropia da distribuição)
        # Simplificado para este exemplo
        diversity = direct_exchanges / len(self.assets)
        
        return np.array([direct_exchanges, indirect_exchanges, route_efficiency, diversity])
        
    def get_asset_vector(self, asset_id: str) -> np.ndarray:
        """
        Retorna o vetor representativo de um ativo.
        
        Args:
            asset_id: Identificador do ativo
            
        Returns:
            np.ndarray: Vetor [liquidez, volume, impacto_preço, permutas, utilidade, confiança]
        """
        if asset_id not in self.assets:
            raise ValueError("Ativo não encontrado no modelo")
            
        # Calcula os componentes do vetor
        liquidity = self.assets[asset_id]['liquidity']
        volume = self.assets[asset_id]['volume']
        price_impact = self.assets[asset_id]['price_impact']
        exchange_vector = self.calculate_exchange_vector(asset_id)
        utility = self.assets[asset_id]['utility']
        confidence = self.assets[asset_id]['confidence']
        
        # Combina os vetores
        return np.array([
            liquidity,
            volume,
            price_impact,
            np.mean(exchange_vector),  # Média do vetor de permutas
            utility,
            confidence
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
            if asset_id not in self.assets:
                raise ValueError(f"Ativo {asset_id} não encontrado no modelo")
                
            asset_vector = self.get_asset_vector(asset_id)
            # Normalização do vetor
            normalized_vector = asset_vector / np.linalg.norm(asset_vector)
            # Cálculo do valor ponderado
            total_value += quantity * np.sum(normalized_vector)
            
        return total_value
        
    def get_all_possible_routes(self, asset_a: str, asset_b: str, max_hops: int = 3) -> List[List[str]]:
        """
        Retorna todas as rotas possíveis entre dois ativos com um número máximo de hops.
        
        Args:
            asset_a: Ativo de origem
            asset_b: Ativo de destino
            max_hops: Número máximo de hops na rota
            
        Returns:
            List[List[str]]: Lista de rotas possíveis
        """
        if asset_a not in self.assets or asset_b not in self.assets:
            raise ValueError("Ativos não encontrados no modelo")
            
        try:
            # Encontra todas as rotas simples com no máximo max_hops+1 vértices
            paths = []
            for path in nx.all_simple_paths(self.liquidity_graph, asset_a, asset_b, cutoff=max_hops):
                paths.append(path)
            return paths
        except nx.NetworkXNoPath:
            return []
            
    def analyze_route_efficiency(self, asset_a: str, asset_b: str, amount: float) -> Dict[str, List[SwapRoute]]:
        """
        Analisa a eficiência de diferentes rotas entre dois ativos.
        
        Args:
            asset_a: Ativo de origem
            asset_b: Ativo de destino
            amount: Quantidade a ser trocada
            
        Returns:
            Dict[str, List[SwapRoute]]: Dicionário com rotas agrupadas por eficiência
        """
        if asset_a not in self.assets or asset_b not in self.assets:
            raise ValueError("Ativos não encontrados no modelo")
            
        # Encontra todas as rotas possíveis
        paths = self.get_all_possible_routes(asset_a, asset_b)
        
        # Calcula a eficiência de cada rota
        routes = []
        for path in paths:
            effective_rate = self.calculate_effective_rate(path, amount)
            
            # Calcula a liquidez efetiva da rota
            route_liquidity = float('inf')
            for i in range(len(path) - 1):
                edge_liquidity = self.liquidity_graph[path[i]][path[i+1]]['weight']
                route_liquidity = min(route_liquidity, edge_liquidity)
                
            route = SwapRoute(
                path=path,
                total_cost=effective_rate,
                effective_rate=effective_rate,
                liquidity=route_liquidity
            )
            routes.append(route)
            
        # Agrupa as rotas por eficiência
        result = {
            'most_efficient': [],
            'balanced': [],
            'highest_liquidity': []
        }
        
        if not routes:
            return result
            
        # Ordena por taxa efetiva (menor é melhor)
        routes_by_cost = sorted(routes, key=lambda x: x.effective_rate)
        result['most_efficient'] = routes_by_cost[:3]  # Top 3 mais eficientes
        
        # Ordena por liquidez (maior é melhor)
        routes_by_liquidity = sorted(routes, key=lambda x: x.liquidity, reverse=True)
        result['highest_liquidity'] = routes_by_liquidity[:3]  # Top 3 com maior liquidez
        
        # Rotas balanceadas (média entre eficiência e liquidez)
        if len(routes) > 3:
            # Normaliza custo e liquidez
            max_cost = max(r.effective_rate for r in routes)
            max_liquidity = max(r.liquidity for r in routes)
            
            # Calcula score balanceado (menor é melhor)
            for route in routes:
                normalized_cost = route.effective_rate / max_cost
                normalized_liquidity = 1 - (route.liquidity / max_liquidity)  # Inverte para que menor seja melhor
                route.balanced_score = (normalized_cost + normalized_liquidity) / 2
                
            # Ordena por score balanceado
            routes_by_balance = sorted(routes, key=lambda x: x.balanced_score)
            result['balanced'] = routes_by_balance[:3]  # Top 3 balanceados
            
        return result 