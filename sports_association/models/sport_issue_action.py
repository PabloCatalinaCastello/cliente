from odoo import fields, models, api, Command


class SportIssueAction(models.Model):
    _name = 'sport.issue.action'
    _description = 'Sport Issue Action'

    name = fields.Char(string='Name', required = True)
    issue_id = fields.Many2one('sport.issue', string='Issue')
    state = fields.Selection(
        [('draft', 'Draft'),
        ('open', 'Open'),
        ('done', 'Done')],
        string='State',
        default='draft',
    )
    
    
