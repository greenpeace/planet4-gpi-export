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
        'FEED_URI': 'gpbr_staging_v1.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def start_requests(self):

        #v1
        start_urls = {
            'http://www.greenpeace.org/brasil/pt/Noticias/Desmatamento-A-falta-de-agua-comeca-aqui/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Desmatamento: A falta de água começa aqui'),
            'http://www.greenpeace.org/brasil/pt/Blog/os-corais-da-amaznia-surpreenderam-nossa-expe/blog/58736/':('Blog','Proteja a Natureza','Biodiversidade','','Migrate','Story','Os Corais da Amazônia surpreenderam nossa expectativa e imaginação'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Rio-Doce-1-Ano-de-Lama-e-Luta/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Rio Doce: 1 Ano de Lama e Luta'),
            'http://www.greenpeace.org/brasil/pt/Blog/ambientalistas-pedem-que-mercado-pare-o-desma/blog/60195/':('Blog','Proteja a Natureza','Florestas','','Migrate','Story','Ambientalistas exigem que mercado pare o desmatamento do Cerrado'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Hidreletricas-na-Amazonia-um-mau-negocio-para-o-Brasil-e-para-o-mundo/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Story','Hidrelétricas na Amazônia: um mau negócio para o Brasil e para o mundo'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Lutas-e-vitorias-Munduruku/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Story','Lutas e vitórias Munduruku'),
            'http://www.greenpeace.org/brasil/pt/Noticias/PL-do-Veneno-volta-a-tramitar-na-Camara-e-pode-seguir-para-votacao/':('News','Transforme a Sociedade','Agricultura','Resista','Migrate','Story','Mais agrotóxico no prato: PL do Veneno caminha à passos largos'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Hidreletrica-no-Tapajos-esta-cancelada/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Story','Hidrelétrica no Tapajós está cancelada'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Corais-da-Amazonia-Nosso-tesouro-recem-descoberto-e-ja-ameacado/':('News','Proteja a Natureza','Biodiversidade','','Migrate','Story','Corais da Amazônia: Nosso tesouro recém-descoberto e já ameaçado'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Rio-essa-merenda-nao-parece-legal/':('News','Transforme a Sociedade','Agricultura','Resista','Migrate','Story','Rio, essa merenda não parece legal!'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Ruralistas-tentam-aprovar-PL-que-libera-mais-veneno-na-nossa-comida/':('News','Transforme a Sociedade','Agricultura','Resista','Migrate','Story','Ruralistas tentam aprovar PL que libera mais veneno na nossa comida'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Carne-Fraca-o-modelo-de-producao-e-falho/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Carne Fraca: o modelo de produção é falho'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Segura-este-abacaxi/':('News','Transforme a Sociedade','Agricultura','Resista','Migrate','Story','Segura este abacaxi!'),
            'http://www.greenpeace.org/brasil/pt/Blog/a-extenso-da-tragdia-da-lama-e-da-dor-na-foz-/blog/59597/':('Blog','Transforme a Sociedade','Resista','','Migrate','Story','A extensão da tragédia da lama e da dor na Foz do Rio Doce'),
            'http://www.greenpeace.org/brasil/pt/Noticias/O-misterioso-caso-da-plantacao-de-Ipe/':('News','Proteja a Natureza','Florestas','','Migrate','Story','O misterioso caso da plantação de Ipê'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Esta-no-Congresso-projeto-para-reduzir-uso-de-agrotoxicos/':('News','Transforme a Sociedade','Agricultura','Resista','Migrate','Story','Está no Congresso: projeto para reduzir uso de agrotóxicos'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Mudancas-climaticas-vao-agravar-a-desigualdade-social-no-Brasil/':('News','Transforme a Sociedade','Clima','Energia','Migrate','Story','Mudanças climáticas vão agravar a desigualdade social no Brasil'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Criacao-do-Santuario-de-Baleias-do-Atlantico-Sul-e-negada-mas-nao-desistiremos/':('News','Proteja a Natureza','Biodiversidade','','Migrate','Story','Criação do Santuário de Baleias é negada, mas não desistiremos'),
            #'http://www.greenpeace.org/brasil/Global/brasil/image/2015/Dezembro/2016/Revolu%C3%A7%C3%A3o%20Energ%C3%A9tica%202016.%20Greenpeace%20Brasil.pdf','Documents','Transforme a Sociedade','Clima','Energia','Migrate','Publication','Revolução Energética: Rumo a um Brasil com 100% de energias limpas e renováveis'),
            #'http://www.greenpeace.org/brasil/Global/brasil/documentos/2016/E%20agora,%20Jose%CC%81.%20Resumo.%20Greenpeace%20Brasil.pdf','Documents','Transforme a Sociedade','Clima','Energia','Migrate','Publication','E agora José? O Brasil em tempos de mudanças climáticas'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Comunicado-do-Greenpeace-sobre-o-protesto-nas-Linhas-de-Nazca-no-Peru/':('News','Greenpeace','Institucional','','Migrate','Press Release','Comunicado do Greenpeace sobre o protesto nas Linhas de Nazca, no Peru'),
        }

        """
        start_urls = {
            'http://www.greenpeace.org/brasil/pt/Blog/a-extenso-da-tragdia-da-lama-e-da-dor-na-foz-/blog/59597/': (
            'Blog', 'Transforme a Sociedade', 'Resista', '', 'Migrate', 'Story',
            'A extensão da tragédia da lama e da dor na Foz do Rio Doce'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Esta-no-Congresso-projeto-para-reduzir-uso-de-agrotoxicos/': (
            'News', 'Transforme a Sociedade', 'Agricultura', 'Resista', 'Migrate', 'Story',
            'Está no Congresso: projeto para reduzir uso de agrotóxicos'),
        }
        """

        for url,data in start_urls.iteritems():
            post_type, categories, tags1, tags2, action, p4_post_type, p4_title = data
            if ( post_type=='Blog' ):
                request = scrapy.Request(url, callback=self.parse_blog, dont_filter='true')
            elif ( post_type=='News' ):
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
            request.meta['p4_title'] = p4_title
            yield request

        # Migrating authors/thumbnails
        '''
        author_usernames = {
            'greenpeace': 'Greenpeace P4',
            'Keith Stewart': 'p4_username_keith',
            'Miriam Wilson'
        }

        # Read in the file
        with open( 'gpca_staging_v1.xml', 'r' ) as file :
            filedata = file.read()

        # Replace with correct usernames.
        for p3_author_username, p4_author_username in author_usernames.iteritems():
            filedata = filedata.replace('<author_username>' + p3_author_username, '<author_username>' + p4_author_username)

        # Remove dir="ltr" attributes from elements as requested.
        filedata = filedata.replace('dir="ltr"', '')

        # Write the file out again
        with open('gpca_staging_v1.xml', 'w') as file:
            file.write(filedata)
        '''

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

        imagesEnlarge=response.xpath('//div[@class="news-list"]//div[@class="post-content"]//a[@class="open-img EnlargeImage"]/@href').extract()
        imagesEnlarge_generated = list()
        for image_file in imagesEnlarge:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.org/',1)
            imagesEnlarge_generated.append(image_file)

        pdfFiles=response.css('div.news-list a[href$=".pdf"]::attr(href)').extract()
        pdf_files_generated = list()
        for pdf_file in pdfFiles:
            print pdf_file
            if (pdf_file.startswith('/')):
                pdf_file = pdf_file.replace('/','http://www.greenpeace.org/',1)
                print pdf_file
            pdf_files_generated.append(pdf_file)
            print pdf_files_generated

        date_field = response.css('div.news-list .caption::text').re_first(r' - \s*(.*)')
        date_field = self.filter_month_name(date_field);
        date_field = date_field.replace(" at", "")
        date_field = date_field.replace(" às", "")
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

        # Filter email id image and replace it with email text.
        delete_images = list()
        for image_file in imagesB_generated:
            if ("/emailimages/" in image_file):
                # PHP webservice script url.
                api_url = "http://localhost_test/PHP_webservice/email_img_to_text.php"
                end_point_url = api_url + "?url=" + image_file
                emailid = urllib2.urlopen(end_point_url).read(1000)
                delete_images.append(image_file)
                # Remove the email images from Post body and replace it with email text.
                body_text = re.sub(
                    '<img[a-zA-Z0-9="\s\_]*src=\"' + image_file + '\"[a-zA-Z0-9="\s]*>',
                    emailid, body_text)

        # Remove the email images from list.
        for image_file in delete_images:
            imagesB_generated.remove(image_file)

        """
        #list images urls
        for image_file in imagesB_generated:
            if ("/emailimages/" in image_file):
                data = [image_file]
                self.csv_writer(data, "email_images_url_list_story.csv")
        """

        p4_title = response.meta['p4_title']
        if (p4_title == ""):
            p4_title = extract_with_css('div.news-list h1::text')

        # To fix enlarge Images still leads to p3 issue - find and replace the anchor tag image link with src image link.
        delete_images_en = list()
        for image_file_en in imagesEnlarge_generated:
            for image_file_b in imagesB_generated:
                filename_en = image_file_en.split("/")[-1]
                filename_b  = image_file_b.split("/")[-1]

                if filename_en == filename_b:
                    # print "file names match " + filename_en
                    body_text = body_text.replace(image_file_en, image_file_b)
                    delete_images_en.append(image_file_en)

        # Remove the replaced enlarge images from list.
        for del_image_file_en in delete_images_en:
            imagesEnlarge_generated.remove(del_image_file_en)

        yield {
            'type': response.meta['p4_post_type'],
            'p3_image_gallery': p3_image_gallery,
            'title': p4_title,
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
            'url': response.url,
            'status': response.meta['status'],
            'thumbnail': thumbnail,
        }

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

        lead_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[1]/div/text()').extract()[0]
        body_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[2]').extract()[0]
        if body_text:
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.org/').replace('href="/', 'href="http://www.greenpeace.org/')
            body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)
            if lead_text:
                body_text = '<div class="leader">' + lead_text + '</div>' + body_text + response.xpath(' //*[@id="content"]/div[4]/div/div[2]/p').extract_first()

        body_text = self.filter_post_content(body_text)

        #subtitle = extract_with_css('div.article h2 span::text')
        #if subtitle:
        #    body_text = '<h2>' + subtitle + '</h2><br />' + body_text

        #thumbnail = response.xpath('string(head//link[@rel="image_src"]/@href)').extract_first()

        date_field = response.css('div.article div.text span.author::text').re_first(r' - \s*(.*)')
        date_field = self.filter_month_name(date_field);
        date_field = date_field.replace(" at", "")
        date_field = date_field.replace(" à", "")
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
            'author': 'Greenpeace Brasil',
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
        # Filter the youtube video and add embed shortcode instead.
        post_data = re.sub(
            '\<iframe[width\=\"height0-9\s]*src\=\"([https]*\:\/\/www.youtube.com[a-zA-Z0-9\/\=\-\?\_]*)\"[\=\"a-zA-Z\/\-\s0-9]*\>[\\n\s]*(.*)[\\n\s]*\<\/iframe\>',
            '[embed]\g<1>[/embed]', post_data)

        # Remove the <script> tags from content.
        post_data = re.sub(
            '<script[\s\S]type\=\"text\/javascript\"*?>[\s\S]*?<\/script>',
            '', post_data)

        return post_data

    def filter_month_name(self, month_name):
        month_br_en = {
            'jan': 'January',
            'fev': 'February',
            'mar': 'March',
            'abr': 'April',
            'mai': 'May',
            'jun': 'June',
            'jul': 'July',
            'ago': 'August',
            'set': 'September',
            'out': 'October',
            'nov': 'November',
            'dez': 'December',
        }

        # Replace the Portuguese month name with english month name.
        for br_month, en_month in month_br_en.iteritems():
            month_name = month_name.replace(br_month, en_month)

        return month_name;

    def csv_writer(self, data, path):
        # Write data to a CSV file path
        with open(path, "a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(data)
