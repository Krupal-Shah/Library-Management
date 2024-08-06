### Importing the required modules and functions ###
import pages.init as init
import pages.login as login
import pages.member as member
import pages.penalty as penalty
import pages.returnBook as returnBook
import pages.search as search
import sqlite3
import os
import getpass

### Creating the connection with database ###
connection = None
cursor = None

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    connection.commit()
    return

### Main ###
def main():
    # Connect to the database
    global connection, cursor

    if connection is None:
        path = input("Please enter database file path: ")
        print()
        if not os.path.isfile(path):
            print("The database file does not exist. Exiting the program.")
            return
        else:
            connect(path)
    
    # Check if data is available in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    connection.commit()
    if cursor.fetchall() == []:
        init.initial(dummy=False)   # Make True for test purposes.
        
    # Login
    loggedIn = False
    while not loggedIn:
        while not loggedIn:
            start = login.screen() # Returns true if they are logging in, false if they are registering.
            if start == 'exit':
                return # Backout for testing purposes
            if not start:
                user = login.register(connection)
                if user:
                    loggedIn = True
            else:
                while True:
                    user = input("Please enter your email address: ")
                    password = getpass.getpass("Please enter your password: ")
                    print()
                    user = login.login(connection, user, password)
                    if user == 2: # 2 means the user wants to return to home screen.
                        break
                    elif user != 1: # 1 means the user is going to try logging in again, so this loop repeats. Otherwise user is the successfully logged in username.
                        loggedIn = True
                        break
        
        # Main Loop
        while True:
            print("What would you like to do?")
            print("1. Display member profile")
            print("2. Return a book")
            print("3. Search for a book")
            print("4. Pay a penalty")
            print("5. Logout")
            print("6. Exit")
            choice = input("Enter the number of the action you would like to perform: ")
            print()
            
            if choice == "1":
                member.member_info(user)
                print()
            elif choice == "2":
                returnBook.returnABook(connection, user)
                print()
            elif choice == "3":
                search.search(connection, user)                
                print()
            elif choice == "4":
                penalty.payPenalty(connection, user)
                print()
            elif choice == "5":
                print("Logging out...")
                loggedIn = False
                break
            elif choice == "6":
                print('Exiting the program...')
                loggedIn = True
                break
            else:
                print("Invalid choice. Please try again.")

    # Close the connection to the database
    if connection is not None:
        connection.close()
    return

if __name__ == "__main__":
    main()