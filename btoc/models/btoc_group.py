# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class Group(models.Model):
    _name = 'btoc.group'

    name = fields.Char()
    user_ids = fields.Many2many(
        'res.partner',
        string='Users')
