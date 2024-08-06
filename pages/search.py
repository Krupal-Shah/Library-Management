import datetime
import pages.util as util

# Global variables
connection = None
cursor = None
user = None

# Function that queries the search results of the books
# Returns the results of the search for the parameters
# sText: The keyword to search for
# page: Which page of the search results to display
def searchResults(sText, page = 1):
    cursor.execute("""
        WITH RankedBooks AS (
            SELECT
                books.book_id as bookid,
                title,
                author,
                pyear,
                ifnull(AVG(rating), "NA") AS Rating, -- average rating of the book
                CASE
                    WHEN (books.book_id = bo.book_id AND bo.end_date IS NULL) THEN 'NO'
                    ELSE 'YES'
                END AS Available,    -- if the book is available or not
                ROW_NUMBER() OVER (
                    ORDER BY
                        CASE
                            WHEN title LIKE '%' || :keyword || '%' THEN 1   
                            ELSE 2
                        END,
                        CASE
                            WHEN title LIKE '%' || :keyword || '%' THEN title   -- ordering by title then author
                            ELSE author
                        END
                ) AS RowNum         -- create a row number for the book to allow ordering
            FROM books
            LEFT OUTER JOIN reviews ON books.book_id = reviews.book_id
            LEFT OUTER JOIN borrowings bo ON books.book_id = bo.book_id 
            WHERE books.title LIKE '%' || :keyword || '%' OR books.author LIKE '%' || :keyword || '%'
            GROUP BY books.book_id, title, author, pyear
        )
                   
        SELECT bookid, title, author, pyear, Rating, Available
            FROM RankedBooks
            WHERE RowNum > 5 * (:pagenum - 1) AND RowNum <= 5 * :pagenum;
    """, {'keyword': sText, 'pagenum': page})
    connection.commit()
    rows = cursor.fetchall()
    return rows

# Function that handles the search results
# Displays the different functions as well as which page to display
def handleSearch():
    while True:
        sText = input("Enter keyword to search or enter to display all books: ")
        pgno = 1
        while pgno > 0:
            rows = searchResults(sText, pgno)
            if rows == []:  # if no results are found
                print("No results. Click enter to return to previous page ...")
                pgno -= 1
            else:  
                util.displayRows(rows, ("Book ID", "Title", "Author", "Publish Year", "Rating", "Available")) # display the results
                print("1. Would you like to borrow a book")
                print("2. Search something else")
                print("3. Exit search")
                print("4. Go to the next page")
                if pgno > 1:
                    print("5. Go to previous page")
            
            choice = input("Enter you choice: ")
            if choice == "1":   # borrow a book
                borrowBook(rows)
            elif choice == "2": # search something else
                break
            elif choice == "3": # exit search
                return
            elif choice == "4": # go to the next page
                pgno += 1
            elif choice == "5": # go to the previous page
                pgno -= 1
            else:
                continue
    return

# Function that allows the user to borrow a book
def borrowBook(results):
    id = input("Enter book ID you would like to borrow: ")
    if id.isdigit():
        id = int(id)
    else:
        print("Invalid input")
        return 0

    rowMapping = {}
    for row in results:
        rowMapping[row[0]] = row[5]     # create a dictionary of the book id and if it is available or not

    if id not in rowMapping.keys(): # if the book is not found
        print("Sorry the book cannot be found!")
        return 0
    elif rowMapping[id] == "YES":   # if the book is available
        cursor.execute("SELECT bid FROM borrowings")
        connection.commit()
        keys = cursor.fetchall()
        key = [i[0] for i in keys]
        bid = 1
        while True: # find the next available bid
            if bid not in key:
                break
            bid += 1
        
        cursor.execute("""
            INSERT INTO BORROWINGS VALUES (:bid, :user, :bookid, :start, NULL)
        """, {'bid': bid, 'user': user, 'bookid': id, 'start': str(datetime.date.today())})
    
        connection.commit()
        cursor.execute("SELECT title FROM books WHERE book_id = ?", [id])
        connection.commit()
        borrowedBook = cursor.fetchone()
        print("You have successfully borrowed ", borrowedBook[0])
    elif rowMapping[id] == 'NO':
        print("Sorry, this book has been already borrowed. You cannot borrow it")
    else:
        print("Sorry the book cannot be found!")

    print()        
    return 1

# Function that allows the user to search for a book
# Main function call this function to search for a book
def search(conn, username):
    # Setup global variables for the connection and the user
    global connection, cursor, user
    connection = conn
    cursor = conn.cursor()
    user = username
    handleSearch()
    return 1