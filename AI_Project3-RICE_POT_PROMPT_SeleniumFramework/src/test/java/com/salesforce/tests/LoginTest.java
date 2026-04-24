package com.salesforce.tests;

import com.salesforce.base.BaseTest;
import com.salesforce.pages.LoginPage;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.Assert;
import org.testng.annotations.Test;

import java.time.Duration;

public class LoginTest extends BaseTest {

    @Test(priority = 1, description = "Verify successful login with valid credentials")
    public void testValidLogin() {
        try {
            LoginPage loginPage = new LoginPage(driver);
            
            // Note: Since this is an automation script, place actual valid credentials below to test
            loginPage.doLogin("valid.user@salesforce.com", "SecurePassword123!");
            
            // Verification: Wait for URL to change to dashboard or title to change
            WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(15));
            boolean isUrlChanged = wait.until(ExpectedConditions.not(ExpectedConditions.urlContains("login.salesforce.com/?locale=in")));
            
            Assert.assertTrue(isUrlChanged, "User was not redirected after successful login.");
        } catch (Exception e) {
            Assert.fail("Valid login test failed due to exception: " + e.getMessage());
        }
    }

    @Test(priority = 2, description = "Verify error message with invalid credentials")
    public void testInvalidLogin() {
        try {
            // Re-navigate to clear states from previous tests
            driver.get("https://login.salesforce.com/?locale=in");
            
            LoginPage loginPage = new LoginPage(driver);
            
            loginPage.doLogin("invalid.user@salesforce.com", "WrongPassword!");
            
            String errorMessage = loginPage.getErrorMessage();
            
            Assert.assertTrue(errorMessage.contains("check your username and password"), 
                    "Expected Error message was not displayed. Actual: " + errorMessage);
        } catch (Exception e) {
            Assert.fail("Invalid login test failed due to exception: " + e.getMessage());
        }
    }
}
