odoo.define('freight_management.website_request', function (require) {
'use strict';
require('web.dom_ready');
$(document).ready(function (){
        $("#freight_hs_code_ids").select2();
       $('#ocean_div').hide();
        $('#land_div').hide();
//        $('#air_div').hide();
        $('#dng_info').hide();
        $("#trac_no").hide();
        $("#trac_no_lb").hide();
        $("#air_lbl1").hide();
        $("#air_lbl2").hide();
        $("#ocean_lbl1").hide();
        $("#ocean_lbl2").hide();

        $("#equipment_type_lbl").hide();
	            $("#shipping_line_id").hide();
	            $("#vessel_id").hide();
	            $("#voyage_no").hide();
	            $("#trucker_number").hide();
	            $("#truck_ref").hide();
	            $("#trucker").hide();
	            $("#incoterm").hide();
	            $("#mawb").hide();
	            $("#flight_no").hide();
	            $("#airline").hide();
	            $("#equipment_type").hide();
	            $("#shp_line_lbl").hide();
	            $("#vessel_lbl").hide();
	            $("#voyage_lbl").hide();
	            $("#trucker_no_lbl").hide();
	            $("#cmr_lbl").hide();
	            $("#trucker_lbl").hide();
	            $("#incoterm_lbl").hide();
	            $("#mawb_lbl").hide();
	            $("#flight_no_lbl").hide();
	            $("#airline_lbl").hide();
	            $("#incoterm1").hide();

	            /*$('.vehicle_size').hide();
                $('.vehicle_type').hide();*/

    $('input[type=radio][name=mode_of_transport]').change(function() {
            console.log('llllllllllllllllllll')
            if (this.value == 'air') {
                console.log("AIR");
                $('#ocean_div').hide();
	            $('#land_div').hide();
//	            $('#air_div').show();



	            $('#air_lbl_1').show()
	            $('#air_data_1').show()
	            $('#air_lbl_2').show()
	            $('#air_data_2').show()

	            $('#ocean_lbl_1').hide()
	            $('#ocean_data_1').hide()
	            $('#ocean_lbl_2').hide()
	            $('#ocean_data_2').hide()

	            $('#land_lbl_1').hide()
	            $('#land_data_1').hide()
	            $('#land_lbl_2').hide()
	            $('#land_data_2').hide()

	            $("#equipment_type_lbl").hide();
	            $("#equipment_type").hide();
	            $("#shipping_line_id").hide();
	            $("#shp_line_lbl").hide();
	            $("#vessel_id").hide();
	            $("#vessel_lbl").hide();

	            $("#voyage_no").hide();
	            $("#voyage_lbl").hide();
	            $("#trucker_number").hide();
	            $("#trucker_no_lbl").hide();
	            $("#truck_ref").hide();
	            $("#cmr_lbl").hide();
	            $("#trucker").hide();
	            $("#trucker_lbl").hide();
	            $("#incoterm").show();
	            $("#incoterm1").show();
	            $("#incoterm")[0].required = true;
	            $("#equipment_type")[0].required = false;

	            $("#vehicle_size")[0].required = false;
	            $("#vehicle_type")[0].required = false;


	            $("#incoterm_lbl").show();

	            $("#mawb").show();
	            $("#mawb_lbl").show();
	            $("#flight_no").show();
	            $("#flight_no_lbl").show();
	            $("#airline").show();
	            $("#airline_lbl").show();
	            $("#trac_no").hide();
                $("#trac_no_lb").hide();


                   $("#air_lbl1").show();
                $("#air_lbl2").show();
                $("#ocean_lbl1").hide();
                $("#ocean_lbl2").hide();
                /*$('.vehicle_size').hide();
                $('.vehicle_type').hide();*/
            }
            else if (this.value == 'ocean') {
                console.log("OCEAN");
                $('#ocean_div').show();
	            $('#land_div').hide();
//	            $('#air_div').hide();

	            $("#vehicle_size")[0].required = false;
	            $("#vehicle_type")[0].required = false;

	            $('#air_lbl_1').hide()
	            $('#air_data_1').hide()
	            $('#air_lbl_2').hide()
	            $('#air_data_2').hide()

	            $('#ocean_lbl_1').show()
	            $('#ocean_data_1').show()
	            $('#ocean_lbl_2').show()
	            $('#ocean_data_2').show()

                $('#land_lbl_1').hide()
	            $('#land_data_1').hide()
	            $('#land_lbl_2').hide()
	            $('#land_data_2').hide()

                $("#equipment_type_lbl").show();
                $("#equipment_type").show();
                $("#incoterm").show();
                $("#incoterm1").show();
//                $("#incoterm").after("<br/>");
                $("#incoterm_lbl").show();
                $("#vessel_id").show();
                $("#vessel_lbl").show();
                $("#voyage_no").show();
                $("#voyage_lbl").show();
                $("#shipping_line_id").show();
                $("#shp_line_lbl").show();
                $("#mawb").hide();
                $("#mawb_lbl").hide();
                $("#flight_no").hide();
                $("#flight_no_lbl").hide();
                $("#truck_ref").hide();
                $("#cmr_lbl").hide();
                $("#trucker").hide();
                $("#trucker_lbl").hide();
                $("#trac_no").hide();
                $("#trac_no_lb").hide();
               /* $('.vehicle_size').hide();
                $('.vehicle_type').hide();*/

                $("#trucker_no_lbl").hide();
                $("#airline").hide();
                $("#airline_lbl").hide();
                $("#air_lbl1").hide();
                $("#air_lbl2").hide();
                $("#ocean_lbl1").show();
                $("#ocean_lbl2").show();
                $("#incoterm")[0].required = true;
                $("#equipment_type")[0].required = true;
            }
            else if (this.value == 'land') {
                console.log("LAND");
                $('#ocean_div').hide();
                /*$('.vehicle_size').show();
                $('.vehicle_type').show();*/

//                $('#air_div').hide();
	            $('#land_div').show();

                $("#vehicle_size")[0].required = true;
	            $("#vehicle_type")[0].required = true;


	            $('#air_lbl_1').hide()
	            $('#air_data_1').hide()
	            $('#air_lbl_2').hide()
	            $('#air_data_2').hide()

	            $('#ocean_lbl_1').hide()
	            $('#ocean_data_1').hide()
	            $('#ocean_lbl_2').hide()
	            $('#ocean_data_2').hide()

	            $('#land_lbl_1').show()
	            $('#land_data_1').show()
	            $('#land_lbl_2').show()
	            $('#land_data_2').show()

                $("#equipment_type_lbl").hide();
                $("#equipment_type").hide();
                $("#shipping_line_id").hide();
                $("#shp_line_lbl").hide();
                $("#voyage_no").hide();
                $("#voyage_lbl").hide();
                $("#vessel_id").hide();
                $("#vessel_lbl").hide();
                $("#incoterm").hide();
                $("#incoterm1").hide();
//                $("#incoterm").next("br").remove();
                $("#incoterm_lbl").hide();
                $("#mawb").hide();
                $("#mawb_lbl").hide();
                $("#flight_no").hide();
                $("#flight_no_lbl").hide();
                $("#truck_ref").show();
                $("#cmr_lbl").show();
                $("#trucker").show();
                $("#trucker_lbl").show();
                $("#trucker_number").show();
                $("#trac_no").show();
                $("#trac_no_lb").show();
                $("#trucker_no_lbl").show();
                $("#airline").hide();
                $("#airline_lbl").hide();
                $("#incoterm")[0].required = false;
                $("#equipment_type")[0].required = false;
                $("#air_lbl1").hide();
                $("#air_lbl2").hide();
                $("#ocean_lbl1").hide();
                $("#ocean_lbl2").hide();
            }
        });
         $("#set_temperature").hide()
         $("#set_temperature_lbl").hide()
        $("#temperature").change(function(){
            var sel = $("#temperature").val()
            if(sel == ""){
                $("#set_temperature").hide()
                $("#set_temperature").next("br").remove();
                $("#set_temperature").next("br").remove();
                $("#set_temperature_lbl").hide()
                $("#set_temperature_lbl").next("br").remove();
                $("#set_temperature_lbl").next("br").remove();
            }
            else{
                $("#set_temperature").show()
                $("#set_temperature_lbl").show()
                $("#set_temperature").after("<br/><br/>")
                $("#set_temperature_lbl").after("<br/><br/>")
            }
        })

//        $('input[type=checkbox][name=danger]').change(function() {
//            var a = $('#danger').is(":checked");
//            if ($('#danger').is(":checked")){
//                $('#danger_info').show();
//                $('#danger_class').show();
//                $('#danger_class_info').show();
//                $('#dangerous_goods_class_field').show();
//                $('#dangerous_goods_class_lbl').show();
//                $('#dng_info').show();
//                $("#dg_bool").after("<br />");
//                $("#dng_info").after("<br />");
//                $("#danger").after("<br />");
//                $("#danger_class_info").after("<br />");
//            }
//            else{
//                $('#danger_info').hide();
//                $('#danger_class').hide();
//                $('#danger_class_info').hide();
//                $('#dng_info').hide();
//                $('#dangerous_goods_class_lbl').hide();
//                $('#dangerous_goods_class_field').hide();
//                $("#dng_info").next("br").remove();
//                $("#dg_bool").next("br").remove();
//                $("#danger").next("br").remove();
//                $("#danger_class_info").next("br").remove();
//            }
//        });
})
})
