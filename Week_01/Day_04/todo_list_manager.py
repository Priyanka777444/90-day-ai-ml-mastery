"""
To do list by Priyanka
for Priyanka
"""
import sqlite3
from datetime import datetime, date


DB = 'todo.db'

def init_db():
    """Create db and table if they don't exits"""

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT NOT NULL,
                   description TEXT,
                   priority TEXT NOT NULL,
                   status TEXT NOT NULL,
                   due_date TEXT,
                   created_at TEXT NOT NULL,
                   completed_at TEXT 
        )
''')
    conn.commit()
    conn.close()
    print("Database initialized")
    
    

def add_task():
    global DB

    #title for task
    while True:
        
        title = str(input("What do you want to add today: "))
        if len(title)>0:
            break
        print("Title Cannot be empty!!")
    
    #description of it
    while True:
        
        description = str(input("Description for this task:  "))
        if len(description)>0:
            break
        print("Give valid Description !")
    
    #priority number
    while True:
        
        prio = input("What is the priority of this task (High/Medium/Low): ").lower()
        if prio in ['High', 'Medium','Low']:
            break
        
        print("Invalid input , Chosse from  ['High', 'Medium','Low']: ")
    
    #status how much done 
    status = "Pending"

    
    #date you want to complete it
    while True:
        due = input("Due date (YYYY-MM-DD) or press Enter to skip: ").strip()
    
        # Allow skipping
        if len(due) == 0:
           due = None
           break
    
        # Validate date format
        try:
           datetime.strptime(due, '%Y-%m-%d')
           break
        except ValueError:
           print("Invalid date format! Use YYYY-MM-DD (e.g., 2024-01-20)")


    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO tasks (title, description, priority, status, due_date, created_at, completed_at)
    VALUES (?,?,?,?,?,?,?)
    ''', (title,description,prio,status,due,str(datetime.now()), None))
    
    conn.commit()
    conn.close()

    print("Task added Successfully")


def view_all():

    try:

        conn = sqlite3.connect(DB)
        cursor = conn.cursor()

        cursor.execute('SELECT*FROM tasks ORDER BY id ASC')

        # Fetch all the results
        tasks = cursor.fetchall()

        if not tasks:
            print("The query returned no results (the list is empty).")
        
        print("\n--- ALL TASKS ---")
        print("ID | Title             |Description     | Priority | Status    | Due Date | Created_at  | Completed_at")
        print("-" * 70)

        for task in tasks:
            tasks_id = task[0]
            title = task[1][:20]  # Limit to 20 characters
            priority = task[3]
            status = task[4]
            due_date = task[5] if task[5] else "No due date"
        
            print(f"{tasks_id:<2} | {title:<20} | {priority:<8} | {status:<9} | {due_date}")
    
        print(f"\nTotal: {len(tasks)} task(s)")
        
    except sqlite3.Error as e:
        print(f"A database error occurred: {e}")
    finally:
        # Close the connection
        if conn:
            conn.close()

def view_by_status():
    """View by status"""
    print("\n1. Pending")
    print("2. Complete")

    decide = int(input("\nSelect status (1-2): "))

    if decide == 1:
        status = "Pending"
    elif decide == 2:
        status = "Complete"
    else:
        print("Invalid Input !")
        return
    
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute('SELECT*FROM tasks WHERE status =?', (status, ))
    tasks = cursor.fetchall()

    conn.close()

     # Display results
    if len(tasks) == 0:
        print(f"\nNo {status.lower()} tasks!")
        return
    
    print(f"\n--- {status.upper()} TASKS ---")
    print("ID | Title                | Status | Due Date")
    print("-" * 60)
    
    for task in tasks:
        task_id = task[0]
        title = task[1][:20]
        priority = task[3]
        due_date = task[5] if task[5] else "No due date"
        
        print(f"{task_id:<2} | {title:<20} | {status:<9} | {due_date}")
    
    print(f"\nTotal: {len(tasks)} task(s)")


def view_by_prio():
    """View by priority"""
    
    print("1. High")
    print("2. Medium")
    print("3. Low")

    whi = int(input("\n Select between these 3 (High ->1, Medium ->2, Low ->3): "))

    if whi == 1:
        prio = "High"
    elif whi == 2:
        prio = "Medium"
    elif whi == 3:
        prio = "Low"
    else:
        print("Invalid input, choose from high , medium , low: ")
        return 

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()


    cursor.execute('SELECT*FROM tasks WHERE priority =?', (prio, ))
    tasks = cursor.fetchall()

    conn.close()

    # Display results
    if len(tasks) == 0:
        print(f"\nNo {prio.lower()} tasks!")
        return
    
    print(f"\n--- {prio.upper()} TASKS ---")
    print("ID | Title                | Priority | Due Date")
    print("-" * 60)
    
    for task in tasks:
        task_id = task[0]
        title = task[1][:20]
        priority = task[3]
        due_date = task[5] if task[5] else "No due date"
        
        print(f"{task_id:<2} | {title:<20} | {priority:<8} | {due_date}")
    
    print(f"\nTotal: {len(tasks)} task(s)")

def mark():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute('SELECT*FROM tasks WHERE status ="Pending"')
    tasks = cursor.fetchall()

    if len(tasks) == 0:
        print("\nNo pending tasks!")
        conn.close()
        return
    while True:
        try:

            id = input("Which task you want to mark , give me the id(0 to cancel): ")
            break
        except ValueError:
            print("Enter valid number!")
            
    if id == 0:
        conn.close()
        return

    cursor.execute('SELECT*FROM tasks WHERE id = ?', (id,))
    task = cursor.fetchone()

    if not task:
        print("Task not found!")
        conn.close()
        return
    
    if task[4] == "Complete":
        print("Task is already complete!")
        conn.close()
        return
    
    cursor.execute('''
        UPDATE tasks 
        SET status = ?, completed_at = ?
        WHERE id = ?
    ''', ("Complete", str(datetime.now()), id))

    conn.commit()
    conn.close()
    print(f"Task with ID {task[1]} updated to status: Completed")


def update():
    """Updating the data"""

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    # Show all tasks
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()

    if len(tasks) == 0:
        print("\nNo tasks to update!")
        conn.close()
        return
    
    print("\n--- ALL TASKS ---")
    for task in tasks:
        print(f"{task[0]}. {task[1]} - {task[4]}")

    while True:
        try:

            id = int(input("Which task you want to Update , give me the id(0 to cancel): "))
            break
        except ValueError:
            print("Enter valid number!")

    if id == 0:
        conn.close()
        return
        
    cursor.execute('SELECT*FROM tasks WHERE id = ?', (id,))
    task = cursor.fetchone()

    if not task:
        print("ID not found!")
        conn.close()
        return
        
    # Show what can be updated
    print(f"\nCurrent task: {task[1]}")
    print("What do you want to update?")
    print("1. Title")
    print("2. Description")
    print("3. Priority")
    print("4. Due Date")

    choice = input("\nEnter choice (1-4): ")

    if choice == "1":
        new_title = input("New title: ").strip()
        if len(new_title) > 0:
            cursor.execute('UPDATE tasks SET title = ? WHERE id = ?', (new_title, id))
            print("Title updated!")
    
    elif choice == "2":
        new_desc = input("New description: ").strip()
        cursor.execute('UPDATE tasks SET description = ? WHERE id = ?', (new_desc,id))
        print("Description updated!")
    
    elif choice == "3":
        while True:
            new_priority = input("New priority (High/Medium/Low): ").capitalize()
            if new_priority in ['High', 'Medium', 'Low']:
                cursor.execute('UPDATE tasks SET priority = ? WHERE id = ?', (new_priority,id))
                print("Priority updated!")
                break
            print("Invalid priority!")
    
    elif choice == "4":
        while True:
            new_due = input("New due date (YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(new_due, '%Y-%m-%d')
                cursor.execute('UPDATE tasks SET due_date = ? WHERE id = ?', (new_due, id))
                print("Due date updated!")
                break
            except ValueError:
                print("Invalid date format!")
    
    else:
        print("Invalid choice!")
    
    conn.commit()
    conn.close()


def delete():
    """Delete a task"""

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()


    # Show all tasks
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()

    if len(tasks) == 0:
        print("\nNo tasks to delete!")
        conn.close()
        return
    
    print("\n--- ALL TASKS ---")
    for task in tasks:
        print(f"{task[0]}. {task[1]} - {task[4]}")
    
    while True:
        try:

            id = int(input("Which id you want to delete and type 0 to cancel: "))
            break
        except ValueError:
            print("Invalid id !, enter valid number")
        
    if id == 0:
        conn.close()
        return
        
    #Check if task exists
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (id,))
    task = cursor.fetchone()

    if not task:
        print("Task not found!")
        conn.close()
        return
    # Confirm deletion
    confirm = input(f"Do you want to delete: '{task[1]}'? (y/n): ").lower()
    
    if confirm == 'y':
        cursor.execute('DELETE FROM tasks WHERE id = ?', (id,))
        conn.commit()
        print(f"\n Task '{task[1]}' deleted!")
    else:
        print("Deletion cancelled.")
    
    conn.close()
  

def main():
    init_db()
    
    print("Welcome to To-Do List Manager by Priyanka!")
    
    while True:
        print("\n1. Add Task")
        print("2. View All Tasks")
        print("3. View by Status")
        print("4. View by Priority")
        print("5. Mark Complete")
        print("6. Update Task")
        print("7. Delete Task")
        print("8. Exit")
        
        choice = input("\nEnter choice (1-8): ")
        
        if choice == "1":
            add_task()
        elif choice == "2":
            view_all()
        elif choice == "3":
            view_by_status()
        elif choice == "4":
            view_by_prio()
        elif choice == "5":
            mark()
        elif choice == "6":
            update()
        elif choice == "7":
            delete()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

main()