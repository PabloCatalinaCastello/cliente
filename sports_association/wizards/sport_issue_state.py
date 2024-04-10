from odoo import fields, models, api



class SportIssueState(models.TransientModel):
    _name = 'sport.issue.state'
    _description = 'Issue State'

    def set_done(self):
        active_ids = self.env.context.get('active_ids')
        issues = self.env['sport.issue'].browse(active_ids)
        issues.write({'date': self.date})
        issues.action_done()