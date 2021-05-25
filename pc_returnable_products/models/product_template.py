from odoo import models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _get_combination_info(self, combination=False, product_id=False, add_qty=1, pricelist=False,
                              parent_combination=False, only_template=False):
        result = super(ProductTemplate, self)._get_combination_info(combination, product_id, add_qty, pricelist,
                                                                    parent_combination, only_template)
        if 'product_id' and 'list_price' and 'price' in result:
            product = self.env['product.product'].browse(result.get('product_id'))
            return_list_price = sum([(product.product_id.sudo().price_compute('list_price')[product.product_id.id] * product.qty) for product in
                                     product.returnable_product_ids])
            list_price = return_list_price + result.get('list_price')
            price = return_list_price + result.get('price')
            result.update({'list_price': list_price, 'price': price})
        if result['product_id']:
            product = self.env['product.product'].sudo().browse(result['product_id'])
            result.update({
                'returnable_product_details': product.returnable_product_details,
            })
        return result
