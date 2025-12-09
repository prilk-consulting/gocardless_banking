# Copyright (c) 2025, Prilk Consulting BV and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests
class GoCardlessBankingAgreement(Document):
	pass

@frappe.whitelist()
def create_gocardless_requisition(agreement_name, institution_id, agreement_id):
    """
    Create a gocardless requisition and save the link in the GoCardless Banking Agreement.
    If the agreement already has a requisition, reuse it instead of creating a new one.
    """
    try:
        # Fetch the GoCardless Banking Agreement record
        gocardless_banking_agreement = frappe.get_doc("GoCardless Banking Agreement", agreement_name)
        gocardless_banking_settings = frappe.get_doc("GoCardless Banking Settings", gocardless_banking_agreement.gocardless_banking_settings)
        access_key = gocardless_banking_settings.get("access_key")
        redirect_url = gocardless_banking_settings.get("redirect_url")

        if not redirect_url:
            redirect_url = f"{frappe.utils.get_url()}/api/method/gocardless_banking.api.handle_auth_redirect"

        # Add source parameter to redirect URL
        redirect_url = f"{redirect_url}?source=settings"

        if not access_key or not redirect_url:
            frappe.throw(frappe._("Missing access token or redirect URL in GoCardless Banking Settings."))

        # API endpoint and headers
        api_base_url = gocardless_banking_settings.get("api_base_url", "https://bankaccountdata.gocardless.com/api/v2")
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
        
        # Try to create requisition
        url = f"{api_base_url}/requisitions/"
        response = requests.post(url, headers=headers, json=payload)
        
        # Check if agreement is already associated
        if response.status_code == 400:
            try:
                error_detail = response.json()
                
                # GoCardless returns errors nested under field names
                # Look for "already associated" in any part of the error response
                error_str = str(error_detail).lower()
                
                # Extract the actual error message
                error_message = ""
                if isinstance(error_detail, dict):
                    # Try nested structure: error_detail["agreement"]["detail"]
                    if "agreement" in error_detail and isinstance(error_detail["agreement"], dict):
                        error_message = error_detail["agreement"].get("detail", "")
                    # Try flat structure: error_detail["detail"]
                    elif "detail" in error_detail:
                        error_message = error_detail.get("detail", "")
                    # Try summary
                    elif "summary" in error_detail:
                        error_message = error_detail.get("summary", "")
                
                # Check if it's the "already associated" error
                if "already associated" in error_str:
                    # Extract existing requisition ID from error message
                    import re
                    match = re.search(r'requisition ([a-f0-9\-]+)', error_str)
                    if match:
                        existing_requisition_id = match.group(1)
                        
                        # Fetch the existing requisition details
                        req_url = f"{api_base_url}/requisitions/{existing_requisition_id}/"
                        req_response = requests.get(req_url, headers=headers)
                        
                        if req_response.status_code == 200:
                            req_data = req_response.json()
                            
                            # Check requisition status
                            req_status = req_data.get("status")
                            
                            # Handle expired requisitions
                            if req_status == "EX":
                                frappe.msgprint(
                                    frappe._("The existing requisition has expired. Please create a new agreement and try again."),
                                    indicator="orange",
                                    title=frappe._("Requisition Expired")
                                )
                                frappe.throw(frappe._("Please create a new End User Agreement as the existing one has expired."))
                            
                            # Determine authentication status
                            if req_status == "LN":  # Linked
                                auth_status = "Authenticated"
                                msg = frappe._("Agreement already has an authenticated requisition. Using existing requisition.")
                                indicator = "green"
                            elif req_status == "CR":  # Created
                                auth_status = "Pending"
                                msg = frappe._("Agreement already has a pending requisition. Using existing requisition.")
                                indicator = "blue"
                            else:
                                auth_status = "Pending"
                                msg = frappe._("Using existing requisition for this agreement.")
                                indicator = "blue"
                            
                            # Update the agreement with existing requisition
                            gocardless_banking_agreement.update({
                                "requisition_id": req_data.get("id"),
                                "requisition_link": req_data.get("link"),
                                "authentication_status": auth_status
                            })
                            gocardless_banking_agreement.save()
                            frappe.db.commit()
                            
                            # Show user-friendly message (not an error)
                            frappe.msgprint(msg, indicator=indicator, title=frappe._("Requisition Reused"))
                            
                            return {
                                "message": msg,
                                "requisition_id": req_data.get("id"),
                                "link": req_data.get("link"),
                                "reused": True,
                                "status": req_status
                            }
                        else:
                            # Could not fetch existing requisition - this IS an error
                            frappe.log_error(
                                f"Could not fetch requisition {existing_requisition_id}\nStatus: {req_response.status_code}\nResponse: {req_response.text}",
                                "GoCardless Requisition Fetch Error"
                            )
                            frappe.throw(frappe._("Could not retrieve existing requisition details. Please contact support."))
                    else:
                        # Could not parse requisition ID from error message
                        frappe.log_error(
                            f"Could not parse requisition ID from error: {error_str}",
                            "GoCardless Parse Error"
                        )
                        frappe.throw(frappe._("Agreement is already associated with a requisition, but could not retrieve details."))
                else:
                    # Different 400 error - this IS an actual error
                    frappe.log_error(
                        f"Status Code: 400\nURL: {url}\nPayload: {frappe.as_json(payload, indent=2)}\nResponse: {frappe.as_json(error_detail, indent=2)}", 
                        "GoCardless API Error"
                    )
                    
                    # Extract user-friendly error message from nested structure
                    if not error_message and isinstance(error_detail, dict):
                        # Try to extract from any nested structure
                        for key, value in error_detail.items():
                            if isinstance(value, dict):
                                error_message = value.get("detail") or value.get("summary", "")
                                if error_message:
                                    break
                    
                    if not error_message:
                        error_message = "Unknown error"
                    
                    frappe.throw(frappe._("Failed to create requisition: {0}").format(error_message))
                    
            except frappe.exceptions.ValidationError:
                raise
            except Exception as parse_error:
                # Unexpected error while parsing response
                frappe.log_error(
                    f"Error parsing API response\n{frappe.get_traceback()}",
                    "GoCardless Response Parse Error"
                )
                frappe.throw(frappe._("Unexpected error while processing API response. Please check Error Log."))
        
        # For other non-success responses
        if response.status_code not in [200, 201]:
            try:
                error_detail = response.json()
            except:
                error_detail = {"text": response.text}
            
            frappe.log_error(
                f"Status Code: {response.status_code}\nURL: {url}\nPayload: {frappe.as_json(payload, indent=2)}\nResponse: {frappe.as_json(error_detail, indent=2)}", 
                "GoCardless API Error"
            )
            frappe.throw(frappe._("Failed to create requisition. Status: {0}").format(response.status_code))
        
        response_data = response.json()
        
        # Validate response - successful creation
        if response_data.get("status") == "CR":
            # Save requisition details in the GoCardless Banking Agreement
            gocardless_banking_agreement.update({
                "requisition_id": response_data.get("id"),
                "requisition_link": response_data.get("link"),
                "authentication_status": "Pending"
            })
            gocardless_banking_agreement.save()
            frappe.db.commit()
            
            frappe.msgprint(
                frappe._("Requisition created successfully. Please use the link to authenticate."),
                indicator="green",
                title=frappe._("Success")
            )
            
            return {
                "message": frappe._("Requisition created successfully."),
                "requisition_id": response_data.get("id"),
                "link": response_data.get("link"),
                "reused": False
            }
        else:
            # Unexpected status in successful response
            frappe.log_error(
                f"Unexpected requisition status: {response_data}",
                "GoCardless Requisition Status"
            )
            frappe.throw(frappe._("Unexpected requisition status: {0}").format(response_data.get("status")))

    except frappe.exceptions.ValidationError:
        # These are our intentional throws - don't log them again
        frappe.db.rollback()
        raise
    except Exception as e:
        # Truly unexpected errors
        frappe.log_error(frappe.get_traceback(), "GoCardless Requisition Error")
        frappe.db.rollback()
        frappe.throw(frappe._("An unexpected error occurred. Please check Error Log for details."))

@frappe.whitelist()     
def get_gocardless_banking_agreement_accounts(gocardless_banking_agreement_name):

	gocardless_banking_agreement = frappe.get_doc("GoCardless Banking Agreement", gocardless_banking_agreement_name)
	gocardless_banking_settings = frappe.get_doc("GoCardless Banking Settings", gocardless_banking_agreement.gocardless_banking_settings)
	access_key = gocardless_banking_settings.get("access_key")
	redirect_url = gocardless_banking_settings.get("redirect_url")

	# Define constants
	api_url = "https://bankaccountdata.gocardless.com/api/v2/requisitions/"


	# Set up headers
	headers = {
		"accept": "application/json",
		"Authorization": f"Bearer {access_key}"
	}

	# Make the GET request
	response = requests.get(f"{api_url}{gocardless_banking_agreement.requisition_id}/", headers=headers)

	# Check if the request was successful
	if response.status_code == 200:
		response_data = response.json()
  
    	# Process each account ID in the response
		for account_id in response_data.get("accounts", []):
			# Try to fetch existing GoCardless Banking Account or create a new one
			gocardless_banking_account_doc = frappe.get_doc({
				"doctype": "GoCardless Banking Account",
				"account_id": account_id
			}) if not frappe.db.exists("GoCardless Banking Account", {"account_id": account_id}) else frappe.get_doc("GoCardless Banking Account", {"account_id": account_id})
			gocardless_banking_account_doc.gocardless_banking_agreement = gocardless_banking_agreement.name
			# Save the document
			gocardless_banking_account_doc.save()
			frappe.msgprint("Requisition data has been processed successfully.")

@frappe.whitelist()
def check_auth_status(gocardless_banking_agreement_name):
    # Fetch the GoCardless Banking Agreement document
    gocardless_banking_agreement = frappe.get_doc("GoCardless Banking Agreement", gocardless_banking_agreement_name)
    gocardless_banking_settings = frappe.get_doc("GoCardless Banking Settings", gocardless_banking_agreement.gocardless_banking_settings)
    # Define the endpoint to fetch requisition status
    url = f"https://bankaccountdata.gocardless.com/api/v2/requisitions/{gocardless_banking_agreement.requisition_id}/"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {gocardless_banking_settings.access_key}",  # Replace with actual token field
    }

    # Make the API request to check status
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        status = data.get("status") # Default to 'Created' if status is missing

        if status == "AC":  # Example: "AC" for Authenticated
            gocardless_banking_agreement.authentication_status = "Authenticated"
            gocardless_banking_agreement.save()
            frappe.db.commit()
            return "Authenticated"
        elif status == "LN":
            gocardless_banking_agreement.authentication_status = "Authenticated"
            gocardless_banking_agreement.save()
            frappe.db.commit()
            return "Authenticated"
        elif status == "RJ":  # Example: "RJ" for Rejected
            gocardless_banking_agreement.authentication_status = "Failed"
            gocardless_banking_agreement.save()
            frappe.db.commit()
            return "Failed"
        else:
            return "Pending"
    else:
        frappe.throw(f"Failed to check authentication status. Error: {response.text}")
