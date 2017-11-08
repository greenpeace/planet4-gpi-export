import scrapy
import logging
import locale
import dateutil.parser

locale.setlocale(locale.LC_ALL, '')

class AllSpider(scrapy.Spider):
    name = 'all'

    custom_settings = {
        'ROBOTSTXT_OBEY': 0,
        'FEED_URI': 'all_gpi_T8.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def start_requests(self):
        start_urls = {'http://www.greenpeace.org/international/en/press/releases/2017/Rainbow-Warrior-arrives-in-Cuba-to-document-the-islands-eco-food-system/':('Press Release','Food','Food,FixFood'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/food-for-life-eat-less-meat-who/blog/54640/':('Story','Food','Food,FixFood,LessMeatMorePlants'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/food-for-life-I-know-who-grew-it/blog/52905/':('Story','Food','Food,FixFood'),}
        for url,data in start_urls.iteritems():
            post_type, categories, tags = data
            if ( post_type=='Story' ):
                request = scrapy.Request(url, callback=self.parse_blog)
            elif ( post_type=='Publication' ):
                request = scrapy.Request(url, callback=self.parse_publication)
            elif ( post_type=='Press Release' ):
                request = scrapy.Request(url, callback=self.parse_press)
            yield request
            request.meta['categories'] = post_type+','+categories
            request.meta['tags'] = tags


    def parse_blog(self, response):
        
        def extract_with_css(query):
            return response.css(query).extract_first()

        yield {
            'type': 'Blog',
            'title': extract_with_css('div.news-list h1::text'),
            'author': response.xpath('string(//div[@class="news-list"]/ul/li/*/*/span[@class="caption"]/span[@class="green1"]/strong)').extract()[0],
            'date': dateutil.parser.parse(response.css('div.news-list .caption::text').re_first(r' - \s*(.*)')),
            #'lead': extract_with_css('div.news-list div.post-content *:first-child strong::text'),
            'lead': response.xpath('string(//div[@class="news-list"]/ul/li/div[@class="post-content"]/div//*[self::p or self::h3 or self::h2][1])').extract()[0],
            'categories': response.meta['categories'],
            'text':  response.css('div.news-list div.post-content').extract_first().replace('src="/international', 'src="http://www.greenpeace.org/international').replace('href="/', 'href="http://www.greenpeace.org/'),
            'imagesA': response.xpath('//div[@class="news-list"]//div[@class="post-content"]//a[img]/@href').extract(),
            #'imagesB': response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img[not(ancestor::a)]/@src').extract(), #don't import image if there's an a tag around it
            'imagesB': response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img/@src').extract(),
            'imagesC': response.xpath('//div[@class="gallery"]//div[@class="img-nav"]//a/@rel').extract(), # Galleries (horrible html)
            'pdfFiles': response.css('div.post-content a[href$=".pdf"]::attr(href)').extract(),
            'tags': response.meta['tags'],
            'url': response.url,
        }

    def parse_press(self, response):

        def extract_with_css(query):
            return response.css(query).extract_first()

        yield {
            'type': 'Press',
            'title': extract_with_css('div.article h1 span::text'),
            'author': 'Greenpeace International',
            #'date': response.css('#content > div.happen-box.article > div > div.text > span').re_first(r' - \s*(.*)'),
            'date': dateutil.parser.parse(response.xpath('string(//*[@id="content"]/div[4]/div/div[2]/span)').extract()[0].replace('Press release - ', '')),
            #'lead': extract_with_css('div.news-list div.post-content *:first-child strong::text'),
            'lead': response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[1]/div/text()').extract()[0],
            'categories': response.meta['categories'],
            #'text':  response.css('div.news-list div.post-content').extract_first(),
            'text':  response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[2]').extract()[0].replace('src="/international', 'src="http://www.greenpeace.org/international').replace('href="/', 'href="http://www.greenpeace.org/'),
            'imagesA': response.xpath('//div[@class="news-list"]//div[@class="post-content"]//a[img]/@href').extract(),
            #'imagesB': response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img[not(ancestor::a)]/@src').extract(), #don't import image if there's an a tag around it
            'imagesB': response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img/@src').extract(),
            'imagesC': response.xpath('//div[@class="gallery"]//div[@class="img-nav"]//a/@rel').extract(), # Galleries (horrible html)
            'pdfFiles': response.css('div.post-content a[href$=".pdf"]::attr(href)').extract(),
            'tags': response.meta['tags'],
            'url': response.url,
        }
     
               
    def parse_publication(self, response):

        def extract_with_css(query):
            return response.css(query).extract_first()

        yield {
            'type': 'Publication',
            'title': extract_with_css('div.article h1 span::text'),
            'author': 'Greenpeace International',
            'date': response.css('div.article div.text span.author::text').re_first(r' - \s*(.*)'),
            #'lead': extract_with_css('div.news-list div.post-content *:first-child strong::text'),
            'lead': extract_with_css('div.article h2 span::text'),
            'categories': response.meta['categories'],
            'text': response.xpath('//*[@id="content"]/div[4]/div/div[2]').extract_first().replace('src="/international', 'src="http://www.greenpeace.org/international').replace('href="/', 'href="http://www.greenpeace.org/'),
            'imagesA': response.xpath('//div[@class="text"]/div[not(@id) and not(@class)]//a[img]/@href').extract(),
            #'imagesB': response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img[not(ancestor::a)]/@src').extract(), #don't import image if there's an a tag around it
            'imagesB': response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img/@src').extract(),
            'imagesC': response.xpath('//div[@class="gallery"]//div[@class="img-nav"]//a/@rel').extract(), # Galleries (horrible html)
            'pdfFiles': response.css('div.article a[href$=".pdf"]::attr(href)').extract(),
            'tags': response.meta['tags'],
            'url': response.url,
        }