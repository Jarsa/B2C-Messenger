# Copyright 2018, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import Warning
from odoo.tools.safe_eval import safe_eval

DEFAULT_PYTHON_CODE = _("""# Available variables:
#  - env: Odoo Environment on which the action is triggered
#  - model: Odoo Model of the record on which the action is triggered;
#    is a void recordset
#  - record: record on which the action is triggered; may be be void
#  - records: recordset of all records on which the action is triggered in
#    multi-mode; may be void
#  - time, datetime, dateutil, timezone: useful Python libraries
#  - log: log(message, level='info'): logging function to record debug
#    information in ir.logging table
#  - Warning: Warning Exception to use with raise
#  - res: Variable destinated to store the reuslt of this function
#  * If selection send_location, you can send:
#      res = {'name': 'Torreón',
#             'state': 'Coahuila',
#             'country': 'México'},
# To return an action, assign: action = {...}\n\n\n\n""")


class B2CWorkflow(models.Model):
    _name = 'b2c.workflow'

    name = fields.Char()
    provider = fields.Selection([])
    step_line_ids = fields.One2many(
        'b2c.workflow.line',
        'workflow_id',
        string='Step Lines',
    )


class B2CWorkflowLine(models.Model):
    _name = 'b2c.workflow.line'
    _order = 'sequence, id'

    workflow_id = fields.Many2one(
        'b2c.workflow',
        string='Workflow',
    )
    name = fields.Char(string='Name of Action',)
    code = fields.Text(
        string='Python Code', groups='base.group_system',
        default=DEFAULT_PYTHON_CODE,
        help="Write Python code that the action will execute."
             "Some variables are available for use; help about "
             "pyhon expression is given in the help tab.")
    message = fields.Char(string='Message',)
    action = fields.Selection([
        ('text', 'Text'),
        ('code', 'Python Code')],
        default='text',
        required=True,
    )
    handler = fields.Char(
        required=True,
        help='Field to express the user input',)
    model_id = fields.Many2one(
        'ir.model', string='Model',
        default=lambda self: self.env.ref('b2c_telegram.model_b2c_base').id)
    delay = fields.Integer(string='Delay',)
    next_step_id = fields.Many2one(
        'b2c.workflow.line', string='Next Step',)
    previus_step_id = fields.Many2one(
        'b2c.workflow.line', string='Previus Step',)
    attachment = fields.Binary(attachment=True,)
    file_name = fields.Char('File Name')
    provider = fields.Selection([])
    sequence = fields.Integer()
    wait_user_response = fields.Boolean()

    @api.multi
    def method_direct_trigger(self, data):
        self.check_access_rights('write')
        for b2c in self:
            res = self.sudo(user=self.env.user.id).run(data)
        return res

    @api.multi
    def run(self, data):
        res = False
        for action in self:
            eval_context = self._get_eval_context(action, data)
            if hasattr(self, 'run_action_%s_multi' % action.action):
                # call the multi method
                run_self = self.with_context(eval_context['env'].context)
                func = getattr(run_self, 'run_action_%s_multi' % action.action)
                res = func(action, eval_context=eval_context)
        return eval_context['res']

    @api.model
    def _get_eval_context(self, action=None, data=None):
        def log(message, level="info"):
            with self.pool.cursor() as cr:
                cr.execute("""
                    INSERT INTO ir_logging(create_date, create_uid,
                    type, dbname, name, level, message, path, line, func)
                    VALUES (NOW() at time zone
                    'UTC', %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (self.env.uid, 'server', self._cr.dbname,
                      __name__, level, message, "action",
                      action.id, action.name))

        eval_context = {}
        model_name = action.model_id.sudo().model
        model = self.env[model_name]
        record = None
        records = None
        if (self._context.get('active_model') ==
                model_name and self._context.get('active_id')):
            record = model.browse(self._context['active_id'])
        if (self._context.get('active_model') ==
                model_name and self._context.get('active_ids')):
            records = model.browse(self._context['active_ids'])
        if self._context.get('onchange_self'):
            record = self._context['onchange_self']
        eval_context.update({
            'env': self.env,
            'model': model,
            'Warning': Warning,
            'record': record,
            'records': records,
            'log': log,
            'res': None,
            'partner': self.env['res.partner'].search([
                ('bot_id', '=', data['chat_id'])]),
            'handler': data['handler'],
            'b2c_model': self.env['b2c.base'],
        })
        return eval_context

    @api.model
    def run_action_code_multi(self, action, eval_context=None):
        return safe_eval(
            action.sudo().code.strip(), eval_context, mode="exec", nocopy=True)
