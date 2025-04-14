# Copyright (c) 2025, Prilk Consulting BV and contributors
# For license information, please see license.txt

# import frappe

import frappe
from frappe.model.document import Document
import frappe.utils
from frappe.utils import add_days, get_datetime
from frappe import _
import requests
import json
from frappe.utils import getdate, add_days
class GoCardlessBankingSettings(Document):
	pass

@frappe.whitelist()
def generate_gocardless_keys(gocardless_banking_settings_name):
    gocardless_banking_settings = frappe.get_doc("GoCardless Banking Settings",gocardless_banking_settings_name)
    secret_id = gocardless_banking_settings.secret_id
    secret_key = gocardless_banking_settings.secret_key
    headers = { 'accept': 'application/json'}
    data = { "secret_id": secret_id,"secret_key": secret_key}
    api_url = "https://bankaccountdata.gocardless.com/api/v2/token/new/"
    response = requests.post(api_url, headers=headers, data=data)
    result = response.json()
    access_key = result.get("access")
    refresh_key = result.get("refresh")
    access_expires = result.get('access_expires')
    refresh_expires = result.get('refresh_expires')
    if access_expires is None:
        frappe.throw(_("Access expiry time is missing from gocardless response."))
    if refresh_expires is None:
        frappe.throw(_("Refresh expiry time is missing from gocardless response."))
    # Calculate expiry datetime
    access_expiry_date = frappe.utils.add_days(frappe.utils.get_datetime(), access_expires // 86400)  # converting seconds to days
    refresh_expiry_date = frappe.utils.add_days(frappe.utils.get_datetime(), refresh_expires // 86400)  # converting seconds to days

    gocardless_banking_settings.access_key = access_key
    gocardless_banking_settings.refresh_key = refresh_key
    gocardless_banking_settings.access_expiry = access_expiry_date,
    gocardless_banking_settings.refresh_expiry = refresh_expiry_date
    gocardless_banking_settings.save()


@frappe.whitelist()
def get_gocardless_banks(gocardless_banking_settings):
    # Fetch GoCardless Settings document
    gocardless_banking_settings = frappe.get_doc("GoCardless Banking Settings", gocardless_banking_settings)
    # Get list of company names
    company_names= frappe.db.get_list('Company', pluck='company_name')
    # Set headers for API request
    headers = {
        'accept': 'application/json',
        'Authorization':"Bearer {}".format(gocardless_banking_settings.access_key) 
        }
    # Set parameters for API request
    params = {
        # 'country': gocardless_banking_settings.country
        }
    # Define API URL for fetching institutions
    api_url = "https://bankaccountdata.gocardless.com/api/v2/institutions/"
    # Make the API request
    response = requests.get(api_url, headers=headers, params=params, verify=False)
    
    # Check response status
    if response.status_code == 401:
        frappe.throw(_("Unauthorized: Please check your gocardless Access Key."))

    elif response.status_code != 200:
        frappe.throw(
            _("Failed to fetch institutions. Status Code: {0}, Response: {1}").format(
                response.status_code, response.text
            )
        )
    else :
        # Parse JSON response
        result = response.json()
        # Prepare additional parameters for each bank
        banks_info = []
        for bank in result:
            bank_info = {
                "id": bank["id"],
                "name": bank["name"],
                "logo": bank["logo"],
                "bic" : bank["bic"],
                "max_historical_days": bank["transaction_total_days"],
                "access_valid_for_days": bank["max_access_valid_for_days"],
                "access_scope": ["balances", "details", "transactions"]
            }
            banks_info.append(bank_info)
        
        # Return banks with additional parameters and company names
        return banks_info, company_names

@frappe.whitelist()
def create_gocardless_banking_agreement(gocardless_banking_settings_name,institution_id,bank_name, max_historical_days, access_valid_for_days, access_scope):
    gocardless_banking_settings = frappe.get_doc("GoCardless Banking Settings",gocardless_banking_settings_name)

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {gocardless_banking_settings.access_key}"
    }
    data = {
        "institution_id": institution_id,
        "max_historical_days": max_historical_days,
        "access_valid_for_days": access_valid_for_days,
        "access_scope": ['balances', 'details', 'transactions']
    }
    
    api_url = "https://bankaccountdata.gocardless.com/api/v2/agreements/enduser/"
    
    response = requests.post(api_url, headers=headers, json=data)
    
    if response.status_code == 201:
        # Parse the response to get the agreement data
        agreement_data = response.json()  
        update_gocardless_banking_agreement(
            gocardless_banking_settings = gocardless_banking_settings,
            bank_name = bank_name,
            agreement_data=agreement_data
        )
        # Return a success message
        return {"message": "Agreement successfully created."}
    else:
        frappe.throw(f"Failed to create agreement. Status Code: {response.status_code}, Response: {response.text}")

def update_gocardless_banking_agreement(gocardless_banking_settings, bank_name, agreement_data):
    # Fetch the parent document (GoCardless Settings)
    # gocardless_banking_settings = frappe.get_doc("GoCardless Settings", gocardless_banking_settings)

    agreement_exist = frappe.db.get_value(
        "GoCardless Banking Agreement",
        {"bank_id": agreement_data.get("institution_id")},
        "name"
    )
    
    # Parse datetime values, remove timezone and microseconds
    created_on = get_datetime(agreement_data.get("created")).replace(tzinfo=None, microsecond=0)
    accepted_on = get_datetime(agreement_data.get("accepted")).replace(tzinfo=None, microsecond=0)
    access_expires_on = add_days(
        get_datetime(agreement_data.get("created")), 
        int(agreement_data.get("access_valid_for_days"))
    ).replace(tzinfo=None, microsecond=0)
    
    if agreement_exist:
        agreement_doc = frappe.get_doc("GoCardless Banking Agreement", agreement_exist)
        agreement_doc.agreement_id = agreement_data.get("id")
        agreement_doc.max_historical_days = agreement_data.get("max_historical_days")
        agreement_doc.access_validity_days = agreement_data.get("access_valid_for_days")
        agreement_doc.created_on = created_on
        agreement_doc.accepted_on = accepted_on
        agreement_doc.expires_on = access_expires_on
        agreement_doc.save()
        message = "GoCardless Banking Agreement updated successfully"    
    else:
    # If no agreement exists, create a new one
        agreement_doc = frappe.get_doc({
            "doctype": "GoCardless Banking Agreement",
            "bank_id": agreement_data.get("institution_id"),
            "bank_name": bank_name,
            "agreement_id": agreement_data.get("id"),
            "gocardless_banking_settings": gocardless_banking_settings.name,
            "max_historical_days": agreement_data.get("max_historical_days"),
            "access_validity_days": agreement_data.get("access_valid_for_days"),
            "created_on": created_on,
            "accepted_on": accepted_on,
            "expires_on": access_expires_on,
        })
        agreement_doc.insert()
        message = "GoCardless Banking Agreement created successfully"

    return {"message": message}


@frappe.whitelist()
def refresh_gocardless_keys(gocardless_banking_settings_name):
    gocardless_banking_settings = frappe.get_doc("GoCardless Banking Settings", gocardless_banking_settings_name)
    # Check if the access key has expired
    if frappe.utils.get_datetime() >= gocardless_banking_settings.access_expiry:
        # Use refresh token to get new keys
        url = "https://bankaccountdata.gocardless.com/api/v2/token/refresh/"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {
            "refresh": gocardless_banking_settings.refresh_key
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        if response.status_code != 200:
            frappe.throw(f"Failed to refresh keys. Response: {response.text}")
        
        response_data = response.json()
        new_access_key = response_data.get('access')
        new_access_expires = response_data.get('access_expires')

        # Calculate new expiry dates
        new_access_expiry_date = frappe.utils.add_days(frappe.utils.getdate(), new_access_expires // 86400)  # convert seconds to days

        # Update the GoCardless Settings with new keys and expiry times
        gocardless_banking_settings.access_key = new_access_key
        gocardless_banking_settings.access_expiry = new_access_expiry_date
        gocardless_banking_settings.save()

        frappe.msgprint(f"Access Keys refreshed successfully for {gocardless_banking_settings_name}.")
    
@frappe.whitelist()
def scheduled_refresh_gocardless_keys():
    """
    Refresh GoCardless access keys for all settings with expired access or refresh tokens.
    """
    current_datetime = get_datetime()

    # Fetch settings where either access_expiry or refresh_expiry is expired
    settings_list = frappe.get_all(
        "GoCardless Banking Settings",
        filters=[
            ["refresh_expiry", "not in", ["", None]],  # Ensure refresh_expiry is valid
            ["access_expiry", "not in", ["", None]],   # Ensure access_expiry is valid
            [
                "or",  # Combine conditions with OR
                [
                    ["refresh_expiry", "<=", current_datetime],
                    ["access_expiry", "<=", current_datetime]
                ]
            ]
        ],
        fields=["name", "access_expiry", "refresh_expiry"]
    )

    for settings in settings_list:
        try:
            if settings.refresh_expiry <= current_datetime:
                generate_gocardless_keys(settings.name)
                frappe.logger().info(f"Generated new keys for: {settings.name} (refresh token expired)")
            elif settings.access_expiry <= current_datetime:
                refresh_gocardless_keys(settings.name)
                frappe.logger().info(f"Refreshed access key for: {settings.name}")
        except Exception as e:
            frappe.log_error(
                f"Error processing {settings.name}: {str(e)}",
                title="GoCardless Key Refresh Error"
            )