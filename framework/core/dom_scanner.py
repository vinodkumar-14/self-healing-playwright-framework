

class DOMScanner:
    """
    Extracts scoped DOM and finds possible error elements.
    """

    def __init__(self, page):
        self.page = page

    def get_scoped_dom(self, parent_locator: str = None) -> str:
        try:
            if parent_locator:
                return self.page.locator(parent_locator).inner_html()
            return self.page.content()
        except Exception:
            return ""

    def find_error_candidates(self, parent_locator: str = None):
        candidates = []

        scope = self.page.locator(parent_locator) if parent_locator else self.page

        selectors = [
            "[role='alert']",
            "[data-test*='error']",
            "[class*='error']",
            ".error-message-container",
            "h3"
        ]

        for selector in selectors:
            try:
                elements = scope.locator(selector).all()
                for el in elements:
                    text = el.inner_text().strip()
                    if text:
                        candidates.append({
                            "selector": selector,
                            "text": text
                        })
            except Exception:
                continue

        return candidates
