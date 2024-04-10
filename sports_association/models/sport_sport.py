from odoo import fields, models


class SportSport(models.Model):
    _name = 'sport.sport'
    _description = 'Sport'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')


