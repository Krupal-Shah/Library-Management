connection = None
cursor = None

def initial(conn, dummy=False):
    print(dummy)
    global cursor, connection
    connection = conn
    cursor = conn.cursor()

    cursor.execute('drop table if exists reviews')
    cursor.execute('drop table if exists penalties')
    cursor.execute('drop table if exists borrowings')
    cursor.execute('drop table if exists books')
    cursor.execute('drop table if exists members')

    cursor.execute(' PRAGMA foreign_keys=ON; ')

    connection.commit()

    cursor.execute(
        '''
        CREATE TABLE members (
            email CHAR(100),
            passwd CHAR(100),
            name CHAR(255) NOT NULL,
            byear INTEGER,
            faculty CHAR(100),
            PRIMARY KEY (email)
        )
        ''')

    cursor.execute(
        '''
        CREATE TABLE books (
            book_id INTEGER,
            title CHAR(255),
            author CHAR(150),
            pyear INTEGER,
            PRIMARY KEY (book_id)
        );
        '''
    )

    cursor.execute(
        '''
        CREATE TABLE borrowings(
            bid INTEGER,
            member CHAR(100) NOT NULL,
            book_id INTEGER NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE,
            PRIMARY KEY (bid),
            FOREIGN KEY (member) REFERENCES members(email),
            FOREIGN KEY (book_id) REFERENCES books(book_id)
        );
        '''
    )

    cursor.execute(
        '''
        CREATE TABLE penalties(
            pid INTEGER,
            bid INTEGER NOT NULL,
            amount INTEGER NOT NULL,
            paid_amount INTEGER,
            PRIMARY KEY (pid),
            FOREIGN KEY (bid) REFERENCES borrowings(bid)
        );
        '''
    )

    cursor.execute(
        '''
        CREATE TABLE reviews(
            rid INTEGER,
            book_id INTEGER NOT NULL,
            member CHAR(100) NOT NULL,
            rating INTEGER NOT NULL,
            rtext CHAR(255),
            rdate DATE,
            PRIMARY KEY (rid),
            FOREIGN KEY (member) REFERENCES members(email),
            FOREIGN KEY (book_id) REFERENCES books(book_id)
        );
        '''
    )

    cursor.execute(
        '''
        CREATE INDEX idx_members_name
            ON members(name);
        '''
    )

    cursor.execute(
        '''
        CREATE INDEX idx_books_title
            ON books(title);
        '''
    )

    cursor.execute(
        '''
        CREATE INDEX idx_books_author
            ON books(author);
        '''
    )

    cursor.execute(
        '''
        CREATE INDEX idx_borrowings_member
            ON borrowings(member);
        '''
    )

    cursor.execute(
        '''
        CREATE INDEX idx_borrowings_book_id
            ON borrowings(book_id);
        '''
    )

    cursor.execute(
        '''
        CREATE INDEX idx_penalties_bid
            ON penalties(bid);
        '''
    )

    cursor.execute(
        '''
        CREATE INDEX idx_reviews_member
            ON reviews(member);
        '''
    )

    cursor.execute(
        '''
        CREATE INDEX idx_reviews_book_id
            ON reviews(book_id);
        '''
    )

    cursor.execute(
        '''
        CREATE INDEX idx_reviews_rating
            ON reviews(rating);
        '''
    )

    connection.commit()

    if dummy:
        cursor.execute(
            '''
            INSERT INTO members VALUES
                ("student1@gmail.ca", "0808", "Nick", 2004, "CS"),
                ("student2@gmail.ca", "1818", "Sarah", 2004, "CS"),
                ("student3@gmail.ca", "2828", "Charlie", 2004, "Math");
            '''
        )

        cursor.execute(
            '''
            INSERT INTO books VALUES
                (1, "To Kill a Mockingbird", "Harper Lee", 1960),
                (2, "The Hobbit", "Tolkien", 1937),
                (3, "Philosopher's Stone and Harry Potter", "J.K. Rowling.", 1997),
                (4, "Chamber of Secrets and Harry Potter", "J.K. Rowling.", 1998),
                (5, "Prisoner of Azkaban and Harry Potter", "J.K. Rowling.", 1999),
                (6, "The Lord of the Rings", "J.R.R. Tolkien", 1954),
                (7, "Goblet of Fire and Harry Potter", "J.K. Rowling.", 2000),
                (8, "Order of the Phoenix and Harry Potter", "J.K. Rowling.", 2003),
                (9, "Half-Blood Prince and Harry Potter", "Harry Potter", 2005),
                (10, "Deathly Hallows and Harry Potter", "Potter Harry", 2007),
                (11, "Spirited Away", "Anderson Harry", 2001),
                (12, "My Neighbor Totoro", "Foster Harry", 1988),
                (13, "Your Name", "Fitzgerald Harry", 2016),
                (14, "Grave of the Fireflies", "Cool Harry", 1988);
            '''
        )

        cursor.execute(
            '''
            INSERT INTO borrowings VALUES
                (1, "student1@gmail.ca", 1, "2023-11-15", "2023-12-15"),
                (2, "student1@gmail.ca", 2, "2023-10-15", "2024-01-15"),
                (3, "student1@gmail.ca", 5, "2024-03-15", NULL),
                (4, "student1@gmail.ca", 7, "2024-01-01", NULL), 
                (5, "student1@gmail.ca", 8, "2023-12-10", NULL), 
                (6, "student2@gmail.ca", 9, "2024-02-29", NULL), 
                (7, "student2@gmail.ca", 13, "2024-02-01", NULL), 
                (8, "student2@gmail.ca", 1, "2023-12-16", "2024-01-15");
            '''
        )

        cursor.execute(
            '''
            INSERT INTO penalties VALUES
                (1, 1, 10, 10),
                (2, 1, 20, 10),
                (3, 1, 30, NULL),
                (4, 2, 100, 100),
                (5, 3, 50, 25), 
                (6, 4, 20, NULL),
                (7, 7, 10, 10);
            '''
        )

        cursor.execute(
            '''
            INSERT INTO reviews VALUES
                (1, 2, "student1@gmail.ca", 3, "Great!", "2023-12-15"),
                (2, 2, "student2@gmail.ca", 4, "Amazing!", "2023-11-15"), 
                (3, 6, "student3@gmail.ca", 5, "Wow!", "2023-10-15"), 
                (4, 3, "student1@gmail.ca", 4, "I love this book!", "2023-07-08"), 
                (5, 3, "student1@gmail.ca", 4, "OMG", "2023-04-22"), 
                (6, 3, "student3@gmail.ca", 5, "The book's setting is pure magic, immersing readers in a captivating world.", "2023-11-03"), 
                (7, 4, "student1@gmail.ca", 3, "So good!", "2022-02-28"), 
                (8, 10, "student1@gmail.ca", 3, " The setting serves as a magical gateway, transporting readers to a vivid and memorable world.", "2022-11-04"),
                (9, 10, "student3@gmail.ca", 4, "I love this book!", "2022-05-08"),
                (10, 10, "student3@gmail.ca", 5, "Cool", "2022-04-10"), 
                (11, 9, "student2@gmail.ca", 4, "Lol", "2022-02-28"), 
                (12, 9, "student2@gmail.ca", 2, "I don't like it at all!", "2022-12-19");
            '''
        )

        connection.commit()

    return