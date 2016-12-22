# -*- coding: utf-8 -*-

import logging
import openerp
from openerp import SUPERUSER_ID
from telebot import types
from openerp.modules.registry import RegistryManager
from openerp.api import Environment

_logger = logging.getLogger("[TELEGRAM_HANDLERS]")


class TelegramBotHandlers(object):

    def __init__(self, bot):
        self.bot = bot
        self.uid = SUPERUSER_ID
        self.context = {}

    def handle(self):
        args = ['-d', 'test']
        openerp.tools.config.parse_config(args)

        r = RegistryManager.get('test')
        cr = r.cursor()
        Environment.reset()
        env = Environment(cr, SUPERUSER_ID, context={})
        _logger.info('TelegramBOTHandlers: handle -> %r' % (self.bot))
        BOT = self.bot

        @BOT.message_handler(commands=['start'])
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
            BOT.send_message(
                chat_id,
                'Hola! ¡Bienvenido a btoc messenger! Me llamo b-2 '
                'y sere tu BOT asistente ¿Que deseeas realizar?',
                reply_markup=markup)

        @BOT.message_handler(
            func=lambda message: message.text == 'Solicitar factura')
        def solicitar_factura(message):
            markup = types.ReplyKeyboardMarkup()
            affirmative = types.KeyboardButton('Si, claro que quiero!')
            negative = types.KeyboardButton('No, gracias!')
            markup.row(affirmative)
            markup.row(negative)
            question = BOT.send_message(
                message.chat.id,
                'Al parecer tus datos no estan registrados en nuestro '
                'sistema.\n ¿Te parece bien que comencemos el registro'
                ' unico para guardar tu informacion?',
                reply_markup=markup)
            BOT.register_next_step_handler(question, process_confirmation_step)

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
                name = BOT.send_message(
                    chat_id,
                    '¿A que nombre voy a facturar?')
                BOT.register_next_step_handler(name, process_name_step)
            else:
                BOT.send_message(
                    chat_id, 'Esta bien. ¿Alguna '
                    'cosa mas en la que pueda ayudarle?', reply_markup=markup)

        def process_name_step(message):
            markup_hide = types.ReplyKeyboardRemove(selective=False)
            chat_id = message.chat.id
            name = message.text
            calle = BOT.send_message(
                chat_id,
                '¿A que calle voy a facturar?',
                reply_markup=markup_hide)
            BOT.register_next_step_handler(calle, process_calle_step)

        def process_calle_step(message):
            try:
                chat_id = message.chat.id
                calle = message.text
                num_int = BOT.send_message(
                    chat_id,
                    '¿Cual es el numero interior?')
                BOT.register_next_step_handler(
                    num_int, procces_numero_int_step)
            except Exception as e:
                BOT.send_message(message, 'ooooops')

        def procces_numero_int_step(message):
            try:
                chat_id = message.chat.id
                numero_int = message.text
                if numero_int.isdigit() or numero_int.upper() == 'N/A':
                    numero_ext = BOT.send_message(
                        chat_id,
                        '¿Cual es el '
                        'numero exterior?')
                    BOT.register_next_step_handler(
                        numero_ext,
                        process_numero_ext_step)
                else:
                    numero_int = BOT.send_message(
                        chat_id,
                        'El numero interior debe de ser un '
                        'numero. \n¿Cual es tu numero interior?')
                    BOT.register_next_step_handler(
                        numero_int,
                        procces_numero_int_step)
            except Exception as e:
                BOT.send_message(message, 'ooooops')

        def process_numero_ext_step(message):
            try:
                chat_id = message.chat.id
                numero_ext = message.text
                if not numero_ext.isdigit():
                    numero_ext = BOT.send_message(
                        chat_id,
                        'El numero exterior debe de ser '
                        'un numero. \n¿Cual es tu numero exterior?')
                    BOT.register_next_step_handler(
                        numero_ext,
                        process_numero_ext_step)
                else:
                    colonia = BOT.send_message(chat_id, '¿Cual es tu colonia?')
                    BOT.register_next_step_handler(
                        colonia,
                        process_colonia_step)
            except Exception as e:
                BOT.send_message(message, 'ooooops')

        def process_colonia_step(message):
            try:
                chat_id = message.chat.id
                colonia = message.text
                localidad = BOT.send_message(chat_id, '¿Cual es tu localidad?')
                BOT.register_next_step_handler(
                    localidad, process_localidad_step)
            except Exception as e:
                BOT.send_message(message, 'ooooops')

        def process_localidad_step(message):
            try:
                chat_id = message.chat.id
                localidad = message.text
                ciudad = BOT.send_message(chat_id, '¿Cual es tu ciudad?')
                BOT.register_next_step_handler(ciudad, process_ciudad_step)
            except Exception as e:
                BOT.send_message(message, 'ooooops')

        def process_ciudad_step(message):
            try:
                chat_id = message.chat.id
                colonia = message.text
                estado = BOT.send_message(chat_id, '¿Cual es tu estado?')
                BOT.register_next_step_handler(estado, procces_estado_step)
            except Exception as e:
                BOT.send_message(message, 'ooooops')

        def procces_estado_step(message):
            try:
                chat_id = message.chat.id
                estado = message.text
                codigo_postal = BOT.send_message(chat_id, '¿Cual es tu'
                    ' codigo postal?')
                BOT.register_next_step_handler(
                    codigo_postal,
                    procces_codigo_postal_step)
            except Exception as e:
                BOT.send_message(message, 'ooooops')

        def procces_codigo_postal_step(message):
            try:
                chat_id = message.chat.id
                codigo_postal = message.text
                if not codigo_postal.isdigit():
                    codigo_postal = BOT.send_message(
                        chat_id,
                        'El codigo postal no tiene letras. '
                        '¿Cual es tu codigo postal?')
                    BOT.register_next_step_handler(
                        codigo_postal, procces_codigo_postal_step)
                else:
                    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                    inciso_moral = types.KeyboardButton(
                        'Persona moral')
                    inciso_fisica = types.KeyboardButton(
                        'Persona fisica')
                    inciso_no_luc = types.KeyboardButton(
                        'Asociaciones no lucrativas')
                    inciso_sin_luc = types.KeyboardButton(
                        'Persona moral sin fin de lucro')
                    markup.row(inciso_moral)
                    markup.row(inciso_fisica)
                    markup.row(inciso_no_luc)
                    markup.row(inciso_sin_luc)
                    regimen_fiscal = BOT.send_message(
                        chat_id,
                        '¿Cual es tu regimen fiscal?',
                        reply_markup=markup)
                    BOT.register_next_step_handler(
                        regimen_fiscal, process_regimen_fiscal)
            except Exception as e:
                BOT.send_message(message, 'ooooops')

        def process_regimen_fiscal(message):
            try:
                markup_hide = types.ReplyKeyboardRemove(selective=False)
                chat_id = message.chat.id
                regimen = message.text
                razon_social = BOT.send_message(
                    chat_id,
                    '¿Cual es tu rfc?',
                    reply_markup=markup_hide)
                BOT.register_next_step_handler(razon_social, procces_rfc_step)
            except Exception as e:
                BOT.send_message(message, 'ooooops')

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
                    itembtn1 = types.KeyboardButton(
                        'Solicitar factura')
                    itembtn2 = types.KeyboardButton(
                        'Notificacion de puntos ganados')
                    itembtn3 = types.KeyboardButton(
                        'Checar vencimiento de productos')
                    itembtn4 = types.KeyboardButton(
                        'Consulta de saldos')
                    itembtn5 = types.KeyboardButton(
                        'Notificar irregularidad')
                    itembtn6 = types.KeyboardButton(
                        'Realizar encuesta')
                    itembtn7 = types.KeyboardButton(
                        'Calificacion de servicios')
                    markup.row(itembtn1, itembtn2, itembtn3)
                    markup.row(itembtn4, itembtn5, itembtn6)
                    markup.row(itembtn7)
                    BOT.send_message(
                        chat_id,
                        'Excelente, has terminado '
                        'de guardar tu informacion! ¿Alguna otra cosa en '
                        'la que te pueda ayudar?',
                        reply_markup=markup)
                else:
                    BOT.send_message(
                        chat_id,
                        'Los primeros 4 digitos de tu RFC parecen '
                        'estar mal. Recuerda que primero son 4 digitos'
                        ' solamente, letras no')
            except Exception as e:
                BOT.send_message(message, 'ooooops')

        @BOT.message_handler(
            func=lambda message: message.text ==
            'Notificacion de puntos ganados')
        def handle_notificacion_puntos(message):
            BOT.send_message(
                message.chat.id,
                'Estimado ' + str(message.chat.first_name) + ', gracias '
                'por su compra, le informamos que con esta operación '
                'le hemos abonado a su tarjeta de lealtad '
                'la cantidad de 357 puntos, quedando hoy con un saldo a su fa'
                'vor de 1, 345 puntos, le esperamos nuevamente en'
                ' nuestras tiendas.')

        @BOT.message_handler(
            func=lambda message: message.text ==
            'Checar vencimiento de productos')
        def handle_consulta_saldo(message):
            BOT.send_message(
                message.chat.id,
                'Estimado ' + str(message.chat.first_name) + ', Ud '
                'dispone de un saldo acumulado en su tarjeta ' +
                str(message.chat.id) + ' de 1345 puntos, y puede ap'
                'licarlos en la compra de nuestras promociones como'
                ':\n\nLínea electrónica, \nSamsung, \nLG \nSony\n '
                'aproveche el 20 % solo hasta el 30 de Octubre del'
                ' 2015, fecha en la que expiran sus puntos acumulados. '
                'Gracias por su preferencia')

        @BOT.message_handler(
            func=lambda message: message.text == 'Consulta de saldos')
        def handle_checar_puntos(message):
            BOT.send_message(
                message.chat.id,
                'Hola ' + message.chat.first_name + ', actualmente cuentas'
                ' con una cantidad de 29 puntos, con los cuales puedes re'
                'alizar compras en alguno nuestros siguientes departamentos')

        @BOT.message_handler(
            func=lambda message: message.text == 'Notificar irregularidad')
        def handle_notificar_irregularidad(message):
            irregularidad = BOT.send_message(
                message.chat.id,
                'Estimado ' + str(message.chat.first_name) + ', A continu'
                'acion digame como, cuando y donde fue que tuvo una regul'
                'aridad dentro de nuestras tiendas')
            BOT.register_next_step_handler(
                irregularidad, procces_notificar_irregularidad)

        @BOT.message_handler(
            func=lambda message: message.text == 'Realizar encuesta')
        def handle_realizar_encuesta(message):
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            inciso_a = types.KeyboardButton('1')
            inciso_b = types.KeyboardButton('2')
            inciso_c = types.KeyboardButton('3')
            inciso_d = types.KeyboardButton('Prefiero no contestar')
            markup.row(inciso_a, inciso_b)
            markup.row(inciso_c, inciso_d)
            ticket = open('/home/hector/Documentos/Jarsa_sistemas'
                          '/B2C-Messenger/telegramOdoo/Picture1.jpg', 'rb')
            BOT.send_photo(message.chat.id, ticket)
            respuesta = BOT.send_message(
                message.chat.id,
                'ENCUESTA DE SATISFACCION \nEstimado Cliente,'
                ' rogamos su valiosa ayuda para calificar el '
                'servicio que ha recibido del promotor que la '
                'atiende en nuestra representación (Sr, Juan '
                'Martínez Pérez), en la breve encuesta que le '
                'enviamos anexa en este mensaje, por favor solo '
                'con el numero de la respuesta que elija.\n\n'
                'El promoBOT, Sr Juan Martínez Pérez: \n1.- Acu'
                'de puntualmente a las reuniones, me proporcion'
                'a toda la información que le solicito, me trat'
                'a amablemente \n2.- Acude a veces a las reunio'
                'nes, hay información que le solicite que no me'
                ' da, a veces es amable. \n3.- Seguido no acude'
                ' a las reuniones, constantemente no me da la i'
                'nformación que le solicito, es grosero ',
                reply_markup=markup)
            BOT.register_next_step_handler(
                respuesta,
                process_guardar_respuesta)

        def procces_notificar_irregularidad(message):
            irregularidad = message.text
            BOT.send_message(
                message.chat.id,
                'Gracias por notificar su irregularidad,'
                'trabajaremos arduamente para corregir estos asuntos')

        def process_guardar_respuesta(message):
            try:
                markup = types.ReplyKeyboardMarkup()
                itembtn1 = types.KeyboardButton(
                    'Solicitar factura')
                itembtn2 = types.KeyboardButton(
                    'Notificacion de puntos ganados')
                itembtn3 = types.KeyboardButton(
                    'Checar vencimiento de productos')
                itembtn4 = types.KeyboardButton(
                    'Consulta de saldos')
                itembtn5 = types.KeyboardButton(
                    'Notificar irregularidad')
                itembtn6 = types.KeyboardButton(
                    'Realizar encuesta')
                itembtn7 = types.KeyboardButton(
                    'Calificacion de servicios')
                markup.row(itembtn1, itembtn2, itembtn3)
                markup.row(itembtn4, itembtn5, itembtn6)
                markup.row(itembtn7)
                respuesta = message.text
                if respuesta not in ['1', '2', '3']:
                    BOT.send_message(
                        message.chat.id,
                        'Entendemos tu discrecion \n'
                        'Gracias por responder!', reply_markup=markup)
                else:
                    BOT.send_message(
                        message.chat.id,
                        'Su respuesta fue: ' + respuesta + '\n Muchas gracias'
                        'por colaborar, seguiremos mejorando gracias a usted!',
                        reply_markup=markup)
            except Exception as e:
                BOT.send_message(message.chat.id, 'oooooops')
