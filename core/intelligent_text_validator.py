
# core/intelligent_text_validator.py

from core.dom_scanner import DOMScanner
from ai_agents.generic_error_agent import GenericErrorAgent


class IntelligentTextValidator:
    """
    Generic intelligent text validation.
    Works across entire application.
    """

    def __init__(self, page):
        self.page = page
        self.dom_scanner = DOMScanner(page)
        self.ai_agent = GenericErrorAgent()

    def validate_text(
            self,
            expected_locator: str,
            expected_text: str,
            parent_locator: str = None
        ):
        try:
            actual_text = self.page.locator(expected_locator).inner_text(timeout=5000)

            if expected_text in actual_text:
                print(f"✅ Validation Passed: '{expected_text}' found")
                return True

        except Exception:
            pass

        # ❌ Validation failed — trigger AI analysis

        scoped_dom = self.dom_scanner.get_scoped_dom(parent_locator)
        error_candidates = self.dom_scanner.find_error_candidates(parent_locator)

        context = {
            "expected_text": expected_text,
            "expected_locator": expected_locator,
            "error_candidates": error_candidates,
            "dom": scoped_dom
        }

        print("\n🧠 AI TEST FAILURE ANALYSIS")

        ai_result = self.ai_agent.analyze(context)

        raise AssertionError(
            f"""
            ❌ TEXT VALIDATION FAILED
            
            Expected Text: '{expected_text}'
            Expected Locator: '{expected_locator}'
            
            Detected Application Error: {ai_result.get('detected_error')}
            Suggested Locator: {ai_result.get('suggested_locator')}
            Reason: {ai_result.get('reason')}
            """
        )

