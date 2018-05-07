# The COPYRIGHT file at the top level of this repository contains the full i
# copyright notices and license terms.

from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['InvoiceLine']


class InvoiceLine:
    __metaclass__ = PoolMeta
    __name__ = 'account.invoice.line'

    @fields.depends('product', 'quantity', 'unit')
    def on_change_with_info_quantity(self, name=None):
        if not self.product or not self.quantity:
            return
        qty = self.product.template.calc_info_quantity(self.quantity, self.unit)
        if self.product.template.use_info_unit:
            return self.unit.round(qty, self.product.template.info_unit.rounding)
        else:
            return qty

    @fields.depends('product', 'info_quantity', 'unit')
    def on_change_info_quantity(self):
        if not self.product:
            return
        qty = self.product.calc_quantity(self.info_quantity, self.unit)
        self.quantity = self.unit.round(qty, self.unit.rounding)
        self.amount = self.on_change_with_amount()

    @fields.depends('product', 'quantity', 'unit')
    def on_change_quantity(self):
        if not self.product:
            return
        qty = self.product.template.calc_info_quantity(self.quantity, self.unit)
        if self.product.template.use_info_unit:
            self.info_quantity = self.unit.round(qty, self.product.template.info_unit.rounding)
        else:
            self.info_quantity = float(qty)

    @fields.depends('unit')
    def on_change_with_unit_digits(self, name=None):
        if self.product and self.product.template.use_info_unit:
            return self.product.template.info_unit.digits
        if self.unit:
            return self.unit.digits
        return 2

    @fields.depends('product', 'unit', 'description', '_parent_invoice.type',
        '_parent_invoice.party', 'party', 'invoice', 'invoice_type')
    def on_change_product(self):
        super(InvoiceLine, self).on_change_product()
        if self.product and self.product.template.use_info_unit:
            self.unit_digits = self.product.template.info_unit.digits

    def _credit(self):
        line = super(InvoiceLine, self)._credit()

        if self.info_quantity:
            line.info_quantity = -self.info_quantity
        else:
            line.info_quantity = self.info_quantity

        for field in ('info_unit_price'):
            setattr(line, field, getattr(self, field))

        return line
