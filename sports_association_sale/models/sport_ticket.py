from odoo import fields, models, api

class SportTicket(models.Model):
    _inherit="sport.ticket"

    sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    