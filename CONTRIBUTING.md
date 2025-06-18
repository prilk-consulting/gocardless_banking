# Contributing to GoCardless Banking Integration for Frappe/ERPNext

Thank you for your interest in contributing to the **GoCardless Banking Integration** app for Frappe/ERPNext! We value contributions from the community to improve this app, which helps businesses seamlessly integrate their bank accounts with ERPNext. Whether you're reporting bugs, suggesting features, or submitting code, your efforts are appreciated.

This document outlines the guidelines for contributing to the project. Please read it carefully to ensure a smooth collaboration process.

---

## Table of Contents

- [How to Contribute](#how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Contributing Code](#contributing-code)
- [Development Setup](#development-setup)
- [Coding Guidelines](#coding-guidelines)
- [Pull Request Process](#pull-request-process)
- [Community and Support](#community-and-support)

---

## How to Contribute

### Reporting Bugs

If you encounter a bug, please help us improve the app by reporting it:

1. **Check existing issues**: Ensure the bug hasn’t already been reported in the [GitHub Issues](https://github.com/prilk-consulting/gocardless_banking/issues).
2. **Open a new issue**: Use the bug report template (if available) and provide:
   - A clear title and description of the bug.
   - Steps to reproduce the issue.
   - Expected and actual behavior.
   - Screenshots or logs, if applicable.
   - Environment details (e.g., ERPNext version, Python version, OS).

3. **Label the issue**: Add the "bug" label to help us prioritize.

### Suggesting Features

We welcome ideas for new features or improvements:

1. **Check existing requests**: Review the [GitHub Issues](https://github.com/prilk-consulting/gocardless_banking/issues) to avoid duplicates.
2. **Submit a feature request**: Create a new issue with the "enhancement" label and include:
   - A clear description of the feature.
   - The problem it solves or the benefit it provides.
   - Any relevant examples or use cases.

### Contributing Code

To contribute code (e.g., bug fixes, new features, or improvements):

1. **Fork the repository**: Create your own copy of the [repository](https://github.com/prilk-consulting/gocardless_banking).
2. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/gocardless_banking.git
   ```
3. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make changes**: Follow the [Coding Guidelines](#coding-guidelines) below.
5. **Commit changes**: Use clear, descriptive commit messages (e.g., `Add transaction sync error handling`).
6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request**: See the [Pull Request Process](#pull-request-process) for details.

---

## Development Setup

To set up the project locally:

1. **Install Frappe Bench**:
   Follow the [Frappe Bench installation guide](https://frappeframework.com/docs/v14/user/en/installation) to set up a Frappe/ERPNext environment.

2. **Install the app**:
   ```bash
   bench get-app https://github.com/prilk-consulting/gocardless_banking
   bench --site [your-site-name] install-app gocardless_banking
   ```

3. **Set up GoCardless API**:
   - Obtain sandbox or production API credentials from [GoCardless](https://gocardless.com/bank-account-data/).
   - Configure credentials in the app settings via ERPNext.

4. **Install dependencies**:
   Ensure all Python dependencies are installed:
   ```bash
   bench setup requirements
   ```

5. **Run the development server**:
   ```bash
   bench start
   ```

---

## Coding Guidelines

To maintain code quality, please adhere to these guidelines:

- **Code Style**:
  - Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code.
  - Use consistent naming conventions (e.g., `snake_case` for variables and functions).
  - Format code with tools like `black` or `autopep8`.

- **Frappe/ERPNext Conventions**:
  - Use Frappe’s [DocType](https://frappeframework.com/docs/v14/user/en/basics/doctypes) structure for new models.
  - Follow Frappe’s [naming conventions](https://frappeframework.com/docs/v14/user/en/basics/naming).
  - Write server-side logic in Python and client-side logic in JavaScript (using Frappe’s APIs).

- **Testing**:
  - Write unit tests for new functionality using Frappe’s testing framework.
  - Ensure tests pass before submitting a pull request:
    ```bash
    bench --site [your-site-name] run-tests --app gocardless_banking
    ```

- **Documentation**:
  - Update relevant documentation (e.g., `README.md`, inline code comments) for new features.
  - Include user-facing documentation for new functionality.

- **Security**:
  - Avoid hardcoding sensitive data (e.g., API keys).
  - Sanitize inputs to prevent security vulnerabilities.
  - Follow GDPR compliance for handling bank account data.

---

## Pull Request Process

1. **Ensure your code works**:
   - Test locally to confirm your changes don’t break existing functionality.
   - Run tests and linting tools.

2. **Create a Pull Request**:
   - Open a PR against the `main` branch of the repository.
   - Use a clear title (e.g., `Add webhook for transaction updates`) and detailed description.
   - Reference any related issues (e.g., `Fixes #123`).

3. **Code Review**:
   - Respond to feedback from maintainers promptly.
   - Make requested changes and update your PR.

4. **Approval and Merge**:
   - Once approved, your PR will be merged by a maintainer.
   - Ensure your branch is up-to-date with `main` to avoid merge conflicts.

---

## Community and Support

- **GitHub Issues**: Use [GitHub Issues](https://github.com/prilk-consulting/gocardless_banking/issues) for bug reports, feature requests, or questions.
- **Email**: Contact the Prilk Consulting BV team at [support@prilk.com](mailto:support@prilk.com) for direct inquiries.
- **Documentation**: Check the [README](README.md) and other docs for setup and usage details.

---

Thank you for contributing to the GoCardless Banking Integration app! Your efforts help make financial management easier for ERPNext users worldwide.

**Happy coding!**
