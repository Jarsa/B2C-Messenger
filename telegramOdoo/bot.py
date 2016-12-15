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
    markup.row(itembtn1, itembtn2)
    markup.row(itembtn3, itembtn4)
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
    tor.register_next_step_handler(question, process_name_step)

def process_name_step(message):
    chat_id = message.chat.id
    if message.text == 'Si, claro que quiero!':
        calle = tor.send_message(chat_id, '¿A que calle voy a facturar?')
        tor.register_next_step_handler(calle, process_calle_step)
    else:
        tor.send_message(chat_id, 'Si quiere.')

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
        regimen_fiscal = tor.send_message(
            chat_id, '¿Cual es tu regimen fiscal?')
        tor.register_next_step_handler(regimen_fiscal, process_regimen_fiscal)
    except Exception as e:
        tor.send_message(message, 'ooooops')

def process_regimen_fiscal(message):
    try:
        chat_id = message.chat.id
        regimen = message.text
        razon_social = tor.send_message(chat_id, '¿Cual es tu razon social?')
        tor.register_next_step_handler(razon_social, process_razon_social)
    except Exception as e:
        tor.send_message(message, 'ooooops')

def process_razon_social(message):
    try:
        chat_id = message.chat.id
        razon_social = message.text
        rfc = tor.send_message(chat_id, '¿Cual es tu RFC?')
        tor.register_next_step_handler(rfc, procces_rfc_step)
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
def handle_text_doc(message):
    tor.send_message(
        message.chat.id,
        'Hola' + message.chat.first_name + ', actualmente cuentas con una'
        ' cantidad de 29 puntos, con los cuales puedes realizar compras en'
        ' alguno nuestros siguientes departamentos')

tor.polling(none_stop=True)
