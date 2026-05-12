import { Page, Locator, expect } from '@playwright/test';

export class BasePage {
    readonly page: Page;

    constructor(page: Page) {
        this.page = page;
    }

    async navigateTo(path: string = '/') {
        await this.page.goto(path);
    }

    async waitForElement(locator: Locator) {
        await expect(locator).toBeVisible({ timeout: 10000 });
    }

    async log(message: string) {
        console.log(`[LOG]: ${message}`);
    }
}
