from flask import Flask, render_template_string, request, send_file
from datetime import datetime
import json
import os

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bug Report Creator</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', sans-serif; }
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        h1 { color: white; text-align: center; margin-bottom: 30px; font-size: 2.5rem; }
        .card { background: white; border-radius: 15px; padding: 30px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; font-weight: 600; color: #333; }
        input, textarea, select { width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 1rem; transition: border-color 0.3s; }
        input:focus, textarea:focus, select:focus { outline: none; border-color: #667eea; }
        textarea { resize: vertical; min-height: 100px; }
        .row { display: flex; gap: 20px; }
        .col { flex: 1; }
        .btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 15px 40px; border-radius: 8px; font-size: 1.1rem; cursor: pointer; transition: transform 0.2s; width: 100%; margin-top: 10px; }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(102,126,234,0.4); }
        .preview { background: #f5f5f5; border-radius: 8px; padding: 20px; margin-top: 20px; white-space: pre-wrap; font-family: monospace; font-size: 0.9rem; max-height: 400px; overflow-y: auto; display: none; }
        .preview.show { display: block; }
        .tabs { display: flex; gap: 10px; margin-bottom: 10px; }
        .tab { padding: 10px 20px; background: #e0e0e0; border: none; border-radius: 8px; cursor: pointer; }
        .tab.active { background: #667eea; color: white; }
        .success { background: #4caf50; color: white; padding: 15px; border-radius: 8px; text-align: center; margin-top: 20px; }
        a { color: #667eea; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Bug Report Creator</h1>
        <div class="card">
            <form id="bugForm">
                <div class="form-group">
                    <label>Bug Title *</label>
                    <input type="text" name="title" required placeholder="Enter bug title...">
                </div>
                
                <div class="form-group">
                    <label>Description *</label>
                    <textarea name="description" required placeholder="Describe the bug..."></textarea>
                </div>
                
                <div class="form-group">
                    <label>Steps to Reproduce *</label>
                    <textarea name="steps" required placeholder="1. Step one&#10;2. Step two&#10;3. Step three"></textarea>
                </div>
                
                <div class="form-group">
                    <label>Expected Behavior *</label>
                    <textarea name="expected" required placeholder="What should happen..."></textarea>
                </div>
                
                <div class="form-group">
                    <label>Actual Behavior *</label>
                    <textarea name="actual" required placeholder="What actually happens..."></textarea>
                </div>
                
                <div class="row">
                    <div class="col">
                        <div class="form-group">
                            <label>Severity *</label>
                            <select name="severity" required>
                                <option value="">Select severity</option>
                                <option value="Critical">Critical</option>
                                <option value="Major">Major</option>
                                <option value="Minor">Minor</option>
                                <option value="Low">Low</option>
                            </select>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-group">
                            <label>Priority *</label>
                            <select name="priority" required>
                                <option value="">Select priority</option>
                                <option value="High">High</option>
                                <option value="Medium">Medium</option>
                                <option value="Low">Low</option>
                            </select>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col">
                        <div class="form-group">
                            <label>Environment</label>
                            <input type="text" name="environment" placeholder="OS, Browser, etc.">
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-group">
                            <label>Assignee</label>
                            <input type="text" name="assignee" placeholder="Assigned to...">
                        </div>
                    </div>
                </div>
                
                <div class="form-group">
                    <label>Your Name</label>
                    <input type="text" name="reporter" placeholder="Your name...">
                </div>
                
                <div class="form-group">
                    <label>Attachments / Notes</label>
                    <textarea name="attachments" placeholder="Any additional notes or attachments..."></textarea>
                </div>
                
                <button type="submit" class="btn">Generate Bug Report</button>
            </form>
            
            <div id="result" class="preview"></div>
            <div id="downloadLinks" class="preview"></div>
        </div>
    </div>
    
    <script>
        const form = document.getElementById('bugForm');
        const resultDiv = document.getElementById('result');
        const downloadDiv = document.getElementById('downloadLinks');
        
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(form);
            const data = Object.fromEntries(formData);
            data.created_at = new Date().toISOString();
            
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            
            const files = await response.json();
            
            let mdContent = `# Bug Report

**Title:** ${data.title}
**Created:** ${data.created_at}
**Reporter:** ${data.reporter || 'N/A'}

---

## Details

**Severity:** ${data.severity}
**Priority:** ${data.priority}
**Environment:** ${data.environment || 'N/A'}
**Assignee:** ${data.assignee || 'Unassigned'}

---

## Description

${data.description}

---

## Steps to Reproduce

${data.steps}

---

## Expected Behavior

${data.expected}

---

## Actual Behavior

${data.actual}

---

## Attachments/Notes

${data.attachments || 'None'}
`;
            
            resultDiv.classList.add('show');
            resultDiv.textContent = mdContent;
            
            downloadDiv.classList.add('show');
            downloadDiv.innerHTML = '<div class="tabs"><button class="tab active" onclick="showTab(\'md\')">Markdown</button><button class="tab" onclick="showTab(\'txt\')">Text</button><button class="tab" onclick="showTab(\'json\')">JSON</button></div>' +
                '<p>Download: <a href="/download/md">bug_report.md</a> | <a href="/download/txt">bug_report.txt</a> | <a href="/download/json">bug_report.json</a></p>';
        });
        
        function showTab(format) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            event.target.classList.add('active');
        }
    </script>
</body>
</html>
'''

reports_store = {}

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = "".join(c for c in data['title'] if c.isalnum() or c in " -_").strip()[:30]
    filename = f"bug_report_{safe_title}_{timestamp}"
    
    report = {
        "title": data.get('title', ''),
        "description": data.get('description', ''),
        "steps_to_reproduce": data.get('steps', ''),
        "expected_behavior": data.get('expected', ''),
        "actual_behavior": data.get('actual', ''),
        "severity": data.get('severity', ''),
        "priority": data.get('priority', ''),
        "environment": data.get('environment', ''),
        "assignee": data.get('assignee', ''),
        "reporter": data.get('reporter', ''),
        "attachments": data.get('attachments', ''),
        "created_at": data.get('created_at', '')
    }
    
    reports_store['current'] = {
        "filename": filename,
        "report": report
    }
    
    md_content = f"""# Bug Report

**Title:** {report['title']}
**Created:** {report['created_at']}
**Reporter:** {report['reporter'] or 'N/A'}

---

## Details

**Severity:** {report['severity']}
**Priority:** {report['priority']}
**Environment:** {report['environment'] or 'N/A'}
**Assignee:** {report['assignee'] or 'Unassigned'}

---

## Description

{report['description']}

---

## Steps to Reproduce

{report['steps_to_reproduce']}

---

## Expected Behavior

{report['expected_behavior']}

---

## Actual Behavior

{report['actual_behavior']}

---

## Attachments/Notes

{report['attachments'] or 'None'}
"""
    
    txt_content = f"""BUG REPORT
{'=' * 50}

Title: {report['title']}
Created: {report['created_at']}
Reporter: {report['reporter'] or 'N/A'}

{'-' * 50}

Severity: {report['severity']}
Priority: {report['priority']}
Environment: {report['environment'] or 'N/A'}
Assignee: {report['assignee'] or 'Unassigned'}

{'-' * 50}

Description:
{report['description']}

Steps to Reproduce:
{report['steps_to_reproduce']}

Expected Behavior:
{report['expected_behavior']}

Actual Behavior:
{report['actual_behavior']}

Attachments/Notes:
{report['attachments'] or 'None'}
"""
    
    json_content = json.dumps(report, indent=2)
    
    with open(f"{filename}.md", "w") as f:
        f.write(md_content)
    with open(f"{filename}.txt", "w") as f:
        f.write(txt_content)
    with open(f"{filename}.json", "w") as f:
        f.write(json_content)
    
    return json.dumps({"success": True, "filename": filename})

@app.route('/download/<format>')
def download(format):
    if 'current' not in reports_store:
        return "No report generated yet", 400
    
    filename = reports_store['current']['filename']
    filepath = f"{filename}.{format}"
    
    if not os.path.exists(filepath):
        return "File not found", 404
    
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)