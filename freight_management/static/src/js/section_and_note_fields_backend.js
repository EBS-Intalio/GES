
odoo.define('freight_management.section_and_note_backend', function (require) {
"use strict";

var BasicFields = require('web.basic_fields');
var SectionAndNoteListBackend = require('account.section_and_note_backend');

SectionAndNoteListBackend.include({
    _renderBodyCell: function (record, node, index, options) {
        var $cell = this._super.apply(this, arguments);

        var isSection = record.data.display_type === 'line_section';

        if (isSection && this.arch.attrs['section-subtotal-data-field']) {
            var sectionSubtotalDataFields = this.arch.attrs['section-subtotal-data-field'].split(',');
            if (node.attrs.name === "name") {
                var nbrColumns = this._getNumberOfCols();
                if (this.handleField) {
                    nbrColumns--;
                }
                if (this.addTrashIcon) {
                    nbrColumns--;
                }
                nbrColumns -= sectionSubtotalDataFields.length;
                $cell.attr('colspan', nbrColumns);
            } else if (sectionSubtotalDataFields.indexOf(node.attrs.name) >= 0) {
                $cell.removeClass('o_hidden');
                return $cell;
            }
        }

        return $cell;
    },
});

BasicFields.NumericField.include({
    init: function () {
        this._super.apply(this, arguments);
        this._setSectionSubtotal();
    },

    _reset: function () {
        this._super.apply(this, arguments);
        this._setSectionSubtotal();
    },

    _setSectionSubtotal: function () {
        if (this.record.data['display_type'] === 'line_section') {
            var sequence = this.record.data.sequence;
            var id = this.record.data.id;
            if (this['__parentedParent'] && this.__parentedParent['state'] && this.__parentedParent.state['data']) {
                var all_rows = this.__parentedParent.state.data;
                var subtotal = 0.0;
                var self_found = false;
                for (var i = 0; i < all_rows.length; i++) {
                    var row = all_rows[i].data;
                    if (row.id == id) {
                        self_found = true;
                        continue;
                    }
                    if (self_found && row.sequence >= sequence) {
                        if (row.display_type === 'line_section' && row.id != id) {
                            break;
                        }
                        subtotal += row[this.name];
                    }
                }
                this.value = subtotal;
            }
        }
    },
});

});
