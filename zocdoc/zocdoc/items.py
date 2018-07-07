# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZocdocItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    doctor = scrapy.Field()
    doctor_type = scrapy.Field()
    practice = scrapy.Field()
    education = scrapy.Field()
    gender = scrapy.Field()
    street_address = scrapy.Field()
    city_state = scrapy.Field()
    languages = scrapy.Field()
    board_certs = scrapy.Field()
    overall_rating = scrapy.Field()
    overall_patient_ratings = scrapy.Field()
    zoc_awards = scrapy.Field()
    npi = scrapy.Field()

