<div align="center">
	<img src="https://avatars.githubusercontent.com/u/118217131?s=400&u=c795a6f774a4427c644c398a4d6a83ce4430c74d&v=4" height="80">
	<h2>Prilk Consulting BV</h2>
   <h3>GoCardless Banking Integration</h3>
</div>

<div align="center">
<p><b>GoCardless Banking</b> is a seamless solution for connecting your bank accounts with ERPNext.</p>

<p>This app is designed to simplify your financial management by effortlessly fetching transactions from 2500+ of banks in UK and Europe and integrating them directly into your ERPNext system.</p>

<p>Experience the ease of automation and gain better control over your finances with the banking integration app for ERPNext users.</p>
</div>

<hr>
<b>Note</b>The Bank Integration works with a goCardless subscription. Visit <a href="https://gocardless.com/bank-account-data/">Gocardless bank account data</a> to check out the pricing and sign up.
<hr>
# GoCardless Banking Integration for Frappe/ERPNext

A Frappe/ERPNext app that integrates with GoCardless Banking API to fetch and manage bank account data and transactions.

## Features

- **Bank Account Integration**
  - Connect Multiple GoCardless Bank Integration Accounts
  - Connect multiple bank accounts
  - Secure authentication flow
  - Automatic account data synchronization
  - Bank account verification

- **Transaction Management**
  - Daily transaction synchronization
  - Manual transaction synchronization
  - Transaction history
  - Account balance tracking
  - Transaction categorization

- **Security & Compliance**
  - Secure API key management
  - GDPR compliant data handling
  - Encrypted data storage
  - Regular key rotation

## Installation

1. Install the app in your Frappe bench:
```bash
bench get-app https://github.com/prilk-consulting/gocardless_banking
```

2. Install the app on your site:
```bash
bench --site [your-site-name] install-app gocardless_banking
```

3. Configure GoCardless API credentials in the app settings

## Configuration

1. **API Setup**
   - Add GoCardless API credentials
   - Configure webhook endpoints
   - Set up environment variables

2. **Bank Account Settings**
   - Configure supported banks
   - Set up account verification
   - Define synchronization preferences

## Usage

1. **Setting Up Bank Accounts**
   - Create a banking agreement
   - Connect bank accounts
   - Verify account access
   - Monitor connection status

2. **Managing Transactions**
   - View transaction history
   - Monitor account balances
   - Track synchronization status
   - Generate reports

## API Integration

The app provides integration with GoCardless Banking API for:
- Bank account data retrieval
- Transaction synchronization
- Account verification
- Balance updates

## Security

- Secure API key storage
- Encrypted bank account details
- GDPR compliance
- Regular security audits

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please:
1. Open an issue in the GitHub repository
2. Contact the development team
3. Check the documentation for common issues

## Roadmap

- [ ] Enhanced transaction analytics
- [ ] Additional bank integrations
- [ ] Improved error handling
- [ ] Advanced reporting features
- [ ] Multi-currency optimization

## Credits

Developed by Prilk Consulting BV

## Acknowledgments

- Frappe Framework
- ERPNext
- GoCardless Banking API
- Open Source Community