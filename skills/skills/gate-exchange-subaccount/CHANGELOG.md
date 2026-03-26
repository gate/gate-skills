# Changelog

## [2026.3.12-1] - 2026-03-12

### Added
- Initial release of gate-exchange-subaccount skill
- Query sub-account status: get details of a specific sub-account by UID
- List all sub-accounts: view all normal sub-accounts under the main account
- Create sub-account: create new normal sub-accounts with login name, optional email and remark
- Lock sub-account: disable login and trading for a specific sub-account with confirmation flow
- Unlock sub-account: restore access for a previously locked sub-account with confirmation flow
- 10 scenario definitions covering normal flows and edge cases

### Audit
- All write operations require explicit user confirmation
- Sub-account UID validated before lock/unlock operations
- State pre-check to avoid redundant lock/unlock operations
- No internal API keys, domains, or proprietary data exposed
- Error messages are user-friendly without internal debug information
