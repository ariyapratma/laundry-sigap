from odoo import models, fields, api


class LaundryService(models.Model):
    _name = "laundry.service"
    _description = "Jenis Layanan Laundry"

    name = fields.char(string="Nama Layanan", required=True)
    _description = fields.Float(string="Harga per kg", default=0.0)

    # Many2many ke pesanan
    order_ids = fields.Many2many("laundry.order", string="Pesanan")
