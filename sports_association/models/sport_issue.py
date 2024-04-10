from odoo import models, fields, Command, api, _
from odoo.exceptions import ValidationError, UserError

class SportIssue(models.Model):
    _name = 'sport.issue'
    _description = 'Sport Issue'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    

    name = fields.Char(string='Name')
    description = fields.Text(string='Description')
    date = fields.Date(string='Date', default=fields.Date.today)
    assistance = fields.Boolean(string='Assistance')
    state = fields.Selection(
        [('draft', 'Draft'),
        ('open', 'Open'),
        ('done', 'Done')],
        string='State',
        default='draft',
        tracking=True,
    )

    color = fields.Integer(string='Color', default=0)
    user_id = fields.Many2one('res.users', string='user', default= lambda self: self.env.user, context={'search_default_filter_no_share': 1})
    sequence = fields.Integer(string='Squence', default=10)
    solution = fields.Html('Solutions')
    assigned = fields.Boolean(string='Assigned', compute="_compute_assigned", inverse="_inverse_assigned", search="_search_assigned", tracking=True)
    clinic_id = fields.Many2one('sport.clinic', string='clinic', tracking=True)
    player_id = fields.Many2one('sport.player', string='Player', tracking=True)
    
    tag_ids = fields.Many2many('sport.issue.tag', string='Tags')
    cost = fields.Float(string='Coste')
    user_phone = fields.Char(string='user_phone', store=True, readonly=False) #related='user_id.phone',
    action_ids = fields.One2many('sport.issue.action', 'issue_id', string='Actions to do')

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The name must be unique!')
    ]

    
    @api.constrains('cost')
    def _check_cost(self):
        for record in self:
            if record.cost<0:
                raise ValidationError(_('The cost must be positive'))

    @api.onchange('clinic_id')
    def _onchange_clinic(self):
        for record in self:
            if record.clinic_id:
                record.assistance = True
            else:
                record.assistance = False

    @api.onchange('user_id')
    def _onchange_user_id(self):
        if self.user_id:
            self.user_phone = self.user_id.phone
        else:
            self.user_phone = False

    
    @api.depends('user_id')
    def _compute_assigned(self):
        for record in self:
            record.assigned = bool(record.user_id)

    def _inverse_assigned(self):
        for record in self:
            if not record.assigned:
                record.user_id = False
            else:
                record.user_id = self.env.user

    def _search_assigned(self, operator, value):
        if operator == '=':
            return [('user_id', operator, value)]
        else:
            return []


    def action_open(self):
        for record in self:
            record.state = 'open'

    def action_draft(self):
        for record in self:
            record.state = 'draft'

    def action_done(self):
        for record in self:
            if not record.date:
                raise UserError(_('The date is required'))
            #tag =self.env['sport.issue.tag'].create({'name':'PRUEBA1'})
            record.state = 'done'
            msg_body = f'La incidencia ha pasado al estado {record.state} con fecha {record.date}'
            record.message_post(body=msg_body)

    def action_add_tag(self):
        for record in self:
            #import wdb; wdb.set_trace()
            tag_ids = self.env['sport.issue.tag'].search([('name', 'ilike', record.name)])
            if tag_ids:
                #record.tag_ids = [Command.set(tag_ids.ids)]
                record.tag_ids = [(6, 0, tag_ids.ids)]
            else:
                record.tag_ids = [Command.create({'name': record.name})]


    def cron_unlink_unused_tags(self):
        tag_ides = self.env['sport.issue.tag'].search([])

        for tag in tag_ides:
            issue = self.env['sport.issue'].search([('tag_ids', 'in', tag.id)])
            if not issue:
                tag.unlink()

    
    