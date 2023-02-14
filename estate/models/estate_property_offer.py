from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offers"
    _order = "price desc"

    price = fields.Float(required=True)
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property")
    validity = fields.Integer(default="7")
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )

    _sql_constraints = [
        (
            "check_offered_price",
            'CHECK("price" > 0)',
            "The offered price must be strictly positive",
        ),
    ]

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        """Sets the DeadLine date of the offer depending on the 'validity'"""
        for record in self:
            try:
                record.date_deadline = record.create_date.date() + relativedelta(
                    days=record.validity
                )
            except Exception:
                record.date_deadline = fields.Date.today() + relativedelta(
                    days=record.validity
                )

    def _inverse_date_deadline(self):
        """Determines the number of days of availability"""
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept_status(self):
        """Accepts the offer, sets selling price and buyer (partner_id in estate.property)"""
        for record in self:
            if "accepted" not in self.property_id.offer_ids.mapped("status"):
                record.status = "accepted"
                self.property_id.selling_price = record.price
                self.property_id.partner_id = record.partner_id
                self.property_id.state = "offer accepted"
            else:
                raise ValidationError(_("You cannot accept multiple offers"))
        return True

    def action_refuse_status(self):
        """Refuses the offer"""
        for record in self:
            if "sold" not in self.property_id.mapped("state"):
                record.status = "refused"
                self.property_id.selling_price = ""
                self.property_id.partner_id = []
                self.property_id.state = "offer received"
            else:
                raise ValidationError(
                    _("You cannot refuse an offer from a sold property")
                )
        return True

    @api.model
    def create(self, vals):
        """Add new offer only if price not lower than the best_price"""
        estate = self.env["estate.property"].browse(vals["property_id"])
        best_offer = estate.best_price
        if vals["price"] >= best_offer:
            estate.state = "offer received"
            return super().create(vals)
        else:
            raise ValidationError(_("The offer must be higer than '%(best_offer)s'."))
