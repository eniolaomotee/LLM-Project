from fastapi import FastAPI,HTTPException,Query
import os
from dotenv import load_dotenv
import openai
import requests
from datetime import datetime

load_dotenv()

openai.api_key = os.getenv('OPEN_API_KEY')

app = FastAPI()

@app.get("/all-issues/")
def fetch_issues(page:int, count:int, start_date:int,end_date:int):
    url = f'https://bridgecard-issuing-app.com/support-bot-service/v1/dashboard/issues?page={page}&count={count}&start_date={start_date}&end_date={end_date}'
    headers = {'accept': 'application/json'}
    response = requests.post(url,headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch URL, please crosscheck")
    return response.json()


def categorize_issue(issue_description):
    # prompt = (
    #     f" Categorize the following issue : {issue_description} \n\n"
    #     "Here are some of your categorization: \n"
    #     "1. 'Customer charged twice, order didn't go through , issue with issuing bank' is a Merchant-Issuing Bank Issue .\n"
    #     "2. 'Selfie image verification failed, user needs to upload a clear image' is a Verification issue. \n"
    #     "3. 'Card declined during transaction despite sufficient balance' is a payment Issue .\n"
    #     "4. 'User unable to login due to incorrect password' is an authentication Issue .\n"
    # )
    prompt = f"Categorize the following issue: {issue_description}"
    try: 
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role":"system", "content":"ANA"},
                {"role":"user","content":prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e :
        print(f"Error from Model: {e}")
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/categorize_issues/")
def categorize_issues(
    start_date: int = Query(),
    end_date: int = Query(),
    page: int = Query(1,description=""),
    count: int = Query(20, description="")):

    if not start_date or not end_date or not page or not count:
        raise HTTPException(status_code=400, detail="All field must be provided")

    try:
        issues_data = fetch_issues(page,count,start_date,end_date)
        categorize_counts = {}
        categorize_results = {}

        start_datetime = datetime.fromtimestamp(start_date)
        end_datetime = datetime.fromtimestamp(end_date)
        

        for issue in issues_data['data']:
            log_datetime = datetime.fromtimestamp(issue['log_created_at'])

            if start_datetime <= log_datetime and log_datetime <= end_datetime:
                category = categorize_issue(issue['log_request_text'])

                if category not in categorize_results:
                    categorize_results[category] = []

                if category in categorize_counts:
                    categorize_counts[category] += 1
                else:
                    categorize_counts[category] = 1

            categorize_results[category].append({
                    "log_id": issue["log_id"],
                    "log_request_text": issue["log_request_text"]
                })
        
        sorted_categories = [
            {
                "category": category,
                "count": categorize_counts[category],
                "issues": categorize_results[category]
            }
            for category in sorted(categorize_counts, key= categorize_counts.get, reverse=True)
        ]

        return {"status":"success","categorized_issues":sorted_categories}

    except Exception as e:
        print(f"Error in categorize_issues: {e}")
        raise HTTPException(status_code=500, detail=str(e))
