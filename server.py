from flask import Flask, render_template, request, jsonify
from arm_script import ARM_calculations
from decimal import Decimal
import mimetypes
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ARMresult", methods =['POST'])
def ARM_result():
   data = request.json

   if data['input'] is not None:
    data = data['input']

    result = ARM_calculations(
        Decimal(data['land-advance']), 
        Decimal(data['contractual-monthly-rate']),
        data['beginning-of-default-period'], 
        data['end-of-default-period'])
   return jsonify( result )



    