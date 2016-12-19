# # -*- coding: utf-8 -*-
import time

import telebot
from telebot import types

API_TOKEN = '308245102:AAHojngXIJ9yTolBgVi8rycd-SFsUjJKs4o'

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def comando_bienvenida(mensaje):
    chat_id = mensaje.chat.id
    markup = types.ReplyKeyboardMarkup()
    itembtn1 = types.KeyboardButton('Solicitar factura')
    itembtn2 = types.KeyboardButton('Notificacion de puntos ganados')
    itembtn3 = types.KeyboardButton('Checar vencimiento de productos')
    itembtn4 = types.KeyboardButton('Consulta de saldos')
    itembtn5 = types.KeyboardButton('Notificar irregularidad')
    itembtn6 = types.KeyboardButton('Realizar encuesta')
    itembtn7 = types.KeyboardButton('Calificacion de servicios')

    markup.row(itembtn1, itembtn2, itembtn3)
    markup.row(itembtn4, itembtn5, itembtn6)
    markup.row(itembtn7)
    bot.send_message(
        chat_id,
        'Hola! ¡Bienvenido a btoc messenger! Me llamo b-2 '
        'y sere tu bot asistente ¿Que deseeas realizar?',
        reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Solicitar factura')
def solicitar_factura(message):
    markup = types.ReplyKeyboardMarkup()
    affirmative = types.KeyboardButton('Si, claro que quiero!')
    negative = types.KeyboardButton('No, gracias!')
    markup.row(affirmative)
    markup.row(negative)
    question = bot.send_message(
        message.chat.id,
        'Al parecer tus datos no estan registrados en nuestro sistema.\n'
        '¿Te parece bien que comencemos el registro unico para guardar tu'
        ' informacion?', reply_markup=markup)
    bot.register_next_step_handler(question, process_confirmation_step)


def process_confirmation_step(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup()
    itembtn1 = types.KeyboardButton('Solicitar factura')
    itembtn2 = types.KeyboardButton('Notificacion de puntos ganados')
    itembtn3 = types.KeyboardButton('Checar vencimiento de productos')
    itembtn4 = types.KeyboardButton('Consulta de saldos')
    itembtn5 = types.KeyboardButton('Notificar irregularidad')
    itembtn6 = types.KeyboardButton('Realizar encuesta')
    itembtn7 = types.KeyboardButton('Calificacion de servicios')

    markup.row(itembtn1, itembtn2, itembtn3)
    markup.row(itembtn4, itembtn5, itembtn6)
    markup.row(itembtn7)
    if message.text == 'Si, claro que quiero!':
        name = bot.send_message(chat_id, '¿A que nombre voy a facturar?')
        bot.register_next_step_handler(name, process_name_step)
    else:
        bot.send_message(
            chat_id, 'Esta bien. ¿Alguna '
            'cosa mas en la que pueda ayudarle?', reply_markup=markup)


def process_name_step(message):
    chat_id = message.chat.id
    name = message.text
    calle = bot.send_message(chat_id, '¿A que calle voy a facturar?')
    bot.register_next_step_handler(calle, process_calle_step)


def process_calle_step(message):
    try:
        chat_id = message.chat.id
        calle = message.text
        num_int = bot.send_message(chat_id, '¿Cual es el numero interior?')
        bot.register_next_step_handler(num_int, procces_numero_int_step)
    except Exception as e:
        bot.send_message(message, 'ooooops')


def procces_numero_int_step(message):
    try:
        chat_id = message.chat.id
        numero_int = message.text
        numero_ext = bot.send_message(chat_id, '¿Cual es el numero exterior?')
        bot.register_next_step_handler(numero_ext, process_numero_ext_step)
    except Exception as e:
        bot.send_message(message, 'ooooops')


def process_numero_ext_step(message):
    try:
        chat_id = message.chat.id
        numero_ext = message.text
        colonia = bot.send_message(chat_id, '¿Cual es tu colonia?')
        bot.register_next_step_handler(colonia, process_colonia_step)
    except Exception as e:
        bot.send_message(message, 'ooooops')


def process_colonia_step(message):
    try:
        chat_id = message.chat.id
        colonia = message.text
        localidad = bot.send_message(chat_id, '¿Cual es tu localidad?')
        bot.register_next_step_handler(localidad, process_localidad_step)
    except Exception as e:
        bot.send_message(message, 'ooooops')


def process_localidad_step(message):
    try:
        chat_id = message.chat.id
        localidad = message.text
        ciudad = bot.send_message(chat_id, '¿Cual es tu ciudad?')
        bot.register_next_step_handler(ciudad, process_ciudad_step)
    except Exception as e:
        bot.send_message(message, 'ooooops')


def process_ciudad_step(message):
    try:
        chat_id = message.chat.id
        colonia = message.text
        estado = bot.send_message(chat_id, '¿Cual es tu estado?')
        bot.register_next_step_handler(estado, procces_estado_step)
    except Exception as e:
        bot.send_message(message, 'ooooops')


def procces_estado_step(message):
    try:
        chat_id = message.chat.id
        estado = message.text
        codigo_postal = bot.send_message(chat_id, '¿Cual es tu codigo postal?')
        bot.register_next_step_handler(
            codigo_postal,
            procces_codigo_postal_step)
    except Exception as e:
        bot.send_message(message, 'ooooops')


def procces_codigo_postal_step(message):
    try:
        chat_id = message.chat.id
        codigo_postal = message.text
        if not codigo_postal.isdigit():
            codigo_postal = bot.send_message(
                chat_id,
                'El codigo postal no tiene letras. ¿Cual es tu codigo postal?')
            bot.register_next_step_handler(
                codigo_postal, procces_codigo_postal_step)
        else:
            markup = types.ReplyKeyboardMarkup()
            inciso_moral = types.KeyboardButton('Persona moral')
            inciso_fisica = types.KeyboardButton('Persona fisica')
            inciso_no_luc = types.KeyboardButton('Asociaciones no lucrativas')
            inciso_sin_luc = types.KeyboardButton(
                'Persona moral sin fin de lucro')
            markup.row(inciso_moral)
            markup.row(inciso_fisica)
            markup.row(inciso_no_luc)
            markup.row(inciso_sin_luc)
            regimen_fiscal = bot.send_message(
                chat_id, '¿Cual es tu regimen fiscal?', reply_markup=markup)
            bot.register_next_step_handler(
                regimen_fiscal, process_regimen_fiscal)
    except Exception as e:
        bot.send_message(message, 'ooooops')


def process_regimen_fiscal(message):
    try:
        chat_id = message.chat.id
        regimen = message.text
        razon_social = bot.send_message(chat_id, '¿Cual es tu rfc?')
        bot.register_next_step_handler(razon_social, procces_rfc_step)
    except Exception as e:
        bot.send_message(message, 'ooooops')


def procces_rfc_step(message):
    try:
        chat_id = message.chat.id
        letras = message.text[0:4]
        numeros = message.text[4:10]
        letras2 = message.text[10:12]
        numeros2 = message.text[12]
        rfc = message.text
        if ((numeros.isdigit() and
            numeros2.isdigit()) and
            (isinstance(letras, basestring) and
                isinstance(letras2, basestring))):
            markup = types.ReplyKeyboardMarkup()
            itembtn1 = types.KeyboardButton('Solicitar factura')
            itembtn2 = types.KeyboardButton('Notificacion de puntos ganados')
            itembtn3 = types.KeyboardButton('Checar vencimiento de productos')
            itembtn4 = types.KeyboardButton('Consulta de saldos')
            itembtn5 = types.KeyboardButton('Notificar irregularidad')
            itembtn6 = types.KeyboardButton('Realizar encuesta')
            itembtn7 = types.KeyboardButton('Calificacion de servicios')

            markup.row(itembtn1, itembtn2, itembtn3)
            markup.row(itembtn4, itembtn5, itembtn6)
            markup.row(itembtn7)
            bot.send_message(
                chat_id,
                'Excelente, has terminado '
                'de guardar tu informacion! ¿Alguna otra cosa en '
                'la que te pueda ayudar?',
                reply_markup=markup)
        else:
            bot.send_message(
                chat_id,
                'Los primeros 4 digitos de tu RFC parecen '
                'estar mal. Recuerda que primero son 4 digitos solamente,'
                ' letras no')
    except Exception as e:
        bot.send_message(message, 'ooooops')


@bot.message_handler(
    func=lambda message: message.text == 'Notificacion de puntos ganados')
def handle_notificacion_puntos(message):
    bot.send_message(
        message.chat.id,
        'Estimado ' + str(message.chat.first_name) + ', gracias '
        'por su compra, le informamos que con esta operación '
        'le hemos abonado a su tarjeta de lealtad '
        'la cantidad de 357 puntos, quedando hoy con un saldo a su favor de 1,'
        ' 345 puntos, le esperamos nuevamente en nuestras tiendas.')


@bot.message_handler(
    func=lambda message: message.text == 'Checar vencimiento de productos')
def handle_realizar_encuesta(message):
    bot.send_message(
        message.chat.id,
        'Estimado ' + str(message.chat.first_name) + ', Ud dispone de un '
        'saldo acumulado en su tarjeta ' + str(message.chat.id) + ' de '
        '1345 puntos, y puede aplicarlos en la compra de nuestras '
        'promociones como:\n\nLínea electrónica, \nSamsung, \nLG \nSony\n '
        'aproveche el 20 % solo hasta el 30 de Octubre del 2015, fecha en '
        'la que expiran sus puntos acumulados. Gracias por su preferencia')


@bot.message_handler(func=lambda message: message.text == 'Consulta de saldos')
def handle_checar_puntos(message):
    bot.send_message(
        message.chat.id,
        'Hola ' + message.chat.first_name + ', actualmente cuentas con una'
        ' cantidad de 29 puntos, con los cuales puedes realizar compras en'
        ' alguno nuestros siguientes departamentos')


@bot.message_handler(
    func=lambda message: message.text == 'Notificar irregularidad')
def handle_notificar_irregularidad(message):
    irregularidad = bot.send_message(
        message.chat.id,
        'Estimado ' + str(message.chat.first_name) + ', A continuacion digame '
        'como, cuando y donde fue que tuvo una regularidad dentro de nuestras'
        ' tiendas')
    bot.register_next_step_handler(
        irregularidad, procces_notificar_irregularidad)


@bot.message_handler(func=lambda message: message.text == 'Realizar encuesta')
def handle_realizar_encuesta(message):
    markup = types.ReplyKeyboardMarkup()
    inciso_a = types.KeyboardButton('1')
    inciso_b = types.KeyboardButton('2')
    inciso_c = types.KeyboardButton('3')
    inciso_d = types.KeyboardButton('Prefiero no contestar')
    markup.row(inciso_a, inciso_b)
    markup.row(inciso_c, inciso_d)
    respuesta = bot.send_message(
        message.chat.id,
        'ENCUESTA DE SATISFACCION \nEstimado Cliente, rogamos su valiosa '
        'ayuda para calificar el servicio que ha recibido del promobot que la '
        'atiende en nuestra representación (Sr, Juan Martínez Pérez), en la '
        'breve encuesta que le enviamos anexa en este mensaje, por favor solo '
        'con el numero de la respuesta que elija.\n\n'
        'El promobot, Sr Juan Martínez Pérez: \n1.- Acude puntualmente a las '
        'reuniones, me proporciona toda la información que le solicito, me tra'
        'ta amablemente \n2.- Acude a veces a las reuniones, hay información '
        'que le solicite que no me da, a veces es amable. \n3.- Seguido no '
        'acude a las reuniones, constantemente no me da la información que le '
        'solicito, es grosero ', reply_markup=markup)
    bot.register_next_step_handler(respuesta, process_guardar_respuesta)


def procces_notificar_irregularidad(message):
    irregularidad = message.text
    bot.send_message(
        message.chat.id,
        'Gracias por notificar su irregularidad,'
        'trabajaremos arduamente para corregir estos asuntos')


def process_guardar_respuesta(message):
    try:
        respuesta = message.text
        if respuesta not in ['1', '2', '3']:
            bot.send_message(
                message.chat.id,
                'Entendemos tu discrecion \n'
                'Gracias por responder!')
        else:
            bot.send_message(
                message.chat.id,
                'Su respuesta fue: ' + respuesta + '\n Muchas gracias'
                'por colaborar, seguiremos mejorando gracias a usted!')
    except Exception as e:
        bot.send_message(message.chat.id, 'oooooops')

bot.polling(none_stop=True)
