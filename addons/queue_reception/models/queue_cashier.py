from odoo import fields, models

class QueueCashier(models.Model):
    _inherit = 'queue.cashier'

    reception_id = fields.Many2one("queue.reception", readonly=1)
