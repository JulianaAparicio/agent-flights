import requests

# Ollama runs a local server on this address once it's installed and running.
# We send it a POST request with our message, and it responds with the
# model's answer.
url = "http://localhost:11434/api/chat"

payload = {
    "model": "llama3.1",
    "messages": [
        {"role": "user", "content": "Hello! Can you confirm you're working?"}
    ],
    "stream": False  # get the full response at once, instead of word-by-word
}

response = requests.post(url, json=payload)
data = response.json()

print(data["message"]["content"])