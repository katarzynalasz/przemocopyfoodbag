from odoo import models, fields


class ReturnableProduct(models.Model):
    _name = 'returnable.product'
    _description = 'Returnable Product'

    parent_id = fields.Many2one('product.product')
    product_id = fields.Many2one('product.product', required=1)
    qty = fields.Integer('Quantity', required=1)
    is_mandatory = fields.Boolean('Is mandatory ?')
