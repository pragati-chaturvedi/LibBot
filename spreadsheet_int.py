import gspread
from oauth2client.service_account import ServiceAccountCredentials

#Connecting to Google Sheets
def connect_to_sheet(sheet_name):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("google_service_credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1 #for access to the first sheet
    return sheet

# print(connect_to_sheet("Library Inventory"))

#List all books
def list_books(sheet):
    data = sheet.get_all_records()
    
    if not data:
        return "No books found in the inventory."
    
    # Group books by category
    books_by_category = {}
    for book in data:
        category = book["Category"]
        if category not in books_by_category:
            books_by_category[category] = []
        books_by_category[category].append(book)

    # Build the formatted response
    response = "📚 Library Inventory :<br><br> Listing books by category - <br>"
    for category, books in books_by_category.items():
        response += f"<br> {category.capitalize()} <br><br>"
        for idx, book in enumerate(books, 1):
            response += (
                f"{idx}. {book['Title of the Book']} by {book['Author']} "
                f"({book['Status'].capitalize()}, Aisle: {book['Aisle'] or 'N/A'})<br>"
            )
        response += "\n"  # Add spacing between categories

    return response

#Search for books by query
def search_books(sheet, query):
    results = []
    data = sheet.get_all_records()
    for row in data:
        # print(row)
        if query.lower() in row['Title of the Book'].lower() or query.lower() in row['Author'].lower() or query.lower() in row['Category'].lower() :
            results.append(row)
    if not results:
        return "No matching books found."

    # Formatting the results for better readability
    formatted_results = "Matching Books:<br>"
    for idx, book in enumerate(results, 1):
        formatted_results += (
            f"{idx}. <br>"
            f"   - Title : {book['Title of the Book']}<br>"
            f"   - Author : {book['Author']}<br>"
            f"   - Category : {book['Category']}<br>"
            f"   - Status : {book['Status']}<br>"
            f"   - Aisle : {book['Aisle']}<br>"
            "----------------------------------------<br>"
        )

    return formatted_results

#Add new book
def add_book(sheet, title, author, category, status):
    # count = len(sheet.get_all_records())
    if search_books(sheet, title) == "No matching books found.":
        sheet.append_row([title, author, category, status])
        return f"Book '{title}' added successfully."
    else:
        return "Book already exists"

#Update book details
def update_book(sheet, title, field, new_value):
    data = sheet.get_all_records()
    
    # Check if the sheet has data
    if not data:
        return "The inventory is empty."
    
    # Get column headers
    headers = list(data[0].keys())
    field_map = {header.lower(): header for header in headers} 

    # Validate the field
    if field.lower() not in field_map:
        return f"Invalid field. Valid fields are: {', '.join(headers)}"
    
    #to assess for case sensitivity
    normalized_field = field_map[field.lower()]

    # Search for the book by title and update the specified field
    for index, row in enumerate(data):
        if row['Title of the Book'].lower() == title.lower():
            col_index = headers.index(normalized_field) + 1  # Find the column index for the field
            sheet.update_cell(index + 2, col_index, new_value)  # Account for header row
            return f"The field '{normalized_field}' for the book '{title}' was updated to '{new_value}'."

    return f"Book '{title}' not found."

#Remove a book by title
def remove_book(sheet, title):
    data = sheet.get_all_records()
    for index, row in enumerate(data):
        if row['Title of the Book'].lower() == title.lower():
            sheet.delete_rows(index + 2)  # Account for header row
            return f"Book '{title}' removed successfully."
    return f"Book '{title}' not found."

#Check book availability
def check_availability(sheet, title):
    data = sheet.get_all_records()
    for row in data:
        if row['Title of the Book'].lower() == title.lower():
            if row['Status'].lower() == "available":
                return f"'{title}' is available in Aisle {row['Aisle']}."
            else:
                return f"'{title}' is currently checked out."
    return f"Book '{title}' not found."

#count total no. of books
def count_books(sheet):
    data = sheet.get_all_records()
    count = len(data)
    if not data:
        return "The inventory is empty"
    
    return f"There are {count} books."

#Get issued books
def get_issued_books(sheet):
    data = sheet.get_all_records()
    result = []
    for row in data:
        if row['Status'].lower() == 'issued':
            result.append(row)
    
    if not result:
        return "No books are issued."
    
    formatted_result = "Issued Books:<br>"
    for idx, book in enumerate(result, 1):
        formatted_result += (
            f"{idx}. <br>"
            f"   - Title : {book['Title of the Book']}<br>"
            f"   - Author : {book['Author']}<br>"
            f"   - Category : {book['Category']}<br>"
            f"   - Status : {book['Status']}<br>"
            "----------------------------------------<br>"
        )

    return formatted_result

#Get available books
def get_available_books(sheet):
    data = sheet.get_all_records()
    result = []
    for row in data:
        if row['Status'].lower() == 'available':
            result.append(row)
    
    if not result:
        return "No books available."
    
    formatted_result = "Available Books:<br>"
    for idx, book in enumerate(result, 1):
        formatted_result += (
            f"{idx}.<br>"
            f"   - Title : {book['Title of the Book']} <br> "
            f"   - Author : {book['Author']} <br> "
            f"   - Category : {book['Category']}<br>"
            f"   - Status : {book['Status']}<br>"
            f"   - Aisle : {book['Aisle']}<br>"
            "----------------------------------------<br>" # Separator for each book
         ) 

    return formatted_result