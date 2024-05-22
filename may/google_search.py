import googleapiclient
from googleapiclient.discovery import build
import os

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.environ.get("GOOGLE_CSE_ID")

def custom_search(query, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=cse_id, **kwargs).execute()
    return res["items"]


def google_search(input_query: str):
    api_key = GOOGLE_API_KEY
    cse_id = GOOGLE_CSE_ID
    num_results = 10
    metadata_results = []
    results = custom_search(
        input_query, num=num_results, api_key=api_key, cse_id=cse_id
    )
    for result in results:
        metadata_result = {
            "snippet": result["snippet"],
            "title": result["title"],
            "link": result["link"],
        }
        metadata_results.append(metadata_result)
    return metadata_results

#     # Outputs a list of dictionaries, each dictionary is a Google Search result