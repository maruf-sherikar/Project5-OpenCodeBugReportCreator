const http = require('http');

console.log("Testing Backend API /api/convert...");

const javaCode = `
package com.example;
import org.testng.annotations.Test;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class LoginTest {
    @Test
    public void testLogin() {
        WebDriver driver = new ChromeDriver();
        driver.get("https://example.com");
        driver.findElement(By.id("username")).sendKeys("admin");
        driver.findElement(By.id("password")).sendKeys("password");
        driver.findElement(By.id("submit")).click();
        driver.quit();
    }
}
`;

const postData = JSON.stringify({
    sourceCode: javaCode,
    options: { usePageObjectModel: true }
});

const options = {
    hostname: 'localhost',
    port: 3001,
    path: '/api/convert',
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData),
    },
};

const req = http.request(options, (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
        if (res.statusCode === 200) {
            console.log("✅ API Success!");
            try {
                const json = JSON.parse(data);
                console.log("--- Converted Code ---");
                if (json.files && json.files.length > 0) {
                    json.files.forEach(f => {
                        console.log(`[FILE] ${f.fileName} (${f.fileType}):`);
                        console.log(f.content.substring(0, 150) + "...");
                    });
                } else {
                    console.log("No files returned (Check LLM response formatting?)");
                    console.log("Raw:", data);
                }
            } catch (e) {
                console.log("Error parsing JSON:", e.message);
                console.log("Raw Response:", data);
            }
        } else {
            console.log(`❌ API Failed: ${res.statusCode}`);
            console.log(data);
        }
    });
});

req.on('error', e => {
    console.error(`❌ Connection Error: ${e.message}`);
});

req.write(postData);
req.end();
