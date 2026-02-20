
import json

from core.ai_engine import AIEngine


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
        
        Return ONLY valid JSON in this exact format:
        
        {{
          "detected_error": "<short error summary>",
          "suggested_locator": "<better locator if applicable>",
          "reason": "<clear explanation of what happened>"
        }}
        """
