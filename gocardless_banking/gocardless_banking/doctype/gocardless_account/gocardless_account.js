// Copyright (c) 2025, Prilk Consulting BV and contributors
// For license information, please see license.txt

// frappe.ui.form.on("GoCardless Account", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('GoCardless Account', {
    refresh: function (frm) {
        frm.add_custom_button(__('Fetch Transactions'), function () {
            frappe.call({
                method: "gocardless_banking.gocardless_banking.doctype.gocardless_account.gocardless_account.fetch_transactions",
                args: {
                    gocardless_account_name: frm.doc.name,
                },
                callback: function(response) {
                    if (response.message) {
                        frappe.msgprint(response.message);
                        frm.reload_doc();
                    }
                }
            });
        });
    }
});


