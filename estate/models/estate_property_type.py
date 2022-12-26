from odoo import fields, models, api

class EstatePropertyType (models.Model):
    """Types of estate propyrtyes"""
    _name = "estate.property.type"
    _description = "Types of property"
    _order = "name"
    
    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer(string='Sequence', default=10)
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_get_offer")
    
    @api.depends('offer_ids')
    def _get_offer(self):
        """Counts the number of offers for a given property type"""
        for rec in self:
            x = self.offer_ids
            rec.offer_count = len(x)
    
    _sql_constraints = [
        ('estate_property_type_unique', 'unique("name")',
         "The name must be unique")
    ]
    