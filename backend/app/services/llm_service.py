import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_response(prompt: str):
    # response here is a Response object, which contains many things like status code, headers, cookies, body etc
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3.2:1b",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()
    #This converts the JSON body into a Python dictionary.

    if "error" in data:
        raise Exception(data["error"])

    return data["response"]