
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"


class FailureAnalysisAgent:

    @staticmethod
    def classify_failure(locator, error_message):
        """
        Determines whether failure is likely due to locator mismatch.
        """

        # prompt = f"""
        # You are an automation debugging assistant.
        #
        # Locator used: {locator}
        # Error message: {error_message}
        #
        # Is this most likely:
        # 1. LOCATOR_MISMATCH
        # 2. PAGE_NOT_LOADED
        # 3. CREDENTIAL_ISSUE
        # 4. UNKNOWN
        #
        # Respond with only one option.
        # """
        #
        # response = requests.post(
        #     OLLAMA_URL,
        #     json={
        #         "model": MODEL,
        #         "prompt": prompt,
        #         "stream": False
        #     }
        # )
        #
        # result = response.choices[0].message.content.strip().upper()
        #
        # if "LOCATOR_MISMATCH" in result:
        #     return "LOCATOR_MISMATCH"
        # elif "TIMEOUT" in result:
        #     return "TIMEOUT"
        # elif "VISIBILITY" in result:
        #     return "VISIBILITY"
        # else:
        #     return "UNKNOWN"
        if "waiting for locator" in error_message.lower():
            return "LOCATOR_MISMATCH"

        if "timeout" in error_message.lower():
            return "TIMEOUT"

        if "not visible" in error_message.lower():
            return "VISIBILITY"

        return "UNKNOWN"

    @staticmethod
    def suggest_locator(old_locator, dom_buttons):
        prompt = f"""
        You are a Playwright self-healing engine.
    
        The following locator failed:
        {old_locator}
    
        Available button elements:
        {dom_buttons}
    
        Return ONLY a valid CSS selector.
        Do NOT explain.
        Do NOT use markdown.
        Return a single-line selector only.
        Example: #login-button
        """

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            }
        )

        locator = response.json()["response"].strip()

        # Sanitize output
        locator = locator.replace("`", "").replace("```", "")
        locator = locator.split("\n")[0].strip()

        print("AI raw locator response:", locator)

        return locator

    @staticmethod
    def analyze_test_failure(error_message, url):
        """
        High-level test failure analysis.
        """

        prompt = f"""
        You are a senior automation debugging assistant.

        Test failed.
        URL: {url}
        Error: {error_message}

        Classify failure type:
        - LOCATOR_ISSUE
        - ASSERTION_FAILURE
        - BACKEND_ERROR
        - TEST_DATA_ISSUE
        - UNKNOWN

        Also provide short explanation.
        """

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            }
        )

        return response.json()["response"].strip()
