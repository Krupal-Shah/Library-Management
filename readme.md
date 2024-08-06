# Library Management System
## Description
This is a simple library management system that is implemented using python and SQLite3. The system is implemented using command-line interface

## Features
- Member Management
- Book Management
- Issue Book
- Return Book
- Pay Fine
- Generate Report

## Requirements
- Python 3
- SQLite3

## How to run
1. Clone the repository
2. Ensure that there is a database file as it will be asked when the program is run. If the file does not exist, a `dummy.db` file is present in the repository which can be used. 
3. Run the program using the command `python main.py`
    1. You can also give it the argument 'dummy' to add random data to the database. `python main.py dummy`
4. If the database has no tables in it, the program will automatically generate the required tables with proper indexes.
    1. The following indexes are created:
        1. Index on members(name): Helps with searching members by name.
        2. Index on books(title) and books(author): Improves search performance for books by title or author.
        3. Index on borrowings(member) and borrowings(book_id): Speeds up searches for borrowings by member or book.
        4. Index on penalties(bid): Optimizes lookups for penalties associated with a borrowing.
        5. Index on reviews(member) and reviews(book_id): Facilitates fast retrieval of reviews by member or book.
        6. Index on reviews(rating): Allows efficient querying based on rating values.
5. Follow the instructions in the command line.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
