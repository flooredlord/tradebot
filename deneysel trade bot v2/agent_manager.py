from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List


class AgentManager:
    """Runs multiple agents in parallel and aggregates their signals."""

    def __init__(self, agents: List[object]):
        self.agents = agents

    def _aggregate_signal(self, symbol: str) -> str:
        votes = [agent.get_signal(symbol) for agent in self.agents]
        buy = votes.count('BUY')
        sell = votes.count('SELL')
        if buy > sell:
            return 'BUY'
        if sell > buy:
            return 'SELL'
        return 'HOLD'

    def get_signals(self, symbols: List[str]) -> Dict[str, str]:
        results: Dict[str, str] = {}
        with ThreadPoolExecutor(max_workers=len(symbols)) as executor:
            future_to_symbol = {executor.submit(self._aggregate_signal, s): s for s in symbols}
            for future in future_to_symbol:
                symbol = future_to_symbol[future]
                try:
                    results[symbol] = future.result()
                except Exception:
                    results[symbol] = 'HOLD'
        return results
