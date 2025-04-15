// Copyright (c) 2025, Prilk Consulting BV and contributors
// For license information, please see license.txt

// frappe.ui.form.on("GoCardless Banking Account", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('GoCardless Banking Account', {
    refresh: function (frm) {
        frm.add_custom_button(__('Fetch Transactions'), function () {
            frappe.call({
                method: "gocardless_banking.gocardless_banking.doctype.gocardless_banking_account.gocardless_banking_account.fetch_transactions",
                args: {
                    gocardless_banking_account_name: frm.doc.name,
                },
                callback: function(response) {
                    if (response.message) {
                        frappe.msgprint(response.message);
                        frm.reload_doc();
                    }
                }
            });
        });

        // Add Fetch Account Details button
        frm.add_custom_button(__('Fetch Account Details'), function() {
            frappe.call({
                method: 'gocardless_banking.gocardless_banking.doctype.gocardless_banking_account.gocardless_banking_account.fetch_account_details',
                args: {
                    gocardless_banking_account_name: frm.doc.name
                },
                freeze: true,
                freeze_message: __('Fetching Account Details...'),
                callback: function(r) {
                    if (!r.exc) {
                        frm.reload_doc();
                    }
                }
            });
        });
    }
});


