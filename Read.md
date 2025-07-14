Financial News Fetcher & Sentiment Analyzer

Project Overview
This is a Python-based application designed to fetch real-time news articles for a specified company and prepare them for sentiment analysis. This project serves as a foundational step in my journey to understand and build agentic AI workflows, demonstrating core skills in API integration, data handling, and clean coding practices.
The primary goal is to create a reliable data pipeline that can be extended in the future with a Large Language Model (LLM) to perform automated sentiment classification on the headlines.

Key Features
Dynamic News Fetching: Connects to the NewsAPI to retrieve the most recent, relevant news articles for any given company stock ticker or name.
Targeted Filtering: The request is specifically configured to pull English-language articles, sorted by publication date to ensure timeliness.
Clean & Readable Output: The script neatly prints the top 5 headlines to the console for a quick overview.
Robust Error Handling: Implemented try-except blocks to gracefully handle potential network issues or unexpected API responses without crashing.


Technologies & Tools
Language: Python 3
Core Library: requests (for making HTTP requests to external APIs)
API: NewsAPI.org


Setup & Installation
This project is designed to be run locally. Here’s how you can set it up:
    1. Download the Code:
        On this GitHub repository page, click the green <> Code button.
        Select "Download ZIP".
        Unzip the folder on your computer.
    2. Install the Necessary Dependencies:
        Open your terminal or command prompt.
        Navigate into the project folder.
        Run the command: pip install requests
    3. Get Your API Key:
        Visit NewsAPI.org and register for a free developer API key.


How to Run the Script
    1. Open the project.py file in your code editor.

    2. Find the following line:
         MY_API_KEY = "YOUR_API_KEY_HERE"

    3. Replace "YOUR_API_KEY_HERE" with your actual API key from NewsAPI.

    4. You can also change the company to search for by editing this line:
         COMPANY_TO_SEARCH = "Microsoft"

    5. Run the script from your terminal:
         python project.py


Future Improvements (Next Steps)

This project is the first building block. The planned next steps are:
  1. Integrate an LLM: Pass the fetched headlines to a language model (like one from the Hugging Face Hub) to classify the sentiment of each headline as 'Positive', 'Negative', or 'Neutral'.
  
  2. Data Storage: Store the results (headline, company, sentiment, date) in a simple database or a CSV file for historical analysis.
  3. Build a Simple UI: Create a basic web interface using a framework like Flask or Streamlit to make the tool more interactive.
