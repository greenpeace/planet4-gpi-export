import scrapy
import logging
import locale

locale.setlocale(locale.LC_ALL, '')

class AllSpider(scrapy.Spider):
    name = 'all'

    custom_settings = {
        'ROBOTSTXT_OBEY': 0,
        'FEED_URI': 'all_gpi_B3.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def start_requests(self):
        start_urls = {'http://www.greenpeace.org/international/en/press/releases/2017/Rainbow-Warrior-arrives-in-Cuba-to-document-the-islands-eco-food-system/':{'Press Release':{'Food':'Food,FixFood'}},
'http://www.greenpeace.org/international/en/press/releases/2016/Research-shows-switching-to-organic-food-can-reduce-pesticide-levels-in-urine/':{'Press Release':{'Food':'Food'}},
'http://www.greenpeace.org/international/en/press/releases/2016/Nobel-laureates-sign-letter-on-Greenpeace-Golden-rice-position---reactive-statement/':{'Press Release':{'Food':'Detox,ReThinkIT'}},
'http://www.greenpeace.org/international/en/press/releases/2015/Greenpeace-demands-scale-up-of-ecological-farming/':{'Press Release':{'Food':'Oceans'}},
'http://www.greenpeace.org/international/en/press/releases/2015/Greenpeace-report-reveals-farmers-are-the-most-vulnerable-to-health-risks-from-pesticides/':{'Press Release':{'Detox':'Food,FixFood'}},
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/fipronil-contaminated-eggs-scandal-EU/blog/60010/':{'Story':{'Detox':'Food,FixFood,Pesticides'}},
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/bees-farming-pesticides-eu/blog/59287/':{'Story':{'Detox':'Food,FixFood'}},
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/pesticides-are-not-needed-to-feed-the-world-u/blog/59160/':{'Story':{'Detox':'Food,FixFood,Pesticides'}},
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/brazil-rotten-meat-crisis-industrial-agriculture/blog/59024/':{'Story':{'Detox':'Food,FixFood,LessMeatMorePlants'}},
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/biological-restoration-of-water-land-Rex-Weyler/blog/58920/':{'Story':{'Food':'Food,FixFood'}},
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/ariculture-revolution-germany-berlin/blog/58577/':{'Story':{'Food':'Food,FixFood'}},
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/seeing-is-believing-growing-Food-for-people-Cuba-agroecology/blog/58480/':{'Story':{'Food':'Food,FixFood,LessMeatMorePlants'}},
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/how-does-eco-Food-affect-your-body/blog/58333/':{'Story':{'Food':'Food,FixFood'}},
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/pesticides-food-safety-reform-Shanghai-china/blog/57848/':{'Story':{'Food':'Food,FixFood'}},
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/save-the-bees-goodbye-to-fipronil-EU/blog/60346/':{'Story':{'Food':'Food,FixFood'}},
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/future-of-food-iPES-sustainable-agriculture/blog/56793/':{'Story':{'Food':'Food,FixFood'}},
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/meat-free-day-better-eating-challenge-ecological/blog/56731/':{'Story':{'Food':'Food,FixFood,LessMeatMorePlants'}},
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/3-plant-based-recipes-you-need-to-try-this-world-meat-free-day/blog/56672/':{'Story':{'Food':'Food,FixFood,LessMeatMorePlants'}},
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/vegetarian-tips-for-going-meat-free/blog/56351/':{'Story':{'Food':'Food,FixFood,LessMeatMorePlants'}},
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/farmers-future-healthy-land/blog/56344/':{'Story':{'Food':'Food,FixFood'}},
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/fridge-film-sustainable-food-farming/blog/56093/':{'Story':{'Food':'Food,FixFood'}},
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/food-for-life-organic-farming-bees-spain/blog/55493/':{'Story':{'Food':'Food,FixFood,Bees'}},
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/Food-for-life-cowspiracy/blog/54404/':{'Story':{'Food':'Food,FixFood,LessMeatMorePlants'}},
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/food-for-life-world-food-day/blog/54448/':{'Story':{'Food':'Food,FixFood'}},
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/food-for-life-europes-pesticide-addiction/blog/54396/':{'Story':{'Food':'Food,FixFood'}},
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/agrotoxics-esperanza-sinaloa/blog/53800/':{'Story':{'Food':'Food,FixFood,Oceans,Nitrates'}},
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/food-for-life-eat-less-meat-who/blog/54640/':{'Story':{'Food':'Food,FixFood,LessMeatMorePlants'}},
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/food-for-life-I-know-who-grew-it/blog/52905/':{'Story':{'Food':'Food,FixFood'}},
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/food-for-life-I-know-who-grew-it/blog/52863/':{'Story':{'Food':'Food,FixFood'}},
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/food-for-life-I-know-who-grew-it/blog/52857/':{'Story':{'Food':'Food,FixFood'}},
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/tropical-deforestation/blog/51830/':{'Story':{'Food':'Food,FixFood,Deforestation'}},
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/join-the-food-movement/blog/51901/':{'Story':{'Food':'Food,FixFood'}},
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Agriculture/The-Environmental-Risks-of-neonicotinoid-pesticides/':{'Publication':{'Food':'Food,FixFood,Bees,Pesticides'}},
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Agriculture/Twenty-Years-of-Failure/':{'Publication':{'Food':'Food,FixFood,GeneticEngineering'}},
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Agriculture/Europes-Pesticide-Addiction/':{'Publication':{'Food':'Food,FixFood,Pesticides'}},
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Agriculture/Food-and-Farming-Vision/':{'Publication':{'Food':'Food,FixFood,EcologicalFarming'}},
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Agriculture/Pesticides-and-our-Health/':{'Publication':{'Food':'Food,FixFood,Bees,Pesticides'}},
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Agriculture/Pesticides-and-our-Health/':{'Publication':{'Food':'Food,FixFood,Pesticides'}},
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Agriculture/Smart-Breeding/':{'Publication':{'Food':'Food,FixFood,'}},
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Agriculture/Plan-Bee-Living-Without-Pesticides/':{'Publication':{'Food':'Food,FixFood,Bees,Pesticides'}},
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Agriculture/The-Bees-Burden/':{'Publication':{'Food':'Food,FixFood,Bees,Pesticides'}},
'http://www.greenpeace.org/international/en/publications/reports/Defining-Ecological-Farming/':{'Publication':{'Food':'Food,FixFood,EcologicalFarming'}},
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Agriculture/Ecological-Livestock/':{'Publication':{'Food':'Food,FixFood,LessMeatMorePlants'}},
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Genetic-engineering/Golden-Illusion/':{'Publication':{'Food':'Food,FixFood,GoldenRice'}},
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Agriculture/Bees-in-Decline/':{'Publication':{'Food':'Food,FixFood,Bees'}}}
        for url,typecattags in start_urls.items():
            for post_type,cattags in typecattags.items():
                for categories,tags in cattags.items():
                    if ( post_type=='Story' ):
                        request = scrapy.Request(url, callback=self.parse_blog)
                        yield request
                    elif ( post_type=='Publication' ):
                        request = scrapy.Request(url, callback=self.parse_publication)
                        yield request
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
            'date': response.css('div.news-list .caption::text').re_first(r' - \s*(.*)'),
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
            'date': response.css('div.news-list .caption::text').re_first(r' - \s*(.*)'),
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