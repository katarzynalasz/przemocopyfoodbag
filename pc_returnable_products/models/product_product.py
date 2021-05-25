from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_returnable_product = fields.Boolean('Can be Return to get coupon ?')
    returnable_product_ids = fields.One2many('returnable.product', 'parent_id', string='Returnable Products')
    returnable_product_details = fields.Char(compute='_compute_returnable_product_details',
                                             string='Returnable Product Details')

    @api.depends('returnable_product_ids', 'returnable_product_ids.product_id',
                 'returnable_product_ids.product_id.name', 'returnable_product_ids.qty')
    def _compute_returnable_product_details(self):
        for rec in self:
            returnable_product_details = ''
            for return_prod in rec.returnable_product_ids.filtered(lambda x: x.product_id):
                info = (str(return_prod.qty) + ' ' + return_prod.product_id.name + '(' +
                        return_prod.product_id.currency_id.symbol + ' ' +
                        str(return_prod.product_id.list_price * return_prod.qty) + ')')
                if returnable_product_details:
                    returnable_product_details += (', ' + info)
                else:
                    returnable_product_details = info
            rec.returnable_product_details = 'Included ' + returnable_product_details if \
                returnable_product_details else ''

    def is_qty_editable(self, products):
        self.ensure_one()
        if self.is_returnable_product :
            if any(products.mapped('returnable_product_ids').filtered(lambda p: p.product_id == self and p.is_mandatory)):
                return False
            else:
                return True
        return True

