from binance.client import Client
import sqlite3
from decimal import *
import datetime
import math

binance = Client('wbqYULmLVD4LisNljzY2mW9gtamtTjXzGe9YCN4VicV4OUJvI9GCLe6agNEtpIgI', '2omMiHOFUF05nJEqKpBR6BHkQIOhEi43ba4wQWRcqX93DNALuRdBrKSwbv3ptNk7')
connection = sqlite3.connect("botOrders.db")
cursor = connection.cursor()

def checkSqlite():
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY ,symbol TEXT, alisFiyati DECIMAL, alisZamani timestamp, kontrolFiyati DECIMAL,kontrolZamani timestamp, yuzdeFark DECIMAL,enYuksekFark DECIMAL,durum INTEGER)")
    except:
        print("error...")

def insertOrders(symbol,alisFiyati,alisZamani,kontrolFiyati,kontrolZamani,yuzdeFark,enYuksekFark,durum):
    params = [(symbol,alisFiyati,alisZamani,kontrolFiyati,kontrolZamani,yuzdeFark,enYuksekFark,durum),]
    try:
        sql = '''INSERT INTO orders (symbol, alisFiyati, alisZamani, kontrolFiyati, kontrolZamani, yuzdeFark, enYuksekFark, durum) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
        cursor.executemany(sql, params)
        connection.commit()
    except sqlite3.IntegrityError as e:
        print('sqlite error: ', e.args[0])

def orderCheck(symbol):
    cursor = connection.execute("SELECT symbol FROM orders WHERE symbol = ? AND durum = 0 ORDER BY id DESC LIMIT 1", (symbol,))
    durum_ = cursor.fetchone()
    if durum_ is not None:
        return False
    else:
        return True

def dateCheck(symbol):
    cursor = connection.execute("SELECT kontrolZamani FROM orders WHERE symbol = ? AND durum = 1 ORDER BY id DESC LIMIT 1", (symbol,))
    date = cursor.fetchone()
    if date is not None:
        gun = datetime.datetime.now() - datetime.datetime.strptime(date[0], '%Y-%m-%d %H:%M:%S.%f')
        if gun > datetime.timedelta(hours=4):
            return True
        else:
            return False
    else:
        return True

def getOrder(symbol):
    cursor = connection.execute("SELECT * FROM orders WHERE symbol = ? ORDER BY id DESC LIMIT 1", (symbol,))
    sonuc = cursor.fetchone()
    return sonuc

def getOpenOrder():
    try:
        cursor = connection.execute("SELECT * FROM orders WHERE durum = 0")
        sonuc = cursor.fetchall()
        return sonuc
    except sqlite3.IntegrityError as e:
        print('sqlite error: ', e.args[0])


def updateOrder(kontrolFiyati,kontrolZamani,yuzdeFark,enYuksekFark,durum,symbol):
    try:
        params = (kontrolFiyati,kontrolZamani,yuzdeFark,enYuksekFark,durum,symbol)
        sql = '''UPDATE orders SET kontrolFiyati = ?, kontrolZamani = ?, yuzdeFark = ?, enYuksekFark = ?, durum = ? WHERE symbol = ? '''
        cursor.execute(sql, params)
        connection.commit()
    except sqlite3.IntegrityError as e:
        print('sqlite error: ', e.args[0])

def buyQtyCalc(coin, number):
    try:
        info = binance.get_symbol_info(symbol=coin)
        step_size = [float(_['stepSize']) for _ in info['filters'] if _['filterType'] == 'LOT_SIZE'][0]
        step_size = '%.8f' % step_size
        step_size = step_size.rstrip('0')
        decimals = len(step_size.split('.')[1])
        return math.floor(number * 10 ** decimals) / 10 ** decimals
    except:
        print("qty calc error")

coinP = ["NEOUSDT","LTCUSDT","QTUMUSDT","ADAUSDT","XRPUSDT","EOSUSDT","IOTAUSDT","XLMUSDT","ONTUSDT","TRXUSDT","ETCUSDT","ICXUSDT","NULSUSDT","VETUSDT","PAXUSDT","LINKUSDT",
"WAVESUSDT","BTTUSDT","ONGUSDT","HOTUSDT","ZILUSDT","ZRXUSDT","FETUSDT","BATUSDT","XMRUSDT","ZECUSDT","IOSTUSDT","CELRUSDT","NANOUSDT","OMGUSDT","THETAUSDT","ENJUSDT",
"MITHUSDT","MATICUSDT","ATOMUSDT","TFUELUSDT","ONEUSDT","FTMUSDT","ALGOUSDT","GTOUSDT","DOGEUSDT","DUSKUSDT","ANKRUSDT","WINUSDT","COSUSDT","NPXSUSDT","COCOSUSDT","MTLUSDT",
"TOMOUSDT","PERLUSDT","DENTUSDT","MFTUSDT","KEYUSDT","DOCKUSDT","WANUSDT","FUNUSDT","CVCUSDT","CHZUSDT","BANDUSDT","BEAMUSDT","XTZUSDT","RENUSDT","RVNUSDT","HBARUSDT",
"NKNUSDT","STXUSDT","KAVAUSDT","ARPAUSDT","IOTXUSDT","RLCUSDT","CTXCUSDT","TROYUSDT","VITEUSDT","FTTUSDT","OGNUSDT","DREPUSDT","TCTUSDT","WRXUSDT","BTSUSDT","LSKUSDT",
"BNTUSDT","LTOUSDT","AIONUSDT","MBLUSDT","COTIUSDT","STPTUSDT","WTCUSDT","DATAUSDT","SOLUSDT","CTSIUSDT","HIVEUSDT","CHRUSDT","GXSUSDT","ARDRUSDT","MDTUSDT","STMXUSDT",
"KNCUSDT","REPUSDT","LRCUSDT","PNTUSDT","SCUSDT","ZENUSDT","SNXUSDT","VTHOUSDT","DGBUSDT","SXPUSDT","DAIUSDT","DCRUSDT","STORJUSDT","MANAUSDT","BALUSDT","BLZUSDT",
"IRISUSDT","KMDUSDT","JSTUSDT","SRMUSDT","ANTUSDT","CRVUSDT","SANDUSDT","OCEANUSDT","NMRUSDT","DOTUSDT","LUNAUSDT","RSRUSDT","PAXGUSDT","WNXMUSDT","TRBUSDT","BZRXUSDT",
"SUSHIUSDT","EGLDUSDT","DIAUSDT","RUNEUSDT","FIOUSDT","UMAUSDT","BELUSDT","WINGUSDT","UNIUSDT","NBSUSDT","OXTUSDT","SUNUSDT","HNTUSDT","FLMUSDT","ORNUSDT","UTKUSDT","XVSUSDT",
"ALPHAUSDT","NEARUSDT","FILUSDT","INJUSDT","AUDIOUSDT","CTKUSDT","AKROUSDT","AXSUSDT","HARDUSDT","DNTUSDT","STRAXUSDT","ROSEUSDT","AVAUSDT","XEMUSDT","SKLUSDT",
"GRTUSDT","JUVUSDT","PSGUSDT","1INCHUSDT","REEFUSDT","OGUSDT","ATMUSDT","ASRUSDT","CELOUSDT","RIFUSDT","TRUUSDT","CKBUSDT","TWTUSDT","FIROUSDT","LITUSDT","SFPUSDT","DODOUSDT",
"CAKEUSDT"]

coinP_ = ["BCHUSDT","MKRUSDT","YFIUSDT","YFIIUSDT","KSMUSDT","AVAXUSDT","UNFIUSDT","BTCSTUSDT","COMPUSDT","AAVEUSDT"]