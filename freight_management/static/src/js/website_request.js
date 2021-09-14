odoo.define('freight_management.website_request', function (require) {
'use strict';
require('web.dom_ready');
$(document).ready(function (){
        $('#req_ocean_div').hide();
        $('#req_rail_div').hide()
	    $('#req_land_div').hide();
	    $('#dng_info_req').hide();
	    $('#danger_info_req').hide();
//	    $('#danger_class').hide();
//	    $('#danger_class_info').hide();
	    $('input[type=datetime-local][name=date]').change(function() {
	        $('#new_date').val(this.value);
	    });

        $("#freight_hs_code_ids").select2();
        $('#main_data').hide()
        $('#shipping_type_div').hide()

        $('#air_lbl_1').hide()
        $('#air_data_1').hide()
        $('#air_lbl_2').hide()
        $('#air_data_2').hide()

        $('#ocean_lbl_1').hide()
        $('#ocean_data_1').hide()
        $('#ocean_lbl_2').hide()
        $('#ocean_data_2').hide()

        $('#land_lbl_1').hide()
        $('#land_data_1').hide()
        $('#land_lbl_2').hide()
        $('#land_data_2').hide()
//        $("#incoterm").removeAttr('required');
        $("#incoterm").attr('required', '');


	            /*$('.vehicle_size').hide();
                $('.vehicle_type').hide();*/

    $('input[type=radio][name=mode_of_transport]').change(function() {
            if (this.value == 'air') {
                $('#main_data').show()

	            $('#air_lbl_1').show()
	            $('#air_data_1').show()
	            $('#air_lbl_2').show()
	            $('#air_data_2').show()
	            $('#shipping_type_div').hide()

//REQUIRED
	            $("#air_source_location_id").attr('required', '');
	            $("#ocean_source_location_id").removeAttr('required');
	            $("#air_destination_location_id").attr('required', '');
	            $("#ocean_destination_location_id").removeAttr('required');
	            $("#equipment_type").removeAttr('required');
	            $("#incoterm").attr('required', '');
	            $("#vehicle_size").removeAttr('required');
	            $("#vehicle_type").removeAttr('required');
//EMD
                $("#incoterm").show()
                $('#incoterm_lbl').show()
	            $('#ocean_lbl_1').hide()
	            $('#ocean_data_1').hide()
	            $('#ocean_lbl_2').hide()
	            $('#ocean_data_2').hide()

	            $('#land_lbl_1').hide()
	            $('#land_data_1').hide()
	            $('#land_lbl_2').hide()
	            $('#land_data_2').hide()
            }
            else if (this.value == 'ocean') {
                console.log("OCEAN");
                $('#main_data').show()
	            $('#air_lbl_1').hide()
	            $('#air_data_1').hide()
	            $('#air_lbl_2').hide()
	            $('#air_data_2').hide()

	            $('#shipping_type_div').show()
	            $('#req_land_div').hide()
	            $('#req_ocean_div').show()
	            $('#req_rail_div').hide()

	            $('#ocean_lbl_1').show()
	            $('#ocean_data_1').show()
	            $('#ocean_lbl_2').show()
	            $('#ocean_data_2').show()
//REQUIRED
                $("#vehicle_size").removeAttr('required');
	            $("#vehicle_type").removeAttr('required');
	            $("#air_source_location_id").removeAttr('required');
	            $("#ocean_source_location_id").attr('required', '');
                $("#air_destination_location_id").removeAttr('required');
	            $("#ocean_destination_location_id").attr('required', '');
	            $("#incoterm").attr('required', '');
	            $("#equipment_type").attr('required', '');
//EMD
                $("#incoterm").show()
                $('#incoterm_lbl').show()
                $('#land_lbl_1').hide()
	            $('#land_data_1').hide()
	            $('#land_lbl_2').hide()
	            $('#land_data_2').hide()
            }
            else if (this.value == 'land') {
                console.log("LAND");
                $('#main_data').show()
	            $('#air_lbl_1').hide()
	            $('#air_data_1').hide()
	            $('#air_lbl_2').hide()
	            $('#air_data_2').hide()

	            $('#shipping_type_div').show()
	            $('#req_land_div').show()
	            $('#req_ocean_div').hide()
	            $('#req_rail_div').hide()
//REQUIRED
                $("#vehicle_size").attr('required', '');
                $("#vehicle_type").attr('required', '');
                $("#equipment_type").removeAttr('required');
	            $("#air_source_location_id").removeAttr('required');
                $("#air_destination_location_id").removeAttr('required');
                $("#ocean_source_location_id").removeAttr('required');
                $("#ocean_destination_location_id").removeAttr('required');
                $("#incoterm").removeAttr('required');
                $("#incoterm").hide()
                $('#incoterm_lbl').hide()
//EMD
	            $('#ocean_lbl_1').hide()
	            $('#ocean_data_1').hide()
	            $('#ocean_lbl_2').hide()
	            $('#ocean_data_2').hide()

	            $('#land_lbl_1').show()
	            $('#land_data_1').show()
	            $('#land_lbl_2').show()
	            $('#land_data_2').show()

            }
            else if (this.value == 'rail') {
                console.log("RAIL");
                $('#main_data').hide()
	            $('#air_lbl_1').hide()
	            $('#air_data_1').hide()
	            $('#air_lbl_2').hide()
	            $('#air_data_2').hide()

	            $('#shipping_type_div').show()
	            $('#req_land_div').hide()
	            $('#req_ocean_div').hide()
	            $('#req_rail_div').show()
//REQUIRED
                $("#vehicle_size").removeAttr('required');
                $("#vehicle_type").removeAttr('required');
                $("#equipment_type").removeAttr('required');
	            $("#air_source_location_id").removeAttr('required');
                $("#air_destination_location_id").removeAttr('required');
                $("#ocean_source_location_id").removeAttr('required');
                $("#ocean_destination_location_id").removeAttr('required');
                $("#incoterm").attr('required', '');
//EMD
                $("#incoterm").show()
                $('#incoterm_lbl').show()
	            $('#ocean_lbl_1').hide()
	            $('#ocean_data_1').hide()
	            $('#ocean_lbl_2').hide()
	            $('#ocean_data_2').hide()
	            $('#land_lbl_1').show()
	            $('#land_data_1').show()
	            $('#land_lbl_2').show()
	            $('#land_data_2').show()
            }
            else{
                $("#incoterm").attr('required', '');
	            $("#incoterm").show()
                $('#main_data').hide()
                $('#req_land_div').hide()
	            $('#req_ocean_div').hide()
	            $('#req_rail_div').hide()
                $('#shipping_type_div').hide()
                $("#vehicle_size").removeAttr('required');
	            $("#vehicle_type").removeAttr('required');
                $("#equipment_type").removeAttr('required');
                $("#air_source_location_id").removeAttr('required');
                $("#air_destination_location_id").removeAttr('required');
                $("#ocean_source_location_id").removeAttr('required');
                $("#ocean_destination_location_id").removeAttr('required');
            }
        });

        $('#dangerous_goods_class_lbl_req').hide();
         $('#dangerous_goods_class_field_req').hide();

        $('input[type=radio][name=is_dangerous_goods]').change(function() {
            console.log("is_dangerous_goods")
              if (this.value == 'yes') {
                $('#danger_info_req').show();
                $('#dangerous_goods_class_field_req').show();
                $('#dangerous_goods_class_lbl_req').show();
                $('#dng_info_req').show();
            }
            else{
                $('#danger_info_req').hide();
                $('#dng_info_req').hide();
                $('#dangerous_goods_class_lbl_req').hide();
                $('#dangerous_goods_class_field_req').hide();
            }
        });

         $("#set_temperature").hide()
         $("#set_temperature_lbl").hide()
         $('input[type=radio][name=temperature]').change(function() {
//        $("#temperature").change(function(){
            var sel = $("#temperature").val()
            if(sel == ""){
                $("#set_temperature").hide()
                $("#set_temperature_lbl").hide()
            }
            else{
                $("#set_temperature").show()
                $("#set_temperature_lbl").show()
            }
        })
})
})
