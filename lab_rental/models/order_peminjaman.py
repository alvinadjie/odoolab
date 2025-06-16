from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta

class OrderPeminjaman(models.Model):
    """order peminjaman"""
    _name = 'order.peminjaman'
    _description = 'Loan Order'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char(default=lambda self: self.env['ir.sequence'].next_by_code('order.peminjaman'))
    tanggal_peminjaman = fields.Date(tracking=1, required=True, string='Request Date')
    tanggal_pengembalian = fields.Date(tracking=1,required=True, string='Return Date')
    actual_return_date = fields.Date(tracking=1)
    approved_date = fields.Date(tracking=1)
    status = fields.Selection(
        [('new', 'New'), ('wait', 'To Approve'), ('confirmed', 'Approved'),('tolak', 'Rejected'),('pending','Pending'),
         ('selesai', 'Done')], string='Status',
        default='new', tracking=1)
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user, required=True, string="Borrower")
    partner_id = fields.Many2one('res.partner', related='user_id.partner_id')
    student_id = fields.Char('Student ID', related='user_id.student_id')
    fakultas_id = fields.Many2one('fakultas', related='user_id.fakultas_id')
    tahun_masuk = fields.Char('Batch Year', related='user_id.tahun_masuk')
    purpose = fields.Char()
    order_peminjaman_ids = fields.One2many('order.peminjaman.line','order_id')
    alasan_penolakan = fields.Char(string="Reject Reason")
    request_to_id = fields.Many2one('res.users')
    is_admin = fields.Boolean(compute='compute_is_admin')
    domain_request_to_ids = fields.Many2many('res.users', compute='compute_domain_admin')
    pr_id = fields.Many2one('product.replacement')
    
    def _check_date_range(self):
        for rec in self:
            if rec.tanggal_peminjaman and rec.tanggal_pengembalian:
                if rec.tanggal_pengembalian < rec.tanggal_peminjaman:
                    raise ValidationError("End date cannot be before start date.")
                if rec.tanggal_pengembalian - rec.tanggal_peminjaman > timedelta(days=14):
                    raise ValidationError("The duration between start and end date cannot exceed two weeks.")
               

    @api.depends('user_id')
    def compute_domain_admin(self):
        for rec in self:
            admin = self.env['res.users'].sudo().search([])
            admin = admin.filtered(lambda x:x.has_group('lab_rental.group_rental_sales_manager'))
            rec.domain_request_to_ids = [(6, 0, admin.ids)]

    @api.depends('user_id')
    def compute_is_admin(self):
        for rec in self:
            rec.is_admin = False
            if self.env.user.has_group('lab_rental.group_rental_sales_manager'):
                rec.is_admin = True
    
    @api.model
    def cron_overdue(self):
        mail_template = self.env.ref('lab_rental.overdue_return_admin_mail_template')
        active_loan = self.env['order.peminjaman'].search([('status','=', 'confirmed'),('tanggal_pengembalian','<',datetime.today())])
        for loan in active_loan:
            mail_template.send_mail(loan.id, force_send=True)
    
    @api.model
    def cron_reminder(self):
        #to be create cron h-3 and due date
        #wording soon and today based on tanggal
        mail_template = self.env.ref('lab_rental.loan_reminder_mail_template')
        reminder_date = self.tanggal_pengembalian - timedelta(days=3)
        active_loan = self.env['order.peminjaman'].search([('status','=', 'confirmed'),('tanggal_pengembalian','<',datetime.today())])
        for loan in active_loan:
            mail_template.send_mail(loan.id, force_send=True)
    
    def defect_product(self):
        # self.status = 'pending'
        # form_id = self.env.ref('lab_rental.product_replacement_view_form').id
        context = {
            'default_lo_id':self.id
        }
        return {'name': 'Product Replacement',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'product.replacement',
                'target': 'current',
                'context':context
                }

    def approve(self):
        self.status = 'confirmed'
        mail_template = self.env.ref('lab_rental.approve_mail_template')
        admin = self.env['res.users'].search([])
        admin = admin.filtered(lambda x:x.has_group('lab_rental.group_rental_sales_manager'))
        res = self.env['res.users'].search_read([('id', 'in', list(admin.ids))], ['email'])
        emails = set(r['email'] for r in res if r.get('email'))
        email_values = {
            # 'email_to': ','.join(sel.partner_id.email)
        }
        self.approved_date = fields.Date.today()
        if self.approved_date > self.tanggal_peminjaman:
            delta_days = (self.approved_date - self.tanggal_peminjaman).days
            self.tanggal_pengembalian = self.tanggal_pengembalian + timedelta(days=delta_days)
        self.env.cr.commit()
        mail_template.send_mail(self.id, force_send=True, email_values=email_values)
        self.sudo().create_delivery_order(self.partner_id)
        #move date when approved date > start date
        
        
    def ajukan_pinjaman(self):
        self._check_date_range()
        for line in self.order_peminjaman_ids:
            line._check_qty()
        mail_template = self.env.ref('lab_rental.loan_request_mail_template')
        self.status = 'wait'
        email_values = {
            # 'email_to': ','.join(sel.partner_id.email)
        }
        mail_template.send_mail(self.id, force_send=True, email_values=email_values)

    def tolak(self):
        mail_template = self.env.ref('lab_rental.reject_mail_template')
        self.status = 'tolak'
        email_values = {
            # 'email_to': ','.join(sel.partner_id.email)
        }
        mail_template.send_mail(self.id, force_send=True, email_values=email_values)
    def done(self):
        mail_template = self.env.ref('lab_rental.return_success_mail_template')
        mail_template_2 = self.env.ref('lab_rental.return_success_by_student_mail_template')
        self.status = 'selesai'
        self.actual_return_date =  fields.Date.today()

        email_values = {
            # 'email_to': ','.join(sel.partner_id.email)
        }
        mail_template.send_mail(self.id, force_send=True, email_values=email_values)
        mail_template_2.send_mail(self.id, force_send=True, email_values=email_values)
        self.sudo().create_receipt(self.partner_id)

    def create_delivery_order(self, partner):
        Picking = self.env['stock.picking']
        Move = self.env['stock.move']

        internal_location = self.env.ref('stock.stock_location_stock')
        partner_location = self.env.ref('stock.stock_location_customers')

        # 1. Get the delivery picking type (usually 'Delivery Orders')
        picking_type = self.env['stock.picking.type'].search([('code', '=', 'outgoing')], limit=1)
        if not picking_type:
            raise UserError("No outgoing picking type found!")
        
        stock_move = []
        for line in self.order_peminjaman_ids:
            stock_move.append((0,0,{
                'name': line.product_id.name,
                'product_id': line.product_id.id,
                'product_uom_qty': line.qty,
                'product_uom': line.product_id.uom_id.id,
                'location_id': internal_location.id,
                'location_dest_id': partner_location.id,
            }))

        # 2. Create the picking (delivery order)
        picking = Picking.create({
            'partner_id': partner.id,
            'picking_type_id': picking_type.id,
            'location_id': internal_location.id,            # usually WH/Stock
            'location_dest_id': partner_location.id,     
            'move_ids_without_package': stock_move
        })

        picking.action_confirm()

        # 4. Assign stock (optional for receipt, since stock is incoming)
        picking.action_assign()

        # 5. Mark as done (receive the product)
        # for move_line in picking.move_ids_without_package:
        #     move_line.product_qty = move_line.product_uom_qty

        picking.button_validate()
    
    def create_receipt(self, partner):
        Picking = self.env['stock.picking']
        Move = self.env['stock.move']

        # 1. Get incoming picking type
        picking_type = self.env['stock.picking.type'].search([('code', '=', 'incoming')], limit=1)
        if not picking_type:
            raise UserError("No incoming picking type found!")
        
        # 2. Create the picking (receipt)
        internal_location = self.env.ref('stock.stock_location_stock')
        partner_location = self.env.ref('stock.stock_location_customers')

        stock_move = []
        for line in self.order_peminjaman_ids:
            stock_move.append((0,0,{
                'name': line.product_id.name,
                'product_id': line.product_id.id,
                'product_uom_qty': line.qty,
                'product_uom': line.product_id.uom_id.id,
                'location_id': partner_location.id,
                'location_dest_id': internal_location.id,
            }))
        picking = Picking.create({
            'partner_id': partner.id,
            'picking_type_id': picking_type.id,
            'location_id': partner_location.id,        # usually Vendors
            'location_dest_id': internal_location.id,
            'move_ids_without_package': stock_move
        })

        picking.action_confirm()

        # 4. Assign stock (optional for receipt, since stock is incoming)
        picking.action_assign()

        # 5. Mark as done (receive the product)
        # for move_line in picking.move_ids_without_package:
        #     move_line.product_qty = move_line.product_uom_qty

        picking.button_validate()

class OrderPeminjamanLine(models.Model):
    """order peminjaman"""
    _name = 'order.peminjaman.line'

    order_id = fields.Many2one('order.peminjaman')
    product_id = fields.Many2one('product.product')
    qty = fields.Float()
    uom_id = fields.Many2one('uom.uom', related='product_id.uom_id')
    qty_available=fields.Float(related='product_id.qty_available')

    def _check_qty(self):
        for rec in self:
            if rec.qty > rec.qty_available:
                raise ValidationError("Product is not available.")