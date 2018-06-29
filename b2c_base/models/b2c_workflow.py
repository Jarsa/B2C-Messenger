# Copyright 2018, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class B2CWorkflow(models.Model):
    _name = 'b2c.workflow'

    b2c_base_id = fields.Many2one(
        comodel_name='b2c.base',)
    handler = fields.Char(
        help='Field to express the user input',)
    action = fields.Char(
        help='Field to express the action triggered by the handler',)
