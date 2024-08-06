# Function that displays (pretty print) the rows of the search results
def displayRows(rows, header):
    widths = [len(h) for h in header]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(len(str(cell)), widths[i])   
    formatted_row = ' '.join('{:%d}|' % width for width in widths)
    print(formatted_row.format(*header))
    for row in rows:
        print(formatted_row.format(*row))
    print()