# Errors Log

This file captures unexpected command failures and errors for future debugging.

---

## [ERR-20260328-001] git_push

**Logged**: 2026-03-28T23:55:00Z
**Priority**: medium
**Status**: pending
**Area**: infra, git

### Summary
Git push to GitHub fails with SSH permission denied (publickey).

### Error
```
git@github.com: Permission denied (publickey).
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

### Context
- Remote configured as: `origin git@github.com:Tiangongdi/shitbot.git (fetch/push)`
- Attempting: `git push -u origin master`
- Local Git repository exists and commit is ready

### Suggested Fix
- Check if SSH public key is added to GitHub account
- If no SSH key configured, switch remote to HTTPS URL:
  ```
  git remote set-url origin https://github.com/Tiangongdi/shitbot.git
  ```
  Then push with username/password authentication

### Metadata
- Reproducible: yes
- Related Files: `.git/config`
- See Also: N/A

---
