from flask import Flask, request, jsonify, render_template
from lib_bot import chatbot
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
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)


@app.route("/")
def home():
    """
    Renders the home page with the chat interface.
    """
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat_route():
    """
    Handles chatbot interactions using OpenAI.
    Expects JSON data: { "prompt": "", "context": [] }
    """
    try:
        data = request.json
        prompt = data.get("prompt")
        if not prompt:
            return jsonify({"error": "'prompt' is required."}), 400

        # Call the chatbot function
        response = chatbot(prompt)

        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Ensure templates folder exists
    if not os.path.exists("templates"):
        os.makedirs("templates")

    app.run(debug=True)
