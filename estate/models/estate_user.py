from odoo import fields, models

class EstateUser(models.Model):
    """Adds a list of available properties linked to a salesperson. Displayed it in their user form view"""
    _inherit = "res.users"
    
    property_ids = fields.One2many("estate.property", "salesperson_id", domain="['|', ('state', '=', 'new'), ('state', '=', 'offer recieved')]")
    
    