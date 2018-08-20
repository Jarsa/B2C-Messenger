# Copyright 2018, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'B2C Base',
    'summary': 'Business to Customer',
    'version': '11.0.1.0.0',
    'category': 'Comunication',
    'website': 'https://www.jarsa.com.mx/',
    'author': 'Jarsa Sistemas S.A. de C.V.',
    'license': 'LGPL-3',
    'installable': True,
    'external_dependencies': {
    },
    'depends': [
        'sale_subscription',
    ],
    'data': [
        'views/b2c_base_view.xml',
        'views/b2c_chat_view.xml',
        'views/b2c_workflow_view.xml',
        'views/b2c_workflow_line_view.xml',
        'views/sale_subscription_view.xml',
    ],
    'demo': [],
}
