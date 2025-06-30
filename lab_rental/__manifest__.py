{
    'name': 'Lab IE SGU - Loan Order',
    'version': '17.0.1.0.0',
    'category': 'Inventory',
    'summary': "The module helps in rental management.",
    'description': "This module allows businesses to order peminjaman",
    'author': 'Andjani',
    'maintainer': 'Andjani',
    'depends': ['product', 'stock', 'base'],
    'data': [
        'security/order_peminjaman_groups.xml',
        'security/rental_order_contract_security.xml',
        'data/email_data.xml',
        'data/ir_sequence_data.xml',
        'data/ir_cron_data.xml',
        'security/ir.model.access.csv',
        'views/order_peminjaman_views.xml',
        'views/product_replacement_views.xml',
        'views/res_partner_views.xml',
        'views/product_product_views.xml',
        'views/scan_product_order_peminjaman_views.xml'
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}

