# -*- coding: utf-8 -*-
# Copyright 2016, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
from openerp.service.telegram import BOT

class BtocIndividualMessage(models.TransientModel):
    _name = 'btoc.individual.message'

    user_id = fields.Many2one('res.partner', string='User')
    message = fields.Text(size=200)

    @api.multi
    def send_message(self):
        for rec in self:
            BOT.send_message(
                chat_id=rec.user_id.telegram_id,
                text=rec.message,
                parse_mode='HTML')
