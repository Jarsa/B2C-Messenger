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
        ('attachment', 'Attachment'),
        ('video', 'Video'),
        ('audio', 'Audio')], string='Telegram Action',
        default='texts', required=True,)
    image = fields.Binary(string='Image', attachment=True)
    text_in_chat = fields.Boolean(
        string='Text of Seleccion in Chat',
    )
    provider = fields.Selection(selection_add=[("telegram", "Telegram")],)
    element_keyboard = fields.Integer(
        string='Quntity of element for Keyboard',
        default=3
    )
    send_location = fields.Boolean(string='Is Location',)
    send_contact = fields.Boolean(string='Is Contact',)
