"""
Password for you by Priyanka
"""
import random
import string
import csv
from datetime import date

#global storage
password = []

#password generator

def generate_password():

    global password

    print("This is a password generator")
    pool = ""
    pool += string.ascii_lowercase

    while True:
        try:
            leng = int(input("Tell me the length of password you want to generate (8-32): "))
            if leng<8 or leng>32:
                print("Pick number between 8-32")
            else:
                break
        except ValueError:
            print("Invalid Input Enter a number!") 
            
        
    while True:
        
        upper = input("Do you want upperclass in password (y-> yes/n->no): ").lower()
        
        if upper in ['y', 'n']:
            break
        print("Enter 'y' or 'n': ")

    if upper == 'y':
        pool += string.ascii_uppercase


    while True:
        sym = input("Do you want Symbols in password (y-> yes/n->no): ").lower()
        
        if sym in ['y', 'n']:
            break
        print("Enter 'y' or 'n' for symbols in password: ")

    if sym == 'y':
        pool += string.punctuation

    while True:
        num = input("Do you numbers in you password (yes -> y/no->n): ")
        if num in ['y','n']:
            break
        print("Enter y for yes and n for no: ")

    if num == 'y':
        pool += string.digits
            

    gen =''.join(random.choices(pool, k=leng))
    print(f"Password Generated: {gen}")
    
    w_save = input("Do you want to save this password y/n: ").lower()
    if w_save == 'y':
        label = input("Label (eg email, locker, photo, gate: )").strip()

        new_pa = {
            'label' : label,
            'password' : gen,
            'created' : str(date.today())
        }

        password.append(new_pa)
        print(f"Saved as '{label}'")
        

def save_manual():
    """
    Manually save the password
    """

    global password
        
    label = input("label : ").strip()
    pwd = input("password: ").strip()

    if len(label) ==0 or len(pwd) == 0:
        print("Label and password cannot be empty: ")
        return

    new_pa = {
            'label' : label,
            'password' : pwd,
            'created' : str(date.today())
        }

    password.append(new_pa)
    print(f"Saved Password for {label}: ")


def save_file():
    """Save all passwords to one CSV file"""
    global password
    
    if len(password) == 0:
        print("Password is empty ")
        return
    
    filename = 'password.csv'
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['label', 'password', 'created'])
        writer.writeheader()
        writer.writerows(password)  
    
    print(f"All passwords saved to {filename}")

def view_all():
    if len(password) == 0:
        print("\nNo password saved yet!")
        return
    print("\n--- ALL PASSWORDS ---")
    print("ID | label          | password            | created")
    print("-" * 65)

    for i, pwd in enumerate(password, 1):
        print(f"{i:<2} | {pwd['label']:<14} | {pwd['password']:<18} | {pwd['created']}")
    
    print(f"\nTotal: {len(password)} password(s)")


def search():
    global password

    if len(password) == 0:
        print("No Password to search")
        return
    
    search_i = input("Search Label is : ").strip().lower()

    mila = None
    for p in password:
        if p['label'].lower() == search_i:
            mila = p
            break
    if mila:
        print("Found")
        print(f"label: {mila['label']}")
        print(f"password: {mila['password']}")
        print(f"created: {mila['created']}")
    else:
        print(f"No Password found for {search_i}")

def delete():
    if len(password) == 0:
        print("\nNo password to delete!")
        return
    
    view_all()
    
    while True:
        try:
            del_id = int(input("\nEnter ID to delete (0 to cancel): "))
            break
        except ValueError:
            print("Enter a valid number!")
    
    if del_id == 0:
        return
    
    if del_id < 1 or del_id > len(password):
        print("Invalid ID!")
        return
    
    removed = password.pop(del_id - 1)
    print(f"\n✅ Deleted password for: {removed['label']}")

def load_password():
    """Load passwords from CSV"""
    global password
    
    try:
        with open('password.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            password = list(reader)
        print(f"Loaded {len(password)} password(s)")
    except FileNotFoundError:
        print("No saved password found. Starting fresh!")

def main():
    load_password()  # Load saved password
    
    print("Welcome to Password Manager by Priyanka!")
    
    while True:
        print("\n1. Generate Password")
        print("2. Save Password (Manual)")
        print("3. View All Password")
        print("4. Search Password")
        print("5. Delete Password")
        print("6. Save & Exit")
        
        choice = input("\nEnter choice (1-6): ")
        
        if choice == "1":
            generate_password()
        elif choice == "2":
            save_manual()
        elif choice == "3":
            view_all()
        elif choice == "4":
            search()
        elif choice == "5":
            delete()
        elif choice == "6":
            save_file()
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

main()



    