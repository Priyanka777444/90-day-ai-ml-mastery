"""
Build by Priyanka
This is calculator with error handling 

"""
name = input("Can you tell me your name please: ")
def Calculator():
    print(f"{name} Welcome to this fantastic calc")

    while True:

        #user input for first number 
        while True:
            try:
                a = int(input("Enter the value of first number: "))
                break
            except ValueError:
                print("Invalid input! Please enter a number.")

        #operators
        operators = ['+', '-', '*', '/', '%']
        while True:
            c = input("Enter operation: (+, -, *, /, %): ")
            if c in operators:
                break
            else:
                print(f"Wrong input, Use from this instead: {operators}")
        #second input 
        while True:
            try:
                b = int(input("Enter the value of second number: "))
                break
            except ValueError:
                print("Invalid input! Please enter a number.")
            

            
        #Calculator Add,Sub,Div,Multiply,mod
        if c == "+":
            print(f'Addition : {int(a+b)}')
        elif c == "-":
            print(f'Subtraction : {int(a-b)}')
        elif c == "*":
            print(f'Multiplication : {int(a*b)}')
        elif c == "%":
            if b == 0:
                print(f'Wrong Input , Zero ')
            else:
                print(f'Modular : {int(a%b)}')
        else:
            if b == 0:
                print(f'Wrong Input , Zero ')
            else:
                print(f'Divivsion : {a/b}')

        #wanna continue
        while True:
            phirse = input("Do you want to do another Calculation yes or no: ").lower()
                
            if phirse == 'yes':
                break
            elif phirse == 'no':
                print(f"Bye {name} have a nice day!!!")
                return 
            else:
                print("Please type yes or no")

        
Calculator()
