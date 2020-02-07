from odoo import api, models, fields, models, _
from datetime import datetime,timedelta,time

class SaleQuotation(models.Model):
    _name = "sale.quotation"
    _description = "Sale Quotation"

    # @api.multi
    # @api.onchange('partner_id')
    # def onchange_partner_id(self):
    #     """
    #     Update the following fields when the partner is changed:
    #     - Pricelist
    #     - Payment term
    #     - Invoice address
    #     - Delivery address
    #     """
    #     if not self.partner_id:
    #         self.update({
    #             'partner_invoice_id': False,
    #             'partner_shipping_id': False,
    #             'payment_term_id': False,
    #             'fiscal_position_id': False,
    #         })
    #         return

    #     addr = self.partner_id.address_get(['delivery', 'invoice'])
    #     values = {
    #         'pricelist_id': self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id or False,
    #         'payment_term_id': self.partner_id.property_payment_term_id and self.partner_id.property_payment_term_id.id or False,
    #         'partner_invoice_id': addr['invoice'],
    #         'partner_shipping_id': addr['delivery'],
    #     }
    #     if self.env.user.company_id.sale_note:
    #         values['note'] = self.with_context(lang=self.partner_id.lang).env.user.company_id.sale_note

    #     if self.partner_id.user_id:
    #         values['user_id'] = self.partner_id.user_id.id
    #     if self.partner_id.team_id:
    #         values['team_id'] = self.partner_id.team_id.id
    #     self.update(values)

    @api.onchange('partner_id')
    def onchange_partner_id_warning(self):
        if not self.partner_id:
            return
        warning = {}
        title = False
        message = False
        partner = self.partner_id

        # If partner has no warning, check its company
        if partner.sale_warn == 'no-message' and partner.parent_id:
            partner = partner.parent_id

        if partner.sale_warn != 'no-message':
            # Block if partner only has warning but parent company is blocked
            if partner.sale_warn != 'block' and partner.parent_id and partner.parent_id.sale_warn == 'block':
                partner = partner.parent_id
            title = ("Warning for %s") % partner.name
            message = partner.sale_warn_msg
            warning = {
                    'title': title,
                    'message': message,
            }
            if partner.sale_warn == 'block':
                self.update({'partner_id': False, 'partner_invoice_id': False, 'partner_shipping_id': False, 'pricelist_id': False})
                return {'warning': warning}

        if warning:
            return {'warning': warning}

    order_line = fields.One2many('sale.order.line', 'order_id', string='Order Lines', copy=True)
    name = fields.Char(string='Serial Number',  copy=False,  index=True, default=lambda self: _('New'))
    sale_id = fields.Many2one('sale.order', string='SO Reference')
    partner_id = fields.Many2one('res.partner',string='Customer')
    # partner_invoice_id = fields.Many2one('res.partner', string='Invoice Address', readonly=True, required=True, help="Invoice address for current sales order.")
    # partner_shipping_id = fields.Many2one('res.partner', string='Delivery Address', readonly=True, required=True, help="Delivery address for current sales order.")        payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms', oldname='payment_term')
    # # payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms', oldname='payment_term')
    date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, copy=False, default=fields.Datetime.now)
    # validity_date = fields.Date(string='Expiration Date', readonly=True, copy=False ),
    # payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms', oldname='payment_term')