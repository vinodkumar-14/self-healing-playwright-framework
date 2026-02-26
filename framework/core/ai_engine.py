
import requests
import json
import os


class AIEngine:
    """
    Handles communication with local Ollama model.
    Ensures structured JSON output and safe parsing.
    """

    def __init__(self, config, model: str = None):
        self.url = config.ollama_url
        # self.url = "http://localhost:11434/api/chat"
        self.model = model or os.getenv(config.ollama_url, config.ollama_model)

    def generate(self, prompt: str) -> dict:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json"  # 🔥 Force JSON response
        }

        try:
            response = requests.post(self.url, json=payload, timeout=60)
            response.raise_for_status()

            raw_output = response.json().get("response", "")

            try:
                return json.loads(raw_output)
            except json.JSONDecodeError:
                # AI did not return proper JSON — fallback safely
                return {
                    "detected_error": "Unknown",
                    "suggested_locator": "N/A",
                    "reason": raw_output.strip()
                }

        except Exception as e:
            return {
                "detected_error": "AI Engine Failure",
                "suggested_locator": "N/A",
                "reason": str(e)
            }
