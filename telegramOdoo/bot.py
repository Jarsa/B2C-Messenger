# # -*- coding: utf-8 -*-
import time

import telebot
from telebot import types

API_TOKEN = '308245102:AAHojngXIJ9yTolBgVi8rycd-SFsUjJKs4o'

tor = telebot.TeleBot(API_TOKEN)

@tor.message_handler(commands=['start'])
def comando_bienvenida(mensaje):
    chat_id = mensaje.chat.id
    markup = types.ReplyKeyboardMarkup()
    itembtn1 = types.KeyboardButton('Checar mis puntos')
    itembtn2 = types.KeyboardButton('Realizar encuesta')
    itembtn3 = types.KeyboardButton('Solicitar factura')
    itembtn4 = types.KeyboardButton('Notificar irregularidad')
    itembtn5 = types.KeyboardButton('Checar vencimiento de productos')
    markup.row(itembtn1, itembtn2)
    markup.row(itembtn3, itembtn4)
    markup.row(itembtn5)
    tor.send_message(
        chat_id,
        'Hola! ¡Bienvenido a btoc messenger! Me llamo b-2 '
        'y sere tu bot asistente ¿Que deseeas realizar?',
        reply_markup=markup)

@tor.message_handler(func=lambda message: message.text == 'Solicitar factura')
def solicitar_factura(message):
    markup = types.ReplyKeyboardMarkup()
    affirmative = types.KeyboardButton('Si, claro que quiero!')
    negative = types.KeyboardButton('No, gracias!')
    markup.row(affirmative)
    markup.row(negative)
    question = tor.send_message(
        message.chat.id,
        'Al parecer tus datos no estan registrados en nuestro sistema.\n'
        '¿Te parece bien que comencemos el registro unico para guardar tu'
        ' informacion?', reply_markup=markup)
    tor.register_next_step_handler(question, process_confirmation_step)

def process_confirmation_step(message):
    chat_id = message.chat.id
    if message.text == 'Si, claro que quiero!':
        name = tor.send_message(chat_id, '¿A que nombre voy a facturar?')
        tor.register_next_step_handler(name, process_name_step)
    else:
        tor.send_message(chat_id, 'Si quiere.')

def process_name_step(message):
    chat_id = message.chat.id
    name = message.text
    calle = tor.send_message(chat_id, '¿A que calle voy a facturar?')
    tor.register_next_step_handler(calle, process_calle_step)

def process_calle_step(message):
    try:
        chat_id = message.chat.id
        calle = message.text
        num_int = tor.send_message(chat_id, '¿Cual es el numero interior?')
        tor.register_next_step_handler(num_int, procces_numero_int_step)
    except Exception as e:
        tor.send_message(message, 'ooooops')

def procces_numero_int_step(message):
    try:
        chat_id = message.chat.id
        numero_int = message.text
        numero_ext = tor.send_message(chat_id, '¿Cual es el numero exterior?')
        tor.register_next_step_handler(numero_ext, process_numero_ext_step)
    except Exception as e:
        tor.send_message(message, 'ooooops')

def process_numero_ext_step(message):
    try:
        chat_id = message.chat.id
        numero_ext = message.text
        colonia = tor.send_message(chat_id, '¿Cual es tu colonia?')
        tor.register_next_step_handler(colonia, process_colonia_step)
    except Exception as e:
        tor.send_message(message, 'ooooops')

def process_colonia_step(message):
    try:
        chat_id = message.chat.id
        colonia = message.text
        localidad = tor.send_message(chat_id, '¿Cual es tu localidad?')
        tor.register_next_step_handler(localidad, process_localidad_step)
    except Exception as e:
        tor.send_message(message, 'ooooops')

def process_localidad_step(message):
    try:
        chat_id = message.chat.id
        localidad = message.text
        ciudad = tor.send_message(chat_id, '¿Cual es tu ciudad?')
        tor.register_next_step_handler(ciudad, process_ciudad_step)
    except Exception as e:
        tor.send_message(message, 'ooooops')

def process_ciudad_step(message):
    try:
        chat_id = message.chat.id
        colonia = message.text
        estado = tor.send_message(chat_id, '¿Cual es tu estado?')
        tor.register_next_step_handler(estado, procces_estado_step)
    except Exception as e:
        tor.send_message(message, 'ooooops')

def procces_estado_step(message):
    try:
        chat_id = message.chat.id
        estado = message.text
        codigo_postal = tor.send_message(chat_id, '¿Cual es tu codigo postal?')
        tor.register_next_step_handler(
            codigo_postal,
            procces_codigo_postal_step)
    except Exception as e:
        tor.send_message(message, 'ooooops')

def procces_codigo_postal_step(message):
    try:
        chat_id = message.chat.id
        codigo_postal = message.text
        markup = types.ReplyKeyboardMarkup()
        inciso_moral = types.KeyboardButton('Persona moral')
        inciso_fisica = types.KeyboardButton('Persona fisica')
        inciso_no_luc = types.KeyboardButton('Asociaciones no lucrativas')
        inciso_sin_luc = types.KeyboardButton('Persona moral sin fin de lucro')
        markup.row(inciso_moral)
        markup.row(inciso_fisica)
        markup.row(inciso_no_luc)
        markup.row(inciso_sin_luc)
        regimen_fiscal = tor.send_message(
            chat_id, '¿Cual es tu regimen fiscal?', reply_markup=markup)
        tor.register_next_step_handler(regimen_fiscal, process_regimen_fiscal)
    except Exception as e:
        tor.send_message(message, 'ooooops')

def process_regimen_fiscal(message):
    try:
        chat_id = message.chat.id
        regimen = message.text
        razon_social = tor.send_message(chat_id, '¿Cual es tu rfc?')
        tor.register_next_step_handler(razon_social, procces_rfc_step)
    except Exception as e:
        tor.send_message(message, 'ooooops')

def procces_rfc_step(message):
    try:
        chat_id = message.chat.id
        rfc = message.text
        tor.send_message(
            chat_id,
            'Excelente, has terminado '
            'de guardar tu informacion!')
    except Exception as e:
        tor.send_message(message, 'ooooops')

@tor.message_handler(func=lambda message: message.text == 'Checar mis puntos')
def handle_checar_puntos(message):
    markup = types.ReplyKeyboardMarkup()
    inciso_a = types.KeyboardButton('Si')
    inciso_b = types.KeyboardButton('No')
    inciso_c = types.KeyboardButton('Tal vez')
    inciso_d = types.KeyboardButton('Prefiero no contestar')
    markup.row(inciso_a, inciso_b)
    markup.row(inciso_c, inciso_d)
    tor.send_message(
        message.chat.id,
        'Hola' + message.chat.first_name + ', actualmente cuentas con una'
        ' cantidad de 29 puntos, con los cuales puedes realizar compras en'
        ' alguno nuestros siguientes departamentos')

@tor.message_handler(func=lambda message: message.text == 'Realizar encuesta')
def handle_realizar_encuesta(message):
    markup = types.ReplyKeyboardMarkup()
    inciso_a = types.KeyboardButton('1')
    inciso_b = types.KeyboardButton('2')
    inciso_c = types.KeyboardButton('3')
    inciso_d = types.KeyboardButton('Prefiero no contestar')
    markup.row(inciso_a, inciso_b)
    markup.row(inciso_c, inciso_d)
    respuesta = tor.send_message(
        message.chat.id,
        'ENCUESTA DE SATISFACCION \nEstimado Cliente, rogamos su valiosa '
        'ayuda para calificar el servicio que ha recibido del promotor que la '
        'atiende en nuestra representación (Sr, Juan Martínez Pérez), en la '
        'breve encuesta que le enviamos anexa en este mensaje, por favor solo '
        'con el numero de la respuesta que elija.\n\n'
        'El promotor, Sr Juan Martínez Pérez: \n1.- Acude puntualmente a las '
        'reuniones, me proporciona toda la información que le solicito, me tra'
        'ta amablemente \n2.- Acude a veces a las reuniones, hay información '
        'que le solicite que no me da, a veces es amable. \n3.- Seguido no '
        'acude a las reuniones, constantemente no me da la información que le '
        'solicito, es grosero ', reply_markup=markup)
    tor.register_next_step_handler(respuesta, process_guardar_respuesta)

def process_guardar_respuesta(message):
    try:
        respuesta = message.text
        if respuesta not in ['1', '2', '3']:
            tor.send_message(
                message.chat.id,
                'Entendemos tu discrecion \n'
                'Gracias por responder!')
            pass
        tor.send_message(
            message.chat.id,
            'Su respuesta fue: ' + respuesta + '\n Muchas gracias'
            'por colaborar, seguiremos mejorando gracias a usted!')
    except Exception as e:
        tor.send_message(message.chat.id, 'oooooops')

tor.polling(none_stop=True)
