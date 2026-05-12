# Bug Report Creator

A simple and elegant bug report creator with both web UI and CLI interfaces.

## Features

- **Web Interface** - Beautiful gradient UI for creating bug reports
- **CLI Interface** - Terminal-based bug report creation
- **Multiple Formats** - Export as Markdown, Plain Text, or JSON
- **Required Fields** - Title, Description, Steps to Reproduce, Expected/Actual Behavior
- **Optional Fields** - Severity, Priority, Environment, Assignee, Reporter

## Installation

```bash
pip install flask
```

## Usage

### Web UI

```bash
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

### CLI

```bash
python bug_report_creator.py
```

## Bug Report Fields

| Field | Required | Description |
|-------|----------|-------------|
| Title | Yes | Bug title |
| Description | Yes | Detailed bug description |
| Steps to Reproduce | Yes | How to reproduce the bug |
| Expected Behavior | Yes | What should happen |
| Actual Behavior | Yes | What actually happens |
| Severity | Yes | Critical/Major/Minor/Low |
| Priority | Yes | High/Medium/Low |
| Environment | No | OS, Browser, etc. |
| Assignee | No | Assigned developer |
| Reporter | No | Your name |
| Attachments/Notes | No | Additional notes |

## Output

Generated files are saved with timestamped filenames:
- `bug_report_{title}_{timestamp}.md`
- `bug_report_{title}_{timestamp}.txt`
- `bug_report_{title}_{timestamp}.json`

## Tech Stack

- Python 3
- Flask (Web UI)

## License

MIT