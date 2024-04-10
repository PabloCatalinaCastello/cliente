from odoo import fields, models, api


class SportCreateIssue(models.TransientModel):
    _name = "sport.create.issue"
    _description = "Create Issue"

    name = fields.Char(string="Issue name")
    clinic_id = fields.Many2one("sport.clinic", string="Clinic") #default=lambda self: self.env.context.get("active_id")
    player_id = fields.Many2one('sport.player', string='Player')
    

    def create_issue(self):
        # active_id = self.env.context('active_id')
        # if self.env.context('active_model') == 'sport.clinic':
        #     clinic = self.env['sport.clinic'].browse(active_id)
        #     self.clinic_id = clinic.id
        # elif self.env.context('avtive_model') == 'sport_player':
        #     player = self.env['sport.player'].browse(active_id)
        #     self.player_id = player.id
        vals = {
            "name": self.name, 
            "clinic_id": self.clinic_id.id,
            "player_id" : self.player_id.id
            }
        issue = self.env["sport.issue"].create(vals)
        return{
            'name': 'Issue',
            'view_mode' : 'form',
            'res_model' : 'sport.issue',
            'res_id' : issue.id,
            'type' : 'ir.actions.act_window',
            'target' : 'current',
        }
