## Step 1: Install Python
```
python3 --version
```

---

## Step 2: Clone and Create Virtual Environment
```
git clone https://github.com/vinodkumar-14/ai-playwright-framework.git

python3 -m venv venv
source venv/bin/activate  # Mac/Linux
```

---

## Step 3: Install Dependencies
```
pip install -r requirements.txt
playwright install
```

---

## Step 4: Install Ollama (Free Local LLM)
Install Ollama: https://ollama.com
### Download
`curl -fsSL https://ollama.com/install.sh | sh`
### Pull Model
`ollama pull mistral`
### Run Test
`ollama run mistral`

---

## Step 5: Allure report
`brew install allure`

---

## Step 6: Run Tests
`pytest`

`pytest tests/test_login.py`

---

# 🤖 AI-Powered Self-Healing Playwright Framework

## 📌 Overview

This project is an AI-powered self-healing test automation framework built using **Python + Playwright**.

The goal of this framework is to reduce test failures caused by minor UI locator changes by automatically detecting and healing broken locators at runtime.

Instead of failing immediately when a locator changes (e.g., `loginbutton` → `login-button`), the framework intelligently analyzes the DOM, identifies similar elements, and retries the action using the best match.

---

## 🚀 Problem Statement

In traditional UI automation frameworks:

- Small locator changes break tests
- Engineers must manually update selectors
- CI/CD pipelines fail due to minor UI updates
- Maintenance cost increases over time

This framework solves that by introducing a **self-healing layer**.

---

## 🧠 How the Self-Healing Engine Works

When an action like `click()` fails:

1. The framework catches the exception.
2. It scans the DOM for clickable elements:
   - `<button>`
   - `<input type="submit">`
   - `<input type="button">`
3. It extracts attributes such as:
   - `id`
   - `name`
   - `data-test`
4. It performs fuzzy matching against the failed locator.
5. If a strong similarity match is found:
   - It retries the action using the healed locator.
6. If deterministic healing fails:
   - The AI agent can analyze DOM context and suggest a new locator.

---

## 🤖 What the AI Agent Handles

The AI agent is responsible for:

- Analyzing locator mismatches
- Understanding DOM structure context
- Suggesting improved or alternative selectors
- Handling non-trivial UI changes
- Providing fallback locator strategies
- Reducing manual debugging effort

The AI is used only when deterministic healing (fuzzy matching) cannot confidently resolve the issue.

This ensures:
- Fast execution
- Minimal hallucination
- Enterprise-grade reliability

---

## Articles

[[Part 1] AI-Driven Test Automation: Self-Healing Framework You Can Run, Explore & Help Improve Using Ollama Model](https://www.linkedin.com/posts/vinodkumar-kouthal-692491a1_aitesting-testautomation-playwright-activity-7429927900419801089-rTiI?utm_source=share&utm_medium=member_desktop&rcm=ACoAABWbI44B2EpkSUdfhTGbZePX5mw_MpjwE4E)

[[Part 2] AI-Driven Test Automation: Detecting & Analysing Application Error Messages](https://www.linkedin.com/posts/vinodkumar-kouthal-692491a1_testautomation-ai-playwright-activity-7431243984120795137-Z70Q?utm_source=share&utm_medium=member_desktop&rcm=ACoAABWbI44B2EpkSUdfhTGbZePX5mw_MpjwE4E)

