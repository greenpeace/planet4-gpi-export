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
        'FEED_URI': 'gpph_staging_v2.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    __connector_csv_filename = "connector_v1_final.csv"
    __connector_csv_log_file = "connector_csv_log_v1"

    def start_requests(self):
        
        start_urls = {
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/4-findings-from-new-york-hearings-that-give-r/blog/61947/':('Press Release','Sustainability','','Climate','Justice','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/6-filipinas-who-fight-for-climate-justice/blog/58896/':('Story','Society','','Climate','Justice','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/an-open-letter-of-solidarity-and-support/blog/47355/':('Story','Society','','Climate','Justice','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/atimonan-catholic-church-goes-solar/blog/53668/':('Story','Sustainability','','Energy','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/backyard-gardening-and-climate-change/blog/50860/':('Story','Sustainability','','Food','Climate','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/beyond-rejection/blog/59363/':('Story','Society','','Activism','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/cavite-city-open-dumpsite-a-pile-of-observati/blog/47867/':('Story','Sustainability','','Pollution','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/ecological-agriculture-the-future-of-food-pro/blog/46997/':('Story','Sustainability','','Food','Justice','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/filipino-farmers-share-seeds-of-hope/blog/51755/':('Story','Sustainability','','Food','Climate','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/for-the-love-of-sharks/blog/53489/':('Story','Sustainability','','Oceans','Food','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/four-reasons-why-communities-are-beating-corp/blog/61830/':('Story','Sustainability','','Climate','Justice','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/giving-the-gift-of-time/blog/62078/':('Story','Community','','Volunteer','Food','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/goodness-its-gulay-familiar-flavors-in-a-plan/blog/62065/':('Story','Sustainability','','Food','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/have-a-colorful-salad-or-pasta-plate-in-farm-/blog/62061/':('Story','Sustainability','','Food','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/how-plant-based-do-you-want-your-diet-to-be/blog/61780/':('Story','Sustainability','','Food','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/i-survived-the-strongest-typhoon-to-ever-hit-/blog/57946/':('Story','Society','','Climate','Justice','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/karla-rey-translator-of-paano-kumain-ng-kulay/blog/62009/':('Story','Sustainability','','Food','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/love-in-the-time-of-climate-change/blog/58729/':('Press Release','Sustainability','','Climate','Justice','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/mabi-david-author-of-paano-kumain-ng-kulay/blog/62003/':('Story','Sustainability','','Food','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/malita-and-san-miguels-duck-a-short-story/blog/42520/':('Story','Sustainability','','Energy','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/mga-bayaning-walang-kapa/blog/60349/':('Story','Community','','Volunteer','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/new-zealander-cycles-the-philippines-coasts-t/blog/57608/':('Story','Sustainability','','Plastic','Oceans','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/noodles-dimsum-and-other-plant-based-asian-fa/blog/62074/':('Story','Sustainability','','Food','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/ompong-through-a-farmers-eyes/blog/61897/':('Story','Sustainability','','Food','Justice','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/plant-based-with-an-exciting-spice-y-twist-in/blog/62071/':('Story','Sustainability','','Food','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/plastic-regulation-its-time-has-come/blog/41107/':('Press Release','Sustainability','','Plastic','Pollution','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/rainbow-warrior-sparks-hope-in-manila/blog/61163/':('Story','Community','','Ships','Climate','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/reducing-our-plastic-footprint/blog/49799/':('Story','Sustainability','','Plastic','Pollution','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/saludo-sa-mga-tunay-na-bayani/blog/57371/':('Story','Society','','Activism','Justice','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/saving-the-environmentmore-fun-in-the-philipp/blog/44871/':('Story','Society','','Activism','Oceans','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/something-old-something-new/blog/62124/':('Story','Sustainability','','Energy','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/sona-reflection-on-the-state-of-water-in-the-/blog/26538/':('Story','Society','','Activism','Climate','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/ten-practical-tips-to-practically-practice-en/blog/41229/':('Story','Sustainability','','Activism','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/territorial-fight-is-an-ecological-tragedy/blog/49781/':('Story','Sustainability','','Oceans','Justice','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/the-boon-of-living-sustainably-slowly-accordi/blog/61395/':('Story','Sustainability','','Climate','Plastic','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/the-possible-the-miraculous-true-wonders/blog/61227/':('Story','Society','','Activism','Climate','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/the-women-of-balangaw/blog/61228/':('Story','Community','','Ships','AboutUs','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/the-women-rafters-of-lake-pandin/blog/48443/':('Story','Community','','Volunteer','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/vegan-longganisa-thats-not-a-typo-and-more-at/blog/62053/':('Story','Sustainability','','Food','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/water-patrol-documents-the-threats-to-majayja/blog/13115/':('Story','Sustainability','','Pollution','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/we-are-not-a-nation-of-40-million-cowards-but/blog/62131/':('Story','Community','','Bataris','Democracy','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/we-have-one-year-to-create-the-largest-ever-p/blog/60541/':('Story','Sustainability','','Oceans','Climate','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/we-have-the-power-to-change-the-tuna-industry/blog/62045/':('Story','Sustainability','','Oceans','Food','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/why-bianca-king-went-plant-based-with-her-die/blog/61740/':('Story','Sustainability','','Food','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/why-im-joining-the-greenpeace-ships-to-fight-/blog/62138/':('Story','Sustainability','','Ships','Plastic','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/world-water-day-breaking-the-wasteful-habit/blog/44446/':('Story','Sustainability','','Pollution','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/news-stories/a-climate-of-tragedy-in-the-ph/':('Story','Sustainability','','Climate','Justice','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/news-stories/a-hero-for-the-environment/':('Story','Community','','AboutUs','Activism','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/news-stories/agrochemicals-a-major-source-o/':('Press Release','Sustainability','','Pollution','Food','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/news-stories/chemical-fertilizer-use-linked/':('Press Release','Sustainability','','Food','Climate','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/news-stories/Contest-Design-a-logo-for-Detox-Pilipinas/':('Story','Sustainability','','Pollution','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/news-stories/Defend-our-oceans/':('Story','Sustainability','','Oceans','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/news-stories/Dont-know-what-to-do-with-your-old-and-damaged-mobile-phones/':('Story','Sustainability','','Pollution','Energy','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/news-stories/drinking-water-in-benguet-bul/':('Story','Sustainability','','Pollution','Food','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/news-stories/e-jeepneys-hit-the-streets-of/':('Story','Sustainability','','Energy','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/news-stories/End-impunity-People-planet-and-peace-over-profit/':('Story','Society','','Climate','Justice','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/news-stories/Green-Holiday-Tips/':('Story','Sustainability','','Activism','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/news-stories/greenpeace-launches-project-cleanwater/':('Story','Sustainability','','Pollution','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/news-stories/Greenpeace-Southeast-Asia-appoints-Yeb-Sano-as-new-Executive-Director/':('Press Release','Community','','AboutUs','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/news-stories/greenpeace-water-patrol-invest/':('Story','Sustainability','','Pollution','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/news-stories/greenpeace-water-patrol-marilao/':('Story','Sustainability','','Pollution','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/news-stories/Hope-amid-devastation-in-one-of-the-worlds-best-marine-sanctuaries/':('Story','Sustainability','','Oceans','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/news-stories/indonesia-makes-it-to-2008-gui/':('Story','Sustainability','','Pollution','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/news-stories/Letter-to-BFAR-on-CNFIDP/':('Story','Sustainability','','Oceans','Food','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/news-stories/lto-issues-new-orange-plates-t/':('Story','Sustainability','','Energy','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/news-stories/Million-Acts-of-Blue/':('Story','Sustainability','','Plastic','Pollution','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/news-stories/on-the-road-to-a-climate-catas/':('Story','Sustainability','','Climate','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/news-stories/rubbis-at-the-bay/':('Story','Sustainability','','Oceans','Plastic','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/news-stories/The-harsh-reality-of-longline-fishing/':('Story','Sustainability','','Oceans','Food','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/news-stories/toxic_threat_in_th_rp/':('Story','Society','','Pollution','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/news-stories/War-on-poverty-and-illegal-fishing-must-continue/':('Story','Society','','Oceans','Justice','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/news-stories/water-pollution-a-grim-realit/':('Story','Sustainability','','Pollution','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/news-stories/We-have-the-power-to-shape-the-future-of-food-and-farming/':('Story','Sustainability','','Food','Justice','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/News/news-stories/Yolanda-survivors-share-their-stories-at-the-first-ever-Climate-Justice-Short-Film-Festival/':('Press Release','Society','','Climate','Justice','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/After-Ompong-Monde-Nissin-JBC-Food-Corporation-top-plastic-waste-count-in-Pasig-River/':('Press Release','Sustainability','','Plastic','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/arroyo-signs-solid-waste-manag/':('Press Release','Sustainability','','Pollution','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Big-fossil-fuel-companies-told-to-show-up-at-unprecedented-investigation-into-human-rights-harms-resulting-from-climate-change/':('Press Release','Sustainability','','Climate','Justice','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Cebu-breaks-free-from-plastic-onboard-the-Rainbow-Warrior/':('Press Release','Sustainability','','Ships','Plastic','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Clean-up-and-brand-audit-in-Lahug-River-as-Cebuanos-rally-for-a-plastic-free-future/':('Press Release','Sustainability','','Plastic','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Climate-change-to-devastate-Philippine-Seas-Greenpeace-proposes-Roadmap-to-Recovery/':('Press Release','Sustainability','','Oceans','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Coca-Cola-Nestle-Danone-Mars-Pepsi-and-Unilever-sign-global-plastics-pledge-but-still-havent-prioritized-reduction/':('Press Release','Sustainability','','Plastic','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Comprehensive-rehab-of-Manila-Bay-is-possible-necessary/':('Press Release','Sustainability','','Pollution','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Corporate-Leadership-Badly-Needed-to-Reverse-Plastic-Pollution-Crisis/':('Press Release','Sustainability','','Plastic','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/EcoGroups-Warn-Against-Plastic-Waste-Burning/':('Press Release','Sustainability','','Plastic','Pollution','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Envi-groups-raise-alarm-on-Nickelodeon-threat-to-sustainability-of-Palawan/':('Press Release','Sustainability','','Oceans','Bataris','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Envi-orgs-slam-disposal-of-Canadian-waste-in-PH-landfill/':('Press Release','Sustainability','','Pollution','Justice','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Environment-groups-relieved-over-Viacom-break-up-with-Coral-World-Park-on-planned-undersea-theme-park-in-Coron/':('Press Release','Sustainability','','Oceans','Bataris','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Fisherfolk-count-gains-one-year-after-Amended-Fisheries-Code/':('Press Release','Sustainability','','Oceans','Food','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Fisherfolk-groups-to-President-Aquino--Save-Philippine-fisheries-adopt-Roadmap-to-Recovery/':('Press Release','Sustainability','','Oceans','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Fisheries-stakeholders-on-the-effective-implementation-of-RA-10654/':('Press Release','Sustainability','','Oceans','Justice','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/For-the-first-time-fossil-fuel-companies-face-national-human-rights-complaint-on-climate-change/':('Press Release','Society','','Climate','Justice','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Garbage-engulfing-Manila-Philippines-after-severe-storm-highlights-plastic-and-climate-crises/':('Press Release','Sustainability','','Plastic','Climate','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Global-survey-reveals-FMCG-companies-contribution-to-plastic-pollution-crisis/':('Press Release','Sustainability','','Plastic','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Going-beyond-corporate-responsibility-Manilas-top-hotels-and-restaurants-advocate-for-sustainable-seafood-/':('Press Release','Sustainability','','Oceans','Food','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/GREEN-ADVOCATES-REMIND-PRESIDENT-DUTERTE-OF-ENVIRONMENTAL-TO-DO-LIST/':('Press Release','Society','','Democracy','Activism','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Green-groups-to-Nestle-Own-up-pay-up-clean-up-your-act/':('Press Release','Sustainability','','Plastic','Activism','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Green-Thumb-Coalition-dares-candidates-to-bare-their-platforms-for-the-environment/':('Press Release','Society','','Democracy','Activism','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Greenpeace-11th-hour-for-the-climate-its-time-for-leadership-to-truly-emerge/':('Press Release','Sustainability','','Climate','Justice','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Greenpeace-action-in-Manila-Bay-protests-broken-system-from-plastic-production-leading-to-massive-waste-crisis/':('Press Release','Sustainability','','Plastic','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Greenpeace-calls-for-ratification-of-Basel-Ban-Amendment-following-discovery-of-Canadian-toxic-shipment/':('Press Release','Sustainability','','Pollution','Climate','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Greenpeace-condemns-bloody-dispersal-of-farmers-in-Cotabato-and-demands-government-action-on-El-Nino/':('Press Release','Society','','Democracy','Food','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Greenpeace-DOJ-terror-list-puts-innocents-in-danger/':('Press Release','Society','','Democracy','Justice','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Greenpeace-expose-juvenile-baby-tuna-catch-in-Philippine-tuna-industry/':('Press Release','Sustainability','','Food','Oceans','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Greenpeace-NCCA-and-KWF-release-Balagtasan-video-on-National-Heroes-Day/':('Press Release','Sustainability','','Climate','Justice','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Greenpeace-Only-five-out-of-23-tuna-canneries-in-Southeast-Asia-make-the-grade--/':('Press Release','Sustainability','','Oceans','Food','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Greenpeace-Philippines-clean-up-name-culprits-behind-plastic-pollution-in-Manila-Bay/':('Press Release','Sustainability','','Plastic','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Greenpeace-Philippines-reaction-to-the-appointment-of-Roy-Cimatu-as-DENR-Secretary-/':('Press Release','Society','','Democracy','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Greenpeace-PRRC-track-plastic-pollution-in-Pasig-River-kicks-off-clean-up-project-along-Manila-Bay/':('Press Release','Sustainability','','Plastic','Pollution','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Greenpeace-ranking-reveals-fashion-companies-action-on-toxic-pollution/':('Press Release','Sustainability','','Pollution','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Greenpeace-ranks-Philippine-tuna-canneries-based-on-sustainable-and-equitable-fisheries-guidelines/':('Press Release','Sustainability','','Oceans','Food','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Greenpeace-Statement-on-the-45th-anniversary-of-the-Declaration-of-Martial-Law/':('Press Release','Society','','Democracy','Justice','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Greenpeace-Statement-on-the-assassination-of-environmental-lawyer-Mia-Manuelita-Cumba-Masacarinas-Green/':('Press Release','Society','','Justice','Democracy','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/greenpeace-statement-on-the-gu/':('Press Release','Sustainability','','Pollution','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Greenpeace-statement-on-the-murder-of-Gloria-Capitan-anti-coal-activist-in-Bataan/':('Press Release','Society','','Energy','Justice','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Greenpeace-statement-on-the-proposed-coal-plant-in-Batangas-City/':('Press Release','Sustainability','','Climate','Energy','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Greenpeace-statement-on-the-release-of-sky-lanterns-during-Haiyan-commemorations-/':('Press Release','Sustainability','','Justice','Plastic','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Greenpeace-tells-ASEAN-Act-on-plastics-pollution-in-regions-ocean/':('Press Release','Sustainability','','Plastic','Pollution','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Greenpeace-to-DENR-Implement-pollution-disclosure-to-save-our-rivers/':('Press Release','Sustainability','','Pollution','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Greenpeace-to-DENR-opening-of-protected-areas-to-special-private-use-is-wrong-move/':('Press Release','Society','','Democracy','Justice','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Groups-demand-immediate-return-of-Canadian-toxic-waste/':('Press Release','Sustainability','','Climate','Pollution','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Groups-remind-Duterte-Address-food-crisis-before-first-100-days-of-presidency-ends/':('Press Release','Sustainability','','Food','Justice','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Groups-Urge-President-Duterte-to-Wage-War-on-Waste-and-Pollution/':('Press Release','Sustainability','','Pollution','Democracy','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Groups-Welcome-Assurance-Given-by-BOC-for-the-Re-Export-of-Korean-Garbage-by-End-of-the-Year/':('Press Release','Sustainability','','Plastic','Pollution','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Guimaras-is-first-coal-free-province-in-Visayas/':('Press Release','Sustainability','','Energy','Climate','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Illegal-dumpsite-in-Manila-Bay-shut-down-by-Greenpeace-EcoWaste-Coalition/':('Press Release','Sustainability','','Pollution','Oceans','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/IPs-Palawan-groups-intensify-opposition-to-planned-Nickelodeon-undersea-attraction/':('Press Release','Sustainability','','Oceans','Bataris','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/La-Union-citizens-call-for-better-measures-vs-corporate-polluters/':('Press Release','Sustainability','','Energy','Justice','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Landmark-CHR-investigation-into-corporate-responsibility-for-climate-change-to-conclude-in-PH-with-collection-of-evidence-now-on-record/':('Press Release','Sustainability','','Climate','Justice','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Landmark-ordinance-in-Cebu-sets-to-establish-the-countrys-first-shark-and-ray-sanctuary/':('Press Release','Sustainability','','Oceans','Activism','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Marilao-River-is-one-of-spotlight-case-studies-in-new-Greenpeace-report-on-Hidden-Costs-of-Toxic-Water-Pollution/':('Press Release','Sustainability','','Pollution','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Nestle-misses-the-mark-with-statement-on-tackling-its-single-use-plastics-problem/':('Press Release','Sustainability','','Plastic','Pollution','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Nestle-Unilever-PG-among-worst-offenders-for-plastic-pollution-in-Philippines-in-beach-audit/':('Press Release','Sustainability','','Plastic','Pollution','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/New-Greenpeace-report-estimates-coal-plant-emissions-could-kill-2400-Filipinos-per-year/':('Press Release','Sustainability','','Energy','Justice','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Over-90-of-sampled-salt-brands-globally-found-to-contain-microplastics/':('Press Release','Sustainability','','Plastic','Food','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/People-and-planet-not-profit---Greenpeace-activists-demand-Shell--show-up-at-climate-change-and-human-rights-inquiry/':('Press Release','Sustainability','','Climate','Justice','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Petitioners-consolidated-reply-to-the-respondent-Carbon-Majors-in-the-National-Public-Inquiry-being-conducted-by-Commission-on-Human-Rights-of-the-Philippines/':('Press Release','Society','','Democracy','Climate','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Philippine-canneries-fall-short-on-sustainability-and-social-responsibility-issues--Greenpeace/':('Press Release','Sustainability','','Food','Oceans','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/philippine-fishing-companies-i/':('Press Release','Sustainability','','Oceans','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Philippine-seas-is-facing-an-unprecedented-crisis-/':('Press Release','Sustainability','','Oceans','Pollution','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Philippines-joins-the-mass-rally-of-activists-to-boost-world-movement-against-coal/':('Press Release','Sustainability','','Energy','Activism','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Philippines-launches-worlds-first-national-human-rights-investigation-into-50-big-polluters/Philippines-Supreme-Court-bans-development-of-genetically-engineered-products/':('Press Release','Sustainability','','Food','Justice','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Philippines-prepares-to-summon-47-companies-to-account-for-climate-change/':('Press Release','Sustainability','','Climate','Justice','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Philippines-set-to-lead-global-tuna-industry-to-sustainability-and-Go-Green/':('Press Release','Sustainability','','Oceans','Food','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Plastic-invades-centre-of-the-centre-of-global-biodiversity-hotspot/':('Press Release','Sustainability','','Plastic','Oceans','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Plastic-pollution-a-multifaceted-problem-calls-out-companies-to-take-action/':('Press Release','Sustainability','','Plastic','Pollution','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Policy-experts-say-environmental-protection-is-crucial-to-ASEAN-economic-integration-success/':('Press Release','Sustainability','','Plastic','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Rainbow-Warrior-to-bring-global-spotlight-on-the-Battle-for-Manila-Bay-vs-major-plastic-producers/':('Press Release','Sustainability','','Ships','Plastic','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Renewable-energy-is-the-key-to-economic-progress/':('Press Release','Sustainability','','Energy','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/See-Manila-Bay-for-yourself-aboard-Greenpeaces-Rainbow-Warrior-this-March/':('Press Release','Sustainability','','Ships','Plastic','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Shell-to-face-pressure-at-AGM-for-failing-to-take-responsibility--for-climate-related-human-rights-harms/':('Press Release','Sustainability','','Climate','Justice','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Solar-energy-use-for-homes-businesses-get-boost-in-form-of-financing-options/':('Press Release','Sustainability','','Energy','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/South-Korea-needs-to-be-reminded-that-Philippines-is-not-a-waste-dump-wont-solve-its-waste-problem/':('Press Release','Sustainability','','Plastic','Pollution','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Statement-on-Cove-Manilas-largest-balloon-drop-record-attempt-on-New-Years-Eve/':('Press Release','Sustainability','','Plastic','Bataris','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/SWS-Survey-on-Eating-Meat/':('Story','Sustainability','','Food','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/The-Rejection-of-Gina-is-a-Rejection-of-Change--Greenpeace-Statement-on-the-Commission-on-Appointments-rejection-of-Regina-Lopez-as-DENR-Secretary/':('Press Release','Society','','Democracy','Activism','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Voters-want-candidates-who-will-address-plastic-pollution-survey-reveals/':('Press Release','Society','','Democracy','Plastic','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/waste-survey-exposes-extent-of/':('Press Release','Sustainability','','Oceans','Plastic','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Worlds-largest-carbon-producers-ordered-to-respond-to-allegations-of-human-rights--abuses-from-climate-change/The-Climate-Change-and-Human-Rights-Petition/':('Press Release','Society','','Climate','Justice','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/Worlds-top-climate-experts-to-testify-in-landmark-investigation-into-fossil-fuel-companies/':('Press Release','Sustainability','','Climate','Justice','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/releases/YOLANDA-5-YEARS-ON-SURVIVORS-IN-LONDON-TO-FIGHT-FOR-CLIMATE-JUSTICE/':('Press Release','Sustainability','','Climate','Justice','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/reports/Briefing-Paper-Forum-on-Fish-Aggregating-Devices/':('Press Release','Sustainability','','Oceans','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/reports/climate-change-water-impacts-philippines/':('Publication','Sustainability','','Climate','Food','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/reports/Coal-A-Public-Health-Crisis/':('Publication','Sustainability','','Energy','Justice','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/reports/Dirty-Laundry-2/':('Publication','Sustainability','','Pollution','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/reports/Existing-and-proposed-coal-plants-in-the-Philippines/':('Publication','Sustainability','','Energy','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/reports/From-Sea-to-Can-2018-Southeast-Asia-Canned-Tuna-Ranking/':('Publication','Sustainability','','Oceans','Food','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/reports/Laguna-Lake-The-Philippines-Industrial-Contamination-Hotspots/':('Press Release','Sustainability','','Pollution','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/reports/Roadmap-to-Roadmap-to-Recovery-of-Philippine-Oceans/':('Publication','Sustainability','','Oceans','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/reports/Sprouting-from-Disaster/':('Publication','Sustainability','','Food','Climate','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/reports/the-state-of-water-in-the-phil/':('Publication','Sustainability','','Pollution','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/reports/True-Cost-of-Coal-in-the-Philippines/':('Publication','Sustainability','','Energy','Climate','','article','Migrate'),
            'http://www.greenpeace.org/seasia/ph/press/reports/Tuna-Cannery-Ranking-/':('Publication','Sustainability','','Oceans','Food','','article','Migrate'),
            'https://www.greenpeace.org/seasia/ph/About-us/Greenpeace-Southeast-Asia/Annual-reports/Annual-Report-2015/':('Publication','Community','','AboutUs','','','article','Migrate'),
            'https://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/ompong-through-a-farmers-eyes/blog/61897/':('Story','Sustainability','','Food','','','news-list','Migrate'),
            'https://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/we-are-not-a-nation-of-40-million-cowards-but/blog/62131/':('Story','Community','','Bataris','Democracy','','news-list','Migrate'),
            'https://www.greenpeace.org/seasia/ph/News/greenpeace-philippine-blog/why-im-joining-the-greenpeace-ships-to-fight-/blog/62138/':('Story','Sustainability','','Ships','Plastic','','news-list','Migrate'),
            'https://www.greenpeace.org/seasia/ph/press/releases/Cebu-breaks-free-from-plastic-onboard-the-Rainbow-Warrior/':('Press Release','Sustainability','','Plastic','Ships','','article','Migrate'),
            'https://www.greenpeace.org/seasia/ph/press/releases/Green-groups-to-Nestle-Own-up-pay-up-clean-up-your-act/':('Press Release','Sustainability','','Plastic','','','article','Migrate'),
            'https://www.greenpeace.org/seasia/ph/press/releases/Greenpeace-action-in-Manila-Bay-protests-broken-system-from-plastic-production-leading-to-massive-waste-crisis/':('Press Release','Sustainability','','Plastic','Pollution','','article','Migrate'),
            'https://www.greenpeace.org/seasia/ph/press/releases/Greenpeace-Philippines-statement-on-the-dead-whale-in-the-Philippines-with-40kgs-of-plastic-in-its-stomach/':('Press Release','Sustainability','','Plastic','Pollution','','article','Migrate'),
            'https://www.greenpeace.org/seasia/ph/press/releases/Greenpeace-statement-on-the-high-ranking-of-Philippine-cities-in-World-Air-Quality-Report/':('Press Release','Sustainability','','Pollution','','','article','Migrate'),
            'https://www.greenpeace.org/seasia/ph/press/releases/IsyuHindiKandidato-wants-us-to-talk-about-issues-that-matter/':('Press Release','Society','','Activism','Democracy','','article','Migrate'),
            'https://www.greenpeace.org/seasia/ph/press/releases/SWS-Survey-on-Eating-Meat/':('Publication','Sustainability','','Food','','','article','Migrate'),
            'https://www.greenpeace.org/seasia/ph/press/releases/Voters-want-candidates-who-will-address-plastic-pollution-survey-reveals/':('Press Release','Society','','Plastic','Democracy','','article','Migrate'),
            'https://www.greenpeace.org/seasia/ph/press/reports/From-Sea-to-Can-2018-Southeast-Asia-Canned-Tuna-Ranking/':('Press Release','Sustainability','','Oceans','Food','','article','Migrate'),
            'https://www.greenpeace.org/seasia/ph/press/reports/Sprouting-from-Disaster/':('Press Release','Sustainability','','Food','','','article','Migrate'),
            'https://www.greenpeace.org/seasia/ph/press/reports/Time-to-Ban-Single-Use-Plastics-and-Protect-the-Oceans/':('Press Release','Sustainability','','Plastic','Oceans','','article','Migrate'),
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
            #date_field = self.filter_month_name(date_field); #This is not needed for sites in english
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
                emailid = emailid.replace('', '')
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
                self.csv_writer(data, "email_images_url_list.csv")
        

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
            #date_field = self.filter_month_name(date_field); #This is not needed for sites in english
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
                emailid = emailid.replace('', '')
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
                self.csv_writer(data, "email_images_url_list.csv")
        


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
            'author': 'Greenpeace Philippines',
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
    """
    def filter_month_name(self, month_name):

        month_ph_en = {
            'siječnja': 'January',
            'veljače': 'February',
            'ožujka': 'March',
            'travnja': 'April',
            'svibnja': 'May',
            'lipnja': 'June',
            'srpnja': 'July',
            'kolovoza': 'August',
            'Augusta': 'August',
            'rujna': 'September',
            'listopada': 'October',
            'Octobera': 'October',
            'studenog': 'November',
            'prosinca': 'December',
        }

        # Replace the Philippino month name with english month name.
        for ph_month, en_month in month_ph_en.iteritems():
            month_name = month_name.replace(ph_month, en_month)

        return month_name;
    """
    def csv_writer(self, data, path):
        # Write data to a CSV file path
        with open(path, "a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(data)
