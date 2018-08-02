# Copyright 2018, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
import json
from time import sleep

import telegram
from io import BytesIO
from odoo import api, fields, models
from telegram.ext import *

HANDLERS = {
    'texts': 'create_text',
    'selection': 'create_selection',
    'image': 'send_image',
    'attachment': 'send_document'
}


class B2CBase(models.Model):
    _name = 'b2c.base'

    name = fields.Char(required=True)
    active = fields.Boolean('Active', default=True)
    image = fields.Binary(
        "Photo", attachment=True)
    token = fields.Char(string="Token Bot")
    color = fields.Integer('Color Index', default=0)
    provider = fields.Selection([],)
    workflow_ids = fields.Many2many(
        'b2c.workflow',
        string='Workflow',
        help='Field used to design the workflow of the bot.')
    last_workflow_id = fields.Many2one(
        'b2c.workflow.line',
        string='Last Workflow',
    )

    @api.multi
    def action_set_active(self):
        self.ensure_one()
        return self.write({'active': True})

    @api.multi
    def action_set_unactive(self):
        self.ensure_one()
        return self.write({'active': False})

    def set_workflows(self):
        print('hi')

    @api.model
    def get_actions(self, action, token, bot, update, handler=''):
        data_bot = self.environment_variables(update)
        if not action:
            action = self.workflow_ids.mapped('step_line_ids').with_context(
                last_workflow=self.last_workflow_id).filtered(
                lambda w: w.previus_step_id == w._context.get('last_workflow'))
        if not action:
            return False
        data = {
            'message': action.message,
            'delay': action.delay,
            'img': action.image,
            'attachment': action.attachment,
            'file_name': action.file_name,
            'update': update,
            'bot': bot,
            'chat_id': data_bot['chat_id'],
        }
        if action.action == 'code' and action.telegram_action == 'selection':
            data['items'] = action.method_direct_trigger()

        if hasattr(self, HANDLERS[action.telegram_action]):
            getattr(self, HANDLERS[action.telegram_action])(data_bot, data)
            self.last_workflow_id = action.id
            if action.next_step_id:
                return self.get_actions(
                    action.next_step_id, token, bot, update)

    def set_actions(self, handler, token, bot, update):
        self = self.search([('token', '=', token)])
        action = self.workflow_ids.mapped('step_line_ids').with_context(
            handler=handler).filtered(
            lambda w: w.handler == w._context.get('handler').lower())
        return self.get_actions(action, token, bot, update, handler)

    def create_text(self, data_bot, data):
        for key in data_bot.keys():
            if key in data['message']:
                data['message'] = data['message'].replace(key, data_bot[key])
        sleep(data['delay'])
        method = 'create_text_%s' % self.provider
        if hasattr(self, method):
            getattr(self, method)(data)

    def send_image(self, data_bot, data):
        self.create_text(data_bot, data)
        method = 'send_image_%s' % self.provider
        if hasattr(self, method):
            getattr(self, method)(data)

    def send_document(self, data_bot, data):
        self.create_text(data_bot, data)
        method = 'send_document_%s' % self.provider
        if hasattr(self, method):
            getattr(self, method)(data)

    def create_selection(self, data_bot, data):
        custom_keyboard = self.build_keyboard(data['items'], data)
        sleep(data['delay'])
        method = 'create_selection_%s' % self.provider
        data['custom_keyboad'] = custom_keyboard
        if hasattr(self, method):
            getattr(self, method)(data)

    def build_keyboard(self, items, data):
        method = 'build_keyboard_%s' % self.provider
        if hasattr(self, method):
            custom_keyboard = getattr(self, method)(items)
        return custom_keyboard

    def environment_variables(self, update):
        method = 'environment_variables_%s' % self.provider
        if hasattr(self, method):
            env_variables = getattr(self, method)(update)
        return env_variables
