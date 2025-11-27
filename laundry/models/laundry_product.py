from odoo import models, fields, api


class LaundryProduct(models.Model):
    _name = "laundry.product"
    _description = "Produk/Jasa Laundry"

    name = fields.Char(string="Nama Produk/Jasa", required=True)
    description = fields.Text(string="Deskripsi")
    price = fields.Float(string="Harga per Satuan", required=True, default=0.0)
    
    # Tambahkan field type agar bisa filter di domain
    type = fields.Selection([
        ('service', 'Service'),      # Layanan
        ('product', 'Product'),      # Barang (jika kamu tambahkan nanti)
        ('consu', 'Consumable'),     # Barang habis pakai (opsional)
    ], string="Tipe Produk", default="service")
    
    unit_of_measure = fields.Selection([
        ("kg", "Kilogram"),
        ("pcs", "Pcs"),
        ("set", "Set")
    ], string="Satuan", default="kg")

    # Relasi ke pesanan (One2many): satu produk bisa muncul di banyak pesanan
    order_line_ids = fields.One2many(
        "laundry.order.line", "product_id", string="Baris Pesanan"
    )