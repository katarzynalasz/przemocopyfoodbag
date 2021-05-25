from odoo import fields, models, api
from odoo.http import request
from odoo.exceptions import UserError, ValidationError
from odoo.addons.website_sale.models.sale_order import SaleOrder as SO

import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):
        old_qty = 0
        product_context = dict(self.env.context)
        product_context.setdefault('lang', self.sudo().partner_id.lang)
        product_with_context = self.env['product.product'].with_context(product_context)
        product = product_with_context.browse(int(product_id))
        if line_id and product.is_returnable_product:
            old_qty = self.env['sale.order.line'].browse(line_id).product_uom_qty
        result = super(SaleOrder, self)._cart_update(product_id=product_id, line_id=line_id, add_qty=add_qty,
                                                     set_qty=set_qty, kwargs=kwargs)
        try:
            if add_qty:
                add_qty = float(add_qty)
        except ValueError:
            add_qty = 1
        try:
            if set_qty:
                set_qty = float(set_qty)
        except ValueError:
            set_qty = 0
        for return_line in product.returnable_product_ids:
            return_line_id = self.env['sale.order.line'].search([('product_id', '=', return_line.product_id.id),
                                                                 ('order_id', '=', self.id)], limit=1)
            return_add_qty = add_qty and add_qty * return_line.qty or add_qty
            return_set_qty = set_qty and set_qty * return_line.qty or set_qty
            if return_line_id:
                if not return_add_qty:
                    return_set_qty += return_line_id.product_uom_qty - (old_qty * return_line.qty)
                line_id = return_line_id.id
            else:
                line_id = None
            self._cart_update(return_line.product_id.id, line_id=line_id,
                              add_qty=return_add_qty,
                              set_qty=return_set_qty, **kwargs)
        return result
