from scrapy_playwright.page import PageMethod
from datetime import datetime, timezone
import scrapy
import json
import re

js_script = """
            async () => {
                const delay = ms => new Promise(res => setTimeout(res, ms));
                for (let i = 0; i <= 10; i++) {
                        const btn = document.evaluate(
                        '//button[contains(., "Lebih Banyak")]',
                        document,
                        null,
                        XPathResult.FIRST_ORDERED_NODE_TYPE,
                        null).singleNodeValue;
                        if(!btn) break;
                        btn.click();
                        window.scrollTo(0, document.body.scrollHeight);
                        await delay(3000)
                }
            }   
            """

class deallsSpider(scrapy.Spider):
    name= "dealls"

    def start_requests(self):

        url = "https://dealls.com/?searchJob=data"
        url = "https://dealls.com"

        yield scrapy.Request(url=url,
                             callback=self.parse,
                             meta={
                                 "playwright":True,
                                 "playwright_include_page":True,
                                 "playwright_page_methods":[
                                     PageMethod("wait_for_load_state", "networkidle"),
                                     PageMethod("evaluate", js_script),
                                     PageMethod("content")
                                     ]
                             }
                            )
        return super().start_requests()
    
    def parse(self, response):
        job_links = response.css("a.rounded-lg[href*='/loker/']::attr(href)").getall()
        for link in job_links[-3:]:
            full_url = 'https://dealls.com' + link
            yield scrapy.Request(url=full_url, 
                                 callback=self.parse_job
                                #  meta={"playwright":True,
                                #        "playwright_page_methods":[
                                #            PageMethod("wait_for_selector","div.grid.w-full.grid-cols-1.gap-4.sm\\:grid-cols-2.lg\\:grid-cols-3.lg\\:gap-6")
                                #         ]
                                #  }
                  )
            
    def parse_job(self, response):
        # Job title
        job_title = response.css("h1 > tspan::text").get()

        # Company name
        company = response.css("h2.text-tertiary-violet-50::text").get()
        
        # Job details (contract, work setup, work location, experience, salary)
        details = response.css("ul.mt-0.flex.flex-col.gap-1.lg\\:mt-2 > *")
        details_list = []
        for detail in details:
            text = detail.css("span > a::text").getall()
            if any(text):
                for i in text:
                    details_list.append(i)
            else:
                text = detail.css("span::text").get()
                details_list.append(text)

        # Job description
        job_desc = response.xpath("//h3[contains(text(), 'Deskripsi Pekerjaan')]/following-sibling::div//li/text()").getall()
        
        # Qualifications
        job_quali = response.xpath("//h3[contains(text(), 'Kualifikasi')]//following-sibling::div//li/text()").getall()
        
        yield {
            "job_url":response.url,
            "job_title":job_title,
            "company_name":company,
            "job_details":details_list,
            "job_desc":job_desc,
            "job_quali":job_quali,
            "scrapped_at_utc":datetime.now(timezone.utc).strftime("%Y-%m-%d_%H:%M:%S")
        }

        

