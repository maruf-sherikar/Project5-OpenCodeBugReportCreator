import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { DashboardPage } from '../pages/DashboardPage';

test.describe('QBM Login Workflows', () => {
    let loginPage: LoginPage;
    let dashboardPage: DashboardPage;

    test.beforeEach(async ({ page }) => {
        loginPage = new LoginPage(page);
        dashboardPage = new DashboardPage(page);
        await loginPage.navigateTo('/');
    });

    test('User should be able to see login page elements', async ({ page }) => {
        await expect(loginPage.usernameInput).toBeVisible();
        await expect(loginPage.passwordInput).toBeVisible();
        await expect(loginPage.loginButton).toBeVisible();
    });

    test('Attempt login and verify dashboard (Positive Case)', async ({ page }) => {
        // Note: Credentials would normally be in .env
        await loginPage.login('test_user', 'test_password');

        // Check if dashboard is visible after login
        const isVisible = await dashboardPage.isVisible();
        expect(isVisible).toBeTruthy();
    });
});
