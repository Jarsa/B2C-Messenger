# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class BtocUser(models.Model):
    _inherit = 'res.partner'

    telegram_id = fields.Char(string='Telegram chat identifier')
    whatsapp_confirm = fields.Boolean()
    whatsapp_confidential = fields.Boolean()
    telegram_confirm = fields.Boolean()
    telegram_confidential = fields.Boolean()
    sms_confirm = fields.Boolean()
    sms_confidential = fields.Boolean()
    facebook = fields.Char()
    facebook_confirm = fields.Boolean()
    facebook_confidential = fields.Boolean()
    twitter = fields.Char()
    twitter_confirm = fields.Boolean()
    twitter_confidential = fields.Boolean()
    skype = fields.Char()
    skype_confirm = fields.Boolean()
    skype_confidential = fields.Boolean()
