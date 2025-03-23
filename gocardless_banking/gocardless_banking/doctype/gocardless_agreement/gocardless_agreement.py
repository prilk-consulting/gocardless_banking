# Copyright (c) 2025, Prilk Consulting BV and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
import requests

class GoCardlessAgreement(Document):
	pass


@frappe.whitelist()
def create_gocardless_requisition(agreement_name, institution_id, agreement_id):
    """
    Create a gocardless requisition and save the link in the GoCardless Agreement.

    Args:
        agreement_name (str): Name of the GoCardless Agreement record.
        institution_id (str): ID of the financial institution.
        agreement_id (str): ID of the agreement associated with the requisition.

    Returns:
        dict: Details of the created requisition.
    """
    # Fetch the GoCardless Agreement record
    gocardless_agreement = frappe.get_doc("GoCardless Agreement", agreement_name)
    gocardless_settings = frappe.get_doc("GoCardless Settings", gocardless_agreement.gocardless_settings)
    access_key = gocardless_settings.get("access_key")
    redirect_url = gocardless_settings.get("redirect_url")

    if not redirect_url:
        redirect_url = f"{frappe.utils.get_url()}/api/method/gocardless_banking.api.handle_auth_redirect"

    if not access_key or not redirect_url:
        frappe.throw(frappe._("Missing access token or redirect URL in GoCardless Settings."))

    # API endpoint and headers
    api_base_url = gocardless_settings.get("api_base_url", "https://bankaccountdata.gocardless.com/api/v2")
    url = f"{api_base_url}/requisitions/"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_key}"
    }

    # Payload
    payload = {
        "redirect": redirect_url,
        "institution_id": institution_id,
        "agreement": agreement_id,
        "user_language": "EN"
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        response = response.json()
        
        # Validate response
        if response.get("status") == "CR":
            # Save requisition details in the GoCardless Agreement
            gocardless_agreement.update({
                "requisition_id": response.get("id"),
                "requisition_link": response.get("link"),
                "authentication_status": "Pending"
            })
            gocardless_agreement.save()
            return {
                "message": frappe._("Requisition created successfully."),
                "requisition_id": response.get("id"),
                "link": response.get("link"),
            }
        else:
            return {
                "message": frappe._("Failed to create requisition."),
                "details": response.get("status", {}).get("description", frappe._("Unknown error"))
            }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), frappe._("gocardless Requisition Error"))
        frappe.db.rollback()
        return {
            "message": frappe._("An error occurred while creating the requisition."),
            "error": str(e)
        }
   
@frappe.whitelist()     
def get_gocardless_agreement_accounts(gocardless_agreement_name):

	gocardless_agreement = frappe.get_doc("GoCardless Agreement", gocardless_agreement_name)
	gocardless_settings = frappe.get_doc("GoCardless Settings", gocardless_agreement.gocardless_settings)
	access_key = gocardless_settings.get("access_key")
	redirect_url = gocardless_settings.get("redirect_url")

	# Define constants
	api_url = "https://bankaccountdata.gocardless.com/api/v2/requisitions/"


	# Set up headers
	headers = {
		"accept": "application/json",
		"Authorization": f"Bearer {access_key}"
	}

	# Make the GET request
	response = requests.get(f"{api_url}{gocardless_agreement.requisition_id}/", headers=headers)

	# Check if the request was successful
	if response.status_code == 200:
		response_data = response.json()
  
    	# Process each account ID in the response
		for account_id in response_data.get("accounts", []):
			# Try to fetch existing GoCardless Account or create a new one
			gocardless_account_doc = frappe.get_doc({
				"doctype": "GoCardless Account",
				"account_id": account_id
			}) if not frappe.db.exists("GoCardless Account", {"account_id": account_id}) else frappe.get_doc("GoCardless Account", {"account_id": account_id})
			gocardless_account_doc.gocardless_agreement = gocardless_agreement.name
			# Save the document
			gocardless_account_doc.save()
			frappe.msgprint("Requisition data has been processed successfully.")

@frappe.whitelist()
def check_auth_status(gocardless_agreement_name):
    # Fetch the GoCardless Agreement document
    gocardless_agreement = frappe.get_doc("GoCardless Agreement", gocardless_agreement_name)
    gocardless_settings = frappe.get_doc("GoCardless Settings", gocardless_agreement.gocardless_settings)
    # Define the endpoint to fetch requisition status
    url = f"https://bankaccountdata.gocardless.com/api/v2/requisitions/{gocardless_agreement.requisition_id}/"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {gocardless_settings.access_key}",  # Replace with actual token field
    }

    # Make the API request to check status
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        status = data.get("status") # Default to 'Created' if status is missing

        if status == "AC":  # Example: "AC" for Authenticated
            gocardless_agreement.authentication_status = "Authenticated"
            gocardless_agreement.save()
            frappe.db.commit()
            return "Authenticated"
        elif status == "LN":
            gocardless_agreement.authentication_status = "Authenticated"
            gocardless_agreement.save()
            frappe.db.commit()
            return "Authenticated"
        elif status == "RJ":  # Example: "RJ" for Rejected
            gocardless_agreement.authentication_status = "Failed"
            gocardless_agreement.save()
            frappe.db.commit()
            return "Failed"
        else:
            return "Pending"
    else:
        frappe.throw(f"Failed to check authentication status. Error: {response.text}")
