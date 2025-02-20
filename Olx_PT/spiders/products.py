import scrapy
import json
from Olx_PT.items import OlxPtItem


class ProductsSpider(scrapy.Spider):
    name = "products"
    domains = "https://www.olx.pt/"
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"}     
    collecting_data = {}    

    def start_requests(self):
        yield scrapy.Request(
                url=self.domains,
                method="GET",
                headers=self.headers,
                callback=self.parse
        )

    def parse(self, response):
        category = response.xpath('//div[@data-testid="home-categories-menu"]/div[@data-testid="home-categories-menu-row"]/a[@class="css-1ep67ka"]/@href').extract_first()
        link = self.domains + category + "carros"
        
        yield scrapy.Request(
            url=link,
            method="GET",
            headers=self.headers,
            callback=self.car_request
        )
    def request_page(self, url):
        yield scrapy.Request(
            url=url,
            method="GET",
            headers=self.headers,
            callback= self.car_request
        )
 
    def car_request(self, response):
        for get_link in response.xpath('//div[@class="css-1apmciz"]/div[@data-cy="ad-card-title"]/a[@class="css-qo0cxu"]/@href').getall():
            link = self.domains + get_link
            

            yield scrapy.Request(
                url=link,
                method="GET",
                headers=self.headers,       
                callback=self.cars
            )
            yield from self.page(response)

    def cars(self, response):
        path_json = response.xpath('//script[@type="application/ld+json"]/text()').extract_first()
        json_info =  json.loads(path_json)

        self.collecting_data["Title"] = json_info["name"]
        self.collecting_data["Model"] = json_info["model"]
        self.collecting_data["Price"] = json_info["offers"]["price"]
        self.collecting_data["Brand"] = json_info["brand"]
        self.collecting_data["production_data"] = json_info["productionDate"]
        self.collecting_data["City"] = json_info["offers"]["areaServed"]["name"]
        self.collecting_data["Description"] = json_info["description"]#.raplace("✅", "")

        yield OlxPtItem(
            self.collecting_data
        )
         


    def page(self, response):
        print
        link_page = response.xpath('//div[@data-testid="pagination-wrapper"]/ul/a[@data-testid="pagination-forward"]/@href').get()
        if link_page:
            url = self.domains + link_page
            yield from self.request_page(url)       





