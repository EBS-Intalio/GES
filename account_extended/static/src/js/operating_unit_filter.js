odoo.define('account_extended.account_reports', function (require) {
'use strict';

var core = require('web.core');
var Context = require('web.Context');
var AbstractAction = require('web.AbstractAction');
var Dialog = require('web.Dialog');
var datepicker = require('web.datepicker');
var session = require('web.session');
var field_utils = require('web.field_utils');
var RelationalFields = require('web.relational_fields');
var StandaloneFieldManagerMixin = require('web.StandaloneFieldManagerMixin');
var WarningDialog = require('web.CrashManager').WarningDialog;
var Widget = require('web.Widget');

var QWeb = core.qweb;
var _t = core._t;


var accountReportsWidget = require('account_reports.account_report');
var accountReportWidget = accountReportsWidget.include({
       render_searchview_buttons: function() {
        this._super();
        var self = this;
        // chart of account filter
        this.$searchview_buttons.find('.js_operating_unit').select2();
        if (self.report_options.operating_unit) {
            self.$searchview_buttons.find('[data-filter="operating_unit"]').select2("val",
             self.report_options.operating_unit);
        }
         this.$searchview_buttons.find('.js_operating_unit').on('change',function(){
            self.report_options.operating_unit = self.$searchview_buttons.find('[data-filter="operating_unit"]').val();
            return self.reload().then(function(){
                self.$searchview_buttons.find('.operating_unit_filter').click();
            })
        });
//        if(this.controlPanelProps && this.controlPanelProps.action && ['Profit and Loss','Balance Sheet','Cash Flow Statement'].includes(this.controlPanelProps.action.display_name))
//        {
//        console.log('hello',this.$searchview_buttons.find('.btn-o_account_reports_filter_operating_unit'))
//           this.$searchview_buttons.find('.btn-o_account_reports_filter_operating_unit').hide();
//        }

    }

  });


});
