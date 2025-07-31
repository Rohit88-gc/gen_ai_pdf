import requests

api_key = "ABcD-XYZ Make your own api key here"  # Replace with your Gemini API key
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def get_openai_response(prompt):
    headers = {"Content-Type": "application/json", "X-goog-api-key": api_key}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        # Clean up any markdown-like formatting (e.g., *, **)
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        text = text.replace("*", "").replace("**", "")  # Remove asterisks
        return text
    else:
        return f"Oops, the digital wizard’s busy! Error: {response.status_code}"

if __name__ == "__main__":
    print(get_openai_response("Test"))
