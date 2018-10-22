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

class AllSpider(scrapy.Spider):
    name = 'all'

    custom_settings = {
        'ROBOTSTXT_OBEY': 0,
        'FEED_URI': 'gphu_staging_v2.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    __connector_csv_filename = "connector_v2_final.csv"
    __connector_csv_log_file = "connector_csv_log_v2"

    def start_requests(self):
    # v1
        start_urls = {
        #'http://www.greenpeace.org/hungary/hu/sajtokozpont/250-ezer-evig-kene-tarolnunk-Paks-II-atomhulladekat/':('Press Release','Klíma & Energia','Atomenergia','','','article','Migrate'),
        'http://www.greenpeace.org/hungary/hu/sajtokozpont/Szaz-evig-is-kiserthet-meg-a-fukusimai-katasztrofa/':('Press Release','Klíma & Energia','Atomenergia','Egészség','','article','Migrate'),
        'http://www.greenpeace.org/hungary/hu/sajtokozpont/240-Greenpeace-aktivista-figyelmeztet-Europa-uj-veszelyzonaba-lepett/':('Press Release','Klíma & Energia','Atomenergia','','','article','Migrate'),
        'http://www.greenpeace.org/hungary/hu/sajtokozpont/217-civil-szervezet-szolitotta-fel-az-unios-minisztereket-hogy-vessenek-veget-a-tengerek-tulhalaszatanak/':('Press Release','Természet & Környezet','Élővilág','Víz','','article','Migrate'),
        'http://www.greenpeace.org/hungary/hu/sajtokozpont/170412_civil_allasfoglalas/':('Press Release','Ember & Társadalom','Béke','','','article','Migrate'),
        'http://www.greenpeace.org/hungary/hu/sajtokozpont/170405_romaipart/':('Press Release','Természet & Környezet','Zöldterület','Egészség','Élővilág','article','Migrate'),
        'http://www.greenpeace.org/hungary/hu/sajtokozpont/14-millio-forintra-perli-az-allam-a-Greenpeace-t-es-Kishantost/':('Press Release','Ember & Társadalom','ÖkológiaiGazdálkodás','Béke','','article','Migrate'),
        'http://www.greenpeace.org/hungary/hu/sajtokozpont/118-civil-szervezet-kiall-a-helyi-kozossegekert-a-bekes-Magyarorszagert-dolgozo-civilekert/':('Press Release','Ember & Társadalom','Béke','','','article','Migrate'),
        'http://www.greenpeace.org/hungary/hu/sajtokozpont/107-civil-szervezet-nyilt-levele-Magyarorszag-ne-tamogassa-a-CETA-elfogadasat/':('Press Release','Ember & Társadalom','Fogyasztás','','','article','Migrate'),
        'http://www.greenpeace.org/hungary/hu/sajtokozpont/100-megujulo-energia-mindenkinek/':('Press Release','Klíma & Energia','Klímavédelem','Megújulók','','article','Migrate'),
        'http://www.greenpeace.org/hungary/hu/sajtokozpont/-Totalis-energiafuggseg-es-kiszolgaltatottsag/':('Press Release','Klíma & Energia','Atomenergia','','','article','Migrate'),
        'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Valaszuton-a-mezgazdasag/':('Publication','Természet & Környezet','ÖkológiaiGazdálkodás','','','article','Migrate'),
        'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Progressziv-EnergiaForradalom-2011-Magyar/':('Publication','Klíma & Energia','Klímavédelem','Megújulók','','article','Migrate'),
        'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Okomodszerek-szantofoldon/':('Publication','Természet & Környezet','ÖkológiaiGazdálkodás','','','article','Migrate'),
        'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Okologiai-allattenyesztes-a-vilagban-es-otthon/':('Publication','Természet & Környezet','ÖkológiaiGazdálkodás','','','article','Migrate'),
        'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Mit-tettunk-2016-ban/':('Publication','','Greenpeace','','','article','Migrate'),
        'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Mergek-vagy-mehek/':('Publication','Természet & Környezet','Élővilág','Méhek','','article','Migrate'),
        'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Mehpusztulas/':('Publication','Természet & Környezet','Élővilág','Méhek','','article','Migrate'),
        'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Megujulo-energia-megallas-nelkul/':('Publication','Klíma & Energia','Megújulók','Klímavédelem','','article','Migrate'),
        'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Maszatos-adatok/':('Publication','Ember & Társadalom','Fogyasztás','','','article','Migrate'),
        'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Kiteregetjuk-a-szennyest/':('Publication','Ember & Társadalom','Szennyezés','Fogyasztás','Egészség','article','Migrate')
}

        for url,data in start_urls.iteritems():
            p4_post_type, categories, tags1, tags2, tags3, post_type, action = data

            if (post_type == 'article'):
                request = scrapy.Request(url, callback=self.parse_page_type2, dont_filter='true')
            elif (post_type == 'news-list'):
                request = scrapy.Request(url, callback=self.parse_page_type1, dont_filter='true')


            if ( action.lower()=='migrate' ):
                request.meta['status'] = 'publish'
            if ( action.lower()=='archive' ):
                request.meta['status'] = 'draft'
            request.meta['categories'] = categories
            request.meta['tags1'] = tags1
            request.meta['tags2'] = tags2
            request.meta['tags3'] = tags3
            request.meta['action'] = action
            request.meta['post_type'] = post_type
            request.meta['p4_post_type'] = p4_post_type
            yield request

        # Migrating authors/thumbnails
        '''
        author_usernames = {
            'greenpeace': 'Greenpeace P4',
            'Keith Stewart': 'p4_username_keith',
            'Miriam Wilson'
        }

        # Read in the file
        with open( 'gpaf_staging_v1.xml', 'r' ) as file :
            filedata = file.read()

        # Replace with correct usernames.
        for p3_author_username, p4_author_username in author_usernames.iteritems():
            filedata = filedata.replace('<author_username>' + p3_author_username, '<author_username>' + p4_author_username)

        # Remove dir="ltr" attributes from elements as requested.
        filedata = filedata.replace('dir="ltr"', '')

        # Write the file out again
        with open('gpaf_staging_v1.xml', 'w') as file:
            file.write(filedata)
        '''

    # Class = 'news-list'
    # pagetypes = blogs,news
    def parse_page_type1(self, response):

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

        pdfFiles=response.css('div.news-list a[href$=".pdf"]::attr(href)').extract()
        pdf_files_generated = list()
        for pdf_file in pdfFiles:
            if (pdf_file.startswith('/')):
                pdf_file = pdf_file.replace('/','http://www.greenpeace.org/',1)
            pdf_files_generated.append(pdf_file)

        date_field = response.css('div.news-list .caption::text').re_first(r' - \s*(.*)')
        date_field = self.filter_month_name(date_field);
        # Filter extra string part from date.
        date_field = date_field.replace(" at", "")
        date_field = date_field.replace(" à", "")
        date_field = date_field.replace(" kl.", "")

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

        body_text = self.filter_post_content(body_text)

        images=response.xpath('//*[@class="post-content"]/div/p/a//img[contains(@style, "float:")]').extract()   #img[@style="margin: 9px; float: left;"]
        imagesD_generated = list()
        for image in images:
            imagesD_generated.append(image)

        blockquotes = response.xpath('//*[@id="content"]//blockquote').extract()
        blockquotes_generated = list()
        for blockquote in blockquotes:
            blockquotes_generated.append(blockquote)

        author_username = response.xpath('string(//div[@class="news-list"]/ul/li/*/*/span[@class="caption"]/span[@class="green1"]/strong/a/@href)').extract_first()
        if (author_username != 'None'):
            Segments  = author_username.strip().split('/')
            try:                                            #if ( ( len(Segments) == 4 ) and Segments[4] ):
                if ( Segments[4] ):
                    author_username = Segments[4]
            except IndexError:
                author_username = ''

        # Get the thumbnail of the post as requested.
        thumbnail = response.xpath('string(head//link[@rel="image_src"]/@href)').extract_first()

        unique_map_id = int(time.time() + random.randint(0, 999))

        # Filter email id image and replace it with email text.
        delete_images = list()
        for image_file in imagesB_generated:
            #f1=open('/tmp/debug.txt', 'a+')
            if ("/emailimages/" in image_file):
                # PHP webservice script url.
                api_url = "http://127.0.0.1/ocr-api-test/email_img_to_text.php"
                end_point_url = api_url + "?url=" + image_file
                emailid = urllib2.urlopen(end_point_url).read(1000)
                # Search replace the \n, <BR>, spaces from email id.
                emailid = emailid.replace('\n', '')
                emailid = emailid.replace('<br>', '')
                emailid = emailid.replace('<BR>', '')
                emailid = emailid.replace(' ', '')
                emailid = emailid.replace('qreenpeace', 'greenpeace')
                emailid = emailid.replace('aqreenpeace', '@greenpeace')
                emailid = emailid.replace('@qreenpeace', '@greenpeace')
                emailid = emailid.replace('agreenpeace', '@greenpeace')
                #f1.write(emailid)
                delete_images.append(image_file)
                # Remove the email images from Post body and replace it with email text.
                body_text = re.sub(
                    '<img[a-zA-Z0-9="\s\_]*src=\"' + image_file + '\"[a-zA-Z0-9="\s]*>',
                    emailid, body_text)
            #f1.close()

        # Remove the email images from list.
        for image_file in delete_images:
            imagesB_generated.remove(image_file)


        """
        #list images urls
        for image_file in imagesB_generated:
            if ("/emailimages/" in image_file):
                data = [image_file]
                self.csv_writer(data, "email_images_url_list_fr_story.csv")
        """

        yield {
            'type': response.meta['p4_post_type'],
            'p3_image_gallery': p3_image_gallery,
            'title': extract_with_css('div.news-list h1::text'),
            #'subtitle': '',
            'author': 'Greenpeace Magyarország',
            'author_username': 'greenpeacehu',
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
            'tags1': response.meta['tags1'],
            'tags2': response.meta['tags2'],
            'tags3': response.meta['tags3'],
            'url': response.url,
            'status': response.meta['status'],
            'map_url': '',
            'unique_map_id': unique_map_id,
            'thumbnail': thumbnail,
        }

    # class = 'happen-box article'
    # pagetypes = parse_publication,parse_press,parse_feature
    def parse_page_type2(self, response):

        def extract_with_css(query):
            return response.css(query).extract_first()

        imagesA=response.xpath('//div[@class="post-content"]//a[img]/@href').extract()
        imagesA_generated = list()
        for image_file in imagesA:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.org/',1)
            imagesA_generated.append(image_file)

        imagesB=response.xpath('//div[@class="post-content"]//img/@src').extract()
        if len(imagesB) == 0:
            imagesB = response.xpath('//div[@id="content"]//img/@src').extract()

        imagesB_generated = list()
        for image_file in imagesB:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.org/',1)
            # Custom fix for GPAF only.
            if 'http://assets.pinterest.com/images/PinExt.png' not in image_file:
                imagesB_generated.append(image_file)

        pdfFiles=response.css('div.article a[href$=".pdf"]::attr(href)').extract()
        pdf_files_generated = list()
        for pdf_file in pdfFiles:
            if (pdf_file.startswith('/')):
                pdf_file = pdf_file.replace('/','http://www.greenpeace.org/',1)
            pdf_files_generated.append(pdf_file)

        image_gallery=response.xpath("//*[contains(@class, 'embedded-image-gallery')]")
        p3_image_gallery = 'false'
        if image_gallery:
            p3_image_gallery = 'true'

        try:
            lead_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[1]/div/text()').extract()[0]
        except IndexError:
            lead_text = ''

        body_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[2]').extract()[0]
        if body_text:
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.org/').replace('href="/', 'href="http://www.greenpeace.org/')
            body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)
            if lead_text:
                body_text = '<div class="leader">' + lead_text + '</div>' + body_text + response.xpath(' //*[@id="content"]/div[4]/div/div[2]/p').extract_first()

        subtitle = extract_with_css('div.article h2 span::text')
        if subtitle:
            body_text = '<h2>' + subtitle + '</h2><br />' + body_text

        thumbnail = response.xpath('string(head//link[@rel="image_src"]/@href)').extract_first()

        date_field = response.css('div.article div.text span.author::text').re_first(r' - \s*(.*)')
        date_field = self.filter_month_name(date_field);
        # Filter extra string part from date.
        date_field = date_field.replace(" at", "")
        date_field = date_field.replace(" à", "")
        date_field = date_field.replace(" kl.", "")

        if date_field:
            date_field = dateutil.parser.parse(date_field)

        # Filter email id image and replace it with email text.
        delete_images = list()
        for image_file in imagesB_generated:
            #f1=open('/tmp/debug.txt', 'a+')
            if ("/emailimages/" in image_file):
                api_url = "http://127.0.0.1/ocr-api-test/email_img_to_text.php"
                end_point_url = api_url+"?url="+image_file
                emailid = urllib2.urlopen(end_point_url).read(1000)
                # Search replace the \n, <BR>, spaces from email id.
                emailid = emailid.replace('\n', '')
                emailid = emailid.replace('<br>', '')
                emailid = emailid.replace('<BR>', '')
                emailid = emailid.replace(' ', '')
                emailid = emailid.replace('qreenpeace', 'greenpeace')
                emailid = emailid.replace('aqreenpeace', '@greenpeace')
                emailid = emailid.replace('@qreenpeace', '@greenpeace')
                emailid = emailid.replace('agreenpeace', '@greenpeace')
                #f1.write(emailid)
                delete_images.append(image_file)
                # Remove the email images from Post body and replace it with email text.
                body_text = re.sub(
                    '<img[a-zA-Z0-9="\s\_]*src=\"'+image_file+'\"[a-zA-Z0-9="\s]*>',
                    emailid, body_text)
            #f1.close()

        # Remove the email images from list.
        for image_file in delete_images:
            imagesB_generated.remove(image_file)

        """
        #list images urls
        for image_file in imagesB_generated:
            if ("/emailimages/" in image_file):
                data = [image_file]
                self.csv_writer(data, "email_images_url_list_fr.csv")
        """


        # Post data mapping logic start.
        unique_map_id = int(time.time() + random.randint(0, 999))

        if "/en/" in response.url:
            # For English language POSTs

            # Check the POST transalation availability
            try:
                map_url = response.xpath('//*[@class="language"]//option[2]/@value').extract()[0]
            except IndexError:
                map_url = ''

            if "/fr/" not in map_url:
                map_url = ''

            if map_url:
                map_url = 'http://www.greenpeace.org' + map_url

                # The Post mapping data added into csv file.
                data = [unique_map_id, response.url, map_url]
                self.csv_writer(data, self.__connector_csv_filename)

                data = [response.url, response.meta['p4_post_type'], response.meta['categories'], response.meta['tags1'], response.meta['tags2'], response.meta['tags3'], response.meta['post_type'], response.meta['action']]
                self.csv_writer(data, "Language_mapping_en_list.csv")
        else:
            # For French language POSTs

            # Check the POST transalation if available
            try:
                map_url = response.xpath('//*[@class="language"]//option[1]/@value').extract()[0]
            except IndexError:
                map_url = ''

            if "/en/" not in map_url:
                map_url = ''

            if map_url:
                map_url = 'http://www.greenpeace.org' + map_url

                with open(self.__connector_csv_filename, "rb") as file_obj:
                    reader = csv.reader(file_obj)
                    for row in reader:
                        if (row[1] == map_url or row[2] == response.url):
                            #print "=======Match found======="
                            unique_map_id = row[0]
                            # Log the details
                            data = ["FR==>", unique_map_id, response.url, map_url,"EN==>", row[0], row[1], row[2]]
                            #print data
                            self.csv_writer(data, self.__connector_csv_log_file)

                            data = [response.url, response.meta['p4_post_type'], response.meta['categories'],
                                    response.meta['tags1'], response.meta['tags2'], response.meta['tags3'],
                                    response.meta['post_type'], response.meta['action']]
                            self.csv_writer(data, "Language_mapping_fr_list.csv")
        # Post data mapping logic ends.

        yield {
            'type': response.meta['p4_post_type'],
            'p3_image_gallery': p3_image_gallery,
            'title': extract_with_css('div.article h1 span::text'),
            #'subtitle': '',
            'author': 'Greenpeace Magyarország',
            'author_username': 'greenpeacehu',
            #'date': response.css('#content > div.happen-box.article > div > div.text > span').re_first(r' - \s*(.*)'),
            'date': date_field,
            #'lead': extract_with_css('div.news-list div.post-content *:first-child strong::text'),
            'lead': extract_with_css('#content > div.happen-box.article > div > div.text > div.leader > div'),
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
            'tags3': response.meta['tags3'],
            'map_url': map_url,
            'unique_map_id': unique_map_id,
            'url': response.url,
        }

    def filter_post_content(self, post_data):
        # Filter the youtube video and add embed shortcode instead.
        post_data = re.sub(
            '\<object[width\=\"height0-9\s]*data\=\"([https]*\:\/\/www.youtube.com[a-zA-Z0-9\/\=\-\?\_]*)\"[\=\"a-zA-Z\/\-\s0-9]*\>[\\n\s]*(.*)[\\n\s]*\<\/object\>',
            '[embed]\g<1>[/embed]', post_data)

        return post_data

    def filter_month_name(self, month_name):
        '''
        month_fr_en = {
            'janvier': 'January',
            'février': 'February',
            'mars': 'March',
            'avril': 'April',
            'mai': 'May',
            'juin': 'June',
            'juillet': 'July',
            'août': 'August',
            'septembre': 'September',
            'octobre': 'October',
            'novembre': 'November',
            'décembre': 'December',
        }
        '''

        # Replace the french month name with english month name.
        #for fr_month, en_month in month_fr_en.iteritems():
        #    month_name = month_name.replace(fr_month, en_month)

        month_da_en = {
            'január': 'January',
            'február': 'February',
            'március': 'March',
            'április': 'April',
            'Lehet': 'May',
            'június': 'June',
            'július': 'July',
            'augusztus': 'August',
            'szeptember': 'September',
            'október': 'October',
            'november': 'November',
            'december': 'December',
        }

        # Replace the danish month name with english month name.
        for fr_month, en_month in month_da_en.iteritems():
            month_name = month_name.replace(fr_month, en_month)

        return month_name;

    def csv_writer(self, data, path):
        # Write data to a CSV file path
        with open(path, "a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(data)
