import requests
import json

def callAI(content, API_KEY):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key="+API_KEY
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "下面有一段文字:"+ content +"   Please accurately extract 5 keywords in this text, each not exceeding 10 bytes, with no spaces inside each keyword. Each two keywords should be separated by ||"
                    }
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = response.json()
    text = result["candidates"][0]["content"]["parts"][0]["text"]
    return text

