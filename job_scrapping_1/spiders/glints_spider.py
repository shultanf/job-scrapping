from scrapy_playwright.page import PageMethod
from scrapy.http import HtmlResponse
import scrapy
import json
import re


class glintsSpider(scrapy.Spider):
    name = "glints"

    def start_requests(self):
        custom_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                                        "Chrome/119.0.0.0 Safari/537.36"
                                        }
        login_url = "https://glints.com/login"

        yield scrapy.Request(url=login_url, 
                             callback=self.parse_login, 
                             headers=custom_headers,
                             meta={
                                 "playwright":True,
                                 "playwright_include_page":True
                             })
        
    async def scroll_to_bottom(self, page):
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")

    async def parse_login(self, response):
        page = response.meta["playwright_page"]

        # Wait for the "Login with Email" button
        await page.wait_for_selector("a[aria-label='Login with Email button']")

        # Click it
        await page.click("a[aria-label='Login with Email button']")

        # Give yourself some time to see the page (use wait_for_timeout)
        await page.wait_for_timeout(5000)
        
        # Login
        email = "shultan.faris157@gmail.com"
        password = "Sketdance@157"
        await page.fill("input[id='login-form-email']", email)
        await page.wait_for_timeout(2000)
        await page.fill("input[id='login-form-password']", password)
        await page.wait_for_timeout(2000)
        await page.click("button[type='submit']")
        await page.wait_for_timeout(5000)

        # Job search
        job_search_url = 'https://glints.com/id/opportunities/jobs/explore?keyword=data&country=ID&locationName=All+Cities%2FProvinces&lowestLocationLevel=1&yearsOfExperienceRanges=NO_EXPERIENCE%2CFRESH_GRAD%2CLESS_THAN_A_YEAR'
        await page.goto(job_search_url)
        await page.wait_for_timeout(3000)

        # Extract job cards
        #xpath_job_cards = '//*[@id="__next"]/div[1]/div[2]/div[2]/div[3]/div[4]/div[2]/div[1]'
        html = await page.content()
        new_response = HtmlResponse(url=page.url, body=html, encoding='utf-8')
        job_cards_before = new_response.css("div[data-glints-tracking-element-name='job_card']")

        # # Extract job cards AFTER scroll
        # await page.wait_for_timeout(5000)
        # await self.scroll_to_bottom(page)
        # await page.wait_for_timeout(3000)
        # job_cards_after = new_response.xpath(xpath_job_cards)

        yield {
            "job_cards_before":job_cards_before
            # "job_cards_before":len(job_cards_before)
            #"job_cards_after":len(job_cards_after)
        }

        await page.close()

        # while True:
        #     await page.wait_for_load_state("domcontentloaded", timeout=3000)
        #     await self.scroll_to_bottom(page)

