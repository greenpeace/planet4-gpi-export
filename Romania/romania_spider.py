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
        'FEED_URI': 'gpro_staging_v2.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    __connector_csv_filename = "connector_v1_final.csv"
    __connector_csv_log_file = "connector_csv_log_v1"

    def start_requests(self):

        # V1
        start_urls = {
            'https://www.greenpeace.org/romania/ro/implica-te/Greenpeace-mi-a-completat-o-imagine-careia-ii-simteam-lipsa-cum-de-nu-face-nimeni-nimic/':('Story','Comunitate','','Participare Civică','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/implica-te/idei-eco-practice/':('Story','Comunitate','','Civism','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/publicatii/harta-paduri-virgine/':('Publication','Păduri','','Biodiversitate','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/Activitati/reactie-propunere-lege-paduri-virgine/':('Press Release','Păduri','','Biodiversitate','Activiști pentru Păduri','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/Activitati/dezvoltare-fara-defrisare/':('Story','Păduri','','Activiști pentru Păduri','Tăieri Ilegale','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/Activitati/lansare-harta-paduri-virgine-potentiale/':('Press Release','Păduri','','Biodiversitate','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/Activitati/padurea-si-comunitatea/':('Press Release','Păduri','','Activiști pentru Păduri','Tăieri Ilegale','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/Despre-paduri-in-2018/':('Story','Păduri','','Biodiversitate','Tăieri Ilegale','Activiști pentru Păduri','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/Activitati/padurile-virgine-mostenire-europeana/':('Story','Păduri','','Biodiversitate','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/cum-stopam-distrugerea-padurilor/':('Story','Păduri','','Tăieri Ilegale','Activiști pentru Păduri','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/Activitati/illegal-logging-report-2015/':('Press Release','Păduri','','Tăieri Ilegale','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/publicatii/forest-forum-from-illegal-logging-to-protection-and-responsibility/':('Publication','Păduri','','Tăieri Ilegale','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/publicatii/illegal-logging-2015-report/':('Publication','Păduri','','Tăieri Ilegale','Activiști pentru Păduri','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/publicatii/raport-taieri-ilegale-2015/':('Publication','Păduri','','Tăieri Ilegale','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/solutii/energia-verde-romania/':('Story','Climă şi energie','','Energie Regenerabilă','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/solutii/pozitie-anre-tarif/':('Press Release','Climă şi energie','','Prosumatori','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/publicatii/raport-dark-cloud/':('Publication','Climă şi energie','','Cărbune','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/about/gpromania/raport-de-activitate-greenpeace-2010/':('Publication','Greenpeace','','DespreNoi','','','article','Migrate'),
        }

        #V2
        start_urls = {
            'https://www.greenpeace.org/romania/ro/campanii/paduri/publicatii/harta-paduri-virgine/':('Publication','Păduri','','Biodiversitate','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/Activitati/reactie-propunere-lege-paduri-virgine/':('Press Release','Păduri','','Biodiversitate','Activiști pentru Păduri','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/publicatii/aplicatia-forest-guardians/':('Publication','Păduri','','Păduri virgine','Activiști pentru Păduri','Tăieri Ilegale','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/Activitati/dezvoltare-fara-defrisare/':('Story','Păduri','','Activiști pentru Păduri','Tăieri Ilegale','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/Activitati/lansare-harta-paduri-virgine-potentiale/':('Press Release','Păduri','','Biodiversitate','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/Activitati/padurea-si-comunitatea/':('Press Release','Păduri','','Activiști pentru Păduri','Tăieri Ilegale','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/ghid-identificare-taieri/':('Press Release','Păduri','','Tăieri Ilegale','Activiști pentru Păduri','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/Activitati/sesizari-taieri-valea-sadului/':('Story','Păduri','','Tăieri Ilegale','Activiști pentru Păduri','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/publicatii/Raportul-taierilor-ilegale-din-padurile-Romaniei-2017/':('Publication','Păduri','','Tăieri Ilegale','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/Raportul-taierilor-ilegale-din-padurile-Romaniei-in-2017/':('Publication','Păduri','','Tăieri Ilegale','Activiști pentru Păduri','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/Activitati/Romania-taie-3-hectare-de-padure-pe-ora/':('Press Release','Păduri','','Tăieri Ilegale','Activiști pentru Păduri','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/publicatii/Lectia-din-Pocreaca/':('Publication','Păduri','','Activiști pentru Păduri','Tăieri Ilegale','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/Activitati/taieri-ilegale-2016/':('Press Release','Păduri','','Tăieri Ilegale','Activiști pentru Păduri','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/Activitati/ziua-mondiala-a-padurilor/':('Story','Păduri','','Biodiversitate','Tăieri Ilegale','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/publicatii/raport-taieri-ilegale-2016/':('Publication','Păduri','','Tăieri Ilegale','Activiști pentru Păduri','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/Activitati/Romania-cuts-down-3-hectares-of-forest-per-hour/':('Press Release','Păduri','','Tăieri Ilegale','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/Activitati/map-primary-forests/':('Press Release','Păduri','','Biodiversitate','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/Despre-paduri-in-2018/':('Story','Păduri','','Biodiversitate','Tăieri Ilegale','Activiști pentru Păduri','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/Activitati/padurile-virgine-mostenire-europeana/':('Story','Păduri','','Biodiversitate','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/cum-stopam-distrugerea-padurilor/':('Story','Păduri','','Tăieri Ilegale','Activiști pentru Păduri','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/Activitati/update-harta-padurilor/':('Story','Păduri','','Biodiversitate','Activiști pentru Păduri','Tăieri Ilegale','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/Activitati/protest-camera-deputatilor/':('Press Release','Păduri','','Activiști pentru Păduri','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/Activitati/blocare-taiere-ilegala/':('Press Release','Păduri','','Biodiversitate','Activiști pentru Păduri','Tăieri Ilegale','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/Activitati/ong-se-unesc-impotriva-taierilor-ilegale-din-romania/':('Press Release','Păduri','','Tăieri Ilegale','Activiști pentru Păduri','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/Activitati/O-lume-fr-Greenpeace-Cum-o-corporaie-ne-atac-dreptul-de-a-apra-pdurile/':('Story','Păduri','','Activiști pentru Păduri','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/cum-salvam-padurile-virgine/':('Story','Păduri','','Biodiversitate','Activiști pentru Păduri','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/Activitati/Tierile-ilegale-i-legea-contraveniilor-silvice/':('Story','Păduri','','Tăieri Ilegale','Activiști pentru Păduri','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/Activitati/illegal-logging-report-2015/':('Press Release','Păduri','','Tăieri Ilegale','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/publicatii/forest-forum-from-illegal-logging-to-protection-and-responsibility/':('Publication','Păduri','','Tăieri Ilegale','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/publicatii/illegal-logging-2015-report/':('Publication','Păduri','','Tăieri Ilegale','Activiști pentru Păduri','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/publicatii/raport-taieri-ilegale-2015/':('Publication','Păduri','','Tăieri Ilegale','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/publicatii/Declaraia-Forumului-Pdurilor/':('Publication','Păduri','','Tăieri Ilegale','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/publicatii/ghid-voluntar-paduri/':('Publication','Păduri','','Activiști pentru Păduri','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/publicatii/romanian-forests-vision/':('Publication','Păduri','','Biodiversitate','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/publicatii/viziune-Greenpeace-pentru-padurile-romaniei/':('Publication','Păduri','','Biodiversitate','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/publicatii/harta-pierderii-padurii-3-hectare/':('Publication','Păduri','','Tăieri Ilegale','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/publicatii/Tierile-ilegale-de-arbori-din-Romania-2013-2014/':('Publication','Păduri','','Tăieri Ilegale','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/publicatii/illegal-logging-cases-romania-2012/':('Publication','Păduri','','Tăieri Ilegale','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/publicatii/map-of-deforestation-areas-in-romania-2009-2011/':('Publication','Păduri','','Tăieri Ilegale','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/publicatii/taieri-arbori-2012/':('Publication','Păduri','','Tăieri Ilegale','Activiști pentru Păduri','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/publicatii/Taierile-ilegale-de-arbori-in-padurile-din-Romania-2009-2011/':('Publication','Păduri','','Activiști pentru Păduri','Tăieri Ilegale','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/publicatii/forestcover-change-in-romania-methodology/':('Publication','Păduri','','Biodiversitate','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/activitati/15-lucruri-pe-care-nu-le-stiai-despre-cernobil/':('Story','Climă şi energie','','Nuclear','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/activitati/15-din-28-termocentrale-ilegal/':('Press Release','Climă şi energie','','Cărbune','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/activitati/exista-viata-dupa-carbune/':('Story','Climă şi energie','','Tranziţie Justă','Cărbune','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/activitati/termocentrale-functioneaza-ilegal-ro/':('Press Release','Climă şi energie','','Cărbune','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/poluarea-aerului/praf-de-romania/':('Story','Climă şi energie','','Aer Curat','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/poluarea-aerului/ce-respiram/':('Story','Climă şi energie','','Aer Curat','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/poluarea-aerului/Greenpeace-Romania-lanseaz-Praf-de-Romania/':('Press Release','Climă şi energie','','Aer Curat','','','article','Migrate'),
            # duplicate post
            #'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/poluarea-aerului/praf-de-romania/':('Story','Climă şi energie','','Aer Curat','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/activitati/7-lucruri-pe-care-le-poti-face-pentru-planeta/':('Story','Climă şi energie','','Activism','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/activitati/illegal-coal-romania/':('Press Release','Climă şi energie','','Cărbune','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/activitati/O-victorie-pentru-aerul-curat-in-Europa-in-ciuda-opoziiei-Germaniei-i-a-celorlalte-ri-blocate-in-era-crbunelui/':('Press Release','Climă şi energie','','Aer Curat','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/poluarea-aerului/cand-e-aerul-poluat/':('Story','Climă şi energie','','Aer Curat','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/activitati/alunecare-teren-alunu-valcea/':('Press Release','Climă şi energie','','Cărbune','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/carbunele-energia-trecutului/cifre-socante-despre-arderea-carbunelui/':('Story','Climă şi energie','','Cărbune','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/carbunele-energia-trecutului/victorie-aer-curat/':('Press Release','Climă şi energie','','Cărbune','Aer Curat','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/solutii/energia-solara/':('Story','Climă şi energie','','Energie Regenerabilă','Prosumatori','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/carbunele-energia-trecutului/carbunele-imbolnaveste/':('Press Release','Climă şi energie','','Cărbune','','','article','Migrate'),
            # duplicate post
            #'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/solutii/energia-verde-romania/':('Story','Climă şi energie','','Energie Regenerabilă','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/solutii/pozitie-anre-tarif/':('Press Release','Climă şi energie','','Prosumatori','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/publicatii/raport-dark-cloud/':('Publication','Climă şi energie','','Cărbune','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/publicatii/perspective-globale-pentru-energie-durabila/':('Publication','Climă şi energie','','Energie Regenerabilă','Cărbune','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/publicatii/europa-trebuie-sa-renunte-la-carbune/':('Publication','Climă şi energie','','Cărbune','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/publicatii/energie-regenerabila-pana-in-2020/':('Publication','Climă şi energie','','Energie Regenerabilă','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/publicatii/surse-finantare-2014-2020/':('Publication','Climă şi energie','','Energie Regenerabilă','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/carbunele-energia-trecutului/extinderea-carierelor/Punct-de-vedere-Greenpeace-extinderea-carierei-Roia/':('Publication','Climă şi energie','','Cărbune','Tranziţie Justă','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/carbunele-energia-trecutului/ue-trebuie-sa-impuna-limite-mult-mai-restrictive-pentru-emisiile-poluante-din-arderea-carbunelui/toxicitatea-carbunelui/':('Publication','Climă şi energie','','Cărbune','Aer Curat','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/carbunele-energia-trecutului/grid-report-2030/raportul-power-2030/':('Publication','Climă şi energie','','Energie Regenerabilă','Cărbune','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/carbunele-energia-trecutului/Raport-costurile-ascunse-ale-carbunelui/':('Publication','Climă şi energie','','Cărbune','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/solutii/cum-s-salv-m-clima/Cum-sa-salvam-clima/':('Publication','Climă şi energie','','Activism','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/carbunele-energia-trecutului/turceni-7-ilegal/':('Press Release','Climă şi energie','','Cărbune','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/carbunele-energia-trecutului/protest-greenpeace-impotriva-exproprierilor-abuzive/':('Press Release','Climă şi energie','','Cărbune','Tranziţie Justă','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/solutii/sun-of-sibiu/':('Press Release','Climă şi energie','','Prosumatori','Energie Regenerabilă','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/carbunele-energia-trecutului/raport-costuri-investitii-carbune/':('Press Release','Climă şi energie','','Cărbune','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/solutii/cristi-ene-producator-instalatii/':('Story','Climă şi energie','','Prosumatori','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/solutii/marius-teodorescu-antreprenor/':('Story','Climă şi energie','','Prosumatori','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/solutii/lucian-popescu-prosumator/':('Story','Climă şi energie','','Prosumatori','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/solutii/panouri-solare-scoala-rovinari/':('Press Release','Climă şi energie','','Prosumatori','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/rosiamontana/activitati/cum-a-salvat-societatea-civila-rosia-montana/':('Story','Comunitate','','Participare Civică','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/solutii/instalare-panouri-rovinari/':('Press Release','Climă şi energie','','Energie Regenerabilă','Cărbune','Tranziţie Justă','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/activitati/Activistii-Greenpeace-mesaj-pentru-liderii-europeni-la-Sibiu/':('Press Release','Climă şi energie','','Cărbune','Energie Regenerabilă','Tranziţie Justă','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/activitati/Rainbow-Warrior-vine-in-Romania/':('Press Release','Climă şi energie','','Cărbune','Energie Regenerabilă','Tranziţie Justă','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/activitati/Greenpeace-Romania-militeaza-pentru-tranzitie-justa/':('Press Release','Climă şi energie','','Tranziţie Justă','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/carbunele-energia-trecutului/Esecul-autoritatilor-romane-sesizat-Comisiei-Europene/':('Press Release','Climă şi energie','','Cărbune','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/solutii/Greenpeace-Romania-lanseaza-campania-fii-prosumator/':('Press Release','Climă şi energie','','Prosumatori','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/publicatii/aplicatia-forest-guardians-ios/':('Press Release','Climă şi energie','','Tăieri Ilegale','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/Empowered-Citizens-Resilient-Societies/':('Press Release','Climă şi energie','','Participare Civică','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/Rosia_Montana_este_despre_oameni/':('Press Release','Climă şi energie','','Participare Civică','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/solutii/Uniunea-European-anuleaz-barierele-puse-in-calea-revoluiei-prosumatorilor-/':('Press Release','Climă şi energie','','Prosumatori','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/Greenpeace-Romania-cumpara-Rosia-Montana/':('Press Release','Climă şi energie','','Activism','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/Activitati/Padurile-virgine-au-mai-scapat-de-un-atac/':('Press Release','Climă şi energie','','Păduri virgine','Biodiversitate','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/paduri/Activitati/Pelicam-si-Greenpeace-lanseaza-Sunetele-Padurilor-la-Tulcea/':('Press Release','Climă şi energie','','Păduri virgine','Biodiversitate','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/activitati/subventii-combustibili-fosili/':('Press Release','Climă şi energie','','Cărbune','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/activitati/aer-curat-acum/':('Press Release','Climă şi energie','','Aer Curat','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/schimbari-climatice-energie/solutii/energia-verde-romania/':('Story','Climă şi energie','','Prosumatori','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/Toxic/activitati/poluare-somes/':('Press Release','Comunitate','','Civism','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/Toxic/activitati/6-tari-care-au-interzis-plasticul/':('Story','Comunitate','','Civism','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/Toxic/activitati/somes-probe-august/':('Press Release','Comunitate','','Civism','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/Probleme-locale/Prahova/Greenpeace-solicita-fabricii-Unilever-de-la-Ploiesti-sa-reduca-poluarea/':('Story','Comunitate','','Participare Civică','','','article','Migrate'),
            # Need manual migration.
            ####'https://www.greenpeace.org/romania/ro/campanii/Probleme-locale/Bucuresti-Ilfov/deseuri-aruncate-in-lacul-morii/Deeuri-aruncate-in-lacul-Morii/':('Story','Comunitate','','Participare Civică','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/campanii/Probleme-locale/Cluj/':('Story','Comunitate','','Participare Civică','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/implica-te/8-idei-reducere-plastic/':('Story','Comunitate','','Participare Civică','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/implica-te/Greenpeace-mi-a-completat-o-imagine-careia-ii-simteam-lipsa-cum-de-nu-face-nimeni-nimic/':('Story','Comunitate','','Participare Civică','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/implica-te/idei-eco-practice/Cutie-de-depozitare-pungi-plastic/':('Story','Comunitate','','Civism','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/implica-te/interviu-cu-un-voluntar-greenpeace/':('Story','Comunitate','','Civism','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/implica-te/idei-eco-practice/ornamente-sau-brad-de-craciun-altfel/':('Story','Comunitate','','Civism','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/stiri/eco-gesturi-pentru-protejarea-planetei/deseuri/':('Story','Comunitate','','Civism','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/stiri/eco-gesturi-pentru-protejarea-planetei/apa-si-hrana/':('Story','Comunitate','','Civism','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/stiri/citate-inspira-sa-salvezi-lumea-8-martie/':('Story','Comunitate','','Participare Civică','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/stiri/natura-are-nevoie-de-pace/':('Story','Comunitate','','Civism','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/about/gpromania/raport-de-activitate-greenpeace-2010/':('Publication','Greenpeace','','DespreNoi','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/about/gpromania/Raport-Greenpeace-Romania-2014/':('Publication','Greenpeace','','DespreNoi','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/about/gpromania/raport-activitate-2013/':('Publication','Greenpeace','','DespreNoi','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/about/gpromania/raport-activitate-2012/':('Publication','Greenpeace','','DespreNoi','','','article','Migrate'),
            'https://www.greenpeace.org/romania/ro/about/gpromania/Raport-de-activitate-Greenpeace-Romania-2011/':('Publication','Greenpeace','','DespreNoi','','','article','Migrate'),
            # duplicate post
            #'https://www.greenpeace.org/romania/ro/about/gpromania/raport-de-activitate-greenpeace-2010/':('Publication','Greenpeace','','DespreNoi','','','article','Migrate'),
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
            date_field = date_field.replace(" på ", " ") #swedish
            date_field = date_field.replace(" di ", " ") #indonesian
            date_field = date_field.replace(" na ", " ") #slovenian
            date_field = date_field.replace(" o ", " ")  # polish

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
                if ( Segments[5] ):
                    author_username = Segments[5]
            except IndexError:
                try:  # if ( ( len(Segments) == 4 ) and Segments[4] ):
                    if (Segments[3]):
                        author_username = Segments[3]
                except IndexError:
                    author_username = ''

        author_name = response.xpath('string(//div[@class="news-list"]/ul/li/*/*/span[@class="caption"]/span[@class="green1"]/strong)').extract()[0]
        if ( author_name ):
            author_name = author_name.strip()

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
                emailid = emailid.replace('', '')
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
                self.csv_writer(data, "email_images_url_list.csv")
        """
        # List authors
        #data = [author_name,author_username]
        #self.csv_writer(data, "author_list.csv")

        yield {
            'type': response.meta['p4_post_type'],
            'p3_image_gallery': p3_image_gallery,
            'title': extract_with_css('div.news-list h1::text'),
            #'subtitle': '',
            'author': author_name,
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
            body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)
            if lead_text:
                body_text = '<div class="leader" style="font-weight: bold;margin-bottom: 12px">' + lead_text + '</div>' + body_text + response.xpath(' //*[@id="content"]/div[4]/div/div[2]/p').extract_first()

        subtitle = extract_with_css('div.article h2 span::text')
        if subtitle:
            body_text = '<h2>' + subtitle + '</h2><br />' + body_text

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
            date_field = date_field.replace(" på ", " ") #swedish
            date_field = date_field.replace(" di ", " ") #indonesian
            date_field = date_field.replace(" na ", " ") #slovenian
            date_field = date_field.replace(" o ", " ")  # polish
        except IndexError:
            date_field = ""

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
                emailid = emailid.replace('', '')
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
                self.csv_writer(data, "email_images_url_list.csv")
        
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
            'author': 'Greenpeace Romania',
            'author_username': 'greenpeace',
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

# Filter month name function is not needed for english speaking sites

    def filter_month_name(self, month_name):

        month_ro_en = {
            'ianuarie': 'January',
            'februarie': 'February',
            'martie': 'March',
            'aprilie': 'April',
            'mai': 'May',
            'iunie': 'June',
            'iulie': 'July',
            'august': 'August',
            'septembrie': 'September',
            'octombrie': 'October',
            'noiembrie': 'November',
            'decembrie': 'December',
        }

        # Replace the romanian month name with english month name.
        for ro_month, en_month in month_ro_en.iteritems():
            month_name = month_name.replace(ro_month, en_month)

        return month_name;

    def csv_writer(self, data, path):
        # Write data to a CSV file path
        with open(path, "a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(data)
