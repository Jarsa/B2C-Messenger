# Copyright 2018, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    bot_id = fields.Char()

    # def search_partner(self, bot_id, name):
    #     partner = self.search([('bot_id', '=', bot_id)])
    #     if not partner:
    #         self.create({
    #             'name': name,
    #             'bot_id': bot_id,
    #         })
