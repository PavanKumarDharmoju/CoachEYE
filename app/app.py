# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import logging
# from chatbot1 import chatbot

# # Set up logging
# logging.basicConfig(level=logging.DEBUG)

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# # Initialize chatbot
# logging.info("Initializing chatbot...")
# logging.info("Chatbot initialized successfully.")

# @app.route("/chat", methods=["POST"])
# def chat():
#     user_message = request.json.get("message")
#     logging.debug(f"Received message: {user_message}")

#     if not user_message:
#         logging.error("No message provided.")
#         return jsonify({"error": "Message is required"}), 400

#     # Query the chatbot
#     try:
#         response = chatbot({"query_text": user_message})
#         logging.debug(f"Chatbot response: {response}")
#     except Exception as e:
#         logging.error(f"Error processing message: {e}")
#         return jsonify({"error": "Failed to process the message"}), 500

#     # Return the response
#     return jsonify({
#         "response": response["answer"],
#         "sources": response.get("sources")  # Include sources if available
#     })

# if __name__ == "__main__":
#     logging.info("Starting Flask app...")
#     app.run(port=5000)


from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from chatbot1 import create_chatbot

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize chatbot
logging.info("Initializing chatbot...")
chatbot = create_chatbot()
logging.info("Chatbot initialized successfully.")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    logging.debug(f"Received message: {user_message}")

    if not user_message:
        logging.error("No message provided.")
        return jsonify({"error": "Message is required"}), 400

    # Query the chatbot
    try:
        response = chatbot({"question": user_message})
        logging.debug(f"Chatbot response: {response}")
    except Exception as e:
        logging.error(f"Error processing message: {e}")
        return jsonify({"error": "Failed to process the message"}), 500

    # Return the response
    return jsonify({
        "response": response["answer"],
        "sources": response.get("sources")  # Include sources if available
    })

if __name__ == "__main__":
    logging.info("Starting Flask app...")
    app.run(port=5000)