// Copyright (c) 2025, Prilk Consulting BV and contributors
// For license information, please see license.txt

// frappe.ui.form.on("GoCardless Agreement", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('GoCardless Agreement', {
    refresh: function (frm) {
        // Add Create Requisition button
        frm.add_custom_button(__('Create Requisition'), function () {
            frappe.call({
                method: "gocardless_banking.gocardless_banking.doctype.gocardless_agreement.gocardless_agreement.create_gocardless_requisition",
                args: {
                    agreement_name: frm.doc.name,
                    institution_id: frm.doc.bank_id,
                    agreement_id: frm.doc.agreement_id
                },
                callback: function (r) {
                    if (!r.exc) {
                        // Success - Show success message
                        frappe.msgprint(__('Requisition created successfully.'));
                        frm.reload_doc();
                    } else {
                        // Error - Check the response for error details
                        if (r.message && r.message.error) {
                            // If the error message exists, show the error message
                            frappe.msgprint(__('Error: ') + r.message.error);
                        } else {
                            // Fallback error message in case the error message structure is different
                            frappe.msgprint(__('An unexpected error occurred while creating the requisition.'));
                        }
                    }
                },
                error: function (err) {
                    // Handle any unexpected errors from the frappe.call itself
                    frappe.msgprint(__('Error: ') + err.message);
                }
            });
        }, __('Actions'));
        if (frm.doc.requisition_link) {  // Ensure the link is populated
            frm.add_custom_button(__('Authenticate'), function () {
                // Open a dialog to show instructions and proceed button
                const dialog = new frappe.ui.Dialog({
                    title: __('Authenticate with gocardless'),
                    fields: [
                        {
                            fieldtype: 'HTML',
                            fieldname: 'instructions',
                            options: `
                                <p>${__('You will be redirected to gocardless for authentication. After completing the process, you will be redirected back to this system.')}</p>
                                <p>${__('Please click "Proceed" to continue.')}</p>
                            `,
                        }
                    ],
                    primary_action_label: __('Proceed'),
                    primary_action: function () {
                        // Redirect user to the gocardless authentication link
                        window.location.href = frm.doc.requisition_link;
                        dialog.hide();
                    }
                });
                dialog.show();
            }, __('Actions'));
        }
    }
});

frappe.ui.form.on('GoCardless Agreement', {
    refresh: function (frm) {
        // Add Get accounts button if requisition_link is available
        if (frm.doc.requisition_link) {
            frm.add_custom_button(__('Get Accounts'), function () {
                frappe.call({
                    method: "gocardless_banking.gocardless_banking.doctype.gocardless_agreement.gocardless_agreement.get_gocardless_agreement_accounts",
                    args: {
                        gocardless_agreement_name: frm.doc.name,
                    },
                    callback: function (r) {
                        if (!r.exc) {
                            // Success - Show success message
                            frappe.msgprint(__('Account retrived successfully.'));
                            frm.reload_doc();
                        } else {
                            // Error - Check the response for error details
                            if (r.message && r.message.error) {
                                // If the error message exists, show the error message
                                frappe.msgprint(__('Error: ') + r.message.error);
                            } else {
                                // Fallback error message in case the error message structure is different
                                frappe.msgprint(__('An unexpected error occurred while creating the requisition.'));
                            }
                        }
                    },
                    error: function (err) {
                        // Handle any unexpected errors from the frappe.call itself
                        frappe.msgprint(__('Error: ') + err.message);
                    }
                });
            }, __('Actions'));
        }
    }
});