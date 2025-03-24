# ChatGPT Google Sheets Integration Bot

This repository contains a Python-based chatbot that integrates OpenAI's ChatGPT API with Google Sheets for dynamic data handling and manipulation. The bot enables natural language commands to manage a library inventory system, including listing, searching, updating, and managing books in real-time. It leverages **function-calling** to interact with Google Sheets and perform specific tasks like adding a book, checking availability, and updating book status.

## Features
- **Natural Language Interaction**: Users can interact with the bot to perform various tasks using plain language.
- **Google Sheets Integration**: Real-time updates and data management directly in Google Sheets.
- **Context-Aware Conversations**: Maintains context for smooth and intuitive interactions.
- **Function Calling**: The chatbot dynamically calls specific functions such as adding a book, searching for books, updating inventory, etc., based on the user's requests.
- **Modular Codebase**: Clean, extensible Python architecture using Flask and OpenAI API for better scalability.

## Tech Stack
- **Python**: Backend logic and data manipulation.
- **Flask**: Web framework for the chatbot interface.
- **OpenAI API**: Conversational AI for natural language understanding.
- **Google Sheets API**: For seamless data integration and updates.
- **gspread**: Python library for interacting with Google Sheets.
- **HTML/CSS/JavaScript**: Frontend for the chat interface.

## How It Works
1. **User Interaction**: The user interacts with the bot through a web-based interface. They input commands such as "Add a new book" or "Check availability of Harry Potter."
2. **AI-Powered Response with Function Calls**: The bot uses the OpenAI API to process user requests and decide which function to call (such as `list_books`, `add_book`, or `search_books`) based on the conversation context.
3. **Real-Time Data Management**: The bot interacts with Google Sheets to update, retrieve, and manipulate the library's inventory in real-time based on the user input.
4. **Dynamic Function Calling**: The chatbot calls specific functions like `add_book`, `search_books`, or `remove_book` to interact with Google Sheets directly.

## Features Explained
- **List Books**: Display all the books in the library categorized by genre.
- **Search Books**: Search for books by title, author, or category.
- **Add Book**: Add a new book to the inventory by specifying the title, author, category, and availability status.
- **Update Book**: Update the status, category, or other fields of an existing book.
- **Check Availability**: Check if a specific book is available or issued.
- **Remove Book**: Remove a book from the library inventory by its title.
- **Get Issued Books**: Retrieve a list of books that are currently issued.
- **Get Available Books**: Retrieve a list of books that are currently available.
