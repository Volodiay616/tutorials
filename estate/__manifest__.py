#!/usr/bin/python3
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Real Estate",
    "version": "14.0.0.1.0",
    "website": "https://github.com/Volodiay616/tutorials",
    "license": "AGPL-3",
    "author": "Vladimir",
    "license": "AGPL-3",
    "depends": ["base_setup", "sale"],
    "category": "Real Estate/Brokerage",
    "application": False,
    "installable": True,
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/estate_menus.xml",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_user_views.xml",
    ],
    "demo": ["demo/estate.property.type.csv", "demo/estate_demo.xml"],
}
