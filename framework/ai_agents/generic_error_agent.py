
import json

from framework.core.ai_engine import AIEngine


class GenericErrorAgent:
    """
    AI Agent responsible for analyzing validation failures
    across the web application.
    """

    def __init__(self, config):
        self.engine = AIEngine(config)

    def analyze(self, context: dict) -> dict:
        prompt = self._build_prompt(context)
        return self.engine.generate(prompt)

    @staticmethod
    def _build_prompt(context: dict) -> str:
        return f"""
        You are an AI Test Failure Analyst.
        
        The automation expected the following:
        
        Expected Text: {context['expected_text']}
        Expected Locator: {context['expected_locator']}
        
        Error-like elements found in DOM:
        {json.dumps(context['error_candidates'], indent=2)}
        
        DOM Snapshot:
        {context['dom'][:3000]}
        
        Analyze why the expected text was not found.

        If an application error message is provided, include it explicitly in your response
        under the key:
        
        Application Error Message (if detected in DOM):
        {context.get('application_error')}
        
        Return ONLY valid JSON in this exact format:
        
        {{
          "application_error_message": "<exact UI error message if present, otherwise null>",
          "detected_error": "<short error summary>",
          "suggested_locator": "<better locator if applicable>",
          "reason": "<clear explanation of what happened>"
        }}
        """
