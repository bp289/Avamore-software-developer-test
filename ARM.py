from datetime import datetime, timedelta

#constants
DATE_FORMAT = '%Y-%m-%d'

DAYS_IN_MONTH = 30
ARRANGEMENT_FEE = 5000
INTEREST_RETENTION = 20000
DEFAULT_RATE = 2
DATE_OF_LOAN = datetime.strptime("2023-01-15" , DATE_FORMAT)
REDEMPTION_STATEMENT_DATE = datetime.strptime("2024-04-23" , DATE_FORMAT)

BUILD_DRAW_DOWNS = {
    "2023-02-14": 25000,
    "2023-03-25": 25000,
    "2023-05-03": 25000,
    "2023-06-11": 25000,
    "2023-07-20": 25000,
    "2023-08-28": 25000,
    "2023-10-06": 25000,
    "2023-11-14": 25000,
    "2023-12-23": 25000,
    "2024-01-31": 25000
}
CAPITAL_REPAYMENTS = {
    "2024-02-23": 100000
}


def calculate_initial_values(land_advance, contractual_monthly_rate, default_start, default_end):
    cur_date_str = DATE_OF_LOAN.strftime(DATE_FORMAT)

    result_dict = {
        'date': DATE_OF_LOAN,
        'opening_PB': land_advance + ARRANGEMENT_FEE,
        'interest_balance': INTEREST_RETENTION,
        'default_on': default_start <= DATE_OF_LOAN <= default_end,
        'draw_down': BUILD_DRAW_DOWNS.get(cur_date_str, 0),
        'payments_received': CAPITAL_REPAYMENTS.get( cur_date_str, 0),
    }

    result_dict['daily_interest'] = get_daily_interest(
        result_dict['opening_PB'], 
        result_dict['draw_down'],
        result_dict['interest_balance'],
        result_dict['default_on'],
        contractual_monthly_rate
    )
    
    result_dict['closing_PB'] =  (result_dict['opening_PB'] + result_dict['draw_down']) - result_dict['payments_received']
    result_dict['accrued_daily_interest'] = result_dict['daily_interest']

    print(
    "date", cur_date_str,
    "opening_pb", result_dict['opening_PB'],
    "Ibalance:", result_dict['interest_balance'],
    "daily interest:", result_dict['daily_interest'],
    "drawdown", result_dict['draw_down'],
    "closing_PB", result_dict['closing_PB'],
    "accrued_daily_interest", result_dict['accrued_daily_interest'],
    "default_on", result_dict['default_on']
    )


    return result_dict

def calculate_next_values( contractual_monthly_rate, previous_values, default_start, default_end):
    current_date = previous_values['date'] + timedelta(days=1)
    cur_date_str = current_date.strftime(DATE_FORMAT)
    result_dict = {
        'date': current_date,
        'opening_PB': previous_values['closing_PB'],
        'interest_balance': max(INTEREST_RETENTION, previous_values['accrued_daily_interest']),
        'default_on': default_start <= current_date <= default_end,
        'draw_down': BUILD_DRAW_DOWNS.get(cur_date_str, 0),
        'payments_received': CAPITAL_REPAYMENTS.get( cur_date_str, 0),
    }

    
    result_dict['closing_PB'] =  (result_dict['opening_PB'] + result_dict['draw_down']) - result_dict['payments_received']
   
    daily_interest = get_daily_interest(
        result_dict['opening_PB'], 
        result_dict['draw_down'],
        result_dict['interest_balance'],
        result_dict['default_on'],
       contractual_monthly_rate
    )


    result_dict['closing_PB'] =  (result_dict['opening_PB'] + result_dict['draw_down']) - result_dict['payments_received']
    result_dict['daily_interest'] = daily_interest
    result_dict['accrued_daily_interest'] =  previous_values['accrued_daily_interest'] +  daily_interest

    print(
    "date", cur_date_str,
    "opening_pb", result_dict['opening_PB'],
    "Ibalance:", result_dict['interest_balance'],
    "daily interest:", result_dict['daily_interest'],
    "drawdown", result_dict['draw_down'],
    "closing_PB", result_dict['closing_PB'],
    "accrued_daily_interest", result_dict['accrued_daily_interest'],
    "default_on", result_dict['default_on']
    )


    return result_dict

def get_daily_interest(
    opening_PB, 
    draw_down,
    interest_balance, 
    default_on, 
    contractual_monthly_rate
):
    result = opening_PB + draw_down + interest_balance
    if default_on:
        return result * ((DEFAULT_RATE/ 100)/ DAYS_IN_MONTH )
    else:
        return result * ((contractual_monthly_rate/100)/ DAYS_IN_MONTH)

def ARM_calculations(land_advance= 100000, contractual_monthly_rate= 0.8, default_period_start = '2024-03-24', default_period_end = '2024-04-23'):

    implied_daily_regular_rate = round(contractual_monthly_rate/ DAYS_IN_MONTH, 2)
    implied_daily_default_rate = round(DEFAULT_RATE / DAYS_IN_MONTH, 2)

    default_start_DT = datetime.strptime(default_period_start , DATE_FORMAT)
    default_end_DT = datetime.strptime(default_period_end , DATE_FORMAT)

    current_values =  calculate_initial_values(land_advance, contractual_monthly_rate, default_start_DT, default_end_DT )
    while current_values['date'] < REDEMPTION_STATEMENT_DATE:
        current_values = calculate_next_values(contractual_monthly_rate, current_values,  default_start_DT, default_end_DT)
    
    return 0


ARM_calculations()


