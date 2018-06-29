# Copyright 2018, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class B2CBase(models.Model):
    _name = 'b2c.base'

    name = fields.Char(required=True)
    active = fields.Boolean('Active', default=True)
    image = fields.Binary(
        "Photo", attachment=True)
    token = fields.Char(string="Token Bot")
    color = fields.Integer('Color Index', default=0)
    provider = fields.Selection([],)
    workflow_ids = fields.One2many(
        comodel_name='b2c.workflow',
        inverse_name='b2c_base_id',
        help='Field used to design the workflow of the bot.')

    @api.multi
    def action_set_active(self):
        self.ensure_one()
        return self.write({'active': True})

    @api.multi
    def action_set_unactive(self):
        self.ensure_one()
        return self.write({'active': False})
