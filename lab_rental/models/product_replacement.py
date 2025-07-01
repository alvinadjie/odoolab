from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class ProductReplacement(models.Model):
    """Product Replacement"""
    _name = 'product.replacement'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _rec_name = 'lo_id'

    lo_id = fields.Many2one('order.peminjaman')
    user_id = fields.Many2one('res.users', related='lo_id.user_id')
    email = fields.Char(related='user_id.email')
    student_id = fields.Char(related='user_id.student_id')
    department_id = fields.Many2one(related='user_id.fakultas_id')
    batch_year = fields.Char(related='user_id.tahun_masuk')
    product_id = fields.Many2one('product.product', required=True)
    qty = fields.Float(required=True)
    report_type = fields.Selection(
        [('damage', 'Damage'), ('loss', 'Loss')], tracking=1, required=True)
    date = fields.Date()
    description = fields.Text(placeholder='description or explanation of the loss')
    is_admin = fields.Boolean(related='lo_id.is_admin')

    status = fields.Selection(
        [('review', 'in Review'), ('done', 'Done')], string='Status',
        default='review', tracking=1)
    
    @api.model
    def create(self, vals):
        res = super(ProductReplacement, self).create(vals)
        res.lo_id.pr_id = res.id
        res.lo_id.status = 'pending'
        if res.report_type == 'loss':
            mail_template = self.env.ref('lab_rental.product_replacement_loss_mail_template')
        else:
            mail_template = self.env.ref('lab_rental.product_replacement_damage_mail_template')
        mail_template.send_mail(res.id, force_send=True)
        return res
    
    def done(self):
        self.status = 'done'