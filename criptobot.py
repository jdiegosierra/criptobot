# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 18:04:32 2018

@author: Diego
"""

from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


def echo(bot, update):
    text1 = "De momento solo tengo implementada la funcion /start."
    text1 = text1 + ' Escriba "/STOP" (EMERGENCIA) o "/parar" para detener los mensajes... ATENCION!'
    text1 = text1 + ' con /STOP solo se podrá volver a iniciar desde el ordenador'
    bot.send_message(chat_id=update.message.chat_id, text=text1)
    
def stop1(bot, update):
    text1 = "Desconexión de emergencia del bot. No podrá realizar más acciones."
    bot.send_message(chat_id=update.message.chat_id, text=text1)
    up.stop() #Este metodo no funciona para todos los casos
        
def stop2(bot, update):
    h.schedule_removal()
    bot.send_message(chat_id=update.message.chat_id, text="Mensajes detenidos.")
    
def start(bot, update, job_queue, chat_data):
    # Add job to queue
    global h
    h = up.job_queue.run_repeating(callback_minute, 10)
    bot.send_message(chat_id=update.message.chat_id, text="Bot iniciado, cada 10 segundos llegará un msg")

def callback_minute(bot, job):
    #Falta implementar bien el chat_id para no tener que ponerlo manualmente. Se hace con context.
    #bot.send_message(chat_id=500840093, text='One message every 10')#Diego
    bot.send_message(chat_id=477349018, text='One message every 10')#Pablo

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)
      
def main():     
    #Creamos un objeto de tipo Updater
    global up
    #up = Updater(token='509446248:AAECtz3wUMKaa5d4TOEHmeQnvxBqA9Mb8YM')#Diego
    up = Updater(token='467810268:AAELK2y560CpAMMwQBkUWmQT-OTrBJ1pQlw')#Pablo
    dispatcher = up.dispatcher
    
    dispatcher.add_handler(CommandHandler('STOP', stop1))
    dispatcher.add_handler(CommandHandler('parar', stop2))
    dispatcher.add_handler(CommandHandler('start', start, pass_job_queue=True,pass_chat_data=True))
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    #job_minute = job.run_repeating(callback_minute, interval=10, first=0)
    #job_minute.enabled = False  # Temporarily disable this job
    #job_minute.schedule_removal()  # Remove this job completely
    
    # log all errors
    dispatcher.add_error_handler(error)
    # Start the Bot
    up._clean_updates()
    up.start_polling()
    
    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    up.idle()
    
if __name__ == '__main__':
    main()
    
