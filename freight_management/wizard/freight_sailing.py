from odoo import api, fields, models, _


class FreightSailing(models.TransientModel):
    _name = 'freight.sailing'

    voyage_no = fields.Char('Voyage No')
    vessel_id = fields.Many2one('freight.vessel', 'Vessel')
    carrier_id = fields.Many2one('res.partner', string='Carrier')

    def add_new_sailing(self):
        """
        Add sailing in the booking
        :return:
        """
        booking = self.env['freight.booking'].browse(self._context.get('active_ids'))
        booking.write({'carrier_id': self.carrier_id and self.carrier_id.id or False,
                       'voyage_no': self.voyage_no,
                       'vessel_id': self.vessel_id and self.vessel_id.id or False})
        return True
