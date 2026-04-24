import re

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

description = """1. When I try to login with wrong password, error message is not shown.
2. Submit button freezes on the form page."""

result = split_bugs(description)
print(f"Found bugs: {len(result)}")
for i, bug in enumerate(result, 1):
    print(f"{i}. {bug}")