from odoo import fields, models

class EstateProperty(models.Model):
    """Automatically generates invoices for sold properties"""
    _inherit = "estate.property"
    
    journal_id = fields.Many2one('account.move')
    move_type = fields.Selection(selection=[
            ('entry', 'Journal Entry'),
            ('out_invoice', 'Customer Invoice'),
            ('out_refund', 'Customer Credit Note'),
            ('in_invoice', 'Vendor Bill'),
            ('in_refund', 'Vendor Credit Note'),
            ('out_receipt', 'Sales Receipt'),
            ('in_receipt', 'Purchase Receipt'),
        ], string='Type', required=True, store=True, index=True, readonly=True, tracking=True,
        default="entry", change_default=True)

    def action_set_sold_state(self):
        """Marks the property as sold and created the invoice"""
        invoice_vals_list = []
        journal = self.env['account.move'].with_context(default_move_type='out_invoice')._get_default_journal()
        invoice_vals = {
            'move_type': 'out_invoice',
            'journal_id': journal.id,
            'partner_id': self.partner_id.id,
            'invoice_line_ids': []
        }
        price_unit = self.selling_price * 0.06
        line_values= [
                (
                    0,
                    0,
                    {
                        "name": self.offer_ids.property_id.display_name,
                        "quantity": "1",
                        "price_unit": price_unit
                    },
                ),
                (
                    0,
                    0,
                    {
                        "name": "Administrative fees",
                        "quantity": "1",
                        "price_unit": 100
                    },
                )
            ]
        invoice_vals['invoice_line_ids'] = line_values
        invoice_vals_list.append(invoice_vals)
        moves = self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(invoice_vals_list)
        return super().action_set_sold_state()