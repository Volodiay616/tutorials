from odoo import api, fields, models


class EstatePropertyType(models.Model):
    """Types of estate propyrtyes"""

    _name = "estate.property.type"
    _description = "Types of property"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer(string="Sequence", default=10)
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_get_offer")

    @api.depends("offer_ids")
    def _compute_get_offer(self):
        """Counts the number of offers for a given property type"""
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    _sql_constraints = [
        ("estate_property_type_unique", 'unique("name")', "The name must be unique")
    ]
