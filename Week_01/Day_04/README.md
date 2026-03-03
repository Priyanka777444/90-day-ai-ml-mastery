# Day 4: To-Do List Manager with SQLite Database

## Features
1. ✅ Add tasks (title, description, priority, due date)
2. ✅ View all tasks (formatted table)
3. ✅ View by status (Pending/Complete)
4. ✅ View by priority (High/Medium/Low)
5. ✅ Mark task complete (with timestamp)
6. ✅ Update task (title/description/priority/due date)
7. ✅ Delete task (with confirmation)
8. ✅ Data persistence (SQLite database)

## Database Schema
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    priority TEXT NOT NULL,
    status TEXT NOT NULL,
    due_date TEXT,
    created_at TEXT NOT NULL,
    completed_at TEXT
)