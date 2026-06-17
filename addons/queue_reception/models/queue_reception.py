from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class QueueReception(models.Model):
    _name = "queue.reception"
    _description = "Reception"


    name = fields.Char(string="Reference", readonly=True, default=lambda x: _("New"))
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    counter_id = fields.Many2one("queue.counter", string="Counter", required=True, domain=[('type','=','reception')])
    state = fields.Selection([('draft','Draft'),('confirm','Confirm')],default='draft')
    date = fields.Datetime(string="Date", default=fields.Date.today())
        


    def action_confirm(self):
        if self.name== _("New"):
            self.name = self.env['ir.sequence'].next_by_code('account.queue') or _("New")
        self.change_state('confirm')
        self.date = fields.Datetime.now()

        cashier_data ={
            "name": self.name,
            "reception_id" : self.id,
        }
        cashier_id = self.env["queue.cashier"].create(cashier_data)
        cashier_id.action_waiting()

    def action_draft(self):
        self.change_state('draft')
        #self.state = 'draft'

    def change_state(self,new_state):
        if self.is_allowed(new_state,self.state):
            self.state = new_state

        else:
            raise ValidationError(_("Moving from %s to %s is not allowed") % (self.state,new_state))


    def is_allowed(self,new_state,old_state):
        allowed = [
            ('draft', 'confirm'),
            ('confirm', 'draft'),
        ]
        return (new_state,old_state) in allowed
