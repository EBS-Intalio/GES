odoo.define('account_extended.action_create_statement_hide_show', function (require) {
"use strict";

    const ActionMenus = require('web.ActionMenus');
    const session = require('web.session');
    const { patch } = require('web.utils');



    patch(ActionMenus, 'account_extended.action_create_statement_hide_show', {
        mounted(){
                if (this.props['context'] != null && !this.props['context'].show_action_bank_statement)

                {

                for (var i = 0; i < this.actionItems.length; i++) {
                    if (this.actionItems[i]['action'] != null && this.actionItems[i]['action']['xml_id'] != null && this.actionItems[i]['action']['xml_id'] == 'account_extended.create_statements')
                    {
                        this.actionItems.splice(i, 1,);
                    }
                }
            }
        },
//         async willStart() {
//            this.actionItems = await this._setActionItems(this.props);
//            console.log("===",this.props['context'])
//
//
//            this.printItems = await this._setPrintItems(this.props);
//        }
    });

});