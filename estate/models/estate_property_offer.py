from odoo import fields, models, api
from datetime import date, time, datetime, timedelta
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer (models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offers"
        
    price = fields.Float(required=True)
    status = fields.Selection(selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one ("estate.property", required=True)
    validity = fields.Integer(default="7")
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            try:
                record.date_deadline = record.create_date.date() + relativedelta(days=record.validity)
            except Exception:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)             
            # if self.create_date == False:
            #     record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)
            # else:
            #     record.date_deadline = record.create_date.date() + relativedelta(days=record.validity)
        
    def _inverse_date_deadline(self):
        for record in self:            
            record.validity = (record.date_deadline - record.create_date.date()).days
    