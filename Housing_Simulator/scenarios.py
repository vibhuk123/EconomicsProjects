from models import BuyerProfile, MarketConditions, AffordabilityResult
from engine import calculate_max_affordability, calculate_piti

class ScenarioEngine:
    def __init__(self, default_market: MarketConditions | None = None, default_buyers: list[BuyerProfile] | None = None) -> None:
        self.default_market = default_market or get_default_market() 
        self.default_buyers = default_buyers or get_default_preset_buyers()

    def compare_buyer_profiles(self, buyers: list[BuyerProfile] | None = None, market: MarketConditions | None = None) -> list[AffordabilityResult]:
        if buyers is None:
            buyers = self.default_buyers
        if market is None:
            market = self.default_market

        results = []

        for buyer in buyers:
            calculation = calculate_max_affordability(buyer, market)
            results.append(calculation)

        return results

    def interest_rate_sweep(self, buyer: BuyerProfile, base_market: MarketConditions, min_rate: float, max_rate: float, step: float) -> list[dict]:
        pass 

    def run_debt_drag_analysis(self, buyer: BuyerProfile, market: MarketConditions, debt_levels: list[float]) -> list[dict]:
        pass

    def run_income_vs_rate_matrix(self, income_range: list[float], rate_range: list[float], down_payment: float, base_market: MarketConditions):
        pass 

def get_default_preset_buyers() -> list[BuyerProfile]:
    pass

def get_default_market() -> MarketConditions:
    pass