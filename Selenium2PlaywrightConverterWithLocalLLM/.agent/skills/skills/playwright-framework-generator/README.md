# 🎭 Playwright Framework Generator Skill

This skill allows Antigravity to generate a full, production-ready **Playwright (TypeScript)** automation framework based on a domain name and specific automation instructions.

## 🚀 Usage

Trigger this skill by saying:
- "Create a Playwright framework for [Domain]"
- "Setup Playwright automation for [Domain] with instructions: [Instructions]"

## 📦 What's Included

- **Page Object Model (POM)**: Organized page classes for maintainability.
- **Custom Reporter**: A uniquely designed reporting utility.
- **Advanced Configuration**: Multi-browser support, retries, and trace capturing.
- **TypeScript Support**: Full type safety for elements and actions.

## 🛠️ Installation

This skill is stored in:
`.agent/skills/skills/playwright-framework-generator/`

To use it, ensure you have the `skills` directory active in your Antigravity environment.

## 📝 Example

**User**: "Create a Playwright framework for https://saucedemo.com. Automate the login and add product to cart."

**Antigravity**: *Generates full folder structure, classes for LoginPage and InventoryPage, and a spec file for the checkout flow.*
