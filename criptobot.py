# -*- coding: utf-8 -*-
"""
Proximo objetivo: Importar correctamente las funciones, depurar fallos
"""

from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
import logging
from functions import historicalData
from threading import Thread

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

    #Falta implementar bien el chat_id para no tener que ponerlo manualmente. Se hace con context.
    #bot.send_message(chat_id=500840093, text=result)#Diego
    #bot.send_message(chat_id=477349018, text='One message every 10')#Pablo
def echo(bot, update):
    text = "Escriba /start mercado('BTC-ETH') intervalo('day') para arrancar el bot."
    text = text + ' Escriba "/STOP" para parar (EMERGENCIA) ATENCION!'
    text = text + ' con /STOP sólo se podrá volver a iniciar desde el ordenador'
    bot.send_message(chat_id=update.message.chat_id, text=text)

    
def stop(bot, update):
    text1 = "Desconexión de emergencia del bot. No podrá realizar más acciones."
    bot.send_message(chat_id=update.message.chat_id, text=text1)
    up.idle("SIGINT")
    
def start(bot, update, args):
    # Add job to queue
    #global h
    #h = up.job_queue.run_repeating(currencycheck, 10)
    """ 
    Creamos un hilo por cada función para que se puedan ejecutar en paralelo
    """
    mercado = args[0] 
    intervalo = args[1]
    thread = Thread(target = historicalData, args = (mercado, intervalo, token_tlgrm, id_conversacion,))
    thread.start()
    #currencycheck(bot, ident)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)
      
def main():  
    
    global token_tlgrm, id_conversacion, up
    token_tlgrm = '509446248:AAECtz3wUMKaa5d4TOEHmeQnvxBqA9Mb8YM'
    id_conversacion = 500840093
    
    up = Updater(token=token_tlgrm)#Diego 
    up.dispatcher.add_handler(CommandHandler('STOP', stop))
    up.dispatcher.add_handler(CommandHandler('start', start, pass_args=True))
    up.dispatcher.add_handler(MessageHandler(Filters.text, echo))
    #job_minute = job.run_repeating(callback_minute, interval=10, first=0)
    #job_minute.enabled = False  # Temporarily disable this job
    #job_minute.schedule_removal()  # Remove this job completely
    # log all errors
    up.dispatcher.add_error_handler(error)
    # Start the Bot
    up._clean_updates()
    up.start_polling()  
    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    up.idle()
    
if __name__ == '__main__':
    main()
    
