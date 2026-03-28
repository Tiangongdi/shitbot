# Learnings Log

This file captures corrections, knowledge gaps, and best practices discovered during development.

---

## [LRN-20260328-001] best_practice

**Logged**: 2026-03-28T23:54:00Z
**Priority**: high
**Status**: resolved
**Area**: config, tools

### Summary
When writing long text content with write_file, JSON parsing can fail due to unescaped quotes in the content.

### Details
The problem occurs when:
- Using `write_file` to write a single large block of text containing quotes (")
- The quotes are not properly escaped in the JSON payload
- Results in "Unterminated string" JSON parse error

User pointed out this issue consistently happens with long text input.

### Suggested Action
Always use **分段追加法** (segmented append approach) for large files:
1. First create an empty file with `write_file`
2. Then append content in multiple smaller segments using `append_to_file`
3. Each append should be a reasonably sized chunk to avoid JSON escaping issues

This avoids putting all the quoted content in a single JSON parameter.

### Metadata
- Source: user_feedback
- Related Files: `./tools/file_tools.py`, any large markdown/doc files
- Tags: json, escaping, write_file, best-practice
- Pattern-Key: tool.write_file.long_text_escaping
- Recurrence-Count: 1
- First-Seen: 2026-03-28
- Last-Seen: 2026-03-28

---
