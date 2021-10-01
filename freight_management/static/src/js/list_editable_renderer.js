
odoo.define('freight_management.list_editable_renderer', function (require) {
"use strict";

var ListRenderer = require('web.ListRenderer');

ListRenderer.include({
    _onRemoveIconClick: function (event) {
        event.stopPropagation();
        var result = confirm("Are you sure you want to delete this record?");
        if (result){
            var id = $(event.target).closest('tr').data('id');
            this.trigger_up('list_record_remove', {id: id});
        }
    }

});
});
