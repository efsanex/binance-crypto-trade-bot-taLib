from binance.client import Client
import numpy as np
import talib as ta
from talib import MA_Type
import time
import re
import requests
from decimal import *
from reFunc import *
import datetime

getcontext().prec = 4
binance = Client('apiKey', 'apiSecret')
checkSqlite()
ceptekiPara = 720
while True:
    for i in range(len(coinP)):
        if len(getOpenOrder()) < 24:
            if orderCheck(coinP[i]):# and dateCheck(coinP[i]): 
                try:
                    interval = '1h'
                    pair = coinP[i] 
                    limit = 500
                    klines = binance.get_klines(symbol=pair, interval=interval, limit=limit)

                    #open_time = [int(entry[0]) for entry in klines]
                    #open = [float(entry[1]) for entry in klines]
                    high = [float(entry[2]) for entry in klines]
                    low = [float(entry[3]) for entry in klines]
                    close = [float(entry[4]) for entry in klines]
                    #volume = [float(entry[5]) for entry in klines]
                    #open_array = np.asarray(open)
                    close_array = np.asarray(close)
                    high_array = np.asarray(high)
                    low_array = np.asarray(low)
                    #volume_array = np.asarray(volume)

                    adx = ta.ADX(high_array, low_array, close_array, timeperiod=14)
                    #########################################
                    #rsi = ta.RSI(close_array, timeperiod=14)
                    #last_rsi = rsi[-1]
                    ##########################################
                    macd, macdsignal, macdhist = ta.MACD(close_array, fastperiod=12, slowperiod=26, signalperiod=9)
                    #last_macd = macd[-1]
                    #last_macd_signal = macdsignal[-1]
                    #previous_macd = macd[-2]
                    #previous_macd_signal = macdsignal[-2]
                    #macd_cross_up = last_macd > last_macd_signal and previous_macd < previous_macd_signal
                    ##############   STOCH_RSI --  K > D yükseliş  ############################
                    #slowK, slowD = ta.STOCH(rsi, rsi, rsi, fastk_period=14,slowk_period=3, slowk_matype=0)
                    ##########################################
                    #fastK, fastD = ta.STOCHF(high_array, low_array, close_array, fastk_period=3, fastd_period=3, fastd_matype=0)
                    ##########################################
                    #upper, middle, lower = ta.BBANDS(close_array, matype=MA_Type.T3)
                    ##########################################
                    #cdlhammer = ta.CDLHAMMER(open_array, high_array, low_array, close_array)
                    ##########################################
                    #plus_di = ta.PLUS_DI(high_array, low_array, close_array, timeperiod=14)
                    ##########################################
                    #minus_di = ta.MINUS_DI(high_array, low_array, close_array, timeperiod=14)
                    ##########################################
                    #mom = ta.MOM(close_array, timeperiod=10)
                    ##########################################
                    #cci = ta.CCI(high_array, low_array, close_array, timeperiod=14)
                    ##########################################
                    #mfi = ta.MFI(high_array, low_array, close_array, volume_array, timeperiod=14)
                    ##########################################
                    #ema200_high = ta.EMA(high_array, timeperiod=200)
                    #ema200_low = ta.EMA(low_array, timeperiod=200)
                    #ema200_close = ta.EMA(close_array, timeperiod=200)
                    #ema20_close = ta.EMA(close_array, timeperiod=20)

                    #SMA20 = ta.SMA(close_array,timeperiod=20)#[-1]
                    #SMA50 = ta.SMA(close_array,timeperiod=50)#[-1] if SMA20 > SMA50:

                    #if(last_rsi < 30 and slowK[-1] < 20 and lower[-1] > close_array[-1] and cdlhammer[-1] == 100):
                    #    print(coinP[i] +" strateji_1")
                    #if(last_rsi < 30 and lower[-1] > close_array[-1]):
                    #    print(coinP[i] +" BbandRsi")
                    #if(adx[-1] > 25 and mom[-1] > 0 and plus_di[-1] > 25 and plus_di[-1] > minus_di[-1]):
                    #    print(coinP[i] +" ADXMomentum")
                    #if(macd[-1] > 0 and macd[-1] > macdsignal[-1]):
                    #    print(coinP[i] +" macD")
                    #if(cci[-1] <= -50.0 and macd[-1] > macdsignal[-1]):
                    #    print(coinP[i] +" macD + CCI")
                    #if(open_array[-1] < ema_low[-1] and fastK[-1] < 30 and fastD[-1] < 30 and adx[-1] > 30):
                    #    print(coinP[i] +" CofiBitStrategy")
                    #ema20_close[-1 > ema200_close[-1] or 
                    #if(macd[-1] > 0 and macd[-1] > macdsignal[-1] and upper[-1] > upper[-2] and rsi[-1] > 65 and close_array[-1] > close_array[-2] or rsi[-1] < 30):
                    if macd[-1] > 0 and adx[-1] > 25:
                        #minAlmaOranı = binance.get_symbol_info(coinP[i])
                        coinBilgi = binance.get_ticker(symbol=coinP[i])
                        #qty = 30 / Decimal(coinBilgi['askPrice'])
                        #alinacakMiktar = buyQtyCalc(coinP[i],qty)
                        #satinAL = binance.order_market_buy(symbol=coinP[i],quantity=alinacakMiktar)
                        botId = "botid"
                        chatId = "chatid"
                        insertOrders(coinP[i],str(Decimal(coinBilgi['askPrice'])),datetime.datetime.now(),str(Decimal(coinBilgi['askPrice'])),datetime.datetime.now(),str(Decimal("0.1")),str(Decimal("0.1")),0)
                        send_text = 'https://api.telegram.org/bot'+botId+'/sendMessage?chat_id='+chatId+'&text='+coinP[i]+' yeni pozisyon açıldı.'
                        response = requests.get(send_text)
                except:
                    print("hata")
    time.sleep(30)