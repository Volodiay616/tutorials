# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Real Estate',
    'depends': ['base_setup', 'sale'],
    'category': 'Real Estate/Brokerage',
    'application': False,
    'installable': True,
    'data':[
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_menus.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_user_views.xml'
    ],
    'demo':[
        'demo/estate.property.type.csv',
        'demo/estate_demo.xml'
    ]
    
    
}
