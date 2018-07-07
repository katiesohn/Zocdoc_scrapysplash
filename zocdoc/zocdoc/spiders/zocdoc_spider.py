


from scrapy import Spider, Request
from zocdoc.items import ZocdocItem
from scrapy_splash import SplashRequest


class ZocdocSpider(Spider):
	name = 'zocdoc_spider'
	allowed_url = ['https://www.zocdoc.com/']	
	# start_urls = ['https://www.zocdoc.com/primary-care-doctors/new-york-46063pm#dr_specialty='
	# + str(i) + '&address=New+York%2C+NY&insurance_carrier=-1&insurance_plan=-1&reason_visit=&gender=-1&language=-1&PatientTypeChild=&offset=' + str(i) '&referrerType=&sort_selection=0&name=&searchQuery=&searchQueryGuid=5e59dbf2-0954-449c-a8ed-ec1aa5cd9953&hasNoSearchResults=false&hospitalid=-1&timeFilter=AnyTime&dayFilter=0&procedureChanged=true&languageChanged=false'
	#    	for i in range(151, 251)]

	start_urls = ['https://www.zocdoc.com/']
	# urls = ['https://www.zocdoc.com/primary-care-doctors/new-york-46063pm#dr_specialty='
	# + str(i) for i in range(151, 250)]
	# start_urls = []
	# for url in urls:
	# 	for i in range(0, 101, 10):
	# 		start_urls.append(url + '&address=New+York%2C+NY&offset=' + str(i))
	

	# print(start_urls)
	# print("@" * 50)

	# start_urls = ['https://www.zocdoc.com/primary-care-doctors/new-york-46063pm?dr_specialty=153&address=New+York%2C+NY&reason_visit=75&insurance_carrier=-1&insurance_plan=-1&gender=-1&language=-1&patienttypechild=&offset='
	#  + str(i) +
	#   '&referrertype=&sort_selection=0&name=&searchquery=&searchqueryguid=7f8f858c-6045-4a2b-9367-bbbbb064d2e2&hasnosearchresults=false&hospitalid=-1&timefilter=AnyTime&dayfilter=0&procedurechanged=false&languagechanged=false&&isfromajax=true'
	#    for i in range(0, 11, 10)]
	#categories = response.xpath('//select[@id="reason_visit"]/option/text()').extract() #these are the categories in the drop down
	#cat_length = len(categories)

	#for category in range(cat_length+1) #want it to iterate through all the categories 
	# category_links = ['https://www.zocdoc.com/primary-care-doctors/new-york-46063pm#dr_specialty='
	# + str(i) + '&address=New+York%2C+NY&insurance_carrier=-1&insurance_plan=-1&reason_visit=&gender=-1&language=-1&PatientTypeChild=&offset=0&referrerType=&sort_selection=0&name=&searchQuery=&searchQueryGuid=5e59dbf2-0954-449c-a8ed-ec1aa5cd9953&hasNoSearchResults=false&hospitalid=-1&timeFilter=AnyTime&dayFilter=0&procedureChanged=true&languageChanged=false'
	#    	for i in range(151, 251)]

	def parse(self, response): #response is from making a request to start_url

		specialties = ['https://www.zocdoc.com/primary-care-doctors/new-york-46063pm#dr_specialty='
		+ str(i) for i in range(151, 251)]
		specialties_1 = []
		for specialty in specialties:
			for i in range(0, 101, 10):
				specialties_1.append(specialty + '&address=New+York%2C+NY&offset=' + str(i))

		for url in specialties_1:
			yield SplashRequest(url=url, callback=self.parse_specialty, args = {"wait": 2}, endpoint = "render.html")
		
	def parse_specialty(self,response):
		# for url in specialties_1:
		# 	print(url)
		# 	print("^" * 50)
		# 	yield SplashRequest(url=url, callback=self.parse_listings, args = {"wait": 2}, endpoint = "render.html")

		links = response.xpath('//div[@class="js-search-prof-row-rating-comment ch-prof-row-rating-comment-container"]/a/@href').extract()
		links = ['https://www.zocdoc.com' + link for link in links] 
		#the above is giving the list of URLs 


		for url in links: 
			yield SplashRequest(url=url, callback=self.parse_details, args = {"wait": 2}, endpoint = "render.html") #instead of yielding
			#item we are yielding new request to the URL

	def parse_details(self,response): 

		doctor = response.xpath('//span[@itemprop="name"]/text()').extract_first()
		doctor_type = response.xpath('//h2[@class="vqj10x-8 eIxxDs ofapnq-0-h2 dHIeUX"]/text()').extract()
		overall_rating = response.xpath('//svg[@class="vqj10x-10 kEVYLj s17gvxzw-0 gGGFdQ s1piosrx-0 ewiPkd"]/@data-rating').extract()
		practice = response.xpath('//a[@data-test="profile-practice-link" and  @tabindex="0"]/text()').extract()
		board_certs=response.xpath('//section[3]/ul/li[@class="s14a81gn-3 elerUy"]/text()').extract()
		education = response.xpath('//li[@class="s14a81gn-3 elerUy"]/span/text()').extract()
		gender = response.xpath('//section[@data-test="Sex-section"]/p/text()').extract()
		street_address = response.xpath('//p[@itemprop="streetAddress"]/text()').extract()
		city_state = response.xpath('//p[@data-test="city-state-zip"]/span/text()').extract()
		overall_patient_ratings = response.xpath('//div[@class="psfp1a-2 lcIktU"]/div/svg/@data-rating').extract()
		zoc_awards = response.xpath('//div[@class="ir1q6m-0 jeeSmD"]/div/div/div/svg/@data-test').extract()
		languages = response.xpath('//section[@data-test="Languages-section"]/ul/li/text()').extract()
		npi = response.xpath('//p[@itemprop="identifier"]/text()').extract()


		item = ZocdocItem()
		item['doctor'] = doctor
		item['doctor_type'] = doctor_type
		item['overall_rating'] = overall_rating
		item['practice'] = practice
		item['board_certs'] = board_certs
		item['education'] = education
		item['gender'] = gender
		item['street_address'] = street_address
		item['city_state'] = city_state
		item['overall_patient_ratings'] = overall_patient_ratings
		item['zoc_awards'] = zoc_awards
		item['languages'] = languages
		item['npi'] = npi

		yield item

		# print(doctor)
		# print(doctor_type)
		# print(overall_rating)
		# #print(specialties)
		# print(practice)
		# print(board_certs)
		# print("#" * 50)
		# print(education)
		# print(gender)
		# print(street_address)
		# print(city_state)
		# print("$" * 50)
		# print(overall_patient_ratings)
		# print(zoc_awards)

