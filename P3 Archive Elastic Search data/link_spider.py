#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import scrapy
import logging
import locale
import dateutil.parser
import re
import dateparser
from datetime import datetime, date
import random
import time
import csv
import urllib2

locale.setlocale(locale.LC_ALL, '')

class LinkSpider(scrapy.Spider):
    name = 'link'

    custom_settings = {
        'ROBOTSTXT_OBEY': 0,
        'FEED_URI': 'gp-international-all_new.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    __connector_csv_filename = "connector_v2_final_.csv"
    __connector_csv_log_file = "connector_csv_log_v2"

    base_urls = 'http://p3-raw.greenpeace.org/'
    total_pages = 1825
    nro_url = base_urls + 'international/en/'

    output_filename = 'international-post_list-all-new.csv'

    #search_page = nro_url + 'System-templates/Search-results/?tab=1&ps=10&all=+&page='

    search_page = 'http://p3-raw.greenpeace.org/international/en/System-templates/Search-results/?tab=0&all=+&page='

    def start_requests(self):

        pagination_links = {}
        # Generate pagination urls
        for page_num in range(self.total_pages):
        #for page_num in range(1, 11):

            # pagination_links.update({page_num: self.nro_url + '#tab=0&gvs=false&page=' + str(page_num)})
            pagination_links.update({page_num: self.search_page + str(page_num)})

        for page_num,list_page_link in pagination_links.iteritems():
            #print list_page_link
            request = scrapy.Request(list_page_link, callback=self.extract_post_links, dont_filter='true')

            yield request

    # Extract links from listing page
    def extract_post_links(self, response):

        raw_post_links = response.css('div.tabs-holder h3 a::attr(href)').extract()

        post_links = list()
        for post_link in raw_post_links:
            if (post_link.startswith('/')):
                post_link = post_link.replace('/', self.base_urls , 1)
                post_links.append(post_link)
                # List p3 posts link
                data = [post_link]
                self.csv_writer(data, self.output_filename)

        # print "post link list =<<<<<<<<<<<<<"
        # print pdf_files_generated

        yield {
            'page' : post_links,
        }

    def csv_writer(self, data, path):
        # Write data to a CSV file path
        with open(path, "a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(data)
