# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import boto3
import json



class JobScrapping1Pipeline:
    def process_item(self, item, spider):
        job_details = item["job_details"]
        self.output = {
            "url":item["job_url"],
            "title":item["job_title"],
            "company":item["company_name"],
            "contract":job_details[0],
            "work_setup":job_details[1],
            "location":job_details[2],
            "experience":job_details[3],
            "salary":job_details[4],
            "scrapped_at_utc":item["scrapped_at_utc"]
        }
    
    def open_spider(self, spider):
        # Upload to data lake
        s3 = boto3.client("s3")

        bucket_name = "job_scrapping_sf"
        key = f"dealls/dealls_{self.output["scrapped_at_utc"]}"

        s3.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=json.dumps(self.output),
            ContentType='application/json'
        )