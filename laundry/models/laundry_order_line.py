from odoo import models, fields, api


class LaundryOrderLine(models.Model):
    _name = "laundry.order.line"
    _description = "Baris Pesanan Laundry"

    order_id = fields.Many2one(
        "laundry.order", string="Pesanan", required=True, ondelete="cascade")
    product_id = fields.Many2one(
        "laundry.product", string="Produk/Jasa", required=True)
    quantity = fields.Float(string="Jumlah", required=True, default=1.0)
    price_unit = fields.Float(
        string="Harga per Satuan", related="product_id.price", readonly=False)
    price_subtotal = fields.Float(
        string="Subtotal", compute="_compute_price_subtotal", store=True)

    @api.depends("quantity", "price_unit")
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = line.quantity * line.price_unit

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.price_unit = self.product_id.price
            self.quantity = 1.0  # reset quantity
