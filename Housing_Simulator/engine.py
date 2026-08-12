from models import BuyerProfile, MarketConditions, Property, AffordabilityResult

# Forward Calculator (PITI for a specific home)
def calculate_piti(buyer: BuyerProfile, market: MarketConditions, property: Property) -> dict:
    loan_amount = property.price - buyer.down_payment

    if loan_amount < 0:
        loan_amount = 0

    # Calculate principal and interest

    if loan_amount == 0:
        monthly_pi = 0
    elif market.interest_rate == 0:
        monthly_pi = loan_amount / market.total_payment_months
    else:
        r = market.monthly_interest_rate
        n = market.total_payment_months
        #monthly_pi = loan_amount * (r(1 + r)^n) / (1 + r)^n - 1
        monthly_pi = loan_amount * (r * (1 + r)**n) / ((1 + r)**n - 1)

    # Monthly property taxes and insurance
    monthly_tax = (property.price * market.property_tax_rate) / 12
    monthly_insurance = (property.price * market.annual_insurance_rate) / 12

    # Private mortgage insurance
    down_payment_percent = (buyer.down_payment / property.price if property.price > 0 else 0.0)
    if down_payment_percent < 0.2 and loan_amount > 0:
        monthly_pmi = (loan_amount * market.pmi_rate) / 12
    else:
        monthly_pmi = 0

    # Total housing monthly cost
    total_piti = monthly_pi + monthly_tax + monthly_insurance + monthly_pmi + property.hoa_monthly_fee

    # Calculate DTI (debt-to-income) ratios
    if buyer.monthly_income == 0:
        raise ValueError('Monthly income can\'t be 0!')

    front_end_dti = total_piti / buyer.monthly_income
    back_end_dti = (total_piti + buyer.total_debts) / buyer.monthly_income

    # Return all info
    info = {
        'pi': monthly_pi,
        'tax': monthly_tax,
        'insurance': monthly_insurance,
        'pmi': monthly_pmi,
        'piti': total_piti,
        'fdti': front_end_dti,
        'bdti': back_end_dti
    }
    return info

def get_max_housing_budget(buyer: BuyerProfile, market: MarketConditions) -> tuple[float, str]:
    front_end_housing_cap = buyer.monthly_income * market.front_end_dti_limit
    back_end_housing_cap = (buyer.monthly_income * market.back_end_dti_limit) - buyer.total_debts

    if front_end_housing_cap < back_end_housing_cap:
        max_piti_budget = front_end_housing_cap
        limiting_factor = 'Front-End DTI Limit'
    else:
        max_piti_budget = back_end_housing_cap
        limiting_factor = 'Back-End DTI Limit'

    if max_piti_budget < 0:
        max_piti_budget = 0

    return (max_piti_budget, limiting_factor)

def calculate_max_affordability(buyer: BuyerProfile, market: MarketConditions) -> AffordabilityResult:
    (max_piti_budget, limiting_factor) = get_max_housing_budget(buyer, market)
    if max_piti_budget <= 0:
        return AffordabilityResult(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, limiting_factor)

    low = buyer.down_payment
    high = 10_000_000.0
    tolerance = 0.01

    while (high-low) > tolerance:
        midpoint = (low + high) / 2
        test_property = Property(midpoint)
        test_calculation = calculate_piti(buyer, market, test_property)
        if test_calculation['piti'] > max_piti_budget:
            high = midpoint
        else:
            low = midpoint

    property = Property(low)
    calculation = calculate_piti(buyer, market, property)

    return AffordabilityResult(
        max_affordable_price=low,
        max_monthly_piti=calculation['piti'],
        monthly_principal_interest=calculation['pi'],
        monthly_property_tax=calculation['tax'],
        monthly_insurance=calculation['insurance'],
        monthly_pmi=calculation['pmi'],
        actual_front_end_dti=calculation['fdti'],
        actual_back_end_dti=calculation['bdti'],
        limiting_factor=limiting_factor
    )
