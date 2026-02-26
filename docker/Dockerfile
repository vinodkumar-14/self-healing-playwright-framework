# Use official Playwright Python image
FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

WORKDIR /ai_playwright_framework

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Allure
RUN apt-get update && \
    apt-get install -y wget unzip && \
    wget https://github.com/allure-framework/allure2/releases/download/2.27.0/allure-2.27.0.zip && \
    unzip allure-2.27.0.zip -d /opt/ && \
    ln -s /opt/allure-2.27.0/bin/allure /usr/bin/allure

# Copy Project
COPY . .

# Install browser
RUN playwright install --with-deps

CMD ["pytest"]