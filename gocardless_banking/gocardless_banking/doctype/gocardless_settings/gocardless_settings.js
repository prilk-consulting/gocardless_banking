// Copyright (c) 2025, Prilk Consulting BV and contributors
// For license information, please see license.txt

// frappe.ui.form.on("GoCardless Settings", {
// 	refresh(frm) {

// 	},
// });






frappe.ui.form.on('GoCardless Settings', {
    // enabled: function (frm) {
    //     frm.toggle_reqd('secret_id', frm.doc.enabled);
    //     frm.toggle_reqd('secret_key', frm.doc.enabled);
    // },
    
    refresh: function(frm) {
        frm.add_custom_button(__('Add Bank Account'), function() {
            get_gocardless_banks(frm);
        });
        // Add a button to generate keys if access_key is not available
        // if (!frm.doc.access_key) {
            frm.add_custom_button(__('Generate Keys'), function() {
                generate_gocardless_keys(frm);
            });
        // }
        // Add a button to refresh keys if access_key is available
        if (frm.doc.access_key) {
            frm.add_custom_button(__('Refresh Keys'), function() {
                refresh_gocardless_keys(frm);
            });
        }
    },
});

function get_gocardless_banks(frm) {
    frappe.call({
        method: 'gocardless_banking.gocardless_banking.doctype.gocardless_settings.gocardless_settings.get_gocardless_banks',
        args: {
            gocardless_settings: frm.doc.name
        },
        callback: function(r) {
            if (!r.exc && r.message) {
                let banks = r.message[0]; // List of banks
                let company_names = r.message[1]; // List of company names

                let bank_names = banks.map(bank => ({
                    label: `${bank.name} (${bank.bic || 'N/A'})`, // Display name and BIC
                    value: bank.id // Use unique ID as the value
                })); // Create a dialog to show the list of banks
                let dialog = new frappe.ui.Dialog({
                    title: 'Select Bank',
                    fields: [
                        {
                            label: 'Company',
                            fieldname: 'company',
                            fieldtype: 'Select',
                            options: company_names
                        },
                        {
                            label: 'Banks',
                            fieldname: 'bank',
                            fieldtype: 'Select',
                            options: bank_names
                        },
                    ],
                    primary_action_label: 'Create Agreement',
                    primary_action(values) {
                        let selected_option = values.bank;
                        if (selected_option) {
                            // let bank_name = selected_option.split(' (')[0]; // Extract name from "Name (BIC)"
                            // let selected_bank = banks.find(bank => bank.name === bank_name);
                            let selected_bank = banks.find(bank => bank.id === selected_option);
                            if (selected_bank) {
                                console.log('Selected Bank:', selected_bank);
                                create_gocardless_agreement(
                                    frm,
                                    institution_id = selected_bank.id,
                                    bank_name = selected_bank.name,
                                    max_historical_days = selected_bank.max_historical_days,
                                    access_valid_for_days = selected_bank.access_valid_for_days,
                                    access_scope = ['balances', 'details', 'transactions']
                                );
                                dialog.hide();
                            }
                        } else {
                            frappe.msgprint(__('Please select a bank.'));
                        }
                    }
                });
                dialog.show();
            }
        }
    });
};

function generate_gocardless_keys(frm) {
    frappe.call({
        method: 'gocardless_banking.gocardless_banking.doctype.gocardless_settings.gocardless_settings.generate_gocardless_keys',
        args: {
            gocardless_settings_name: frm.doc.name
        },
        callback: function(r) {
            if (!r.exc) {
                frappe.msgprint({
                    title: __("Generate keys"),
                    message: __("gocardless keys have been generated.",),
                    alert: 1
                });
                frm.reload_doc();               
            }
        }
    });
};

function refresh_gocardless_keys(frm) {
    frappe.call({
        method: 'gocardless_banking.gocardless_banking.doctype.gocardless_settings.gocardless_settings.refresh_gocardless_keys',
        args: {
            gocardless_settings_name: frm.doc.name
        },
        callback: function(r) {
            if (!r.exc) {
                frappe.msgprint({
                    title: __("Generate keys"),
                    message: __("gocardless keys have been refreshed.",),
                    alert: 1
                });
                frm.reload_doc();               
            }
        }
    });
};

function create_gocardless_agreement(frm,institution_id, bank_name) {
    frappe.call({
        method: 'gocardless_banking.gocardless_banking.doctype.gocardless_settings.gocardless_settings.create_gocardless_agreement',
        args: {
            gocardless_settings_name: frm.doc.name,
            institution_id: institution_id,
            bank_name: bank_name,
            max_historical_days: max_historical_days,
            access_valid_for_days: access_valid_for_days,
            access_scope: ['balances', 'details', 'transactions'],
        },
        callback: function(r) {
            if (!r.exc) {
                frappe.msgprint(__('End User Agreement created successfully.'));
            } else {
                frappe.msgprint(__('Failed to create End User Agreement.'));
            }
        }
    });
}
