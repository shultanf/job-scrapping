from scrapy_playwright.page import PageMethod
from scrapy.http import HtmlResponse
import scrapy
import json
import re


class linkedinSpider(scrapy.Spider):
    name = "linkedin"

    def start_requests(self):
        login_url = 'https://www.linkedin.com/login/'


        yield scrapy.Request(url=login_url, callback=self.parse, meta={"playwright":True,
                                                                       "playwright_include_page": True})
    
    async def parse(self, response):
        page = response.meta["playwright_page"]

        # Fill login input
        username = 'shultan.faris157@gmail.com'
        password = 'rukna1-dobnuc-zebdoJ'
        await page.fill("input[id='username']", username)
        await page.fill("input[id='password']", password)

        # Click submit
        await page.click("button[type='submit']")

        # Wait for selector
        await page.wait_for_selector("div.artdeco-card.overflow-hidden.p4.mb2")

        
        # Go to Jobs page
        await page.goto("https://www.linkedin.com/jobs/search/?keywords=data")

        html = await page.content()

        new_response = HtmlResponse(url=page.url, body=html, encoding='utf-8')

        job_list = new_response.xpath('//*[@id="main"]/div/div[2]/div[1]/div/ul/li')
        
        job_links = []
        job_titles = []
        for job in job_list:
            job_title = job.css("a::text").get()
            job_link = job.css("a::attr(href)").get()
            job_links.append(job_link)
            job_titles.append(job_title)
        yield {
            "job_links":job_links,
            "job_links_len":len(job_links),
            # "job_list":job_list,
            "job_list_len":len(job_list)
        }

        await page.close()



        # <h1 class="t-24 t-bold inline"><a href="/jobs/view/4319111437/?alternateChannel=search&amp;eBP=CwEAAAGaWD7qnYxm-TzqFRDKShqVhMHlMk1beAY5NrWsuhimg1_M-Ud3k7f-Unme96PGD1yzL2k-LK_ghlCAkuY_3D_bFAt62HC1gjHhrzDzp494JaH-isY2hT1znHHb0c7hbkeU1yhcjFV9-0J1F_yuGyIhqolLowpk0JjbTMW5VmtdVsd2bXUuSozk6ubulEx5G5rJRs6G3o8xiibMWhRIq_3ZEiRhxf9xA4EoFRoxWFGWPxlQOc72HvDGOzXVhJsFw3OWDqYiXz7SDwuMzYPR4vWtUxJQQZ6g_Cxan804Xar0yzfqSaNtKI0IsrN3q7kxAJQS7shgcWtYkxi-HMzjUXBjjDFC6WCTpooVulDsIMntmCY5cJstd2BdrP-vohksFDy33GFE3hFblx_KrDq2425NODcKmWPDGXka0Ba844uwNUUZJIIVb-OYh01BXo5Hda6Y1low1eraSaxX18DuBK__Di9Nu1tKkEdgXiwaDLkJced7GYruU9odIXT5xC0B1TKZmmyLAQ&amp;refId=Tnw%2BV24lUzT%2BCHM55KE%2BUQ%3D%3D&amp;trackingId=q%2BW8Jdh2PtMIyDBey1KhEA%3D%3D&amp;trk=d_flagship3_search_srp_jobs" id="ember124" class="ember-view">Data Engineer</a></h1>