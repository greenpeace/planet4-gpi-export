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
z

locale.setlocale(locale.LC_ALL, '')

class DataSpider(scrapy.Spider):
    name = 'data'

    custom_settings = {
        'ROBOTSTXT_OBEY': 0,
        'FEED_URI': 'gp-master_test.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    __connector_csv_filename = "connector_v2_final_.csv"
    __connector_csv_log_file = "connector_csv_log_v2"

    base_urls = 'http://p3-raw.greenpeace.org/'
    total_pages = 1713

    def start_requests(self):

        # V1
        start_urls = {
            'http://www.greenpeace.org/eastasia/news/blog/will-chinese-tech-giant-huawei-dethrone-apple/blog/60980/': (
            'Blog', 'Live Sustainably', '', 'Detox', '', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/rethinking-it-saving-the-world-one-gadget-at-/blog/59772/': (
            'Blog', 'Live Sustainably', '', 'Detox', '', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/powering-up-meet-the-women-electrifying-china/blog/58885/': (
            'Blog', 'Climate & Energy', '', 'Renewable Energy', '', '', 'news-list', 'Migrate'),

        }

        start_urls = {
            1:'http://p3-raw.greenpeace.org/international/en/',
            2:'http://p3-raw.greenpeace.org/international/en/#tab=0&gvs=false&page=2',
            3:'http://p3-raw.greenpeace.org/international/en/#tab=0&gvs=false&page=3',
            4:'http://p3-raw.greenpeace.org/international/en/#tab=0&gvs=false&page=4',
            5:'http://p3-raw.greenpeace.org/international/en/#tab=0&gvs=false&page=5',
        }

        print "data"

        pagination_links = {}
        # for page_num in range(self.total_pages):
        for page_num in range(1):
            pagination_links.update({page_num: self.base_urls + 'international/en/#tab=0&gvs=false&page=' + str(page_num)})

        # print "all links >>>>>>>>>>"
        # print pagination_links
        # pagination_links = scrapy.Request(start_urls, callback=self.extract_pagination_links, dont_filter='true')
        #
        # print "in main function......."
        # print pagination_links
        #
        # print "start url"
        # print start_urls

        # override
        start_urls = pagination_links

        for page_num,list_page_link in start_urls.iteritems():
            request = scrapy.Request(list_page_link, callback=self.extract_post_links, dont_filter='true')

            yield request

    # Extract pagination links from listing page.
    def extract_pagination_links(response):

        last_pagination_links = response.css('div.paginator ul li:last-child a::attr(href)').extract()

        print "in sub function......."
        print last_pagination_links

        post_links = list()
        for post_link in raw_post_links:
            if (post_link.startswith('/')):
                post_link = post_link.replace('/', self.base_urls, 1)
                post_links.append(post_link)

        # print "post link list =<<<<<<<<<<<<<"
        # print pdf_files_generated

        return last_pagination_links
        # yield {
        #     'page': post_links,
        # }

    # Extract links from listing page
    def extract_post_links(self, response):

        raw_post_links = response.css('div.tabs-holder h3 a::attr(href)').extract()

        post_links = list()
        for post_link in raw_post_links:
            if (post_link.startswith('/')):
                post_link = post_link.replace('/', self.base_urls , 1)
                post_links.append(post_link)

        # print "post link list =<<<<<<<<<<<<<"
        # print pdf_files_generated

        yield {
            'page' : post_links,
        }

    def filter_post_content(self, post_data):
        # Filter the youtube video and add embed shortcode instead.
        post_data = re.sub(
            '\<object[width\=\"height0-9\s]*data\=\"([https]*\:\/\/www.youtube.com[a-zA-Z0-9\/\=\-\?\_]*)\"[\=\"a-zA-Z\/\-\s0-9]*\>[\\n\s]*(.*)[\\n\s]*\<\/object\>',
            '[embed]\g<1>[/embed]', post_data)

        return post_data

    # Filter month name function is not needed for english speaking sites
    def filter_month_name(self, month_name):

        month_ro_en = {
            'Ocak': 'January',
            'ינואר': 'January',
            'Şubat': 'February',
            'פברואר': 'February',
            'מרץ': 'March',
            'אפריל': 'April',
            'Mayıs': 'May',
            'מאי': 'May',
            'יוני': 'June',
            'יולי': 'July',
            'אוגוסט': 'August',
            'ספטמבר': 'September',
            'אוקטובר': 'October',
            'Kasım': 'November',
            'נובמבר': 'November',
            'דצמבר': 'December',
        }

        # Replace the romanian month name with english month name.
        for ro_month, en_month in month_ro_en.iteritems():
            month_name = month_name.replace(ro_month, en_month)

        return month_name;

    def csv_writer(self, data, path):
        # Write data to a CSV file path
        with open(path, "a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(data)
