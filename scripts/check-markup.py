#!/usr/bin/env python3
"""Validate HTML5 parsing and CSS syntax. Dependencies: requirements-qa.txt."""
from pathlib import Path
import html5lib
import tinycss2

root = Path(__file__).resolve().parents[1]
errors = []
files = list(root.rglob('*.html'))
for path in files:
    parser = html5lib.HTMLParser()
    parser.parse(path.read_text())
    errors.extend(f'{path.relative_to(root)}: {error}' for error in parser.errors)

def validate_css(rules):
    for rule in rules:
        if rule.type == 'error':
            errors.append(str(rule))
        elif rule.type == 'qualified-rule':
            for declaration in tinycss2.parse_declaration_list(rule.content, skip_comments=True, skip_whitespace=True):
                if declaration.type == 'error':
                    errors.append(str(declaration))
        elif rule.type == 'at-rule' and rule.content:
            validate_css(tinycss2.parse_rule_list(rule.content, skip_comments=True, skip_whitespace=True))

validate_css(tinycss2.parse_stylesheet((root / 'styles/style.css').read_text(), skip_comments=True, skip_whitespace=True))
print(f'{len(files)} HTML documents and shared CSS: {len(errors)} parse errors')
for error in errors:
    print(error)
raise SystemExit(bool(errors))
