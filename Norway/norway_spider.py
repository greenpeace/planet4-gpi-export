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
        'FEED_URI': 'gpno_production_v1.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    __connector_csv_filename = "connector_v2_final.csv"
    __connector_csv_log_file = "connector_csv_log_v2"

    def start_requests(self):
        # v1
        start_urls = {
            'http://www.greenpeace.org/norway/no/kampanjer/tjaresand/Statoil-and-the-tar-sands-in-Canada-/':('Nyheter','Klima','','Energi','Klimaendringer','Olje','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2018/Eier-du-aksjer-i-Statoil-Hjelp-oss-a-stanse-grunnlovsstridig-oljeboring/':('Nyheter','Klima','','Energi','Klimaendringer','Olje','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2016/Trump-kan-bli-en-katastrofe-for-miljoet---men-det-finnes-hap/':('Nyheter','Klima','','Klimaendringer','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/blogg/topp-10-dummeste-ting-sagt-om-global-oppvarmi/blog/50995/':('Nyheter','Klima','','Klimaendringer','','','news-list','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2017/Ny-rapport---Oljefondet-bor-trekkes-ut-fra-alle-olje--og-gassaksjer/':('Nyheter','Klima','','Olje','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2018/Okonomer-stotter-stans-i-oljeleting/':('Nyheter','Klima','','Klimasøksmål','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/press/releases/2016/Norways-oil-fund-starts-divestment-from-coal/':('Nyheter','Klima','','Olje','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2018/Forspiller-Norge-15-milliarder-kroner-og-sjanse-til-a-gjore-noe-godt-for-regnskogen-/':('Nyheter','Klima','','Natur','Skog','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2018/Oljefondet-inn-i-mer-fornybar-energi/':('Nyheter','Klima','','Olje','Løsninger','Energi','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2017/New-report-The-Oilfund-should-divest-from-oil-and-gas/':('Nyheter','Klima','','Olje','Løsninger','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2018/Greenpeace-avslorer-77-milliarder-pensjonspenger-i-kull/':('Nyheter','Klima','','Olje','Løsninger','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2018/Avviser-direkte-anke-til-Hoyesterett-i-klimasoksmalet/':('Nyheter','Klima','','Klimasøksmål','Olje','Løsninger','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2016/Saksoker-staten-for-klimalovbrudd/':('Nyheter','Klima','','Klimasøksmål','Folkebevegelse','Løsninger','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2017/Oppdatering-om-klimasoksmalet/':('Nyheter','Klima','','Klimasøksmål','Olje','Løsninger','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2018/Anker-klimadommen-til-Hoyesterett/':('Nyheter','Klima','','Klimasøksmål','Olje','Løsninger','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2018/Norge-ma-levere-krisepakke-for-klima/':('Pressemelding','Klima','','Klimaendringer','Olje','Løsninger','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2016/Vil-stevne-regjeringen-for-grunnlovsbrudd/':('Nyheter','Mennesker','','Klimasøksmål','Olje','Løsninger','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2016/Alternative-julegaver-som-sparer-miljoet-og-sprer-glede/':('Nyheter','Mennesker','','Forbruk','Løsninger','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2017/Hvor-gronn-er-din-smarttelefon-/':('Nyheter','Mennesker','','Forbruk','Forurensning','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/Blogg/10-tips-for-en-giftfri-garderobe/blog/55731/':('Nyheter','Mennesker','','Forbruk','Løsninger','','news-list','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2017/Plastforurensning-av-havet-/':('Pressemelding','Natur','','Hav','Forurensning','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2013/Tunfisk-En-liten-guide-for-deg-som-vil-spise-barekraftig/':('Nyheter','Natur','','Hav','Løsninger','Forbruk','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2017/Norsk-hvalfangst-er-unodvendig-og-i-strid-med-internasjonale-avtaler/':('Nyheter','Natur','','Hav','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2016/Moratorium-pa-arktisk-bunntraling/':('Pressemelding','Natur','','Hav','Løsninger','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2016/Norge-ma-forby-mikroplast/':('Nyheter','Natur','','Hav','Forurensning','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/Blogg/trlfiske-ved-svalbard-delegger-srbar-havbunn-/blog/55698/':('Pressemelding','Natur','','Hav','Biodiversitet','','news-list','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2017/Mikroplastforurensning-fra-kunstgress---et-kjempeproblem/':('Nyheter','Natur','','Hav','Forurensning','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2018/Aker-fisker-krill-i-pingvinens-matfat-/':('Nyheter','Natur','','Hav','Biodiversitet','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2018/Greenpeace-har-funnet-mikroplast-i-avsides-omrader-av-Antarktis/':('Pressemelding','Natur','','Hav','Forurensning','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2018/Vil-beskytte-Antarktis/':('Nyheter','Natur','','Hav','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2016/Vil-verne-Svalbard-mot-farlig-fiske/':('Nyheter','Natur','','Hav','Biodiversitet','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2017/220-000-mennesker-verden-over-ber-Norge-beskytte-havet/':('Nyheter','Natur','','Folkebevegelse','Hav','Biodiversitet','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2018/Gode-nyheter-for-Antarktis/':('Pressemelding','Natur','','Hav','Biodiversitet','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2016/Syv-myter-om-GMO-og-sannheten-bak-dem/':('Nyheter','Greenpeace','','Forbruk','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2017/4-tiltak-du-kan-gjore-for-et-renere-hav/':('Nyheter','Greenpeace','','Hav','Løsninger','Forbruk','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2016/Greenpeace-foreslar-losning-for-atomavfall/':('Nyheter','Greenpeace','','Energi','Forurensning','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2017/Vare-krav-til-ny-regjering/':('Nyheter','Greenpeace','','Løsninger','Olje','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2018/Hav-vern-og-verdiskapning-hand-i-hand/':('Nyheter','Natur','','Hav','Biodiversitet','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/Hvordan-DU-kan-hjelpe-verdens-klima/':('Nyheter','Mennesker','','Løsninger','Forbruk','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2018/Norge-odela-for-viktig-marint-vern-i-Antarktis/':('Pressemelding','Natur','','Hav','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2018/Til-klimastreikerne---takk/':('Nyheter','Mennesker','','Folkebevegelse','Løsninger','Klimaendringer','article','Migrate'),
            'http://www.greenpeace.org/norway/no/Klimaendringer-rammer-kvinner-hardest/':('Nyheter','Mennesker','','Klimaendringer','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2018/Oljefondet-ut-av-olje-og-gass/':('Pressemelding','Klima','','Olje','Energi','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2018/Oljefondet-trekker-investeringer-fra-plantasjeselskap-etter-Greenpeace-rapport/':('Pressemelding','Klima','','Olje','Skog','Biodiversitet','article','Migrate'),
            'http://www.greenpeace.org/norway/no/Derfor-bruker-vi-sivil-ulydighet/':('Nyheter','Greenpeace','','Folkebevegelse','EngasjerDeg','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2018/Norge-finansierer-fortsatt-fremtidens-klimakatastrofe/':('Pressemelding','Klima','','Olje','Energi','','article','Migrate'),

            'http://www.greenpeace.org/norway/no/nyheter/2018/Mindre-kjott-mer-gront/':('Nyheter','Mennesker','','Forbruk','Klimaendringer','Løsninger','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2016/Appell-om-ulv/':('Pressemelding','Natur','','Biodiversitet','Natur','Folkebevegelse','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2017/Klimasoksmalet/':('Nyheter','Klima','','Olje','Klimasøksmål','Energi','article','Migrate'),
            'http://www.greenpeace.org/norway/no/press/releases/Greenpeace-er-arrestert/':('Nyheter','Klima','','Olje','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2017/Historisk-klimarettssak-avsluttet/':('Nyheter','Klima','','Olje','Klimasøksmål','Energi','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2017/Ny-rapport-Alvorlige-funn-viser-at-regjeringen-har-jukset-om-arktisk-olje/':('Pressemelding','Klima','','Olje','Klimasøksmål','Energi','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/Norge-er-verdens-syvende-storste-eksportor-av-CO2-utslipp/':('Pressemelding','Klima','','Olje','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2017/Klimarettssaken-en-seier-for-miljoet/':('Nyheter','Klima','','Olje','Klimasøksmål','Energi','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2016/Klimasoksmalet-skal-i-retten/':('Pressemelding','Klima','','Olje','Klimasøksmål','Energi','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2017/-Klimasoksmalet---dag-for-dag/':('Nyheter','Klima','','Klimasøksmål','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2018/Greenpeace-and-Nature-and-Youth-take-the-Norwegian-Government-to-the-Supreme-Court/':('Pressemelding','Klima','','Klimasøksmål','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/blogg/et-klimasksml-som-utfordrer-olja/blog/58240/':('Nyheter','Klima','','Klimasøksmål','','','news-list','Migrate'),
            'http://www.greenpeace.org/norway/no/press/releases/Ingen-rett-til-a-borde/':('Pressemelding','Klima','','Olje','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2017/Klimarettssak-i-november/':('Pressemelding','Klima','','Klimasøksmål','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2017/Skal-Statoil-virkelig-fa-bore-fritt-i-alkefuglenes-svommetrekk-og-oppsamlingsomrader/':('Nyheter','Klima','','Olje','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2016/Norway-allows-dangerous-oil-exploration-in-fragile-Artic-waters/':('Pressemelding','Klima','','Olje','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2017/Krever-at-Statoil-avlyser-oljeboring/':('Pressemelding','Klima','','Olje','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2018/Historisk-klima-dom-i-Nederland/':('Nyheter','Klima','','Klimasøksmål','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/press/releases/Greenpeace-aktivister-fri-fra-arrest/':('Pressemelding','Klima','','Olje','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2017/Oljeleting-i-Barentshavet-nord-uten-grobunn-i-virkeligheten/':('Pressemelding','Klima','','Olje','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/Tingretten-frifinner-staten/':('Pressemelding','Klima','','Klimasøksmål','Olje','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2017/Program-for-Kulturhuset-under-rettssaken/':('Nyheter','Klima','','Klimasøksmål','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2017/Forste-uke-av-klimarettssaken-oppsummert/':('Nyheter','Klima','','Klimasøksmål','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2018/Ny-oljeleting-i-Barentshavet/':('Pressemelding','Klima','','Olje','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/blogg/Aksjonsblogg-Norsk-oljepolitikk-henger-ikke-pa-greip/':('Nyheter','Klima','','Olje','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2017/Dom-i-klimasoksmal/':('Pressemelding','Klima','','Klimasøksmål','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/reports/Media-Briefing-Lawsuit-2017/':('Nyheter','Klima','','Klimasøksmål','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/blogg/hva-er-iskanten-og-hvorfor-er-den-viktig/blog/51204/':('Nyheter','Klima','','Olje','','','news-list','Migrate'),
            'http://www.greenpeace.org/norway/no/press/releases/Krever-stans-i-ny-oljeboring/':('Pressemelding','Klima','','Olje','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/reports/Media-Briefing-Oil-Drilling-in-the-Barents-Sea/':('Pressemelding','Klima','','Olje','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/blogg/9-ting-du-ikke-visste-om-bjrnya/blog/49329/':('Nyheter','Klima','','Olje','','','news-list','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2016/Klimasoksmal-mottok-pris/':('Nyheter','Klima','','Klimasøksmål','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2018/Staten-sier-nei-til-hoyesterett-/':('Pressemelding','Klima','','Klimasøksmål','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2018/Oljesvart-utdeling-i-omstridt-TFO-ordning/':('Pressemelding','Klima','','Olje','','','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2017/Gi-regnskogen-i-Kongo-en-sjanse/':('Nyheter','Natur','','Skog','Klimaendringer','Biodiversitet','article','Migrate'),
            'http://www.greenpeace.org/norway/no/nyheter/2018/Spikeren-i-kista-for-palmeolje-pa-tanken/':('Nyheter','Natur','','Skog','Klimaendringer','Biodiversitet','article','Migrate'),
             }

        for url,data in start_urls.iteritems():
            p4_post_type, category1, category2, tags1, tags2, tags3, post_type, action = data

            if (post_type == 'article'):
                request = scrapy.Request(url, callback=self.parse_page_type2, dont_filter='true')
            elif (post_type == 'news-list'):
                request = scrapy.Request(url, callback=self.parse_page_type1, dont_filter='true')


            if ( action.lower()=='migrate' ):
                request.meta['status'] = 'publish'
            if ( action.lower()=='archive' ):
                request.meta['status'] = 'draft'
            request.meta['category1'] = category1
            request.meta['category2'] = category2
            request.meta['tags1'] = tags1
            request.meta['tags2'] = tags2
            request.meta['tags3'] = tags3
            request.meta['action'] = action
            request.meta['post_type'] = post_type
            request.meta['p4_post_type'] = p4_post_type
            yield request

        # Migrating authors/thumbnails
        author_usernames = {
            '': 'Greenpeace Norway',
            'tjacobso': 'tjacobso',
            'ylvvethe': 'ylvvethe',
            'tgulowse': 'tgulowse',
            'etellnes': 'etellnes',
            'Therese Jacobson': 'tjacobso',
            'Ylva Vethe': 'ylvvethe',
            'Truls Gulowsen': 'tgulowse',
            'Erlend Tellnes': 'etellnes'
        }

        # Read in the file
        with open( 'gpno_production_v1.xml', 'r' ) as file :
            filedata = file.read()

        # Replace with correct usernames.
        for p3_author_username, p4_author_username in author_usernames.iteritems():
            filedata = filedata.replace('<author_username>' + p3_author_username + '</author_username>', '<author_username>' + p4_author_username + '</author_username>')

        # Remove dir="ltr" attributes from elements as requested.
        filedata = filedata.replace('dir="ltr"', '')

        # Write the file out again
        with open('gpno_production_v1.xml', 'w') as file:
            file.write(filedata)

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

        imagesEnlarge=response.xpath('//div[@class="news-list"]//div[@class="post-content"]//a[@class="open-img EnlargeImage"]/@href').extract()
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
        if date_field:
            date_field = self.filter_month_name(date_field);
            # Filter extra string part from date.
            date_field = date_field.replace(" at", "")  #english
            date_field = date_field.replace(" à", "")
            date_field = date_field.replace(" kl.", "")
            date_field = date_field.replace(" v", "")
            date_field = date_field.replace(" en ", " ") #spanish
            date_field = date_field.replace(" på ", " ") #swedish, norwegian
            date_field = date_field.replace(" di ", " ") #indonesian
            date_field = date_field.replace(" na ", " ") #slovenian

            date_field = dateutil.parser.parse(date_field)

        image_gallery=response.xpath("//*[contains(@class, 'embedded-image-gallery')]")
        p3_image_gallery = 'false'
        if image_gallery:
            p3_image_gallery = 'true'

        body_text = response.css('div.news-list div.post-content').extract_first()
        if body_text:
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.org/').replace('href="/', 'href="http://www.greenpeace.org/')
            body_text = body_text.replace('<span class="btn-open">Zoom</span>', '')

        body_text = self.filter_post_content(body_text)

        images=response.xpath('//img[contains(@style, "float:")]').extract()   #img[@style="margin: 9px; float: left;"]
        imagesD_generated = list()
        for image in images:
            imagesD_generated.append(image)

        blockquotes = response.xpath('//*[@id="content"]//blockquote').extract()
        blockquotes_generated = list()
        for blockquote in blockquotes:
            blockquotes_generated.append(blockquote)

        author_username = response.xpath('string(//div[@class="news-list"]/ul/li/*/*/span[@class="caption"]/span[@class="green1"]/strong)').extract_first()

        if (author_username != 'None'):
            author_username = author_username.strip().replace('av ', '')

        # Get the thumbnail of the post as requested.
        thumbnail = response.xpath('string(head//link[@rel="image_src"]/@href)').extract_first()

        unique_map_id = int(time.time() + random.randint(0, 999))

        # Filter email id image and replace it with email text.
        delete_images = list()
        for image_file in imagesB_generated:
            if ("/emailimages/" in image_file):
                # PHP webservice script url.
                api_url = "http://127.0.0.1/ocr-api-test/email_img_to_text.php"
                end_point_url = api_url + "?url=" + image_file
                emailid = urllib2.urlopen(end_point_url).read(1000)
                # Search replace the \n, <BR>, spaces from email id.
                emailid = emailid.replace('\n', '')
                emailid = emailid.replace('<br />', '') #test
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
        
          
        #list images urls
        for image_file in imagesB_generated:
            if ("/emailimages/" in image_file):
                data = [image_file]
                self.csv_writer(data, "email_images_url_list_sl_story.csv")

        yield {
            'type': response.meta['p4_post_type'],
            'p3_image_gallery': p3_image_gallery,
            'title': extract_with_css('div.news-list h1::text'),
            #'subtitle': '',
            'author': author_username,
            'author_username': author_username,
            'date': date_field,
            #'lead': extract_with_css('div.news-list div.post-content *:first-child strong::text'),
            'lead': response.xpath('string(//div[@class="news-list"]/ul/li/div[@class="post-content"]/div//*[self::p or self::h3 or self::h2][1])').extract()[0],
            'category1': response.meta['category1'],
            'category2': response.meta['category2'],
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
            body_text = body_text.replace('class="btn-open"', '')
            body_text = body_text.replace('Zoom', '')
            body_text = body_text.replace('dir="ltr"', '')
            if lead_text:
                body_text = '<div class="leader">' + lead_text + '</div>' + body_text + response.xpath(' //*[@id="content"]/div[4]/div/div[2]/p').extract_first()

        image_divs=response.xpath('//*[contains(@class, "events-box")]').extract()
        imagesD_generated = list()
        for image_div in image_divs:
            imagesD_generated.append(image_div)

        #subtitle = extract_with_css('div.article h2 span::text')
        #if subtitle:
        #    body_text = '<h2>' + subtitle + '</h2><br />' + body_text

        thumbnail = response.xpath('string(head//link[@rel="image_src"]/@href)').extract_first()

        date_field = response.css('div.article div.text span.author::text').re_first(r' - \s*(.*)')
        try:
            date_field = self.filter_month_name(date_field); 
            # Filter extra string part from date.
            date_field = date_field.replace(" at", "")  #english
            date_field = date_field.replace(" à", "")
            date_field = date_field.replace(" kl.", "")
            date_field = date_field.replace(" v", "")
            date_field = date_field.replace(" en ", " ") #spanish
            date_field = date_field.replace(" på ", " ") #swedish, norwegian
            date_field = date_field.replace(" di ", " ") #indonesian
            date_field = date_field.replace(" na ", " ") #slovenian
        except IndexError:
            date_field = ""

        if date_field:
            date_field = dateutil.parser.parse(date_field)

        # Filter email id image and replace it with email text.
        delete_images = list()
        for image_file in imagesB_generated:
            if ("/emailimages/" in image_file):
                api_url = "http://127.0.0.1/ocr-api-test/email_img_to_text.php"
                end_point_url = api_url+"?url="+image_file
                emailid = urllib2.urlopen(end_point_url).read(1000)
                # Search replace the \n, <BR>, spaces from email id.
                emailid = emailid.replace('\n', '')
                emailid = emailid.replace('<br />', '') #test
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
        
        
        #list images urls
        for image_file in imagesB_generated:
            if ("/emailimages/" in image_file):
                data = [image_file]
                self.csv_writer(data, "email_images_url_list_sl.csv")


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

                data = [response.url, response.meta['p4_post_type'], response.meta['category1'],response.meta['category2'], response.meta['tags1'], response.meta['tags2'], response.meta['tags3'], response.meta['post_type'], response.meta['action']]
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

                            data = [response.url, response.meta['p4_post_type'], response.meta['category1'], response.meta['category2'],
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
            'author': 'Greenpeace Norway',
            'author_username': 'Greenpeace Norway',
            #'date': response.css('#content > div.happen-box.article > div > div.text > span').re_first(r' - \s*(.*)'),
            'date': date_field,
            #'lead': extract_with_css('div.news-list div.post-content *:first-child strong::text'),
            'lead': extract_with_css('#content > div.happen-box.article > div > div.text > div.leader > div'),
            'category1': response.meta['category1'],
            'category2': response.meta['category2'],
            #'text':  response.css('div.news-list div.post-content').extract_first(),
            'text':  body_text,
            'imagesA': imagesA_generated,
            #'imagesB': response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img[not(ancestor::a)]/@src').extract(), #don't import image if there's an a tag around it
            'imagesB': imagesB_generated,
            'imagesC': response.xpath('//div[@class="gallery"]//div[@class="img-nav"]//a/@rel').extract(), # Galleries (horrible html)
            'imagesD': imagesD_generated,
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

        month_no_en = {
            'januar': 'January',
            'februar': 'February',
            'mars': 'March',
            'april': 'April',
            'mai': 'May',
            'juni': 'June',
            'juli': 'July',
            'august': 'August',
            'september': 'September',
            'oktober': 'October',
            'november': 'November',
            'desember': 'December',
        }

        # Replace the Norwegan month name with english month name.
        for no_month, en_month in month_no_en.iteritems():
            month_name = month_name.replace(no_month, en_month)

        return month_name;
    

    def csv_writer(self, data, path):
        # Write data to a CSV file path
        with open(path, "a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(data)
