# -*- coding: utf-8 -*
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
        'FEED_URI': 'gpin_batch_v2_test.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def start_requests(self):

        start_urls = {
            # - 1st batch
            # Press Release
            'http://www.greenpeace.org/india/en/Press/Greenpeace-launches-Junglistan-campaign-to-garner-public-support-for-forests-/': ('Press Release', 'Environment', 'forest', 'fossil fuels', 'Migrate'),
            'http://www.greenpeace.org/india/en/Press/The-Kedia-Model-Is-Here/': ('Press Release', 'Health and Living', 'sustainable agriculture', 'safefood', 'Migrate'),
            'http://www.greenpeace.org/india/en/Press/Greenpeace-launches-Food-for-Life-campaign-on-World-Environment-Day--Kedia-Village-an-iconic-success-story-in-the-Ecological-Agricultural-Revolution---/': ('Press Release', 'Health and Living', 'sustainable agriculture', 'safefood', 'Migrate'),
            'http://www.greenpeace.org/india/en/Press/Bihars-First-Solar-Powered-Cold-Storage-in-Kedia/': ('Press Release', 'Health and Living', 'sustainable agriculture', 'safefood', 'Migrate'),
            'http://www.greenpeace.org/india/en/Press/Coal-mining-threatens-over-11-million-ha-of-forest-tiger-elephant-habitat/': ('Press Release', 'Environment', 'forest', 'fossil fuels', 'Migrate'),

            # Story
            'http://www.greenpeace.org/india/en/news/Feature-Stories/Low-cost-solar-PV-pumping-set-demonstrated-in-Kalyan-Bigha-by-Greenpeace/': ('Feature', 'Clean Energy', 'renewables', 'fossil fuels', 'Migrate'),
            'http://www.greenpeace.org/india/en/news/Feature-Stories/Dharnai-Goes-LIVE-Powered-by-Greenpeaces-First-Solar-Microgrid/': ('Feature', 'Clean Energy', 'renewables', 'fossil fuels', 'Migrate'),
            'http://www.greenpeace.org/india/en/news/Feature-Stories/Greenpeace-Activists-take-Go-Solar-message-to-the-Temple-of-the-Sun-in-Machu-Pichu-as-Climate-Summit-begins-in-Lima/': ('Feature', 'Clean Energy', 'renewables', 'fossil fuels', 'Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Community_blogs1/foot-spa-and-bamboo-shoot-curry-in-junglistan/blog/42078/': ('Story', 'Environment', 'forest', 'fossil fuels', 'Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Community_blogs1/junglistan-nivas-the-new-hangout-for-the-vill/blog/42179/': ('Story', 'Environment', 'forest', 'fossil fuels', 'Migrate'),

            # - 2nd batch
            #'http://www.greenpeace.org/india/en/Press/Chhattisgarh-govt-inadequate-in-addressing-human-elephant-conflict/':('Story','Environment','forest','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Press/Chhattisgarh-govt-inadequate-in-addressing-human-elephant-conflict/':('Press Release','Environment','forest','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Community_blogs1/junglistan-at-school/blog/46078/':('Story','Environment','forest','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Community_blogs1/junglistan-diaries-tedx-with-brikesh-singh/blog/45293/':('Story','Environment','forest','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/junglistan-diaries-padmapur-forests-residence/blog/42005/':('Story','Environment','forest','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Community-blogs1/junglistan-diaries-tedx-with-brikesh-singh/blog/45293/':('Story','Environment','forest','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/did-you-just-ask-me-why-support-junglistan/blog/41829/':('Story','Environment','forest','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/republic-of-junglistan-becomes-a-star-attract/blog/38628/':('Story','Environment','forest','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/bhaloo-and-sheroo-welcome-you-to-junglistan/blog/38048/':('Story','Environment','forest','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Community_blogs1/junglistan-diaries-booster-shots-of-inspirati/blog/42256/':('Story','Environment','forest','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/republic-of-junglistan-reaches-bangalore/blog/38234/':('Story','Environment','forest','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Community_blogs1/junglistan-diaries-the-writings-on-the-wall/blog/42120/':('Story','Environment','forest','fossil fuels','Migrate'),
            # Hindi article - manual migration
            #'http://www.greenpeace.org/india/hi/press/Greenpeace-launches-Food-for-Life-campaign-on-World-Environment-Day--Kedia-Village-an-iconic-success-story-in-the-Ecological-Agricultural-Revolution/':('Press Release','Health and Living','sustainable agriculture','safefood','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Community_blogs1/kedia-naama-24-volunteers-51-hours-of-journey/blog/57218/':('Story','Health and Living','sustainable agriculture','safefood','Migrate'),
            'http://www.greenpeace.org/india/en/news/Feature-Stories/Bangalore-join-hands-with-the-global-movement-against-Monsanto-and-GMOs/':('Feature','Health and Living','health','safefood','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Community_blogs1/food-sovereignty-gmos-and-the-brai-bill/blog/46333/':('Story','Health and Living','health','safefood','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Community_blogs1/how-we-said-no-to-gmo/blog/51786/':('Story','Health and Living','health','safefood','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Campaign_blogs/gmo-omg-no-not-again/blog/57813/':('Story','Health and Living','health','safefood','Migrate'),
            'http://www.greenpeace.org/india/en/news/Feature-Stories/Bangalore-join-hands-with-the-global-movement-against-Monsanto-and-GMOs/?id=382915_1110989&idkeep=True&epslanguage=en-IN':('Feature','Health and Living','health','safefood','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Campaign_blogs/gm-mustard-throwing-caution-to-the-wind-is-no/blog/54773/':('Story','Health and Living','health','safefood','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Campaign_blogs/sarso-satyagraha-gm-mustard-deferred/blog/55498/':('Story','Health and Living','health','safefood','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Campaign_blogs/for-our-beloved-mustard/blog/54678/':('Story','Health and Living','health','safefood','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Campaign_blogs/8-problems-with-the-gm-mustard-commercialisat/blog/59430/':('Story','Health and Living','health','safefood','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Community-blogs1/tax-incentives-for-solar-energy-in-bihar/blog/43168/':('Story','Clean Energy','renewables','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Campaign_blogs/solar-street-lights-light-up-villages-in-utta/blog/46426/':('Story','Clean Energy','renewables','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Community-blogs1/kerala-launches-ambitious-solar-project/blog/43955/':('Story','Clean Energy','renewables','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Campaign_blogs/dharnai-story-of-one-solar-village/blog/53565/':('Story','Clean Energy','renewables','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Campaign_blogs/crisis-to-solution-paving-way-to-solar-pumpin/blog/47670/':('Story','Clean Energy','renewables','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Campaign_blogs/nitish-kumar-visits-solar-village-of-dharnai/blog/50174/':('Story','Clean Energy','renewables','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Campaign_blogs/atom-solar-sun-trolley-is-here/blog/48938/':('Story','Clean Energy','renewables','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Campaign_blogs/end-to-the-solar-eclipse-in-delhi/blog/50501/':('Story','Clean Energy','renewables','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Campaign_blogs/solarverse-the-prose-of-solar-power/blog/55239/':('Story','Clean Energy','renewables','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Campaign_blogs/sustaining-with-solar/blog/51175/':('Story','Clean Energy','renewables','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Community-blogs1/a-dream-with-solar-power/blog/45340/':('Story','Clean Energy','renewables','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Campaign_blogs/going-solar-a-great-investment-plan/blog/59679/':('Story','Clean Energy','renewables','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/news/Feature-Stories/Climate-summit-comment-From-Bihar-India-could-distributed-solar-succeed-where-coal-has-failed/':('Feature','Clean Energy','renewables','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Press/Solar-powered-PV-pump-set-to-revolutionise-agriculture-in-Bihar-/':('Press Release','Clean Energy','renewables','fossil fuels','Migrate'),
            #'http://www.greenpeace.org/india/en/Press/Bihars-First-Solar-Powered-Cold-Storage-in-Kedia/':('Press Release','Clean Energy','renewables','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Press/Greenpeace-Supports-Indias-decision-to-challenge-WTO-ruling-on-Indias-Solar-Mission/':('Press Release','Clean Energy','renewables','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Press/Ex-CM-Nitish-Kumar-hails-Greenpeaces-solar-micro-grid/':('Press Release','Clean Energy','renewables','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Press/Delhi-Solar-Policy-draft-targets-2GW-by-2025-Time-to-maximise-solar-potential-of-capital-says-Greenpeace/':('Press Release','Clean Energy','renewables','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Press/DERC-proposal-on-net-metering-and-connectivity-in-rooftop-solar-PV-projects-is-deterring-Greenpeace/':('Press Release','Clean Energy','renewables','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Press/Greenpeace-releases-the-roadmap-to-a-solar-revolution-in-Delhi/':('Press Release','Clean Energy','renewables','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Press/Sukhdev-Vihar-residents-join-Greenpeaces-demand-for-a-solar-revolution-in-Delhi/':('Press Release','Clean Energy','renewables','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Press/Roll-back-tariff-hikes-and-fulfill-poll-promise-on-solar-energy-Greenpeace-tells-Kejriwal/':('Press Release','Clean Energy','renewables','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Press/Tamil-Nadus-solar-policy-a-positive-and-ambitious-step/':('Press Release','Clean Energy','renewables','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Press/Greenpeace-blockades-Power-Minister-Haroon-Yusufs-residence-with-solar-panels/':('Press Release','Clean Energy','renewables','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Press/Delhi-makes-way-for-a-Solar-Comet-on-World-Environment-Day/':('Press Release','Clean Energy','renewables','fossil fuels','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Campaign_blogs/the-indian-airpocalypse/blog/61110/':('Story','Clean Energy','fossil fuels','health','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Campaign_blogs/the-ministry-has-spoken-a-national-clean-air-/blog/60929/':('Story','Clean Energy','fossil fuels','health','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Campaign_blogs/why-we-need-clean-energy-to-have-clean-air/blog/61165/':('Story','Clean Energy','fossil fuels','health','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Community_blogs1/are-the-green-spaces-in-delhi-free-from-air-p/blog/51981/':('Story','Clean Energy','fossil fuels','health','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Campaign_blogs/are-indias-efforts-to-tackle-air-pollution-an/blog/58923/':('Story','Clean Energy','fossil fuels','health','Migrate'),
            'http://www.greenpeace.org/india/en/Blog/Campaign_blogs/join-greenpeace-india-for-a-clean-air-nation/blog/58109/':('Story','Clean Energy','fossil fuels','health','Migrate'),
            'http://www.greenpeace.org/india/en/news/Feature-Stories/As-India-struggles-to-breathe-over-300-coal-power-plants-are-violating-air-pollution-laws-and-MoEFCC-does-nothing/':('Feature','Clean Energy','fossil fuels','health','Migrate'),
            'http://www.greenpeace.org/india/en/Press/National-Clean-Air-Program-NCAP-Good-Start-But-Needs-Transparent-Action-Greenpeace-India/':('Press Release','Clean Energy','fossil fuels','health','Migrate'),
            'http://www.greenpeace.org/india/en/Press/Not-just-Delhi-Air-in-most-Indian-cities-hazardous-Greenpeace-report/':('Press Release','Clean Energy','fossil fuels','health','Migrate'),
            # Same URL and params
            #'http://www.greenpeace.org/india/en/Press/Not-just-Delhi-Air-in-most-Indian-cities-hazardous-Greenpeace-report/':('Press Release','Clean Energy','fossil fuels','health','Migrate'),
            'http://www.greenpeace.org/india/en/Press/India-Continues-to-Reel-Under-Airpocalypse-of-Unbreathable-Air-Greenpeace-India-Report/':('Press Release','Clean Energy','fossil fuels','health','Migrate'),
            'http://www.greenpeace.org/india/en/Press/Greenpeace-India-welcomes-MoEFCC-move-for-National-Clean-Air-Program-calls-it-as-the-Important-First-Step-towards-tackling-air-pollution/':('Press Release','Clean Energy','fossil fuels','health','Migrate'),
            'http://www.greenpeace.org/india/en/Press/Break-Free-from-Air-Pollution--Mumbai-Demands-Clean-Air-Action-Plan/':('Press Release','Clean Energy','fossil fuels','health','Migrate'),
            'http://www.greenpeace.org/india/en/Press/Greenpeace-launches-Clean-Air-Nation-Movement-Calls-on-government-to-deliver-commitment-of-Clean-Air-My-Birthright/':('Press Release','Clean Energy','fossil fuels','health','Migrate'),
            'http://www.greenpeace.org/india/en/Press/Greenpeace-India-demands-Regional-Action-Plan-to-control-air-pollution-in-Uttar-Pradesh/':('Press Release','Clean Energy','fossil fuels','health','Migrate'),
            'http://www.greenpeace.org/india/en/Press/Lucknow-Unites-to-Fight-Back-Air-Pollution-in-the-City-and-the-State/':('Press Release','Clean Energy','fossil fuels','health','Migrate'),
            'http://www.greenpeace.org/india/en/Press/Immediate-Enforcement-of-National-Clean-Air-Program-must-not-follow-Emission-Standard-precedent-says-Greenpeace-India/':('Press Release','Clean Energy','fossil fuels','health','Migrate'),
            'http://www.greenpeace.org/india/en/Press/Delhi-just-the-tip-of-the-air-pollution-iceberg-Greenpeace-analyses-NAQI-data-across-Indian-cities/':('Press Release','Clean Energy','fossil fuels','health','Migrate'),
            'http://www.greenpeace.org/india/en/Press/Greenpeace-India-launches-Clean-Air-Nation-application-on-Google-Store/':('Press Release','Clean Energy','fossil fuels','health','Migrate'),
            'http://www.greenpeace.org/india/en/Press/Switch-On-The-Sun--Greenpeace-India-Applauds-Delhi-Government-Adoption-Of-Solar-Energy--Vision/': ('Press Release', 'Clean Energy', 'renewables', 'fossil fuels', 'Migrate'),
            'http://www.greenpeace.org/india/en/news/Thousands-of-citizens-demand-that-the-BRAI-bill-be-Withdrawn-and-India-be-GMO-free/': ('Press Release', 'Health and Living', 'health', 'safefood', 'Migrate'),
            'http://www.greenpeace.org/india/en/news/Chandrapur-MP-visits-Brikesh-and-offers-his-support-to-Junglistan/': ('Press Release', 'Environment', 'forest', 'fossil fuels', 'Migrate'),
            'http://www.greenpeace.org/india/en/news/keep-our-rice-gmo-free/': ('Press Release', 'Health and Living', 'health', 'safefood', 'Migrate'),
            'http://www.greenpeace.org/india/en/news/notes-from-the-solar-generatio/': ('Press Release', 'Clean Energy', 'renewables', 'fossil fuels', 'Migrate'),
        }

        for url, data in start_urls.iteritems():
            post_type, categories, tags1, tags2, action = data
            if (post_type == 'Story'):
                request = scrapy.Request(url, callback=self.parse_blog, dont_filter='true')
            elif (post_type == 'Publication'):
                request = scrapy.Request(url, callback=self.parse_publication, dont_filter='true')
            elif (post_type == 'Press release' or post_type == 'Press Release'):
                request = scrapy.Request(url, callback=self.parse_press, dont_filter='true')
            elif (post_type == 'Feature'):
                request = scrapy.Request(url, callback=self.parse_feature, dont_filter='true')

            if (action.lower() == 'migrate'):
                request.meta['status'] = 'publish'
            if (action.lower() == 'archive'):
                request.meta['status'] = 'draft'
            request.meta['categories'] = categories
            request.meta['tags'] = tags1
            request.meta['tags1'] = tags2
            request.meta['action'] = action
            yield request

    def parse_feature(self, response):

        def extract_with_css(query):
            return response.css(query).extract_first()

        image_gallery = response.xpath("//*[contains(@class, 'embedded-image-gallery')]")
        p3_image_gallery = 'false'
        if image_gallery:
            p3_image_gallery = 'true'

        imagesB = response.xpath('//*[@id="content"]//img/@src').extract()
        imagesB_generated = list()
        for image_file in imagesB:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/', 'http://www.greenpeace.org/', 1)
            imagesB_generated.append(image_file)

        pdfFiles = response.css('div.article a[href$=".pdf"]::attr(href)').extract()
        pdf_files_generated = list()
        for pdf_file in pdfFiles:
            print pdf_file
            if (pdf_file.startswith('/')):
                pdf_file = pdf_file.replace('/', 'http://www.greenpeace.org/', 1)
                print pdf_file
            pdf_files_generated.append(pdf_file)
            print pdf_files_generated

        date_field = response.xpath('//*[@id="content"]/div[4]/div/div[2]/span/text()').extract()[0]
        if (date_field.startswith('Feature story - ')):
            date_field = date_field.replace('Feature story - ', '', 1)
        if date_field:
            if (date_field.startswith('Feature story - ')):
                date_field = date_field.replace('Feature story - ', '', 1)
            date_field = dateutil.parser.parse(date_field)

        lead_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[1]/div').extract()[0]
        body_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[2]').extract()[0]
        if body_text:
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/',
                                                                              'src="http://www.greenpeace.org/').replace(
                'href="/', 'href="http://www.greenpeace.org/')
            body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)
            if lead_text:
                body_text = '<div>' + lead_text + '</div>' + body_text + response.xpath(
                    ' //*[@id="content"]/div[4]/div/div[2]/p').extract_first()
        subtitle = extract_with_css('div.article h2 span::text')
        if subtitle:
            body_text = '<h2>' + subtitle + '</h2><br />' + body_text

        yield {
            'type': 'Story',
            'p3_image_gallery': p3_image_gallery,
            # 'title': extract_with_css('#content > div.happen-box.article > h1::text'),
            'title': response.xpath('//*[@id="content"]/div[4]/h1/span/text()').extract()[0],
            'subtitle': extract_with_css('div.article h1 span::text'),
            'author': 'Greenpeace India',
            'date': date_field,
            # 'lead': extract_with_css('div.news-list div.post-content *:first-child strong::text'),
            'lead': lead_text,
            'categories': response.meta['categories'],
            'text': body_text,
            'imagesA': response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img/@src').extract(),
            'imagesB': imagesB_generated,
            # 'imagesB': response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img[not(ancestor::a)]/@src').extract(), #don't import image if there's an a tag around it
            'imagesC': response.xpath('//div[@class="gallery"]//div[@class="img-nav"]//a/@rel').extract(),
            # Galleries (horrible html)
            'pdfFiles': pdf_files_generated,
            'tags': response.meta['tags'],
            'url': response.url,
        }

    def parse_blog(self, response):

        def extract_with_css(query):
            return response.css(query).extract_first()

        imagesA = response.xpath('//div[@class="news-list"]//div[@class="post-content"]//a[img]/@href').extract()
        imagesA_generated = list()
        for image_file in imagesA:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/', 'http://www.greenpeace.org/', 1)
            imagesA_generated.append(image_file)

        imagesB = response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img/@src').extract()
        imagesB_generated = list()
        for image_file in imagesB:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/', 'http://www.greenpeace.org/', 1)
            imagesB_generated.append(image_file)

        imagesEnlarge = response.xpath('//div[@class="news-list"]//div[@class="post-content"]//a[@class="open-img EnlargeImage"]/@href').extract()
        imagesEnlarge_generated = list()
        for image_file in imagesEnlarge:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/', 'http://www.greenpeace.org/', 1)
            imagesEnlarge_generated.append(image_file)

        pdfFiles = response.css('div.article a[href$=".pdf"]::attr(href)').extract()
        pdf_files_generated = list()
        for pdf_file in pdfFiles:
            print pdf_file
            if (pdf_file.startswith('/')):
                pdf_file = pdf_file.replace('/', 'http://www.greenpeace.org/', 1)
                print pdf_file
            pdf_files_generated.append(pdf_file)
            print pdf_files_generated

        date_field = response.css('div.news-list .caption::text').re_first(r' - \s*(.*)')
        if date_field:
            date_field = dateutil.parser.parse(date_field)

        image_gallery = response.xpath("//*[contains(@class, 'embedded-image-gallery')]")
        p3_image_gallery = 'false'
        if image_gallery:
            p3_image_gallery = 'true'

        body_text = response.css('div.news-list div.post-content').extract_first()
        if body_text:
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.org/').replace('href="/', 'href="http://www.greenpeace.org/')
            body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)

        subtitle = extract_with_css('div.article h2 span::text')
        if subtitle:
            body_text = '<h2>' + subtitle + '</h2><br />' + body_text

        yield {
            'type': 'Story',
            'p3_image_gallery': p3_image_gallery,
            'title': extract_with_css('div.news-list h1::text'),
            'subtitle': '',
            'author': response.xpath(
                'string(//div[@class="news-list"]/ul/li/*/*/span[@class="caption"]/span[@class="green1"]/strong)').extract()[0],
            # 'author_username': author_username,
            'date': date_field,
            # 'lead': extract_with_css('div.news-list div.post-content *:first-child strong::text'),
            'lead': response.xpath(
                'string(//div[@class="news-list"]/ul/li/div[@class="post-content"]/div//*[self::p or self::h3 or self::h2][1])').extract()[0],
            'categories': response.meta['categories'],
            'text': body_text,
            'imagesA': imagesA_generated,
            'imagesEnlarge': imagesEnlarge_generated,
            'imagesB': imagesB_generated,
            'imagesC': response.xpath('//div[@class="gallery"]//div[@class="img-nav"]//a/@rel').extract(),
            # Galleries (horrible html)
            'pdfFiles': pdf_files_generated,
            'tags': response.meta['tags'],
            'url': response.url,
            'status': response.meta['status'],
        }

    def parse_press(self, response):

        def extract_with_css(query):
            return response.css(query).extract_first()

        imagesA = response.xpath('//div[@class="news-list"]//div[@class="post-content"]//a[img]/@href').extract()
        imagesA_generated = list()
        for image_file in imagesA:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/', 'http://www.greenpeace.org/', 1)
            imagesA_generated.append(image_file)

        imagesB = response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img/@src').extract()
        imagesB_generated = list()
        for image_file in imagesB:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/', 'http://www.greenpeace.org/', 1)
            imagesB_generated.append(image_file)

        pdfFiles = response.css('div.article a[href$=".pdf"]::attr(href)').extract()
        pdf_files_generated = list()
        for pdf_file in pdfFiles:
            print pdf_file
            if (pdf_file.startswith('/')):
                pdf_file = pdf_file.replace('/', 'http://www.greenpeace.org/', 1)
                print pdf_file
            pdf_files_generated.append(pdf_file)
            print pdf_files_generated

        image_gallery = response.xpath("//*[contains(@class, 'embedded-image-gallery')]")
        p3_image_gallery = 'false'
        if image_gallery:
            p3_image_gallery = 'true'

        lead_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[1]/div/text()').extract()[0]
        date_field = response.xpath('string(//*[@id="content"]/div[4]/div/div[2]/span)').extract()[0]
        if (date_field.startswith('Feature story - ')):
            date_field = date_field.replace('Feature story - ','',1)
        if (date_field.startswith('Press release - ')):
            date_field = date_field.replace('Press release - ','',1)
        if date_field:
            date_field = dateutil.parser.parse(date_field)
        body_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[2]').extract()[0]
        if body_text:
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.org/').replace('href="/', 'href="http://www.greenpeace.org/')
            body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)
            if lead_text:
                body_text = '<div>' + lead_text + '</div>' + body_text + response.xpath(
                    ' //*[@id="content"]/div[4]/div/div[2]/p').extract_first()
        subtitle = extract_with_css('div.article h2 span::text')
        if (subtitle == 'None'):
            subtitle = ''
        if subtitle:
            body_text = '<h2>' + subtitle + '</h2><br />' + body_text

        yield {
            'type': 'Press Release',
            'p3_image_gallery': p3_image_gallery,
            'title': extract_with_css('div.article h1 span::text'),
            'subtitle': subtitle,
            'author': 'Greenpeace India',
            # 'date': response.css('#content > div.happen-box.article > div > div.text > span').re_first(r' - \s*(.*)'),
            'date': date_field,
            # 'lead': extract_with_css('div.news-list div.post-content *:first-child strong::text'),
            'lead': lead_text,
            'categories': response.meta['categories'],
            # 'text':  response.css('div.news-list div.post-content').extract_first(),
            'text': body_text,
            'imagesA': imagesA_generated,
            # 'imagesB': response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img[not(ancestor::a)]/@src').extract(), #don't import image if there's an a tag around it
            'imagesB': imagesB_generated,
            'imagesC': response.xpath('//div[@class="gallery"]//div[@class="img-nav"]//a/@rel').extract(),
            # Galleries (horrible html)
            'pdfFiles': pdf_files_generated,
            'tags': response.meta['tags'],
            'url': response.url,
        }

    def parse_publication(self, response):

        def extract_with_css(query):
            return response.css(query).extract_first()

        imagesA = response.xpath('//div[@class="text"]/div[not(@id) and not(@class)]//a[img]/@href').extract()
        imagesA_generated = list()
        for image_file in imagesA:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/', 'http://www.greenpeace.org/', 1)
            imagesA_generated.append(image_file)

        imagesB = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[2]//img/@src').extract()
        imagesB_generated = list()
        for image_file in imagesB:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/', 'http://www.greenpeace.org/', 1)
            imagesB_generated.append(image_file)

        pdfFiles = response.css('div.article a[href$=".pdf"]::attr(href)').extract()
        pdf_files_generated = list()
        for pdf_file in pdfFiles:
            if (pdf_file.startswith('/')):
                pdf_file = pdf_file.replace('/', 'http://www.greenpeace.org/', 1)
            pdf_files_generated.append(pdf_file)
            print pdf_files_generated

        date_field = response.css('div.article div.text span.author::text').re_first(r' - \s*(.*)')
        if date_field:
            date_field = dateutil.parser.parse(date_field)

        lead_text = extract_with_css('#content > div.happen-box.article > div > div.text > div.leader > div')

        image_gallery = response.xpath("//*[contains(@class, 'embedded-image-gallery')]")
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

        yield {
            'type': 'Publication',
            'p3_image_gallery': p3_image_gallery,
            'title': extract_with_css('div.article h1 span::text'),
            'subtitle': extract_with_css('div.article h2 span::text'),
            'author': 'Greenpeace India',
            'date': date_field,
            # 'lead': extract_with_css('div.news-list div.post-content *:first-child strong::text'),
            'lead': extract_with_css('#content > div.happen-box.article > div > div.text > div.leader > div'),
            'categories': response.meta['categories'],
            'text': body_text,
            'imagesA': imagesA_generated,
            # 'imagesB': response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img[not(ancestor::a)]/@src').extract(), #don't import image if there's an a tag around it
            'imagesB': imagesB_generated,
            'imagesC': response.xpath('//div[@class="gallery"]//div[@class="img-nav"]//a/@rel').extract(),
            # Galleries (horrible html)
            'pdfFiles': pdf_files_generated,
            'tags': response.meta['tags'],
            'url': response.url,
        }