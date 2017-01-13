# -*- coding: utf-8 -*-
# Copyright 2016, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError
from openerp.service.telegram import BOT


class BtocGroupMessage(models.TransientModel):
    _name = 'btoc.group.message'

    group_ids = fields.Many2one('btoc.group', string='Group')
    message = fields.Text(size=200)

    @api.multi
    def send_message(self):
        for rec in self:
            try:
                for user in rec.group_ids.user_ids:
                    BOT.send_message(
                        chat_id=user.telegram_id,
                        text=rec.message,
                        parse_mode='HTML')
            except:
                raise ValidationError(
                    _("Fatal error, don't worry. "
                        "Please contact to your system administrator"))
