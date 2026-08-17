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
            buyer = self.default_buyers[0]
        if market is None:
            market = self.default_market

        results = []
        current_rate = start_rate

        while current_rate <= end_rate + 1e-9:
            temp_market = MarketConditions(current_rate, market.property_tax_rate, market.annual_insurance_rate, market.loan_term_years, market.pmi_rate, market.front_end_dti_limit, market.back_end_dti_limit)
            temp_calculation = calculate_max_affordability(buyer, temp_market)
            temp_dict = {
                'interest_rate': round(current_rate, 4),
                'max_affordable_price': round(temp_calculation.max_affordable_price, 2),
                'max_monthly_piti': round(temp_calculation.max_monthly_piti, 2),
                'monthly_principal_interest': round(temp_calculation.monthly_principal_interest, 2),
                'limiting_factor': temp_calculation.limiting_factor
            }
            results.append(temp_dict)
            current_rate += step

        return results

    def run_debt_drag_analysis(self, start_debt: float, end_debt: float, step: float, buyer: BuyerProfile | None = None, market: MarketConditions | None = None) -> list[dict]:
        if buyer is None:
            buyer = self.default_buyers[0]
        if market is None:
            market = self.default_market

        results = []
        current_debt = start_debt

        baseline_buyer = BuyerProfile(buyer.annual_income, buyer.down_payment, buyer.monthly_student_loans, 0)

        while current_debt <= end_debt + 1e-9:
            temp_buyer = BuyerProfile('temp buyer', buyer.annual_income, buyer.down_payment, buyer.monthly_student_loans, current_debt)
            temp_calculation = calculate_max_affordability(temp_buyer, market)
            baseline_calculation = calculate_max_affordability(baseline_buyer, market)
            baseline_price = baseline_calculation.max_affordable_price

            temp_dict = {
                'monthly_debt': round(current_debt, 2),
                'max_affordable_price': round(temp_calculation.max_affordable_price, 2),
                'max_monthly_piti': temp_calculation.max_monthly_piti,
                'limiting_factor': temp_calculation.limiting_factor,
                'purchasing_power_lost': round(baseline_price - temp_calculation.max_affordable_price, 2)
            }

            results.append(temp_dict)
            current_debt += step

        return results

    def run_income_vs_rate_matrix(self, incomes: list[float], rates: list[float], buyer: BuyerProfile | None = None, market: MarketConditions | None = None) -> list[dict]:
        if buyer is None:
            buyer = self.default_buyers[0]
        if market is None:
            market = self.default_market

        result = []

        for income in incomes:
            for rate in rates:
                temp_buyer = BuyerProfile('temp buyer', income, buyer.down_payment, buyer.monthly_student_loans, buyer.monthly_other_debts)
                temp_market = MarketConditions(rate, market.property_tax_rate, market.annual_insurance_rate, market.loan_term_years, market.pmi_rate, market.front_end_dti_limit, market.back_end_dti_limit)
                temp_result = calculate_max_affordability(temp_buyer, temp_market)
                temp_dict = {
                    'annual_income': income,
                    'interest_rate': round(rate, 4),
                    'max_affordable_price': round(temp_result.max_affordable_price, 2),
                    'limiting_factor': temp_result.limiting_factor
                }
                result.append(temp_dict)

        return result

# Get a default list of buyers of different types
def get_default_preset_buyers() -> list[BuyerProfile]:
    default_buyers = [
        BuyerProfile(
            name='Typical Buyer',
            annual_income=120_000,
            down_payment=60_000
        ),
        BuyerProfile(
            name='Student Debt Buyer',
            annual_income=65_000,
            down_payment=15_000,
            monthly_student_loans=500
        ),
        BuyerProfile(
            name='High-Income Buyer',
            annual_income=200_000,
            down_payment=150_000,
            monthly_other_debts=800
        ),
        BuyerProfile(
            name='High-Debt Buyer',
            annual_income=45_000,
            down_payment=5_000,
            monthly_student_loans=750,
            monthly_other_debts=300
        ),
        BuyerProfile(
            name='Debt + Large Down Payment Buyer',
            annual_income=90_000,
            down_payment=100_000,
            monthly_student_loans=750,
            monthly_other_debts=300
        ),
        BuyerProfile(
            name='Zero-Down Buyer',
            annual_income=75_000,
            down_payment=0
        )
    ]

    return default_buyers

def get_default_market() -> MarketConditions:
    default_market = MarketConditions(
        interest_rate=6.5,
        property_tax_rate=1.1,
        annual_insurance_rate=0.005,
        loan_term_years=30,
        pmi_rate=0.0075,
        front_end_dti_limit=28,
        back_end_dti_limit=36
    )

    return default_market