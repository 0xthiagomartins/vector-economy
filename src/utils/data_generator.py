import numpy as np
import pandas as pd
from typing import List, Dict, Tuple

class MockDataGenerator:
    """
    Gerador de dados mockados para teste do modelo vetorial.
    """
    
    def __init__(self, num_assets: int = 10, seed: int = 42):
        """
        Inicializa o gerador de dados.
        
        Args:
            num_assets: Número de ativos a serem gerados
            seed: Semente para reprodutibilidade
        """
        np.random.seed(seed)
        self.num_assets = num_assets
        self.assets = [f"TOKEN_{i}" for i in range(num_assets)]
        
    def generate_liquidity_data(self) -> pd.DataFrame:
        """
        Gera dados de liquidez mockados para as pools.
        
        Returns:
            pd.DataFrame: DataFrame com dados de liquidez
        """
        data = []
        
        # Gera pools entre alguns pares de ativos (não todos os pares possíveis)
        num_pools = int(self.num_assets * 1.5)  # Mais pools que ativos, mas não todos os pares
        
        for _ in range(num_pools):
            token_a, token_b = np.random.choice(self.assets, size=2, replace=False)
            liquidity = np.random.uniform(10000, 1000000)
            data.append({
                'token_a': token_a,
                'token_b': token_b,
                'liquidity': liquidity,
                'volume_24h': liquidity * np.random.uniform(0.1, 0.5),
                'fee_tier': np.random.choice([0.001, 0.003, 0.005])
            })
                
        return pd.DataFrame(data)
        
    def generate_portfolio_data(self, num_portfolios: int = 3) -> List[Dict[str, float]]:
        """
        Gera carteiras mockadas com diferentes composições de ativos.
        
        Args:
            num_portfolios: Número de carteiras a serem geradas
            
        Returns:
            Lista de dicionários representando as carteiras
        """
        portfolios = []
        
        for _ in range(num_portfolios):
            # Seleciona um subconjunto aleatório de ativos
            num_assets_in_portfolio = np.random.randint(2, self.num_assets)
            selected_assets = np.random.choice(self.assets, size=num_assets_in_portfolio, replace=False)
            
            # Gera pesos aleatórios e normaliza
            weights = np.random.dirichlet(np.ones(num_assets_in_portfolio))
            
            # Cria a carteira com valores entre 100 e 10000 para cada ativo
            portfolio = {}
            for asset, weight in zip(selected_assets, weights):
                portfolio[asset] = weight * np.random.uniform(100, 10000)
            
            portfolios.append(portfolio)
            
        return portfolios
        
    def generate_market_data(self) -> pd.DataFrame:
        """
        Gera dados de mercado mockados para os ativos.
        
        Returns:
            pd.DataFrame: DataFrame com dados de mercado
        """
        data = []
        
        for asset in self.assets:
            data.append({
                'asset': asset,
                'price': np.random.uniform(0.1, 1000),
                'volume_24h': np.random.uniform(10000, 1000000),
                'liquidity_score': np.random.uniform(0.1, 0.9),
                'market_cap': np.random.uniform(100000, 10000000)
            })
            
        return pd.DataFrame(data)
        
    def generate_trade_routes(self) -> List[Tuple[str, str, float]]:
        """
        Gera rotas de troca mockadas entre ativos.
        
        Returns:
            List[Tuple[str, str, float]]: Lista de rotas com seus custos
        """
        routes = []
        
        for i in range(self.num_assets):
            for j in range(i + 1, self.num_assets):
                if np.random.random() < 0.7:  # 70% de chance de ter rota direta
                    cost = np.random.uniform(0.001, 0.01)
                    routes.append((self.assets[i], self.assets[j], cost))
                    routes.append((self.assets[j], self.assets[i], cost))
                    
        return routes 