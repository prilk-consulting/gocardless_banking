<div align="center">
	<img src="https://avatars.githubusercontent.com/u/118217131?s=400&u=c795a6f774a4427c644c398a4d6a83ce4430c74d&v=4" height="80">
	<h2>Prilk Consulting BV</h2>
   <h3>GoCardless Banking Integration with ERPNext</h3>
</div>

## Overview

**GoCardless Banking Integration** is a powerful Frappe/ERPNext app that connects your bank accounts to ERPNext, enabling seamless financial management. With support for over **2,500 banks** across UK and EU (European Union), this app automates transaction fetching, account synchronization, and balance tracking, saving you time and ensuring accuracy.

> **Note**: This integration requires a GoCardless subscription. Visit [GoCardless Bank Account Data](https://gocardless.com/bank-account-data/) for pricing and sign-up details. As of July 2025, Gocardless provides a free subscription £/€0 per month with a limit of Up to 50 bank connections per month.

---

## Key Features

### 🏦 Bank Account Integration

- Connect multiple GoCardless accounts
- Support for multiple bank connections
- Automatic synchronization of account data
- Secure authentication with GoCardless.
- Bank account verification via GoCardless

### 💸 Transaction Management

- Daily automated and manual transaction synchronization
- Detailed transaction history
- Account balance auto update.

### 🔒 Security & Compliance

- Encrypted API key storage
- GDPR-compliant data handling
- Secure bank account data encryption
- Regular key rotation for enhanced security

---

## Installation

Follow these steps to install the GoCardless Banking Integration app on your Frappe/ERPNext instance.

1. **Install the app** in your Frappe bench or via Frappecloud:

   ```bash
   bench get-app https://github.com/prilk-consulting/gocardless_banking
   ```

2. **Install the app on your site**:

   ```bash
   bench --site [your-site-name] install-app gocardless_banking
   ```

---

## Configuration

### 1. GoCardless Banking Account Set up

- Obtain GoCardless API credentials from GoCardless.
- Add credentials to the app settings in ERPNext.
- Activate Gocardless Account in the app.

### 2. Add Bank Accounts

- Select your bank from the list of banks.
- Verify Bank account credentials via GoCardless.
- Link ERPNext Bank Account to GoCardless Bank Account.
- Enable Automated sync if required.

---

## Usage

### Managing Transactions

- Fetch Transactions automatically or manually.
- View and filter transaction history via ERPNext Bank Transaction document.
- Check account balances and Track synchronization status.

---


## Upcoming Features

- Integration with Advanced Bank Reconciliation
- Alerts and monitoring
- Analytics and Reporting

---

## Support and Feature Request

For assistance, please:

- Open an issue on the GitHub repository.
- Contact the Prilk Consulting team at [Support page](https://www.prilk.com/contact).

---

## Contribution

We welcome contributions to enhance the GoCardless Banking Integration app! To contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

Please read our Contributing Guidelines for more details.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Credits

Developed by Prilk Consulting BV.

### Acknowledgments

- Frappe Framework
- ERPNext
- GoCardless Banking API
- The open-source community

---

Simplify your financial management with GoCardless Banking Integration for ERPNext.

**Get Started Today!**
