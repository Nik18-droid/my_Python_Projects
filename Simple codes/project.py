# We need to import the 'requests' library first. This library allows Python
# to send HTTP requests, which is how we talk to APIs on the internet.
# If you don't have it installed, open your terminal or command prompt and type:
# pip install requests
import requests

# We'll define a function to keep our code organized. This function will take
# the API key and the company name as input.


def get_company_news(api_key, company_name):
    """
    Fetches the latest news headlines for a specific company using the NewsAPI.

    Args:
        api_key (str): 17313a8c325843b89b3d5d42d406a43e
        company_name (str): Nvidia.
    """
    # This is the base URL for the NewsAPI endpoint we want to use.
    # The 'everything' endpoint lets us search for articles.
    url = "https://newsapi.org/v2/everything"

    # These are the parameters we'll send with our request.
    # 'q': This is the query, which will be our company name.
    # 'sortBy': We'll sort by 'publishedAt' to get the newest articles first.
    # 'apiKey': This is your secret key to authenticate your request.
    params = {
        'q': company_name,
        'sortBy': 'publishedAt',
        'language': 'en',  # We want news in English.
        'apiKey': api_key

    }

    # Now, we'll use a try-except block for error handling. This is good practice.
    # It means "try to do this, and if an error happens, don't crash."
    try:
        # This is the line that actually sends the request to the NewsAPI server.
        response = requests.get(url, params=params)

        # This will check if the request was successful (e.g., status code 200 OK).
        # If there was a server error, it will raise an exception.
        response.raise_for_status()

        # The API sends back data in a format called JSON. We need to convert it
        # into a Python dictionary so we can work with it easily.
        data = response.json()

        # The 'articles' key in the dictionary contains a list of all the articles.
        articles = data.get('articles', [])

        # Check if the list of articles is empty.
        if not articles:
            print(f"No news articles found for '{company_name}'.")
            return

        # Print a nice header for our output.
        print(f"--- Latest News for {company_name} ---")

        # We'll loop through the first 5 articles in the list and print their titles.
        # We use articles[:5] to get a "slice" of the list containing the first 5 items.
        for article in articles[:5]:
            # The 'title' key in each article dictionary contains the headline.
            print(f"- {article['title']}")

    except requests.exceptions.RequestException as e:
        # This code will run if there was a network problem (e.g., no internet).
        print(f"An error occurred with the request: {e}")
    except Exception as e:
        # This will catch any other unexpected errors.
        print(f"An unexpected error occurred: {e}")


# --- This is the main part of our script where we run the code ---
if __name__ == "__main__":
    # IMPORTANT: Replace "YOUR_API_KEY_HERE" with the actual API key you get
    # from the NewsAPI.org website.
    MY_API_KEY = "17313a8c325843b89b3d5d42d406a43e"

    # The company we want to search for. You can change this to "Microsoft", "Google", etc.
    COMPANY_TO_SEARCH = "Nvidia"

    # Check if the user has replaced the placeholder API key.
    if MY_API_KEY == "YOUR_API_KEY_HERE":
        print("Please replace 'YOUR_API_KEY_HERE' with your actual NewsAPI key.")
    else:
        # Call our function to fetch and print the news.
        get_company_news(MY_API_KEY, COMPANY_TO_SEARCH)
