from dataclasses import dataclass, field
from typing import Optional

@dataclass
class BuyerProfile:
    annual_income: float
    down_payment: float
    monthly_student_loans: float = 0.0
    monthly_other_debts: float = 0.0

    def __post_init__(self) -> None:
        if self.annual_income < 0:
            raise ValueError('Annual income can\'t be negative!')
        if self.down_payment < 0:
            raise ValueError('Down payment can\'t be negative!')
        if self.monthly_student_loans < 0 or self.monthly_other_debts < 0:
            raise ValueError('Monthly debt obhligations can\'t be negative!')

    @property
    def monthly_income(self) -> float:
        return self.annual_income / 12

    @property
    def total_debts(self) -> float:
        return self.monthly_student_loans + self.monthly_other_debts

@dataclass
class MarketConditions:
    interest_rate: float
    property_tax_rate: float
    annual_insurance_rate: float = 0.005
    loan_term_years: int = 30
    pmi_rate: float = 0.0075
    front_end_dti_limit: float = 0.28
    back_end_dti_limit: float = 0.36

    def __post_init__(self) -> None:
        if self.interest_rate > 1:
            self.interest_rate /= 100
        if self.property_tax_rate > 1:
            self.property_tax_rate /= 100
        if self.annual_insurance_rate > 1:
            self.annual_insurance_rate /= 100
        if self.pmi_rate > 1:
            self.pmi_rate /= 100
        if self.front_end_dti_limit > 1:
            self.front_end_dti_limit /= 100
        if self.back_end_dti_limit > 1:
            self.back_end_dti_limit /= 100

        if self.interest_rate < 0:
            raise ValueError('Interest must be greater than 0!')
        if self.loan_term_years <= 0:
            raise ValueError('Loan term must be a positive integer!')

    @property
    def monthly_interest_rate(self) -> float:
        return self.interest_rate / 12

    @property
    def total_payment_months(self) -> int:
        return self.loan_term_years * 12

@dataclass
class Property:
    price: float
    hoa_monthly_fee: float = 0.0

    def __post_init__(self) -> None:
        if self.price <= 0:
            raise ValueError('House price must be greaqter than 0!')
        if self.hoa_monthly_fee < 0:
            raise ValueError('Hoa fee must not be negative!')

@dataclass
class AffordabilityResult:
    max_affordable_price: float
    max_monthly_piti: float
    monthly_principal_interest: float
    monthly_property_tax: float
    monthly_insurance: float
    monthly_pmi: float
    actual_front_end_dti: float
    actual_back_end_dti: float
    limiting_factor: str