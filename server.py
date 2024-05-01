from flask import Flask, render_template, request, jsonify

import mimetypes
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')

DAYS_IN_MONTH = 30
ARRANGEMENT_FEE = 5000
INTEREST_RETENTION = 20000
DAILY_DEFAULT_RATE = 2

DATE_OF_LOAN = "15-Jan-23"

REDEMPTION_STATEMENT_DATE = "23-Apr-24"
BUILD_DRAWDOWNS = {
    "14-Feb-23": 25000,
    "25-Mar-23": 25000,
    "3-May-23": 25000,
    "11-Jun-23": 25000,
    "20-Jul-23": 25000,
    "28-Aug-23": 25000,
    "6-Oct-23": 25000,
    "14-Nov-23": 25000,
    "23-Dec-23": 25000,
    "31-Jan-24": 25000
}

CAPITAL_REPAYMENTS = {
    "23-Feb-24": 100000
}

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ARMresult", methods =['POST'])
def ARM_result():
   data = request.json
   return jsonify({ "data": "success" })

 

# def ARM_calculations(land_advance= 100000, contractual_monthly_rate=0.8, beginning_Of_default_period = 3/24/2024, end_Of_default_period = 4/23/2024):
#     implied_daily_regular_rate = round(contractual_monthly_rate / DAYS_IN_MONTH, 2)
#     implied_daily_default_rate = round(DAILY_DEFAULT_RATE / 30, 2)
    
#     return 0



# def getDailyInterest(opening_PB, draw_down, interest_balance, defaultOn, implied_daily_regular_rate, implied_daily_default_rate):
#     result = opening_PB + draw_down + interest_balance
#     if defaultOn:
#         return result * implied_daily_default_rate
#     else:
#         return result * implied_daily_regular_rate

    