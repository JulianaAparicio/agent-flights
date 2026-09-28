import json
import traceback
import requests
from flight_tool import search_cheapest_flight

OLLAMA_URL = "http://localhost:11434/api/chat"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_cheapest_flight",
            "description": "Searches for the cheapest round-trip flight between two airports on given dates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "from_airport": {"type": "string", "description": "Departure airport IATA code, e.g. MIA"},
                    "to_airport": {"type": "string", "description": "Destination airport IATA code, e.g. EZE"},
                    "departure_date": {"type": "string", "description": "Departure date in YYYY-MM-DD format"},
                    "return_date": {"type": "string", "description": "Return date in YYYY-MM-DD format"},
                },
                "required": ["from_airport", "to_airport", "departure_date", "return_date"],
            },
        },
    }
]

AVAILABLE_FUNCTIONS = {
    "search_cheapest_flight": search_cheapest_flight,
}


def ask_agent(messages):
    print("[DEBUG] Starting ask_agent...")
    # "messages" now comes in already built, containing the full
    # conversation history so far (not just the latest question).

    print("[DEBUG] Sending first request to Ollama...")
    response = requests.post(OLLAMA_URL, json={
        "model": "llama3.1",
        "messages": messages,
        "tools": TOOLS,
        "stream": False,
    })
    print(f"[DEBUG] Ollama responded with status code: {response.status_code}")
    response.raise_for_status()

    data = response.json()
    print(f"[DEBUG] Raw response: {data}")

    model_message = data["message"]
    tool_calls = model_message.get("tool_calls")

    if not tool_calls:
        print("[DEBUG] Model did not request any tool call.")
        return model_message["content"]

    print(f"[DEBUG] Model requested {len(tool_calls)} tool call(s).")
    messages.append(model_message)

    for call in tool_calls:
        function_name = call["function"]["name"]
        arguments = call["function"]["arguments"]
        print(f"[Agent is calling tool: {function_name} with {arguments}]")

        function_to_call = AVAILABLE_FUNCTIONS[function_name]
        result = function_to_call(**arguments)
        print(f"[DEBUG] Tool result: {result}")

        messages.append({
            "role": "tool",
            "content": json.dumps(result),
        })

    print("[DEBUG] Sending second request to Ollama with tool results...")
    final_response = requests.post(OLLAMA_URL, json={
        "model": "llama3.1",
        "messages": messages,
        "tools": TOOLS,
        "stream": False,
    })
    final_response.raise_for_status()
    return final_response.json()["message"]["content"]


def run_conversation():
    # This list holds the ENTIRE conversation, not just one message.
    # Every time we send something to Ollama, we send this whole history,
    # so the model has context from earlier in the chat.
    conversation_history = []

    print("Flight Agent ready. Ask me about flights (type 'quit' to exit).\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["quit", "exit", "salir"]:
            print("Goodbye!")
            break

        conversation_history.append({"role": "user", "content": user_input})

        try:
            reply = ask_agent(conversation_history)
            print(f"\nAgent: {reply}\n")
            conversation_history.append({"role": "assistant", "content": reply})
        except Exception:
            print("\n[ERROR] Something went wrong:")
            traceback.print_exc()


if __name__ == "__main__":
    run_conversation()