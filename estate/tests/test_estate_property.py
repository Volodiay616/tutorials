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
        
        self.assertRecordValues(self.properties, [{
            'name': 'House',
            'state': 'offer accepted',
            'selling_price': self.properties.offer_ids.price
            }])
        self.assertRecordValues(self.properties.partner_id, [{
            'name': self.buyer_2['name']
            }])
       
        with self.assertRaises(UserError):
            self.properties.offer_ids['partner_id' == self.buyer_1.id].action_accept_status() #попробовать для покупателя 1
        
        self.properties.action_set_sold_state()
        self.assertRecordValues(self.properties, [
            {'name': 'House', 'state': 'sold'}
            ])

        with self.assertRaises(UserError):
            self.properties.action_set_canceled_state() 
            
         
    # def test_offer_sold_property(self):
        # """Test that nobody cannot create offer to 'sold' property"""
        
        # Test that offer price at least 90'%' of the expected price
        # with self.assertRaises(ValidationError):
        #     self.properties.offer_ids = self.env['estate.property.offer'].create({
        #         'price': self.properties.expected_price * 0.89,
        #         'partner_id': self.buyer_1.id,
        #         'property_id': self.properties.id
        #     })
        
        