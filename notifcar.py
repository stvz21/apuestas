import telebot

class Notificar:
    bot = telebot.TeleBot("1238627815:AAGBjaRN0CxD6zsCTg0tyJSOBt_lw6GZU5M", parse_mode='MARKDOWN')
    
    def __init__(self):
        pass
        
    @bot.message_handler(func=lambda message: True)
    def mensaje(self, msg):
        self.bot.send_message('@miluTest', msg)
    
    
    
    