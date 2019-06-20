# -*- coding: utf-8 -*-
# © 2015 Vauxoo
# © 2015 Eezee-It, MONK Software
# © 2013 Camptocamp
# © 2009-2013 Akretion,
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountInvoiceRefund(models.TransientModel):
    _inherit = "account.invoice.refund"

    def _default_description(self):
        return self.env.context.get('description', '')

    description = fields.Char(default=_default_description)

    @api.depends('date_invoice')
    @api.one
    def _get_refund_only(self):
        # for correct of account.invoice.refund
        # we need to override active_ids of crm.claim with account.invoice ids
        # because previously this wizard was only called from account.invoice
        context = self.env.context
        invoice_ids = context.get('invoice_ids')
        ctx = context.copy()
        if context.get('active_model') == 'crm.claim' and invoice_ids:
            ctx.update({
                'active_id': invoice_ids[:1],
                'active_ids': invoice_ids,
            })
        return super(
            AccountInvoiceRefund, self.with_context(ctx))._get_refund_only()

    @api.multi
    def compute_refund(self, mode='refund'):
        self.ensure_one()
        invoice_ids = self.env.context.get('invoice_ids', [])
        if invoice_ids:
            self = self.with_context(active_ids=invoice_ids)
        return super(AccountInvoiceRefund, self).compute_refund(mode=mode)
