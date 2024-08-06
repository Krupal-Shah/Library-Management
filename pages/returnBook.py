import pages.util as util

connection=None
cursor=None

def returnABook(conn, userEmail): 
    global connection, cursor
    connection=conn
    cursor=connection.cursor()

    inMenu=True
    while inMenu:   # Loop menu so user can use it multiple times
        cursor.execute("""
                SELECT b.bid AS Borrow_ID, 
                       bk.title AS Title, 
                       b.start_date AS CheckOut, 
                       DATETIME(strftime('%s', b.start_date)+strftime('%s', '1970-01-21'), 'unixepoch') AS DateDue
                FROM borrowings b, books bk, members m
                WHERE b.member LIKE :member AND 
                       bk.book_id=b.book_id AND 
                       b.member=m.email AND 
                       b.end_date IS NULL;
                """, {"member":userEmail})
        connection.commit()
        rows=cursor.fetchall()  # Get all the info needed for the current borrowings
        print()
        print("Here are the books currently borrowed: ")
        if len(rows) == 0:      # If there are no borrowings
            print("No books currently borrowed")
            input("Hit enter to return to main menu")
            return 0
        
        util.displayRows(rows, ("Borrow ID", "Book Title", "Start Date", "Return Date")) # display the results

        print("1.Return a book")
        print("2.Go back")
        choice=input("Please select an option: ")

        if choice=='1': # Return a book
            for i in range(len(rows)): # Print out borrowings that can be returned
                print(f"Input {i+1} to return borrowing of {rows[i][1]}") # Input # to return borrowing of Book 1, Book 2, etc.
            print("Input N to return to previous menu")
            bookReturnChoice=input("Please select an option: ")

            if bookReturnChoice.isdigit() and int(bookReturnChoice) < len(rows)+1: # If a book was chosen to be returned
                bookReturn=rows[int(bookReturnChoice)-1][0] # Store the bid of the individual
            
                # Return book by adding an end date to the borrowing
                cursor.execute("""
                    UPDATE borrowings SET end_date=DATE('now')
                    WHERE member=:member AND bid=:inputID;
                               """, {"member":userEmail, "inputID":bookReturn}) 
                connection.commit()

                # Get the latest penalty id and add 1 to it for a unique pid
                cursor.execute("SELECT pid FROM penalties ORDER BY pid DESC") 
                connection.commit()
                newPenalty=int(cursor.fetchall()[0][0])+1

                 # Calculate the time the book has been borrowed
                cursor.execute("SELECT ifnull(julianday(end_date) - julianday(start_date), 0) FROM borrowings;")
                connection.commit()
                updatedAmount=cursor.fetchall()[bookReturn-1][0]

                # Check if the book is over due, and apply penalty
                if updatedAmount>20: 
                    cursor.execute("""
                            INSERT INTO penalties (pid, bid, amount, paid_amount) 
                            VALUES (:newPid, :chosenBookId, :newAmount, NULL)
                                """, {"newPid":str(newPenalty), "chosenBookId":bookReturn, "newAmount":updatedAmount-20}) # Add a new penalty for the returned book
                    connection.commit()
                
                addReview=""
                while addReview=="": # make sure the user inputs a valid choice
                    for i in range(len(rows)):
                        if bookReturn==rows[i][0]:
                            bookData=rows[i][1] # get the title of the book

                    print(f"Would you like to give {bookData} a review? (Y/n)")
                    addReview=input(">")

                    if addReview.lower()!="y" and addReview.lower()!="n": # Check if valid choice
                        print("Invalid Input")
                        addReview=""

                if addReview.lower()=='y': # Write a review 
                    # If a book was chosen to be reviewed
                    print(f"Input review of {bookData}:") # Prompt for review with book title(ie. Book 1)
                    reviewText=input(">") # Input review text

                    reviewRating=0
                    while reviewRating==0: # Make sure the input is valid
                        print(f"Input rating(1-5) of {bookData}:") # prompt for review rating with book title
                        reviewRating=input(">") # Input review rating

                        if reviewRating.isdigit() and int(reviewRating)<6 and int(reviewRating)>0: # check if choice is a valid review digit
                            reviewRating=int(reviewRating)
                        else:
                            print("Invalid input")
                            reviewRating=0

                    cursor.execute("""
                        SELECT r.rid
                        FROM reviews r
                        ORDER BY r.rid DESC;
                    """)
                    connection.commit()
                    newRid=int(cursor.fetchall()[0][0])+1 #Generate a new rid

                    cursor.execute("""
                        SELECT DISTINCT bk.book_id
                        FROM borrowings b, books bk, members m
                        WHERE b.member LIKE :member AND 
                              bk.book_id=b.book_id AND 
                              b.member=m.email AND 
                              bk.title=:chosenBook;
                    """, {"member":userEmail, "chosenBook":bookData})
                    connection.commit()
                    chosenBookId=cursor.fetchall()[0][0]#Get the book id of the chosen book

                    cursor.execute("""
                        INSERT INTO reviews (rid, book_id, member, rating, rtext, rdate)
                        VALUES (:reviewID, :bookID, :user, :score, :reviewWriting, DATETIME('now', 'localtime'))
                    """, {"reviewID":str(newRid), "bookID":chosenBookId, "user":userEmail, "score":reviewRating, "reviewWriting":reviewText}) #create new review in reviews table
                    connection.commit()
            elif bookReturnChoice.lower()=="n": #Return to main menu
                choice=0
            else: # If an invalid choice is made when choosing a book to return 
                print("Invalid input")

        elif choice=='2': # Leave the return file
            inMenu=False
        else:
            print("Not a valid choice")
            
    return 1