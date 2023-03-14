import telebot

class Notificar:
    estado = True
    def __init__(self):
        self.bot = telebot.AsyncTeleBot("5871277082:AAFsEc0clhaeJ0wokJVfGF0_P3P0385Sb0M", parse_mode='MARKDOWN')
        # @self.bot.message_handler(commands=['start'])
        # def send_welcome(message):
        #     self.process_command_start(message)
        
        # @self.bot.message_handler(commands=['stop'])
        # def send_welcome(message):
        #     self.process_command_stop(message)

        
    #@bot.message_handler(func=lambda message: True)
    def mensaje(self, msg):
        self.bot.send_message('@miluTest', msg)
    
    # def process_command_start(self, message):
    #     self.estado = True
    #     self.bot.reply_to(message, "El bot se ha activado")
    
    # def process_command_stop(self, message):
    #     self.estado = False
    #     self.bot.reply_to(message, "El bot se ha detenido")
    
    # def escucha(self):
    #     #self.bot.polling()
    
    
    
    
