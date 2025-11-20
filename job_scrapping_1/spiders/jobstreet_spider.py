import scrapy
import json
import re

class jobstreetSpider(scrapy.Spider):
    name = "jobstreet"

    def start_requests(self):
        url = "https://id.jobstreet.com/id/data-jobs"

        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        xpath_jobs = '//*[@id="app"]/div/div[6]/div/section/div[2]/div/div/div[1]/div/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div'
        jobs = response.xpath(xpath_jobs)
        # job_link =jobs[0].css("article > div > a::attr(href)").get()
        job_link =jobs[0].xpath("//article/div/a/@href").get()

        yield {
            "jobs_len":len(jobs),
            "job_sample":jobs[0],
            "job_link_sample":job_link
        }