from odoo import models, fields, api


class LaundryService(models.Model):
    _name = "laundry.service"
    _description = "Jenis Layanan Laundry"

    name = fields.Char(string='Nama Layanan', required=True)
    price = fields.Float(string='Harga per kg', default=0.0)
    description = fields.Text(string='Deskripsi') 

    # Many2many ke pesanan
    order_ids = fields.Many2many("laundry.order", string="Pesanan")
