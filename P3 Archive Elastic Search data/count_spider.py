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

class CountSpider(scrapy.Spider):
    name = 'count'

    # P3 base url.
    base_urls = 'http://p3-raw.greenpeace.org/'

    # P3 posts counts list csv file.
    csv_post_counts_per_nro = 'gp-post_count_all_final.csv'

    source_csv_path = 'nro_search_list.csv'

    # Log file path.
    scrapper_error_log = 'count-post_scrapper_error_log.txt'

    custom_settings = {
        'ROBOTSTXT_OBEY': 0,
        'FEED_URI': 'gp-post_count_data_per_nro_test_new.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def start_requests(self):

        post_links = {}

        # Check number of lines in csv file.
        #num_lines = sum(1 for line in open(self.source_csv_path))
        #print num_lines

        line_num = 0
        with open(self.source_csv_path, 'r') as csv_file:  # Opens the file in read mode
            csv_reader = csv.reader(csv_file)  # Making use of reader method for reading the file

            for line in csv_reader:  # Iterate through the loop to read line by line
                line_num += 1
                #print line[0]
                # Extract selected number of post links from CSV file.
                post_links.update({line_num: line[0]})

        # print post_links
        for page_num, post_link in post_links.iteritems():
            # print post_link
            request = scrapy.Request(post_link, callback=self.parse_all_post, dont_filter='true')
            yield request


        # post_links = {
        #     1:'http://p3-raw.greenpeace.org/international/en/System-templates/Search-results/?tab=0&ps=10&all=+',
        #     2:'http://p3-raw.greenpeace.org/africa/en/Search-results/?all=+',
        #     3:'http://p3-raw.greenpeace.org/africa/fr/Search-results/?all=+',
        #     4:'http://p3-raw.greenpeace.org/argentina/es/System-templates/footer-links/Busca-en-esta-pagina/?all=+',
        #     5:'http://p3-raw.greenpeace.org/australia/en/System-templates/Site-Settings-Pages/Search/?all=+',
        #     6:'http://p3-raw.greenpeace.org/belgium/fr/system-templates/recherche/?all=+',
        #     7:'http://p3-raw.greenpeace.org/belgium/nl/system-templates/zoek/?all=+',
        # }
        #
        # # print post_links
        # for page_num,post_link in post_links.iteritems():
        #     # print post_link
        #     request = scrapy.Request(post_link, callback=self.parse_all_post, dont_filter='true')
        #     yield request



    # handle all types of post/pages content type.
    def parse_all_post(self, response):

        def extract_with_css(query):
            return response.css(query).extract_first()

        check_count_div = extract_with_css('div.basicsearch ul li a')
        imagesA_generated = list()

        if check_count_div is None:
            data = [response.url,'"basicsearch" div not found...' ]
            self.csv_writer(data, self.scrapper_error_log)
        else:
            #print 'i am here...'
            # taxonomy = response.css('div.basicsearch ul li a').extract()
            # print taxonomy
            # taxonomy.insert(0, response.url)
            # self.csv_writer(taxonomy, self.csv_post_counts_per_nro)

            imagesA = response.xpath('//div[@class="basicsearch"]//a').extract()
            for image_file in imagesA:

                page_link = re.search('(?<=<a href=")[^"]+', image_file).group(0)
                page_title = re.search('(?<= title=")[^"]+', image_file).group(0)
                page_count = re.search('\(([\d]+)\)', image_file).group(0)

                page_link = page_link.replace('/', self.base_urls, 1)
                page_count = page_count.replace('(','',1)
                page_count = page_count.replace(')', '', 1)

                # print page_link
                # print page_title
                # print page_count

                imagesA_generated.append(image_file)

                data = [response.url, page_link, page_title, page_count]
                self.csv_writer(data, self.csv_post_counts_per_nro)

                break
                # match = re.search(r'href=[\'"]?([^\'" >]+)', image_file)
                # if match:
                #     print match.group(0)
                # match = re.search(r'n\>([\D]+)\<\/s', image_file)
                # if match:
                #     print match.group(0)
                # match = re.search(r'\(([\d]+)\)', image_file)
                # if match:
                #     print match.group(0)

                # print re.sub('<a.*>(.*)<\/a>', "\g<1>", image_file)
                # if (image_file.startswith('/')):
                #     image_file = image_file.replace('/', 'http://www.greenpeace.org/', 1)
                # imagesA_generated.append(image_file)


        # log errors...
        # log_data = list()
        # if post_title is None:
        #     log_data.append('title blank')
        #     # data = [response.url,'title blank' ]
        #     # self.csv_writer(data, self.scrapper_error_log)
        #
        # if body_text is None:
        #     log_data.append('body_text blank')
        #     # data = [response.url,'body_text blank' ]
        #     # self.csv_writer(data, self.scrapper_error_log)
        #
        # if date_field is None:
        #     log_data.append('date_field blank')
        #     # data = [response.url,'date_field blank' ]
        #     # self.csv_writer(data, self.scrapper_error_log)
        #
        # if len(log_data):
        #     log_data.insert(0, response.url)
        #     log_data.append('func ' + func_name)
        #     self.csv_writer(log_data, self.scrapper_error_log)

        yield {
            'count': imagesA_generated,
            'url': response.url,
        }

    # class = 'happen-box article'
    # pagetypes = parse_publication,parse_press,parse_feature
    def parse_article_list(self, response):

        def extract_with_css(query):
            return response.css(query).extract_first()

        try:
            lead_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[1]/div/text()').extract()[0]
        except IndexError:
            lead_text = ''

        try:
            body_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[2]').extract()[0]
        except IndexError:
            body_text = ''

        if body_text == '':
            try:
                body_text = response.xpath('//*[@id="content"]/div[5]/div/div[2]/div[2]').extract()[0]
            except IndexError:
                body_text = ''

        if body_text:
            # body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            # body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)
            if lead_text:
                body_text = lead_text + body_text + response.xpath(
                    ' //*[@id="content"]/div[4]/div/div[2]/p').extract_first()
                # body_text = body_text + response.xpath(' //*[@id="content"]/div[4]/div/div[2]/p').extract_first()

        subtitle = extract_with_css('div.article h2 span::text')
        if subtitle:
            body_text = '<h2>' + subtitle + '</h2><br />' + body_text

        date_field = response.css('div.article div.text span.author::text').re_first(r' - \s*(.*)')
        date_field = self.filter_date_content(date_field)

        #post_title = extract_with_css('div.article h1 span::text')

        taxonomy = response.css('div.tags ul li a::text').extract()

        # yield {
        #     'title': post_title,
        #     'text': body_text,
        #     'date': date_field,
        #     'taxonomy': taxonomy,
        #     'url': response.url,
        #     'language': response.meta['language'],
        # }

        return [body_text, date_field, taxonomy, '']


    # Class = 'news-list'
    # pagetypes = blogs,news
    def parse_news_list(self, response):

        def extract_with_css(query):
            return response.css(query).extract_first()

        date_field = response.css('div.news-list .caption::text').re_first(r' - \s*(.*)')
        date_field = self.filter_date_content(date_field)

        body_text = response.css('div.news-list div.post-content').extract_first()
        #if body_text:
            # body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.org/').replace('href="/', 'href="http://www.greenpeace.org/')
            # body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            # body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)

        # body_text = self.filter_post_content(body_text)

        try:
            lead_text = response.xpath('string(//div[@class="news-list"]/ul/li/div[@class="post-content"]/div//*[self::p or self::h3 or self::h2][1])').extract()[0]
        except IndexError:
            lead_text = ''

        if lead_text:
            body_text = lead_text + body_text

        # blockquotes = response.xpath('//*[@id="content"]//blockquote').extract()
        # blockquotes_generated = list()
        # for blockquote in blockquotes:
        #     blockquotes_generated.append(blockquote)

        author_name = response.xpath('string(//div[@class="news-list"]/ul/li/*/*/span[@class="caption"]/span[@class="green1"]/strong)').extract()[0]
        if ( author_name ):
            author_name = author_name.strip()

        # post_title = extract_with_css('div.news-list h1::text')

        taxonomy = response.css('div.tags ul li a::text').extract()

        # yield {
        #     'title': post_title,
        #     'author': author_name,
        #     'date': date_field,
        #     #'lead': extract_with_css('div.news-list div.post-content *:first-child strong::text'),
        #     'lead': response.xpath('string(//div[@class="news-list"]/ul/li/div[@class="post-content"]/div//*[self::p or self::h3 or self::h2][1])').extract()[0],
        #     'text':  body_text,
        #     'blockquote': blockquotes_generated,
        #     'url': response.url,
        # }

        return [body_text, date_field, taxonomy, author_name]


    # class = 'happen-box article'
    # pagetypes = parse_publication,parse_press,parse_feature
    def parse_article_list1(self, response):

        def extract_with_css(query):
            return response.css(query).extract_first()

        try:
            lead_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[1]/div/text()').extract()[0]
        except IndexError:
            lead_text = ''

        body_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[2]').extract()[0]
        if body_text:
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/',
                                                                              'src="http://www.greenpeace.org/').replace(
                'href="/', 'href="http://www.greenpeace.org/')
            body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)
            if lead_text:
                body_text = '<div class="leader" style="font-weight: bold;margin-bottom: 12px">' + lead_text + '</div>' + body_text + response.xpath(
                    ' //*[@id="content"]/div[4]/div/div[2]/p').extract_first()
                # body_text = body_text + response.xpath(' //*[@id="content"]/div[4]/div/div[2]/p').extract_first()

        subtitle = extract_with_css('div.article h2 span::text')
        if subtitle:
            body_text = '<h2>' + subtitle + '</h2><br />' + body_text

        date_field = response.css('div.article div.text span.author::text').re_first(r' - \s*(.*)')
        # try:
        #     date_field = self.filter_month_name(date_field);
        #     # Filter extra string part from date.
        #     date_field = date_field.replace(" at", "")  # english
        #     date_field = date_field.replace(" à", "")
        #     date_field = date_field.replace(" kl.", "")
        #     date_field = date_field.replace(" v", "")
        #     date_field = date_field.replace(" en ", " ")  # spanish
        #     date_field = date_field.replace(" på ", " ")  # swedish
        #     date_field = date_field.replace(" di ", " ")  # indonesian
        #     date_field = date_field.replace(" na ", " ")  # slovenian
        #     date_field = date_field.replace(" o ", " ")  # polish
        # except IndexError:
        #     date_field = ""
        #
        # if date_field:
        #     date_field = dateutil.parser.parse(date_field)
        date_field = self.filter_date_content(date_field)

        post_title = extract_with_css('div.article h1 span::text')

        if post_title is None:
            data = [response.url,'title blank' ]
            self.csv_writer(data, self.scrapper_error_log)

        if body_text is None:
            data = [response.url,'body_text blank' ]
            self.csv_writer(data, self.scrapper_error_log)

        yield {
            'title': post_title,
            # 'subtitle': '',
            # 'author': 'Greenpeace East Asia',
            # 'date': response.css('#content > div.happen-box.article > div > div.text > span').re_first(r' - \s*(.*)'),
            'date': date_field,
            # 'lead': extract_with_css('div.news-list div.post-content *:first-child strong::text'),
            # 'lead': extract_with_css('#content > div.happen-box.article > div > div.text > div.leader > div'),
            # 'category1': response.meta['category1'],
            # 'category2': response.meta['category2'],
            # 'text':  response.css('div.news-list div.post-content').extract_first(),
            'text': body_text,
            # 'tags1': response.meta['tags1'],
            # 'tags2': response.meta['tags2'],
            # 'tags3': response.meta['tags3'],
            'url': response.url,
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

    # Filter date content.
    def filter_date_content(self, date_field):
        try:
            date_field = self.filter_month_name(date_field);
            # Filter extra string part from date.
            date_field = date_field.replace(" at", "")  # english
            date_field = date_field.replace(" à", "")
            date_field = date_field.replace(" kl.", "")
            date_field = date_field.replace(" v", "")
            date_field = date_field.replace(" en ", " ")  # spanish
            date_field = date_field.replace(" på ", " ")  # swedish
            date_field = date_field.replace(" di ", " ")  # indonesian
            date_field = date_field.replace(" na ", " ")  # slovenian
            date_field = date_field.replace(" o ", " ")  # polish
        except IndexError:
            date_field = ""

        if date_field:
            date_field = dateutil.parser.parse(date_field)

        return date_field

    def csv_writer(self, data, path):
        # Write data to a CSV file path
        with open(path, "a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(data)
