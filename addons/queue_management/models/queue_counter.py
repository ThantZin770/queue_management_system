from odoo import api, fields, models

class QueueCounter(models.Model):
    _name = 'queue.counter'
    _description = 'QueueCounter'

    name = fields.Char()
    type = fields.Selection([('reception', 'Reception'),('cashier','Cashier'),('pharmacy','Pharmacy')],default='reception')

