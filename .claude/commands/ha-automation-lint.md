---
description: Validate Home Assistant automation YAML for syntax errors and best practices
argument-hint: [file-path]
allowed-tools: Read, Bash
---

# Home Assistant Automation Linter

Validate Home Assistant automation YAML configuration files for syntax errors, deprecated patterns, and best practices.

## Task

1. **Identify the target file(s)**:
   - If `$1` is provided, validate that specific automation file
   - If no argument, search for automation files in current directory (*.yaml, *.yml in automations/ or config/)
   - Handle both single automation files and automation.yaml with multiple entries

2. **Validate YAML syntax**:
   - Check for valid YAML structure using `yamllint` or Python yaml parser
   - Report any syntax errors with line numbers
   - Ensure proper indentation and key structure

3. **Check Home Assistant automation structure**:
   - Verify required fields: `alias`, `trigger`, `condition` (optional), `action`
   - Validate trigger types: `state`, `numeric_state`, `time`, `time_pattern`, `sun`, `event`, `mqtt`, `webhook`, `device`, `zone`, `geo_location`, `tag`, `calendar`, `persistent_notification`, `template`
   - Validate condition types: `state`, `numeric_state`, `time`, `sun`, `zone`, `template`, `and`, `or`, `not`
   - Validate action structure and common services
   - Check automation mode: `single`, `restart`, `queued`, `parallel` (with optional `max` for `queued`/`parallel`)

4. **Detect deprecated patterns**:
   - Old condition shortcut syntax (should use full object structure)
   - Deprecated `platform:` syntax in triggers (should be `trigger:`)
   - Missing explicit `conditions:` array when multiple conditions exist
   - Using `if:` instead of structured conditions
   - Deprecated service call formats (e.g., old entity_id vs target syntax)

5. **Suggest best practices**:
   - Recommend using `choose` action instead of multiple sequential automations with same trigger
   - Suggest template conditions instead of complex state conditions
   - Recommend using device triggers for cleaner configuration
   - Suggest naming conventions: descriptive aliases, kebab-case for templates
   - Point out performance improvements (e.g., using numeric_state triggers instead of template for numeric comparisons)
   - Flag potential issues: empty conditions/actions, missing delay units, hardcoded values that should be templated

6. **Report findings**:
   - **Critical issues** (blocks execution): Syntax errors, missing required fields, invalid trigger/condition/action types
   - **Warnings** (should fix): Deprecated patterns, non-existent entity references, potential performance issues
   - **Suggestions** (nice to have): Best practice improvements, cleaner syntax options
   - Show file location, line number, and specific field for each issue
   - Provide corrected YAML snippets for common fixes

## Target File

${1:-.}

## Notes

- Use Python's `yaml` module or bash `yamllint` for syntax validation
- Home Assistant entities often reference `light.living_room`, `sensor.temperature`, etc. - suggest validation against common patterns but don't require them
- For Jinja2 templates in triggers/conditions, validate syntax basics but acknowledge complexity
- Provide output in clear, actionable format suitable for automation developers
- Include links to relevant Home Assistant documentation for unfamiliar concepts
