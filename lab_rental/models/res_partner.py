from odoo import api, fields, models, _
from odoo.exceptions import UserError


class Fakultas(models.Model):
    """student attribute"""
    _name = 'fakultas'

    name = fields.Char()

class ResPartner(models.Model):
    """student attribute"""
    _inherit = 'res.partner'

    student_id = fields.Char('Student ID')
    fakultas_id = fields.Many2one('fakultas', string='Department')
    tahun_masuk = fields.Char(string="Batch Year")

class ResUsers(models.Model):
    """student attribute"""
    _inherit = 'res.users'

    student_id = fields.Char('Student ID')
    fakultas_id = fields.Many2one('fakultas', string='Department')
    tahun_masuk = fields.Char(string="Batch Year")
