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
        'FEED_URI': 'gpcz_staging_v2.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    __connector_csv_filename = "connector_v2_final.csv"
    __connector_csv_log_file = "connector_csv_log_v2"

    def start_requests(self):
        # v1
        start_urls = {
            'http://www.greenpeace.org/czech/cz/blogy/Zmena-klimatu-a-energetika/blackout-nehrozi/blog/61832/':('Článek','Energetická revoluce','ObnovitelnéZdroje','KonecDobyFosilní','','news-list','Migrate'),
            'http://www.greenpeace.org/czech/cz/blogy/Zmena-klimatu-a-energetika/chvaletice-reakce-infocz/blog/61542/':('Článek','Energetická revoluce','AktivníSpolečnost','KonecDobyFosilní','','news-list','Migrate'),
            'http://www.greenpeace.org/czech/cz/blogy/Zmena-klimatu-a-energetika/kolik-stoji-vedro/blog/61831/':('Článek','Příroda','ZměnaKlimatu','KonecDobyFosilní','','news-list','Migrate'),
            'http://www.greenpeace.org/czech/cz/blogy/Zmena-klimatu-a-energetika/teplo-nebo-cisty-vzduch-oboji/blog/61545/':('Článek','Náš svět','Ovzduší','KonecDobyFosilní','','news-list','Migrate'),
            'http://www.greenpeace.org/czech/cz/Multimedia1/Publikace/Energeticka-revoluce-pro-CR/':('Publikace','Energetická revoluce','ObnovitelnéZdroje','','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/Multimedia1/Publikace/Hodnoceni-nadnarodnich-spolecnosti/':('Publikace','Příroda','Lesy&Pralesy','','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/Multimedia1/Publikace/jak-se-oblekat-na-vylety/':('Publikace','Příroda','BezChemie','','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/Multimedia1/Publikace/Toxicke-uhli-zdravotni-naklady-slabych-emisnich-limitu-EU/':('Publikace','Příroda','Ovzduší','','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/Multimedia1/Publikace/V-plamenech/':('Publikace','Příroda','Lesy&Pralesy','','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/Multimedia1/Publikace/Vyrocni-zprava-2017/':('Publikace','Greenpeace','O nás','','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/news/moratorium-indonesie-nestaci/':('Tisková zpráva','Příroda','Lesy&Pralesy','','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/news/Za-klimatickou-spravedlnost-a-ciste-ovzdusi-bez-vyjimek/':('Článek','Energetická revoluce','KonecDobyFosilní','AktivníSpolečnost','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/-Pes-70-tisic-lidi-se-pidalo-k-vyzv-za-omezeni-jednorazovych-plast-v-tchto-dnech-pii-supermarketm/':('Tisková zpráva','Náš svět','PlastJePast','Neplýtváme','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/antarktida-expedice/':('Tisková zpráva','Příroda','Oceány','','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/antarktida-kril-report/':('Tisková zpráva','Příroda','Oceány','','','article','Migrate')
        }

        # v2
        start_urls = {
            'http://www.greenpeace.org/czech/cz/blogy/Zmena-klimatu-a-energetika/blackout-nehrozi/blog/61832/':('Článek','Energetická revoluce','ObnovitelnéZdroje','KonecDobyFosilní','','news-list','Migrate'),
            'http://www.greenpeace.org/czech/cz/blogy/Zmena-klimatu-a-energetika/chvaletice-reakce-infocz/blog/61542/':('Článek','Energetická revoluce','AktivníSpolečnost','KonecDobyFosilní','','news-list','Migrate'),
            'http://www.greenpeace.org/czech/cz/blogy/Zmena-klimatu-a-energetika/kolik-stoji-vedro/blog/61831/':('Článek','Příroda','ZměnaKlimatu','KonecDobyFosilní','','news-list','Migrate'),
            'http://www.greenpeace.org/czech/cz/blogy/Zmena-klimatu-a-energetika/teplo-nebo-cisty-vzduch-oboji/blog/61545/':('Článek','Náš svět','Ovzduší','KonecDobyFosilní','','news-list','Migrate'),
            'http://www.greenpeace.org/czech/cz/Multimedia1/Publikace/Energeticka-revoluce-pro-CR/':('Publikace','Energetická revoluce','ObnovitelnéZdroje','','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/Multimedia1/Publikace/Hodnoceni-nadnarodnich-spolecnosti/':('Publikace','Příroda','Lesy&Pralesy','','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/Multimedia1/Publikace/jak-se-oblekat-na-vylety/':('Publikace','Příroda','BezChemie','','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/Multimedia1/Publikace/Toxicke-uhli-zdravotni-naklady-slabych-emisnich-limitu-EU/':('Publikace','Příroda','Ovzduší','','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/Multimedia1/Publikace/V-plamenech/':('Publikace','Příroda','Lesy&Pralesy','','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/Multimedia1/Publikace/Vyrocni-zprava-2017/':('Publikace','Greenpeace','O nás','','','article','Migrate'),
            # data issue for below post during import.
            #'http://www.greenpeace.org/czech/cz/news/moratorium-indonesie-nestaci/':('Tisková zpráva','Příroda','Lesy&Pralesy','','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/news/Za-klimatickou-spravedlnost-a-ciste-ovzdusi-bez-vyjimek/':('Článek','Energetická revoluce','KonecDobyFosilní','AktivníSpolečnost','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/-Pes-70-tisic-lidi-se-pidalo-k-vyzv-za-omezeni-jednorazovych-plast-v-tchto-dnech-pii-supermarketm/':('Tisková zpráva','Náš svět','PlastJePast','Neplýtváme','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/antarktida-expedice/':('Tisková zpráva','Příroda','Oceány','','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/antarktida-kril-report/':('Tisková zpráva','Příroda','Oceány','','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/blogy/Dalsi-temata/antarktida-historie/blog/61537/':('Článek','Příroda','Oceány','','','news-list','Migrate'),
            'http://www.greenpeace.org/czech/cz/blogy/Dalsi-temata/ekovyzva-2018-ohlednuti/blog/61512/':('Článek','Náš svět','Neplýtváme','BezChemie','','news-list','Migrate'),
            'http://www.greenpeace.org/czech/cz/blogy/Dalsi-temata/hasicky-indonesie/blog/61220/':('Článek','Příroda','Lesy&Pralesy','','','news-list','Migrate'),
            'http://www.greenpeace.org/czech/cz/blogy/Dalsi-temata/jak-byt-vegetarianem/blog/56410/':('Článek','Příroda','ZměnaKlimatu','','','news-list','Migrate'),
            'http://www.greenpeace.org/czech/cz/blogy/Dalsi-temata/mikroplasty-kosmetika/blog/60009/':('Článek','Náš svět','PlastJePast','Oceány','','news-list','Migrate'),
            'http://www.greenpeace.org/czech/cz/blogy/Dalsi-temata/plast-je-past-akce-v-brne/blog/61818/':('Článek','Náš svět','PlastJePast','AktivníSpolečnost','','news-list','Migrate'),
            'http://www.greenpeace.org/czech/cz/blogy/Dalsi-temata/rajky-v-ohrozeni/blog/61884/':('Článek','Příroda','Lesy&Pralesy','','','news-list','Migrate'),
            'http://www.greenpeace.org/czech/cz/blogy/Dalsi-temata/zakony-na-plasty/blog/61001/':('Článek','Náš svět','PlastJePast','','','news-list','Migrate'),
            'http://www.greenpeace.org/czech/cz/blogy/Oceany/antarktida-chranene-oblasti-morskeho-dna/blog/61736/':('Článek','Příroda','Oceány','','','news-list','Migrate'),
            'http://www.greenpeace.org/czech/cz/blogy/Oceany/co-jsou-mikroplasty-a-pro-je-musme-omezit/blog/61839/':('Článek','Náš svět','PlastJePast','','','news-list','Migrate'),
            'http://www.greenpeace.org/czech/cz/blogy/Oceany/krunyrovka-krilova-magazin/blog/61538/':('Článek','Příroda','Oceány','','','news-list','Migrate'),
            'http://www.greenpeace.org/czech/cz/blogy/Oceany/myty-o-oze-vitr/blog/61540/':('Článek','Energetická revoluce','ObnovitelnéZdroje','KonecDobyFosilní','','news-list','Migrate'),
            'http://www.greenpeace.org/czech/cz/blogy/Oceany/plast-strategie-EU/blog/61084/':('Článek','Náš svět','PlastJePast','','','news-list','Migrate'),
            'http://www.greenpeace.org/czech/cz/blogy/Oceany/plast-z-obleceni/blog/61862/':('Článek','Náš svět','PlastJePast','','','news-list','Migrate'),
            'http://www.greenpeace.org/czech/cz/blogy/Oceany/plasty-a-role-korporaci/blog/61408/':('Článek','Náš svět','PlastJePast','','','news-list','Migrate'),
            'http://www.greenpeace.org/czech/cz/blogy/Oceany/plasty-vraci-uder/blog/61543/':('Článek','Příroda','PlastJePast','','','news-list','Migrate'),
            'http://www.greenpeace.org/czech/cz/blogy/Oceany/rozhovor-john-hocevar/blog/61539/':('Článek','Příroda','Oceány','','','news-list','Migrate'),
            'http://www.greenpeace.org/czech/cz/blogy/Oceany/top-5-tucnaku/blog/61063/':('Článek','Příroda','Oceány','','','news-list','Migrate'),
            'http://www.greenpeace.org/czech/cz/blogy/Oceany/zaloba-bref-referendum/blog/61030/':('Článek','Příroda','Ovzduší','KonecDobyFosilní','','news-list','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/antarktida-ponor/':('Tisková zpráva','Příroda','Oceány','','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/CSOB-konec-investic-uhli/':('Tisková zpráva','Energetická revoluce','KonecDobyFosilní','ZměnaKlimatu','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/Emise-z-Chvaletic/':('Tisková zpráva','Příroda','Ovzduší','KonecDobyFosilní','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/EU-smernice-plastove-znecisteni/':('Tisková zpráva','Náš svět','PlastJePast','','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/Evropsky-parlament-podpoil-obanskou-energetiku/':('Tisková zpráva','Energetická revoluce','ObnovitelnéZdroje','ZměnaKlimatu','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/Evropsky-soudni-dvur-Belovez-rozhodnuti/':('Tisková zpráva','Příroda','Lesy&Pralesy','','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/GLYFOSAT-EVROPSKE-STATY-ODHLASOVALY-PRODLOUZENI-O-DALSICH-PET-LET-BEZ-OMEZENI/':('Tisková zpráva','Náš svět','BezChemie','','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/Greenpeace-odebira-vzorky-vody-z-Vltavy-Bude-v-nich-hledat-mikroplasty/':('Tisková zpráva','Náš svět','PlastJePast','','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/Greenpeace-vyzyva-k-omezeni-ivoine-vyroby-Produkce-a-spoteba-masa-se-musi-sniit-na-polovinu/':('Tisková zpráva','Příroda','ZměnaKlimatu','Neplýtváme','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/kril-oznameni/':('Tisková zpráva','Příroda','Oceány','','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/Lide-protestovali-proti-nadbytecnym-plastum/':('Tisková zpráva','Náš svět','PlastJePast','Neplýtváme','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/Na-zdi-na-praskem-ikov-se-uhnizdi-ptaci-z-raje-Streetart-upozoruje-na-kaceni-prales/':('Tisková zpráva','Příroda','Lesy&Pralesy','','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/norsky-sod-verdikt/':('Tisková zpráva','Příroda','Oceány','KonecDobyFosilní','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/obvineni-uhradili-skodu-chvaletice/':('Tisková zpráva','Energetická revoluce','KonecDobyFosilní','AktivníSpolečnost','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/pocerady-zaloba-priznani/':('Tisková zpráva','Energetická revoluce','KonecDobyFosilní','Ovzduší','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/reakce-obvineni-Chvaletice/':('Tisková zpráva','Energetická revoluce','KonecDobyFosilní','KonecDobyFosilní','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/Rezignaci-na-zvyeni-poplatk-z-tby-by-vlada-poruila-svj-program-Ve-prospch-uhlobaron/':('Tisková zpráva','Energetická revoluce','KonecDobyFosilní','Neplýtváme','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/skola-solarni-panely-horni-jiretin/':('Tisková zpráva','Energetická revoluce','ObnovitelnéZdroje','','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/Soud-bude-znovu-eit-tbu-ropy-v-Arktid-Ekologicke-organizace-se-odvolaly/':('Tisková zpráva','Příroda','Oceány','KonecDobyFosilní','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/uhli-a-rtut-studie/':('Tisková zpráva','Náš svět','BezChemie','Ovzduší','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/utlum-uhli-politicke-strany/':('Tisková zpráva','Energetická revoluce','KonecDobyFosilní','ObnovitelnéZdroje','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/Vetsina-poslancu-dala-prednost-uhelne-lobby-vyjimky-bref/':('Tisková zpráva','Náš svět','Ovzduší','KonecDobyFosilní','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/Vyetovani-Greenpeacu-ukazuje-e-kaceni-prales-se-pesouva-na-Papuu---/':('Tisková zpráva','Příroda','Lesy&Pralesy','','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/vzrostl-vyvoz-elektriny/':('Tisková zpráva','Energetická revoluce','KonecDobyFosilní','Ovzduší','','article','Migrate'),
            'http://www.greenpeace.org/czech/cz/press/zastupce-souhlasi-s-vysi-skody/':('Tisková zpráva','Energetická revoluce','KonecDobyFosilní','AktivníSpolečnost','','article','Migrate'),
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
        date_field = date_field.replace(" v", "")

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
            if ("/emailimages/" in image_file):
                # PHP webservice script url.
                api_url = "http://localhosttest/ocr_webservice/email_img_to_text.php"
                end_point_url = api_url + "?url=" + image_file
                emailid = urllib2.urlopen(end_point_url).read(1000)
                # Search replace the \n, <BR>, spaces from email id.
                emailid = emailid.replace('\n', '')
                emailid = emailid.replace('<br>', '')
                emailid = emailid.replace('<BR>', '')
                emailid = emailid.replace(' ', '')
                delete_images.append(image_file)
                # Remove the email images from Post body and replace it with email text.
                body_text = re.sub(
                    '<img[a-zA-Z0-9="\s\_]*src=\"' + image_file + '\"[a-zA-Z0-9="\s]*>',
                    '<a href="mailto:' + emailid.strip() + '" target="_blank">' + emailid.strip() + '</a>', body_text)

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
            'author': response.xpath('string(//div[@class="news-list"]/ul/li/*/*/span[@class="caption"]/span[@class="green1"]/strong)').extract()[0],
            'author_username': author_username,
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
        date_field = date_field.replace(" v", "")

        if date_field:
            date_field = dateutil.parser.parse(date_field)

        # Filter email id image and replace it with email text.
        delete_images = list()
        for image_file in imagesB_generated:
            if ("/emailimages/" in image_file):
                api_url = "http://localhosttest/ocr_webservice/email_img_to_text.php"
                end_point_url = api_url+"?url="+image_file
                emailid = urllib2.urlopen(end_point_url).read(1000)
                # Search replace the \n, <BR>, spaces from email id.
                emailid = emailid.replace('\n', '')
                emailid = emailid.replace('<br>', '')
                emailid = emailid.replace('<BR>', '')
                emailid = emailid.replace(' ', '')
                delete_images.append(image_file)
                # Remove the email images from Post body and replace it with email text.
                body_text = re.sub(
                    '<img[a-zA-Z0-9="\s\_]*src=\"'+image_file+'\"[a-zA-Z0-9="\s]*>',
                    '<a href="mailto:' + emailid.strip() + '" target="_blank">' + emailid.strip() + '</a>', body_text)

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
        map_url = ''
        """
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
        """

        yield {
            'type': response.meta['p4_post_type'],
            'p3_image_gallery': p3_image_gallery,
            'title': extract_with_css('div.article h1 span::text'),
            #'subtitle': '',
            'author': 'Greenpeace Česká republika',
            'author_username': 'greenpeace',
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

        month_cz_en = {
            'ledna': 'January',
            #'Únor': 'February', #pending
            'února':'February',
            'března': 'March',
            #'duben': 'April', #pending
            'dubna':'April',
            'května': 'May',
            'června': 'June',
            #'červenec': 'July', #pending
            'července':'July',
            'srpna': 'August',
            'září': 'September',
            'říjen': 'October', #pending
            #'listopad': 'November', #pending
            'listopadu': 'November',  # pending
            'prosinec': 'December', #pending
        }

        # Replace the Czech month name with english month name.
        for cz_month, en_month in month_cz_en.iteritems():
            month_name = month_name.replace(cz_month, en_month)

        return month_name;

    def csv_writer(self, data, path):
        # Write data to a CSV file path
        with open(path, "a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(data)
