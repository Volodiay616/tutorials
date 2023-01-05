from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"
        
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
    partner_id = fields.Many2one("res.partner", string="Buyer", readonly=True, copy=False)
    salesperson_id = fields.Many2one("res.user", string="Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")
         
    _sql_constraints = [
        ('check_expected_price', 'CHECK("expected_price" > 0)',
         'The expected price must be strictly positive'),
        ('check_selling_price', 'CHECK("selling_price" >= 0)',
         'The selling price must be strictly positive')
    ]
        
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        """Calculates the total area of the property"""
        for line in self:
            line.total_area = line.living_area + line.garden_area
            
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        """Determines the offer with a higher price"""
        for record in self:
            try:
                record.best_price = max(record.offer_ids.mapped('price'))
            except Exception:
                record.best_price == 0
                
    @api.onchange('garden')
    def _onchange_garden(self):
        """Sets default values depending on the state of the 'garden'"""
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""            
  
    def action_set_sold_state(self):
        """Marks the property as sold"""
        for record in self:
            if record.state != "canceled":
                record.state = "sold"
            else:
                raise UserError('Canceled properties cannot be sold.')
        return True
    
    def action_set_canceled_state(self):
        """Marks the property as canceled"""
        for record in self:
            if record.state != "sold":
                record.state = "canceled"
            else:
                raise UserError('Sold properties cannot be canceled.')
        return True
    
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        """:selling price must be at least 90% of the expected price"""
        for rec in self:
           if rec.selling_price != 0 and (rec.selling_price / rec.expected_price * 100) < 90:
                raise ValidationError("The selling price must be at least 90'%' of the expected price! You must reduce the expected price if you want to accept this offer.")
    
    def unlink(self):
        """allows to delete only New or Canceled propertyes"""
        for rec in self:
            if rec.state not in ('new', 'canceled'):
                raise UserError('Only New or Canceled Propertyes can be deleted')
            else:
                return super(EstateProperty, self).unlink()   