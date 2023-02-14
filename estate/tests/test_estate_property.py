from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tests.common import Form, SavepointCase


@tagged("post_install")
class TestEstateProperty(SavepointCase):
    """Estate Property model testing"""

    @classmethod
    def setUpClass(cls):
        super(TestEstateProperty, cls).setUpClass()

        # create property
        cls.properties = cls.env["estate.property"].create(
            {"name": "House", "expected_price": 1000}
        )
        # Create buyer_1
        cls.partners = cls.env["res.partner"].with_context(no_reset_password=True)
        cls.buyer_1 = cls.partners.create({"name": "Buyer_1"})
        # Create buyer_2
        cls.buyer_2 = cls.partners.create({"name": "Buyer_2"})

    def test_action_sell(self):
        """Test that everything behaves like it should when selling a property."""
        # Add garden to property
        with Form(self.properties) as f:
            f.garden = True
        f.save()
        # Chek standarts garden options
        self.assertRecordValues(
            self.properties,
            [
                {
                    "name": "House",
                    "state": "new",
                    "garden_area": 10,
                    "garden_orientation": "north",
                }
            ],
        )
        # Test that accepted offer price at least 90'%' of the expected price
        with self.assertRaises(ValidationError):
            self.properties.offer_ids = self.env["estate.property.offer"].create(
                {
                    "price": self.properties.expected_price * 0.89,
                    "partner_id": self.buyer_1.id,
                    "property_id": self.properties.id,
                }
            )
            self.properties.offer_ids[
                "price" == self.properties.expected_price * 0.89
            ].action_accept_status()
        # Create new offer
        self.env["estate.property.offer"].create(
            {
                "price": self.properties.expected_price,
                "partner_id": self.buyer_1.id,
                "property_id": self.properties.id,
            }
        )
        # Check state and best_price fields after recived offer
        self.assertRecordValues(
            self.properties,
            [
                {
                    "name": "House",
                    "state": "offer received",
                    "best_price": self.properties.expected_price,
                },
            ],
        )
        # Create new offer with higher price
        self.env["estate.property.offer"].create(
            {
                "price": self.properties.expected_price * 1.1,
                "partner_id": self.buyer_2.id,
                "property_id": self.properties.id,
            }
        )
        # Chek that best_price changed
        self.assertRecordValues(
            self.properties,
            [
                {
                    "name": "House",
                    "state": "offer received",
                    "best_price": self.properties.expected_price * 1.1,
                },
            ],
        )
        # Create new offer with lower price than recived offer price
        with self.assertRaises(ValidationError):
            self.properties.offer_ids = self.env["estate.property.offer"].create(
                {
                    "price": self.properties.expected_price,
                    "partner_id": self.buyer_1.id,
                    "property_id": self.properties.id,
                }
            )
        # Accept the offer
        self.properties.offer_ids[
            "partner_id" == self.buyer_2.id
        ].action_accept_status()
        # Check property state and selleng_price fields
        self.assertRecordValues(
            self.properties,
            [
                {
                    "name": "House",
                    "state": "offer accepted",
                    "selling_price": self.properties.offer_ids[
                        "partner_id" == self.buyer_2.id
                    ].price,
                }
            ],
        )
        # Check parner_id (byer) field
        self.assertRecordValues(
            self.properties.partner_id, [{"name": self.buyer_2["name"]}]
        )
        # Try accept offer for "offer accepted" properties
        with self.assertRaises(ValidationError):
            self.properties.offer_ids[
                "partner_id" == self.buyer_1.id
            ].action_accept_status()
        # Setup a sold state
        self.properties.action_set_sold_state()
        self.assertRecordValues(self.properties, [{"name": "House", "state": "sold"}])
        # Try cancel sold property
        with self.assertRaises(ValidationError):
            self.properties.action_set_canceled_state()
        # Try delete sold property
        with self.assertRaises(ValidationError):
            self.properties.unlink()
