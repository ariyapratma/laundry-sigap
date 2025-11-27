from odoo import models, fields, api


class LaundryEmployee(models.Model):
    _name = "laundry.employee"
    _description = "Karyawan Laundry"

    employee_id = fields.Many2one(
        "hr.employee", string="Karyawan", required=True)

    name = fields.Char(related="employee_id.name", string="Nama")

    department = fields.Char(
        related="employee_id.department_id.name", string="Departemen")
    phone = fields.Char(related="employee_id.work_phone")
    email = fields.Char(related="employee_id.work_email")

    # One2one ke user
    user_id = fields.Many2one("res.users", string="User Akun")
