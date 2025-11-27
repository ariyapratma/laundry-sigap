from odoo import models, fields, api


class LaundryOrder(models.Model):
    _name = "laundry.order"
    _description = "Pesanan Laundry"
    # Untuk chatter & notifikasi
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string="Nomor Pesanan",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: "New"
    )
    date_order = fields.Datetime(
        string="Tanggal Pesanan",
        default=fields.Datetime.now
    )
    customer_id = fields.Many2one(
        "laundry.customer", string="Pelanggan", required=True
    )
    employee_id = fields.Many2one(
        'laundry.employee', string='Karyawan Penanggung Jawab'
    )
    service_ids = fields.Many2many(
        "laundry.service", string="Layanan", required=True
    )
    total_weight = fields.Float(string="Berat Total (kg)", default=0.0)
    total_price = fields.Float(
        string="Total Harga", compute="_compute_total_price", store=True
    )
    state = fields.Selection([
        ("draft", "Draft"),
        ("confirmed", "Dikonfirmasi"),
        ("in_progress", "Sedang Diproses"),
        ("ready", "Siap Diambil"),
        ("done", "Selesai"),
        ("cancelled", "Dibatalkan"),
    ], string="Status", default="draft", tracking=True)

    # One2many ke baris pesanan
    order_line_ids = fields.One2many(
        "laundry.order.line", "order_id", string="Detail Pesanan"
    )

    # Hitung total harga dari order line
    amount_total = fields.Float(
        string="Total Harga",
        compute="_compute_amount_total",
        store=True,
        help="Total dari semua baris pesanan"
    )

    @api.depends("order_line_ids.price_subtotal")
    def _compute_amount_total(self):
        for order in self:
            order.amount_total = sum(
                line.price_subtotal for line in order.order_line_ids)

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

    # ---------------
    # Button Actions
    # ---------------
    def action_ready(self):
        self.write({'state': 'ready'})

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_process(self):
        self.write({'state': 'in_progress'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_print_report(self):
        return {
            'name': 'Cetak Laporan',
            'type': 'ir.actions.act_window',
            'res_model': 'laundry.report.wizard',
            'view_mode': 'form',
            'target': 'new',
        }
