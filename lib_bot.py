import os
import openai
import json
from dotenv import load_dotenv
from spreadsheet_int import (
    connect_to_sheet,
    list_books,
    search_books, 
    add_book,
    update_book,
    remove_book, 
    count_books,
    check_availability,
    get_issued_books,
    get_available_books
)

# Importing environment variables from .env file
load_dotenv()

# Set the API key from .env file
openai.api_key = os.getenv("OPENAI_API_KEY")


def chatbot(prompt):
    # print(f"User: {prompt}")
    messages = [{"role": "system", "content": "You are a rude assistant."}]

    functions = [
        {
            "name": "list_books",
            "description": "List all books in the library inventory, including title, author, category, status, and aisle.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name" : "search_books",
            "description": "Search for books in the library inventory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query":{
                        "type": "string",
                        "description": "Search term to look for in the title, author, or genre."
                        },
                    },
                    "required": ["query"]
                }
        },
        {
            "name" : "add_book",
            "description" : "Adding a new book to the inventory",
            "parameters" : {
                "type":"object",
                "properties": {
                    "title": {
                        "type":"string",
                        "description" : "Name of the Book",
                    },
                    "author": {
                        "type":"string",
                        "description": "Name of the Author of the Book",
                    },
                    "category": {
                        "type":"string",
                        "description": "Genre of the Book",
                    },
                    "status":{
                        "type":"string",
                        "descrription": "Status of availability (eg. 'available' or 'issued')",
                    },
                },
                "required" : ["title","author", "category", "status"],
            },
        },
        {
            "name": "update_book",
            "description": "Update a specific field (e.g., Status, Category) for a book in the library inventory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the book to update."
                    },
                    "field": {
                        "type": "string",
                        "description": "The field to update (e.g., Status, Category)."
                    },
                    "new_value": {
                        "type": "string",
                        "description": "The new value to set for the specified field."
                    }
                },
                "required": ["title", "field", "new_value"]
            }
        },
        {
            "name": "check_availability",
            "description": "Check if a book is available in the library.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Title of the book to check."}
                },
                "required": ["title"]
            }
        },
        
        {
            "name": "remove_book",
            "description": "Remove a book from the library inventory using its title.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Title of the book to remove."}
                },
                "required": ["title"]
            }
        },
        {
            "name": "count_books",
            "description": "Get the total number of books in the library inventory.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "get_issued_books",
            "description": "Retrieve a list of all books that are currently issued.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "get_available_books",
            "description": "Retrieve a list of all books that are currently available.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }

    ]
    
    # Add user input to the message history
    messages.append({"role": "user", "content": prompt})

    try:
        # Requesting GPT for chat completion
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            functions=functions,
            function_call="auto" #ChatGPT decides which function to call
        )

        print(response)

        # Get assistant's response
        chat_message = response.choices[0].message

        messages.append({"role" : "assistant", "content": chat_message})
        print(messages)

        if chat_message.function_call:
            func_name = chat_message.function_call.name
            func_args = json.loads(chat_message.function_call.arguments)
            # print("Name", func_name)
            # print(func_args)

            #Connect to google sheets
            sheet = connect_to_sheet("Library Inventory")

            #Mapping function calls 
            if func_name == "list_books":
                return list_books(sheet)
            elif func_name == "search_books":
                return search_books(sheet, **func_args)
            elif func_name == "add_book":
                return add_book(sheet, **func_args)
            elif func_name == "update_book":
                return update_book(sheet, **func_args)
            elif func_name == "remove_book":
                return remove_book(sheet, **func_args)
            elif func_name == "check_availability":
                return check_availability(sheet, **func_args)
            elif func_name == "count_books":
                return count_books(sheet)
            elif func_name == "get_available_books":
                return get_available_books(sheet)
            elif func_name == "get_issued_books" :
                return get_issued_books(sheet)
            
             # If no function call, return the assistant's response
        return chat_message.content
    
    except Exception as e:
        return f"Error: {str(e)}"