
import subprocess
import allure
import pytest
import shutil
import os

from datetime import datetime
from playwright.sync_api import sync_playwright

from ai_agents.failure_analysis_agent import FailureAnalysisAgent

ALLURE_RESULTS_DIR = "allure-results"
ALLURE_REPORT_DIR = "allure-report"
ALLURE_HISTORY_DIR = os.path.join(ALLURE_REPORT_DIR, "history")


@pytest.fixture(scope="function")
def page(request):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(record_video_dir='reports/videos/')
        page = context.new_page()
        yield page

        # 🔥 After test finishes
        video = page.video
        context.close()  # Important: video is saved only after context.close()

        if video:
            video_path = video.path()

            test_name = request.node.name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            new_name = f"{test_name}_{timestamp}.webm"
            new_path = os.path.join("reports/videos", new_name)

            os.rename(video_path, new_path)

            print(f"Video saved as: {new_path}")

            allure.attach.file(
                new_path,
                name="Execution Video",
                attachment_type=allure.attachment_type.WEBM
            )

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
            page.screenshot(path="reports/screenshots/failure.png")

            # Call AI test-level analysis
            ai_result = FailureAnalysisAgent.analyze_test_failure(
                error_message,
                url
            )

            print("\n🧠 AI TEST FAILURE ANALYSIS")
            print(ai_result)

def pytest_configure(config):
    os.makedirs("reports", exist_ok=True)
    os.makedirs("reports/screenshots", exist_ok=True)
    os.makedirs("reports/videos", exist_ok=True)

def pytest_sessionstart(session):
    """
    Copy previous Allure history before tests start.
    """
    if os.path.exists(ALLURE_HISTORY_DIR):
        history_dst = os.path.join(ALLURE_RESULTS_DIR, "history")

        if os.path.exists(history_dst):
            shutil.rmtree(history_dst)

        shutil.copytree(ALLURE_HISTORY_DIR, history_dst)
        print("✅ Allure history copied successfully.")
    else:
        print("ℹ️ No previous Allure history found.")

def pytest_sessionfinish(session, exitstatus):
    """
    Generate Allure report automatically after tests finish.
    """
    print("\n📊 Generating Allure Report...")

    subprocess.run(
        [
            "allure",
            "generate",
            ALLURE_RESULTS_DIR,
            "-o",
            ALLURE_REPORT_DIR,
            "--clean",
        ],
        check=False,
    )

    print("✅ Allure report generated successfully.")
