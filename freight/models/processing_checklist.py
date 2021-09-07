# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class ProcessingChecklist(models.Model):
    _name = 'processing.checklist'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Processing Checklist'

    name = fields.Char(string='Name', copy=False)

    @api.model
    def create(self, values):
        if not values.get('name', False) or values['name'] == _('New'):
            values['name'] = self.env['ir.sequence'].next_by_code('processing.checklist') or _('New')
        checklist = super(ProcessingChecklist, self).create(values)
        return checklist

    transport = fields.Selection(([('air', 'Air'), ('ocean', 'Ocean'), ('land', 'Land')]), string='Transport')

    #Air Fields
    booking_confirmed = fields.Boolean('Booking Confirmed')
    Coordinate_with_driver_to_collect_shipment = fields.Boolean('Coordinate with Driver to collect Shipment')
    pass_customs_documents = fields.Boolean('Pass Customs Documents')
    final_airway_bill_execution = fields.Boolean('Final Airway Bill Execution')
    hand_awb_to_driver = fields.Boolean('Hand AWB to Driver')
    shipment_dropped_to_airport = fields.Boolean('Shipment Dropped to Airport')
    inspection_if_needed = fields.Boolean('Inspection if needed')
    confirm_flight_is_on_schedule = fields.Boolean('Confirm Flight is on Schedule')
    hand_shipment_to_airport = fields.Boolean('Hand Shipment to Airport')
    send_prealert_to_customer = fields.Boolean('Send Prealert to Customer')
    track_fleight = fields.Boolean('Track Fleight')
    fleight_arrival_confirmation = fields.Boolean('Fleight Arrival Confirmation')
    collect_original_documents_form_airport = fields.Boolean('Collect Original Documents form Airport')
    pass_bill_of_entry_customs = fields.Boolean('Pass Bill of Entry /Customs')
    book_collection_timing = fields.Boolean('Book Collection Timing')
    vehicle_collects_the_shipment = fields.Boolean('Vehicle collects the shipment')
    driver_contact_consignee_to_arrange_delivery = fields.Boolean('driver contact consignee to arrange delivery')
    proof_of_delivery = fields.Boolean('Proof of Delivery')
    add_additional_charges_not_included_in_quotation = fields.Boolean('Add additional charges not included in quotation')
    billing = fields.Boolean('Billing')

    #Ocean Fields
    Coordinate_with_driver = fields.Boolean('Coordinate with Driver')
    driver_pickup_empty_container_from_origin_port = fields.Boolean('Driver pickup empty container from Origin Port')
    deliver_container_to_point_of_loading = fields.Boolean('Deliver Container to Point of Loading')
    stuffing = fields.Boolean('Stuffing')
    collect_documents_from_shipper = fields.Boolean('Collect documents from Shipper')
    pass_export_decleration = fields.Boolean('Pass Export Decleration')
    deliver_containers_back_to_port = fields.Boolean('Deliver Containers back to Port')
    share_shipping_instructions_to_carrier = fields.Boolean('Share Shipping Instructions to Carrier')
    receive_draft_bL_form_carrier = fields.Boolean('Receive Draft BL form Carrier')
    share_mbl_draft_with_shipper_for_confirmation_ammendments = fields.Boolean('Share MBL Draft with Shipper for confirmation / Ammendments')
    confirm_final_mbl_draft = fields.Boolean('Confirm Final MBL Draft')
    confirm_vessel_etd_advice_customer_if_any_delays  = fields.Boolean('Confirm Vessel ETD / Advice customer if any delays')
    vessel_departs = fields.Boolean('Vessel Departs')
    receive_invoice_form_carrier = fields.Boolean('Receive Invoice form Carrier')
    settele_cahrges_receive_bl_in_hand = fields.Boolean('Settele Cahrges/ Receive BL in Hand')
    bl_delivered_to_consignee = fields.Boolean('BL delivered to Consignee')
    confirm_all_original_documents_are_with_consignee = fields.Boolean('Confirm all Original documents are with Consignee')
    vessel_arrives = fields.Boolean('Vessel Arrives')
    apply_for_delivery_order = fields.Boolean('Apply for Delivery Order')
    pass_bill_of_entry = fields.Boolean('Pass Bill of Entry')
    prepare_lgp = fields.Boolean('Prepare LGP (for LCL Shipments)')
    coordinate_with_consignee_for_delivery = fields.Boolean('Coordinate with Consignee for Delivery')
    book_inspection_is_requiered = fields.Boolean('Book Inspection is requiered')
    apply_for_do_extention_if_needed = fields.Boolean('Apply for DO extention if needed')
    final_delivery = fields.Boolean('Final Delivery')
    return_container_to_port = fields.Boolean('Return Container to Port')

    #Land Fields
    confirm_exact_date_and_time_of_loading = fields.Boolean('Confirm exact date and time of loading')
    obtain_truck_details = fields.Boolean('Obtain truck Details')
    truck_loads_shipment = fields.Boolean('Truck Loads Shipment')
    confirm_all_documents_handed_over_to_driver = fields.Boolean('Confirm all documents handed over to driver')
    truck_mover_towards_boarder = fields.Boolean('Truck mover towards boarder')
    update_consignee_of_any_delays_if_any = fields.Boolean('Update Consignee of any delays if any')
    truck_passes_origin_boarder = fields.Boolean('Truck passes origin boarder')
    truck_passes_transit_boarder_if_any = fields.Boolean('Truck passes transit boarder if any')
    truck_passes_final_boarder = fields.Boolean('Truck passes final boarder')
    truck_reaches_consignee = fields.Boolean('Truck reaches consignee')
    truck_off_loaded = fields.Boolean('Truck offloaded')
    obtain_deliver_note_form_customer = fields.Boolean('Obtain deliver note form customer')