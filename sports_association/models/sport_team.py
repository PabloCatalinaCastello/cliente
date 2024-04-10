from odoo import fields, models, Command


class SportTeam(models.Model):
    _name = "sport.team"
    _description = "Sport Team"


    name = fields.Char(string="Name", required=True)
    sport_id = fields.Many2one("sport.sport", string="Sport")
    player_ids = fields.One2many("sport.player", "team_id", string="Players")
    logo = fields.Image("Logo")
    position = fields.Char(string='Position')
    player_count = fields.Integer(string='Player Count', compute="_compute_player_count", readonly=True)
    

    def _compute_player_count(self):
        for record in self:
            record.player_count = len(record.player_ids)


    def action_make_all_starter(self):
        for record in self.player_ids:
            record.action_make_starter()


    def action_make_all_subtitutes(self):
        for record in self.player_ids:
            record.action_make_substitute()
    

    def action_add_players(self):
        for record in self:
            players = self.env['sport.player'].search([('team_id', '=', False), ('age', '<', 30)])
            players |= record.player_ids
            record.player_ids = [Command.set(players.ids)]


    #def action_add_players(self):
        #players = self.env['sport.player'].search([('team_id', '=', False), ('age', '<', 30)])
            #for player in players:
                #player.team_id = self.id
            #return True

    def action_view_players(self):
        return {
            'name': 'Players',
            'type': 'ir.actions.act_window',
            'res_model': 'sport.player',
            'view_mode': 'tree,form',
            'domain': [('team_id', '=', self.id)],
        }
