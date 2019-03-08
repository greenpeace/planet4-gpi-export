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
        'FEED_URI': 'gpsl_staging_v2.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    __connector_csv_filename = "connector_v2_final.csv"
    __connector_csv_log_file = "connector_csv_log_v2"

    def start_requests(self):
        # v2
        start_urls = {
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/skupna-izjava-zahteve-glede-sporazumov-ceta-i/blog/56431/':('Blog','O nas','','Greenpeace','','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/medtem-ko-politiki-odloajo-o-nai-energetski-p/blog/50850/':('Blog','Podnebje','','Podnebje','','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/vesel-svetovni-dan-antarktike/blog/60804/':('Blog','Narava','','Oceani','Antarktika','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/5-stvari-ki-jih-verjetno-niste-vedeli-o-antar/blog/60983/':('Blog','Narava','','Oceani','Antarktika','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/najbolji-pingvin-antarktike/blog/61028/':('Blog','Narava','','Oceani','Antarktika','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/potopitev-na-dno-antarktinega-oceana-je-izpol/blog/61098/':('Blog','Narava','','Oceani','Antarktika','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/za-valentinovo-najbolj-ljubee-ivali-antarktik/blog/61145/':('Blog','Narava','','Oceani','Antarktika','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/onesnaenje-s-plastiko-doseglo-antarktiko/blog/61601/':('Blog','Narava','','Oceani','Antarktika','Plastika','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/kaj-podnebne-spremembe-pomenijo-za-antarktiko/blog/61962/':('Blog','Narava','','Oceani','Podnebje','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/break-free-osvobodimo-se-umazane-energije/blog/58860/':('Blog','Podnebje','','BrezPremoga','BreakFree','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/poroilo-nevarne-kemikalije-najdene-v-opremi-z/blog/55377/':('Blog','Prekomerna potrošnja','','Detox','DetoxOutdoor','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/patagonska-odprava-na-vrh-cerro-torreja-brez-/blog/55296/':('Blog','Prekomerna potrošnja','','Detox','DetoxOutdoor','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/nobelova-nagrada-za-mir-podeljena-mednarodni-/blog/60427/':('Blog','Podnebje','','jedrska','','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/s-soncem-proti-energetski-revini/blog/60322/':('Blog','Podnebje','','EnergetskeSkupnosti','Sonce','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/energetska-politika-v-igavo-korist/blog/54332/':('Blog','Podnebje','','EnergetskeSkupnosti','','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/energija-okoli-nas-ali-kaj-imajo-skupnega-kav/blog/42398/':('Blog','Podnebje','','BrezPremoga','sonce','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/sadnja-dreves-ob-mednarodnem-dnevu-gozdov/blog/52393/':('Blog','Narava','','Gozdovi','Prostovoljstvo','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/gozdna-zaitna-postaja-v-romunskih-karpatih/blog/57623/':('Blog','Narava','','Gozdovi','Prostovoljstvo','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/pogozdovanje-na-hrvakem-boranka/blog/61918/':('Blog','Narava','','Gozdovi','Prostovoljstvo','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/naftni-otoki-jadrana/blog/52435/':('Blog','Narava','','Oceani','jadran','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/plastika-ne-onesnauje-zgolj-naih-oceanov-spro/blog/61950/':('Blog','Prekomerna potrošnja','','Plastika','Podnebje','UmazaniPosli','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/kaj-se-dogaja-z-izpusti-toplogrednih-plinov-v/blog/58368/':('Blog','Podnebje','','Podnebje','','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/pogum-podnebnega-upanja/blog/61941/':('Blog','Podnebje','','IPCC','PodnebnePosledice','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/hranjenje-ivali-ali-nas-samih/blog/51257/':('Blog','Prekomerna potrošnja','','Prehrana','','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/brez-pravne-drave-ni-zdravega-okolja/blog/43492/':('Blog','O nas','','Greenpeace','','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/dan-za-spremembe-dan-za-spotovanje/blog/56048/':('Blog','O nas','','Greenpeace','Prostovoljstvo','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/vege-sarmice-po-receptu-mame-stefke/blog/62070/':('Blog','Prekomerna potrošnja','','Prehrana','Greenpeace','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/vsakdo-ima-pravico-do-zdravega-okolja-pa-jo-i/blog/45635/':('Blog','Podnebje','','BrezPremoga','TEŠ','UmazaniPosli','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/ladijski-dnevnik-pred-odhodom-442015/blog/52510/':('Blog','O nas','','Oceani','Prostovoljstvo','arktika','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/ladijski-dnevnik-pot-in-prvi-dnevi-1242015/blog/52585/':('Blog','O nas','','Oceani','Prostovoljstvo','arktika','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/ladijski-dnevnik-prve-aktivnosti-19-4-2015/blog/52639/':('Blog','O nas','','Oceani','Prostovoljstvo','arktika','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/ladijski-dnevnik-e-dobro-uteeni-26-4-2015/blog/52710/':('Blog','O nas','','Oceani','Prostovoljstvo','arktika','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/ladijski-dnevnik-naravnost-proti-avstriji-3-5/blog/52790/':('Blog','O nas','','Oceani','Prostovoljstvo','arktika','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/ladijski-dnevnik-vi-odhod-je-e-v-zraku-10-5-2/blog/52851/':('Blog','O nas','','Oceani','Prostovoljstvo','arktika','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/print-green-slv-tiskaj-zeleno/blog/51532/':('Blog','O nas','','Greenpeace','Prostovoljstvo','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/mali-naravovarstveniki/blog/52198/':('Blog','O nas','','Greenpeace','Prostovoljstvo','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/za-spremembe-zemljo-in-abice/blog/52472/':('Blog','O nas','','Greenpeace','Prostovoljstvo','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/art-kamp-2015/blog/53454/':('Blog','O nas','','Prostovoljstvo','Jadran','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/mednarodni-dan-prostovoljstva-5-december/blog/54992/':('Blog','O nas','','Greenpeace','Prostovoljstvo','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/biti-ali-ne-biti-kritini-to-je-zdaj-vpraanje/blog/55364/':('Blog','O nas','','Greenpeace','Prostovoljstvo','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/motivacijsko-izobraevalni-vikend-s-prostovolj/blog/56374/':('Blog','O nas','','Greenpeace','Prostovoljstvo','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/motivacijsko-izobraevalni-vikend-za-prostovol/blog/58525/':('Blog','O nas','','Greenpeace','Prostovoljstvo','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/gradovi-kralja-matjaa/blog/52036/':('Blog','O nas','','Oceani','Prostovoljstvo','arktika','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/biti-prostovoljec/blog/45042/':('Blog','O nas','','Greenpeace','Prostovoljstvo','TrajnostnoRibištvo','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/dr-dejan-savi-fosilna-goriva-bo-treba-prepove/blog/59391/':('Blog','Podnebje','','BrezPremoga','TEŠ','EnergetskeSkupnosti','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/greenpeaceove-ladje-plujejo-v-spopad-s-plasti/blog/62126/':('Blog','Prekomerna potrošnja','','Plastika','UmazaniPosli','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Poleg-uvoza-premoga-e-ve-javnega-denarja-za-TE/':('Sporočilo za javnost','Podnebje','','BrezPremoga','TEŠ','UmazaniPosli','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Nemija-nartuje-konec-premoga/':('Sporočilo za javnost','Podnebje','','BrezPremoga','TEŠ ','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Koncno-Sosedske-soncne-elektrarne-tudi-v-Sloveniji/':('Sporočilo za javnost','Podnebje','','EnergetskeSkupnosti','sonce','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Nova-pravila-EU-omogoajo-milijardne-subvencije-za-fosilna-goriva-in-jedrsko-energijo/':('Sporočilo za javnost','Podnebje','','BrezPremoga','TEŠ','UmazaniPosli','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Zakljuek-podnebne-konference-COP24/':('Sporočilo za javnost','Podnebje','','Podnebje','IPCC','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Podnebni-pogajalci--kaj-pa-poari/':('Sporočilo za javnost','Narava','','Gozdovi ','PodnebnePosledice','Podnebje','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Komisija-za-Antarktini-ocean-ni-uspela-izpolniti-svojega-mandata-glede-zaite-antarktinih-voda/':('Sporočilo za javnost','Narava','','Oceani','Antarktika','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/PODNEBNI-ZNANSTVENIKI-STREZNILI-POLITIKE-/':('Sporočilo za javnost','Podnebje','','BrezPremoga','IPCC','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/RAZKRITO-58-milijard-EUR-prikritih-subvencij-za-premog-zemeljski-plin-in-jedrsko-energijo/':('Sporočilo za javnost','Podnebje','','BrezPremoga','TEŠ','UmazaniPosli','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Vlada-zopet-pozabila-na-prebivalce-blokovskih-naselij/':('Sporočilo za javnost','Podnebje','','EnergetskeSkupnosti','sonce','veter','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/ODZIV-V-TE-u-bi-kurili-odpadke/':('Sporočilo za javnost','Podnebje','','BrezPremoga','TEŠ','UmazaniPosli','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Vendarle-korak-naprej-v-slovenski-energetiki/':('Sporočilo za javnost','Podnebje','','EnergetskeSkupnosti','sonce','veter','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Se-samooskrba-iz-OVE-obeta-tudi-prebivalcem-v-blokih/':('Sporočilo za javnost','Podnebje','','EnergetskeSkupnosti','sonce','veter','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Parlamentarna-veina-ustavila-najnoveji-poskus-prikritega-reevanja-TE-a/':('Sporočilo za javnost','Podnebje','','BrezPremoga','TEŠ','UmazaniPosli','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Nova-subvencija-TEu/':('Sporočilo za javnost','Podnebje','','BrezPremoga','TEŠ','UmazaniPosli','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Darilo-premogovni-industriji-prazne-besede-ljudem/':('Sporočilo za javnost','Podnebje','','BrezPremoga','TEŠ','UmazaniPosli','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Boino-darilo-Ministrstva-za-infrastrukturo/':('Sporočilo za javnost','Podnebje','','BrezPremoga','TEŠ ','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Norveka-pred-sodie/':('Sporočilo za javnost','Podnebje','','Podnebje','Arktika','UmazaniPosli','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/SO-POZABILI-NA-SONCE/':('Sporočilo za javnost','Podnebje','','EnergetskeSkupnosti','sonce ','Prostovoljstvo','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Presuena-Slovenija-v-primeu-premoga/':('Sporočilo za javnost','Podnebje','','BrezPremoga','TEŠ','PodnebnePosledice','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Okolje-je-naa-glavnica-ki-je-ne-dovolimo-zapraviti/':('Sporočilo za javnost','O nas','','Greenpeace','','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Vlade-opuanje-premoga-ne-zanima/':('Sporočilo za javnost','Podnebje','','BrezPremoga','TEŠ ',' Podnebje','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/AS-ZA-PODNEBNO-UKREPANJE-JE-ZDAJ/':('Sporočilo za javnost','Podnebje','','Podnebje','BrezPremoga','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Podnebni-shod---budnica-Vladi/':('Sporočilo za javnost','Podnebje','','BrezPremoga ','BreakFree','Prostovoljstvo','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/ODZIV-na-izjavo-Energetika-Ljubljana-e-bi-lahko-bi-postavili-toplarno-na-objeme-/':('Sporočilo za javnost','Podnebje','','Podnebje','BrezPremoga','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Iz-prispevka-za-obnovljive-vire-subvencija-za-fosilni-vir/':('Sporočilo za javnost','Podnebje','','Podnebje','UmazaniPosli','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Vlada-se-uklanja-fosilni-industriji-pozablja-na-ljudi/':('Sporočilo za javnost','Podnebje ','','TEŠ','BreakFree','UmazaniPosli','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/ODZIV-Subvencija-za-TE-domnevno-ustavljena/':('Sporočilo za javnost','Podnebje ','','BrezPremoga','TEŠ','UmazaniPosli','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Subvenciji-za-TE6-je-potrebno-odlono-nasprotovati/':('Sporočilo za javnost','Podnebje ','','BrezPremoga','TEŠ','UmazaniPosli','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Komentar---Ratifikacija-Parikega-sporazuma-v-DZ-RS/':('Sporočilo za javnost','Podnebje ','','BrezPremoga','TEŠ','IPCC','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Prebivalci-kot-steber-energetske-tranzicije/':('Sporočilo za javnost','Podnebje','','EnergetskeSkupnosti','sonce','veter','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Onesnaenje-zraka-zaradi-premoga-ne-pozna-meja/':('Sporočilo za javnost','Podnebje ','','BrezPremoga','TEŠ ','Podnebje','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Izgubljeno-zdravje-in-domovi-dediina-ernobila-in-Fukuime/':('Sporočilo za javnost','Podnebje ','','jedrska','','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Nevarne-kemikalije-v-mnogih-znamkah-oblail-za-dejavnosti-na-prostem/':('Sporočilo za javnost','Prekomerna potrošnja','','Detox','DetoxOutdoor','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Kolo-podnebnih-ukrepov-se-obraa-poasi-a-v-Parizu-se-je-obrnilo/':('Sporočilo za javnost','Podnebje ','','Podnebje ','BrezPremoga','IPCC','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Kaj-pa-nae-podnebje/':('Sporočilo za javnost','Podnebje ','','Podnebje ','BrezPremoga','Prostovoljstvo','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Namesto-obnovljivega-energetskega-preboja-dodatna-jedrska-elektrarna-v-Krkem/':('Sporočilo za javnost','Podnebje ','','jedrska','','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Pred-parikim-podnebnim-vrhom-Na-poti-k-100--obnovljive-energije-za-vse/':('Sporočilo za javnost','Podnebje ','','Podnebje','BrezPremoga','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Ne-nafta-sonce-naj-napaja-Jadran/':('Sporočilo za javnost','Narava','','jadran','sonce','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Civilne-organizacije-iz-Jadranske-regije-stopijo-skupaj-za-zaito-Jadrana/':('Sporočilo za javnost','Narava','','jadran','oceani','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Papezeva_okroznica_okolju/':('Sporočilo za javnost','Podnebje ','','Podnebje','','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Energetski-koncept-Slovenije-spreminjajo-v-Jedrski-koncept-Slovenije/':('Sporočilo za javnost','Podnebje ','','BrezPremoga','jedrska','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Klici-SOS-za-Jadran-odmevajo-na-Hrvaki-ambasadi-v-Sloveniji/':('Sporočilo za javnost','Narava','','jadran','Oceani','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/V-naftno-avanturo-v-Jadranu-s-pomanjkljivo-okoljsko-tudijo/':('Sporočilo za javnost','Narava','','jadran','Oceani','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/rni-dnevi-za-modri-Jadran/':('Sporočilo za javnost','Narava','','jadran','Oceani','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Jedrska-varnost-tiri-leta-po-Fukuimi/':('Sporočilo za javnost','Podnebje ','','jedrska','','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Greenpeace-ob-ponovnih-poplavah-opozarja-Slovenija-potrebuje-podnebno-strategijo/':('Sporočilo za javnost','Podnebje ','','Podnebje ','PodnebnePosledice','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Poroilo-Priklenjeni/':('Sporočilo za javnost','Podnebje ','','Podnebje','UmazaniPosli','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Vlada-v-odhodu-uniuje-prihodnost-obnovljivih-virov-energije/':('Sporočilo za javnost','Podnebje','','EnergetskeSkupnosti','sonce','veter','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Rainbow-Warrior-v-Sloveniji-v-podporo-obnovljivim-virom-energije/':('Sporočilo za javnost','Podnebje','','EnergetskeSkupnosti','sonce','veter','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Stalia-politinih-strank-o-obnovljivhi-virih-in-jedrski-energiji/':('Sporočilo za javnost','Podnebje','','EnergetskeSkupnosti','jedrska','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/komentar_koalicijske_pogodbe/':('Sporočilo za javnost','Podnebje','','Podnebje','jedrska','TEŠ','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Raziskava-javnega-menja-ve-kot-91--Slovencev-podpira-napredne-podnebno-energetske-cilje-EU/':('Sporočilo za javnost','Podnebje','','EnergetskeSkupnosti','sonce','veter','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/IPCC---3-porocilo/':('Sporočilo za javnost','Podnebje','','Podnebje','IPCC','PodnebnePosledice','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/EU-se-mora-odzvati-na-straljivo-poroilo-IPCC-o--posledicah-podnebnih-sprememb/':('Sporočilo za javnost','Podnebje','','Podnebje','IPCC','PodnebnePosledice','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_Bratusek/':('Sporočilo za javnost','Podnebje ','','Podnebje ','','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_zustaviteTES1/':('Sporočilo za javnost','Prekomerna potrošnja','','Detox','','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_zustaviteTES/':('Sporočilo za javnost','Podnebje ','','BrezPremoga Podnebje ','TEŠ','UmazaniPosli','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_barcolana/':('Sporočilo za javnost','Narava','','Oceani','Arktika','Prostovoljstvo','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_komentar_EZ1/':('Sporočilo za javnost','Narava','','Oceani','Arktika','Prostovoljstvo','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_30dni/':('Sporočilo za javnost','Narava','','Oceani','Arktika','Prostovoljstvo','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_odprtopismoIPCC1/':('Sporočilo za javnost','Narava','','Oceani','Arktika','Prostovoljstvo','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_odprtopismoIPCC/':('Sporočilo za javnost','Podnebje','','Podnebje','IPCC','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_PRipcc/':('Sporočilo za javnost','Narava','','Oceani','Arktika','Prostovoljstvo','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/odprto_pismo/':('Sporočilo za javnost','Podnebje ','','BrezPremoga','TEŠ','UmazaniPosli','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/endcoal/':('Sporočilo za javnost','Podnebje ','','BrezPremoga','TEŠ','UmazaniPosli','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/premogubija/':('Sporočilo za javnost','Podnebje ','','BrezPremoga','TEŠ','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/tihiubijalci/':('Sporočilo za javnost','Podnebje ','','BrezPremoga','zdravje','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_odlocitevEU/':('Sporočilo za javnost','Narava','','Oceani ','TrajnostnoRibištvo','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_predaja_ladjic1/':('Sporočilo za javnost','Narava','','Oceani ','TrajnostnoRibištvo','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_aspr/':('Sporočilo za javnost','Narava','','Oceani ','TrajnostnoRibištvo','Prostovoljstvo','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_odprtopismovladi/':('Sporočilo za javnost','Podnebje ','','BrezPremoga','TEŠ','UmazaniPosli','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_energetska_revolucija2012/':('Sporočilo za javnost','Podnebje','','EnergetskeSkupnosti','sonce','veter','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_prekomeren_ribolov/':('Sporočilo za javnost','Narava','','Oceani','TrajnostnoRibištvo','Prostovoljstvo','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_odziv-tes/':('Sporočilo za javnost','Podnebje ','','BrezPremoga','TEŠ','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_potrjeno_porostvo/':('Sporočilo za javnost','Podnebje ','','BrezPremoga','TEŠ','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_novinarskates/':('Sporočilo za javnost','Podnebje ','','BrezPremoga','TEŠ','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_odprto_pismotes/':('Sporočilo za javnost','Podnebje ','','BrezPremoga','TEŠ','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_eib_posojilo/':('Sporočilo za javnost','Podnebje ','','BrezPremoga','TEŠ','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_netet/':('Sporočilo za javnost','Podnebje ','','BrezPremoga','','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_Fukusima2013/':('Sporočilo za javnost','Podnebje ','','jedrska','','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_akcija_hse/':('Sporočilo za javnost','Podnebje','','BrezPremoga','Prostovoljstvo','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_heal/':('Sporočilo za javnost','Podnebje ','','BrezPremoga','zdravje','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_akcija_hse_koncniPR/':('Sporočilo za javnost','Podnebje','','BrezPremoga','Prostovoljstvo','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_izjava_koalicije/':('Sporočilo za javnost','Podnebje ','','BrezPremoga','TEŠ','UmazaniPosli','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/odziv_tes6/':('Sporočilo za javnost','Podnebje ','','BrezPremoga','TEŠ','UmazaniPosli','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_tiskovka_ustavimotes6/':('Sporočilo za javnost','Podnebje ','','BrezPremoga','TEŠ','UmazaniPosli','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_odprto_pismo/':('Sporočilo za javnost','Podnebje ','','BrezPremoga','TEŠ','UmazaniPosli','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_tour/':('Sporočilo za javnost','Podnebje','','BrezPremoga','Podnebje','prostovoljstvo','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_press-release2/':('Sporočilo za javnost','Podnebje ','','BrezPremoga','TEŠ','UmazaniPosli','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/_press-release6/':('Sporočilo za javnost','Podnebje ','','BrezPremoga','TEŠ','UmazaniPosli','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/novo-porocilo-ipcc-obnovljiva-energija/':('Sporočilo za javnost','Podnebje ','','EnergetskeSkupnosti','IPCC','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/greenpeace-in-dopps-ob-dnevu-z/':('Sporočilo za javnost','Podnebje ','','Podnebje','EnergetskeSkupnosti','Veter','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/v-kopenhagnu-zapravljena-zgodo/':('Sporočilo za javnost','Podnebje ','','Podnebje','','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/odprto-pismo-premieru-borutu-p/':('Sporočilo za javnost','Podnebje ','','jedrska','','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/greenpeace-in-umanotera-za-enj/':('Sporočilo za javnost','O nas','','Greenpeace','Podnebje','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Novo-poroilo-dokazuje-da-celoten-ivljenjski-cikel-plastike-ogroa-ljudi/':('Sporočilo za javnost','Prekomerna potrošnja','','Plastika','zdravje','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/informativna-gradiva/_dirty_laundry/':('Publikacija','Prekomerna potrošnja','','Detox','','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/informativna-gradiva/_dirty_laundryII/':('Publikacija','Prekomerna potrošnja','','Detox','','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/informativna-gradiva/_lekcije_iz_fukusime/':('Publikacija','Podnebje','','Jedrska','','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/informativna-gradiva/_dirty_laundry_povzetek/':('Publikacija','Prekomerna potrošnja','','Detox','','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/informativna-gradiva/_dirty_laundryIII/':('Publikacija','Prekomerna potrošnja','','Detox','','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/informativna-gradiva/_metodologija_sostanj/':('Publikacija','Podnebje','','BrezPremoga','TEŠ','zdravje','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/informativna-gradiva/_porocilo_sostanjpdf/':('Publikacija','Podnebje','','BrezPremoga','TEŠ','zdravje','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/informativna-gradiva/_QA_sostanjpdf1/':('Publikacija','Podnebje','','BrezPremoga','TEŠ','zdravje','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/informativna-gradiva/_pointofnoreturn/':('Publikacija','Podnebje','','BrezPremoga','Podnebje','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/informativna-gradiva/tihi_morilci/':('Publikacija','Podnebje','','BrezPremoga','veter','sonce','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/informativna-gradiva/powER-2030-grid-report/':('Publikacija','Podnebje','','BrezPremoga','veter','sonce','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/informativna-gradiva/Poroilo-Priklenjeni/':('Publikacija','Podnebje','','podnebje','umazaniPosli','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/kaj-delamo/izberi-isto-energijo/_energetska_revolucija/':('Publikacija','Podnebje','','BrezPremoga','Sonce','veter','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/informativna-gradiva/Stopinje-v-snegu/':('Publikacija','Prekomerna potrošnja','','Detox','detoxOutdoor','','article','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Blog/Blog/zakaj-se-pridruujem-greenpeaceovima-ladjama-p/blog/62139/?fbclid=IwAR1Y4KSFM4YrwQPbkJl4mXdR0_SzxaSOFA_6maB5On5nX72GL3heRFOZSik':('Blog','Prekomerna potrošnja','','Plastika','','','news-list','Migrate'),
        'http://www.greenpeace.org/slovenia/si/Medijsko-sredisce/zadnje-objave/Nestle-in-Unilever-imenovana-za-najveja-onesnaevalca-s-plastiko/':('Sporočilo za javnost','Prekomerna potrošnja','','Plastika','','','article','Migrate'),
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
        '''
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
            lead_text = response.xpath('//*[@id="content"]/div[3]/div/div[2]/div[1]/div/text()').extract()[0]
        except IndexError:
            lead_text = ''

        body_text = response.xpath('//*[@id="content"]/div[3]/div/div[2]/div[2]').extract()[0]
        if body_text:
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.org/').replace('href="/', 'href="http://www.greenpeace.org/')
            body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)
            if lead_text:
                body_text = '<div class="leader">' + lead_text + '</div>' + body_text + response.xpath(' //*[@id="content"]/div[3]/div/div[2]/p').extract_first()

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
        except IndexError:
            date_field = ""

        if date_field:
            date_field = dateutil.parser.parse(date_field)
        '''
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
            'author': 'Greenpeace Slovenia',
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

        month_sl_en = {
            'januar': 'January',
            'februar': 'February',
            'marec': 'March',
            'april': 'April',
            'maj': 'May',
            'junij': 'June',
            'julij': 'July',
            'avgust': 'August',
            'september': 'September',
            'oktober': 'October',
            'november': 'November',
            'december': 'December',
        }

        # Replace the Bulgarian month name with english month name.
        for sl_month, en_month in month_sl_en.iteritems():
            month_name = month_name.replace(sl_month, en_month)

        return month_name;

    def csv_writer(self, data, path):
        # Write data to a CSV file path
        with open(path, "a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(data)
