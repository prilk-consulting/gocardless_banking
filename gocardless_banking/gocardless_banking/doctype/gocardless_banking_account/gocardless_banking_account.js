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

        // Add Remove Duplicates button if bank account is linked
        if (frm.doc.bank_account) {
            frm.add_custom_button(__('Remove Duplicates'), function() {
                frappe.confirm(
                    __('This will remove duplicate Bank Transactions (excluding reconciled ones). Continue?'),
                    function() {
                        frappe.call({
                            method: 'gocardless_banking.gocardless_banking.doctype.gocardless_banking_account.gocardless_banking_account.remove_duplicate_transactions',
                            args: {
                                gocardless_banking_account_name: frm.doc.name
                            },
                            freeze: true,
                            freeze_message: __('Removing duplicate transactions...'),
                            callback: function(r) {
                                if (r.message) {
                                    frappe.msgprint({
                                        title: __('Duplicates Removed'),
                                        message: __('Processed: {0}<br>Updated: {1}<br>Deleted: {2}',
                                            [r.message.total_processed, r.message.updated, r.message.deleted]),
                                        indicator: 'green'
                                    });
                                }
                            }
                        });
                    }
                );
            }, __('Actions'));
        }
    }
});


