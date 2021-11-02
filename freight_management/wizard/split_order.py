from odoo import models

class FreightOrder(models.TransientModel):
    _name = 'split.order'

    def split_order(self):
        if self._context.get('active_id'):
            old_order = self.env['freight.order'].browse(self._context.get('active_id'))
            new_order = old_order.copy()
            new_order_lines = []
            for order_line in old_order.order_line_ids:
                if order_line.remaining > 0:
                    vals = {
                        'product_id':order_line.product_id.id,
                        'description':order_line.description,
                        'inner_packs':order_line.inner_packs,
                        'outer_packs':order_line.outer_packs,
                        'type':order_line.type,
                        'quantity':order_line.quantity_received,
                        'unit_of_qty':order_line.unit_of_qty and order_line.unit_of_qty.id,
                        'line_price':order_line.line_price,
                        'item_price':order_line.item_price,
                        'invoice_no':order_line.invoice_no,
                        'origin':order_line.origin and order_line.origin.id,
                        'manufacturer':order_line.manufacturer and order_line.manufacturer.id,
                        'manufacturer_address':order_line.manufacturer_address and order_line.manufacturer_address.id,
                        'freight_order_line_ref_id':order_line.id if self._context.get('split_order') else False,
                    }
                    qty = order_line.remaining
                    if not self._context.get('split_order'):
                        vals.update({'quantity': qty})
                        qty = order_line.quantity - order_line.remaining

                    order_line.write({'quantity': qty, 'quantity_received': 0})
                    new_order_lines.append((0, 0, vals))

            if self._context.get('split_order'):
                new_order.split_order_id = old_order.id
            else:
                new_order.new_order_id = old_order.id
            new_order.write({'order_line_ids':new_order_lines})

        return True
