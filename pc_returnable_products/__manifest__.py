{
    'name': 'Returnable Products Management',
    'version': '14.0',
    'category': 'Sales',
    'author': 'Vaidehi-Mital',
    'summary': 'Promote your sales with the voucher coupon for the returnable products.',
    'license': 'OPL-1',

    'depends': ['website_sale', 'stock'],
    'data': [
        'security/ir.model.access.csv',

        'views/product_product.xml',
        'views/returnable_product.xml',
        'views/website_sale_templates.xml',
        'views/templates.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
