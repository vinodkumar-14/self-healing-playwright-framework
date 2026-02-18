
import pytest
from playwright.sync_api import sync_playwright

from ai_agents.failure_analysis_agent import FailureAnalysisAgent

@pytest.fixture(scope="function")
def page():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(record_video_dir='videos/')
        page = context.new_page()
        yield page
        context.close()
        browser.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page", None)

        if page:
            error_message = str(report.longrepr)
            url = page.url

            # Capture screenshot
            page.screenshot(path="failure.png")

            # Call AI test-level analysis
            ai_result = FailureAnalysisAgent.analyze_test_failure(
                error_message,
                url
            )

            print("\n🧠 AI TEST FAILURE ANALYSIS")
            print(ai_result)

