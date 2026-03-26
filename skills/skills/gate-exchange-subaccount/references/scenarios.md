# Gate Exchange Sub-Account — Scenarios & Prompt Examples

## Scenario 1: Query Sub-Account Status by UID

**Context**: User wants to check the current status of a specific sub-account by providing its UID.

**Prompt Examples**:
- "What is the status of sub-account UID 123456?"
- "Check sub-account 789012"
- "Show me details for sub-account UID 555555"
- "Is sub-account 123456 locked or normal?"

**Expected Behavior**:
1. Extract `user_id` from user input (e.g. `123456`)
2. Call `cex_sa_get_sa(user_id=123456)`
3. If found: display sub-account details (username, UID, status, type, remark, creation time)
4. If not found: respond "Sub-account with UID 123456 was not found. Please verify the UID and try again."

---

## Scenario 2: List All Sub-Accounts

**Context**: User is a main account holder and wants to see all sub-accounts they have created.

**Prompt Examples**:
- "Show me all my sub-accounts"
- "Which sub-accounts have I created?"
- "List my sub-accounts"
- "How many sub-accounts do I have?"

**Expected Behavior**:
1. Call `cex_sa_list_sas(type="0")` to retrieve all normal sub-accounts
2. If authenticated and has sub-accounts: display table with username, UID, remark (if any), and current status for each sub-account
3. If no sub-accounts: respond "You have not created any sub-accounts yet."
4. If not authenticated: prompt "Please log in to your Gate account first."

---

## Scenario 3: Create a New Sub-Account

**Context**: User wants to create a new normal sub-account under their main account.

**Prompt Examples**:
- "I want to create a sub-account"
- "Create a new sub-account for me"
- "Add a sub-account"
- "Help me set up a new sub-account"

**Expected Behavior**:
1. Call `cex_sa_list_sas(type="0")` to check the current number of normal sub-accounts and confirm creation availability
2. If creation quota is available: ask user to provide a login name — "Please enter a login name for the new sub-account."
3. Optionally collect email and remark
4. Confirm details: "Please confirm you want to create a sub-account with login name '{login_name}'. Reply 'confirm' to proceed."
5. On confirmation: call `cex_sa_create_sa(login_name="{login_name}")`
6. Report the newly created sub-account details (UID, username, status)
7. If creation quota is exhausted: respond "You have reached the maximum number of normal sub-accounts. Please contact support if you need more."

---

## Scenario 4: Lock a Sub-Account

**Context**: User wants to lock a specific sub-account to disable its login and trading capabilities.

**Prompt Examples**:
- "Lock sub-account UID 123456"
- "I want to lock sub-account 789012"
- "Disable sub-account 555555"
- "Freeze sub-account UID 123456"

**Expected Behavior**:
1. Extract `user_id` from user input (e.g. `123456`)
2. Call `cex_sa_get_sa(user_id=123456)` to verify the sub-account exists and belongs to the main account
3. If sub-account is already locked: respond "Sub-account 123456 is already locked. No action needed."
4. If sub-account is in normal state: ask for confirmation — "Are you sure you want to lock sub-account 123456 ({login_name})? This will disable login and trading. Reply 'confirm' to proceed."
5. On confirmation: call `cex_sa_lock_sa(user_id=123456)`
6. Report result: "Sub-account 123456 has been locked successfully."

---

## Scenario 5: Unlock a Sub-Account

**Context**: User wants to unlock a previously locked sub-account to restore its access.

**Prompt Examples**:
- "Unlock sub-account UID 123456"
- "I want to unlock sub-account 789012"
- "Enable sub-account 555555"
- "Unfreeze sub-account UID 123456"

**Expected Behavior**:
1. Extract `user_id` from user input (e.g. `123456`)
2. Call `cex_sa_get_sa(user_id=123456)` to verify the sub-account exists and is currently locked
3. If sub-account is already in normal (unlocked) state: respond "Sub-account 123456 is already in normal state. No action needed."
4. If sub-account is locked: ask for confirmation — "Are you sure you want to unlock sub-account 123456 ({login_name})? Reply 'confirm' to proceed."
5. On confirmation: call `cex_sa_unlock_sa(user_id=123456)`
6. Report result: "Sub-account 123456 has been unlocked successfully."

---

## Scenario 6: UID Not Provided for Lock/Unlock

**Context**: User wants to lock or unlock a sub-account but does not provide the UID.

**Prompt Examples**:
- "Lock my sub-account"
- "I want to unlock a sub-account"
- "Help me disable one of my sub-accounts"

**Expected Behavior**:
1. Detect lock/unlock intent but no UID provided
2. Ask: "Which sub-account would you like to {lock/unlock}? Please provide the sub-account UID."
3. Optionally, call `cex_sa_list_sas(type="0")` and display available sub-accounts for the user to choose from

---

## Scenario 7: Not Logged In

**Context**: User requests a sub-account operation without a valid session.

**Prompt Examples**:
- "Show my sub-accounts"
- "Check sub-account status for UID 123456"

**Expected Behavior**:
1. Call the corresponding MCP tool
2. API returns "not login" error
3. Respond: "Please log in to your Gate account to manage sub-accounts."

---

## Scenario 8: Not a Main Account

**Context**: User tries to manage sub-accounts but their account is not a main account.

**Prompt Examples**:
- "Create a sub-account"
- "List my sub-accounts"

**Expected Behavior**:
1. Call the corresponding MCP tool
2. API returns permission error indicating the user is not a main account
3. Respond: "Sub-account management requires main account privileges. Please switch to your main account."

---

## Scenario 9: Sub-Account Does Not Belong to User

**Context**: User provides a UID that does not belong to any of their sub-accounts.

**Prompt Examples**:
- "Lock sub-account UID 999999"
- "Check status of sub-account 888888"

**Expected Behavior**:
1. Call `cex_sa_get_sa(user_id=999999)`
2. API returns error indicating the sub-account does not belong to the user
3. Respond: "Sub-account with UID 999999 was not found or does not belong to your main account. Please verify the UID and try again."

---

## Scenario 10: Create Sub-Account with Duplicate Login Name

**Context**: User tries to create a sub-account with a login name that is already taken.

**Prompt Examples**:
- "Create a sub-account with login name 'trader01'"

**Expected Behavior**:
1. Confirm details with user
2. Call `cex_sa_create_sa(login_name="trader01")`
3. API returns error indicating the login name is already taken
4. Respond: "The login name 'trader01' is already taken. Please choose a different name."
