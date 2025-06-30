from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    condition = fields.Char()
    brand_type = fields.Char('Brand / Type')
    not_for_rent = fields.Boolean(string='Not for Lend')
    

