from scrapy import Spider, Request
from zocdocreviews.items import ZocdocreviewsItem
from scrapy_splash import SplashRequest


class ZocdocreviewsSpider(Spider):
	name = 'zocdocreviews_spider'
	allowed_url = ['https://www.zocdoc.com/']
	start_urls = ['https://www.zocdoc.com/']

	def parse(self, response): #response is from making a request to start_url

		specialties = ['https://www.zocdoc.com/primary-care-doctors/new-york-46063pm#dr_specialty='
		+ str(i) for i in range(220, 251)]
		specialties_1 = []
		for specialty in specialties:
			for i in range(0, 101, 10):
				specialties_1.append(specialty + '&address=New+York%2C+NY&offset=' + str(i))

		for url in specialties_1:
			yield SplashRequest(url=url, callback=self.parse_specialty, args = {"wait": 2}, endpoint = "render.html")


	def parse_specialty(self,response):

		links = response.xpath('//div[@class="js-search-prof-row-rating-comment ch-prof-row-rating-comment-container"]/a/@href').extract()
		links = ['https://www.zocdoc.com' + link for link in links] 
		#the above is giving the list of URLs 

		for url in links: 
			yield SplashRequest(url=url, callback=self.parse_details, args = {"wait": 2}, endpoint = "render.html") 


	def parse_details(self,response): 

		doctor = response.xpath('//span[@itemprop="name"]/text()').extract_first()
		doctor_type = response.xpath('//h2[@class="vqj10x-8 eIxxDs ofapnq-0-h2 dHIeUX"]/text()').extract()

		# print(doctor)
		# print(doctor_type)
		# print("$"*50)


		reviews = response.xpath('//div[@class="iw11ga-0 iRmoTf"]')

		for review in reviews:
			text = review.xpath('.//*[@class="iw11ga-1 fxAeuW"]/div/span/text()').extract_first()
			name = review.xpath('.//*[@class="iw11ga-2 kydqFg"]/span/span/text()').extract_first()
			print(text)
			print(name)
			print("!" *50)

			item = ZocdocreviewsItem()
			
			item['doctor'] = doctor
			item['doctor_type'] = doctor_type
			item['name'] = name
			item['text'] = text

			yield item


		# item = ZocdocreviewsItem()
		# item['doctor'] = doctor
		# item['doctor_type'] = doctor_type


		# yield item

