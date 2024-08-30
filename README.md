# LLM Project
This project provides a FastAPI-based web service that fetches support issues from an external API, categorizes them using OpenAI's GPT-4, and returns a summary of categorized issues.

## Features
a. Fetch Issues: Retrieves support issues within a specified date range from an external API.


b. Categorize Issues: Uses AI to categorize each issue based on its description.


c. Summarize Results: Returns a sorted summary of categorized issues, including the category name, count, and the actual issues.

## Setting up

git clone https://github.com/eniolaomotee/llm-project.git

cd issue-categorization-api

## Create a Virtual Environment and Activate It:

python3 -m venv venv

source venv/bin/activate  

On Windows use `venv\Scripts\activate`

## Install Dependencies:
pip install -r requirements.txt

## Set Up Environment Variables:
Create a .env file in the project root and add your OpenAI API key:

OPENAI_API_KEY=your_openai_api_key_here

## Running the API
Start the FastAPI server:
uvicorn main:app --reload
The API will be available at http://127.0.0.1:8000/docs.

## Usage
To categorize issues, send a GET request to:

GET /categorize_issues/?start_date=START_DATE&end_date=END_DATE&page=1&count=20

start_date: UNIX timestamp for the start of the date range.

end_date: UNIX timestamp for the end of the date range.

page: Page number for pagination (default: 1).

count: Number of issues per page (default: 20).

Example Request


curl -X 'GET' \
  'http://127.0.0.1:8000/docs/categorize_issues/?start_date=1724607876&end_date=1724867076&page=1&count=20' \
  -H 'accept: application/json'
Example Response
{
  "status": "success",
  "categorized_issues": [
    {
      "category": "Payment Issues",
      "count": 2,
      "issues": [
      {
          "log_id": 12345,
          "log_request_text": "Balance Issue"
        },
        {
          "log_id": 67890,
          "log_request_text": "Card Issue"
        }
      ]
    },
    {
      "category": "Verification Issues",
      "count": 1,
      "issues": [
        {
          "log_id": 54321,
          "log_request_text": "KYC issue"
        }
      ]
    }
  ]
}
## Project Structure
main.py: Contains the FastAPI app and the logic for fetching, categorizing, and summarizing issues.


.env: Environment file for storing sensitive information like API keys.


requirements.txt: Lists the Python dependencies for the project.

## Acknowledgments
FastAPI - The web framework used.


OpenAI GPT-4 - The AI model used
