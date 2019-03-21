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
from dateutil.relativedelta import relativedelta


locale.setlocale(locale.LC_ALL, '')

class AllSpider(scrapy.Spider):
    name = 'all'

    custom_settings = {
        'ROBOTSTXT_OBEY': 0,
        'FEED_URI': 'gpth_staging_v2.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    __connector_csv_filename = "connector_v2_final.csv"
    __connector_csv_log_file = "connector_csv_log_v2"

    def start_requests(self):
        # v2
        start_urls = {
            # B1
            'http://www.greenpeace.org/seasia/th/press/reports/Greenpeace-and-Thai-Union-Group-Summary-of-Agreement_TH/':('ข่าวประชาสัมพันธ์','ปกป้อง','','ทะเลและมหาสมุทร','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/Recommendations-from-People-Network-for-Sustainable-Development-to-Minister-of-Environment/':('ข่าวประชาสัมพันธ์','ปกป้อง','','สภาพภูมิอากาศ','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/Local-fishing-statement-on-Thailand-Yellow-Card/':('ข่าวประชาสัมพันธ์','ปกป้อง','','ทะเลและมหาสมุทร','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/Greenpeace-pushes-for-stronger-tuna-conservation-and-management-measures-in-WCPFC/':('ข่าวประชาสัมพันธ์','ปกป้อง','','ทะเลและมหาสมุทร','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/Thai-Union-Commits-to-More-Sustainable-Socially-Responsible-Seafood/':('ข่าวประชาสัมพันธ์','ปกป้อง','','ทะเลและมหาสมุทร','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/Nearly-700000-people-call-on-Thai-Union-for-more-sustainable-ethical-tuna/':('ข่าวประชาสัมพันธ์','ปกป้อง','','ทะเลและมหาสมุทร','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/Mars-Nestle-commit-to-clean-up-pet-food-supply-chains-increasing-pressure-on-Thai-Union-to-act/':('ข่าวประชาสัมพันธ์','ปกป้อง','','ทะเลและมหาสมุทร','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/Greenpeace-demands-Thai-Government-to-improve-PM25-air-quality-standards/':('ข่าวประชาสัมพันธ์','ปกป้อง','','อากาศสะอาด','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/greenpeace-opinion-toward-new-air-quality-index-pollution-control-department/':('ข่าวประชาสัมพันธ์','ปกป้อง','','อากาศสะอาด','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/Greenpeace-calls-on-Prime-Minister-Prayuth-Chan-Ocha-to-tackle-air-pollution-crisis/':('ข่าวประชาสัมพันธ์','ปกป้อง','','อากาศสะอาด','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/Thailand-suffers-from-poor-air-quality-and-fails-to-meet-Sustainable-Development-Goals--Greenpeace/':('ข่าวประชาสัมพันธ์','ปกป้อง','','อากาศสะอาด','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/open-letter-to-PCD-on-air-pollution/':('ข่าวประชาสัมพันธ์','ปกป้อง','','อากาศสะอาด','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/Thailand-city-ranking-2016/':('ข่าวประชาสัมพันธ์','ปกป้อง','','อากาศสะอาด','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/right-to-clean-air/':('ข่าวประชาสัมพันธ์','ปกป้อง','','อากาศสะอาด','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/greenpeace-investigation-wilmar-brands-palm-oil-deforestation-indonesia/':('ข่าวประชาสัมพันธ์','ปกป้อง','','ป่าไม้','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/nestle-aiming-at-100-recyclable-or-reusable-packaging-by-2025/':('ข่าวประชาสัมพันธ์','ปฏิเสธ','','พลาสติก','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/Muaklek-coal-greenpeace-statement/':('ข่าวประชาสัมพันธ์','ปฏิเสธ','','ถ่านหิน','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/mueklek-EHIA/':('ข่าวประชาสัมพันธ์','ปฏิเสธ','','ถ่านหิน','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/Greenpeace-Rainbow-Warrior-arrives-for-a-solidarity-visit-to-Teluk-Patani/':('ข่าวประชาสัมพันธ์','ปฏิเสธ','','ถ่านหิน','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/NEW-REPORT-Global-Coal-Plant-Development-Drops-for-a-Second-Consecutive-Year/':('ข่าวประชาสัมพันธ์','ปฏิเสธ','','ถ่านหิน','สภาพภูมิอากาศ','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/save-Tueloe-Patani-from-coal/':('ข่าวประชาสัมพันธ์','ปฏิเสธ','','ถ่านหิน','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/Greenpeace-statement-EHIA-Songkla-coal-plant/':('ข่าวประชาสัมพันธ์','ปฏิเสธ','','ถ่านหิน','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/NEW-REPORT-Global-Coal-Plant-Development-Freefall-Sparks-Renewed-Hope-On-Climate-Goals/':('ข่าวประชาสัมพันธ์','ปฏิเสธ','','ถ่านหิน','สภาพภูมิอากาศ','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/Resettlement-in-contaminated-areas-steamrolls-ahead-as-residents-mark-Fukushima-anniversary/':('ข่าวประชาสัมพันธ์','ปฏิเสธ','','นิวเคลียร์','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/Fukushima-nuclear-disaster-an-ongoing-crisis-with-no-end-in-sight-Greenpeace/':('ข่าวประชาสัมพันธ์','ปฏิเสธ','','นิวเคลียร์','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/nuclear-legacies-Chernobyl-Fukushima/':('ข่าวประชาสัมพันธ์','ปฏิเสธ','','นิวเคลียร์','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/statement-paraquat-ban-veto/':('ข่าวประชาสัมพันธ์','เปลี่ยนแปลง','','ระบบอาหาร','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/veggie-TH/':('ข่าวประชาสัมพันธ์','เปลี่ยนแปลง','','ระบบอาหาร','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/Greenpeace-calls-for-less-meat-more-vegetables-to-help-fight-climate-change/':('ข่าวประชาสัมพันธ์','เปลี่ยนแปลง','','ระบบอาหาร','สภาพภูมิอากาศ','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/greenpeace-calls-for-decrease-in-meat-and-dairy-production-and-consumption-for-a-healthier-planet/':('ข่าวประชาสัมพันธ์','เปลี่ยนแปลง','','ระบบอาหาร','สภาพภูมิอากาศ','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/An-effort-to-change-school-lunch-menus-to-sustainable-safe-and-non-chemical/':('ข่าวประชาสัมพันธ์','เปลี่ยนแปลง','','ระบบอาหาร','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/100Renewable-Energy-in-Krabi-possible-by-2026/':('ข่าวประชาสัมพันธ์','เปลี่ยนแปลง','','พลังงานหมุนเวียน','สภาพภูมิอากาศ','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/Greenpeace-RE-sector-to-build-massive-workforce-in-Thailand-More-than-170000-green-jobs-by-2050-with-100-percent-Renewable-Energy/':('ข่าวประชาสัมพันธ์','เปลี่ยนแปลง','','พลังงานหมุนเวียน','สภาพภูมิอากาศ','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/campaigns/eco-farming-for-our-food/eco-fertilizer/':('บทความ','เปลี่ยนแปลง','','ระบบอาหาร','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/59239/':('บทความ','เปลี่ยนแปลง','','ระบบอาหาร','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/pm25/blog/61132/ ':('บทความ','ปกป้อง','','อากาศสะอาด','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/pm25/blog/57660/ ':('บทความ','ปกป้อง','','อากาศสะอาด','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/59982/':('บทความ','ปกป้อง','','ทะเลและมหาสมุทร','พลาสติก','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/58766/':('บทความ','ปฏิเสธ','','ถ่านหิน','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/5/blog/59464/':('บทความ','เปลี่ยนแปลง','','ไลฟ์สไตล์','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/5/blog/62084/':('บทความ','เปลี่ยนแปลง','','คนและสังคม','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/10/blog/61797/':('บทความ','ปกป้อง','','ป่าไม้','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/62110/':('บทความ','ปกป้อง','','สภาพภูมิอากาศ','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/62092/':('บทความ','ปกป้อง','','สภาพภูมิอากาศ','คนและสังคม','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/pabuk/blog/62085/':('บทความ','ปกป้อง','','สภาพภูมิอากาศ','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/62079/':('บทความ','ปกป้อง','','สภาพภูมิอากาศ','คนและสังคม','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/56699/':('บทความ','ปกป้อง','','สภาพภูมิอากาศ','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/3-2561/blog/62069/':('บทความ','ปกป้อง','','สภาพภูมิอากาศ','พลาสติก','อากาศสะอาด','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/10/blog/59232/':('บทความ','ปกป้อง','','สภาพภูมิอากาศ','','','news-list','Migrate'),
            'https://www.greenpeace.org/seasia/th/news/blog1/5-15/blog/61956/':('บทความ','ปกป้อง','','สภาพภูมิอากาศ','','','news-list','Migrate'),

            # B2
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/61886/':('บทความ','ปกป้อง','','สภาพภูมิอากาศ','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/61725/':('บทความ','ปกป้อง','','สภาพภูมิอากาศ','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/5/blog/61662/':('บทความ','ปกป้อง','','สภาพภูมิอากาศ','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/60969/':('บทความ','ปกป้อง','','สภาพภูมิอากาศ','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/61485/':('บทความ','ปกป้อง','','สภาพภูมิอากาศ','คนและสังคม','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/global-warning/blog/60317/':('บทความ','ปกป้อง','','สภาพภูมิอากาศ','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/55565/':('บทความ','ปกป้อง','','ทะเลและมหาสมุทร','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/61755/':('บทความ','ปกป้อง','','ทะเลและมหาสมุทร','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/61752/':('บทความ','ปกป้อง','','ทะเลและมหาสมุทร','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/61746/':('บทความ','ปกป้อง','','ทะเลและมหาสมุทร','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/59888/':('บทความ','ปกป้อง','','ทะเลและมหาสมุทร','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/11/blog/57467/':('บทความ','ปกป้อง','','ทะเลและมหาสมุทร','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/59863/':('บทความ','ปกป้อง','','ทะเลและมหาสมุทร','คนและสังคม','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/59831/':('บทความ','ปกป้อง','','ทะเลและมหาสมุทร','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/7/blog/58373/':('บทความ','ปกป้อง','','ทะเลและมหาสมุทร','ไลฟ์สไตล์','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/62142/':('บทความ','ปกป้อง','','อากาศสะอาด','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/62141/':('บทความ','ปกป้อง','','อากาศสะอาด','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/pm25/blog/62121/':('บทความ','ปกป้อง','','อากาศสะอาด','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/pm25/blog/62116/':('บทความ','ปกป้อง','','อากาศสะอาด','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/2562-pm25/blog/62106/':('บทความ','ปกป้อง','','อากาศสะอาด','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/62104/':('บทความ','ปกป้อง','','อากาศสะอาด','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/62099/':('บทความ','ปกป้อง','','อากาศสะอาด','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/pm25/blog/62098/':('บทความ','ปกป้อง','','อากาศสะอาด','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/pm25/blog/62094/':('บทความ','ปกป้อง','','อากาศสะอาด','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/62086/':('บทความ','ปกป้อง','','อากาศสะอาด','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/3-pm25/blog/62083/':('บทความ','ปกป้อง','','อากาศสะอาด','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/pm25-aqi/blog/61803/':('บทความ','ปกป้อง','','อากาศสะอาด','คนและสังคม','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/pm-25/blog/57678/':('บทความ','ปกป้อง','','อากาศสะอาด','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/61365/':('บทความ','ปกป้อง','','อากาศสะอาด','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/people-aqi/blog/61316/':('บทความ','ปกป้อง','','อากาศสะอาด','คนและสังคม','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/pm25/blog/61248/':('บทความ','ปกป้อง','','อากาศสะอาด','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/pm25/blog/61175/':('บทความ','ปกป้อง','','อากาศสะอาด','คนและสังคม','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/pm25/blog/61156/':('บทความ','ปกป้อง','','อากาศสะอาด','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/pm25/blog/61053/':('บทความ','ปกป้อง','','อากาศสะอาด','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/livable-city-40-04-mayday-khon-kaen-smart-cit/blog/61051/':('บทความ','ปกป้อง','','อากาศสะอาด','คนและสังคม','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/ccdc-pm25/blog/60873/':('บทความ','ปกป้อง','','อากาศสะอาด','คนและสังคม','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/pm25-2560/blog/60005/':('บทความ','ปกป้อง','','อากาศสะอาด','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/-/blog/59924/':('บทความ','ปกป้อง','','อากาศสะอาด','คนและสังคม','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/59891/':('บทความ','ปกป้อง','','อากาศสะอาด','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/pm25/blog/59763/':('บทความ','ปกป้อง','','อากาศสะอาด','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/59590/':('บทความ','ปกป้อง','','อากาศสะอาด','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/pm25/blog/59453/':('บทความ','ปกป้อง','','อากาศสะอาด','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/pm25/blog/57660/':('บทความ','ปกป้อง','','อากาศสะอาด','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/righttocleanair/blog/57448/':('บทความ','ปกป้อง','','อากาศสะอาด','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/right-to-cean-air/':('บทความ','ปกป้อง','','อากาศสะอาด','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/55937/':('บทความ','ปกป้อง','','อากาศสะอาด','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/25-pm25/blog/55226/':('บทความ','ปกป้อง','','อากาศสะอาด','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/62113/':('บทความ','ปกป้อง','','ป่าไม้','','','news-list','Migrate'),
            'https://www.greenpeace.org/seasia/th/news/blog1/blog/61924/':('บทความ','ปกป้อง','','ป่าไม้','คนและสังคม','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/61641/':('บทความ','ปกป้อง','','ป่าไม้','','','news-list','Migrate'),

            # B3
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/60210/':('บทความ','ปกป้อง','','ป่าไม้','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/59325/':('บทความ','ปกป้อง','','ป่าไม้','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/57150/':('บทความ','ปกป้อง','','ป่าไม้','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/62137/':('บทความ','ปฏิเสธ','','พลาสติก','ไลฟ์สไตล์','คนและสังคม','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/how-to-2019-2019/blog/62082/':('บทความ','ปฏิเสธ','','พลาสติก','ไลฟ์สไตล์','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/62075/':('บทความ','ปฏิเสธ','','พลาสติก','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/62066/':('บทความ','ปฏิเสธ','','พลาสติก','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/csr/blog/62059/':('บทความ','ปฏิเสธ','','พลาสติก','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/7-go-green-7-Eleven/blog/62017/':('บทความ','ปฏิเสธ','','พลาสติก','','','news-list','Migrate'),
            'https://www.greenpeace.org/seasia/th/news/blog1/better-moon-x-refill-station/blog/61969/':('บทความ','ปฏิเสธ','','พลาสติก','ไลฟ์สไตล์','คนและสังคม','news-list','Migrate'),
            'https://www.greenpeace.org/seasia/th/news/blog1/blog/61948/':('บทความ','ปฏิเสธ','','พลาสติก','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/101/blog/61895/':('บทความ','ปฏิเสธ','','พลาสติก','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/61878/':('บทความ','ปฏิเสธ','','พลาสติก','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/61870/':('บทความ','ปฏิเสธ','','พลาสติก','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/61823/':('บทความ','ปฏิเสธ','','พลาสติก','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/61600/':('บทความ','ปฏิเสธ','','พลาสติก','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/55642/':('บทความ','ปฏิเสธ','','พลาสติก','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/61138/':('บทความ','ปฏิเสธ','','พลาสติก','คนและสังคม','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/60816/':('บทความ','ปฏิเสธ','','พลาสติก','คนและสังคม','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/60760/':('บทความ','ปฏิเสธ','','พลาสติก','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/the-story-of-a-spoon/blog/55906/':('บทความ','ปฏิเสธ','','พลาสติก','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/59511/':('บทความ','ปฏิเสธ','','พลาสติก','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/58586/':('บทความ','ปฏิเสธ','','พลาสติก','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/58977/':('บทความ','ปฏิเสธ','','พลาสติก','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/58423/':('บทความ','ปฏิเสธ','','พลาสติก','ไลฟ์สไตล์','คนและสังคม','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/6/blog/57544/':('บทความ','ปฏิเสธ','','พลาสติก','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/ehia/blog/62042/':('บทความ','ปฏิเสธ','','ถ่านหิน','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/61817/':('บทความ','ปฏิเสธ','','ถ่านหิน','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/61522/':('บทความ','ปฏิเสธ','','ถ่านหิน','คนและสังคม','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/ehia/blog/61119/':('บทความ','ปฏิเสธ','','ถ่านหิน','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/5/blog/60691/':('บทความ','ปฏิเสธ','','ถ่านหิน','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/60251/':('บทความ','ปฏิเสธ','','ถ่านหิน','คนและสังคม','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/eia-ehia/blog/58855/':('บทความ','ปฏิเสธ','','ถ่านหิน','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/58711/':('บทความ','ปฏิเสธ','','ถ่านหิน','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/-/blog/58565/':('บทความ','ปฏิเสธ','','ถ่านหิน','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/57775/':('บทความ','ปฏิเสธ','','ถ่านหิน','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/56227/':('บทความ','ปฏิเสธ','','ถ่านหิน','','','news-list','Migrate'),
            'https://www.greenpeace.org/seasia/th/news/blog1/blog/61909/':('บทความ','ปฏิเสธ','','นิวเคลียร์','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/5/blog/61482/':('บทความ','ปฏิเสธ','','นิวเคลียร์','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/32/blog/61432/':('บทความ','ปฏิเสธ','','นิวเคลียร์','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/61320/':('บทความ','ปฏิเสธ','','นิวเคลียร์','คนและสังคม','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/60276/':('บทความ','ปฏิเสธ','','นิวเคลียร์','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/60112/':('บทความ','ปฏิเสธ','','นิวเคลียร์','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/72/blog/59986/':('บทความ','ปฏิเสธ','','นิวเคลียร์','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/59681/':('บทความ','ปฏิเสธ','','นิวเคลียร์','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/15-things-you-didnt-know-about-chernobyl/blog/56124/':('บทความ','ปฏิเสธ','','นิวเคลียร์','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/62132/':('บทความ','เปลี่ยนแปลง','','ระบบอาหาร','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/-/blog/62136/':('บทความ','เปลี่ยนแปลง','','ระบบอาหาร','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/62112/':('บทความ','เปลี่ยนแปลง','','ระบบอาหาร','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/61978/':('บทความ','เปลี่ยนแปลง','','ระบบอาหาร','','','news-list','Migrate'),

            # B4
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/61989/':('บทความ','เปลี่ยนแปลง','','ระบบอาหาร','ไลฟ์สไตล์','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/61997/':('บทความ','เปลี่ยนแปลง','','ระบบอาหาร','ไลฟ์สไตล์','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/61979/':('บทความ','เปลี่ยนแปลง','','ระบบอาหาร','คนและสังคม','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/5/blog/61917/':('บทความ','เปลี่ยนแปลง','','ระบบอาหาร','ไลฟ์สไตล์','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/61912/':('บทความ','เปลี่ยนแปลง','','ระบบอาหาร','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/60458/':('บทความ','เปลี่ยนแปลง','','ระบบอาหาร','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/61559/':('บทความ','เปลี่ยนแปลง','','ระบบอาหาร','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/55510/':('บทความ','เปลี่ยนแปลง','','ระบบอาหาร','ไลฟ์สไตล์','คนและสังคม','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/Blog_PR_20_year_GMO/blog/55468/':('บทความ','เปลี่ยนแปลง','','ระบบอาหาร','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/59037/':('บทความ','เปลี่ยนแปลง','','ระบบอาหาร','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/60073/':('บทความ','เปลี่ยนแปลง','','ระบบอาหาร','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/world-meat-free-day-/blog/56728/':('บทความ','เปลี่ยนแปลง','','ระบบอาหาร','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/55972/':('บทความ','เปลี่ยนแปลง','','ระบบอาหาร','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/53150/':('บทความ','เปลี่ยนแปลง','','ระบบอาหาร','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/change-your-food-change-the-world-5/blog/51867/':('บทความ','เปลี่ยนแปลง','','ระบบอาหาร','ไลฟ์สไตล์','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/campaigns/eco-farming-for-our-food/sustainable-chicken-feed/':('บทความ','เปลี่ยนแปลง','','ระบบอาหาร','ไลฟ์สไตล์','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/60761/':('บทความ','เปลี่ยนแปลง','','ระบบอาหาร','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/59369/':('บทความ','เปลี่ยนแปลง','','ระบบอาหาร','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/61086/':('บทความ','เปลี่ยนแปลง','','ระบบอาหาร','คนและสังคม','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/62134/':('บทความ','เปลี่ยนแปลง','','พลังงานหมุนเวียน','สภาพภูมิอากาศ','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/57945/':('บทความ','เปลี่ยนแปลง','','พลังงานหมุนเวียน','สภาพภูมิอากาศ','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/53686/':('บทความ','เปลี่ยนแปลง','','พลังงานหมุนเวียน','สภาพภูมิอากาศ','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/100/blog/61620/':('บทความ','เปลี่ยนแปลง','','พลังงานหมุนเวียน','สภาพภูมิอากาศ','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/59240/':('บทความ','เปลี่ยนแปลง','','พลังงานหมุนเวียน','สภาพภูมิอากาศ','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/59960/':('บทความ','เปลี่ยนแปลง','','พลังงานหมุนเวียน','สภาพภูมิอากาศ','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/59733/':('บทความ','เปลี่ยนแปลง','','พลังงานหมุนเวียน','สภาพภูมิอากาศ','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/59677/':('บทความ','เปลี่ยนแปลง','','พลังงานหมุนเวียน','สภาพภูมิอากาศ','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/campaigns/climate-and-energy/energy-revolution/Renewable-Energy-Myth/1-The-grid-needs-baseload-power/':('บทความ','เปลี่ยนแปลง','','พลังงานหมุนเวียน','สภาพภูมิอากาศ','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/campaigns/climate-and-energy/energy-revolution/Renewable-Energy-Myth/2-RE-can-not-keep-up-with-growing-demand/':('บทความ','เปลี่ยนแปลง','','พลังงานหมุนเวียน','สภาพภูมิอากาศ','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/campaigns/climate-and-energy/energy-revolution/Renewable-Energy-Myth/3-RE-requires-huge-unfair-subsidies/':('บทความ','เปลี่ยนแปลง','','พลังงานหมุนเวียน','สภาพภูมิอากาศ','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/campaigns/climate-and-energy/energy-revolution/Renewable-Energy-Myth/4-RE-is-only-for-rich-countries-Coal-is-better-for-lifting-countries-out-of-poverty/':('บทความ','เปลี่ยนแปลง','','พลังงานหมุนเวียน','สภาพภูมิอากาศ','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/campaigns/climate-and-energy/energy-revolution/Renewable-Energy-Myth/5-RE-drives-up-electricity-prices/':('บทความ','เปลี่ยนแปลง','','พลังงานหมุนเวียน','สภาพภูมิอากาศ','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/campaigns/climate-and-energy/energy-revolution/Renewable-Energy-Myth/6-Battery-storage-is-too-expensive/':('บทความ','เปลี่ยนแปลง','','พลังงานหมุนเวียน','สภาพภูมิอากาศ','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/campaigns/climate-and-energy/energy-revolution/Renewable-Energy-Myth/7-Solar-panels-contain-toxic-materials/':('บทความ','เปลี่ยนแปลง','','พลังงานหมุนเวียน','สภาพภูมิอากาศ','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/campaigns/climate-and-energy/energy-revolution/Renewable-Energy-Myth/8-RE-uses-up-a-lot-of-land/':('บทความ','เปลี่ยนแปลง','','พลังงานหมุนเวียน','สภาพภูมิอากาศ','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/campaigns/climate-and-energy/energy-revolution/Renewable-Energy-Myth/9-Wind-turbines-kill-wildlife/':('บทความ','เปลี่ยนแปลง','','พลังงานหมุนเวียน','สภาพภูมิอากาศ','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/campaigns/climate-and-energy/energy-revolution/Renewable-Energy-Myth/10-RE-can-not-provide-the-jobs-that-FFs-do/':('บทความ','เปลี่ยนแปลง','','พลังงานหมุนเวียน','สภาพภูมิอากาศ','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/campaigns/climate-and-energy/energy-revolution/Renewable-Energy-Myth/11-Wind-power-is-not-good-for-local-people/':('บทความ','เปลี่ยนแปลง','','พลังงานหมุนเวียน','สภาพภูมิอากาศ','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/campaigns/climate-and-energy/energy-revolution/Renewable-Energy-Myth/12-RE-leads-to-grid-instability/':('บทความ','เปลี่ยนแปลง','','พลังงานหมุนเวียน','สภาพภูมิอากาศ','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/campaigns/climate-and-energy/energy-revolution/Renewable-Energy-Myth/13-Small-scale-solar-increases-costs-for-other-consumers/':('บทความ','เปลี่ยนแปลง','','พลังงานหมุนเวียน','สภาพภูมิอากาศ','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/6/blog/62144/':('บทความ','เปลี่ยนแปลง','','คนและสังคม','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/61894/':('บทความ','เปลี่ยนแปลง','','คนและสังคม','พลาสติก','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/ywm36/blog/61842/':('บทความ','เปลี่ยนแปลง','','คนและสังคม','พลาสติก','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/13/blog/59690/':('บทความ','เปลี่ยนแปลง','','คนและสังคม','สภาพภูมิอากาศ','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/59647/':('บทความ','เปลี่ยนแปลง','','คนและสังคม','เกี่ยวกับกรีนพีซ','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/45/blog/57504/':('บทความ','เปลี่ยนแปลง','','คนและสังคม','เกี่ยวกับกรีนพีซ','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/58300/':('บทความ','เปลี่ยนแปลง','','คนและสังคม','ไลฟ์สไตล์','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/-low-impact-living/blog/62081/':('บทความ','เปลี่ยนแปลง','','ไลฟ์สไตล์','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/62060/':('บทความ','เปลี่ยนแปลง','','ไลฟ์สไตล์','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/62052/':('บทความ','เปลี่ยนแปลง','','ไลฟ์สไตล์','','','news-list','Migrate'),

            # B5
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/62036/':('บทความ','เปลี่ยนแปลง','','ไลฟ์สไตล์','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/59505/':('บทความ','เปลี่ยนแปลง','','ไลฟ์สไตล์','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/5/blog/62125/':('บทความ','เปลี่ยนแปลง','','ไลฟ์สไตล์','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/th/news/blog1/blog/61187/':('บทความ','เปลี่ยนแปลง','','เกี่ยวกับกรีนพีซ','','','news-list','Migrate'),
            'https://www.greenpeace.org/seasia/th/press/reports/Thailand-Brand-Audit-Result/':('สิ่งพิมพ์','ปฏิเสธ','','พลาสติก','ทะเลและมหาสมุทร','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/campaigns/Urban-Revolution/Air-Pollution/Right-To-Clean-Air/City-ranking/2018/':('สิ่งพิมพ์','ปกป้อง','','อากาศสะอาด','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/No-Return-to-Normal/':('สิ่งพิมพ์','ปฏิเสธ','','นิวเคลียร์','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/annual-report-2017/':('สิ่งพิมพ์','กรีนพีซ','','เกี่ยวกับกรีนพีซ','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/campaigns/Urban-Revolution/Air-Pollution/Right-To-Clean-Air/Unmask-our-cities-booklet/':('สิ่งพิมพ์','ปกป้อง','','อากาศสะอาด','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/Less-is-more-handbook/':('สิ่งพิมพ์','เปลี่ยนแปลง','','ระบบอาหาร','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/campaigns/Ocean/Thailand-canned-tuna-ranking/2016/':('สิ่งพิมพ์','ปกป้อง','','ทะเลและมหาสมุทร','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/OCEANS-IN-THE-BALANCE-THAILAND-IN-FOCUS/':('สิ่งพิมพ์','ปกป้อง','','ทะเลและมหาสมุทร','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/save-our-ocean/':('สิ่งพิมพ์','ปกป้อง','','ทะเลและมหาสมุทร','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/supply-chained/':('สิ่งพิมพ์','ปกป้อง','','ทะเลและมหาสมุทร','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/2018-world-air-quality-report/':('สิ่งพิมพ์','ปกป้อง','','อากาศสะอาด','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/Satellite-derived-PM25-Mapping-Report/':('สิ่งพิมพ์','ปกป้อง','','อากาศสะอาด','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/campaigns/Urban-Revolution/Air-Pollution/Right-To-Clean-Air/City-ranking/2017/':('สิ่งพิมพ์','ปกป้อง','','อากาศสะอาด','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/campaigns/Urban-Revolution/Air-Pollution/Right-To-Clean-Air/City-ranking/2016/':('สิ่งพิมพ์','ปกป้อง','','อากาศสะอาด','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/campaigns/Urban-Revolution/Air-Pollution/Right-To-Clean-Air/City-ranking/2015/':('สิ่งพิมพ์','ปกป้อง','','อากาศสะอาด','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/campaigns/Urban-Revolution/Air-Pollution/Right-To-Clean-Air/City-ranking/First-half-2017/':('สิ่งพิมพ์','ปกป้อง','','อากาศสะอาด','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/campaigns/Urban-Revolution/plastic-pollution/No-single-use-plastic/Overwhelmed-plastic-trash/':('สิ่งพิมพ์','ปฏิเสธ','','พลาสติก','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/campaigns/Urban-Revolution/plastic-pollution/No-single-use-plastic/plastic-journey-in-the-ocean/':('สิ่งพิมพ์','ปฏิเสธ','','พลาสติก','ทะเลและมหาสมุทร','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/campaigns/Urban-Revolution/plastic-pollution/No-single-use-plastic/Top-10-sources-of-plastic-marine-debris/':('สิ่งพิมพ์','ปฏิเสธ','','พลาสติก','ทะเลและมหาสมุทร','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/plastic-cup-in-a-life-time/':('สิ่งพิมพ์','ปฏิเสธ','','พลาสติก','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/Lets-say-NO-to-single-use-plastic/':('สิ่งพิมพ์','ปฏิเสธ','','พลาสติก','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/what-is-microbeads/':('สิ่งพิมพ์','ปฏิเสธ','','พลาสติก','','','article','Migrate'),
            'https://www.greenpeace.org/seasia/th/press/reports/Crisis-of-Convenience/':('สิ่งพิมพ์','ปฏิเสธ','','พลาสติก','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/Teluk-Patani-Sustainable-Livelihood-and-CHIA/':('สิ่งพิมพ์','ปฏิเสธ','','ถ่านหิน','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/boom-and-bust-2018/':('สิ่งพิมพ์','ปฏิเสธ','','ถ่านหิน','สภาพภูมิอากาศ','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/Global-Shift/':('สิ่งพิมพ์','ปฏิเสธ','','ถ่านหิน','สภาพภูมิอากาศ','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/boom-and-bust-2017/':('สิ่งพิมพ์','ปฏิเสธ','','ถ่านหิน','สภาพภูมิอากาศ','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/Tueloe-Patani-Community-Health-Impact-Assessment/':('สิ่งพิมพ์','ปฏิเสธ','','ถ่านหิน','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/Nuclear-Scars/':('สิ่งพิมพ์','ปฏิเสธ','','นิวเคลียร์','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/Radiation-Reloaded/':('สิ่งพิมพ์','ปฏิเสธ','','นิวเคลียร์','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/lessons-from-fukushima/':('สิ่งพิมพ์','ปฏิเสธ','','นิวเคลียร์','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/Plant-Atlas/':('สิ่งพิมพ์','เปลี่ยนแปลง','','ระบบอาหาร','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/Less-Is-More/':('สิ่งพิมพ์','เปลี่ยนแปลง','','ระบบอาหาร','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/urban-farming/':('สิ่งพิมพ์','เปลี่ยนแปลง','','ระบบอาหาร','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/Pesticides-and-our-Health/':('สิ่งพิมพ์','เปลี่ยนแปลง','','ระบบอาหาร','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/Food-and-Farming-Vision/':('สิ่งพิมพ์','เปลี่ยนแปลง','','ระบบอาหาร','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/Twenty-Years-of-Failure/':('สิ่งพิมพ์','เปลี่ยนแปลง','','ระบบอาหาร','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/Krabi-goes-green/':('สิ่งพิมพ์','เปลี่ยนแปลง','','พลังงานหมุนเวียน','สภาพภูมิอากาศ','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/Renewable-Energy-Job-Creation-in-Thailand/':('สิ่งพิมพ์','เปลี่ยนแปลง','','พลังงานหมุนเวียน','สภาพภูมิอากาศ','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/annual-report-2016/':('สิ่งพิมพ์','กรีนพีซ','','เกี่ยวกับกรีนพีซ','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/annual-report-2015/':('สิ่งพิมพ์','กรีนพีซ','','เกี่ยวกับกรีนพีซ','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/annual-report-2014/':('สิ่งพิมพ์','กรีนพีซ','','เกี่ยวกับกรีนพีซ','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/annual-report-2013/':('สิ่งพิมพ์','กรีนพีซ','','เกี่ยวกับกรีนพีซ','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/annual-report-2012/':('สิ่งพิมพ์','กรีนพีซ','','เกี่ยวกับกรีนพีซ','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/annual-report-2011/':('สิ่งพิมพ์','กรีนพีซ','','เกี่ยวกับกรีนพีซ','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/annual-report-2010/':('สิ่งพิมพ์','กรีนพีซ','','เกี่ยวกับกรีนพีซ','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/annual-report-2009/':('สิ่งพิมพ์','กรีนพีซ','','เกี่ยวกับกรีนพีซ','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/reports/Greenpeace-Chronicles/':('สิ่งพิมพ์','กรีนพีซ','','เกี่ยวกับกรีนพีซ','','','article','Migrate'),
            #-------- Showing URLError: <urlopen error [Errno 8] nodename nor servname provided, or not known>
            #'http://www.greenpeace.org/seasia/th/press/releases/Greenpeace-statement-on-Thailand-Yellow-Card-sanction-lifting/':('ข่าวประชาสัมพันธ์','ปกป้อง','','ทะเลและมหาสมุทร','','','article','Migrate'),
            #'http://www.greenpeace.org/seasia/th/press/releases/greenpeace-condemns-japan-governments-sneaky-withdrawal-from-the-international-whaling-commission/':('ข่าวประชาสัมพันธ์','ปกป้อง','','ทะเลและมหาสมุทร','','','article','Migrate'),
            #'http://www.greenpeace.org/seasia/th/press/releases/greenpeace-condemns-japan-governments-reported-withdrawal-from-iwc/':('ข่าวประชาสัมพันธ์','ปกป้อง','','ทะเลและมหาสมุทร','','','article','Migrate'),
            #'http://www.greenpeace.org/seasia/th/press/releases/WCPFC-14/':('ข่าวประชาสัมพันธ์','ปกป้อง','','ทะเลและมหาสมุทร','','','article','Migrate'),
            #'http://www.greenpeace.org/seasia/th/press/releases/2018-world-air-quality-report/':('ข่าวประชาสัมพันธ์','ปกป้อง','','อากาศสะอาด','','','article','Migrate'),
            #'http://www.greenpeace.org/seasia/th/press/releases/who-air-pollution-data-a-call-to-action-to-ditch-fossil-fuels/':('ข่าวประชาสัมพันธ์','ปกป้อง','','อากาศสะอาด','','','article','Migrate'),
            #'https://www.greenpeace.org/seasia/th/press/releases/Wings-of-Paradise-world-th/':('ข่าวประชาสัมพันธ์','ปกป้อง','','ป่าไม้','','','article','Migrate'),
            #'http://www.greenpeace.org/seasia/th/press/releases/Plastic-prohibited-th/':('ข่าวประชาสัมพันธ์','ปฏิเสธ','','พลาสติก','','','article','Migrate'),
            #'https://www.greenpeace.org/seasia/th/press/releases/coca-cola-nestle-danone-mars-pepsi-and-unilever-sign-global-plastics-pledge-but-still-havent-prioritized-reduction/':('ข่าวประชาสัมพันธ์','ปฏิเสธ','','พลาสติก','','','article','Migrate'),
            #'https://www.greenpeace.org/seasia/th/press/releases/salt-platice-TH/':('ข่าวประชาสัมพันธ์','ปฏิเสธ','','พลาสติก','ทะเลและมหาสมุทร','','article','Migrate'),
            #'http://www.greenpeace.org/seasia/th/press/releases/Greenpeace-expedition-finds-plastic-pollution-and-hazardous-chemicals-in-remote-Antarctic-waters/':('ข่าวประชาสัมพันธ์','ปฏิเสธ','','พลาสติก','ทะเลและมหาสมุทร','','article','Migrate'),
            #'https://www.greenpeace.org/seasia/th/press/releases/thailand-brand-audit-result/':('ข่าวประชาสัมพันธ์','ปฏิเสธ','','พลาสติก','ทะเลและมหาสมุทร','','article','Migrate'),
            #'http://www.greenpeace.org/seasia/th/press/releases/23-countries-and-states-to-phase-out-coal-as-US432-billion-of-capital-leaves-the-industry/':('ข่าวประชาสัมพันธ์','ปฏิเสธ','','ถ่านหิน','สภาพภูมิอากาศ','','article','Migrate'),
            #'http://www.greenpeace.org/seasia/th/press/releases/Greenpeace-International-responds-to-nuclear-testing-conducted-by-North-Korea/':('ข่าวประชาสัมพันธ์','ปฏิเสธ','','นิวเคลียร์','','','article','Migrate'),
            #'http://www.greenpeace.org/seasia/th/press/releases/solar-fund/':('ข่าวประชาสัมพันธ์','เปลี่ยนแปลง','','พลังงานหมุนเวียน','สภาพภูมิอากาศ','','article','Migrate'),
        }

        start_urls = {
            # -------- Showing URLError: <urlopen error [Errno 8] nodename nor servname provided, or not known>
            'http://www.greenpeace.org/seasia/th/press/releases/Greenpeace-statement-on-Thailand-Yellow-Card-sanction-lifting/':('ข่าวประชาสัมพันธ์','ปกป้อง','','ทะเลและมหาสมุทร','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/greenpeace-condemns-japan-governments-sneaky-withdrawal-from-the-international-whaling-commission/':('ข่าวประชาสัมพันธ์','ปกป้อง','','ทะเลและมหาสมุทร','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/greenpeace-condemns-japan-governments-reported-withdrawal-from-iwc/':('ข่าวประชาสัมพันธ์','ปกป้อง','','ทะเลและมหาสมุทร','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/WCPFC-14/':('ข่าวประชาสัมพันธ์','ปกป้อง','','ทะเลและมหาสมุทร','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/2018-world-air-quality-report/':('ข่าวประชาสัมพันธ์','ปกป้อง','','อากาศสะอาด','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/who-air-pollution-data-a-call-to-action-to-ditch-fossil-fuels/':('ข่าวประชาสัมพันธ์','ปกป้อง','','อากาศสะอาด','','','article','Migrate'),
            'https://www.greenpeace.org/seasia/th/press/releases/Wings-of-Paradise-world-th/':('ข่าวประชาสัมพันธ์','ปกป้อง','','ป่าไม้','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/Plastic-prohibited-th/':('ข่าวประชาสัมพันธ์','ปฏิเสธ','','พลาสติก','','','article','Migrate'),
            'https://www.greenpeace.org/seasia/th/press/releases/coca-cola-nestle-danone-mars-pepsi-and-unilever-sign-global-plastics-pledge-but-still-havent-prioritized-reduction/':('ข่าวประชาสัมพันธ์','ปฏิเสธ','','พลาสติก','','','article','Migrate'),
            'https://www.greenpeace.org/seasia/th/press/releases/salt-platice-TH/':('ข่าวประชาสัมพันธ์','ปฏิเสธ','','พลาสติก','ทะเลและมหาสมุทร','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/Greenpeace-expedition-finds-plastic-pollution-and-hazardous-chemicals-in-remote-Antarctic-waters/':('ข่าวประชาสัมพันธ์','ปฏิเสธ','','พลาสติก','ทะเลและมหาสมุทร','','article','Migrate'),
            'https://www.greenpeace.org/seasia/th/press/releases/thailand-brand-audit-result/':('ข่าวประชาสัมพันธ์','ปฏิเสธ','','พลาสติก','ทะเลและมหาสมุทร','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/23-countries-and-states-to-phase-out-coal-as-US432-billion-of-capital-leaves-the-industry/':('ข่าวประชาสัมพันธ์','ปฏิเสธ','','ถ่านหิน','สภาพภูมิอากาศ','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/Greenpeace-International-responds-to-nuclear-testing-conducted-by-North-Korea/':('ข่าวประชาสัมพันธ์','ปฏิเสธ','','นิวเคลียร์','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/th/press/releases/solar-fund/':('ข่าวประชาสัมพันธ์','เปลี่ยนแปลง','','พลังงานหมุนเวียน','สภาพภูมิอากาศ','','article','Migrate'),
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


        #date_field = response.css('div.news-list .caption::text').re_first(r' - \s*(.*)')
        #date_field = extract_with_css('div.news-list .caption '),

        # Added only for Thai migration.
        date_field = response.xpath('string(//div[@class="news-list"]/ul/li/*/*/span[@class="caption"])').extract()[0]
        date_field = date_field[date_field.find('--'):]

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
            date_field = date_field.replace(" ที่ ", " ")  # Thai

            date_field = dateutil.parser.parse(date_field)
            date_field = self.parse_thai_date(date_field)   # added only for Thia migration.

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
            date_field = date_field.replace(" na ", " ") #slovenian
        except IndexError:
            date_field = ""

        if date_field:
            date_field = dateutil.parser.parse(date_field)
            date_field = self.parse_thai_date(date_field)

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
            'author': 'Greenpeace Thailand',
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

        month_th_en = {
            'มกราคม': 'January',
            'กุมภาพันธ์': 'February',
            'มีนาคม': 'March',
            'เมษายน': 'April',
            'พฤษภาคม': 'May',
            'มิถุนายน': 'June',
            'กรกฎาคม': 'July',
            'สิงหาคม': 'August',
            'กันยายน': 'September',
            'ตุลาคม': 'October',
            'พฤศจิกายน': 'November',
            'ธันวาคม': 'December',
        }

        # Replace the Thai month name with english month name.
        for th_month, en_month in month_th_en.iteritems():
            month_name = month_name.replace(th_month, en_month)

        return month_name;

    def csv_writer(self, data, path):
        # Write data to a CSV file path
        with open(path, "a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(data)

    # parse the Thai date format.
    def parse_thai_date(self, date_info):
        buddhist_year = date_info.year
        if (buddhist_year > 2540):
            date_info = date_info - relativedelta(years=543)

        return date_info
