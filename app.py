from flask import Flask, render_template,request, flash,redirect,jsonify
import config,csv
from binance.client import Client
from binance.enums import *
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS']= 'Content-Type'

client = Client(config.API_KEY, config.API_SECRET)
app.secret_key = b'jbdhjabdabsjdbajhwbdajqwd213[d'
@app.route('/')
@cross_origin()
def hello_world():
    title = 'Scanner'
    account = client.get_account()
    balances = account["balances"]
    ex_info = client.get_exchange_info()
    symbols= ex_info['symbols']
    
    return render_template('index.html',title=title,my_balances=balances,symbols=symbols)

@app.route('/buy',methods=['POST'])
def buy():
    try:
        order = client.create_order(
            symbol=request.form['symbol'],
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quantity=request.form['quantity']
        )
    except Exception as e:
        flash(e.message, "error")

    return redirect('/')

@app.route('/sell')
def sell():
    return 'sell'

@app.route('/settings')
def settings():
    return 'settings'

@app.route('/history')
def history():
    candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_5MINUTE, "1 Dec, 2020", "14 Dec, 2020")

    processed_candles = []
    for i in candlesticks:
        candle = {
            "time":i[0]/1000,
            "open":i[1],
            "high":i[2],
            "low":i[3],
            "close":i[4],
        }
        processed_candles.append(candle)
    return jsonify(processed_candles)
