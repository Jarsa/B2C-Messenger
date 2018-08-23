# Copyright 2018, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models


class B2CChat(models.Model):
    _name = 'b2c.chat'
    _description = 'Chat'
    _inherit = ['mail.thread']

    name = fields.Char(string='Name',)
    chat_id = fields.Char(string='ID Conversation',)
    provider = fields.Char(string='Provider',)
    workflow_id = fields.Many2one('b2c.workflow', string='Bot Workflow',)
    bot_token = fields.Char()

    @api.model
    def create_message(self, action):
        msj = action.message
        if action.image:
            msj = (action.message +
                   " <br/> <img src='data:image/png;base64," +
                   action.image.decode('utf-8') + "' />")
        return msj
