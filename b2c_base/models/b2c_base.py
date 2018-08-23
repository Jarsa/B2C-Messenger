# Copyright 2018, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
import json
import urllib.request
from time import sleep

import simplejson as json
import telegram
from io import BytesIO
from odoo import _, api, fields, models
from telegram.ext import *

HANDLERS = {
    'texts': 'create_text',
    'selection': 'create_selection',
    'image': 'send_image',
    'attachment': 'send_document',
    'video': 'send_video',
    'audio': 'send_audio',
}


class B2CBase(models.Model):
    _name = 'b2c.base'

    name = fields.Char(required=True)
    active = fields.Boolean('Active', default=True)
    image = fields.Binary(
        "Photo", attachment=True)
    token = fields.Char(string="Token Bot")
    provider = fields.Selection([],)
    workflow_ids = fields.Many2many(
        'b2c.workflow',
        string='Workflow',
        help='Field used to design the workflow of the bot.')
    last_workflow_id = fields.Many2one(
        'b2c.workflow.line',
        string='Last Workflow',
    )
    subscription_id = fields.Many2one(
        'sale.subscription',
        string='Sale Subscription',
    )

    @api.multi
    def action_set_active(self):
        self.ensure_one()
        return self.write({'active': True})

    @api.multi
    def action_set_unactive(self):
        self.ensure_one()
        return self.write({'active': False})

    @api.multi
    def set_workflows(self):
        return {
           'name': _('Workflow Lines'),
           'view_type': 'form',
           'view_mode': 'tree',
           'target': 'current',
           'res_model': 'b2c.workflow.line',
           'domain': [('workflow_id', 'in', self.workflow_ids.ids)],
           'type': 'ir.actions.act_window',
           'context': {
               'search_default_workflow_group_by': True,
               'create': False,
               'edit': False,
               'delete': False,
            }
        }

    @api.model
    def get_actions(self, action, token, bot, update, handler=''):
        data_bot = self.environment_variables(update)
        obj_chat = self.env['b2c.chat']
        chat_id = obj_chat.search([('chat_id', '=', data_bot['chat_id'])])
        if not chat_id:
            chat_id = obj_chat.create({
                'chat_id': data_bot['chat_id'],
                'provider': action.provider,
                'workflow_id': action.workflow_id.id,
                'bot_token': self.token,
            })
        if handler:
            chat_id.message_post(
                body=handler,
                author_id=self.env['res.partner'].search([
                    ('bot_id', '=', data_bot['chat_id'])]).id)
        if action.message:
            chat_id.message_post(
                body=obj_chat.create_message(action))
        if not action and self.last_workflow_id.wait_user_response:
            return self.get_actions(
                self.last_workflow_id.next_step_id, token, bot, update)
        if not action:
            return False
        data = {
            'message': action.message,
            'delay': action.delay,
            'img': action.image,
            'text_in_chat': action.text_in_chat,
            'attachment': action.attachment,
            'file_name': action.file_name,
            'update': update,
            'bot': bot,
            'element_keyboard': action.element_keyboard,
            'chat_id': data_bot['chat_id'],
            'handler': handler,
            'send_location': action.send_location,
            'send_contact': action.send_contact,
        }
        if action.action == 'code':
            data['items'] = action.method_direct_trigger(data)

        if hasattr(self, HANDLERS[action.telegram_action]):
            getattr(self, HANDLERS[action.telegram_action])(data_bot, data)
            self.last_workflow_id = action.id
            if action.next_step_id and not action.wait_user_response:
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
        method = 'send_image_%s' % self.provider
        if hasattr(self, method):
            getattr(self, method)(data)
        self.create_text(data_bot, data)

    def send_document(self, data_bot, data):
        self.create_text(data_bot, data)
        method = 'send_document_%s' % self.provider
        if hasattr(self, method):
            getattr(self, method)(data)

    def send_video(self, data_bot, data):
        self.create_text(data_bot, data)
        method = 'send_video_%s' % self.provider
        if hasattr(self, method):
            getattr(self, method)(data)

    def send_audio(self, data_bot, data):
        self.create_text(data_bot, data)
        method = 'send_audio_%s' % self.provider
        if hasattr(self, method):
            getattr(self, method)(data)

    def create_selection(self, data_bot, data):
        for key in data_bot.keys():
            if key in data['message']:
                data['message'] = data['message'].replace(key, data_bot[key])
        if 'items' in data.keys():
            custom_keyboard = self.build_keyboard(data['items'], data)
            data['custom_keyboard'] = custom_keyboard
        sleep(data['delay'])
        method = 'create_selection_%s' % self.provider
        if hasattr(self, method):
            getattr(self, method)(data)

    def build_keyboard(self, items, data):
        method = 'build_keyboard_%s' % self.provider
        if hasattr(self, method):
            custom_keyboard = getattr(self, method)(
                data['element_keyboard'], items)
        return custom_keyboard

    def environment_variables(self, update):
        method = 'environment_variables_%s' % self.provider
        if hasattr(self, method):
            env_variables = getattr(self, method)(update)
        return env_variables

    @api.multi
    def get_coordinates(self, name, state, country):
        address = (name + "," + state + "," +
                   country)
        google_url = (
            'http://maps.googleapis.com/maps/api/geocode/json?' +
            'address=' + address + '&sensor=false')
        try:
            result = json.load(urllib.request.urlopen(
                google_url.replace(' ', '%20')))
            if result['status'] == 'OK':
                location = result['results'][0]['geometry']['location']
            return {
                'latitude': location['lat'],
                'longitude': location['lng'],
            }
        except:
            raise UserError(_("Google Maps is not available."))
