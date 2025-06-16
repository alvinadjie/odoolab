# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
{
    'name': 'Odoo - Order Peminjaman Lab',
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

