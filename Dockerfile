FROM mcr.microsoft.com/playwright/python:v1.55.0-noble

WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies (Scrapy, Playwright, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# # Install Playwright browsers (Chromium)
# RUN playwright install --with-deps chromium

# Set Scrapy command
CMD ["scrapy", "crawl", "dealls"]
