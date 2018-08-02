# Copyright 2018, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class B2CWorkflow(models.Model):
    _inherit = 'b2c.workflow'

    provider = fields.Selection(selection_add=[("telegram", "Telegram")],)


class B2CWorkflowLine(models.Model):
    _inherit = 'b2c.workflow.line'

    telegram_action = fields.Selection([
        ('texts', 'Texts'),
        ('selection', 'Selection'),
        ('image', 'Image'),
        ('attachment', 'Attachment')], string='Telegram Action',
        default='texts', required=True,)
    image = fields.Binary(string='Image', attachment=True)
    provider = fields.Selection(selection_add=[("telegram", "Telegram")],)
