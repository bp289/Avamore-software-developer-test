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


#helper
calculate_annual_rate = lambda daily: (((1 + daily) ** 365) - 1) * 100
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

def calculate_initial_values(land_advance, contractual_monthly_rate, default_start, default_end):
    cur_date_str = DATE_OF_LOAN.strftime(DATE_FORMAT)

    result_dict = {
        'date': cur_date_str ,
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


    return result_dict

def calculate_next_values( contractual_monthly_rate, previous_values, default_start, default_end):
    current_date = datetime.strptime(previous_values['date'], DATE_FORMAT) + timedelta(days=1)
    cur_date_str = current_date.strftime(DATE_FORMAT)
    result_dict = {
        'date': cur_date_str,
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


    return result_dict

def ARM_calculations(
    land_advance,
    contractual_monthly_rate,
    default_period_start,
    default_period_end
):
    implied_daily_regular_rate = round(((contractual_monthly_rate/100)/ DAYS_IN_MONTH) * 100, 2)
    implied_daily_default_rate = round(((DEFAULT_RATE/100) / DAYS_IN_MONTH) * 100, 2)
    implied_regular_annual_rate = round(calculate_annual_rate((contractual_monthly_rate/100)/ DAYS_IN_MONTH), 1)
   


    default_start_DT = datetime.strptime(default_period_start , DATE_FORMAT)
    default_end_DT = datetime.strptime(default_period_end , DATE_FORMAT)

    current_values = calculate_initial_values(
        land_advance,
        contractual_monthly_rate,
        default_start_DT, 
        default_end_DT 
    )
    
    total_interest_due = current_values['accrued_daily_interest']
    
    table = [current_values]
    while datetime.strptime(current_values['date'],  DATE_FORMAT) < REDEMPTION_STATEMENT_DATE:
        current_values = calculate_next_values(
            contractual_monthly_rate,
            current_values,  
            default_start_DT, 
            default_end_DT
        )
        total_interest_due = max(total_interest_due, current_values['accrued_daily_interest'])
    
    return {
        'total_interest_due': round(total_interest_due, 2), 
        'daily_data': table , 
        "implied_daily_default_rate": implied_daily_default_rate, 
        "implied_daily_regular_rate": implied_daily_regular_rate,
        "implied_regular_annual_rate": implied_regular_annual_rate
    }

# input validations:
def validate_positive_float(inputVal):
        try:
            float_val = float(inputVal)
            if float_val > 0:
                return float_val
            else:
                print("Value must be a positive float.")
                return None
        except ValueError:
            print("Invalid input. Please enter a valid float.")
            return None

def validate_date_format(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return date_str
    except ValueError:
        print("Invalid input. Please enter a valid date format.")
        return None

def validate_date_range(start_date, end_date):
    valid = datetime.strptime(start_date, '%Y-%m-%d') <= datetime.strptime(end_date,'%Y-%m-%d')
    if(not valid):
       print('start date needs to be before end date')
       return None
    else:
        return end_date

def validate_inputs():
    land_advance = None;
    while land_advance == None:
        land_advance = validate_positive_float(
            input('enter land advance: ')
        )
    
    contractual_monthly_rate = None
    while contractual_monthly_rate == None:
        contractual_monthly_rate = validate_positive_float(
            input('enter contractual monthly rate (%) ')
        )

    default_period_start = None
    while default_period_start  == None:
        default_period_start = validate_date_format(
            input('enter default period start date in format "YYYY-MM-DD: ')
        )

    default_period_end = None
    while default_period_end == None:
        end_date = validate_date_format(
            input('enter default period end date in format "YYYY-MM-DD: ')
        )
        if end_date == None:
           continue
        default_period_end = validate_date_range(default_period_start, end_date)

    return(land_advance, contractual_monthly_rate, default_period_start, default_period_end)

if __name__ == '__main__':
   land_advance, contractual_monthly_rate, default_period_start, default_period_end = validate_inputs()
   output =ARM_calculations(
       land_advance, 
       contractual_monthly_rate, 
       default_period_start, 
       default_period_end)
   print(f"total_interest_due: {output["total_interest_due"]}")
   print(f"implied_daily_default_rate: {output["implied_daily_default_rate"]} ")
   print(f"implied_daily_regular_rate: {output["implied_daily_regular_rate"]}")
   print(f"implied_regular_annual_rate: {output["implied_regular_annual_rate"]}")
   

    
