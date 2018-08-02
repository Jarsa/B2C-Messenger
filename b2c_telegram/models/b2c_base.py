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
        data['bot'].send_message(data['chat_id'], data['message'])

    def send_image_telegram(self, data):
        data['bot'].send_photo(
            data['chat_id'], BytesIO(base64.decodebytes(data['img'])))

    def create_selection_telegram(self, data):
        data['bot'].send_message(
            text=data['message'], chat_id=data['chat_id'],
            reply_markup=data['custom_keyboad'])

    def send_document_telegram(self, data):
        data['bot'].send_document(
            data['chat_id'], BytesIO(base64.decodebytes(data['attachment'])),
            data['file_name'])

    def build_keyboard_telegram(self, items):
        keyboard = [telegram.KeyboardButton(
            text=item) for item in items]
        reply_keyboard = []
        for index in range(0, len(keyboard), 3):
            reply_keyboard.append(keyboard[index:index+3])
        return telegram.ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True)

    def environment_variables_telegram(self, update):
        return {
            '$date': fields.Datetime.to_string(update.message.date),
            '$name': update.message.from_user.full_name,
            'chat_id': update.message.chat_id,
            '$number': self.env['res.partner'].search(
                [('bot_id', '=', update.message.chat_id)
                 ]).mobile or '**-**-**-**-**',
        }
