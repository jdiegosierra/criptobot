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
        
def getData(mercado, intervalo):
#        
#        data = my_bittrex.get_latest_candle(mercado, intervalo)
#        df = pd.DataFrame(data["result"])        
#        filedf = pd.read_excel("data/" + mercado + ".xlsx")
#        filedf = filedf.append(df, ignore_index=True)       
#        filedf.to_excel("data/" + mercado + ".xlsx")
    print("ACTUALIZANDO EXCEL DE " + mercado + " CON INTERVALO " + intervalo)
    my_bittrex = Bittrex(None, None, api_version=API_V2_0)
    data = my_bittrex.get_candles(mercado, intervalo)
    """ data["result"] para limpiar los datos anteriores a result """
    df = pd.DataFrame(data["result"])
    df = df.rename(index=str, columns={"BV": 'basevolume',"C": 'close',"H": 'high',"L": 'low',"O": 'open',"T": 'date',"V": '24hvolume'})
    df.to_excel("data/" + mercado + ".xlsx")
    
def historicalData(mercado, intervalo, token_tlgrm, id_conversacion):
    
    """
    Descarga el histórico de datos de Bittrex del mercado pasado por argumento 
    e inicia la actualización automática en un archivo excel. De momento solo está
    implementado para parámetro "day"
    
    Argumentos de ejemplo:
        #mercado = "BTC-ETH"
        #intervalo = [“oneMin”, “fiveMin”, “thirtyMin”, “hour”, “day”]
    
    """                     
    
    if (intervalo == "day"):
        delay = 86400
    elif(intervalo == "hour"):
        delay = 3600
    elif(intervalo == "thirtyMin"):
        delay = 1800
    elif(intervalo == "fiveMin"):
        delay = 300
    elif(intervalo == "oneMin"):
        delay = 60
    else:
        print("ERROR INTRODUCIENDO INTERVALO, COMPRUEBE LOS INTERVALOS DISPONIBLES")
    
    periodic_scheduler = PeriodicScheduler()   
    periodic_scheduler.setup(delay, getData, (mercado, intervalo,)) 
    periodic_scheduler.run() 

def comprar():
    print("COMPRANDO")
    
def vender():
    print("VENDIENDO")
    
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
    

def magicHour(mercado, periodo):
    pendiente = calcularPendiente(mercado, periodo)
    pendiente = True
    if (pendiente == True):
        print("Se va a analizar los datos")
        stock = StockDataFrame.retype(pd.read_excel("data/" + mercado + ".xlsx"))
        print("el RSI es: " + str(stock['rsi_6']))
        comprar()
    else:
        print("Pendiente negativa, no se analizan datos")
    

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
    
    
    
    