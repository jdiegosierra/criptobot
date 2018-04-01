# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 00:32:32 2018

@author: Diego Sierra Fernandez
"""

from bittrex.bittrex import Bittrex, API_V2_0
import sched
import pandas as pd
import time

def historicalData(mercado, intervalo, token_tlgrm, id_conversacion):
    
    """
    Descarga el histórico de datos de Bittrex del mercado pasado por argumento 
    e inicia la actualización automática en un archivo excel. De momento solo está
    implementado para parámetro "day"
    
    Argumentos de ejemplo:
        #mercado = "BTC-ETH"
        #intervalo = [“oneMin”, “fiveMin”, “thirtyMin”, “hour”, “day”]
    
    """          

    class PeriodicScheduler(object):                                                  
        def __init__(self):                                                           
            self.scheduler = sched.scheduler(time.time, time.sleep)                   
                                                                                
        def setup(self, interval, action, actionargs=()):                             
            action(*actionargs)                                                       
            self.scheduler.enter(interval, 1, self.setup,                             
                            (interval, action, actionargs))                           
                                                                            
        def run(self):                                                                
            self.scheduler.run()
            
    def getData(my_bittrex, mercado, intervalo):
        print("OBTENIENDO DATO")
        data2 = my_bittrex.get_latest_candle(mercado, intervalo)
        df2 = pd.DataFrame(data2["result"])        
        filedf = pd.read_excel("data/" + mercado + ".xlsx")
        filedf = filedf.append(df2, ignore_index=True)       
        filedf.to_excel("data/" + mercado + ".xlsx")
        
    print("Intervalo es: " + intervalo)
    
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
        
    
    my_bittrex = Bittrex(None, None, api_version=API_V2_0)
    data = my_bittrex.get_candles(mercado, intervalo)
    
    """ data["result"] para limpiar los datos anteriores a result """
    df = pd.DataFrame(data["result"])
    df.to_excel("data/" + mercado + ".xlsx")
    
    periodic_scheduler = PeriodicScheduler()   
    periodic_scheduler.setup(delay, getData, (my_bittrex, mercado, intervalo,)) # it executes the event just once 
    periodic_scheduler.run() # it starts the scheduler

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
    
    
    
    