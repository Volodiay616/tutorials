from odoo.tests.common import Form, TransactionCase, SavepointCase
from odoo.exceptions import UserError, ValidationError
from odoo.tests import tagged

@tagged('post_install')
class TestEstateProperty(SavepointCase):
    """Estate Property model testing"""
    @classmethod
    def setUpClass(cls):
        super(TestEstateProperty, cls).setUpClass()
        
        #create property
        cls.properties = cls.env['estate.property'].create({
            'name': 'House',
            'expected_price': 1000
        }
        )
        #Create buyer_1
        cls.partners = cls.env["res.partner"].with_context(no_reset_password=True)
        cls.buyer_1 = cls.partners.create(
            {
                "name": "Buyer_1"
            }
        )
        # Create buyer_2
        cls.buyer_2 = cls.partners.create(
            {
                "name": "Buyer_2"
            }
        )
        
    def test_action_sell(self):
        """Test that everything behaves like it should when selling a property."""
        self.assertRecordValues(self.properties, [
            {'name': 'House', 'state': 'new'}
            ])
        self.properties.offer_ids = self.env['estate.property.offer'].create({
                'price': self.properties.expected_price,
                'partner_id': self.buyer_1.id,
                'property_id': self.properties.id
            })
        self.assertRecordValues(self.properties, [
            {'name': 'House', 'state': 'offer received', 'best_price': self.properties.expected_price},
            ])
        self.properties.offer_ids = self.env['estate.property.offer'].create({
                'price': self.properties.expected_price * 1.1,
                'partner_id': self.buyer_2.id,
                'property_id': self.properties.id
            })
        self.assertRecordValues(self.properties, [
            {'name': 'House', 'state': 'offer received', 'best_price': self.properties.expected_price * 1.1 },
            ])
        self.properties.offer_ids['partner_id' == self.buyer_2.id].action_accept_status() #попробовать для покупателя 1
        self.assertRecordValues(self.properties, [
            {'name': 'House', 'state': 'offer accepted'}
            ])
        self.properties.action_set_sold_state() #почему то выполняется 2 раза, первый раз проходит второй нет
        self.assertRecordValues(self.properties, [
            {'name': 'House', 'state': 'sold'}
            ])

        with self.assertRaises(ValidationError):
            self.properties.action_set_canceled_state()  
    # def test_offer_sold_property(self):
        """Test that nobody cannot create offer to 'sold' property"""
        
        # Test that offer price at least 90'%' of the expected price
        # with self.assertRaises(ValidationError):
        #     self.properties.offer_ids = self.env['estate.property.offer'].create({
        #         'price': self.properties.expected_price * 0.89,
        #         'partner_id': self.buyer_1.id,
        #         'property_id': self.properties.id
        #     })
        
        # Test
        with self.assertRaises(UserError):
            price_2 = self.properties.expected_price * 1.1
            self.properties.offer_ids = self.env['estate.property.offer'].create({
                'price': price_2,
                'partner_id': self.buyer_2.id
            })
        
        # self.assertEqual(self.properties.best_price, price_2, "Must be 10% more than Expected Price")
        
        # self.properties['state'] = 'sold'
        # self.properties['state'] = 'new'
        # with self.assertRaises(UserError):
            
            
        # with self.assertRaises(ValidationError):
        #     self.properties.action_set_canceled_state()
        
        # self.properties.offer_ids.create()
                
        # so_line_1 = self.sale_order_1.order_line[0]
        
        # self.assertEqual(so_line_1.line_number, 1, "line number must be equal to 1")
        # self.assertEqual(so_line_1.product_id, self.product_cat, "must be product cat")
        