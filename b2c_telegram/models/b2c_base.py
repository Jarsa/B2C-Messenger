# Copyright 2018, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from .b2c_bot import B2CBotTelegram


class B2CBase(models.Model):
    _inherit = 'b2c.base'

    provider = fields.Selection(selection_add=[("telegram", "Telegram")])

    def set_actions(self):
        import ipdb; ipdb.set_trace()
        print('hi')