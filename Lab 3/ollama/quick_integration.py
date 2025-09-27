# quick_integration.py
# Minimal example: call local Ollama (phi3:mini) and print the response.

import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "phi3:mini"

def ask_ollama(question: str) -> str:
    """Send a prompt to the local Ollama server and return the response text."""
    try:
        r = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": question,
                "stream": False
            },
            timeout=120,  # seconds
        )
        r.raise_for_status()
        data = r.json()
        return data.get("response", "No response")
    except requests.exceptions.RequestException as e:
        return f"[ERROR] Request failed: {e}"

if __name__ == "__main__":
    # A simple one-shot example:
    question = "What's the weather like?"
    print(">> Prompt:", question)
    answer = ask_ollama(question)
    print("<< Answer:", answer)

    # Optional: quick interactive loop (uncomment to use)
    # print("\nType your questions (type /bye to exit):")
    # while True:
    #     q = input("You: ").strip()
    #     if q.lower() in ("/bye", "exit", "quit"):
    #         break
    #     print("AI:", ask_ollama(q))
