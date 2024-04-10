from odoo import fields, models

class SportClinic(models.Model):
    _name = 'sport.clinic'
    _description = 'Sport Clinic'
    
    name = fields.Char(string='Name', required=True)
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')

    issue_ids = fields.One2many('sport.issue', 'clinic_id', string='issue')
    available = fields.Boolean(string='Available')
    issue_cont = fields.Integer(string='Issue Count', compute="_compute_issue_count")


    def _compute_issue_count(self):
        for record in self:
            record.issue_cont = len(record.issue_ids)
    

    def action_check_assistance(self):
        self.issue_ids.write({'assistance': True})


    def action_view_issues(self):
        return{
            'name': 'Issues',
            'type': 'ir.actions.act_window',
            'res_model': 'sport.issue',
            'view_mode': 'tree,form',
            'domain': [('clinic_id', '=', self.id)],
        }
    
