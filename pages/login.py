import getpass

cursor = None
connection = None

def screen():
    """
    The intial text that will appear once database is open
    """
    print("Welcome to the Library Management System!")
    print("Already have an account? Hit enter to proceed to login")
    print('New library member? Type "y" or "yes" to create your new account')
    decision = input("")
    if (decision.lower() == 'y') or (decision.lower() == 'yes'):
        return False
    elif decision == 'exit':
        return decision # Backout for testing purposes
    else:
        return True

def register(conn):
    """
    If the user does not already have an account, this function will be called to add their information to the database.
    """
    global cursor, connection
    connection = conn
    cursor = conn.cursor()

    print("To sign-up, please enter all the following information:")
    while True: # This loop will repeat until a proper email address that isn't already in the system is chosen.
        user = input("Email address (required): ")
        cursor.execute("SELECT * FROM members WHERE email =:email", {"email":user})
        connection.commit()
        if cursor.fetchone() is not None: # Meaning an account was found that has the chosen email address.
            print('An account with this email address already exists!\nReturn to home screen by typing "b" or "back" or hit enter to use a different email')
            decision = input("")
            if (decision.lower() == 'b') or (decision.lower() == 'back'):
                return False # Returning false sends the user back to the login screen.
        #elif len(user) == 0:
        elif ("@" not in user): # Ensuring a proper email address is entered.
            print('A proper email address is required!\nHit enter to try again, or return to home screen by typing "b" or "back"')
            decision = input("")
            if (decision.lower() == 'b') or (decision.lower() == 'back'):
                return False
        else:
            break # Loop breaks if no problems are encountered.
    while True:
        client = input("Name (required): ")
        if (len(client) == 0) or (client.isspace()): # We don't want their name to be empty or just a bunch of spaces.
            print('You must enter your name!\nHit enter to try again, or return to home screen by typing "b" or "back"')
            decision = input("")
            if (decision.lower() == 'b') or (decision.lower() == 'back'):
                return False
        else:
            break
    proper_input = False # Input for birth year should only be a number, or nothing if they want to skip it. 
    while not proper_input:
        try:
            DOB = input("Birth year (optional, hit enter to skip): ")
            if len(DOB) == 0: # If name is nothing, skip it by giving it a None value.
                DOB = None
            else:
                DOB = int(DOB) # Error will occur here if it is not a number, triggering the except statement.
            proper_input = True
        except:
            proper_input = False
            print("Invalid input for birth year, please try again.")
    nFaculty = input("Faculty name (optional, hit enter to skip): ")
    if len(nFaculty) == 0:
        nFaculty = None
    while True:
        password = getpass.getpass("Please choose a password (required): ") # getpass.getpass hides what the user is typing.
        if (len(password) == 0):
            print("You must choose a password!")
            continue
        elif password.isspace():
            print("Your password must contain at least 1 non-whitespace character!")
            continue
        confirmation = getpass.getpass("Confirm your password: ")
        if password == confirmation:
            break # Ends if password is valid, and correctly inputted twice.
        else:
            print("Passwords do not match. Please try again.")
    # Insert new account into 'members' table:
    cursor.execute("INSERT INTO members VALUES (:email, :passwd, :name, :byear, :faculty)", {"email":user, "passwd":password, "name":client, "byear":DOB, "faculty":nFaculty})
    connection.commit()
    return user

def login(conn, user, password):
    """
    Returns the user who is accessing the database if they enter their email and password correctly.
    """
    global cursor, connection
    connection = conn
    cursor = conn.cursor()
    # This format prevents SQL injection:
    cursor.execute("SELECT email, name FROM members WHERE email LIKE :email AND passwd =:passwd", {"email":user, "passwd":password}) # Use LIKE (without '%' signs) to make entered email case insensitive.
    connection.commit()
    name = cursor.fetchone() # The way the login process is structured means that only 1 result can come up for any email.
    if name is not None: 
        print("Welcome " + name[1].title() + "!")
        return name[0] # We return the email address stored in the database, not the one manually entered, so that all subsequent functions dont have to worry about case sensitivity.
    else:
        print('Login failed. Hit enter to try again, or return to home screen by typing "b" or "back"')
        decision = input("")
        if (decision.lower() == 'b') or (decision.lower() == 'back'):
            return 2
        return 1