cursor = None
connection = None

def displayPenalty(table):
    """
    Writes out all the penalties the user has that are unpaid
    """
    if len(table) == 0: # No penalties for this user.
        return False # False means that the majority of the payPenalty function will not run.
    else:
        for row in table:
            print("PENALTY:")
            print("Book = " + row[0] + "\nPenalty ID = " + str(row[1]) + "\nPenalty Amount = $" + str(row[2]))
            if row[3] == None:
                print("Amount Paid Thus Far = $0")
            else:
                print("Amount Paid Thus Far = $" + str(row[3]))
            print()
    return True

def payPenalty(conn, user):
    """
    Updates database should the user decide to pay a penalty
    """
    global cursor, connection
    connection = conn
    cursor = conn.cursor()

    while True:
        cursor.execute("""
            SELECT books.title, penalties.pid, penalties.amount, penalties.paid_amount
            FROM members, borrowings, books, penalties
            WHERE members.email =:email
            AND members.email = borrowings.member
            AND borrowings.bid = penalties.bid
            AND borrowings.book_id = books.book_id
            AND ((penalties.paid_amount IS NULL) OR ((penalties.amount - penalties.paid_amount) > 0));
            """,
            {"email":user})
        connection.commit()
        table = cursor.fetchall()
        if displayPenalty(table): # Display will be printed out here, or it will be False if there is nothing to be displayed.
            proper_number = False # PID has to be an int.
            while not proper_number:
                try:
                    penalty = int(input("Select a penalty to pay ('Penalty ID'): "))
                    payment = int(input("How much will you be paying today?: $"))
                    # If either are not numbers, the except statement will run.
                    proper_number = True
                except:
                    proper_number = False
                    print("Invalid input.")
                    print('Hit enter to try again, or type "b" or "back" to return home')
                    decision = input("")
                    if (decision.lower() == 'b') or (decision.lower() == 'back'):
                        return 
            for i in range(len(table)):
                if table[i][1] == penalty: # Table is looped through until the chosen penalty is found.
                    if table[i][3] == None: # No payments have been made yet.
                        new_paid_amount = payment
                    else: # Some payment has already been made. 
                        new_paid_amount = table[i][3] + payment
                    if new_paid_amount > table[i][2]: # We don't let the user enter an amount more than what is due.
                        print("Amount trying to pay exceeds penality cost!\nPayment unsuccessful.")
                    else:
                        cursor.execute("""
                            UPDATE penalties
                            SET paid_amount =:payment
                            WHERE pid =:PID
                            """,
                            {"payment":new_paid_amount, "PID":penalty})
                        connection.commit()
                        print("Payment successful!")
                    break
            else:
                print("ID could not be found")
            print('Hit enter to return home, or type "p" or "pay" to pay another penalty')
            decision = input("")
            if (decision.lower() != 'p') and (decision.lower() != 'pay'):
                return # Don't need to return anything, the database is already updated, just end the function.
        else:
            print("You have no penalties!")
            return