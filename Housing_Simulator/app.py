# Main app
from scenarios import get_default_market, get_default_preset_buyers
from models import BuyerProfile, MarketConditions, AffordabilityResult
from engine import calculate_max_affordability
import subprocess
from time import sleep

default_market = get_default_market()

def show_main_menu():
    subprocess.run('clear')
    print("\n=================================================")
    print("=        HOUSING AFFORDABILITY SIMULATOR        =")
    print("=================================================")
    print('\nCurrent Market')
    print(f'    Interest Rate: {default_market.interest_rate}')
    print(f'    Propert Tax: {round(default_market.property_tax_rate*100, 2)}%')
    print(f'    Loan Term: {default_market.loan_term_years} years')
    print(f'    Front-End DTI: {round(default_market.front_end_dti_limit*100, 2)}%')
    print(f'    Back-End DTI: {round(default_market.back_end_dti_limit*100, 2)}%')
    print('\nWhat would you like to do?')
    print('\n1. Analyze a buyer')
    print('2. Evaluate a specific property')
    print('3. Compare preset buyers')
    print('4. Interest rate analysis')
    print('5. Debt burden analysis')
    print('6. Income vs. interest rate analysis')
    print('7. Change market conditions')
    print('8. Exit')

# Option 1 Functions
def analyze_buyer():
    subprocess.run('clear')
    print('===============1. Analyze a buyer===============')
    buyer = get_buyer()
    if buyer is None:
        return
    market = get_market()
    if market is None:
        return

    result = calculate_max_affordability(buyer, market)
    display_affordability_results(buyer, market, result)

    input('\nPress Enter to return to the main menu...')

def get_buyer() -> BuyerProfile:
    subprocess.run('clear')
    buyers = get_default_preset_buyers()
    buyer = None

    while True:
        print('===============Choose Buyer===============')
        print('=                                        =')
        print('=    1. Typical Buyer                    =')
        print('=    2. Student Debt Buyer               =')
        print('=    3. High-Income Buyer                =')
        print('=    4. High-Debt Buyer                  =')
        print('=    5. Debt + Large Down Payment Buyer  =')
        print('=    6. Zero-Down Buyer                  =')
        print('=    7. Custom Buyer                     =')
        print('=    0. Back                             =')
        print('=                                        =')
        print('==========================================')

        choice = int(input('\nPick a buyer: '))

        if choice == 0:
            print('\nExiting buyer analyzer!')
            sleep(1)
            return None
        elif choice == 1:
            buyer = buyers[0]
            break
        elif choice == 2:
            buyer = buyers[1]
            break
        elif choice == 3:
            buyer = buyers[2]
            break
        elif choice == 4:
            buyer = buyers[3]
            break
        elif choice == 5:
            buyer = buyers[4]
            break
        elif choice == 6:
            buyer = buyers[5]
            break
        elif choice == 7:
            buyer = create_custom_buyer()
            break
        else:
            print('\nInvalid selection! Please choose one of the options available!')

    if buyer is not None:
        print(f'\nYou picked buyer: {buyer.name}, moving on to market selection!')
    sleep(2)
    return buyer

def create_custom_buyer() -> BuyerProfile:
    print('\n===============Create a custom buyer!===============')
    buyer_name = str(input('Enter buyer name: '))
    buyer_annual_income = float(input('Enter buyer\'s annual income: $'))
    buyer_down_payment = float(input('Enter buyer\'s down payment: $'))
    buyer_monthly_student_loans = float(input('Enter buyer\'s monthly student loan payment: $'))
    buyer_monthly_debts = float(input('Enter buyer\'s monthly debt payment: $'))

    custom_buyer = BuyerProfile(name=buyer_name, annual_income=buyer_annual_income, down_payment=buyer_down_payment, monthly_student_loans=buyer_monthly_student_loans, monthly_other_debts=buyer_monthly_debts)

    return custom_buyer

def get_market() -> MarketConditions:
    subprocess.run('clear')

    market = None

    while True:
        print('===============Choose a market===============')
        print('=                                           =')
        print('=    1. Default market                      =')
        print('=    2. Custom market                       =')
        print('=    0. Back                                =')
        print('=                                           =')
        print('=============================================')

        market_choice = int(input('\nPick a market: '))
        if market_choice == 0:
            print('\nExiting buyer analyzer!')
            sleep(1)
            return None
        elif market_choice == 1:
            market = get_default_market()
            break
        elif market_choice == 2:
            market = build_custom_market()
            break
        else:
            print('\nInvalid Selection! Please pick a valid selection!')

    return market

def build_custom_market() -> MarketConditions:
    print('\nCreate a custom market:\n')
    market_interest_rate = float(input('Interest Rate: '))
    market_property_tax_rate = float(input('Property Tax Rate: '))
    market_annual_insurance_rate = float(input('Annual Insurance Rate: '))
    market_loan_term_years = int(input('Loan Term Years: '))
    market_pmi_rate = float(input('PMI Rate: '))
    market_front_end_dti_limit = float(input('Front-End DTI Limit: '))
    market_back_end_dti_limit = float(input('Back-End DTI Limit: '))

    custom_market = MarketConditions(interest_rate=market_interest_rate, property_tax_rate=market_property_tax_rate, annual_insurance_rate=market_annual_insurance_rate, loan_term_years=market_loan_term_years, pmi_rate=market_pmi_rate, front_end_dti_limit=market_front_end_dti_limit, back_end_dti_limit=market_back_end_dti_limit)

    return custom_market

def display_affordability_results(buyer: BuyerProfile, market: MarketConditions, result: AffordabilityResult) -> None:
    subprocess.run('clear')
    print('=========================================')
    print('         AFFORDABILITY ANALYSIS          ')
    print('=========================================')
    print(f'\nBuyer: {buyer.name}\n')
    print('Buyer Information')
    print('-----------------------------------------')
    print(f'Annual Income:         ${buyer.annual_income}')
    print(f'Down Payment:          ${buyer.down_payment}')
    print(f'Student Loans:         ${buyer.monthly_student_loans}')
    print(f'Other Debt:            ${buyer.monthly_other_debts}')
    print('\nMarket Conditions\n')
    print(f'Interest Rate:          {market.interest_rate}%')
    print(f'Propert Tax:            {market.property_tax_rate}%')
    print(f'Loan Term:              {market.loan_term_years} years')

def evaluate_property():
    pass

def compare_buyers():
    pass

def analyze_interest_rate():
    pass

def analyze_debt_burden():
    pass

def analyze_income_vs_interest_rate():
    pass

def change_market_conditions():
    pass

def main():
    simulation_running = True

    while simulation_running:
        show_main_menu()
        option = int(input('\nSelect an option: '))
        if option == 1:
            print('\nStarting buyer analyzer...')
            sleep(0.5)
            analyze_buyer()
        elif option == 2:
            evaluate_property()
        elif option == 3:
            compare_buyers()
        elif option == 4:
            analyze_interest_rate()
        elif option == 5:
            analyze_debt_burden()
        elif option == 6:
            analyze_income_vs_interest_rate()
        elif option == 7:
            change_market_conditions()
        elif option == 8:
            print('\nExiting...')
            sleep(1)
            simulation_running = False
        else:
            print('\nInvalid selection! Please pick again!')
            sleep(1)

    subprocess.run('clear')
    print('SIMULATION OVER...')
    sleep(1)
    subprocess.run('clear')

if __name__ == '__main__':
    main()