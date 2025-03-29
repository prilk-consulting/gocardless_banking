# Copyright (c) 2025, Prilk Consulting BV and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests
import json


class GoCardlessBankingAccount(Document):
	pass

@frappe.whitelist()
def fetch_transactions(gocardless_banking_account_name):
    # Fetch the GoCardless Banking Account details
    gocardless_banking_account = frappe.get_doc("GoCardless Banking Account", gocardless_banking_account_name)
    gocardless_banking_agreement = frappe.get_doc("GoCardless Banking Agreement", gocardless_banking_account.gocardless_banking_agreement)
    gocardless_banking_settings = frappe.get_doc("GoCardless Banking Settings", gocardless_banking_agreement.gocardless_banking_settings)

    if not gocardless_banking_settings.access_key:
        frappe.throw("Access token is missing for this GoCardless Banking Account.")

    if not gocardless_banking_account.account_id:
        frappe.throw("Account ID is missing for this GoCardless Banking Account.")

    # API URL to fetch transactions
    url = f"https://bankaccountdata.gocardless.com/api/v2/accounts/{gocardless_banking_account.account_id}/transactions/"
    headers = {
        "Authorization": f"Bearer {gocardless_banking_settings.access_key}",
        "accept": "application/json",
    }

    try:
        # Make the API request
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Process transactions
        transactions = data.get("transactions", {})
        create_bank_transactions(gocardless_banking_account_name, transactions)

        # Update the last synced timestamp
        gocardless_banking_account.last_synced = frappe.utils.now()
        gocardless_banking_account.save()

        return f"Transactions fetched and created for {gocardless_banking_account_name}."
    except requests.exceptions.RequestException as e:
        frappe.log_error(message=str(e), title="Transaction Fetch Failed")
        frappe.throw(f"Failed to fetch transactions: {str(e)}")

def create_bank_transactions(gocardless_banking_account_name, transactions):
    # Create booked transactions
    for booked in transactions.get("booked", []):
        create_transaction(gocardless_banking_account_name, booked, transaction_type="Booked")

    # Create pending transactions
    for pending in transactions.get("pending", []):
        create_transaction(gocardless_banking_account_name, pending, transaction_type="Pending")


def create_transaction(gocardless_banking_account_name, transaction_data, transaction_type):
    # Fetch the GoCardless Banking Account document
    gocardless_banking_account = frappe.get_doc("GoCardless Banking Account", gocardless_banking_account_name)
    # Check if a Bank Transaction with this transactionId already exists
    transaction_id = transaction_data.get("transactionId")
    if transaction_id and frappe.get_value("Bank Transaction", {"transaction_id": transaction_id}, "name"):
        # Skip this transaction if it already exists
        frappe.log_error(f"Skipping duplicate transaction with ID: {transaction_id}", "gocardless Transaction Import")
        return None  # Return None to indicate the transaction was skipped
    
    # Create a new Bank Transaction document
    bank_transaction = frappe.new_doc("Bank Transaction")
    
    # Assign values to the transaction fields
    bank_transaction.bank_account = gocardless_banking_account.bank_account
    bank_transaction.transaction_id = transaction_data.get("transactionId")
    # bank_transaction.debtor_name = transaction_data.get("debtorName")

    # Get the transaction amount and determine if it's a deposit or withdrawal
    transaction_amount = float(transaction_data["transactionAmount"]["amount"])
    
    # Dynamically set bank party details based on transaction amount
    if transaction_amount < 0:
        # Withdrawal: Use creditor details (party receiving money)
        bank_transaction.bank_party_name = transaction_data.get("creditorName")
        creditor_account = transaction_data.get("creditorAccount", {})
        bank_transaction.bank_party_iban = creditor_account.get("iban")
        bank_transaction.bank_party_account_number = creditor_account.get("iban")
    else:
        # Deposit: Use debtor details (party sending money)
        bank_transaction.bank_party_name = transaction_data.get("debtorName")
        debtor_account = transaction_data.get("debtorAccount", {})
        bank_transaction.bank_party_iban = debtor_account.get("iban")
        bank_transaction.bank_party_account_number = debtor_account.get("iban")

    if transaction_amount < 0:
        bank_transaction.withdrawal = abs(transaction_amount)  # Withdrawal is stored as a positive value
    else:
        bank_transaction.deposit = transaction_amount

    # Set other fields
    bank_transaction.currency = transaction_data["transactionAmount"]["currency"]
    bank_transaction.date = transaction_data.get("valueDate") or transaction_data.get("bookingDate")
    
    # Optional: Set the transaction type and description (if required)
    bank_transaction.transaction_type = transaction_type
    bank_transaction.description = json.dumps(transaction_data, indent=4)  # Store the API response as a JSON string
    
    # Insert the transaction record into the database
    bank_transaction.insert()

def scheduled_fetch_transactions():
    gocardless_banking_accounts = frappe.get_all("GoCardless Banking Account", filters={"automatic_sync": 1}, fields=["name"])
    for gocardless_banking_account in gocardless_banking_accounts:
        fetch_transactions(gocardless_banking_account.name)
