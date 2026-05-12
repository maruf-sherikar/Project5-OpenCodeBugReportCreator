# AI Bug Report Generator

A web application that generates structured bug reports from free-text descriptions using AI/NLP.

## Features

- **Single Input**: Takes only a free-text bug description
- **Auto-Generation**: Automatically generates all bug report fields
- **No Hallucination**: Validates input before generating; asks for clarification if unclear
- **Confidence Scoring**: Reports clarity score (≥80% required to generate)
- **Excel Export**: Download bug report as Excel file

## Usage

### Start the Server

```bash
python bug_report_app.py
```

Then open http://localhost:5000 in your browser.

### Using OpenAI API (Optional)

Set the API key as an environment variable:

```bash
set OPENAI_API_KEY=your-api-key
python bug_report_app.py
```

## Test Cases

### Test Case 1: Clear Description (Generates Report)

**Input:**
```
When I try to login with invalid credentials (wrong username or password), the error message is not displayed properly. The page just reloads without showing any feedback to the user.
```

**Output:**
```json
{
  "title": "When I try to login with invalid credentials...",
  "description": "When I try to login with invalid credentials (wrong username or password), the error message is not displayed properly. The page ...",
  "steps_to_reproduce": "1. Click on login field\n2. Enter invalid credentials\n3. Observe the behavior",
  "expected_behavior": "Proper error message should be displayed",
  "actual_behavior": "The page reloads without showing any feedback to the user",
  "severity": "Medium",
  "priority": "Medium",
  "environment": "Web",
  "test_type": "UI",
  "status": "New",
  "confidence": 85
}
```

### Test Case 2: Clear Description with More Details

**Input:**
```
Clicking the Submit button on the registration form does not work. The page freezes and nothing happens. I am using Chrome browser on Windows 11.
```

**Output:**
```json
{
  "title": "Clicking the Submit button on the...",
  "severity": "Major",
  "priority": "High",
  "environment": "Web",
  "test_type": "Functional",
  "confidence": 90,
  ...
}
```

### Test Case 3: Unclear Description (Asks for Clarification)

**Input:**
```
bug
```

**Output:**
```json
{
  "needs_clarification": true,
  "message": "I am not fully understanding the issue. Could you please provide more details such as steps, expected behavior, or actual behavior?",
  "confidence": 20
}
```

### Test Case 4: Missing Result Information

**Input:**
```
I clicked the login button
```

**Output:**
```json
{
  "needs_clarification": true,
  "message": "I am not fully understanding the issue. Could you please provide more details such as steps, expected behavior, or actual behavior?",
  "confidence": 65
}
```

## Validation Rules

The system validates input based on:

1. **Minimum Length**: At least 10 characters
2. **Word Count**: At least 5 words
3. **Required Keywords**:
   - Action words: click, enter, type, submit, select, navigate, press, tap, open, close
   - Result words: error, wrong, incorrect, fail, crash, freeze, not, unable, cannot
   - Location words: page, screen, button, form, field, input, login, menu, modal, dropdown
4. **Confidence Threshold**: ≥80% required to generate report

If any of these criteria are not met, the system will ask for clarification instead of generating a potentially incorrect report.

## Excel Export

The Excel file contains these columns:
- Title
- Description
- Steps to Reproduce
- Expected Behavior
- Actual Behavior
- Severity
- Priority
- Environment
- Test Type
- Status

## API Endpoints

- `GET /` - Main UI
- `POST /generate` - Generate bug report
- `POST /download-excel` - Download as Excel

## Dependencies

- Flask
- openpyxl