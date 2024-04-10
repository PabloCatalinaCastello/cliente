from odoo import fields, models, api

class SportMatch(models.Model):
    _name = 'sport.match'
    _description = 'Sport Match'

    sport_id = fields.Many2one('sport.sport', string='Sport')
    date = fields.Date(string='Date')
    winner_team_id = fields.Many2one('sport.team', string='Winner Team', compute="_compute_winner_team_id", store=True)
    score_winning = fields.Integer(string='Score Winning', default=3)
    match_line_ids = fields.One2many('sport.match.line', 'match_id', string='Match Lines')
    league_id = fields.Many2one('sport.league', string='League')
    

    @api.depends('match_line_ids.score')
    def _compute_winner_team_id(self):
        for record in self:
            winner = record.match_line_ids.sorted(key=lambda r: r.score, reverse=True)
            record.winner_team_id = winner[0].team_id.id if winner else False

class SportMatchLine(models.Model):
    _name = 'sport.match.line'
    _description = 'Sport Match Line'
    _order = 'score desc'
    _sql_constraints = [
    ('team_unique_in_match', 'UNIQUE(match_id, team_id)', 'Team must be unique in match')]

    match_id = fields.Many2one('sport.match', string='Match')
    team_id = fields.Many2one('sport.team', string='Team')
    score = fields.Integer(string='Score')
    
    
    



    
    
    
    
        
    
