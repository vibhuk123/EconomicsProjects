# Main app
from scenarios import get_default_market
from os import system
from time import sleep

default_market = get_default_market()

def show_main_menu():
    print("\n=================================================")
    print("=        Housing Affordability Simulator        =")
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

def main():
    simulation_running = True

    while simulation_running:
        show_main_menu()
        option = int(input('\nSelect an option: '))
        if option == 8:
            print('\nExiting...')
            sleep(1)
            simulation_running = False

    system('clear')
    print('SIMULATION OVER...')
    sleep(0.5)
    system('clear')

if __name__ == '__main__':
    main()