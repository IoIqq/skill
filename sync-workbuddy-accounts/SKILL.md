---
name: sync-workbuddy-accounts
description: >-
  When the user has multiple WorkBuddy accounts logged in on the same machine,
  and wants to merge conversations from another account into their current account.
  This skill detects other account sessions in the local database and rewrites
  their user_id so they appear under the current account.
agent_created: true
---

# Sync WorkBuddy Accounts

## Purpose

Merge conversations from a different WorkBuddy account into the current account by updating the `user_id` field in the local SQLite database and the `app/sessions.json` index.

Both accounts must have been used on the **same Windows machine, same Windows user** — the data is already on disk, just tagged with a different user ID.

## When to Trigger

Trigger this skill when the user says something like:

- "帮我同步另一个账号的会话"
- "把旧账号的对话合并过来"
- "切换账号后之前的会话不见了"
- "sync conversations from another account"
- "merge workbuddy accounts"

## Workflow

### 1. Identify the Old Account's user_id

Query the `sessions` table in `~/.workbuddy/workbuddy.db` to find user IDs that are **not** the current account's user ID:

```python
import sqlite3
conn = sqlite3.connect(r'~/.workbuddy/workbuddy.db')
cursor = conn.execute('SELECT DISTINCT user_id FROM sessions')
all_uids = [row[0] for row in cursor.fetchall()]
```

If there is only one user_id, there are no other accounts to merge. Inform the user and stop.

If there are two or more, the "other" accounts are the ones with fewer sessions, or the ones the user can identify by session titles.

### 2. Preview the Sessions to Merge

List all sessions belonging to the old user_id:

```python
cursor = conn.execute('''
    SELECT id, title, status, created_at, cwd
    FROM sessions
    WHERE user_id = ?
    ORDER BY created_at DESC
''', (OLD_UID,))
```

Show the user a summary: session title, date, message count (from the JSONL file), status.

### 3. Confirm with the User

Ask: "确认将这 N 个会话合并到当前账号？操作会修改本地数据库，并自动创建备份。"

### 4. Backup

Back up these files before making any changes:

- `~/.workbuddy/workbuddy.db` → `workbuddy.db.bak`
- `~/.workbuddy/app/sessions.json` → `sessions.json.bak`
- `~/.workbuddy/workbuddy.db-wal` → `workbuddy.db-wal.bak` (if exists)
- `~/.workbuddy/workbuddy.db-shm` → `workbuddy.db-shm.bak` (if exists)

### 5. Update the Database

```python
conn.execute('UPDATE sessions SET user_id = ? WHERE user_id = ?', (NEW_UID, OLD_UID))
conn.commit()
```

### 6. Update app/sessions.json

```python
import json
with open(sessions_json_path, 'r') as f:
    data = json.load(f)
for s in data.get('sessions', []):
    if s.get('userId') == OLD_UID:
        s['userId'] = NEW_UID
with open(sessions_json_path, 'w') as f:
    json.dump(data, f, indent=2)
```

### 7. Verify

Query `SELECT COUNT(*) FROM sessions WHERE user_id = ?` for both old and new IDs to confirm the old ID has 0 remaining and the new ID count has increased by the expected number.

### 8. Tell the User

- How many sessions were merged
- Where the backup files are located
- Suggest restarting WorkBuddy if the session list doesn't refresh automatically

## Important Notes

- The actual conversation message data is stored in JSONL files under `~/.workbuddy/projects/<workspace-path-hash>/<session-id>.jsonl`. These files do **not** contain user_id — they are keyed by session ID only, so they don't need to be modified.
- The `traces/` directory contains telemetry data also keyed by PID, not user_id — no changes needed there.
- If the user has used more than 2 accounts, repeat the process for each extra user_id, or ask the user which ones to merge.
- Never delete old user data. Only update the `user_id` field. The old account's server-side data is unaffected — this is a local-only operation.
