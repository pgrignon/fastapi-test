from fastapi import FastAPI
from pydantic import BaseModel
import utils

app = FastAPI()

headers = {
    "Ocp-Apim-Subscription-Key": "83a00384bd1a4a2b8319628ccf41029e",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

class Model(BaseModel):
    text_to_analyze: list

@ app.post("/")
def analyze_text(text: Model):
    response = {"sentiment": [], "keyphrases": []}
    no_of_text = len(text.text_to_analyze)
    for i in range(no_of_text):
        document = {"documents": [{"id": i+1, "language": "en", "text": text.text_to_analyze[i]}]}
        
        sentiment = utils.call_text_analytics_api(headers, document, endpoint='sentiment')
        keyphrases = utils.call_text_analytics_api(headers, document, endpoint='keyPhrases')
        
        response["sentiment"].append(sentiment["documents"][0])
        response["keyphrases"].append(keyphrases["documents"][0])
    return response