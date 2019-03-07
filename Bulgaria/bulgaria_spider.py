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
        'FEED_URI': 'gpbg_staging_v2_B2_bad_posts.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    __connector_csv_filename = "connector_v2_final.csv"
    __connector_csv_log_file = "connector_csv_log_v2"

    def start_requests(self):
        # v2
        start_urls = {
            # B1
            'http://www.greenpeace.org/bulgaria/bg/about_us/Osnovatelite/':('Story','Грийнпийс','','ЗаНас','ВключиСе','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/seas_and_oceans/support-sustainable-fisheries/pozicia-IWC-MOSV-kitove/':('Publication','Природа','','Рибарство','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/seas_and_oceans/support-sustainable-fisheries/declaration-of-the-small-scale-fishermen/':('Publication','Природа','','Рибарство','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/plastics/poziciya-krugova-ikonomika/':('Publication','Свободни от пластмаса','','Пластмаса','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/anti-yadrena-kampaniya/fukushima/bez-vryshtane-doklad/':('Publication','Енергия','','АЕЦ','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/anti-yadrena-kampaniya/qdreni-stres-testove/':('Publication','Енергия','','АЕЦ','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/anti-yadrena-kampaniya/fukushima/yadreni-belezi/':('Publication','Енергия','','АЕЦ','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/anti-yadrena-kampaniya/fukushima/urotsi-ot-fukushima/':('Publication','Енергия','','АЕЦ','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/anti-yadrena-kampaniya/sedmi-blok-aec-kozlodui/stanovishte-na-greenpeace-bulgariq-otnosno-produljavane-na-sroka-na-eksploataciq-na-5-i-6-blok-na-aec-kozlodui/':('Press Release','Енергия','','АЕЦ','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/anti-yadrena-kampaniya/aec-belene/aec-belene-hronologiq/':('Publication','Енергия','','АЕЦ','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/anti-yadrena-kampaniya/yadreni-incidenti/':('Publication','Енергия','','АЕЦ','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/badeshte-bez-vuglishta/poziciya-energiini-pomoshti/':('Publication','Енергия','','Въглища','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/badeshte-bez-vuglishta/Coal-reports-in-English/lifting-EU-dark-cloud/':('Publication','Енергия','','Въглища','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/badeshte-bez-vuglishta/Coal-reports-in-English/Europes-dark-cloud/':('Publication','Енергия','','Въглища','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/badeshte-bez-vuglishta/Coal-reports-in-English/Coal-Water-Report/':('Publication','Енергия','','Въглища','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/badeshte-bez-vuglishta/Coal-reports-in-English/The-Buried-Secrets-of-Coal/':('Publication','Енергия','','Въглища','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/badeshte-bez-vuglishta/Coal-reports-in-English/Coal-Dinosaurs-on-Life-Support/':('Publication','Енергия','','Въглища','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/badeshte-bez-vuglishta/Coal-reports-in-English/Water-for-Life-or-Water-for-Coal/':('Publication','Енергия','','Въглища','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/badeshte-bez-vuglishta/Coal-reports-in-English/the-suffocating-grip-of-coal/':('Publication','Енергия','','Въглища','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/badeshte-bez-vuglishta/dokladi-na-bulgarski-ezik/doklad-ispaniya/':('Publication','Енергия','','Въглища','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/badeshte-bez-vuglishta/dokladi-na-bulgarski-ezik/dimna-zavesa/':('Publication','Енергия','','Въглища','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/badeshte-bez-vuglishta/dokladi-na-bulgarski-ezik/toksichni-vaglishta/':('Publication','Енергия','','Въглища','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/badeshte-bez-vuglishta/dokladi-na-bulgarski-ezik/zarovenite-tayni-na-varglishtata/':('Publication','Енергия','','Въглища','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/badeshte-bez-vuglishta/dokladi-na-bulgarski-ezik/vaglishtni-dinozavri-na-zhivotopoddarzhashti-sistemi/':('Publication','Енергия','','Въглища','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/badeshte-bez-vuglishta/dokladi-na-bulgarski-ezik/voda-za-jivot-ili-voda-za-vuglishta/':('Publication','Енергия','','Въглища','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/badeshte-bez-vuglishta/dokladi-na-bulgarski-ezik/doklad-za-vredata-ot-goreneto-na-vuglishta-vurhy-choveshkoto-zdrave/':('Publication','Енергия','','Въглища','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/Slunchevi-Istorii/Milosh-Bratsigovo/':('Story','Енергия','','СмениЕнергията','ВъзобновяемаЕнергия','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/Slunchevi-Istorii/Bratsigovo-VEI-inovatsia/':('Publication','Енергия','','СмениЕнергията','ВъзобновяемаЕнергия','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/resheniya/':('Publication','Енергия','','ВъзобновяемаЕнергия','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/resheniya/Renewable-energy-myths/myth-1/':('Story','Енергия','','ВъзобновяемаЕнергия','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/resheniya/Renewable-energy-myths/myth-2/':('Story','Енергия','','ВъзобновяемаЕнергия','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/resheniya/Renewable-energy-myths/myth-3/':('Story','Енергия','','ВъзобновяемаЕнергия','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/resheniya/Renewable-energy-myths/myth-4/':('Story','Енергия','','ВъзобновяемаЕнергия','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/resheniya/Renewable-energy-myths/myth-5/':('Story','Енергия','','ВъзобновяемаЕнергия','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/resheniya/Renewable-energy-myths/myth-6/':('Story','Енергия','','ВъзобновяемаЕнергия','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/resheniya/Renewable-energy-myths/myth-7/':('Story','Енергия','','ВъзобновяемаЕнергия','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/resheniya/Renewable-energy-myths/myth-8/':('Story','Енергия','','ВъзобновяемаЕнергия','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/resheniya/Renewable-energy-myths/myth-9/':('Story','Енергия','','ВъзобновяемаЕнергия','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/resheniya/Renewable-energy-myths/myth-10/':('Story','Енергия','','ВъзобновяемаЕнергия','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/resheniya/Renewable-energy-myths/myth-11/':('Story','Енергия','','ВъзобновяемаЕнергия','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/resheniya/Renewable-energy-myths/myth-12/':('Story','Енергия','','ВъзобновяемаЕнергия','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/resheniya/Renewable-energy-myths/myth-13/':('Story','Енергия','','ВъзобновяемаЕнергия','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/resheniya/Renewable-energy-myths/myth-14/':('Story','Енергия','','ВъзобновяемаЕнергия','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/resheniya/Renewable-energy-myths/myth-15/':('Story','Енергия','','ВъзобновяемаЕнергия','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/resheniya/Renewable-energy-myths/Myth-16/':('Story','Енергия','','ВъзобновяемаЕнергия','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/resheniya/Renewable-energy-myths/Myth-17/':('Story','Енергия','','ВъзобновяемаЕнергия','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/resheniya/Renewable-energy-myths/myth-18/':('Story','Енергия','','ВъзобновяемаЕнергия','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/energiya-ot-pokriva/doklad-energiya-ot-pokriva/':('Publication','Енергия','','СмениЕнергията','ВъзобновяемаЕнергия','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/positions/lovtsi-na-mitove/':('Publication','Енергия','','ВъзобновяемаЕнергия','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/positions/poziciya-na-koaliciya-za-klimata/':('Publication','Енергия','','ВъзобновяемаЕнергия','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/positions/pravo_na_dostup_vei/':('Publication','Енергия','','СмениЕнергията','ВъзобновяемаЕнергия','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/positions/Energiini-grajdani/':('Publication','Енергия','','СмениЕнергията','ВъзобновяемаЕнергия','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/solarni-planini/':('Story','Енергия','','СмениЕнергията','ВъзобновяемаЕнергия','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/solarni-planini/interview/':('Story','Енергия','','СмениЕнергията','ВъзобновяемаЕнергия','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/solarni-planini/5-neshta/':('Story','Енергия','','СмениЕнергията','ВъзобновяемаЕнергия','','article','Migrate'),

            # B2
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/energiya_na_budeshteto/':('Publication','Енергия','','ВъзобновяемаЕнергия','Въглища','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/chistota-na-vyzduha/kachestvo-vuzduh/':('Publication','Енергия','','Въглища','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/chistota-na-vyzduha/za-vyzduha-v-bulgaria/':('Publication','Енергия','','Въглища','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/resheniq-ekologichno-zemedelie/ekologichno-proizvodstvo-na-domati/':('Publication','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/resheniq-ekologichno-zemedelie/alternatives-neonics/':('Publication','Природа','','Пчели','Земеделие','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/resheniq-ekologichno-zemedelie/plan-bee/':('Publication','Природа','','Пчели','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/resheniq-ekologichno-zemedelie/pioneri-v-ekologichnoto-zemedelie/':('Publication','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/resheniq-ekologichno-zemedelie/kak-ekologichnite-resheniya-mogat-da-procaftyat/':('Publication','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/resheniq-ekologichno-zemedelie/viziya-ekologichno-zemedelie/':('Publication','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/problemi/pismo/':('Publication','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/problemi/neonikotinoidi-i-riskovete-za-okolnata-sreda-doklad/':('Publication','Природа','','Пчели','Земеделие','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/problemi/Razvenchavane-na-mitovete/':('Publication','Природа','','Пчели','Земеделие','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/problemi/masovite-ubiici-na-pcheli/':('Publication','Природа','','Пчели','Земеделие','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/problemi/novi-tehniki-za-genno-inzhenerstvo/':('Publication','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/problemi/rutinnata-upotreba-na-pestitsidi-v-proizvodstvoto-na-yabalki-v-es/':('Publication','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/problemi/pristrastenostta-na-Evropa-kum-pesticidi/':('Publication','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/problemi/gorchiviyat-privkus/':('Publication','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/problemi/pesticidite-i-nasheto-zdrave-povod-za-narastvashto-bezpokoistvo/':('Publication','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/problemi/doklad-upadakat-na-pchelite/':('Publication','Природа','','Пчели','Земеделие','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/obicham-hranata-si/luskavi-sledi/':('Story','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/obicham-hranata-si/zhitejska-filosofiya/':('Story','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/obicham-hranata-si/neraboteshtata-sistema/':('Publication','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/obicham-hranata-si/da-imash-vsichko/':('Story','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/obicham-hranata-si/golqmo-reshenie/':('Story','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/eu-bans-three-killer-pectisides-a-light-of-hope/blog/45138/':('Story','Природа','','Пчели','Земеделие','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/one-wave/blog/45529/':('Story','Природа','','Рибарство','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/blog/48959/':('Publication','Природа','','Пчели','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/troyanovo/blog/49311/':('Story','Енергия','','Въглища','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/8-/blog/51213/':('Story','Енергия','','Въглища','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/energiyno-nezavisimi-obshtini/blog/51882/':('Story','Енергия','','СмениЕнергията','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/senchestite-zemi-na-fukushima/blog/51898/':('Story','Енергия','','АЕЦ','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/blog/52544/':('Story','Енергия','','СмениЕнергията','ВключиСе','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/blog/53124/':('Story','Енергия','','Въглища','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/blog-ot-dimitar-sabev/blog/55186/':('Story','Енергия','','Въглища','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/pismo-ot-izpalnitelniya-direktor-na-greenpeace-kumi-naidoo/blog/55184/':('Story','Грийнпийс','','ВключиСе','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/5-prosti-nachina-da-pomognesh-na-okeana/blog/55334/':('Story','Свободни от пластмаса','','Пластмаса','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/blog/55473/':('Story','Свободни от пластмаса','','Пластмаса','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/-/blog/55577/':('Story','Свободни от пластмаса','','Пластмаса','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/blog/55718/':('Story','Природа','','Земеделие','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/Fermeri-Fukushima/blog/55851/':('Story','Енергия','','АЕЦ','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/Fukushima-i-Chernobil/blog/55852/':('Story','Енергия','','АЕЦ','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/voenni-bazi-v-Okinava/blog/55853/':('Story','Грийнпийс','','ВключиСе','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/Chernobil-hrana-i-vyzduh/blog/56088/':('Story','Енергия','','АЕЦ','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/15-neshta-koito-ne-znaete-za-chernobil/blog/56186/':('Story','Енергия','','АЕЦ','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/5-prichini-za-zabrana-na-vyglishtata/blog/56281/':('Story','Енергия','','Въглища','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/Fukushima-i-Chernobil-osveteni/blog/56309/':('Story','Енергия','','АЕЦ','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/gorski-pozhari-Chernobil/blog/56310/':('Story','Енергия','','АЕЦ','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/Francia-ban-neonikotinoidi/blog/56441/':('Press Release','Природа','','Земеделие','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/Hiroshima-Nagasaki-never-again/blog/56607/':('Story','Енергия','','АЕЦ','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/masovite-ubiici-na-pchelite/blog/56734/':('Story','Природа','','Пчели','Земеделие','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/v-yabulkovata-gradina/blog/56741/':('Story','Природа','','Земеделие','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/iPES-Food-doklad/blog/56844/':('Story','Природа','','Земеделие','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/hranitelna-sigurnost/blog/56928/':('Story','Природа','','Земеделие','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/tatkova-gradina/blog/57064/':('Story','Природа','','Земеделие','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/Franciq-zakon-oprashiteli/blog/57088/':('Press Release','Природа','','Пчели','Земеделие','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/microplastic-blog/blog/57136/':('Story','Свободни от пластмаса','','Пластмаса','','','news-list','Migrate'),

            # B3
            'http://www.greenpeace.org/bulgaria/bg/blog/blog/57208/':('Story','Енергия','','АЕЦ','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/zabrani-plastmasa/blog/57326/':('Story','Свободни от пластмаса','','Пластмаса','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/da-bydesh-voin-na-dygata/blog/57482/':('Story','Грийнпийс','','ВключиСе','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/we-will-move-ahead/blog/58104/':('Story','Енергия','','Въглища','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/bio-ferma-Sofina/blog/58132/':('Story','Природа','','Земеделие','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/obeshtaniya-za-2017/blog/58381/':('Story','Грийнпийс','','ВключиСе','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/tri-prichini-za-poveche-morski-rezervati/blog/57421/':('Story','Природа','','Рибарство','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/neonikotinoidite-seriozna-zaplaha/blog/58470/':('Story','Природа','','Пчели','Земеделие','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/Vsqka-proizvedena-plastmasa/blog/58561/':('Story','Свободни от пластмаса','','Пластмаса','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/sushilnya-za-furazh/blog/59095/':('Story','Природа','','Земеделие','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/farmerasmus-fermeri-v-bulgaria/blog/59092/':('Story','Природа','','Земеделие','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/belgiiski-i-bulgarski-fermeri-vuv-franciya/blog/59096/':('Story','Природа','','Земеделие','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/romania-live-long-and-protest/blog/58764/':('Story','Грийнпийс','','ВключиСе','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/farmerasmus/blog/59094/':('Story','Природа','','Земеделие','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/blog/58907/':('Story','Енергия','','СмениЕнергията','ВъзобновяемаЕнергия','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/shtastlivi-kravi/blog/58929/':('Story','Природа','','Земеделие','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/blog/59005/':('Story','Свободни от пластмаса','','Пластмаса','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/5/blog/59006/':('Story','Енергия','','СмениЕнергията','ВъзобновяемаЕнергия','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/blog/59007/':('Story','Свободни от пластмаса','','Пластмаса','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/kak-golemo-selo-osydi-bulgaria/blog/59090/':('Story','Енергия','','Въглища','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/blog/59102/':('Press Release','Природа','','Земеделие','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/blog/59117/':('Story','Свободни от пластмаса','','Пластмаса','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/blog/59130/':('Story','Грийнпийс','','ВключиСе','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/blog/59131/':('Story','Енергия','','СмениЕнергията','ВъзобновяемаЕнергия','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/blog/59157/':('Story','Енергия','','Въглища','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/blog/59163/':('Story','Грийнпийс','','ВключиСе','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/blog/59224/':('Story','Енергия','','Въглища','СмениЕнергията','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/bref/blog/59241/':('Story','Енергия','','Въглища','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/bref/blog/59295/':('Story','Енергия','','Въглища','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/blog/59467/':('Story','Свободни от пластмаса','','Пластмаса','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/-/blog/59468/':('Story','Свободни от пластмаса','','Пластмаса','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/dont-bottle-it/blog/59469/':('Story','Свободни от пластмаса','','Пластмаса','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/mina-pernik/blog/59502/':('Story','Енергия','','Въглища','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/depozitivno/blog/59561/':('Story','Свободни от пластмаса','','Пластмаса','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/poslednata-slamka/blog/59562/':('Story','Свободни от пластмаса','','Пластмаса','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/kafe/blog/59563/':('Story','Свободни от пластмаса','','Пластмаса','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/energijni-grazhdani/blog/59579/':('Story','Енергия','','СмениЕнергията','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/blog-doklad-ispania/blog/59712/':('Story','Енергия','','Въглища','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/UN-nuclear-treaty/blog/59902/':('Story','Енергия','','АЕЦ','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/solar/blog/59785/':('Story','Енергия','','СмениЕнергията','Въглища','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/blog/60128/':('Story','Свободни от пластмаса','','Пластмаса','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/blog-vyzobnovyaema-energiya/blog/60430/':('Story','Енергия','','ВъзобновяемаЕнергия','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/2025/blog/60690/':('Story','Енергия','','Въглища','ВъзобновяемаЕнергия','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/21-/blog/60917/':('Story','Енергия','','СмениЕнергията','ВъзобновяемаЕнергия','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/plastic/blog/60936/':('Story','Свободни от пластмаса','','Пластмаса','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/predpazvane-mrasen-vazduh/blog/61102/':('Story','Енергия','','Въглища','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/blog/61146/':('Story','Грийнпийс','','ВключиСе','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/studen_rezerv_delo/blog/61186/':('Story','Енергия','','Въглища','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/jivot-bez-otpadutsi/blog/61257/':('Story','Свободни от пластмаса','','Пластмаса','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/plavasht_Chernobyl_Lomonosov/blog/61436/':('Story','Енергия','','АЕЦ','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/milioni-domashni-tsentrali/blog/61492/':('Story','Енергия','','ВъзобновяемаЕнергия','ВключиСе','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/Toplofikatsiya_Pernik_Globa/blog/61587/':('Story','Енергия','','Въглища','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/nejna_promyana/blog/61722/':('Story','Общности','','ВключиСе','Въглища','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/VEI-Revolutsiyata-Produljava/blog/61812/':('Story','Енергия','','ВъзобновяемаЕнергия','СмениЕнергията','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/stanovishte-nacionalen-plan-biomasa-2018-2017/':('Press Release','Енергия','','СмениЕнергията','ВъзобновяемаЕнергия','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/finansovite-mini-doklad/':('Press Release','Енергия','','Въглища','','','article','Migrate'),

            # B4
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/zamarsyavane_cherno_more/':('Press Release','Свободни от пластмаса','','Пластмаса','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/Toplofikatsiya_Sliven_Razreshitelno/':('Press Release','Енергия','','Въглища','Пластмаса','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/pismo_plastmasa_MOSV/':('Press Release','Свободни от пластмаса','','Пластмаса','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/EP_studen_rezerv/':('Press Release','Енергия','','Въглища','ВъзобновяемаЕнергия','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/otgovor_trud_sliven/':('Press Release','Енергия','','Въглища','ЗаНас','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/Predizvikatelstvo_Snimki_Energiya/':('Press Release','Енергия','','ВъзобновяемаЕнергия','ВключиСе','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/8-mart-2018/':('Press Release','Грийнпийс','','ЗаНас','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/Brikel_moshtnosti_otkaz/':('Press Release','Енергия','','Въглища','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/den-na-vodata-2018/':('Press Release','Свободни от пластмаса','','Пластмаса','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/fossil-fuel-subsidies-awards/':('Press Release','Енергия','','Въглища','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/izgaryane-otpadutsi-Sliven/':('Press Release','Енергия','','Въглища','Пластмаса','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/Fossil-Fuel-Subsidies-Awards-Winners/':('Press Release','Енергия','','Въглища','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/activists-sun-banner-ndk-vei/':('Press Release','Енергия','','ВъзобновяемаЕнергия','СмениЕнергията','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/Fest_Stara_Zagora/':('Press Release','Енергия','','ВъзобновяемаЕнергия','ВключиСе','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/7-rojden-den/':('Press Release','Грийнпийс','','ЗаНас','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/Slunchev_Festival_Pernik_2018/':('Press Release','Енергия','','Въглища','ВъзобновяемаЕнергия','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/projektsiya_BobovDol/':('Press Release','Енергия','','Въглища','ВъзобновяемаЕнергия','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/restart_AEC_Belene_pozitsiya/':('Press Release','Енергия','','АЕЦ','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/EC_plastic_ban/':('Press Release','Свободни от пластмаса','','Пластмаса','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/tec-zamursyavane-zdrave-ikonomika/':('Press Release','Енергия','','Въглища','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/demonstratsiya_VEI_Luxembourg/':('Press Release','Енергия','','ВъзобновяемаЕнергия','Въглища','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/EU_Renewable_Energy_Directive/':('Press Release','Енергия','','СмениЕнергията','ВъзобновяемаЕнергия','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/Pozitsiya_Sukrateni_Minyori/':('Press Release','Енергия','','Въглища','ВъзобновяемаЕнергия','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/Aktivni_Hora_Pernik/':('Press Release','Общности','','ВключиСе','Въглища','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/25-metra-riba-Burgas/':('Press Release','Свободни от пластмаса','','Пластмаса','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/promeni-APK/':('Press Release','Грийнпийс','','ЗаНас','ВключиСе','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/APK-iskane-veto/':('Press Release','Грийнпийс','','ЗаНас','ВключиСе','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/objalvane-reshenie-brikel-otpaduci/':('Press Release','Енергия','','Въглища','Пластмаса','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/Nova-Mina-Aldomirovtsi-Kontsesiya/':('Press Release','Енергия','','Въглища','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/BobovDol-Otpaduci-Izgaryane/':('Press Release','Енергия','','Въглища','Пластмаса','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/Maritza-Iztok-Derogatsii/':('Press Release','Енергия','','Въглища','ВъзобновяемаЕнергия','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/Republika-Pernik-Oobovdol-Otpaduci-Izgaryane/':('Press Release','Енергия','','Въглища','Пластмаса','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/miliardi-studen-rezerv/':('Press Release','Енергия','','Въглища','ВъзобновяемаЕнергия','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/Slunchev-Festival-Golemo-Selo-2018/':('Press Release','Енергия','','Въглища','ВъзобновяемаЕнергия','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/demonstratsiya-avstriya-studen-rezerv/':('Press Release','Енергия','','Въглища','ВъзобновяемаЕнергия','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/tec-sliven-pojar/':('Press Release','Енергия','','Въглища','Пластмаса','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/APK-promeni-objalvane/':('Press Release','Грийнпийс','','ЗаНас','ВключиСе','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/sol-plastmasa-zamursyavane-izsledvane/':('Press Release','Свободни от пластмаса','','Пластмаса','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/bobov-dol-narushenie-izgaryane-zdrave/':('Press Release','Енергия','','Въглища','Пластмаса','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/25-metra-riba-Sofia/':('Press Release','Свободни от пластмаса','','Пластмаса','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/tec-zamursyavane-analiz-norma-dostup/':('Press Release','Енергия','','Въглища','ВключиСе','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/koncert-dishai-pernik-chist-vuzduh/':('Press Release','Общности','','ВключиСе','Въглища','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/BEH-zamursyavane-vuzduh-zdrave/':('Press Release','Енергия','','Въглища','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/projektsiya-BobovDol-otpaduci-gorene/':('Press Release','Енергия','','Въглища','ВключиСе','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2018/solarni-lampi-Golemo-selo/':('Press Release','Енергия','','ВъзобновяемаЕнергия','Въглища','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2019/Derogatsiya-Maritza-Iztok-2/':('Press Release','Енергия','','Въглища','ВъзобновяемаЕнергия','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2019/Germaniya-Otkaz-Vuglishta/':('Press Release','Енергия','','Въглища','ВъзобновяемаЕнергия','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/novini/2019/Solarna-Laboratoriya-Bobov-Dol/':('Press Release','Енергия','','ВъзобновяемаЕнергия','Въглища','','article','Migrate'),
        }

        start_urls = {
            # B2
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/vazobnovyaema-energiya/energiya_na_budeshteto/':('Publication','Енергия','','ВъзобновяемаЕнергия','Въглища','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/chistota-na-vyzduha/kachestvo-vuzduh/':('Publication','Енергия','','Въглища','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/climate_change/chistota-na-vyzduha/za-vyzduha-v-bulgaria/':('Publication','Енергия','','Въглища','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/resheniq-ekologichno-zemedelie/ekologichno-proizvodstvo-na-domati/':('Publication','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/resheniq-ekologichno-zemedelie/alternatives-neonics/':('Publication','Природа','','Пчели','Земеделие','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/resheniq-ekologichno-zemedelie/plan-bee/':('Publication','Природа','','Пчели','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/resheniq-ekologichno-zemedelie/pioneri-v-ekologichnoto-zemedelie/':('Publication','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/resheniq-ekologichno-zemedelie/kak-ekologichnite-resheniya-mogat-da-procaftyat/':('Publication','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/resheniq-ekologichno-zemedelie/viziya-ekologichno-zemedelie/':('Publication','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/problemi/pismo/':('Publication','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/problemi/neonikotinoidi-i-riskovete-za-okolnata-sreda-doklad/':('Publication','Природа','','Пчели','Земеделие','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/problemi/Razvenchavane-na-mitovete/':('Publication','Природа','','Пчели','Земеделие','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/problemi/masovite-ubiici-na-pcheli/':('Publication','Природа','','Пчели','Земеделие','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/problemi/novi-tehniki-za-genno-inzhenerstvo/':('Publication','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/problemi/rutinnata-upotreba-na-pestitsidi-v-proizvodstvoto-na-yabalki-v-es/':('Publication','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/problemi/pristrastenostta-na-Evropa-kum-pesticidi/':('Publication','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/problemi/gorchiviyat-privkus/':('Publication','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/problemi/pesticidite-i-nasheto-zdrave-povod-za-narastvashto-bezpokoistvo/':('Publication','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/problemi/doklad-upadakat-na-pchelite/':('Publication','Природа','','Пчели','Земеделие','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/obicham-hranata-si/luskavi-sledi/':('Story','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/obicham-hranata-si/zhitejska-filosofiya/':('Story','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/obicham-hranata-si/neraboteshtata-sistema/':('Publication','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/obicham-hranata-si/da-imash-vsichko/':('Story','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/campaigns/agriculture/obicham-hranata-si/golqmo-reshenie/':('Story','Природа','','Земеделие','','','article','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/eu-bans-three-killer-pectisides-a-light-of-hope/blog/45138/':('Story','Природа','','Пчели','Земеделие','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/one-wave/blog/45529/':('Story','Природа','','Рибарство','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/blog/48959/':('Publication','Природа','','Пчели','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/troyanovo/blog/49311/':('Story','Енергия','','Въглища','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/8-/blog/51213/':('Story','Енергия','','Въглища','','','news-list','Migrate'),
            #### 'http://www.greenpeace.org/bulgaria/bg/blog/energiyno-nezavisimi-obshtini/blog/51882/':('Story','Енергия','','СмениЕнергията','','','news-list','Migrate'),
            #### 'http://www.greenpeace.org/bulgaria/bg/blog/senchestite-zemi-na-fukushima/blog/51898/':('Story','Енергия','','АЕЦ','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/blog/52544/':('Story','Енергия','','СмениЕнергията','ВключиСе','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/blog/53124/':('Story','Енергия','','Въглища','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/blog-ot-dimitar-sabev/blog/55186/':('Story','Енергия','','Въглища','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/pismo-ot-izpalnitelniya-direktor-na-greenpeace-kumi-naidoo/blog/55184/':('Story','Грийнпийс','','ВключиСе','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/5-prosti-nachina-da-pomognesh-na-okeana/blog/55334/':('Story','Свободни от пластмаса','','Пластмаса','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/blog/55473/':('Story','Свободни от пластмаса','','Пластмаса','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/-/blog/55577/':('Story','Свободни от пластмаса','','Пластмаса','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/blog/55718/':('Story','Природа','','Земеделие','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/Fermeri-Fukushima/blog/55851/':('Story','Енергия','','АЕЦ','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/Fukushima-i-Chernobil/blog/55852/':('Story','Енергия','','АЕЦ','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/voenni-bazi-v-Okinava/blog/55853/':('Story','Грийнпийс','','ВключиСе','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/Chernobil-hrana-i-vyzduh/blog/56088/':('Story','Енергия','','АЕЦ','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/15-neshta-koito-ne-znaete-za-chernobil/blog/56186/':('Story','Енергия','','АЕЦ','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/5-prichini-za-zabrana-na-vyglishtata/blog/56281/':('Story','Енергия','','Въглища','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/Fukushima-i-Chernobil-osveteni/blog/56309/':('Story','Енергия','','АЕЦ','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/gorski-pozhari-Chernobil/blog/56310/':('Story','Енергия','','АЕЦ','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/Francia-ban-neonikotinoidi/blog/56441/':('Press Release','Природа','','Земеделие','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/Hiroshima-Nagasaki-never-again/blog/56607/':('Story','Енергия','','АЕЦ','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/masovite-ubiici-na-pchelite/blog/56734/':('Story','Природа','','Пчели','Земеделие','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/v-yabulkovata-gradina/blog/56741/':('Story','Природа','','Земеделие','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/iPES-Food-doklad/blog/56844/':('Story','Природа','','Земеделие','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/hranitelna-sigurnost/blog/56928/':('Story','Природа','','Земеделие','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/tatkova-gradina/blog/57064/':('Story','Природа','','Земеделие','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/Franciq-zakon-oprashiteli/blog/57088/':('Press Release','Природа','','Пчели','Земеделие','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/microplastic-blog/blog/57136/':('Story','Свободни от пластмаса','','Пластмаса','','','news-list','Migrate'),
        }

        start_urls = {
            'http://www.greenpeace.org/bulgaria/bg/blog/energiyno-nezavisimi-obshtini/blog/51882/':('Story','Енергия','','СмениЕнергията','','','news-list','Migrate'),
            'http://www.greenpeace.org/bulgaria/bg/blog/senchestite-zemi-na-fukushima/blog/51898/':('Story','Енергия','','АЕЦ','','','news-list','Migrate'),
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

        author_username = response.xpath('string(//div[@class="news-list"]/ul/li/*/*/span[@class="caption"]/strong/span[@class="green1"]/a/@href)').extract_first()

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

        author_name = response.xpath('string(//div[@class="news-list"]/ul/li/*/*/span[@class="caption"]/strong/span[@class="green1"])').extract()[0]
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
                emailid = emailid.replace(' ', '')
                delete_images.append(image_file)
                # Remove the email images from Post body and replace it with email text.
                body_text = re.sub(
                    '<img[a-zA-Z0-9="\s\_]*src=\"' + image_file + '\"[a-zA-Z0-9="\s]*>',
                    '<a href="mailto:' + emailid.strip() + '" target="_blank">' + emailid.strip() + '</a>', body_text)

        # Remove the email images from list.
        for image_file in delete_images:
            imagesB_generated.remove(image_file)

        '''
        #list images urls
        for image_file in imagesB_generated:
            if ("/emailimages/" in image_file):
                data = [image_file]
                self.csv_writer(data, "email_images_url_list_fr_story.csv")
        '''

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
                body_text = '<div class="leader">' + lead_text + '</div>' + body_text + response.xpath(' //*[@id="content"]/div[4]/div/div[2]/p').extract_first()

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
                emailid = emailid.replace(' ', '')
                delete_images.append(image_file)
                # Remove the email images from Post body and replace it with email text.
                body_text = re.sub(
                    '<img[a-zA-Z0-9="\s\_]*src=\"'+image_file+'\"[a-zA-Z0-9="\s]*>',
                    '<a href="mailto:' + emailid.strip() + '" target="_blank">' + emailid.strip() + '</a>', body_text)

        # Remove the email images from list.
        for image_file in delete_images:
            imagesB_generated.remove(image_file)

        '''
        #list images urls
        for image_file in imagesB_generated:
            if ("/emailimages/" in image_file):
                data = [image_file]
                self.csv_writer(data, "email_images_url_list_fr.csv")
        '''


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
            'author': 'Greenpeace Bulgaria',
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

    def filter_month_name(self, month_name):

        month_bg_en = {
            'януари': 'January',
            'февруари': 'February',
            'март': 'March',
            'април': 'April',
            'май': 'May',
            'юни': 'June',
            'юли': 'July',
            'август': 'August',
            'септември': 'September',
            'октомври': 'October',
            'ноември': 'November',
            'декември': 'December',
        }

        # Replace the Bulgarian month name with english month name.
        for bg_month, en_month in month_bg_en.iteritems():
            month_name = month_name.replace(bg_month, en_month)

        return month_name;

    def csv_writer(self, data, path):
        # Write data to a CSV file path
        with open(path, "a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(data)
