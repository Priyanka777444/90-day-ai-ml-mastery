"""
Database setup and operations
Updated: Added ia_id column to books for Internet Archive reading links
         Added delete_book function
"""
import sqlite3
from datetime import datetime

DB_NAME = 'mylife.db'

def _get_conn():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    conn = _get_conn()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        account_name TEXT NOT NULL,
        bank_name TEXT NOT NULL,
        account_type TEXT NOT NULL,
        balance REAL NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL,
        UNIQUE(user_id, account_name))''')

    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        date TEXT NOT NULL,
        account_id INTEGER,
        created_at TEXT NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS income (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        source TEXT NOT NULL,
        description TEXT,
        date TEXT NOT NULL,
        account_id INTEGER,
        created_at TEXT NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS transfers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        from_account_id INTEGER NOT NULL,
        to_account_id INTEGER NOT NULL,
        description TEXT,
        date TEXT NOT NULL,
        created_at TEXT NOT NULL)''')
    
    c.execute("""CREATE TABLE IF NOT EXISTS monthly_budget (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            month TEXT NOT NULL,          -- format: YYYY-MM
            budget REAL NOT NULL,
            UNIQUE(user_id, month))""")
    

    # Books — 12 columns
    # id | user_id | book_id | title | author | cover_url | shelf
    # | pages_total | pages_read | languages | ia_id | added_at
    c.execute('''CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        book_id TEXT NOT NULL,
        title TEXT NOT NULL,
        author TEXT,
        cover_url TEXT,
        shelf TEXT NOT NULL,
        pages_total INTEGER DEFAULT 0,
        pages_read INTEGER DEFAULT 0,
        languages TEXT DEFAULT '',
        ia_id TEXT DEFAULT '',
        added_at TEXT NOT NULL)''')

    # Safe migrations for older databases
    for col, definition in [
        ("languages", "TEXT DEFAULT ''"),
        ("ia_id",     "TEXT DEFAULT ''"),
    ]:
        try:
            c.execute(f"ALTER TABLE books ADD COLUMN {col} {definition}")
            conn.commit()
        except sqlite3.OperationalError:
            pass  # already exists

    conn.commit()
    conn.close()

# ==================== ACCOUNT FUNCTIONS ====================
def add_account(user_id, name, bank, acc_type, balance=0):
    conn = _get_conn()
    conn.execute(
        "INSERT INTO accounts (user_id, account_name, bank_name, account_type, balance, created_at) VALUES (?,?,?,?,?,?)",
        (user_id, name, bank, acc_type, balance, str(datetime.now())))
    conn.commit(); conn.close()

def get_accounts(user_id):
    conn = _get_conn()
    rows = conn.execute('SELECT * FROM accounts WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()
    return [tuple(r) for r in rows]
def get_category_expense(user_id, month):
    conn = _get_conn()
    data = conn.execute('SELECT category, SUM(amount) as total FROM expenses WHERE user_id = ? AND substr(date, 1, 7) = ? GROUP BY category ORDER BY total DESC',(user_id, month)).fetchall()
    conn.close()
    return data

def get_account_balance(account_id):
    conn = _get_conn()
    res = conn.execute('SELECT balance FROM accounts WHERE id = ?', (account_id,)).fetchone()
    conn.close()
    return res[0] if res else 0

def save_monthly_budget(user_id, month, budget):
    conn = _get_conn()
    conn.execute('INSERT OR REPLACE INTO monthly_budget (user_id, month, budget) VALUES (?, ?, ?)', 
                 (user_id, month, budget))
    conn.commit()
    conn.close()

def get_monthly_budget(user_id, month):
    conn = _get_conn()
    data = conn.execute(
        'SELECT budget FROM monthly_budget WHERE user_id = ? AND month = ?', 
        (user_id, month)
    ).fetchone()
    conn.close()
    return data[0] if data else 0

def get_monthly_expense(user_id, month):
    conn = _get_conn()
    data = conn.execute('SELECT SUM(amount) FROM expenses WHERE user_id = ? AND substr(date, 1, 7) = ?', (user_id, month)).fetchone()
    conn.commit()
    conn.close()
    return data[0] if data[0] else 0

def delete_account(acc_id):
    conn = _get_conn()
    conn.execute('DELETE FROM accounts WHERE id = ?', (acc_id,))
    conn.commit(); conn.close()

# ==================== EXPENSE FUNCTIONS ====================
def add_expense(user_id, amount, category, desc, date, account_id):
    conn = _get_conn()
    conn.execute(
        "INSERT INTO expenses (user_id, amount, category, description, date, account_id, created_at) VALUES (?,?,?,?,?,?,?)",
        (user_id, amount, category, desc, date, account_id, str(datetime.now())))
    conn.execute('UPDATE accounts SET balance = balance - ? WHERE id = ?', (amount, account_id))
    conn.commit(); conn.close()

def get_expenses(user_id, account_id=None):
    """Returns: id(0) amount(1) category(2) description(3) date(4) account_name(5) bank_name(6)"""
    conn = _get_conn()
    query = """SELECT e.id, e.amount, e.category, e.description, e.date,
                      a.account_name, a.bank_name
               FROM expenses e
               JOIN accounts a ON e.account_id = a.id
               WHERE e.user_id = ?"""
    params = [user_id]
    if account_id:
        query += " AND e.account_id = ?"
        params.append(account_id)
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [tuple(r) for r in rows]

def delete_expense(expense_id):
    conn = _get_conn()
    expense = conn.execute('SELECT amount, account_id FROM expenses WHERE id = ?', (expense_id,)).fetchone()
    if expense:
        conn.execute('UPDATE accounts SET balance = balance + ? WHERE id = ?', (expense[0], expense[1]))
        conn.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
    conn.close()
    return bool(expense)

# ==================== INCOME FUNCTIONS ====================
def add_income(user_id, amount, source, desc, date, account_id):
    conn = _get_conn()
    conn.execute(
        "INSERT INTO income (user_id, amount, source, description, date, account_id, created_at) VALUES (?,?,?,?,?,?,?)",
        (user_id, amount, source, desc, date, account_id, str(datetime.now())))
    conn.execute('UPDATE accounts SET balance = balance + ? WHERE id = ?', (amount, account_id))
    conn.commit(); conn.close()

def get_income(user_id):
    conn = _get_conn()
    rows = conn.execute("""SELECT i.amount, i.source, i.description, i.date, a.account_name
                           FROM income i
                           JOIN accounts a ON i.account_id = a.id
                           WHERE i.user_id = ?""", (user_id,)).fetchall()
    conn.close()
    return [tuple(r) for r in rows]

# ==================== TRANSFER FUNCTIONS ====================
def transfer_money(user_id, amount, from_id, to_id, desc, date):
    conn = _get_conn()
    conn.execute(
        "INSERT INTO transfers (user_id, amount, from_account_id, to_account_id, description, date, created_at) VALUES (?,?,?,?,?,?,?)",
        (user_id, amount, from_id, to_id, desc, date, str(datetime.now())))
    conn.execute('UPDATE accounts SET balance = balance - ? WHERE id = ?', (amount, from_id))
    conn.execute('UPDATE accounts SET balance = balance + ? WHERE id = ?', (amount, to_id))
    conn.commit(); conn.close()

def get_transfers(user_id):
    conn = _get_conn()
    rows = conn.execute("""SELECT t.date, t.amount, f.account_name, o.account_name, t.description
                           FROM transfers t
                           JOIN accounts f ON t.from_account_id = f.id
                           JOIN accounts o ON t.to_account_id = o.id
                           WHERE t.user_id = ?""", (user_id,)).fetchall()
    conn.close()
    return [tuple(r) for r in rows]

# ==================== BOOK FUNCTIONS ====================
def add_book(user_id, book_id, title, author, cover, shelf, pages, languages="", ia_id=""):
    conn = _get_conn()
    conn.execute(
        "INSERT INTO books (user_id, book_id, title, author, cover_url, shelf, pages_total, languages, ia_id, added_at) "
        "VALUES (?,?,?,?,?,?,?,?,?,?)",
        (user_id, book_id, title, author, cover, shelf, pages, languages, ia_id or "", str(datetime.now())))
    conn.commit(); conn.close()

def get_books(user_id, shelf=None):
    """
    Always returns exactly 12 named columns:
    id(0) user_id(1) book_id(2) title(3) author(4) cover_url(5)
    shelf(6) pages_total(7) pages_read(8) languages(9) ia_id(10) added_at(11)
    """
    conn = _get_conn()
    query = """SELECT id, user_id, book_id, title, author, cover_url,
                      shelf, pages_total, pages_read,
                      COALESCE(languages, '') AS languages,
                      COALESCE(ia_id, '')     AS ia_id,
                      added_at
               FROM books WHERE user_id = ?"""
    params = [user_id]
    if shelf:
        query += " AND shelf = ?"
        params.append(shelf)
    query += " ORDER BY added_at DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [tuple(r) for r in rows]

def delete_book(book_id):
    """Delete a book from the library by its internal DB id."""
    conn = _get_conn()
    conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit(); conn.close()

def update_book_shelf(book_id, new_shelf):
    conn = _get_conn()
    conn.execute('UPDATE books SET shelf = ? WHERE id = ?', (new_shelf, book_id))
    conn.commit(); conn.close()

def update_book_progress(book_internal_id, pages_read):
    conn = _get_conn()
    conn.execute('UPDATE books SET pages_read = ? WHERE id = ?', (pages_read, book_internal_id))
    conn.commit(); conn.close()