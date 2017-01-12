# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class Campaign(models.Model):
    _name = 'btoc.campaign'

    name = fields.Char(required=True)
    message_ids = fields.One2many(
        'btoc.message', 'campaign_id', string="Messages")
    date = fields.Datetime(default=fields.Date.today())
    