from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import re

app = Flask(__name__)

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Bug Report Generator</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', sans-serif; }
        body { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); min-height: 100vh; padding: 40px 20px; }
        .container { max-width: 900px; margin: 0 auto; }
        h1 { color: #00d9ff; text-align: center; margin-bottom: 10px; font-size: 2.2rem; }
        .subtitle { color: #888; text-align: center; margin-bottom: 30px; font-size: 0.95rem; }
        .card { background: #1e1e2f; border-radius: 16px; padding: 35px; box-shadow: 0 25px 80px rgba(0,0,0,0.5); border: 1px solid #2a2a4a; }
        .form-group { margin-bottom: 25px; }
        label { display: block; margin-bottom: 10px; font-weight: 600; color: #ccc; font-size: 0.95rem; }
        textarea { width: 100%; padding: 18px; border: 2px solid #2a2a4a; border-radius: 10px; font-size: 1rem; background: #151525; color: #fff; transition: border-color 0.3s; resize: vertical; min-height: 150px; }
        textarea:focus { outline: none; border-color: #00d9ff; }
        .btn { background: linear-gradient(135deg, #00d9ff 0%, #0099cc 100%); color: #000; border: none; padding: 16px 50px; border-radius: 10px; font-size: 1.1rem; font-weight: 600; cursor: pointer; transition: all 0.3s; width: 100%; margin-top: 10px; }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 15px 40px rgba(0,217,255,0.3); }
        .btn:disabled { background: #444; cursor: not-allowed; transform: none; }
        .warning-box { background: #2a1f1f; border: 1px solid #ff6b6b; border-radius: 10px; padding: 20px; margin-top: 25px; display: none; }
        .warning-box.show { display: block; }
        .warning-box h3 { color: #ff6b6b; margin-bottom: 10px; font-size: 1.1rem; }
        .warning-box p { color: #ff9999; line-height: 1.6; }
        .result-box { background: #151525; border-radius: 10px; padding: 25px; margin-top: 25px; display: none; border: 1px solid #00d9ff; }
        .result-box.show { display: block; }
        .result-box h3 { color: #00d9ff; margin-bottom: 20px; font-size: 1.2rem; }
        .field { margin-bottom: 18px; }
        .field-label { color: #888; font-size: 0.85rem; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 0.5px; }
        .field-value { color: #fff; font-size: 1rem; line-height: 1.5; }
        .confidence { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; margin-left: 10px; }
        .confidence.high { background: #1a3d1a; color: #4ade80; }
        .confidence.low { background: #3d1a1a; color: #ff6b6b; }
        .btn-download { background: #28a745; color: white; border: none; padding: 12px 30px; border-radius: 8px; font-size: 1rem; cursor: pointer; margin-top: 20px; }
        .btn-download:hover { background: #218838; }
        .btn-download:disabled { background: #444; cursor: not-allowed; }
        .spinner { display: none; width: 20px; height: 20px; border: 3px solid #fff; border-top-color: transparent; border-radius: 50%; animation: spin 1s linear infinite; margin-left: 10px; }
        @keyframes spin { to { transform: rotate(360deg); } }
        .loading { display: flex; align-items: center; justify-content: center; }
        .json-output { background: #0d0d1a; border-radius: 8px; padding: 20px; margin-top: 20px; }
        .json-output pre { color: #00d9ff; font-family: 'Consolas', monospace; font-size: 0.9rem; overflow-x: auto; white-space: pre-wrap; }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Bug Report Generator</h1>
        <p class="subtitle">Enter a free-text bug description and get a structured bug report</p>
        
        <div class="card">
            <form id="bugForm">
                <div class="form-group">
                    <label>Bug Description (Free Text) *</label>
                    <textarea name="description" id="description" required placeholder="Describe the bug in your own words. Include what happened, where it happened, and any details you noticed...

Example: When I try to login with invalid credentials, the error message is not displayed properly. The page just reloads without showing any feedback to the user."></textarea>
                </div>
                
                <button type="submit" class="btn" id="generateBtn">
                    <span id="btnText">Generate Bug Report</span>
                    <div class="spinner" id="spinner"></div>
                </button>
            </form>
            
            <div class="warning-box" id="warningBox">
                <h3>⚠️ Need More Information</h3>
                <p id="warningMessage"></p>
            </div>
            
            <div class="result-box" id="resultBox">
                <h3>Generated Bug Report</h3>
                <div id="reportContent"></div>
                <button class="btn-download" id="downloadBtn" onclick="downloadExcel()">Download Excel</button>
                <div class="json-output">
                    <label>JSON Output:</label>
                    <pre id="jsonOutput"></pre>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let currentReport = null;
        
        const form = document.getElementById('bugForm');
        const generateBtn = document.getElementById('generateBtn');
        const btnText = document.getElementById('btnText');
        const spinner = document.getElementById('spinner');
        const warningBox = document.getElementById('warningBox');
        const warningMessage = document.getElementById('warningMessage');
        const resultBox = document.getElementById('resultBox');
        const reportContent = document.getElementById('reportContent');
        const jsonOutput = document.getElementById('jsonOutput');
        const downloadBtn = document.getElementById('downloadBtn');
        
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const description = document.getElementById('description').value.trim();
            if (!description) {
                alert('Please enter a bug description');
                return;
            }
            
            generateBtn.disabled = true;
            btnText.textContent = 'Processing...';
            spinner.style.display = 'inline-block';
            warningBox.classList.remove('show');
            resultBox.classList.remove('show');
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ description })
                });
                
                const data = await response.json();
                
                spinner.style.display = 'none';
                btnText.textContent = 'Generate Bug Report';
                generateBtn.disabled = false;
                
                if (data.needs_clarification) {
                    warningBox.classList.add('show');
                    warningMessage.textContent = data.message;
                    return;
                }
                
                currentReport = data.report;
                displayReport(data.report);
                
            } catch (error) {
                spinner.style.display = 'none';
                btnText.textContent = 'Generate Bug Report';
                generateBtn.disabled = false;
                alert('Error: ' + error.message);
            }
        });
        
        function displayReport(report) {
            const confidenceClass = report.confidence >= 80 ? 'high' : 'low';
            
            reportContent.innerHTML = `
                <div class="field">
                    <div class="field-label">Bug Title</div>
                    <div class="field-value">${report.title}</div>
                </div>
                <div class="field">
                    <div class="field-label">Description</div>
                    <div class="field-value">${report.description}</div>
                </div>
                <div class="field">
                    <div class="field-label">Steps to Reproduce</div>
                    <div class="field-value">${report.steps_to_reproduce}</div>
                </div>
                <div class="field">
                    <div class="field-label">Expected Behavior</div>
                    <div class="field-value">${report.expected_behavior}</div>
                </div>
                <div class="field">
                    <div class="field-label">Actual Behavior</div>
                    <div class="field-value">${report.actual_behavior}</div>
                </div>
                <div class="field">
                    <div class="field-label">Severity <span class="confidence ${confidenceClass}">${report.severity}</span></div>
                    <div class="field-value">${report.severity}</div>
                </div>
                <div class="field">
                    <div class="field-label">Priority</div>
                    <div class="field-value">${report.priority}</div>
                </div>
                <div class="field">
                    <div class="field-label">Environment</div>
                    <div class="field-value">${report.environment}</div>
                </div>
                <div class="field">
                    <div class="field-label">Test Type</div>
                    <div class="field-value">${report.test_type}</div>
                </div>
                <div class="field">
                    <div class="field-label">Status</div>
                    <div class="field-value">${report.status}</div>
                </div>
                <div class="field">
                    <div class="field-label">Confidence Score</div>
                    <div class="field-value">${report.confidence}%</div>
                </div>
            `;
            
            jsonOutput.textContent = JSON.stringify(report, null, 2);
            resultBox.classList.add('show');
        }
        
        async function downloadExcel() {
            if (!currentReport) return;
            
            try {
                const response = await fetch('/download-excel', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(currentReport)
                });
                
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `bug_report_${Date.now()}.xlsx`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                a.remove();
            } catch (error) {
                alert('Error downloading Excel: ' + error.message);
            }
        }
    </script>
</body>
</html>
'''

def validate_input(description):
    issues = []
    
    if not description or len(description.strip()) < 10:
        issues.append("Description is too short or empty")
    
    keywords = {
        'action': ['click', 'enter', 'submit', 'type', 'select', 'navigate', 'press', 'tap', 'open', 'close'],
        'result': ['error', 'wrong', 'incorrect', 'fail', 'crash', 'freeze', 'not', 'unable', 'cannot'],
        'location': ['page', 'screen', 'button', 'form', 'field', 'input', 'login', 'menu', 'modal', 'dropdown']
    }
    
    desc_lower = description.lower()
    
    has_action = any(kw in desc_lower for kw in keywords['action'])
    has_result = any(kw in desc_lower for kw in keywords['result'])
    has_location = any(kw in desc_lower for kw in keywords['location'])
    
    score = sum([has_action, has_result, has_location])
    
    if score < 2:
        if not has_action:
            issues.append("Missing information about what action was performed")
        if not has_result:
            issues.append("Missing information about what went wrong or the observed behavior")
        if not has_location:
            issues.append("Missing information about where the bug occurred (page/screen/element)")
    
    word_count = len(description.split())
    if word_count < 5:
        issues.append("Description is too brief (less than 5 words)")
    
    return issues, score

def generate_bug_report(description):
    issues, clarity_score = validate_input(description)
    
    if issues:
        return {
            "needs_clarification": True,
            "message": "I am not fully understanding the issue. Could you please provide more details such as steps, expected behavior, or actual behavior?",
            "issues": issues,
            "clarity_score": clarity_score
        }
    
    if OPENAI_API_KEY:
        return generate_with_openai(description)
    else:
        return generate_local(description)

def generate_with_openai(description):
    import requests
    
    prompt = f'''Analyze this bug description and generate a structured bug report. 

IMPORTANT RULES:
1. Only generate if description is clear with ≥80% confidence
2. If unclear, return "NEEDS_CLARIFICATION" with specific missing info
3. Do NOT fabricate information

Bug Description: {description}

Return a JSON object with these exact fields:
- title: Short clear summary (max 60 chars)
- description: Refined version of input
- steps_to_reproduce: Numbered list
- expected_behavior: What should happen
- actual_behavior: What actually happened
- severity: Low | Medium | High | Critical
- priority: Low | Medium | High
- environment: Web | Mobile | API | Desktop
- test_type: Functional | UI | Performance | Security
- status: New
- confidence: 0-100 score of how clear the description is
- missing_info: Array of any unclear aspects (empty if clear)

Respond ONLY with valid JSON.'''
    
    try:
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {OPENAI_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'gpt-3.5-turbo',
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': 0.3
            },
            timeout=30
        )
        
        if response.status_code == 200:
            content = response.json()['choices'][0]['message']['content']
            result = json.loads(content)
            result['needs_clarification'] = result.get('confidence', 100) < 80
            if result['needs_clarification']:
                result['message'] = "I am not fully understanding the issue. Could you please provide more details such as steps, expected behavior, or actual behavior?"
            return result
        else:
            return generate_local(description)
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return generate_local(description)

def generate_local(description):
    desc_lower = description.lower()
    
    severity_indicators = {
        'Critical': ['crash', 'freeze', 'data loss', 'security', 'breach', 'unauthorized', 'system down'],
        'Major': ['error', 'fail', 'not working', 'broken', 'wrong', 'incorrect'],
        'Medium': ['issue', 'problem', 'delay', 'slow', 'unexpected'],
        'Low': ['typo', 'cosmetic', 'minor', 'suggestion', 'improvement']
    }
    
    severity = 'Medium'
    for sev, indicators in severity_indicators.items():
        if any(ind in desc_lower for ind in indicators):
            severity = sev
            break
    
    priority_map = {'Critical': 'High', 'Major': 'High', 'Medium': 'Medium', 'Low': 'Low'}
    priority = priority_map[severity]
    
    environment = 'Web'
    if any(x in desc_lower for x in ['mobile', 'ios', 'android', 'app']):
        environment = 'Mobile'
    elif any(x in desc_lower for x in ['api', 'endpoint', 'rest', 'json', 'backend']):
        environment = 'API'
    elif any(x in desc_lower for x in ['desktop', 'exe', 'install']):
        environment = 'Desktop'
    
    test_type = 'Functional'
    if any(x in desc_lower for x in ['ui', 'visual', 'display', 'style', 'color', 'layout', 'button']):
        test_type = 'UI'
    elif any(x in desc_lower for x in ['performance', 'slow', 'load', 'speed', 'memory']):
        test_type = 'Performance'
    elif any(x in desc_lower for x in ['security', 'auth', 'login', 'password', 'injection']):
        test_type = 'Security'
    
    clarity_score = 80
    
    if any(x in desc_lower for x in ['step', 'then', 'after', 'before', 'first', 'next']):
        clarity_score += 10
    if any(x in desc_lower for x in ['expected', 'should', 'but', 'instead']):
        clarity_score += 5
    
    clarity_score = min(clarity_score, 95)
    
    action_words = ['click', 'enter', 'type', 'submit', 'select', 'navigate', 'press', 'open']
    found_actions = [w for w in action_words if w in desc_lower]
    
    if found_actions:
        steps = f"1. {found_actions[0].title()} on the relevant element\n2. Observe the behavior"
    else:
        steps = "1. Perform the described action\n2. Observe the behavior"
    
    words = description.split()
    title = ' '.join(words[:6])[:60]
    if len(words) > 6:
        title += '...'
    
    expected = "The system should behave correctly according to requirements"
    if 'error' in desc_lower or 'wrong' in desc_lower:
        expected = "Proper error message should be displayed"
    if 'login' in desc_lower:
        expected = "User should be able to login successfully or see appropriate error"
    
    actual = description
    
    if clarity_score < 80:
        return {
            "needs_clarification": True,
            "message": "I am not fully understanding the issue. Could you please provide more details such as steps, expected behavior, or actual behavior?",
            "confidence": clarity_score
        }
    
    return {
        "needs_clarification": False,
        "title": title,
        "description": description,
        "steps_to_reproduce": steps,
        "expected_behavior": expected,
        "actual_behavior": actual,
        "severity": severity,
        "priority": priority,
        "environment": environment,
        "test_type": test_type,
        "status": "New",
        "confidence": clarity_score
    }

def create_excel(report):
    wb = Workbook()
    ws = wb.active
    ws.title = "Bug Report"
    
    header_fill = PatternFill(start_color="00D9FF", end_color="00D9FF", fill_type="solid")
    header_font = Font(bold=True, color="000000")
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    headers = ["Title", "Description", "Steps to Reproduce", "Expected Behavior", "Actual Behavior", "Severity", "Priority", "Environment", "Test Type", "Status"]
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.border = thin_border
        cell.alignment = Alignment(horizontal='center', wrap_text=True)
    
    values = [
        report.get('title', ''),
        report.get('description', ''),
        report.get('steps_to_reproduce', ''),
        report.get('expected_behavior', ''),
        report.get('actual_behavior', ''),
        report.get('severity', ''),
        report.get('priority', ''),
        report.get('environment', ''),
        report.get('test_type', ''),
        report.get('status', 'New')
    ]
    
    for col, value in enumerate(values, 1):
        cell = ws.cell(row=2, column=col, value=value)
        cell.border = thin_border
        cell.alignment = Alignment(wrap_text=True, vertical='top')
    
    ws.column_dimensions['A'].width = 25
    ws.column_dimensions['B'].width = 35
    ws.column_dimensions['C'].width = 30
    ws.column_dimensions['D'].width = 30
    ws.column_dimensions['E'].width = 30
    ws.column_dimensions['F'].width = 12
    ws.column_dimensions['G'].width = 12
    ws.column_dimensions['H'].width = 12
    ws.column_dimensions['I'].width = 15
    ws.column_dimensions['J'].width = 10
    
    ws.row_dimensions[2].height = 100
    
    return wb

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    description = data.get('description', '').strip()
    
    if not description:
        return jsonify({
            "needs_clarification": True,
            "message": "Please provide a bug description"
        })
    
    result = generate_bug_report(description)
    return jsonify(result)

@app.route('/download-excel', methods=['POST'])
def download_excel():
    import io
    
    report = request.json
    
    if not report or report.get('needs_clarification'):
        return jsonify({"error": "No valid report to export"}), 400
    
    wb = create_excel(report)
    
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    
    filename = f"bug_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

if __name__ == '__main__':
    print("=" * 60)
    print("AI Bug Report Generator")
    print("=" * 60)
    print("\nTo use OpenAI API, set OPENAI_API_KEY environment variable")
    print("Otherwise, local generation will be used")
    print("\nStarting server at http://localhost:5000")
    print("=" * 60)
    app.run(debug=False, port=5000)
