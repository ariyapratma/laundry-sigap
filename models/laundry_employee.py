from odoo import models, fields, api


class LaundryEmployee(models.Model):
    _name = "laundry.employee"
    _description = "Karyawan Laundry"

    name = fields.Char(string="Nama Karyawan", required=True)
    phone = fields.Char(string="Nomor Telepon")
    email = fields.Char(string="Email")

    # One2one ke user
    user_id = fields.Many2one("res.users", string="User Akun")
