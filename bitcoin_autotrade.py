import time
import pyupbit
import datetime
import schedule
from fbprophet import Prophet
import json

access = "----------------------"
secret = "----------------------"

def sell_all(coin) :
    balance = upbit.get_balance(coin)
    price = pyupbit.get_current_price(coin)
    if price * balance > 5000 :
        upbit.sell_market_order(coin, balance)

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0


def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]


def searching_coin():
    searching_list = []
    coins = pyupbit.get_tickers(fiat="KRW")
    while searching_list == []:
        try:
            for coin in coins:
                k = pyupbit.get_ohlcv(coin, interval="minutes1", count=30)
                if k[27:].describe()["volume"]["mean"]/k[7:10].describe()["volume"]["mean"] > 100:
                    searching_list.append(coin)
        
                    
        except TypeError as e:
            print(e)
    return searching_list[-1]





#로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:

        krw = get_balance("KRW")
        #코인 찾기 & 매수
        if krw > 5000:
            #원화 조회
            best_coin = searching_coin()
            t_coin = best_coin
            print(t_coin)
            upbit.buy_market_order(t_coin, krw*0.9995)
            print("buy")
            buy_price = pyupbit.get_current_price(t_coin)
            buy_time = datetime.datetime.now()
            
        else:
            while True:
            #코인 팔기 조건 1 마진 5%먹으면 팔기
                if get_current_price(t_coin) > buy_price*1.02:
                    sell_all(t_coin)
                    time.sleep(1)
                    print("sell")
                    break

                #코인 팔기 조건2 마진이 -2%면 팔기
                elif get_current_price(t_coin) < buy_price*0.99 :
                    sell_all(t_coin)
                    time.sleep(1)  
                    print("sell")
                    break

                #코인 팔기 조건 3 10분이 지나면 팔기
                elif datetime.datetime.now() > buy_time + datetime.timedelta(minutes=20):
                    sell_all(t_coin)
                    time.sleep(1)
                    print("sell")
                    break

                else:
                    continue

            
            
    except Exception as e:
        print(e)
        time.sleep(1)