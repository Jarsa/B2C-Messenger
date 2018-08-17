# Copyright 2018, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

import odoorpc
import telegram

from odoo.tools import config
from odoo import api, fields, models, registry, sql_db, SUPERUSER_ID
from odoo.addons.b2c_base.models.b2c_bot import B2CBot
from odoo.service import db, server
from odoo.tools import config
from telegram.ext import *

_logger = logging.getLogger(__name__)


class B2CBotTelegram(B2CBot):

    def get_bot(self):
        return Updater(self.token)

    def e_method(self, handler, bot, update):
        db_registry = registry(config['db_name'])
        with api.Environment.manage(), db_registry.cursor() as cr:
            env = api.Environment(cr, SUPERUSER_ID, {})
            b2c_base = env['b2c.base']
            b2c_base.set_actions(handler, self.token, bot, update)

    def start(self, bot, update):
        bot_id = update.message.from_user.id
        name = update.message.from_user.full_name
        db_registry = registry(config['db_name'])
        with api.Environment.manage(), db_registry.cursor() as cr:
            env = api.Environment(cr, SUPERUSER_ID, {})
            obj_partner = env['res.partner']
            partner = obj_partner.search([('bot_id', '=', bot_id)])
            if not partner:
                obj_partner.create({
                    'name': name,
                    'bot_id': bot_id,
                })
        self.e_method('/start', bot, update)

    def listener(self, bot, update):
        chat_id = update.message.chat_id
        message = update.message.text
        self.e_method(message, bot, update)
        print('ID: ' + str(chat_id) + ' Message: ' + message)

    def button(self, bot, update):
        query = update.callback_query
        chat_id = query.message.chat_id
        message = query.data
        self.e_method(message, bot, update)

    def start_polling(self):
        token = self.token
        updater = Updater(token)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CallbackQueryHandler(self.button))
        dp.add_handler(MessageHandler(Filters.text, self.listener))

        # Start the Bot
        updater.start_polling()
        _logger.info("Starting Telegram Bot with Token %s" % (self.token))

    def stop_polling(self):
        updater = Updater(self.token)
        updater.job_queue.stop()
        updater.stop()
        _logger.info(
            "Graceful stop requested. STelegram Bot with token %s stopped." % (
                self.token))
