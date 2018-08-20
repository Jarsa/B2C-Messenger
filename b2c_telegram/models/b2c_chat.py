# Copyright 2018, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models
from .b2c_bot import B2CBotTelegram


class B2CChat(models.Model):
    _inherit = 'b2c.chat'

    @api.multi
    @api.returns('self', lambda value: value.id)
    def message_post(self, body='', subject=None, message_type='notification',
                     subtype=None, parent_id=False, attachments=None,
                     content_subtype='html', **kwargs):
        if self._context.get('default_model') == 'b2c.chat':
            bot_base = self.env['b2c.base'].search(
                [('token', '=', self.bot_token)])
            bot = B2CBotTelegram(self.bot_token).get_bot()
            if bot:
                bot.bot.send_message(self.chat_id, body)
        return super().message_post(
            body, subject, message_type, subtype, parent_id,
            attachments, content_subtype, **kwargs)
