import numpy as np
import pandas as pd
from typing import List, Dict, Tuple

class MockDataGenerator:
    """
    Gerador de dados mockados para teste do modelo vetorial.
    """
    
    def __init__(self, num_assets: int = 10):
        self.num_assets = num_assets
        self.assets = [f"TOKEN_{i}" for i in range(num_assets)]
        
    def generate_liquidity_data(self) -> pd.DataFrame:
        """
        Gera dados de liquidez mockados para as pools.
        
        Returns:
            pd.DataFrame: DataFrame com dados de liquidez
        """
        data = []
        
        for i in range(self.num_assets):
            for j in range(i + 1, self.num_assets):
                liquidity = np.random.uniform(1000, 1000000)
                data.append({
                    'token_a': self.assets[i],
                    'token_b': self.assets[j],
                    'liquidity': liquidity,
                    'volume_24h': liquidity * np.random.uniform(0.1, 0.5),
                    'fees_24h': liquidity * np.random.uniform(0.001, 0.003)
                })
                
        return pd.DataFrame(data)
        
    def generate_portfolio_data(self, num_portfolios: int = 5) -> List[Dict[str, float]]:
        """
        Gera carteiras mockadas com diferentes composições de ativos.
        
        Args:
            num_portfolios: Número de carteiras para gerar
            
        Returns:
            List[Dict[str, float]]: Lista de carteiras
        """
        portfolios = []
        
        for _ in range(num_portfolios):
            portfolio = {}
            total_assets = np.random.randint(3, self.num_assets + 1)
            selected_assets = np.random.choice(self.assets, total_assets, replace=False)
            
            for asset in selected_assets:
                portfolio[asset] = np.random.uniform(1, 1000)
                
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
            price = np.random.uniform(1, 1000)
            data.append({
                'asset': asset,
                'price': price,
                'market_cap': price * np.random.uniform(1000000, 100000000),
                'volume_24h': price * np.random.uniform(100000, 10000000),
                'price_change_24h': np.random.normal(0, 0.05),
                'liquidity_score': np.random.uniform(0, 1)
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
                    routes.append((this.assets[j], this.assets[i], cost))
                    
        return routes 