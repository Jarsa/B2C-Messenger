# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class Message(models.Model):
    _name = 'btoc.message'

    name = fields.Char(required=True)
    message = fields.Text()
    campaign_id = fields.Many2one(
        'btoc.campaign', required=True, string="Campaign")
    color = fields.Integer()
