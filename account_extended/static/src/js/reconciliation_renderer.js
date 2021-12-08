odoo.define('account_extended.ReconciliationRenderer', function (require) {
"use strict";


var reconcile = require('account.ReconciliationRenderer')
reconcile.LineRenderer.include({
events: {
        'click .accounting_view caption .o_buttons button': '_onValidate',
        'click .accounting_view tfoot': '_onChangeTab',
        'click': '_onTogglePanel',
        'click .o_field_widget': '_onStopPropagation',
        'keydown .o_input, .edit_amount_input': '_onStopPropagation',
        'click .o_notebook li a': '_onChangeTab',
        'click .cell': '_onEditAmount',
        'change input.filter': '_onFilterChange',
        'change select.filter_head': '_onFilterChangeHead',
        'change select.filter_head_asc_desc': '_onFilterChangeHead_asc_desc',
        'click .match .load-more a': '_onLoadMore',
        'click .match .mv_line td': '_onSelectMoveLine',
        'click .accounting_view tbody .mv_line td': '_onSelectProposition',
        'click .o_reconcile_models button': '_onQuickCreateProposition',
        'click .create .add_line': '_onCreateProposition',
        'click .reconcile_model_create': '_onCreateReconcileModel',
        'click .reconcile_model_edit': '_onEditReconcileModel',
        'keyup input': '_onInputKeyup',
        'blur input': '_onInputKeyup',
        'keydown': '_onKeydown',
    },
     _onFilterChangeHead_asc_desc: function (event) {
        this.model.context.filter_head_asc_desc = event.target.value
        console.log('this.context',event.target.value)
        this.trigger_up('change_filter', {'data': ''});
    },
    _onFilterChangeHead: function (event) {
        this.model.context.filter_head = event.target.value
        console.log('this.context',event.target.value)
        this.trigger_up('change_filter', {'data': ''});
    },

})
})