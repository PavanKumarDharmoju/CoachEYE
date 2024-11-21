CoachEYE
========

Welcome to the CoachEYE repository! This project provides a chatbot interface tailored for assisting coaches and analysts of the Northwestern soccer team. It incorporates machine learning, a streamlined front-end interface, and a robust backend for generating tactical insights, analyzing team data, and improving player performance.

* * * * *

📂 Folder Structure
-------------------

.

├── app

│   ├── app.py                # Main Flask application

│   ├── chatbot1.py           # Chatbot logic implementation

│   ├── compare_embeddings.py # Embedding comparison logic

├── static

│   ├── index.html            # Front-end UI for the chatbot

├── scripts

│   ├── create_database.py    # Script to create the Chroma database

│   ├── chatbot.py            # Backend logic for chatbot responses

├── dataprocessed             # Folder for processed soccer data

├── chroma                    # Chroma vectorstore folder

└── README.md                 # Documentation file

* * * * *

🛠️ Prerequisites
-----------------

Ensure you have the following installed:

-   Python (>= 3.8)

-   pip (Python package manager)

* * * * *

📦 Setup Instructions
---------------------

Follow these steps to set up and run the project:

### 1\. Clone the Repository

git clone https://github.com/your-username/northwestern-soccer-assistant.git

cd northwestern-soccer-assistant

### 2\. Create a Virtual Environment

python -m venv venv

source venv/bin/activate  # On Windows: venv\Scripts\activate

### 3\. Run this command
conda install onnxruntime -c conda-forge

### 4\. Install Dependencies

pip install -r requirements.txt

### 5\. Configure OPENAI_API_KEY

export OPENAI_API_KEY = "Your_API_Key"


### 6\. Prepare the Chroma Database

Navigate to the scripts folder and run the create_database.py script to generate the Chroma database from your data:

python scripts/create_database.py

* * * * *

🚀 Running the Application
--------------------------

### 1\. Start the Backend: Navigate to the app folder and run the Flask application:

python app/app.py

1.  The application should be running at http://127.0.0.1:5000.

### 2\. Open the Front-End:\

The chatbot and front-end reference file paths using the placeholder file:///Users/pavankumardharmoju/Documents/GitHub/langchain-rag-tutorial/. This path must be updated to match your current working directory.

-   Open the static/index.html file in a browser.

-   Interact with the chatbot for soccer insights and assistance.

* * * * *

📑 Features
-----------

-   Tactical Analysis: Generate actionable strategies for in-game scenarios.

-   Player Development Insights: Analyze player performance metrics for improvement.

-   Interactive Chat Interface: Easy-to-use front-end interface for soccer queries.

-   Quick Prompts: Pre-defined suggestions for common coaching scenarios.

* * * * *

📂 Key Files and Their Roles
----------------------------

app/app.py -> Main Flask application, handles API requests for the chatbot
app/chatbot1.py -> Core chatbot logic
app/compare_embeddings.py -> Compares embeddings for similarity search
static/index.html -> Front-end interface for user interactions
scripts/create_database.py -> Creates the Chroma database from data files
scripts/chatbot.py -> Contains helper functions and utilities for the chatbot
dataprocessed -> Folder containing processed soccer data
chroma -> Folder containing Chroma vectorstore data

* * * * *

🧪 Testing and Validation
-------------------------

1.  Ensure all Python scripts execute without errors.

2.  Verify the chatbot generates responses with relevant soccer insights.

3.  Test the database creation process using create_database.py.

4.  Validate that the front-end interface connects seamlessly with the backend.

* * * * *

🤝 Contributing
---------------

Contributions are welcome! To contribute:

1.  Fork the repository.

2.  Create a feature branch (git checkout -b feature-name).

3.  Commit your changes (git commit -m "Add feature-name").

4.  Push to your fork (git push origin feature-name).

5.  Create a pull request.

* * * * *

📝 License
----------

This project is licensed under the MIT License. See the LICENSE file for details.

* * * * *

📬 Contact
----------

For questions or support, please contact:

-   Team Name: SoccerSynth

-   Email: salonipatel2024@u.northwestern.edu
