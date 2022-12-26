from odoo import fields, models

class EstatePropertyTag (models.Model):
    """Tags for real estate objects"""
    _name = "estate.property.tag"
    _description = "Estate Property Tags"
    _order = "name"
    
    name = fields.Char(required=True)
    color = fields.Integer()
    
    _sql_constraints = [
        ('estate_property_tag_unique', 'unique("name")',
         "The tag must be unique")
    ]