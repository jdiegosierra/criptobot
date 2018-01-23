# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 18:04:32 2018

@author: Diego
"""

from telegram.ext import Updater, Filters, MessageHandler, CommandHandler

def echo(bot, update):
    print("probando")
    text1 = "De momento solo tengo implementada la funcion parar."
    text1 = text1 + ' Escriba "/stop" para detener el bot... ATENCION!'
    text1 = text1 + '  solo se podrá volver a iniciar desde el ordenador'
    bot.send_message(chat_id=update.message.chat_id, text=text1)
    
def stop(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Deteniendo bot...")
    updater.stop()
    
#Creamos un objeto de tipo Updater
updater = Updater(token='509446248:AAECtz3wUMKaa5d4TOEHmeQnvxBqA9Mb8YM')#Diego
#updater = Updater(token='467810268:AAELK2y560CpAMMwQBkUWmQT-OTrBJ1pQlw')#Pablo
dispatcher = updater.dispatcher

start_handler = CommandHandler('stop', stop)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()