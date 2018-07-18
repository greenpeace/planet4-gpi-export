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

import csv
import urllib2

locale.setlocale(locale.LC_ALL, '')

class AllSpider(scrapy.Spider):
    name = 'all'

    custom_settings = {
        'ROBOTSTXT_OBEY': 0,
        'FEED_URI': 'gpeuunit_v1_test.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def start_requests(self):

        #v1
        start_urls = {
            'http://www.greenpeace.org/eu-unit/en/News/2016/209-pesticides-used-in-the-EU-could-endanger-humans-or-environment/':('News','NATURE & FOOD','Pesticides','Farming','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Advocate-General-opinion-EU-Singapore-deal/':('News','DEMOCRACY & EUROPE','Trade','EUaffairs','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/bee-harming-pesticides-banned-EFSA-reports/':('News','NATURE & FOOD','Pesticides','Farming','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/TTIP-Q-and-A-unpacking-EU-US-trade-talks/':('News','DEMOCRACY & EUROPE','Trade','','Migrate','Briefing'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/Improved-EU-decision-making-in-the-area-of-health-and-consumer-protection/':('News','POLLUTION','Health','EUaffairs','Migrate','Letter'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/Bratislava-summit-Europe-at-a-crossroads/':('Publications','DEMOCRACY & EUROPE','EUaffairs','Democracy','Migrate','Letter'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/CETA-SandD-progressive-trade-principles/':('Publications','DEMOCRACY & EUROPE','Trade','','Migrate','Briefing'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/Civil-society-calls-for-a-new-Europe-for-people-and-planet/':('Publications','DEMOCRACY & EUROPE','EUaffairs','Democracy','Migrate','Letter'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/Commission-fails-to-regulate-new-GMOs-after-intense-US-lobbying/':('Publications','NATURE & FOOD','GMOs','Transparency','Migrate','Briefing'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/Leaked-TiSA-texts-reveal-threats-to-climate-/':('Publications','DEMOCRACY & EUROPE','Trade','ClimateChange','Migrate','Report')
        }

        for url,data in start_urls.iteritems():
            post_type, categories, tags1, tags2, action, p4_post_type = data
            if ( post_type=='Publications' or post_type=='News' ):
                request = scrapy.Request(url, callback=self.parse_news, dont_filter='true')

            if ( action.lower()=='migrate' ):
                request.meta['status'] = 'publish'
            if ( action.lower()=='archive' ):
                request.meta['status'] = 'draft'
            request.meta['categories'] = categories
            request.meta['tags1'] = tags1
            request.meta['tags2'] = tags2
            request.meta['action'] = action
            request.meta['p4_post_type'] = p4_post_type
            request.meta['p4_title'] = ""
            yield request

    def parse_news(self, response):

        def extract_with_css(query):
            return response.css(query).extract_first()

        imagesA=response.xpath('//div[@class="text"]/div[not(@id) and not(@class)]//a[img]/@href').extract()
        imagesA_generated = list()
        for image_file in imagesA:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.org/',1)
            imagesA_generated.append(image_file)

        imagesB=response.xpath('//div[@class="text"]//img/@src').extract()
        if len(imagesB) == 0:
            imagesB = response.xpath('//div[@id="article"]//img/@src').extract()

        imagesB_generated = list()
        for image_file in imagesB:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.org/',1)
            # Custom fix for GPBR only.
            if 'http://assets.pinterest.com/images/PinExt.png' not in image_file:
                imagesB_generated.append(image_file)

        pdfFiles=response.css('div.article a[href$=".pdf"]::attr(href)').extract()
        pdf_files_generated = list()
        for pdf_file in pdfFiles:
            print pdf_file
            if (pdf_file.startswith('/')):
                pdf_file = pdf_file.replace('/','http://www.greenpeace.org/',1)
                print pdf_file
            pdf_files_generated.append(pdf_file)
            print pdf_files_generated

        image_gallery=response.xpath("//*[contains(@class, 'embedded-image-gallery')]")
        p3_image_gallery = 'false'
        if image_gallery:
            p3_image_gallery = 'true'

        lead_text = response.xpath('//*[@id="content"]/div[3]/div/div[2]/div[1]/div/text()').extract()[0]
        body_text = response.xpath('//*[@id="content"]/div[3]/div/div[2]/div[2]').extract()[0]
        if body_text:
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.org/').replace('href="/', 'href="http://www.greenpeace.org/')
            body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)
            if lead_text:
                body_text = '<h4 class="leader">' + lead_text + '</h4>' + body_text
            body_text = body_text + response.xpath(' //*[@id="content"]/div[3]/div/div[2]/p').extract_first()
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.org/').replace('href="/', 'href="http://www.greenpeace.org/')

        body_text = self.filter_post_content(body_text)

        subtitle = extract_with_css('div.article h2 span::text')
        if subtitle:
            body_text = '<h2>' + subtitle + '</h2><br />' + body_text

        #thumbnail = response.xpath('string(head//link[@rel="image_src"]/@href)').extract_first()

        date_field = response.css('div.article div.text span.author::text').re_first(r' - \s*(.*)')

        if date_field:
            date_field = dateutil.parser.parse(date_field)


        # Filter email id image and replace it with email text.
        delete_images = list()
        for image_file in imagesB_generated:
            if ("/emailimages/" in image_file):
                api_url = "http://localhost_test/test_script/email_img_to_text.php"
                end_point_url = api_url+"?url="+image_file
                emailid = urllib2.urlopen(end_point_url).read(1000)
                delete_images.append(image_file)
                # Remove the email images from Post body and replace it with email text.
                body_text = re.sub(
                    '<img[a-zA-Z0-9="\s\_]*src=\"'+image_file+'\"[a-zA-Z0-9="\s]*>',
                    emailid, body_text)

        # Remove the email images from list.
        for image_file in delete_images:
            imagesB_generated.remove(image_file)


        """
        #list images urls
        for image_file in imagesB_generated:
            if ("/emailimages/" in image_file):
                data = [image_file]
                self.csv_writer(data, "email_images_url_list.csv")
        """

        p4_title = response.meta['p4_title']
        if (p4_title == ""):
            p4_title = extract_with_css('div.article h1 span::text')


        # To fix enlarge Images still leads to p3 issue - find and replace the anchor tag image link with src image link.
        delete_images_a = list()
        for image_file_a in imagesA_generated:
            for image_file_b in imagesB_generated:
                filename_a = image_file_a.split("/")[-1]
                filename_b = image_file_b.split("/")[-1]

                if filename_a == filename_b:
                    #print "file names match " + filename_a
                    body_text = body_text.replace(image_file_a, image_file_b)
                    delete_images_a.append(image_file_a)

        # Remove the replaced enlarge images from list.
        for del_image_file_a in delete_images_a:
            imagesA_generated.remove(del_image_file_a)


        yield {
            'type': response.meta['p4_post_type'],
            'p3_image_gallery': p3_image_gallery,
            'title': p4_title,
            #'subtitle': '',
            'author': 'Greenpeace European Unit',
            'author_username': 'greenpeace',
            #'date': response.css('#content > div.happen-box.article > div > div.text > span').re_first(r' - \s*(.*)'),
            'date': date_field,
            #'lead': extract_with_css('div.news-list div.post-content *:first-child strong::text'),
            'lead': '',
            'categories': response.meta['categories'],
            #'text':  response.css('div.news-list div.post-content').extract_first(),
            'text':  body_text,
            'imagesA': imagesA_generated,
            #'imagesB': response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img[not(ancestor::a)]/@src').extract(), #don't import image if there's an a tag around it
            'imagesB': imagesB_generated,
            'imagesC': response.xpath('//div[@class="gallery"]//div[@class="img-nav"]//a/@rel').extract(), # Galleries (horrible html)
            'pdfFiles': pdf_files_generated,
            'tags1': response.meta['tags1'],
            'tags2': response.meta['tags2'],
            'url': response.url,
        }

    def filter_post_content(self, post_data):
        """
        # Filter the youtube video and add embed shortcode instead.
        post_data = re.sub(
            '\<iframe[width\=\"height0-9\s]*src\=\"([https]*\:\/\/www.youtube.com[a-zA-Z0-9\/\=\-\?\_]*)\"[\=\"a-zA-Z\/\-\s0-9]*\>[\\n\s]*(.*)[\\n\s]*\<\/iframe\>',
            '[embed]\g<1>[/embed]', post_data)

        # Search and replace youtube url with https.
        post_data = post_data.replace('http://www.youtube.com', 'https://www.youtube.com')
        """
        # Remove the <script> tags from content.
        post_data = re.sub(
            '<script[\s\S]type\=\"text\/javascript\"*?>[\s\S]*?<\/script>',
            '', post_data)

        return post_data

    def csv_writer(self, data, path):
        # Write data to a CSV file path
        with open(path, "a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(data)
