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
import telegram

superior = 55
inferior = 45
buy = True 

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
    try:
        bot.send_message(chat_id=update.message.chat_id, text=texto)
    except telegram.error.TimedOut:
        print("Ha habido un error enviando mensaje en getData")
    
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

def comprar(mercado, bot, update):
    global buy
    df1 = pd.read_excel("data/" + mercado + ".xlsx", index=None)
    df2 = pd.read_excel("data/" + "resultados" + ".xlsx")
    df2 = df2.append({'compra': float(df1["close"][-1:])}, ignore_index=True)
    df2.to_excel("data/" + "resultados" + ".xlsx")
    texto = "Se ha COMPRADO en " + str(float(df1["close"][-1:]))
    buy = False
    try:
        bot.send_message(chat_id=update.message.chat_id, text=texto)
    except telegram.error.TimedOut:
        print("Ha habido un error enviando mensaje en comprar")
    
def vender(mercado, bot, update):
    global buy
    df1 = pd.read_excel("data/" + mercado + ".xlsx")
    df2 = pd.read_excel("data/" + "resultados" + ".xlsx")
    df2 = df2.append({'venta': float(df1["close"][-1:])}, ignore_index=True)
    df2.to_excel("data/" + "resultados" + ".xlsx")
    texto = "Se ha VENDIDO en " + str(float(df1["close"][-1:]))
    buy = True
    try:
        bot.send_message(chat_id=update.message.chat_id, text=texto)
    except telegram.error.TimedOut:
        print("Ha habido un error enviando mensaje en vender")

def nada(mercado, bot, update):
    texto = "No se ha hecho NADA "
    try:
        bot.send_message(chat_id=update.message.chat_id, text=texto)
    except telegram.error.TimedOut:
        print("Ha habido un error enviando mensaje en funcion nada")
    
    
def checkIntercect(mercado, update):
    df = pd.read_excel("data/" + mercado + ".xlsx")
    if ((df["kdjk"][-2:-1] > df["kdjd"][-2:-1]).bool() and (df["kdjk"][-1:] < df["kdjd"][-1:]).bool()):
        return True
    elif ((df["kdjk"][-2:-1] < df["kdjd"][-2:-1]).bool() and (df["kdjk"][-1:] > df["kdjd"][-1:]).bool()):
        return True
    else:
        return False
    
def pintarCruce(mercado, color):
    df = pd.read_excel("data/" + mercado + ".xlsx")
    plt.figure(figsize=(50, 10))    
    plt.subplot(2,1,1)
    plt.title("CLOSE")
    plt.plot(df["close"][-72:])
    plt.subplot(2,1,2)
    plt.title("STOCHASTIC")
    plt.plot(df["kdjk"][-72:], c = 'b')
    plt.plot(df["kdjd"][-72:], c = 'magenta')
    plt.plot(df["kdjj"][-72:], c = 'darkslateblue')
    plt.axhline(superior, color = 'r')
    plt.axhline(inferior, color = 'r')
    plt.axhspan(inferior,superior, alpha = 0.25)
    plt.axvline(len(df.index)-2+0.5, color = color)   
    plt.savefig("figure/" + mercado + ".png")

def pintar(mercado):
    df = pd.read_excel("data/" + mercado + ".xlsx")
    plt.figure(figsize=(50, 10))    
    plt.subplot(2,1,1)
    plt.title("CLOSE")
    plt.plot(df["close"][-72:])
    plt.subplot(2,1,2)
    plt.title("STOCHASTIC")
    plt.plot(df["kdjk"][-72:], c = 'b')
    plt.plot(df["kdjd"][-72:], c = 'magenta')
    plt.plot(df["kdjj"][-72:], c = 'darkslateblue')
    plt.axhline(superior, color = 'r')
    plt.axhline(inferior, color = 'r')
    plt.axhspan(inferior,superior, alpha = 0.25)
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
    time.sleep(10)
    periodic_scheduler = PeriodicScheduler()   
    periodic_scheduler.setup(getDelay(intervalo), magicfunc, (mercado, intervalo, bot, update,)) 
    periodic_scheduler.run() 
    
def actuafunc(mercado, bot, update):
    df = pd.read_excel("data/" + mercado + ".xlsx")
    print("Buy es: " + str(buy))
    print("La media es: " + str(df["kdjk"][-2:].mean()))
    if ((df["kdjk"][-2:].mean() >= superior) and buy == False):
        vender(mercado, bot, update)
        pintarCruce(mercado, 'r')
    elif ((df["kdjk"][-2:].mean() <= inferior) and buy == True):
        comprar(mercado, bot, update)
        pintarCruce(mercado, 'g')
    else:
        nada(mercado, bot, update)
        pintarCruce(mercado, 'y')

    
def magicfunc(mercado, intervalo, bot, update):
    
    try:
        bot.send_message(chat_id=update.message.chat_id, text="ANALIZANDO...")
    except telegram.error.TimedOut:
        print ("Ha habido un error enviando el mensaje ANALIZANDO...")
    #pendiente = calcularPendiente(mercado, periodo)#periodo tiene que ser un numero
    pendiente = True
    if (pendiente == True):
        #update.message.reply_text("Pendiente positiva, se analizarán datos.")
        try:
            df = pd.read_excel("data/" + mercado + ".xlsx")
            stock = StockDataFrame.retype(df)
            df["kdjk"] = stock['kdjk']
            del df['rsv_9']
            del df['kdjk_9']
            del df['kdjd_9']
            del df['kdjj_9']
            df.to_excel("data/" + mercado + ".xlsx")
            try:
                cruce = checkIntercect(mercado, update)
            except IndexError:
                print("Ha habido un error en checkIntercect")
            if (cruce == True):
                try:
                    bot.send_message(chat_id=update.message.chat_id, text="Se ha detectado un momento para actuar")
                except telegram.error.TimedOut:
                    print("Se ha producido un error enviando el mensaje de deteccion del momento")
                actuafunc(mercado, bot, update)
                try: 
                    bot.send_photo(chat_id=update.message.chat_id, photo=open("figure/" + mercado + ".png", 'rb')) 
                except telegram.error.TimedOut:
                    print("Se ha producido un error enviando la imagen")
            else:
                pintar(mercado)
        except EOFError:
            print("Ha habido un error leyendo el excel pero el programa debería seguir funcionando")
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Pendiente negativa, no se analizan datos")
    

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
    
    
    
    