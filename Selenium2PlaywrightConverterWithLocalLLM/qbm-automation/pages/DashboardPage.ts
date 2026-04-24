import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';

export class DashboardPage extends BasePage {
    readonly dashboardHeader: Locator;
    readonly sidebar: Locator;

    constructor(page: Page) {
        super(page);
        this.dashboardHeader = page.locator('h1, h2, .page-title, :has-text("Dashboard")').first();
        this.sidebar = page.locator('nav, .sidebar, #sidebar');
    }

    async isVisible() {
        await this.log('Checking for Dashboard visibility');
        await expect(this.dashboardHeader).toBeVisible();
        return await this.dashboardHeader.isVisible();
    }
}
