odoo.define('pc_returnable_products.VariantMixin', function (require) {
'use strict';

var VariantMixin = require('sale.VariantMixin');
var publicWidget = require('web.public.widget');
var ajax = require('web.ajax');
var core = require('web.core');
var QWeb = core.qweb;

publicWidget.registry.WebsiteSale.include({
    /**
     * Adds the stock checking to the regular _onChangeCombination method
     * @override
     */
    _onChangeCombination: function (ev, $parent, combination){
        this._super.apply(this, arguments);
        $parent
            .find('.returnable_product_details')
            .first()
            .text(combination.returnable_product_details || 0)
            .trigger('change');
    }
});

return VariantMixin;

});
