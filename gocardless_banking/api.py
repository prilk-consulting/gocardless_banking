import frappe
from frappe.model.document import Document
import frappe.utils
import requests

from gocardless_banking.gocardless_banking.doctype.gocardless_agreement.gocardless_agreement import check_auth_status
@frappe.whitelist(allow_guest=True)
def handle_auth_redirect():
    """
    Handle gocardless's redirect after authentication and update the status.
    Sample     # Fetch the agreement using requisition_id
    gocardless_agreement = frappe.get_all(
        "GoCardless Agreement",
        filters={"requisition_id": requisition_id},
        fields=["name", "owner"]
    )
    Sample error : How to handle this?
    //http://127.0.0.1:8000/?ref=846eee4b-ccb3-49cd-b581-be26f72d808a&error=ConsentLinkReused&details=This+link+has+already+been+used+for+authorization+and+is+no+longer+valid.
    """
    requisition_id = frappe.form_dict.get("ref")
    error = frappe.form_dict.get("error")
    error_details = frappe.form_dict.get("details")
    # Fetch the agreement using requisition_id
    gocardless_agreement = frappe.get_all(
        "GoCardless Agreement",
        filters={"requisition_id": requisition_id},
        fields=["name", "owner"]
    )
    if not gocardless_agreement:
        frappe.throw(frappe._("No agreement found for the provided requisition ID."))
    if gocardless_agreement:
        gocardless_agreement_name = gocardless_agreement[0]["name"]
    # Handle errors in the callback
    if error:
        frappe.log_error(
            f"Error in gocardless callback: {error} - {error_details}",
            "gocardless Authorization Error"
        )
        frappe.throw(frappe._(f"Authorization failed: {error} - {error_details}"))
        # return frappe.redirect(f"/error-page?error={error}&details={error_details}")

    elif not requisition_id:
        frappe.throw(frappe._("Missing requisition id in callback URL."))
    else:
        result = check_auth_status(gocardless_agreement_name)
        if "Error" in result:
            frappe.throw(result)
            return result
        else:
            # Define the custom URL to redirect the user after authentication success
            custom_redirect_url = f"{frappe.utils.get_url()}/app/gocardless-agreement/{gocardless_agreement_name}"
            # Redirect to the custom URL after authentication success
            frappe.local.response["type"] = "redirect"
            frappe.local.response["location"] = custom_redirect_url
            return
        