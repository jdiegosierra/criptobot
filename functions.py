# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 00:32:32 2018

@author: Diego Sierra Fernandez
"""

from bittrex.bittrex import Bittrex, API_V2_0
import sched
import pandas as pd
import time
from stockstats import StockDataFrame
import matplotlib.pyplot as plt

# Clase para repetir eventos periodicamente (Falta def stop)
class PeriodicScheduler(object):                                                  
    def __init__(self):                                                           
        self.scheduler = sched.scheduler(time.time, time.sleep)                   
                                                                            
    def setup(self, interval, action, actionargs=()):                             
        action(*actionargs)                                                       
        self.scheduler.enter(interval, 1, self.setup,                             
                        (interval, action, actionargs))                           
                                                                        
    def run(self):                                                                
        self.scheduler.run()

        
def getData(mercado, intervalo, bot, update):
    texto = "ACTUALIZANDO EXCEL DE " + mercado + " CON INTERVALO " + intervalo
    bot.send_message(chat_id=update.message.chat_id, text=texto)
    
    my_bittrex = Bittrex(None, None, api_version=API_V2_0)
    data = my_bittrex.get_candles(mercado, intervalo)
    """ data["result"] para limpiar los datos anteriores a result """
    df = pd.DataFrame(data["result"])
    df = df.rename(index=str, columns={"BV": 'basevolume',"C": 'close',"H": 'high',"L": 'low',"O": 'open',"T": 'date',"V": '24hvolume'})
    df.to_excel("data/" + mercado + ".xlsx")

def getDelay(intervalo):
    if (intervalo == "day"):
        return 86400
    elif(intervalo == "hour"):
        return 3600
    elif(intervalo == "thirtyMin"):
        return 1800
    elif(intervalo == "fiveMin"):
        return 300
    elif(intervalo == "oneMin"):
        return 60
    else:
        return "ERROR INTRODUCIENDO INTERVALO, COMPRUEBE LOS INTERVALOS DISPONIBLES"
    
def funcion1(mercado, intervalo, bot, update):
    
    """
    Descarga el histórico de datos de Bittrex del mercado pasado por argumento 
    e inicia la actualización automática en un archivo excel. De momento solo está
    implementado para parámetro "day"
    
    Argumentos de ejemplo:
        #mercado = "BTC-ETH"
        #intervalo = [“oneMin”, “fiveMin”, “thirtyMin”, “hour”, “day”]
    
    """                     
    
    periodic_scheduler = PeriodicScheduler()   
    periodic_scheduler.setup(getDelay(intervalo), getData, (mercado, intervalo, bot, update,)) 
    periodic_scheduler.run() 

def comprar():
    print("COMPRANDO")
    
def vender():
    print("VENDIENDO")

def checkIntercect(mercado):
    df = pd.read_excel("data/" + mercado + ".xlsx")
    if ((df["kdjk"][-2:-1] > df["kdjd"][-2:-1]).bool() and (df["kdjk"][-1:] < df["kdjd"][-1:]).bool()):
        return True
    elif ((df["kdjk"][-2:-1] < df["kdjd"][-2:-1]).bool() and (df["kdjk"][-1:] > df["kdjd"][-1:]).bool()):
        return True
    else:
        return False
    
def pintar(mercado):
    df = pd.read_excel("data/" + mercado + ".xlsx")
    #    box = {
#      'facecolor'  : '.75',
#      'edgecolor' : 'k',
#      'boxstyle'    : 'round'
#    }
    plt.figure(figsize=(50, 10))
    
#   plt.text(-0.5, -0.20, 'Brackmard minimum', bbox = box)
    plt.subplot(2,1,1)
    plt.title("CLOSE")
    plt.plot(df["close"][-72:])
    plt.subplot(2,1,2)
    plt.title("STOCHASTIC")
    plt.plot(df["kdjk"][-72:], c = 'b')
    plt.plot(df["kdjd"][-72:], c = 'g')
    #plt.plot(df["kdjj"][-72:], c = 'r')
    plt.savefig("figure/" + mercado + ".png")

def calcularPendiente(mercado, periodo):
    filedf = pd.read_excel("data/" + mercado + ".xlsx")
    df1 = filedf["close"][-periodo:]
    df2 = filedf["close"][-periodo*2:-periodo]
    #print("pendiente 1: " + str(df1.mean()))
    #print("pendiente 2: " + str(df2.mean()))
    if (df1.mean() >= df2.mean()):
        return True
    else: 
        return False
    
def funcion2(mercado, intervalo, bot, update):
    periodic_scheduler = PeriodicScheduler()   
    periodic_scheduler.setup(getDelay(intervalo), magicfunc, (mercado, intervalo, bot, update,)) 
    periodic_scheduler.run() 
    
def magicfunc(mercado, intervalo, bot, update):
    #pendiente = calcularPendiente(mercado, periodo)#periodo tiene que ser un numero
    pendiente = True
    if (pendiente == True):
        update.message.reply_text("Pendiente positiva, se analizarán datos.")
        df = pd.read_excel("data/" + mercado + ".xlsx")
        stock = StockDataFrame.retype(df)
        df["kdjk"] = stock['kdjk']
        del df['rsv_9']
        del df['kdjk_9']
        del df['kdjd_9']
        del df['kdjj_9']
        df.to_excel("data/" + mercado + ".xlsx")
        pintar(mercado)
        bot.send_photo(chat_id=update.message.chat_id, photo=open("figure/" + mercado + ".png", 'rb'))
        if (checkIntercect(mercado) == True):
            update.message.reply_text("SE HA ENCONTRADO UN CRUCE")
            update.message.reply_text("SE HA ENCONTRADO UN CRUCE")
            update.message.reply_text("SE HA ENCONTRADO UN CRUCE")
            update.message.reply_text("SE HA ENCONTRADO UN CRUCE")

    else:
        update.message.reply_text("Pendiente negativa, no se analizan datos")
    

#def currencycheck(bot, ident):
#    """ 
#    Comprueba si hay criptomonedas nuevas.
#    """
#    
#    my_bittrex = Bittrex(None, None, api_version=API_V2_0)
#    todayCurrency = my_bittrex.get_currencies()
#    
#    file = open("currencys.txt","r")
#    yesterdayCurrency = json.loads(file.read())
#    file.close()
#    
#    for i in range(len(todayCurrency["result"])):
#        flag = False
#        tcurrency = todayCurrency["result"][i]["CurrencyLong"]
#        for j in range(len(yesterdayCurrency["result"])):
#            ycurrency = yesterdayCurrency["result"][i]["CurrencyLong"]
#            if tcurrency == ycurrency:
#                flag = True
#                break
#        if flag == False:
#            print("Nueva moneda encontrada llamada: "+tcurrency)
#            bot.send_message(chat_id=ident, text="Nueva moneda encontrada llamada: "+tcurrency)
#    print("Checkeo terminado")
#    bot.send_message(chat_id=ident, text="Checkeo terminado")
    
    
    
    