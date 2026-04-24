# Salesforce Selenium Automation Framework

This project is an enterprise-grade Selenium automation framework built using Java, Maven, and TestNG. It is specifically designed to test the Salesforce login functionality using a robust Page Object Model (POM) architecture.

## 🚀 Key Features
- **Page Object Model (POM)**: Ensures clean separation between test logic and UI elements.
- **Strict XPath Usage**: Uses relative and robust XPath locators.
- **Explicit Waits**: Avoids deprecated anti-patterns like `Thread.sleep()` using robust Selenium WebDriver Explicit Waits.
- **Comprehensive Exception Handling**: Wraps interactions in try-catch blocks to ensure readable error traces and stable executions.
- **TestNG / Maven Integration**: Enables scalable test runs, continuous integration readiness, and dependency management.

---

## 🧠 The RICE POT Prompt Framework

This repository was generated using the **RICE POT** structured artificial intelligence prompting technique. To help others learn from this methodology, below is the breakdown of the exact conversational context supplied to the AI to construct this robust framework:

### R.I.C.E.
* **R - Role**: "Act as a Lead Quality Assurance Automation Architect and Senior SDET."
* **I - Instructions**: "Build an enterprise-grade Selenium automation framework using Java, Maven, and TestNG to automate the Salesforce login page for both valid and invalid scenarios."
* **C - Context**: "The framework must ensure highly maintainable code. We need a strict Page Object Model (POM) architecture to keep page UI elements separated from execution flows."
* **E - Expectations**: "Strictly avoid deprecated practices such as `Thread.sleep()`. Rely heavily on Explicit Waits. Implement robust exception handling at every interaction point to prevent silent failures."

### P.O.T.
* **P - Parameters**: "Use precise and dynamic XPath locators for all WebElements. Ensure the configuration uses `pom.xml` accurately for TestNG, WebDriverManager, and Selenium dependencies."
* **O - Output Format**: "Provide perfectly structured Java files (e.g., `BaseTest.java`, `LoginPage.java`, `LoginTest.java`) neatly organized in `src/main` and `src/test` directories."
* **T - Target Audience / Tone**: "The code must feature meaningful comments and be easily understandable for Junior QA Engineers to learn from, while still meeting the stringent standards of Enterprise DevOps pipelines."

---

## 🛠️ Setup & Execution

### Prerequisites
- Java JDK 11 or higher
- Maven installed and configured
- Chrome Browser

### Running the Tests
To execute the automation suite, simply navigate to the root directory in your terminal and run:

```bash
mvn clean test
```
