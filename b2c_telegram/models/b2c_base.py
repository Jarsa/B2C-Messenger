# Copyright 2018, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
import json

from io import BytesIO
from odoo import api, fields, models
from telegram.ext import *
import telegram
from .b2c_bot import B2CBotTelegram


class B2CBase(models.Model):
    _inherit = 'b2c.base'

    provider = fields.Selection(selection_add=[("telegram", "Telegram")])

    def create_text_telegram(self, data):
        custom_keyboard = False
        if data['send_location'] and not data.get('items'):
            custom_keyboard = telegram.ReplyKeyboardMarkup(
                [[telegram.KeyboardButton(
                    text="Send Location", request_location=True)]],
                one_time_keyboard=True)
        if data['send_contact'] and not data.get('items'):
            custom_keyboard = telegram.ReplyKeyboardMarkup(
                [[telegram.KeyboardButton(
                    text="Send Contact", request_contact=True)]],
                one_time_keyboard=True)
        if data.get('items') and data['send_location']:
            address = self.get_coordinates(
                data['items']['name'],
                data['items']['state'],
                data['items']['country'])
            data['bot'].send_location(
                data['chat_id'],
                latitude=address['latitude'],
                longitude=address['longitude'])
        if data['text_in_chat']:
            reply_keyboard = self.build_keyboard_inline_telegram(data['items'])
            data['bot'].send_message(
                data['chat_id'], data['message'],
                reply_markup=reply_keyboard)
        else:
            data['bot'].send_message(
                data['chat_id'], data['message'], reply_markup=custom_keyboard)

    def send_image_telegram(self, data):
        data['bot'].send_photo(
            data['chat_id'], BytesIO(base64.decodebytes(data['img'])))

    def create_selection_telegram(self, data):
        if 'custom_keyboard' in data.keys():
            custom_keyboard = data['custom_keyboard']
        data['bot'].send_message(
            text=data['message'], chat_id=data['chat_id'],
            reply_markup=custom_keyboard)

    def send_document_telegram(self, data):
        data['bot'].send_document(
            data['chat_id'], BytesIO(base64.decodebytes(data['attachment'])),
            data['file_name'])

    def send_video_telegram(self, data):
        data['bot'].send_video(
            data['chat_id'],
            BytesIO(base64.decodebytes(data['attachment'])),
            timeout=50)

    def send_audio_telegram(self, data):
        data['bot'].send_audio(
            data['chat_id'],
            BytesIO(base64.decodebytes(data['attachment'])),
            title=data['file_name'],
            timeout=50)

    def build_keyboard_telegram(self, element, items):
        keyboard = [telegram.KeyboardButton(
            text=item or '') for item in items]
        reply_keyboard = []
        for index in range(0, len(keyboard), element):
            reply_keyboard.append(keyboard[index:index+element])
        return telegram.ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True)

    def build_keyboard_inline_telegram(self, items):
        keyboard = [telegram.InlineKeyboardButton(
            text=item, callback_data=item) for item in items]
        reply_keyboard = []
        for index in range(0, len(keyboard), 3):
            reply_keyboard.append(keyboard[index:index+3])
        return telegram.InlineKeyboardMarkup(
            reply_keyboard)

    def environment_variables_telegram(self, update):
        return {
            '$date': fields.Datetime.to_string(update.message.date),
            '$name': update.message.from_user.full_name,
            'chat_id': update.message.chat_id,
            '$number': self.env['res.partner'].search(
                [('bot_id', '=', update.message.chat_id)
                 ]).mobile or '**-**-**-**-**',
        }
