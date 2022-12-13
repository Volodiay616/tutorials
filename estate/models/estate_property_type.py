from odoo import fields, models

class EstatePropertyType (models.Model):
    _name = "estate.property.type"
    _description = "Types of property"
    
    name = fields.Char(required=True)
    