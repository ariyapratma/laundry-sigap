from odoo import models, fields, api


class LaundryOrder(models.Model):
    _name = "laundry.order"
    _description = "Pesanan Laundry"
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Untuk notifikasi email

    name = fields.Char(string="Nomor Pesanan", required=True,
                       copy=False, readonly=True, default=lambda self: "New")
    date_order = fields.Datetime(
        string="Tanggal Pesanan", default=fields.Datetime.now)
    customer_id = fields.Many2one(
        "laundry.customer", string="Pelanggan", required=True)
    employee_id = fields.Many2one(
        'laundry.employee', string='Karyawan Penanggung Jawab')
    service_ids = fields.Many2many(
        "laundry.service", string="Layanan", required=True)
    total_weight = fields.Float(string="Berat Total (kg)", default=0.0)
    total_price = fields.Float(
        string="Total Harga", compute="_compute_total_price", store=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Dikonfirmasi"),
            ("in_progress", "Sedang Diproses"),
            ("done", "Selesai"),
            ("cancelled", "Dibatalkan"),
        ],
        string="Status",
        default="draft",
    )

    @api.depends('service_ids', 'total_weight')
    def _compute_total_price(self):
        for order in self:
            total = 0.0
            for service in order.service_ids:
                total += service.price * order.total_weight
            order.total_price = total

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'laundry.order') or 'New'
        return super(LaundryOrder, self).create(vals)

    def action_confirm(self):
        self.state = 'confirmed'

    def action_in_progress(self):
        self.state = 'in_progress'

    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancelled'
