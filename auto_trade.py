import settings
from binance.client import Client
from binance.enums import *
import time

client = Client(settings.API_KEY, settings.SECRET_KEY)
ticker = client.get_ticker(symbol='BTCUSDT')


hold_amount = 0.0
BUY_UNIT = 0.005
INTERVAL = 60
buy_price = 0
THRESHOLD = 0.005
orderId = None

while True:
    try:
        ticker = client.get_ticker(symbol='BTCUSDT')
        bidPrice = float(ticker['bidPrice'])
        askPrice = float(ticker['askPrice'])
        
        print(buy_price, bidPrice, askPrice)

        # buy by market price if don't have token
        if orderId is None and hold_amount == 0.0:
            res = client.create_order(
                symbol="BTCUSDT",
                side=SIDE_BUY,
                type=ORDER_TYPE_MARKET,
                quantity=BUY_UNIT,
            )
            orderId = res['orderId']
            buy_price = askPrice
            hold_amount = BUY_UNIT
            print('-- buy --')
            print(res)
        
        elif hold_amount:
            # sell by market price if the price difference over than threshold
            if bidPrice >= buy_price * (1 + THRESHOLD) or bidPrice <= buy_price * (1 - THRESHOLD):
                res = client.create_order(
                    symbol="BTCUSDT",
                    side=SIDE_SELL,
                    type=ORDER_TYPE_MARKET,
                    quantity=hold_amount,
                )
                hold_amount = 0.0
                orderId = None
                print('-- sell --')
                print(res)

    except Exception as e:
        print(e)

    time.sleep(INTERVAL)

    