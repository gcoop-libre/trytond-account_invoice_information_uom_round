# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['Template']


class Template:
    __metaclass__ = PoolMeta
    __name__ = "product.template"

    @fields.depends('use_info_unit', 'info_price', 'info_ratio', 'default_uom',
        'info_list_price')
    def on_change_info_list_price(self, name=None):
        self.list_price = self.get_unit_price(self.info_list_price)
