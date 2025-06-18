<div align="center">
	<img src="https://avatars.githubusercontent.com/u/118217131?s=400&u=c795a6f774a4427c644c398a4d6a83ce4430c74d&v=4" height="80">
	<h2>Prilk Consulting BV</h2>
   <h3>GoCardless Banking Integration</h3>
</div>

## Overview

**GoCardless Banking Integration** is a powerful Frappe/ERPNext app that connects your bank accounts to ERPNext, enabling seamless financial management. With support for over **2,500 banks** across the UK and Europe, this app automates transaction fetching, account synchronization, and balance tracking, saving you time and ensuring accuracy.

> **Note**: This integration requires a GoCardless subscription. Visit [GoCardless Bank Account Data](https://gocardless.com/bank-account-data/) for pricing and sign-up details.

---

## Key Features

### 🏦 Bank Account Integration

- Connect multiple GoCardless bank accounts
- Secure OAuth-based authentication
- Automatic synchronization of account data
- Bank account verification
- Support for multiple bank connections

### 💸 Transaction Management

- Daily and manual transaction synchronization
- Detailed transaction history
- Real-time account balance tracking
- Transaction categorization for better insights

### 🔒 Security & Compliance

- Encrypted API key storage
- GDPR-compliant data handling
- Secure bank account data encryption
- Regular key rotation for enhanced security

---

## Installation

Follow these steps to install the GoCardless Banking Integration app on your Frappe/ERPNext instance.

1. **Install the app** in your Frappe bench:

   ```bash
   bench get-app https://github.com/prilk-consulting/gocardless_banking
   ```

2. **Install the app on your site**:

   ```bash
   bench --site [your-site-name] install-app gocardless_banking
   ```

3. **Configure GoCardless API credentials** in the app settings (see Configuration).

---

## Configuration

### 1. API Setup

- Obtain GoCardless API credentials from GoCardless.
- Add credentials to the app settings in ERPNext.
- Configure webhook endpoints for real-time updates.
- Set environment variables for secure operation.

### 2. Bank Account Settings

- Select supported banks from the list of 2,500+ institutions.
- Configure account verification settings.
- Define synchronization preferences (e.g., daily or manual).

---

## Usage

### Setting Up Bank Accounts

1. Create a banking agreement in ERPNext.
2. Connect your bank accounts via the secure GoCardless authentication flow.
3. Verify account access and monitor connection status.

### Managing Transactions

- View and filter transaction history.
- Monitor real-time account balances.
- Track synchronization status and resolve any issues.
- Generate financial reports for better decision-making.

---

## API Integration

The app integrates with the GoCardless Banking API to provide:

- Real-time bank account data retrieval
- Automated transaction synchronization
- Secure account verification
- Continuous balance updates

---

## Security

We prioritize your data security with:

- **Encrypted Storage**: API keys and bank account details are securely encrypted.
- **GDPR Compliance**: Full adherence to data protection regulations.
- **Regular Audits**: Ongoing security reviews to ensure robustness.
- **Key Rotation**: Periodic updates to API keys for added protection.

---

## Contributing

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

## Support

For assistance, please:

- Open an issue on the GitHub repository.
- Contact the Prilk Consulting BV team at support@prilk.com.
- Refer to the documentation for troubleshooting.

---

## Credits

Developed with ❤️ by Prilk Consulting BV.

### Acknowledgments

- Frappe Framework
- ERPNext
- GoCardless Banking API
- The open-source community

---

Simplify your financial management with GoCardless Banking Integration for ERPNext.

**Get Started Today!**
