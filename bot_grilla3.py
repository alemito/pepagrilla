import telebot #Manejo de API de Telegram
from justwatch import JustWatch

bot = telebot.TeleBot("5416781883:AAFTprcIK7Kanu-Lq4aTazFL8nDAv6RC8y8")

#Datos globales:


#El objeto "message" tiene toda la data del chat.

# responde al comando /start

@bot.message_handler(commands=["start", "help"])
def cmd_start(message):
    #Da la bienvenida"
    bot.reply_to(message,"Bienvenido a la grilla de series y peliculas")


# Responde a los mensajes de texto que no son comandos.
@bot.message_handler(content_types=["text"])
def bot_mensajes_texto(message):
    try:
        just_watch = JustWatch(country='AR') #Seteo el pais de busqueda
        busqueda = message.text #Obtener el texto de la busqueda
        results = just_watch.search_for_item(query=f'{busqueda}') # realiza la busqueda en justwatch
        streaming = ['srp','nfx','prv','dnp'] #Listado de operadores que tengo.
        lista= []
        try:
            for proveedor in results['items'][0]['offers']:
                if proveedor['package_short_name'] in streaming:
                        if proveedor['package_short_name'] == "prv":
                            lista.append("Prime Video")
                        elif proveedor['package_short_name'] == "srp":
                            lista.append("Star +")
                        elif proveedor['package_short_name'] == "nfx":
                            lista.append("Netflix")
                        elif proveedor['package_short_name'] == "dnp":
                            lista.append("Disney +")
                else:
                        lista.append("Otro proveedor")
            lista = list(dict.fromkeys(lista)) # Quito duplicados
            bot.send_message(message.chat.id, f"Encontre a {results['items'][0]['title']} en")
            for x in lista:
                 bot.send_message(message.chat.id,f"{x}")

        except (IndexError,KeyError):
            bot.reply_to(message,"No obtuve resultados en la busqueda.")
    except (ValueError):
        bot.reply_to(message,"No pude procesar correctamente la busqueda")                
# MAIN

if __name__ == '__main__':
    bot.infinity_polling() #Bucle infinito, con esto esta siempre esperando respuestas en el chat.
    