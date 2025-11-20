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

        yield scrapy.Request(url=url,
                             callback=self.parse,
                             meta={
                                 "playwright":True,
                                 "playwright_include_page":True,
                                 "playwright_page_methods":[
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

        


    def parse_jobb(self, response, **kwargs):
        # xpath_jobs = '//*[@id="__next"]/div[3]/main/div[2]/div[3]/div/a'
        # jobs = response.xpath(xpath_jobs)

        jobs = response.css("a.rounded-lg")
        
        for job in jobs:
            # Job title
            title = job.css("div.font-bold::text").get()

            # Company name
            company = job.css("div.flex.items-center.gap-\\[4\\.6px\\]::text").get()
            
            # Details
            details = job.css("div.mb-1\\.5.flex.flex-col.gap-1.lg\\:mb-3 > div")
            details_list = []
            for index, detail in enumerate(details):
                if index == 0:
                    text = detail.css("span > button::text").get()
                    details_list.append(text)
                else:
                    text = detail.css("span::text").get()
                    details_list.append(text)

            # Job contract (full-time, part-time, contract, etc)
            # contract = details_list[0]
            # contract = job.css("div.flex.items-center.gap-2.text-neutral-100.text-xs.md\\:text-sm span::text").get()

            # Work location and setup (on-site, hybrid, remote, etc.)
            # xpath_workplace = './/div/div[1]/div[2]/div[2]/span'
            # workplace = response.xpath(f"{xpath_workplace}/text()").getall()
            # workplace = job.css("flex items-center gap-2 text-neutral-100 text-xs md:text-sm")

            # workplace = details_list[1].split("•")
            # work_setup = workplace[0].lower().strip()
            # work_location = workplace[-1].lower().strip()

            yield {
                "title":title,
                "company":company,
                "details":[detail for detail in details_list],
                # "contract":contract,
                # "workplace": workplace,
                # "work_setup": work_setup,
                # "work_location": work_location
            }

            # # Min. qualification
            # xpath_qualification = './/div/div[1]/div[2]/div[3]/span'
            # min_qualification = response.xpath(f"{xpath_qualification}/text()").get().lower()

            # # is_experience_needed = bool(re.search(r'\bexperience\b', min_qualification))
            # # if is_experience_needed == True:
            # #     min_years_experience = re.findall(r'/d+', min_qualification)[0]
            # # else:
            # #     min_years_experience = None

            # # Salary
            # xpath_salary = './/div/div[1]/div[2]/div[4]/span' + '/text()'
            # salary = response.xpath(xpath_salary).getall()

        # next = ''