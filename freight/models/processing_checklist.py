# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class ProcessingChecklist(models.Model):
    _name = 'processing.checklist'
    _inherit = [ 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Processing Checklist'

    name = fields.Char(string='Name', copy=False)

    @api.model
    def create(self, values):
        if not values.get('name', False) or values['name'] == _('New'):
            values['name'] = self.env['ir.sequence'].next_by_code('processing.checklist') or _('New')
        checklist = super(ProcessingChecklist, self).create(values)
        return checklist

    transport = fields.Selection(([('air', 'Air'), ('ocean', 'Ocean'), ('land', 'Land')]), string='Transport')

    state = fields.Selection([('draft', 'Draft'), ('done_partially', 'Done Partially'), ('confirm', 'Confirm')], default='draft', string='Status', track_visibility='onchange')

    book_id = fields.Many2one('freight.booking', 'Freight Book')

    # show_create_shipment = fields.Boolean('show create shipment')

    #common fields
    booking_confirmed = fields.Boolean('Booking Confirmed', track_visibility='onchange')
    add_additional_charges_not_included_in_quotation = fields.Boolean('Add additional charges not included in quotation', track_visibility='onchange')
    billing = fields.Boolean('Billing', track_visibility='onchange')

    #Air Fields
    Coordinate_with_driver_to_collect_shipment = fields.Boolean('Coordinate with Driver to collect Shipment', track_visibility='onchange')
    pass_customs_documents = fields.Boolean('Pass Customs Documents', track_visibility='onchange')
    final_airway_bill_execution = fields.Boolean('Final Airway Bill Execution', track_visibility='onchange')
    hand_awb_to_driver = fields.Boolean('Hand AWB to Driver', track_visibility='onchange')
    shipment_dropped_to_airport = fields.Boolean('Shipment Dropped to Airport', track_visibility='onchange')
    inspection_if_needed = fields.Boolean('Inspection if needed', track_visibility='onchange')
    confirm_flight_is_on_schedule = fields.Boolean('Confirm Flight is on Schedule', track_visibility='onchange')
    hand_shipment_to_airport = fields.Boolean('Hand Shipment to Airport', track_visibility='onchange')
    send_prealert_to_customer = fields.Boolean('Send Prealert to Customer', track_visibility='onchange')
    track_fleight = fields.Boolean('Track Fleight', track_visibility='onchange')
    fleight_arrival_confirmation = fields.Boolean('Fleight Arrival Confirmation', track_visibility='onchange')
    collect_original_documents_form_airport = fields.Boolean('Collect Original Documents form Airport', track_visibility='onchange')
    pass_bill_of_entry_customs = fields.Boolean('Pass Bill of Entry /Customs', track_visibility='onchange')
    book_collection_timing = fields.Boolean('Book Collection Timing', track_visibility='onchange')
    vehicle_collects_the_shipment = fields.Boolean('Vehicle collects the shipment', track_visibility='onchange')
    driver_contact_consignee_to_arrange_delivery = fields.Boolean('driver contact consignee to arrange delivery', track_visibility='onchange')
    proof_of_delivery = fields.Boolean('Proof of Delivery', track_visibility='onchange')

    #Ocean Fields
    Coordinate_with_driver = fields.Boolean('Coordinate with Driver', track_visibility='onchange')
    driver_pickup_empty_container_from_origin_port = fields.Boolean('Driver pickup empty container from Origin Port', track_visibility='onchange')
    deliver_container_to_point_of_loading = fields.Boolean('Deliver Container to Point of Loading', track_visibility='onchange')
    stuffing = fields.Boolean('Stuffing', track_visibility='onchange')
    collect_documents_from_shipper = fields.Boolean('Collect documents from Shipper', track_visibility='onchange')
    pass_export_decleration = fields.Boolean('Pass Export Decleration', track_visibility='onchange')
    deliver_containers_back_to_port = fields.Boolean('Deliver Containers back to Port', track_visibility='onchange')
    share_shipping_instructions_to_carrier = fields.Boolean('Share Shipping Instructions to Carrier', track_visibility='onchange')
    receive_draft_bL_form_carrier = fields.Boolean('Receive Draft BL form Carrier', track_visibility='onchange')
    share_mbl_draft_with_shipper_for_confirmation_ammendments = fields.Boolean('Share MBL Draft with Shipper for confirmation / Ammendments', track_visibility='onchange')
    confirm_final_mbl_draft = fields.Boolean('Confirm Final MBL Draft', track_visibility='onchange')
    confirm_vessel_etd_advice_customer_if_any_delays  = fields.Boolean('Confirm Vessel ETD / Advice customer if any delays', track_visibility='onchange')
    vessel_departs = fields.Boolean('Vessel Departs', track_visibility='onchange')
    receive_invoice_form_carrier = fields.Boolean('Receive Invoice form Carrier', track_visibility='onchange')
    settele_cahrges_receive_bl_in_hand = fields.Boolean('Settele Cahrges/ Receive BL in Hand', track_visibility='onchange')
    bl_delivered_to_consignee = fields.Boolean('BL delivered to Consignee', track_visibility='onchange')
    confirm_all_original_documents_are_with_consignee = fields.Boolean('Confirm all Original documents are with Consignee', track_visibility='onchange')
    vessel_arrives = fields.Boolean('Vessel Arrives', track_visibility='onchange')
    apply_for_delivery_order = fields.Boolean('Apply for Delivery Order', track_visibility='onchange')
    pass_bill_of_entry = fields.Boolean('Pass Bill of Entry', track_visibility='onchange')
    prepare_lgp = fields.Boolean('Prepare LGP (for LCL Shipments)', track_visibility='onchange')
    coordinate_with_consignee_for_delivery = fields.Boolean('Coordinate with Consignee for Delivery', track_visibility='onchange')
    book_inspection_is_requiered = fields.Boolean('Book Inspection is requiered', track_visibility='onchange')
    apply_for_do_extention_if_needed = fields.Boolean('Apply for DO extention if needed', track_visibility='onchange')
    final_delivery = fields.Boolean('Final Delivery', track_visibility='onchange')
    return_container_to_port = fields.Boolean('Return Container to Port', track_visibility='onchange')

    #Land Fields
    confirm_exact_date_and_time_of_loading = fields.Boolean('Confirm exact date and time of loading', track_visibility='onchange')
    obtain_truck_details = fields.Boolean('Obtain truck Details', track_visibility='onchange')
    truck_loads_shipment = fields.Boolean('Truck Loads Shipment', track_visibility='onchange')
    confirm_all_documents_handed_over_to_driver = fields.Boolean('Confirm all documents handed over to driver', track_visibility='onchange')
    truck_mover_towards_boarder = fields.Boolean('Truck mover towards boarder', track_visibility='onchange')
    update_consignee_of_any_delays_if_any = fields.Boolean('Update Consignee of any delays if any', track_visibility='onchange')
    truck_passes_origin_boarder = fields.Boolean('Truck passes origin boarder', track_visibility='onchange')
    truck_passes_transit_boarder_if_any = fields.Boolean('Truck passes transit boarder if any', track_visibility='onchange')
    truck_passes_final_boarder = fields.Boolean('Truck passes final boarder', track_visibility='onchange')
    truck_reaches_consignee = fields.Boolean('Truck reaches consignee', track_visibility='onchange')
    truck_off_loaded = fields.Boolean('Truck offloaded', track_visibility='onchange')
    obtain_deliver_note_form_customer = fields.Boolean('Obtain deliver note form customer', track_visibility='onchange')

    def select_all(self):
        for rec in self:
            if rec.transport == 'air':
                rec.booking_confirmed = True
                rec.add_additional_charges_not_included_in_quotation = True
                rec.billing = True
                rec.Coordinate_with_driver_to_collect_shipment = True
                rec.pass_customs_documents = True
                rec.final_airway_bill_execution = True
                rec.hand_awb_to_driver = True
                rec.shipment_dropped_to_airport = True
                rec.inspection_if_needed = True
                rec.confirm_flight_is_on_schedule = True
                rec.hand_shipment_to_airport = True
                rec.send_prealert_to_customer = True
                rec.track_fleight = True
                rec.fleight_arrival_confirmation = True
                rec.collect_original_documents_form_airport = True
                rec.pass_bill_of_entry_customs = True
                rec.book_collection_timing = True
                rec.vehicle_collects_the_shipment = True
                rec.driver_contact_consignee_to_arrange_delivery = True
                rec.proof_of_delivery = True
            elif rec.transport == 'ocean':
                rec.booking_confirmed = True
                rec.add_additional_charges_not_included_in_quotation = True
                rec.billing = True
                rec.Coordinate_with_driver = True
                rec.driver_pickup_empty_container_from_origin_port = True
                rec.deliver_container_to_point_of_loading = True
                rec.stuffing = True
                rec.collect_documents_from_shipper = True
                rec.pass_export_decleration = True
                rec.deliver_containers_back_to_port = True
                rec.share_shipping_instructions_to_carrier = True
                rec.receive_draft_bL_form_carrier = True
                rec.share_mbl_draft_with_shipper_for_confirmation_ammendments = True
                rec.confirm_final_mbl_draft = True
                rec.confirm_vessel_etd_advice_customer_if_any_delays = True
                rec.vessel_departs = True
                rec.receive_invoice_form_carrier = True
                rec.settele_cahrges_receive_bl_in_hand = True
                rec.bl_delivered_to_consignee = True
                rec.confirm_all_original_documents_are_with_consignee = True
                rec.vessel_arrives = True
                rec.apply_for_delivery_order = True
                rec.pass_bill_of_entry = True
                rec.prepare_lgp = True
                rec.coordinate_with_consignee_for_delivery = True
                rec.book_inspection_is_requiered = True
                rec.apply_for_do_extention_if_needed = True
                rec.final_delivery = True
                rec.return_container_to_port = True
            elif rec.transport == 'land':
                rec.booking_confirmed = True
                rec.add_additional_charges_not_included_in_quotation = True
                rec.billing = True
                rec.confirm_exact_date_and_time_of_loading = True
                rec.obtain_truck_details = True
                rec.truck_loads_shipment = True
                rec.confirm_all_documents_handed_over_to_driver = True
                rec.truck_mover_towards_boarder = True
                rec.update_consignee_of_any_delays_if_any = True
                rec.truck_passes_origin_boarder = True
                rec.truck_passes_transit_boarder_if_any = True
                rec.truck_passes_final_boarder = True
                rec.truck_reaches_consignee = True
                rec.truck_off_loaded = True
                rec.obtain_deliver_note_form_customer = True

    def action_done_partially(self):
        self.state = 'done_partially'

    def action_confirm(self):
        for rec in self:
            if rec.transport == 'air':
                if rec.booking_confirmed and rec.add_additional_charges_not_included_in_quotation and rec.billing \
                    and rec.Coordinate_with_driver_to_collect_shipment and rec.pass_customs_documents and rec.final_airway_bill_execution \
                    and rec.hand_awb_to_driver and rec.shipment_dropped_to_airport and rec.inspection_if_needed and rec.confirm_flight_is_on_schedule \
                    and rec.hand_shipment_to_airport and rec.send_prealert_to_customer and rec.track_fleight and rec.fleight_arrival_confirmation \
                    and rec.collect_original_documents_form_airport and rec.pass_bill_of_entry_customs and rec.book_collection_timing and rec.vehicle_collects_the_shipment \
                    and rec.driver_contact_consignee_to_arrange_delivery and rec.proof_of_delivery:
                    rec.state = 'confirm'
                    # rec.show_create_shipment = True
                else:
                    raise ValidationError(_('Please Make sure all condition are True for Air Transport Mode.'))

            elif rec.transport == 'ocean':
                if rec.booking_confirmed and rec.add_additional_charges_not_included_in_quotation and rec.billing \
                    and rec.Coordinate_with_driver and rec.driver_pickup_empty_container_from_origin_port and rec.deliver_container_to_point_of_loading \
                    and rec.stuffing and rec.collect_documents_from_shipper and rec.pass_export_decleration and rec.deliver_containers_back_to_port \
                    and rec.share_shipping_instructions_to_carrier and rec.receive_draft_bL_form_carrier and rec.share_mbl_draft_with_shipper_for_confirmation_ammendments \
                    and rec.confirm_final_mbl_draft and rec.confirm_vessel_etd_advice_customer_if_any_delays and rec.vessel_departs and rec.receive_invoice_form_carrier \
                    and rec.settele_cahrges_receive_bl_in_hand and rec.bl_delivered_to_consignee and rec.confirm_all_original_documents_are_with_consignee \
                    and rec.vessel_arrives and rec.apply_for_delivery_order and rec.pass_bill_of_entry and rec.prepare_lgp and rec.coordinate_with_consignee_for_delivery \
                    and rec.book_inspection_is_requiered and rec.apply_for_do_extention_if_needed and rec.final_delivery and rec.return_container_to_port:
                    rec.state = 'confirm'
                    # rec.show_create_shipment = True
                else:
                    raise ValidationError(_('Please Make sure all condition are True for Ocean Transport Mode.'))

            elif rec.transport == 'land':
                if rec.booking_confirmed and rec.add_additional_charges_not_included_in_quotation and rec.billing \
                    and rec.confirm_exact_date_and_time_of_loading and rec.obtain_truck_details and rec.truck_loads_shipment \
                    and rec.confirm_all_documents_handed_over_to_driver and rec.truck_mover_towards_boarder and rec.update_consignee_of_any_delays_if_any \
                    and rec.truck_passes_origin_boarder and rec.truck_passes_transit_boarder_if_any and rec.truck_passes_final_boarder and rec.truck_reaches_consignee \
                    and rec.truck_off_loaded and rec.obtain_deliver_note_form_customer:
                    rec.state = 'confirm'
                    # rec.show_create_shipment = True
                else:
                    raise ValidationError(_('Please Make sure all condition are True for Land Transport Mode.'))
