from odoo import fields, models, api
from datetime import date, time, datetime
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
        
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        string='State',
        selection=[("new", "New"), ("offer received", "Offer Received"), ("offer accepted", "Offer Accepted"), ("sold", "Sold"), ("canceled", "Canceled")],
        default="new"
        )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    partner_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")
    
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for line in self:
            line.total_area = line.living_area + line.garden_area
            
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            try:
                record.best_price = max(record.offer_ids.mapped('price'))
            except Exception:
                record.best_price == 0
                
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""
               