from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ARMresult", methods =['POST'])
def ARMresult():
   data = request.json
   return jsonify({ "data": "success" })

 
