# -*- coding: utf-8 -*-
# # © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'B2C Messenger Panel Control',
    'summary': 'B2C Messenger Panel Control',
    'version': '9.0.1.0.0',
    'category': 'Generic Modules',
    'author': (
        'Jarsa sistemas S.A de C.V. ,'
        'Odoo Community Association (OCA)'),
    'website': 'https://www.odoo-community.org',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/btoc_user_view.xml',
        'views/btoc_campaign_view.xml',
        'views/btoc_message_view.xml',
        'views/btoc_messenger_view.xml',
        'views/btoc_views.xml',
    ],
    'installable': True,
    'active': True
}
