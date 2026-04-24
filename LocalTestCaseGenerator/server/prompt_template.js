/* 
  Allows for easier editing of the prompt without touching code.
  We will replace {{REQUIREMENTS}} with user input.
*/

const PROMPT_TEMPLATE = `
You are an expert QA Engineer. Your task is to generate comprehensive test cases based on the user's requirements.

User Requirements:
"{{REQUIREMENTS}}"

Output Format:
Please provide the test cases in a clear Markdown format.
For each test case, include:
1. **Test Case ID** (e.g., TC-001)
2. **Title**: value
3. **Pre-conditions**: value
4. **Test Steps**: numbered list
5. **Expected Result**: value
6. **Priority**: (High/Medium/Low)

Ensure you cover positive flows, negative flows, and edge cases.
`;

module.exports = { PROMPT_TEMPLATE };
