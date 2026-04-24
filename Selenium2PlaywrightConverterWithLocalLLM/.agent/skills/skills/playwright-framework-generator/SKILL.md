---
name: playwright-framework-generator
description: This skill automates the creation of a full Playwright JS/TS automation framework from scratch, implementing Page Object Model (POM), custom reporters, and industry-standard best practices.
version: 1.0.0
author: Antigravity
created: 2026-02-13
category: automation-testing
tags: [playwright, automation, testing, pom, framework-generator, typescript]
---

# Playwright Framework Generator

## Purpose
This skill provides a comprehensive workflow to scaffold a professional-grade Playwright automation framework. It ensures the generated code follows strict **Page Object Model (POM)** patterns, includes a **Custom Reporter**, and adheres to Playwright best practices (waiting locators, clean configuration, and TypeScript safety).

## When to Use
- When starting a new web automation project from scratch.
- When you need to demonstrate a clean Playwright architecture.
- When generating automation tests for a specific domain/URL and set of instructions.

## Core Workflow

### 1. Discovery
The skill must first ask the user for:
- **Project Name**: (e.g., `my-automation-suite`)
- **Domain Name**: The base URL (e.g., `https://example.com`)
- **Automation Instructions**: Specific scenarios to automate (e.g., "Login with valid credentials and verify dashboard").

### 2. Framework Scaffolding
Generate the following structure:

```text
{{PROJECT_NAME}}/
├── playwright.config.ts    # Advanced configuration with Custom Reporter
├── package.json            # Scripts: test, report, debug
├── tsconfig.json           # TypeScript configuration
├── pages/                  # Page Object Model classes
│   └── BasePage.ts         # Common methods (wait, navigation, logs)
├── tests/                  # Test spec files
├── utils/                  # Custom report utils and helpers
└── .gitignore              # Node modules and test results
```

### 3. Guidelines & Best Practices
The skill MUST ensure:
- **Locators**: Use Playwright's modern locators (e.g., `getByRole`, `getByPlaceholder`) instead of raw CSS/XPath where possible.
- **POM**: Encapsulate locators and actions within Page classes.
- **Reporting**: Include a custom reporter implementation that logs test steps clearly.
- **Async/Await**: Proper use of asynchronous patterns.
- **Clean Config**: Setup for multiple browsers (Chromium, Firefox, WebKit) and retries.

## Technical Implementation Snippets

### playwright.config.ts
```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  reporter: [
    ['html'],
    ['list'],
    ['./utils/custom-reporter.ts'] // Custom Reporter path
  ],
  use: {
    baseURL: '{{DOMAIN_URL}}',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],
});
```

### Page Object Pattern
```typescript
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly usernameInput: Locator;
  readonly loginButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.usernameInput = page.getByPlaceholder('Username');
    this.loginButton = page.getByRole('button', { name: 'Login' });
  }

  async login(user: string) {
    await this.usernameInput.fill(user);
    // ...
  }
}
```

## Step-by-Step Execution
1. **Initialize `package.json`**: Add `playwright`, `@playwright/test`, and `typescript`.
2. **Create `playwright.config.ts`**: Configure base URL and reporting.
3. **Generate Base Classes**: Create `pages/BasePage.ts`.
4. **Generate Feature Pages**: Based on user instructions, create specific Page Objects.
5. **Generate Test Specs**: Map user instructions to test cases using the Page Objects.
6. **Final Validation**: Ensure `npm install` and `npx playwright test` would run correctly.
