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

    def interest_rate_sweep(self, start_rate: float, end_rate: float, step: float, buyer: BuyerProfile | None = None, market: MarketConditions | None = None) -> list[dict]:
        if buyer is None:
            buyer = get_default_preset_buyers()[0]
        if market is None:
            market = get_default_market()

        results = []
        current_rate = start_rate

        while current_rate <= end_rate + 1e-9:
            temp_market = MarketConditions(current_rate, market.property_tax_rate, market.annual_insurance_rate, market.loan_term_years)
            temp_calculation = calculate_max_affordability(buyer, temp_market)
            results.append(temp_calculation)

    def run_debt_drag_analysis(self, buyer: BuyerProfile, market: MarketConditions, debt_levels: list[float]) -> list[dict]:
        pass

    def run_income_vs_rate_matrix(self, income_range: list[float], rate_range: list[float], down_payment: float, base_market: MarketConditions):
        pass 

def get_default_preset_buyers() -> list[BuyerProfile]:
    pass

def get_default_market() -> MarketConditions:
    pass