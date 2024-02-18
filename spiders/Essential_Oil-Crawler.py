import csv
from pathlib import Path
import scrapy
from scrapy.exporters import CsvItemExporter
class CrawlerOilSpider(scrapy.Spider):
    name = "crawler_ess_oil"
    allowed_domains = ["bioinfo.cimap.res.in"]
    start_urls = ["https://bioinfo.cimap.res.in/aromadb/web_essential_oil.php"]
     # To store in JSON format 
    custom_settings = { 
        'FEEDS': {'essential_oil.json': {'format': 'json', 'overwrite': True}} 
    } 

    def parse(self, response):
        serial_no=[]
        oil_name=[]
        plant_name=[]
        plant_var_name=[]
        plant_tiss_name=[]
        plant_comp_name=[]
        for row in response.xpath('//*[@class="table table-striped table-bordered table-condensed"]//tbody//tr'):
            ess_name=row.xpath('td[2]//text()')
            serial_no=[]
            serial_no.append(row.xpath('td[1]//text()').extract_first())
            oil_name.append(row.xpath('td[2]//text()').extract_first())
            plant_name.append(row.xpath('td[3]//text()').extract_first())
            plant_var_name.append(row.xpath('td[4]//text()').extract_first())
            plant_tiss_name.append(row.xpath('td[5]//text()').extract_first())
            plant_comp_name.append(row.xpath('td[6]//text()').extract_first())

            data= {"serialnumber:": serial_no,
                    
                    'Essential Oil Name': row.xpath('td[2]//text()').extract_first(),
          'Plant Name' : row.xpath('td[3]//text()').extract_first(),
          'Plant Variety Name' : row.xpath('td[4]//text()').extract_first(),
          'Plant Tissue Name': row.xpath('td[5]//text()').extract_first(),
           'Compound' : row.xpath('td[6]/a/text()').extract(),
                    }
            #yield data
            for next_page in row.xpath('td[7]/a/@href').extract_first():
                # Construct the absolute URL if the link is relative
                next_page_url = "https://bioinfo.cimap.res.in/aromadb/"+  row.xpath('td[7]/a/@href').extract_first()    # Yield a request to follow the link and pass additional data
                yield scrapy.Request(url=next_page_url, callback=self.parse_page, meta={'data': data})

    def parse_page(self, response):
        Compound_Name=[]
        Compound_Per=[]
        # crawl the pgae after opening the link of the next page where compound and its % is given     
        for row in response.xpath('//*[@class="table table-striped table-bordered table-condensed"]//tbody//tr'):
            Serial_N=[]
            Serial_N.append(row.xpath('td[1]//text()').extract_first())
            Compound_Name.append(row.xpath('td[2]//text()').extract_first())
            Compound_Per.append(row.xpath('td[3]//text()').extract_first())            
        additional_data = {
            #'Serial Number': Serial_N,
            'Compound Name': Compound_Name,
            'Compound Percentage(%)': Compound_Per,
            # Add more data extraction as needed
        }

        # Combine additional data with previously passed data
        data = response.meta['data']
        data.update(additional_data)

        # Yield the combined data
        yield data
        