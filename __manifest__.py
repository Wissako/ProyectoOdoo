{
    'name': "Gestor De Proyectos",

    'summary': "Gestor donde se lleva el seguimiento de proyectos",

    'description': """
        gestor de proyectos para controlar el desarrollo de apps en 2ºDAM
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'data': [
    'security/security.xml',
    'security/ir.model.access.csv',
    'views/views.xml',
],

}

