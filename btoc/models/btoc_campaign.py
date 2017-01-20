# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
from openerp.service.telegram import BOT

class BtocCampaign(models.Model):
    _name = 'btoc.campaign'

    name = fields.Char(required=True)
    message = fields.Text()
    color = fields.Integer()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('stand-by', 'Stand by'),
        ('sending', 'Sending'),
        ('sent', 'Sent')],
        default='draft')
    schedule = fields.Datetime()
    creation_date = fields.Datetime()
    sent_date = fields.Datetime()
    next_departure = fields.Datetime(
        compute='_compute_schedule')
    group_ids = fields.Many2many(
        'btoc.group',
        string='Target group')
    attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Attachments')
    color = fields.Integer()
    attachment_count = fields.Integer(
        compute='_compute_count_attachment')
    message_sent = fields.Integer()
    success_message = fields.Integer()
    failed_message = fields.Integer()
    users_reached = fields.Integer()

    @api.model
    def create(self, values):
        res = super(BtocCampaign, self).create(values)
        res.creation_date = fields.datetime.now()
        return res

    @api.multi
    def action_send_all(self):
        for rec in self:
            rec.state = 'stand-by'

    @api.multi
    def action_cancel(self):
        for rec in self:
            rec.state = 'draft'

    @api.depends('schedule')
    def _compute_schedule(self):
        for rec in self:
            rec.next_departure = rec.schedule

    @api.depends('attachment_ids')
    def _compute_count_attachment(self):
        for rec in self:
            rec.attachment_count = len(rec.attachment_ids)

    @api.model
    def process_start_campaign(self):
        campaigns = self.search([
            ('schedule', '<=', fields.Datetime.now()),
            ('state', '=', 'stand-by')])
        for campaign in campaigns:
            for group in campaigns.group_ids:
                for user in group.user_ids:
                    try:
                        BOT.send_message(user.telegram_id, campaign.message)
                        campaign.success_message += 1
                        campaign.users_reached += 1
                    except:
                        campaign.failed_message += 1
                    campaign.message_sent += 1
            campaign.write({'state': 'sent'})
