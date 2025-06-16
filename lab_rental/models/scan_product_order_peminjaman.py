from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta

class ScanProductOrderPeminjaman(models.TransientModel):
    """scan product order peminjaman"""
    _name = 'scan.product.order.peminjaman'
    _description = 'Scan Product Loan Order'

    product_id = fields.Many2one('product.product')
    qty_available  = fields.Float(related='product_id.qty_available')
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