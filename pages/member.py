import pages.util as util

connection = None
cursor = None

def member_info(conn, username): 
    global connection, cursor
    connection = conn
    cursor = conn.cursor()

    #Finds previous, current, overdue borrowings unpaid penalties and total debt.
    cursor.execute("""
        WITH 
        PrevB AS (
            SELECT COUNT(*) AS Previous_Borrowings FROM borrowings 
            WHERE end_date IS NOT NULL AND member = :user
        ), 
        
        CurB AS (
            SELECT COUNT(*) AS Current_Borrowings FROM borrowings 
            WHERE end_date IS NULL AND member = :user
        ), 
        
        OverB AS (
            SELECT COUNT(*) AS Overdue_Borrowings FROM borrowings 
            WHERE end_date IS NULL AND member = :user AND
            julianday('now') - julianday(start_date) > 20
        ),

        pen1 AS (
            SELECT COUNT(*) AS Unpaid_penalties, SUM(amount - ifnull(paid_amount, 0)) AS Total_Debt FROM penalties p
            LEFT JOIN borrowings b ON b.bid = p.bid
            WHERE ifnull(p.paid_amount, 0) < p.amount AND member = :user
        )

        SELECT name, email, byear, faculty, Previous_Borrowings, Current_Borrowings, Overdue_Borrowings, Unpaid_penalties, Total_Debt
        FROM members, PrevB, CurB, OverB, pen1 where email = :user;

    """, {'user': username})
    connection.commit()
    row = cursor.fetchone()
    if row != None:
        util.displayRows(row, ('Name', 'Email', 'DOB', 'Faculty', 'Past Borrowings', 'Current Borrowings', 'Overdue', 'Penalties', 'Debt'))
        return 1
    else:
        print("No user found")
        return 0