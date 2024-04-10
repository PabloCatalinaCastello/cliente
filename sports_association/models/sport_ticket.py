from odoo import fields, models, api



class SportTicket(models.Model):
    _name = 'sport.ticket'
    _description = 'Sport Ticket'

    name = fields.Char('Name', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    match_id = fields.Many2one('sport.match', string='Match')
    
    
    