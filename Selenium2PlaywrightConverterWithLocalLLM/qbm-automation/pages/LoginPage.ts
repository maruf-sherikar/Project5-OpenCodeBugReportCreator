import { Page, Locator } from '@playwright/test';
import { BasePage } from './BasePage';

export class LoginPage extends BasePage {
    readonly usernameInput: Locator;
    readonly passwordInput: Locator;
    readonly loginButton: Locator;

    constructor(page: Page) {
        super(page);
        this.usernameInput = page.locator('input[name="username"], input#username, input[placeholder*="Username"]');
        this.passwordInput = page.locator('input[name="password"], input#password, input[placeholder*="Password"]');
        this.loginButton = page.locator('button[type="submit"], button:has-text("Login"), input[type="submit"]');
    }

    async login(username: string, password: string) {
        await this.log(`Attempting login for user: ${username}`);
        await this.usernameInput.fill(username);
        await this.passwordInput.fill(password);
        await this.loginButton.click();
    }
}
