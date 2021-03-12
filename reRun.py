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
while True:
    try:
        for i in range(len(getOpenOrder())):
            time.sleep(1)
            coinBilgi = binance.get_ticker(symbol=getOpenOrder()[i][1]) 
            kontrolFiyati = Decimal(coinBilgi['askPrice'])
            kontrolZamani = datetime.datetime.now()
            alisFiyati = Decimal(getOpenOrder()[i][2])
            yuzdeFark = Decimal(((kontrolFiyati - alisFiyati) / alisFiyati) * 100)
            enYuksekFark_ = Decimal(getOpenOrder()[i][7])
            durum = 0
            if(yuzdeFark > enYuksekFark_):
                enYuksekFark_ = yuzdeFark
            if(enYuksekFark_ - yuzdeFark > 3):
                #balance_ = binance.get_asset_balance(asset=getOpenOrder()[i][1])
                #eldekiAdet = balance_['free']
                #satılacakMiktar = buyQtyCalc(getOpenOrder()[i][1],eldekiAdet)
                #sat = binance.order_market_sell(symbol=getOpenOrder()[i][1],quantity=satılacakMiktar)
                durum = 1
                botId = "botid"
                chatId = "chatid"
                send_text = 'https://api.telegram.org/bot'+botId+'/sendMessage?chat_id='+chatId+'&text='+getOpenOrder()[i][1]+' '+str(yuzdeFark)+' satış işlemi'
                response = requests.get(send_text)
            updateOrder(str(kontrolFiyati),kontrolZamani,str(yuzdeFark),str(enYuksekFark_),durum,getOpenOrder()[i][1])
            print('sembol: '+getOpenOrder()[i][1]+' Alış: '+str(getOpenOrder()[i][2])+' AlışZamanı: '+str(getOpenOrder()[i][3])+' kontrolFiyatı: '+str(getOpenOrder()[i][4])+' kontrolZamanı: '+str(getOpenOrder()[i][5])+' Fark: '+str(getOpenOrder()[i][6])+' enYuksek: '+str(getOpenOrder()[i][7]))
            #time.sleep(1)
    except:
        print("hata")