# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Estate',
    'depends': ['base_setup', 'sale'],
    'application': False,
    'installable': True,
    'data':[
        'security/ir.model.access.csv',
        'views/estate_menus.xml',
    ]
    
}