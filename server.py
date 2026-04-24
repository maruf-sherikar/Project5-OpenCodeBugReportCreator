from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import re

HTML = '''<!DOCTYPE html>
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
        .subtitle { color: #888; text-align: center; margin-bottom: 30px; }
        .card { background: #1e1e2f; border-radius: 16px; padding: 35px; box-shadow: 0 25px 80px rgba(0,0,0,0.5); border: 1px solid #2a2a4a; }
        .form-group { margin-bottom: 25px; }
        label { display: block; margin-bottom: 10px; font-weight: 600; color: #ccc; }
        textarea { width: 100%; padding: 18px; border: 2px solid #2a2a4a; border-radius: 10px; font-size: 1rem; background: #151525; color: #fff; min-height: 150px; }
        textarea:focus { outline: none; border-color: #00d9ff; }
        .btn { background: linear-gradient(135deg, #00d9ff 0%, #0099cc 100%); color: #000; border: none; padding: 16px 50px; border-radius: 10px; font-size: 1.1rem; font-weight: 600; cursor: pointer; width: 100%; margin-top: 10px; }
        .btn:hover { transform: translateY(-2px); }
        .warning-box { background: #2a1f1f; border: 1px solid #ff6b6b; border-radius: 10px; padding: 20px; margin-top: 25px; display: none; }
        .warning-box.show { display: block; }
        .warning-box h3 { color: #ff6b6b; margin-bottom: 10px; }
        .warning-box p { color: #ff9999; }
        .result-box { background: #151525; border-radius: 10px; padding: 25px; margin-top: 25px; display: none; border: 1px solid #00d9ff; }
        .result-box.show { display: block; }
        .result-box h3 { color: #00d9ff; margin-bottom: 20px; }
        .field { margin-bottom: 18px; }
        .field-label { color: #888; font-size: 0.85rem; margin-bottom: 5px; text-transform: uppercase; }
        .field-value { color: #fff; }
        .btn-download { background: #28a745; color: white; border: none; padding: 12px 30px; border-radius: 8px; font-size: 1rem; cursor: pointer; margin-top: 20px; }
        .json-output { background: #0d0d1a; border-radius: 8px; padding: 20px; margin-top: 20px; }
        .json-output pre { color: #00d9ff; font-family: monospace; font-size: 0.9rem; white-space: pre-wrap; }
        .bug-item { background: #1a1a2e; padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 3px solid #00d9ff; }
        .bug-number { color: #00d9ff; font-weight: bold; margin-bottom: 8px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Bug Report Generator</h1>
        <p class="subtitle">Enter free-text bug description(s) - use numbering (1., 2., 3.) or line breaks for multiple bugs</p>
        <div class="card">
            <form id="bugForm">
                <div class="form-group">
                    <label>Bug Description (Free Text) *</label>
                    <textarea name="description" id="description" placeholder="Enter one or multiple bugs...

Example:
1. When I try to login with wrong password, error message is not shown
2. Submit button freezes on the form page"></textarea>
                </div>
                <button type="submit" class="btn">Generate Bug Report</button>
            </form>
            <div class="warning-box" id="warningBox">
                <h3>Need More Information</h3>
                <p id="warningMessage"></p>
            </div>
            <div class="result-box" id="resultBox">
                <h3>Generated Bug Reports</h3>
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
        document.getElementById('bugForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const desc = document.getElementById('description').value.trim();
            if (!desc) return alert('Please enter a bug description');
            const res = await fetch('/generate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ description: desc })
            });
            const data = await res.json();
            if (data.needs_clarification) {
                document.getElementById('warningBox').classList.add('show');
                document.getElementById('warningMessage').textContent = data.message;
                document.getElementById('resultBox').classList.remove('show');
                return;
            }
            currentReport = data;
            displayReport(data);
        });
        function displayReport(report) {
            document.getElementById('warningBox').classList.remove('show');
            let html = '';
            const fields = ['title', 'description', 'steps_to_reproduce', 'expected_behavior', 'actual_behavior', 'severity', 'priority', 'environment', 'test_type', 'status'];
            report.forEach((bug, index) => {
                html += '<div class="bug-item"><div class="bug-number">Bug #' + (index + 1) + '</div>';
                fields.forEach(f => {
                    html += '<div class="field"><div class="field-label">' + f.replace(/_/g, ' ') + '</div><div class="field-value">' + (bug[f] || '') + '</div></div>';
                });
                html += '</div>';
            });
            document.getElementById('reportContent').innerHTML = html;
            document.getElementById('jsonOutput').textContent = JSON.stringify(report, null, 2);
            document.getElementById('resultBox').classList.add('show');
        }
        async function downloadExcel() {
            if (!currentReport) return;
            const res = await fetch('/download-excel', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(currentReport)
            });
            const blob = await res.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'bug_report.xlsx';
            a.click();
        }
    </script>
</body>
</html>'''

def split_bugs(description):
    text = description.strip()
    if not text:
        return []
    
    bugs = []
    
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if re.match(r'^\d+[\.\)]\s+', line):
            if bugs and bugs[-1] not in ['SPLIT_MARKER']:
                bugs.append(line)
            else:
                bugs.append(line)
        elif bugs and bugs[-1] != 'SPLIT_MARKER':
            bugs[-1] = bugs[-1] + ' ' + line
        else:
            bugs.append(line)
    
    if not bugs:
        pattern = r'\d+[\.\)]\s+(?=[A-Z])'
        parts = re.split(pattern, text)
        bugs = [p.strip() for p in parts if p.strip()]
    
    if not bugs:
        bugs = [text]
    
    cleaned = []
    for bug in bugs:
        bug = bug.strip()
        bug = re.sub(r'^\d+[\.\)]\s+', '', bug)
        bug = bug.strip()
        if bug:
            cleaned.append(bug)
    
    return cleaned if cleaned else [text]

def generate_single_report(description):
    desc_lower = description.lower()
    
    severity_indicators = {'Critical': ['crash', 'freeze', 'data loss', 'security', 'breach'], 'Major': ['error', 'fail', 'not working', 'broken', 'wrong'], 'Medium': ['issue', 'problem', 'delay', 'slow'], 'Low': ['typo', 'cosmetic', 'minor']}
    severity = 'Medium'
    for sev, inds in severity_indicators.items():
        if any(i in desc_lower for i in inds):
            severity = sev
            break
    
    priority = {'Critical': 'High', 'Major': 'High', 'Medium': 'Medium', 'Low': 'Low'}[severity]
    
    environment = 'Web'
    if any(x in desc_lower for x in ['mobile', 'ios', 'android', 'app']): environment = 'Mobile'
    elif any(x in desc_lower for x in ['api', 'endpoint', 'rest', 'backend']): environment = 'API'
    
    test_type = 'Functional'
    if any(x in desc_lower for x in ['ui', 'visual', 'display', 'button', 'style']): test_type = 'UI'
    elif any(x in desc_lower for x in ['performance', 'slow', 'load', 'speed']): test_type = 'Performance'
    elif any(x in desc_lower for x in ['security', 'auth', 'login', 'password']): test_type = 'Security'
    
    action_words = ['click', 'enter', 'type', 'submit', 'select', 'navigate']
    found = [w for w in action_words if w in desc_lower]
    steps = "1. " + (found[0].title() if found else "Perform") + " the action\n2. Observe the behavior"
    
    words = description.split()
    title = ' '.join(words[:6])[:60] + ('...' if len(words) > 6 else '')
    
    expected = "System should work correctly"
    if 'error' in desc_lower or 'wrong' in desc_lower: expected = "Proper error message should be displayed"
    if 'login' in desc_lower: expected = "User should login or see appropriate error"
    
    return {
        "title": title,
        "description": description,
        "steps_to_reproduce": steps,
        "expected_behavior": expected,
        "actual_behavior": description,
        "severity": severity,
        "priority": priority,
        "environment": environment,
        "test_type": test_type,
        "status": "New"
    }

def generate_report(description):
    bug_descriptions = split_bugs(description)
    print(f"DEBUG: Found {len(bug_descriptions)} bugs: {bug_descriptions}")
    reports = []
    for bug_desc in bug_descriptions:
        if len(bug_desc.strip()) > 10:
            reports.append(generate_single_report(bug_desc))
    
    if not reports:
        return {"needs_clarification": True, "message": "Could not detect any valid bug descriptions. Please provide more details."}
    
    print(f"DEBUG: Generated {len(reports)} reports")
    return reports

def create_excel(reports):
    wb = Workbook()
    ws = wb.active
    ws.title = "Bug Reports"
    header_fill = PatternFill(start_color="00D9FF", end_color="00D9FF", fill_type="solid")
    header_font = Font(bold=True, color="000000")
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
    headers = ["#", "Title", "Description", "Steps to Reproduce", "Expected Behavior", "Actual Behavior", "Severity", "Priority", "Environment", "Test Type", "Status"]
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.border = thin_border
    
    for row, report in enumerate(reports, 2):
        values = [row-1] + [report.get(f, '') for f in ['title', 'description', 'steps_to_reproduce', 'expected_behavior', 'actual_behavior', 'severity', 'priority', 'environment', 'test_type', 'status']]
        for col, value in enumerate(values, 1):
            ws.cell(row=row, column=col, value=value).border = thin_border
    
    ws.column_dimensions['A'].width = 6
    ws.column_dimensions['B'].width = 25
    ws.column_dimensions['C'].width = 35
    ws.column_dimensions['D'].width = 30
    ws.column_dimensions['E'].width = 30
    ws.column_dimensions['F'].width = 30
    return wb

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(HTML.encode())
    
    def do_POST(self):
        if self.path == '/generate':
            length = int(self.headers['Content-Length'])
            data = self.rfile.read(length)
            desc = json.loads(data)['description']
            report = generate_report(desc)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(report).encode())
        elif self.path == '/download-excel':
            length = int(self.headers['Content-Length'])
            data = self.rfile.read(length)
            reports = json.loads(data)
            wb = create_excel(reports)
            import io
            buffer = io.BytesIO()
            wb.save(buffer)
            buffer.seek(0)
            self.send_response(200)
            self.send_header('Content-type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            self.send_header('Content-Disposition', 'attachment; filename=bug_report.xlsx')
            self.end_headers()
            self.wfile.write(buffer.read())

print("Starting server at http://localhost:8002")
server = HTTPServer(('localhost', 8002), Handler)
server.serve_forever()