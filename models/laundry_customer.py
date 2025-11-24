from odoo import models, fields, api


class LaundryCustomer(models.Model):
    _name = "laundry.customer"
    _description = "Pelanggan Laundry"

    name = fields.Char(string="Nama", required=True)
    phone = fields.Char(string="Nomor Telepon")
    email = fields.Char(string="Email")
    address = fields.Text(string="Alamat")

    # One2many ke pesanan
    order_ids = fields.One2many(
        "laundry.order", "customer_id", string="Pesanan")
