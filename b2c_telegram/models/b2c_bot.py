# Copyright 2018, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

from telegram.ext import CommandHandler, Updater
from odoo.addons.b2c_base.models.b2c_bot import B2CBot

_logger = logging.getLogger(__name__)


class B2CBotTelegram(B2CBot):

    def hello(self, bot, update):
        update.message.reply_text(
            'Hello {}'.format(update.message.from_user.first_name))

    def start_polling(self):
        updater = Updater(self.token)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", self.hello))
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

    def create_handler(self, handler, action, dp):
        dp.add_handler(CommandHandler(handler, action))
