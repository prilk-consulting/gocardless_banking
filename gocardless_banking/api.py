import frappe
from frappe.model.document import Document
import frappe.utils
import requests

from gocardless_banking.gocardless_banking.doctype.gocardless_banking_agreement.gocardless_banking_agreement import check_auth_status, get_gocardless_banking_agreement_accounts
from gocardless_banking.gocardless_banking.doctype.gocardless_banking_account.gocardless_banking_account import fetch_account_details

@frappe.whitelist(allow_guest=True)
def handle_auth_redirect():
    """
    Handle gocardless's redirect after authentication and update the status.
    """
    requisition_id = frappe.form_dict.get("ref")
    error = frappe.form_dict.get("error")
    error_details = frappe.form_dict.get("details")
    source = frappe.form_dict.get("source")  # Get the source parameter

    # Fetch the agreement using requisition_id
    gocardless_banking_agreement = frappe.get_all(
        "GoCardless Banking Agreement",
        filters={"requisition_id": requisition_id},
        fields=["name", "owner"]
    )
    if not gocardless_banking_agreement:
        frappe.throw(frappe._("No agreement found for the provided requisition ID."))
    if gocardless_banking_agreement:
        gocardless_banking_agreement_name = gocardless_banking_agreement[0]["name"]

    # Handle errors in the callback
    if error:
        frappe.log_error(
            f"Error in gocardless callback: {error} - {error_details}",
            "gocardless Authorization Error"
        )
        frappe.throw(frappe._(f"Authorization failed: {error} - {error_details}"))

    elif not requisition_id:
        frappe.throw(frappe._("Missing requisition id in callback URL."))
    else:
        result = check_auth_status(gocardless_banking_agreement_name)
        if "Error" in result:
            frappe.throw(result)
            return result
        else:
            # If source is settings, fetch bank accounts first
            if source == "settings":
                try:
                    # Wait for auth status to be confirmed
                    frappe.db.commit()
                    # First get the bank accounts
                    get_gocardless_banking_agreement_accounts(gocardless_banking_agreement_name)                   
                    # Get all linked accounts for this agreement
                    linked_accounts = frappe.get_all(
                        "GoCardless Banking Account",
                        filters={"gocardless_banking_agreement": gocardless_banking_agreement_name},
                        fields=["name"]
                    )
                    # Fetch details for each account
                    for account in linked_accounts:
                        fetch_account_details(account.name)
                        frappe.db.commit()
                        
                except Exception as e:
                    frappe.log_error(f"Error fetching bank accounts: {str(e)}", "GoCardless Bank Account Fetch Error")
                filters = {
                    "gocardless_banking_agreement": ["=", gocardless_banking_agreement_name]
                }
                encoded_filters = frappe.utils.json.dumps(filters)
                custom_redirect_url = f"{frappe.utils.get_url()}/app/gocardless-banking-account/view/list?filters={encoded_filters}"
            else:
                custom_redirect_url = f"{frappe.utils.get_url()}/app/gocardless-banking-agreement/{gocardless_banking_agreement_name}"
            
            # Redirect to the custom URL after authentication success
            frappe.local.response["type"] = "redirect"
            frappe.local.response["location"] = custom_redirect_url
            return
        