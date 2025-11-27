from odoo import models, fields, api


class LaundryCustomer(models.Model):
    _name = "laundry.customer"
    _description = "Pelanggan Laundry"

    # name = fields.Char(string="Nama", required=True)
    # phone = fields.Char(string="Nomor Telepon")
    # email = fields.Char(string="Email")
    # address = fields.Text(string="Alamat")
    partner_id = fields.Many2one(
        "res.partner", string="Pelanggan", required=True)


    name = fields.Char(related="partner_id.name", string="Nama")
    phone = fields.Char(related="partner_id.phone", string="Nomor Telepon")
    email = fields.Char(related="partner_id.email", string="Email")
    address = fields.Char(related="partner_id.street", string="Alamat")

    total_orders = fields.Integer(
        string="Jumlah Pesanan",
        compute="_compute_total_orders",
        store=True,
        help="Total pesanan yang pernah dibuat oleh pelanggan ini"
    )

    # One2many ke pesanan
    order_ids = fields.One2many(
        "laundry.order", "customer_id", string="Pesanan")


    @api.depends("order_ids")
    def _compute_total_orders(self):
        for customer in self:
            customer.total_orders = len(customer.order_ids)
