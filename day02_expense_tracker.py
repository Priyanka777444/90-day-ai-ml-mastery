"""
Expense tracker by priyanka
Let's do it
"""
import csv 
import datetime


today = datetime.date.today()
name = input("Enter your Sweet name here :")
storage = []
#category foe expense
Categories = ["Food", "Enterntainment","Travelling","Bills","Shopping","Other"]
def Add_Paise():
    global storage
    print(f"\n Categories: {Categories}")

    while True:

    #show cat
        cat = input(f"{name} Select a category: ")
        if cat in Categories:
            break
        else:
            print(f"{name}, Please choose from this {Categories}") 
            bol = input(f"{name}, Do you want to add new Category yes or no: ").capitalize()
            if bol == 'yes':
                dijiye = input("Give me new category: ")
                Categories.append(dijiye)
            elif bol == 'no':
                print("Type done to end ")
            else:
                return
            
    while True:
        description = input("Description for this: ").strip()
        if len(description) == 0:
            print("Description is mandatory")
        else:
            break
    
    while True:
        Paise = input("Add your expense here: ")

        #money telling
        try:
            value = int(Paise)
            if value <= 0:
                print(f"{name} Expenses should be positive") 
            else:                    
                break
        except ValueError:
            print(f"{name} It is a invalid input, please provide postive number for money addition")
    new_paise = {
                    'Date' : today,
                    'Category' : cat,
                    'Amount' : value,
                    'Description' : description
                }
    storage.append(new_paise)
    print(f"\nExpense Added:  {cat} - ₹{value}")

def view_all():
    if len(storage) ==0:
        print("No Expense!!")
        return
    print(f"All of you are expenses")
    print("Date  |  Category | Amount | Description ")
    print("-"*50)

    for i, expense in enumerate(storage,1):
        print(f"{i} | {expense['Date']} | {expense['Category']: < 12} | {expense['Amount']} | {expense['Description']: <6}")
    
    print(f"\n Total : {len(storage)} expense(s)")    

def view_by_cat():
    #which cat user select
    which_cat = input("Which Category expense you want to see: ").capitalize()
    
    if which_cat not in Categories:
        print(f"Invalid Category choose from {Categories} or may be you want to add new category then refer to option 1")
        return
    
    #filt
    filt = []
    for expense in storage:
        if expense['Category'] == which_cat:
            filt.append(expense)

    if len(filt)==0:
        print(f"No expense in {which_cat}")
        return
    
    print(f"\n--- {which_cat.upper()} EXPENSES ---")
    total = 0
    for expense in filt:
        print(f"{expense['Date']} | ₹{expense['Amount']} | {expense['Description']}")
        total += expense['Amount']
    
    print(f"\nCategory Total: ₹{total}")

 
    
def Total():
    if len(storage) == 0:
        print("No expense here!")
        return
    
    total = 0
    for expense in storage:
        total += expense['Amount']

    print(f"{name} your total amount is {total}")

def delete():
    if len(storage) == 0:
        print("No expense to delete")
        return
    print("Select from this: ")
    view_all()

    while True:
        try:
            remove = int(input("Which expense you want to remove enter the id or enter 0 to cancel: "))
            break
        except ValueError:
            print("Enter valide number")


    if remove == 0:
        return
    if remove < 1 or remove> len(storage):
        print("Invalid input it is not present")
        return
    removed = storage.pop(remove - 1)
    print(f"Deleted : {removed['Category']} {removed['Amount']} Successfully")

def save_exit():
    global storage

    if len(storage) == 0:
        print("No expense to save here!")
        return
    
    filename = 'expense.csv'
    keys = ["Date", "Category", "Amount","Description"]

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames = keys)
        writer.writeheader()
        writer.writerows(storage)

    print(f"{name} , Expenses saved to this file {filename}")
    print("Well Done all of you expenses are saved successfully\n Hope you enjoyed , Have a nice day bye!!;)")

    exit()

def main():
    """Main program loop"""
    print(f"{name} , Welcome to Expense Tracker!\n Wish you great experience here.")
    
    while True:
        # Show menu
        print("\n1. Add Expense")
        print("2. View All")
        print("3. View by Category")
        print("4. Total Spent")
        print("5. Delete Expense")
        print("6. Save & Exit")
        
        # Get choice
        choice = input("\nEnter choice (1-6): ")
        
        # Handle choice
        if choice == "1":
            Add_Paise()
        elif choice == "2":
            view_all()
        elif choice == "3":
            view_by_cat()
        elif choice == "4":
            Total()
        elif choice == "5":
            delete()
        elif choice == "6":
            save_exit()
            break
        else:
            print("Invalid choice! Enter 1-6.")


main()