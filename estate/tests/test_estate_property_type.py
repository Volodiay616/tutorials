from odoo.tests import tagged
from odoo.tests.common import SavepointCase


@tagged("post_install")
class TestEstatePropertyType(SavepointCase):
    """Estate Property model testing"""

    @classmethod
    def setUpClass(cls):
        super(TestEstatePropertyType, cls).setUpClass()

        # create types of property
        cls.types = cls.env["estate.property.type"]
        cls.house_type = cls.types.create({"name": "House"})
        cls.appartment_type = cls.types.create({"name": "Appartment"})
        # create properties
        cls.house = cls.env["estate.property"].create(
            {
                "name": "House",
                "expected_price": 1000,
                "property_type_id": cls.house_type.id,
            }
        )
        cls.appartment = cls.env["estate.property"].create(
            {
                "name": "Appartment",
                "expected_price": 100,
                "property_type_id": cls.appartment_type.id,
            }
        )
        # Create buyer_1
        cls.partners = cls.env["res.partner"].with_context(no_reset_password=True)
        cls.buyer_1 = cls.partners.create({"name": "Buyer_1"})
        # Create buyer_2
        cls.buyer_2 = cls.partners.create({"name": "Buyer_2"})

    def test_compute_get_offer(self):
        # create offers for House
        self.env["estate.property.offer"].create(
            {
                "price": self.house.expected_price,
                "partner_id": self.buyer_1.id,
                "property_id": self.house.id,
            }
        )
        self.env["estate.property.offer"].create(
            {
                "price": self.house.expected_price,
                "partner_id": self.buyer_2.id,
                "property_id": self.house.id,
            },
        )
        # Create offer for appartment
        self.env["estate.property.offer"].create(
            {
                "price": self.appartment.expected_price,
                "partner_id": self.buyer_1.id,
                "property_id": self.appartment.id,
            }
        )
        self.assertEqual(
            self.house_type.offer_count, 2, "House type offer count must be equal to 2"
        )
        self.assertEqual(
            self.appartment_type.offer_count,
            1,
            "Appartment type offer count must be equal to 1",
        )
