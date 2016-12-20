# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api


class Messenger(models.Model):
    _name = 'btoc.messenger'

    campaign_id = fields.Many2one(
        'btoc.campaign', required=True, string="Campaign")
    contact_ids = fields.Many2many(
        'res.partner', string="Contact(s)", required=True)
    message_id = fields.Many2one(
        'btoc.message', string="Message Name", required=True)
    message = fields.Char(compute="_get_message")

    @api.depends('message_id')
    def _get_message(self):
        for rec in self:
            rec.message = rec.message_id.message
