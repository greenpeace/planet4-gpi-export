import scrapy
import logging
import locale
import dateutil.parser
import re
import dateparser
from datetime import datetime, date

locale.setlocale(locale.LC_ALL, '')

class AllSpider(scrapy.Spider):
    name = 'all'

    custom_settings = {
        'ROBOTSTXT_OBEY': 0,
        'FEED_URI': 'gpnz_test_batch_2.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def start_requests(self):

        start_urls = {
            # Story
            # - 1st batch
            'http://www.greenpeace.org/new-zealand/en/blog/life-aboard-the-stop-deep-sea-oil-flotilla/blog/34474/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/fonterra-embarrasses-the-government-over-palm/blog/33265/':('Story','Protect','Forests', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/petition-sign-the-deep-water-oil-drilling-in-/blog/24877/':('Story','Resist','Oil&Gas', 'Oceans', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/remember-the-rainbow-warrior-and-the-marshall/blog/24895/':('Story','Greenpeace','AboutUs', '', 'Migrate'),

            # - 2nd batch
            'http://www.greenpeace.org/new-zealand/en/blog/tiama-joins-the-flotilla-to-stop-deep-sea-oil/blog/34473/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/iwi-fishing-boat-disrupts-oil-survey-ship/blog/34408/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/stopping-deep-sea-oil-vanessas-log-12042011/blog/34252/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/stopping-deep-sea-oil-vanessas-log/blog/34249/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/vanessas-blog-seismic-events-at-sea/blog/34156/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/jefs-blog-toward-whangaparoa/blog/34155/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/fighting-spirit-at-flotilla-send-off/blog/33965/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/brownlee-and-oil-relics-of-a-dying-age/blog/24866/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/are-the-governments-deep-water-oil-plans-runn/blog/35784/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/police-protect-us-oil-giant-anadarkos-survey-/blog/37357/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/rena-oil-spill-an-unfortunate-lesson/blog/37226/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/the-oil-is-less-obvious-but-the-problem-is-sp/blog/37351/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/rena-oil-spill-could-make-deep-sea-oil-drilli/blog/37303/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/toxic-rena-oil-washes-ashore/blog/37291/':('Story','Resist','Oil&Gas', '', 'Migrate'),

            # Press Release
            # - 1st batch
            'http://www.greenpeace.org/new-zealand/en/press/John-Key-Should-Resign-as-Tourism-Minister-Greenpeace/':('Press Release','Protect','Freshwater', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Backdoor-talks-to-keep-coal-powering-NZ-an-absolute-disgrace/':('Press Release','Resist','Coal', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-Response-to-TPP-Protests/':('Press Release','Resist','Freedom', '', 'Migrate'),

            # - 2nd batch
            'http://www.greenpeace.org/new-zealand/en/press/Record-shattering-NASA-announcement-indicates-NZ-faces-extreme-weather-events/':('Press Release','Protect', 'Climate', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-activists-convicted-but-receive-no-further-punishment-over-10-hour-occupation-of-the-Tangaroa/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Governments-failing-oil-agenda-hits-hurdle-as-all-NZ-exploration-plans-are-trashed/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Genesis-letter/':('Press Release','Resist','Coal', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-launches-civil-disobedience-campaign-against-NZs-largest-oil-event/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Climate-action-a-matter-of-life-and-death-after-February-temperatures-smash-global-records/':('Press Release','Protect','Climate', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Landcorp-Ditches-Industrial-Dairy-Plans-Over-Pollution-Fears-Greenpeace-Response/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Whiskas-Embroiled-in-Modern-Day-Slavery-Scandal/':('Press Release','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Dairy-Irrigation-Subsidies-Must-Be-Ditched-to-Avert-Crisis-Greenpeace-Says/':('Press Release','Resist','Freedom', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-response-to-MRAG-Asia-Pacific-report-into-IUU-fishing-in-the-Pacific/':('Press Release','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/US-environmental-kingpin-Bill-McKibben-throws-his-weight-behind-civil-disobedience-in-NZ/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Hundreds-descend-on-Central-Auckland-to-blockade-NZs-largest-oil-event/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Oil-Block-Offer-a-Desperate-Last-Ditch-Bid-by-the-Government-to-Try-and-Save-Failing-Oil-Plans/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),

            # Publication
            # - 1st batch
            'http://www.greenpeace.org/new-zealand/en/reports/Made-in-Taiwan/':('Publication','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/global-wind-energy-outlook/':('Publication','Transform','Renewables', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/OIA-Docs-for-Thompson-and-Clark-MBIE-Relationship/':('Publication','Resist','Freedom', 'Oil&Gas', 'Migrate'),

            # - 2nd batch
            'http://www.greenpeace.org/new-zealand/en/reports/future-investment-energy/':('Publication','Transform','Renewables', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/the-power-and-appeal-of-wind/':('Publication','Transform','Renewables', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/dirty-old-coal/':('Publication','Resist','Coal', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/enviro-impacts-of-coal/':('Publication','Resist','Coal', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/Save-our-beaches-from-oil-disaster/':('Publication','Resist','Oil&Gas', 'Coal', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/Changing-Tuna/':('Publication','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/Out-Of-Our-Depth-Deep-sea-oil-exploration-in-New-Zealand/':('Publication','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/The-Future-is-Here-report/':('Publication','Transform','Renewables', 'Oil&Gas', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/Joint-Statement-on-Crown-Minerals-Bill-Amendment-2013/':('Publication','Resist','Oil&Gas', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/-Response-to-Minister-of-Energy-and-Resources-July-2013/':('Publication','Resist','Oil&Gas', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/New-Zealand-Oil-Spill-Report/':('Publication','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/Fewer-boats-more-fish/':('Publication','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/Out-of-line---The-failure-of-the-global-tuna-longline-fisheries/':('Publication','Protect','Oceans', '', 'Migrate'),
        }

        for url,data in start_urls.iteritems():
            post_type, categories, tags1, tags2, action = data
            if ( post_type=='Story' ):
                request = scrapy.Request(url, callback=self.parse_blog, dont_filter='true')
            elif ( post_type=='Publication' ):
                request = scrapy.Request(url, callback=self.parse_publication, dont_filter='true')
            elif ( post_type=='Press release' or post_type=='Press Release' ):
                request = scrapy.Request(url, callback=self.parse_press, dont_filter='true')
            elif ( post_type=='Feature' ):
                request = scrapy.Request(url, callback=self.parse_feature, dont_filter='true')

            if ( action.lower()=='migrate' ):
                request.meta['status'] = 'publish'
            if ( action.lower()=='archive' ):
                request.meta['status'] = 'draft'
            request.meta['categories'] = categories
            request.meta['tags'] = tags1
            request.meta['tags1'] = tags2
            request.meta['action'] = action
            yield request

    def parse_feature(self, response):

        def extract_with_css(query):
            return response.css(query).extract_first()

        image_gallery=response.xpath("//*[contains(@class, 'embedded-image-gallery')]")
        p3_image_gallery = 'false'
        if image_gallery:
            p3_image_gallery = 'true'

        imagesB=response.xpath('//*[@id="content"]//img/@src').extract()
        imagesB_generated = list()
        for image_file in imagesB:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.org/',1)
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

        date_field = response.xpath('//*[@id="content"]/div[4]/div/div[2]/span/text()').extract()[0]
        if (date_field.startswith('Feature story - ')):
            date_field = date_field.replace('Feature story - ','',1)
        if date_field:
            if (date_field.startswith('Feature story - ')):
                date_field = date_field.replace('Feature story - ','',1)
            date_field = dateutil.parser.parse(date_field)

        lead_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[1]/div').extract()[0]
        body_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[2]').extract()[0]
        if body_text:
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.org/').replace('href="/', 'href="http://www.greenpeace.org/')
            body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)
            if lead_text:
                body_text = '<div>' + lead_text + '</div>' + body_text + response.xpath(' //*[@id="content"]/div[4]/div/div[2]/p').extract_first()

        yield {
            'type': 'Story',
            'p3_image_gallery': p3_image_gallery,
            #'title': extract_with_css('#content > div.happen-box.article > h1::text'),
            'title': response.xpath('//*[@id="content"]/div[4]/h1/span/text()').extract()[0],
            'subtitle': extract_with_css('div.article h1 span::text'),
            'author': 'Greenpeace New Zealand',
            'date': date_field,
            #'lead': extract_with_css('div.news-list div.post-content *:first-child strong::text'),
            'lead': lead_text,
            'categories': response.meta['categories'],
            'text':  body_text,
            'imagesA': response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img/@src').extract(),
            'imagesB': imagesB_generated,
            #'imagesB': response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img[not(ancestor::a)]/@src').extract(), #don't import image if there's an a tag around it
            'imagesC': response.xpath('//div[@class="gallery"]//div[@class="img-nav"]//a/@rel').extract(), # Galleries (horrible html)
            'pdfFiles': pdf_files_generated,
            'tags': response.meta['tags'],
            'url': response.url,
        }


    def parse_blog(self, response):

        def extract_with_css(query):
            return response.css(query).extract_first()

        imagesA=response.xpath('//div[@class="news-list"]//div[@class="post-content"]//a[img]/@href').extract()
        imagesA_generated = list()
        for image_file in imagesA:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.org/',1)
            imagesA_generated.append(image_file)

        imagesB=response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img/@src').extract()
        imagesB_generated = list()
        for image_file in imagesB:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.org/',1)
            imagesB_generated.append(image_file)

        imagesEnlarge=response.xpath('//div[@class="news-list"]//div[@class="post-content"]//a[@class="open-img BlogEnlargeImage"]/@href').extract()
        imagesEnlarge_generated = list()
        for image_file in imagesEnlarge:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.org/',1)
            imagesEnlarge_generated.append(image_file)

        pdfFiles=response.css('div.article a[href$=".pdf"]::attr(href)').extract()
        pdf_files_generated = list()
        for pdf_file in pdfFiles:
            print pdf_file
            if (pdf_file.startswith('/')):
                pdf_file = pdf_file.replace('/','http://www.greenpeace.org/',1)
                print pdf_file
            pdf_files_generated.append(pdf_file)
            print pdf_files_generated

        date_field = response.css('div.news-list .caption::text').re_first(r' - \s*(.*)')
        if date_field:
            date_field = dateutil.parser.parse(date_field)

        image_gallery=response.xpath("//*[contains(@class, 'embedded-image-gallery')]")
        p3_image_gallery = 'false'
        if image_gallery:
            p3_image_gallery = 'true'

        body_text = response.css('div.news-list div.post-content').extract_first()
        if body_text:
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.org/').replace('href="/', 'href="http://www.greenpeace.org/')
            body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)

        images=response.xpath('//*[@class="post-content"]/div/p/a//img[contains(@style, "float:")]').extract()   #img[@style="margin: 9px; float: left;"]
        imagesD_generated = list()
        for image in images:
            imagesD_generated.append(image)

        blockquotes = response.xpath('//*[@id="content"]//blockquote').extract()
        blockquotes_generated = list()
        for blockquote in blockquotes:
            blockquotes_generated.append(blockquote)

        yield {
            'type': 'Story',
            'p3_image_gallery': p3_image_gallery,
            'title': extract_with_css('div.news-list h1::text'),
            #'subtitle': '',
            'author': response.xpath('string(//div[@class="news-list"]/ul/li/*/*/span[@class="caption"]/span[@class="green1"]/strong)').extract()[0],
            #'author_username': author_username,
            'date': date_field,
            #'lead': extract_with_css('div.news-list div.post-content *:first-child strong::text'),
            'lead': response.xpath('string(//div[@class="news-list"]/ul/li/div[@class="post-content"]/div//*[self::p or self::h3 or self::h2][1])').extract()[0],
            'categories': response.meta['categories'],
            'text':  body_text,
            'imagesA': imagesA_generated,
            'imagesEnlarge': imagesEnlarge_generated,
            'imagesB': imagesB_generated,
            'imagesC': response.xpath('//div[@class="gallery"]//div[@class="img-nav"]//a/@rel').extract(), # Galleries (horrible html)
            'imagesD': imagesD_generated,
            'blockquote': blockquotes_generated,
            'pdfFiles': pdf_files_generated,
            'tags': response.meta['tags'],
            'url': response.url,
            'status': response.meta['status'],
        }

    def parse_press(self, response):

        def extract_with_css(query):
            return response.css(query).extract_first()

        imagesA=response.xpath('//div[@class="news-list"]//div[@class="post-content"]//a[img]/@href').extract()
        imagesA_generated = list()
        for image_file in imagesA:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.org/',1)
            imagesA_generated.append(image_file)

        imagesB=response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img/@src').extract()
        imagesB_generated = list()
        for image_file in imagesB:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.org/',1)
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

        lead_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[1]/div/text()').extract()[0]
        body_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[2]').extract()[0]
        if body_text:
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.org/').replace('href="/', 'href="http://www.greenpeace.org/')
            body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)
            if lead_text:
                body_text = '<div>' + lead_text + '</div>' + body_text + response.xpath(' //*[@id="content"]/div[4]/div/div[2]/p').extract_first()

        yield {
            'type': 'Press Release',
            'p3_image_gallery': p3_image_gallery,
            'title': extract_with_css('div.article h1 span::text'),
            #'subtitle': '',
            'author': 'Greenpeace New Zealand',
            #'date': response.css('#content > div.happen-box.article > div > div.text > span').re_first(r' - \s*(.*)'),
            'date': dateutil.parser.parse(response.xpath('string(//*[@id="content"]/div[4]/div/div[2]/span)').extract()[0].replace('Press release - ', '')),
            #'lead': extract_with_css('div.news-list div.post-content *:first-child strong::text'),
            'lead': lead_text,
            'categories': response.meta['categories'],
            #'text':  response.css('div.news-list div.post-content').extract_first(),
            'text':  body_text,
            'imagesA': imagesA_generated,
            #'imagesB': response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img[not(ancestor::a)]/@src').extract(), #don't import image if there's an a tag around it
            'imagesB': imagesB_generated,
            'imagesC': response.xpath('//div[@class="gallery"]//div[@class="img-nav"]//a/@rel').extract(), # Galleries (horrible html)
            'pdfFiles': pdf_files_generated,
            'tags': response.meta['tags'],
            'url': response.url,
        }
     
               
    def parse_publication(self, response):

        def extract_with_css(query):
            return response.css(query).extract_first()

        imagesA=response.xpath('//div[@class="text"]/div[not(@id) and not(@class)]//a[img]/@href').extract()
        imagesA_generated = list()
        for image_file in imagesA:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.org/',1)
            imagesA_generated.append(image_file)

        imagesB=response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[2]//img/@src').extract()
        imagesB_generated = list()
        for image_file in imagesB:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.org/',1)
            imagesB_generated.append(image_file)
        
        pdfFiles=response.css('div.article a[href$=".pdf"]::attr(href)').extract()
        pdf_files_generated = list()
        for pdf_file in pdfFiles:
            if (pdf_file.startswith('/')):
                pdf_file = pdf_file.replace('/','http://www.greenpeace.org/',1)
            pdf_files_generated.append(pdf_file)
            print pdf_files_generated

        date_field = response.css('div.article div.text span.author::text').re_first(r' - \s*(.*)')
        if date_field:
            date_field = dateutil.parser.parse(date_field)

        lead_text = extract_with_css('#content > div.happen-box.article > div > div.text > div.leader > div')

        image_gallery=response.xpath("//*[contains(@class, 'embedded-image-gallery')]")
        p3_image_gallery = 'false'
        if image_gallery:
            p3_image_gallery = 'true'
        
        body_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[2]').extract_first()
        attachment_field = response.xpath('//*[@id="content"]/div[4]/div/div[2]/p/a').extract_first()
        if body_text:
            if attachment_field:
                body_text = body_text + attachment_field
            if lead_text:
                body_text = '<div>' + lead_text + '</div>' + body_text

        if body_text:
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.org/').replace('href="/', 'href="http://www.greenpeace.org/')
            body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)

        subtitle = extract_with_css('div.article h2 span::text')
        if subtitle:
            body_text = '<h2>' + subtitle + '</h2><br />' + body_text

        images=response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[2]//img[contains(@style, "float:")]').extract()   #img[@style="margin: 9px; float: left;"]
        imagesD_generated = list()
        for image in images:
            imagesD_generated.append(image)

        yield {
            'type': 'Publication',
            'p3_image_gallery': p3_image_gallery,
            'title': extract_with_css('div.article h1 span::text'),
            #'subtitle': subtitle,
            'author': 'Greenpeace New Zealand',
            'date': date_field,
            #'lead': extract_with_css('div.news-list div.post-content *:first-child strong::text'),
            'lead': extract_with_css('#content > div.happen-box.article > div > div.text > div.leader > div'),
            'categories': response.meta['categories'],
            'text': body_text,
            'imagesA': imagesA_generated,
            #'imagesB': response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img[not(ancestor::a)]/@src').extract(), #don't import image if there's an a tag around it
            'imagesB': imagesB_generated,
            'imagesC': response.xpath('//div[@class="gallery"]//div[@class="img-nav"]//a/@rel').extract(), # Galleries (horrible html)
            'imagesD': imagesD_generated,
            'pdfFiles': pdf_files_generated,
            'tags': response.meta['tags'],
            'url': response.url,
        }
