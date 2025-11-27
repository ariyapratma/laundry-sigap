from odoo import models, fields, api


class LaundryReportWizard(models.TransientModel):
    _name = "laundry.report.wizard"
    description = "Cetak Laporan Pesanan"

    date_from = fields.Date("Dari Tanggal", required=True)
    date_to = fields.Date("Sampai Tanggal", required=True)

    def action_print_report(self):
        return self.env.ref('laundry.action_laundry_order_report').report_action(None, data={
            'date_from': self.date_from,
            'date_to': self.date_to,
        })
