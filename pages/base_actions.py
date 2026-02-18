
from ai_agents.failure_analysis_agent import FailureAnalysisAgent
from difflib import get_close_matches
from difflib import SequenceMatcher


class BaseActions:
    base_timeout = 30000 # 30 secs

    def __init__(self, page):
        self.page = page

    def click(self, locator: str, similarity_threshold: float = 0.75):
        try:
            print(f"Attempting to click locator: {locator}")
            self.page.click(locator, timeout=5000)
            print("Click successful ✅")
            return

        except Exception as original_exception:
            print("Initial click failed ❌")
            print(f"Error: {original_exception}")
            print("Starting self-healing process...")

            try:
                # 🔎 Extract clickable elements
                clickable_elements = self.page.eval_on_selector_all(
                    "button, input[type=submit], input[type=button]",
                    """
                    elements => elements.map(e => ({
                        tag: e.tagName,
                        id: e.id,
                        name: e.name,
                        dataTest: e.getAttribute('data-test')
                    }))
                    """
                )

                print("Extracted clickable elements:", clickable_elements)

                # 🧠 Collect candidate attributes
                candidates = []
                for element in clickable_elements:
                    for value in [element["id"], element["name"], element["dataTest"]]:
                        if value:
                            candidates.append(value)

                print("Candidate attributes:", candidates)

                if not candidates:
                    print("No candidates found. Cannot heal.")
                    raise original_exception

                # 🔍 Extract raw locator value (remove # or .)
                raw_locator = locator.replace("#", "").replace(".", "")

                # 🎯 Fuzzy matching
                best_match = None
                best_score = 0

                for candidate in candidates:
                    score = SequenceMatcher(None, raw_locator, candidate).ratio()
                    if score > best_score:
                        best_score = score
                        best_match = candidate

                print(f"Best match: {best_match}")
                print(f"Similarity score: {best_score}")

                # ✅ If good enough → retry click
                if best_match and best_score >= similarity_threshold:
                    healed_locator = f"#{best_match}"
                    print(f"Retrying with healed locator: {healed_locator}")
                    self.page.click(healed_locator, timeout=5000)
                    print("Self-healing successful ✅")
                    return

                print("No strong fuzzy match found. Healing failed.")

            except Exception as healing_exception:
                print("Healing process failed ❌")
                print(f"Healing error: {healing_exception}")

            # ❌ If everything fails, raise original error
            print("Raising original exception.")
            raise original_exception
