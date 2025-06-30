from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta

class ScanProductOrderPeminjaman(models.TransientModel):
    """scan product order peminjaman"""
    _name = 'scan.product.order.peminjaman'
    _description = 'Scan Product Loan Order'

    product_id = fields.Many2one('product.product')
    qty_available  = fields.Float(related='product_id.qty_available')
    categ_id = fields.Many2one('product.category', related='product_id.categ_id')
    default_code = fields.Char(related='product_id.default_code')
    barcode = fields.Char(related='product_id.barcode')
    brand_type = fields.Char(related='product_id.brand_type')
    condition = fields.Char(related='product_id.condition')
    not_for_rent = fields.Boolean(related='product_id.not_for_rent')
    qty = fields.Float()

    def create_loan_order(self):
        lo=self.env['order.peminjaman']
        line_ids = []
        line_ids.append((0,0,{
                'product_id': self.product_id.id,
                'qty': self.qty,
            }))
        loan_order = lo.create({
            'user_id':self.env.user.id,
            'tanggal_peminjaman':fields.Date.today(),
            'tanggal_pengembalian':fields.Date.today(),
            'order_peminjaman_ids':line_ids
        })

        return {
        'type': 'ir.actions.act_window',
        'name': 'Loan Order',
        'res_model': 'order.peminjaman',
        'res_id': loan_order.id,
        'view_mode': 'form',
        'target': 'current',
    }