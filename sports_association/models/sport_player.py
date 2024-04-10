from odoo import fields, models, api
from datetime import datetime


class SportPlayer(models.Model):
    _name = "sport.player"
    _description = "Sport Player"
    _inherits = {'res.partner': 'partner_id'}

    name = fields.Char(related='partner_id.name', inherited=True, readonly=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True, ondelete="cascade")
    
    team_id = fields.Many2one("sport.team", string="Team")
    birth_date = fields.Date(string="Birth Date", copy=False)
    age = fields.Integer(string="Age", compute="_compute_age", store=True, readonly=True)
    starter = fields.Boolean(string="Starter", default=True, copy=False)
    position = fields.Char(string="Position", copy=False)
    sport_team = fields.Char(string="Sport", related="team_id.sport_id.name", store=True ,readonly=True)
    active = fields.Boolean(string='Active', default=True)
    

    def action_make_starter(self):
        self.starter = True

    def action_make_substitute(self):
        self.starter = False

    # def copy(self, default=None):
    #     self.ensure_one()
    #     default = dict(default or {})
    #     if ('name' not in default) and ('partner_id' not in default):
    #         default['name'] = _("%s (copy)", self.name)
    #     return super().copy(default)

    @api.depends("birth_date")
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                record.age = (fields.Date.today() - record.birth_date).days / 365
            else:
                record.age = 0
