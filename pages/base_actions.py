
from difflib import SequenceMatcher

import allure

class BaseActions:
    base_timeout = 5000 # 5 secs

    def __init__(self, page):
        self.page = page

    @allure.step("Enter text into locator: {locator}")
    def enter_text(self, locator, text, timeout=base_timeout, similarity_threshold: float = 0.75):
        try:
            self.page.fill(locator, text, timeout=timeout)
        except Exception as original_exception:
            print("Initial click failed ❌")
            print(f"Error: {original_exception}")
            print("Starting self-healing process...")

            try:
                # 🔎 Extract clickable elements
                clickable_elements = self.page.eval_on_selector_all(
                    "text, input[type=text]",
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

                # 🧠 Collect structured candidates
                candidates = []

                for element in clickable_elements:
                    if element["id"]:
                        candidates.append({"attr": "id", "value": element["id"]})
                    if element["name"]:
                        candidates.append({"attr": "name", "value": element["name"]})
                    if element["dataTest"]:
                        candidates.append({"attr": "data-test", "value": element["dataTest"]})

                print("Structured candidates:", candidates)

                if not candidates:
                    raise original_exception

                raw_locator = locator.replace("#", "").replace(".", "")

                best_match = None
                best_score = 0

                for candidate in candidates:
                    score = SequenceMatcher(None, raw_locator, candidate["value"]).ratio()
                    if score > best_score:
                        best_score = score
                        best_match = candidate

                print(f"Best match: {best_match}")
                print(f"Similarity score: {best_score}")

                if best_match and best_score >= similarity_threshold:

                    if best_match["attr"] == "id":
                        healed_locator = f"#{best_match['value']}"
                    elif best_match["attr"] == "name":
                        healed_locator = f"[name='{best_match['value']}']"
                    elif best_match["attr"] == "data-test":
                        healed_locator = f"[data-test='{best_match['value']}']"

                    print(f"Retrying with healed locator: {healed_locator}")

                    self.page.fill(healed_locator, text, timeout=timeout)
                    print("Self-healing successful ✅")
                    allure.attach(
                        str(best_match),
                        name="Healing Match Info",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    return

                print("No strong fuzzy match found. Healing failed.")

            except Exception as healing_exception:
                print("Healing process failed ❌")
                print(f"Healing error: {healing_exception}")

            # ❌ If everything fails, raise original error
            print("Raising original exception.")
            raise original_exception

    @allure.step("Click on the locator: {locator}")
    def click(self, locator: str, timeout=base_timeout, similarity_threshold: float = 0.75):
        try:
            print(f"Attempting to click locator: {locator}")
            self.page.click(locator, timeout=timeout)
            print("Click successful ✅")
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
