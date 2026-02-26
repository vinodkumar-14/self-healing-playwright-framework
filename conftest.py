
import subprocess
import allure
import pytest
import shutil
import os

from playwright.sync_api import sync_playwright
from pymongo import MongoClient
from datetime import datetime

from framework.ai_agents.failure_analysis_agent import FailureAnalysisAgent
from framework.config.config_reader import ConfigReader
from framework.pages.login_page import LoginPage
from framework.pages.inventory import Inventory

ALLURE_RESULTS_DIR = "allure-results"
ALLURE_REPORT_DIR = "allure-report"
ALLURE_HISTORY_DIR = os.path.join(ALLURE_REPORT_DIR, "history")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

client = MongoClient(MONGO_URI)
db = client["self_healing"]
collection = db["failures"]


@pytest.fixture(scope="session")
def headless():
    return ConfigReader()

@pytest.fixture(scope="function")
def page(request, config):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=config.headless)
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

        page.close()
        browser.close()


@pytest.fixture(scope="session")
def config():
    return ConfigReader()

@pytest.fixture
def login(page, config):
    return LoginPage(page, config)

@pytest.fixture
def inventory(page, config):
    return Inventory(page, config)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page", None)

        if page:
            failure_data = {
                "test_name": item.name,
                "nodeid": item.nodeid,
                "error": str(report.longrepr),
            }

            try:
                collection.insert_one(failure_data)
                print(f"[SELF-HEALING] Failure logged for {item.name}")
            except Exception as e:
                print(f"[SELF-HEALING WARNING] Could not log to MongoDB: {e}")

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

# def pytest_runtest_call(item):
#     for i in range(2):  # retry once
#         try:
#             item.runtest()
#             return
#         except Exception as e:
#             if i == 1:
#                 raise
#             print(f"[SELF-HEALING] Retrying {item.name}")

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

def pytest_generate_tests(metafunc):
    if "user_data" in metafunc.fixturenames:
        config = ConfigReader()
        metafunc.parametrize("user_data", config.get_users())
