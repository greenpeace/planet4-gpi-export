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
        'FEED_URI': 'gpden_staging_v2.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    __connector_csv_filename = "connector_v2_final.csv"
    __connector_csv_log_file = "connector_csv_log_v2"

    def start_requests(self):
        # v1
        start_urls = {
            'http://www.greenpeace.org/denmark/da/nyheder/blog/plastikforurening-truer-med-at-kvle-vores-bl-/blog/60747/':('Story','HAV','Plastik','','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/milj-og-fdevareministerens-fem-myter-om-landb/blog/61121/':('Story','LAND','Landbrug','Klimaforandringer','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/ellemann-jensen-mangler-at-kmpe-den-vigtigste/blog/61816/':('Story','LAND','Landbrug','','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/billig-el-og-grnt-spin-fr-os-ikke-meget-nrmer/blog/61435/':('Story','KLIMA','Energi','','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/4-r-efter-den-mexicanske-golf/blog/48991/':('Story','KLIMA','Energi','Klimaforandringer','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/Gilleleje-kuttere-afsloret-i-trawlfiskeri-i-Oresund/':('Press Release','HAV','Fiskeri','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2017/Greenpeace-i-aktion-ved-fodevaretopmode-31-grise-udstiller-Danmark-som-darlige-varter-og-beder-regeringen-skrue-ned-for-kodet/':('Press Release','LAND','Landbrug','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2016/5-ar-efter-Fukushima---55000-mennesker-retur-til-alt-for-hoj-radioaktiv-straling/':('Press Release','KLIMA','Energi','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/Danske-supermarkeder-dumper-tun-test/':('Press Release','HAV','Fiskeri','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/Greenpeace-om-Arla-indflydelse-Regeringen-forsommer-vigtigste-dagsorden-pa-fodevaretopmode/':('Press Release','LAND','Landbrug','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/rapporter-og-dokumenter/2006/8-danskere/':('Publication','MENNESKER','Forbrug','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/rapporter-og-dokumenter/2018/Udspil-til-regeringen-Sadan-skal-dansk-landbrug-bidrage-til-et-mere-stabilt-klima/':('Publication','LAND','Landbrug','Klimaløsninger','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/rapporter-og-dokumenter/2014/Rapport-Monsterbade-overfisker-Danmarks-og-verdens-pressede-fiskebestande/':('Publication','HAV','Fiskeri','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2004/bifangst-af-delfiner-og-marsvi/':('Press Release','HAV','Fiskeri','Esperanza','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2006/10-tidligere-miljoministre-fr/':('Press Release','KLIMA','Energi','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/2015/DET-MENER-PARTIERNE/':('Story','KLIMA','Klimaløsninger','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/2018/Greenpeace-i-aktion-ved-fodevaretopmode-31-grise-udstiller-Danmark-som-darlige-varter-og-beder-regeringen-skrue-ned-for-kodet/':('Story','LAND','Landbrug','Klimaforandringer','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/2018/ATP-investerer-sort/':('Story','KLIMA','Klimaforandringer','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/2018/Dansk-Landbrugs-storste-ammoniakudslip/':('Story','LAND','Landbrug','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/2012/Dit-toj-er-fyldt-med-farlige-kemikalier/':('Story','MENNESKER','Forbrug','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/rapporter-og-dokumenter/2018/Greenpeace-undersogelse-Kommunerne-halter-efter-befolkningen-pa-kod/':('Publication','LAND','Landbrug','Klimaforandringer','','article','Migrate'),
            ## - duplicate post
            ##'http://www.greenpeace.org/denmark/da/press/rapporter-og-dokumenter/2018/Udspil-til-regeringen-Sadan-skal-dansk-landbrug-bidrage-til-et-mere-stabilt-klima/':('Publication','LAND','Landbrug','Klimaforandringer','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2017/Hjalpepakke-til-Marsk-forlanger-levetid-for-oliegas/':('Press Release','KLIMA','Klimaforandringer','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/Afgorelse-faldet-i-historisk-klimaretssag/':('Press Release','KLIMA','Klimaforandringer','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2017/Greenpeace-rapport-Sadan-skyller-stor-papirproducent-Nordens-urskov-ud-i-toilettet/':('Press Release','LAND','Skov','','','article','Migrate')
        }


        # v2
        #### - duplicate post.
        start_urls = {
            # Batch 1
            'http://www.greenpeace.org/denmark/da/nyheder/2011/Folg-den-alvorlige-situation-i-Japan/Sporgsmal-og-svar/':('Story','KLIMA','Energi','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/2012/den-lyseroede-floddelfin/':('Story','LAND','Skov','Fiskeri','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/2012/Dit-toj-er-fyldt-med-farlige-kemikalier/':('Story','MENNESKER','Forbrug','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/2012/Levis-giver-efter-og-forbyder-farlige-kemikalier/':('Story','MENNESKER','Forbrug','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/2013/En-uge-oversvommet-med-hajer-/':('Story','HAV','Fiskeri','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/2014/Rapport-Monsterbade-overfisker-Danmarks-og-verdens-pressede-fiskebestande/':('Story','HAV','Fiskeri','','','article','Migrate'),
            #### 'http://www.greenpeace.org/denmark/da/nyheder/2014/Rapport-Monsterbade-overfisker-Danmarks-og-verdens-pressede-fiskebestande/':('Story','HAV','Fiskeri','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/2015/DET-MENER-PARTIERNE/':('Story','KLIMA','Klimaløsninger','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/2016/Godt-for-DONG-ikke-for-klimaet/':('Story','KLIMA','Energi','Klimaforandringer','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/2016/Hvad-gemmer-tundasen/':('Story','HAV','Fiskeri','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/2016/Mikroperler---bittesma-djavle-der-fylder-havene-og-fisk-med-plastik/':('Story','HAV','Plastik','Forbrug','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/2016/Sejr-for-Amazonas-regnskoven-Odelaggende-mega-damning-i-Brasilien-annulleret/':('Story','LAND','Skov','Energi','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/2016/Tjernobyl-30-ar-efter-en-ulykke-uden-ende-/':('Story','KLIMA','Energi','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/2017/Havbrug-er-tikkende-bomber-under-vores-natur/':('Story','HAV','Fiskeri','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/2017/Trump-tager-et-skridt-frem-for-en-doende-kulindustri-to-tilbage-for-klimaet/':('Story','KLIMA','Energi','Klimaforandringer','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/2018/Afsloring-Ulovligt-trawlfiskeri-i-Oresund/':('Story','HAV','Fiskeri','Havbeskyttelse','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/2018/ATP-investerer-sort/':('Story','KLIMA','Klimaforandringer','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/2018/Beskidt-transport/':('Story','LAND','Landbrug','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/2018/Dansk-Landbrugs-storste-ammoniakudslip/':('Story','LAND','Landbrug','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/2018/Greenpeace-i-aktion-ved-fodevaretopmode-31-grise-udstiller-Danmark-som-darlige-varter-og-beder-regeringen-skrue-ned-for-kodet/':('Story','LAND','Landbrug','Klimaforandringer','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/2018/Greenpeace-undersogelse-EU-belonner-de-storste-ammoniak-forurenere/':('Story','LAND','Landbrug','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/2018/Hovedstaden-baner-vej-for-plantemad-pa-menuen-/':('Story','LAND','Landbrug','Forbrug','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/2018/Tag-udgangspunkt-i-gronsagerne/':('Story','MENNESKER','Forbrug','Landbrug','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/30-r-efter-rainbow-warrior-sidder-stadig-i-os/blog/53491/':('Story','MENNESKER','RainbowWarrior','','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/4-r-efter-den-mexicanske-golf/blog/48991/':('Story','KLIMA','Energi','Klimaforandringer','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/50-procent-vedvarende-energi-i-2030-ikke-ambi/blog/58839/':('Story','KLIMA','Klimaforandringer','Klimaløsninger','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/7-gode-grunde-til-at-beskytte-det-arktiske-oc/blog/56985/':('Story','HAV','Havbeskyttelse','','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/8-skove-i-verden-vi-skal-kmpe-for/blog/55946/':('Story','LAND','Skov','','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/atomkraft-er-en-dd-sild/blog/56648/':('Story','KLIMA','Energi','','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/atomkraft-er-hverken-sikker-eller-ren/blog/39364/':('Story','KLIMA','Energi','','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/atomkraft-farlig-nu-og-mange-tusind-r-frem/blog/54696/':('Story','KLIMA','Klimaforandringer','','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/billig-el-og-grnt-spin-fr-os-ikke-meget-nrmer/blog/61435/':('Story','KLIMA','Energi','','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/censureret-video-se-reklame-samarbejdet-melle/blog/49895/':('Story','KLIMA','Klimaforandringer','','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/danmark-skal-kmpe-p-det-grnne-vinderhold-i-eu/blog/61313/':('Story','KLIMA','Energi','Klimaløsninger','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/den-danske-kdindustri-skal-p-slankekur/blog/60958/':('Story','LAND','Landbrug','','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/den-virkelige-pris-for-en-dse-tun/blog/57575/':('Story','HAV','Fiskeri','','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/derfor-skal-vi-have-frre-svin-i-danmark-tale-/blog/61845/':('Story','LAND','Landbrug','','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/dong-lukker-2-blokke-p-enstedvrket-og-stigsns/blog/32177/':('Story','KLIMA','Energi','Klimaløsninger','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/ellemann-jensen-mangler-at-kmpe-den-vigtigste/blog/61816/':('Story','LAND','Landbrug','','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/en-uge-bag-kulissen/blog/42771/':('Story','MENNESKER','Græsrod','','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/eu-belnner-de-strste-forurenere-og-kdprodukti/blog/61526/':('Story','LAND','Landbrug','Klimaforandringer','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/fire-ting-der-skal-til-for-at-stoppe-skovbran/blog/54642/':('Story','LAND','Skov','Klimaforandringer','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/forslag-til-nye-klima-og-energiml-er-de-ambit/blog/60785/':('Story','KLIMA','Energi','Klimaløsninger','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/gmo-landbrug-lser-ikke-verdens-sultproblemer/blog/58179/':('Story','LAND','Landbrug','','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/har-du-tnkt-p-at-blive-frivillig/blog/35259/':('Story','MENNESKER','Græsrod','','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/havmiljet-og-torskebestanden-har-vundet-i-gil/blog/58594/':('Story','HAV','Fiskeri','','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/hvad-gemmer-tundsen-p/blog/58688/':('Story','HAV','Fiskeri','','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/hvalfangst-p-island-trods-internationalt-forb/blog/45631/':('Story','HAV','Fiskeri','','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/hvor-bliver-havisen-af/blog/58135/':('Story','KLIMA','Klimaforandringer','Havbeskyttelse','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/i-dag-rydder-vi-op-p-tunhylderne/blog/59150/':('Story','HAV','Fiskeri','','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/ikke-flere-legeaftaler-med-shell/blog/49712/':('Story','KLIMA','Klimaforandringer','Forbrug','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/kingfisher-er-en-monsterbd/blog/51474/':('Story','HAV','Fiskeri','','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/kitkat-i-problemer/blog/32087/':('Story','LAND','Skov','Forbrug','','news-list','Migrate'),

            # Batch 2
            'http://www.greenpeace.org/denmark/da/nyheder/blog/mgbeskidte-svinetransporter/blog/61738/':('Story','LAND','Landbrug','','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/milj-og-fdevareministerens-fem-myter-om-landb/blog/61121/':('Story','LAND','Landbrug','Klimaforandringer','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/millioner-af-afrikanere-truet-af-overfiskeri/blog/60763/':('Story','HAV','Fiskeri','','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/mindre-kd-p-den-kommunale-menu/blog/61726/':('Story','LAND','Landbrug','Klimaløsninger','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/nu-ved-vi-hvad-slogans-som-just-do-it-og-impo/blog/47223/':('Story','MENNESKER','Forbrug','','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/p-besg-hos-aleuterne/blog/41334/':('Story','HAV','Fiskeri','Esperanza','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/piratfiskere-p-rovdrift-i-resund/blog/61291/':('Story','HAV','Fiskeri','','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/plastikforurening-truer-med-at-kvle-vores-bl-/blog/60747/':('Story','HAV','Plastik','','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/regeringens-olie-og-gas-stop-gr-ingen-gavn-fo/blog/61290/':('Story','KLIMA','Klimaforandringer','Klimaløsninger','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/nyheder/blog/tre-grunde-til-at-stoppe-frihandelsaftalerne-/blog/57723/':('Story','MENNESKER','Forbrug','Græsrod','','news-list','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2004/bifangst-af-delfiner-og-marsvi/':('Press Release','HAV','Fiskeri','Esperanza','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2006/10-tidligere-miljoministre-fr/':('Press Release','KLIMA','Energi','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2006/blodig-alvor-greenpeace-afslorer/':('Press Release','MENNESKER','Forbrug','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2006/blodig-alvor/':('Press Release','MENNESKER','Forbrug','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2006/giftige-stoffer-i-baerbare-computere/':('Press Release','MENNESKER','Forbrug','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2006/regeringens-energipolitik-er-k/':('Press Release','KLIMA','Klimaforandringer','Energi','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2007/1-generations-biobrandsel-er-en-uholdbar-losning/':('Press Release','KLIMA','Energi','Klimaforandringer','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2007/nokia-snubler-i-mangelfuld-ret/':('Press Release','MENNESKER','Forbrug','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2008/hvor-ender-verdens-elektronika/':('Press Release','MENNESKER','Forbrug','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2009/greenpeace-besoger-gilleleje/':('Press Release','HAV','Fiskeri','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2011/Biodiesel-i-Danmark-kan-skade-bade-klima-miljo-og-verdens-fattige/':('Press Release','KLIMA','Energi','Klimaforandringer','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2011/Giftigt-stof-fundet-i-toj-fra-HM-og-andre-store-tojmarker/':('Press Release','MENNESKER','Forbrug','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2011/Nike-tager-historisk-skridt-til-giftfri-tojproduktion/':('Press Release','MENNESKER','Forbrug','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2013/GMO-piner-jorden-og-skaber-mistrivsel-hos-danske-svin/':('Press Release','LAND','Landbrug','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2014/Greenpeace-rapport-Monsterbade-overfisker-Danmarks-og-verdens-pressede-fiskebestande/':('Press Release','HAV','Fiskeri','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2015/Greenpeace-undersogelse-10-procent-af-tekstilbranchen-forpligter-sig-til-kemikaliefrit-toj-/':('Press Release','MENNESKER','Forbrug','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2016/5-ar-efter-Fukushima---55000-mennesker-retur-til-alt-for-hoj-radioaktiv-straling/':('Press Release','KLIMA','Energi','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2016/Greenpeace-rapport-Tandpastaen-har-bismag-af-afbrandt-regnskov/':('Press Release','MENNESKER','Forbrug','Skov','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2016/Nike-Esprit-Victorias-Secret-og-LiNing-skraber-kemi-bunden/':('Press Release','MENNESKER','Forbrug','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2017/Greenpeace-ekspedition-har-fundet-mikroplastik-og-flourstoffer-ved-Antarktis/':('Press Release','HAV','Plastik','Forbrug','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2017/Greenpeace-i-aktion-ved-fodevaretopmode-31-grise-udstiller-Danmark-som-darlige-varter-og-beder-regeringen-skrue-ned-for-kodet/':('Press Release','LAND','Landbrug','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2017/Greenpeace-undersogelse-EU-belonner-de-storste-ammoniak-forurenere/':('Press Release','LAND','Landbrug','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2017/Greenpeace-undersogelse-Flertal-i-EUs-Landbrugsudvalg-har-starke-band-til-erhvervet/':('Press Release','LAND','Landbrug','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/ATP-investerer-milliarder-i-sort/':('Press Release','KLIMA','Klimaforandringer','Klimaløsninger','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/Danske-supermarkeder-dumper-tun-test/':('Press Release','HAV','Fiskeri','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/Energiaftale-satter-klimaambitionerne-pa-standby/':('Press Release','KLIMA','Energi','Klimaforandringer','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/Gilleleje-kuttere-afsloret-i-trawlfiskeri-i-Oresund/':('Press Release','HAV','Fiskeri','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/Godt-okologi-udspil-fra-LF-og-Okologisk-Landsforening-misser-kodets-belastning-af-klimaet/':('Press Release','LAND','Landbrug','Klimaforandringer','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/Greenpeace-om-Arla-indflydelse-Regeringen-forsommer-vigtigste-dagsorden-pa-fodevaretopmode/':('Press Release','LAND','Landbrug','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/Greenpeace-undersogelse-Kommunerne-halter-efter-befolkningen-pa-kod/':('Press Release','LAND','Landbrug','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/rapporter-og-dokumenter/2006/8-danskere/':('Publication','MENNESKER','Forbrug','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/rapporter-og-dokumenter/2013/Point-of-No-Return/':('Publication','KLIMA','Klimaforandringer','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/rapporter-og-dokumenter/2014/Rapport-Monsterbade-overfisker-Danmarks-og-verdens-pressede-fiskebestande/':('Publication','HAV','Fiskeri','','','article','Migrate'),
            #### 'http://www.greenpeace.org/denmark/da/press/rapporter-og-dokumenter/2018/Greenpeace-undersogelse-Kommunerne-halter-efter-befolkningen-pa-kod/':('Publication','LAND','Landbrug','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/rapporter-og-dokumenter/2018/Pa-piratjagt-i-Oresund/':('Publication','HAV','Fiskeri','Havbeskyttelse','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/rapporter-og-dokumenter/2018/Udspil-til-regeringen-Sadan-skal-dansk-landbrug-bidrage-til-et-mere-stabilt-klima/':('Publication','LAND','Landbrug','Klimaløsninger','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/Afgorelse-faldet-i-historisk-klimaretssag/':('Press Release','KLIMA','Klimaforandringer','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/Greenpeace-Kvoteskandale-kan-vare-redning-for-dansk-fiskeri-og-havmiljo/':('Press Release','LAND','Fiskeri','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2016/Klimabelastende-klik-Netflix-leverer-serier-og-film-fra-fossiltung-strom/':('Press Release','KLIMA','Klimaforandringer','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2016/Obama-freder-Arktis-fra-nye-olieboringer-de-naste-fem-ar/':('Press Release','KLIMA','Klimaforandringer','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2016/Total-opgiver-skifergas-i-Danmark-Kampe-sejr-for-miljoet-og-klimaet/':('Press Release','KLIMA','Klimaforandringer','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2017/Flertal-giver-akut-forstehjalp-til-elbiler/':('Press Release','KLIMA','Klimaforandringer','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2017/Greenpeace-Ansvarlig-beslutning-at-Nordea-trakker-investeringer-fra-amerikansk-olierorledning/':('Press Release','KLIMA','Klimaforandringer','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2017/Greenpeace-rapport-Sadan-skyller-stor-papirproducent-Nordens-urskov-ud-i-toilettet/':('Press Release','LAND','Skov','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/pressemeddelelser/2017/Hjalpepakke-til-Marsk-forlanger-levetid-for-oliegas/':('Press Release','KLIMA','Klimaforandringer','','','article','Migrate'),
            'http://www.greenpeace.org/denmark/da/press/rapporter-og-dokumenter/2018/Greenpeace-undersogelse-Kommunerne-halter-efter-befolkningen-pa-kod/':('Publication','LAND','Landbrug','Klimaforandringer','','article','Migrate')
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
        author_usernames = {
            'Birgitte-Lesanner' : 'birgitte-lesanner',
            'Jan-Sondergard' : 'jan-sondergard',
            'Sune-Scheller' : 'sune-scheller',
            'Tarjei-Haaland' : 'tarjei-haaland',
            'David Bickett' : 'davidbickett',
            'Kristine Clement' : 'kristineclement'
        }

        # Read in the file
        with open( 'gpden_staging_v2.xml', 'r' ) as file :
            filedata = file.read()

        # Replace with correct usernames.
        for p3_author_username, p4_author_username in author_usernames.iteritems():
            filedata = filedata.replace('<author_username>' + p3_author_username,
                                        '<author_username>' + p4_author_username)

        # Remove dir="ltr" attributes from elements as requested.
        filedata = filedata.replace('dir="ltr"', '')

        # Write the file out again
        with open('gpden_staging_v2.xml', 'w') as file:
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
                if ( Segments[5] ):
                    author_username = Segments[5]
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
                    emailid, body_text)

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

        # list author with author username
        author_name = response.xpath('string(//div[@class="news-list"]/ul/li/*/*/span[@class="caption"]/span[@class="green1"]/strong)').extract()[0]
        # filter author name for extra strings in it.
        author_name = author_name.replace("af ", "")
        """
        data = [author_name, author_username]
        self.csv_writer(data, "blog_author_list.csv")
        """

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
                body_text = '<div class="leader"><b>' + lead_text + '</b></div>' + body_text + response.xpath(' //*[@id="content"]/div[4]/div/div[2]/p').extract_first()
                # Fix pdf link issue for denmark.
                body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.org/').replace('href="/', 'href="http://www.greenpeace.org/')

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
                    emailid, body_text)

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
            'author': 'Greenpeace Denmark',
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

        month_da_en = {
            'januar': 'January',
            'februar': 'February',
            'marts': 'March',
            'april': 'April',
            'maj': 'May',
            'juni': 'June',
            'juli': 'July',
            'august': 'August',
            'september': 'September',
            'oktober': 'October',
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
