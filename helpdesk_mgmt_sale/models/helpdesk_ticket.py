from odoo import api, fields, models


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    sale_order_ids = fields.One2many("sale.order", "ticket_id")
    so_count = fields.Integer(
        string="Sale Order Count", compute="_compute_so_count", store=True
    )

    @api.depends("sale_order_ids")
    def _compute_so_count(self):
        for ticket in self:
            ticket.so_count = len(ticket.sale_order_ids)

    def action_view_sale_orders(self):
        """Returns action to view sale orders related to this ticket."""
        action = self.env["ir.actions.actions"]._for_xml_id("sale.action_orders")
        action["domain"] = [("ticket_id", "=", self.id)]
        action["context"] = {
            "default_ticket_id": self.id,
            "default_partner_id": self.partner_id.id,
        }
        return action