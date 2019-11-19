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
        'FEED_URI': 'gpea_staging_v1.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    __connector_csv_filename = "connector_v2_final_.csv"
    __connector_csv_log_file = "connector_csv_log_v2"

    def start_requests(self):

        # V1
        start_urls = {
            # B1
            'http://www.greenpeace.org/eastasia/publications/reports/climate-energy/2019/mindworks-part1/':('Publication','Live Sustainably','','Climate Impacts','consumption','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/publications/reports/climate-energy/2019/mindworks-part2/':('Publication','Live Sustainably','','Climate Impacts','consumption','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/publications/annual-reports/2018/':('Publication','About Greenpeace','','AboutUs','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/20181/Electricity-consumption-from-Chinas-internet-industry-to-increase-by-two-thirds-by-2023-Greenpeace-/':('Press','Climate & Energy','','Renewable Energy','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/toxics/2019/with-poor-oversight-Chinas-industrial-parks/':('Press','Live Sustainably','','Detox','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/toxics/2019/Global-protests-push-Samsung-to-finally-recycle-Galaxy-Note-7---Greenpeace1/':('Press','Live Sustainably','','Detox','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/toxics/2019/Cash-strapped-cities-in-China-greenlight-toxic-land-for-development/':('Press','Live Sustainably','','Detox','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/stories/oceans/2019/why-we-need-a-Global-Ocean-Treaty/':('Story','Protect Nature','','Oceans','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/stories/oceans/2019/five-jaw-dropping-facts-about-sharks/':('Story','Protect Nature','','Oceans','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/top-5-trends-hopes-up-on-climate/blog/62140/':('Blog','Live Sustainably','','Climate Impacts','consumption','','news-list','Migrate'),
            # 'http://www.greenpeace.org/eastasia/magazines/issue12/':('Publication','About Greenpeace','','AboutUs','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/publications/annual-reports/2017/':('Publication','About Greenpeace','','AboutUs','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2018/As-Huawei-seeks-to-enter-US-market-climate-commitment-sorely-lacking---Greenpeace/':('Press','Climate & Energy','','Renewable Energy','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2018/PM25-in-Beijing-down-54-nationwide-air-quality-improvements-slow-as-coal-use-increases/':('Press','Live Sustainably','','Reduce Air Pollution','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2018/Glacial-lake-in-western-China-bursts-annual-average-temperatures-in-area-up-2-to-3-C-since-1961/':('Press','Climate & Energy','','Climate Impacts','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2018/Greenpeace-survey-reveals-impact-of-climate-change-on-glaciers-in-China/':('Press','Climate & Energy','','Climate Impacts','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/oceans/2018/Oil-tanker-carrying-1-million-barrels-of-oil-on-fire-off-China-coast---Greenpeace-response/':('Press','Climate & Energy','','','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/oceans/2018/Taiwanese-seafood-giant-linked-to-human-rights-violations---Greenpeace/':('Press','Protect Nature','','Ocean','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/toxics/2018/Taipei-City-Marathon-pledges-green-for-its-first-ever-sustainable-event1/':('Press','Live Sustainably','','Plastic','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/stories/about/2018/edxed/':('Story','About Greenpeace','','AboutUs','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/stories/forests/2018/dirty-palm-oil/':('Story','Protect Nature','','Forest','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/stories/oceans/2018/plastic-free-future/':('Story','Protect Nature','','Oceans','Plastic','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/stories/toxics/2018/consumer-revolution/':('Story','Live Sustainably','','consumption','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/beyond-the-beach-clean-up/blog/62035/':('Blog','Protect Nature','','Oceans','Plastic','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/why-in-a-post-ipcc-world-we-need-more-from-ou/blog/61987/':('Blog','Climate & Energy','','Renewable Energy','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/change-can-come-from-all-of-us-greenpeace-chi/blog/61756/':('Blog','About Greenpeace','','AboutUs','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/you-did-it-samsung-chooses-renewable-energy/blog/61622/':('Blog','Climate & Energy','','Renewable Energy','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/in-china-a-wave-of-support-for-antarctic-prot/blog/61429/':('Blog','Protect Nature','','Oceans','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/making-change-in-2018/blog/61133/':('Blog','Live Sustainably','','consumption','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/will-chinese-tech-giant-huawei-dethrone-apple/blog/60980/':('Blog','Live Sustainably','','Detox','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/rethinking-it-saving-the-world-one-gadget-at-/blog/59772/':('Blog','Live Sustainably','','Detox','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/powering-up-meet-the-women-electrifying-china/blog/58885/':('Blog','Climate & Energy','','Renewable Energy','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/drought-ground-collapse-and-forced-migration-/blog/55957/':('Blog','Live Sustainably','','Detox','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/toxics/2017/Chinas-ban-on-imports-of-24-types-of-waste-is-a-wake-up-call-to-the-world---Greenpeace/':('Press','Live Sustainably','','Detox','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/forests/2017/Land-fill-project-in-eastern-China-threatens-survival-of-critically-endangered-spoon-billed-sandpiper---Greenpeace-report/':('Press','Protect Nature','','Biodiversity','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/publications/reports/forests/2017/Jiangsus-Vanishing-Wetlands-Report/':('Publication','Protect Nature','','Biodiversity','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/20-years-of-golden-greenpeace-memories/blog/60874/':('Blog','About Greenpeace','','AboutUs','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/what-does-the-good-life-mean-to-you/blog/60872/':('Blog','Live Sustainably','','Renewable Energy','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/7-moments-from-greenpeace-in-1997/blog/60869/':('Blog','About Greenpeace','','AboutUs','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/for-a-greenpeace-of-mind/blog/60770/':('Blog','Live Sustainably','','Consumption','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/china-has-a-big-overfishing-problem/blog/60635/':('Blog','Protect Nature','','Oceans','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/toxics/2017/2016-Singles-Day-clothing-sales-produce-258000-tonnes-of-CO2-emissions-Greenpeace/':('Press','Live Sustainably','','Consumption','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/5-reasons-why-coal-is-on-the-way-out/blog/60542/':('Blog','Climate & Energy','','Coal','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2017/Green-bond-financed-coal-to-chemical-plant-in-China-will-emit-millions-of-tons-of-CO2---Greenpeace/':('Press','Climate & Energy','','Coal','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/pushing-from-the-grassroots-up/blog/60014/':('Blog','Climate & Energy','','Renewable Energy','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/huge-win-for-chinas-green-peafowl/blog/59974/':('Blog','Protect Nature','','Biodiversity','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2017/Cutting-Chinas-redundant-coal-power-capacity-would-provide-enough-water-for-27-million-people-in-water-stressed-areas/':('Press','Climate & Energy','','Coal','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/stories/about/2017/create-worry-free-world/':('Story','About Greenpeace','','AboutUs','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/stories/about/2017/how-we-making-history-with-you/':('Story','About Greenpeace','','AboutUs','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/oceans/2017/Almost-one-third-of-Chinas-annual-fisheries-catch-is-trash-fish---Greenpeace/':('Press','Protect Nature','','Oceans','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/meet-the-self-styled-pv-doctor-who-brought-so/blog/59925/':('Blog','Climate & Energy','','Renewable Energy','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/a-coal-merchant-and-his-son/blog/59861/':('Blog','Climate & Energy','','Renewable Energy','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/forests/2017/Illegal-mining-discovered-in-Chinas-last-remaining-green-peafowl-habitat---Greenpeace/':('Press','Protect Nature','','Forest','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/publications/reports/toxics/2017/How-Repairable-is-Your-Mobile-Device/':('Publication','Live Sustainably','','Detox','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2017/Belt-and-Road-participants-call-for-full-implementation-of-Paris-Agreement/':('Press','Climate & Energy','','Coal','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/5-ways-tech-companies-are-making-your-devices/blog/59729/':('Blog','Live Sustainably','','Detox','Consumption','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/toxics/2017/Apple-Samsung-products-among-least-repairable-in-new-Greenpeace-assessment-of-tech-brands/':('Press','Live Sustainably','','Detox','Consumption','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/toxics/2017/Nearly-half-of-Chinese-provinces-miss-water-targets-85-of-Shanghais-river-water-not-fit-for-human-contact/':('Press','Live Sustainably','','Detox','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/toxics/2017/Cocktail-of-chemicals-being-released-from-Lianyungang-Chemical-Industrial-Park---Greenpeace-investigation/':('Press','Live Sustainably','','Detox','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/forest-guardians-the-communities-living-on-th/blog/58994/':('Blog','Protect Nature','','Forest','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/others/2017-/Sustainability-should-be-priority-for-Chinas-Belt-and-Road--Greenpeace/':('Press','Climate & Energy','','Coal','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/shopping-doesnt-make-us-happy/blog/59348/':('Blog','Live Sustainably','','Consumption','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2017/CO2-emissions-from-Chinas-coal-to-chemical-industry-could-increase-400-over-13th-Five-Year-Plan-period/':('Press','Climate & Energy','','Coal','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/publications/reports/climate-energy/climate-energy-2017/Estimating-Carbon-Emissions-from-Chinas-Coal-to-Chemical-Industry-during-the-13th-Five-year-Plan-Period/':('Publication','Climate & Energy','','Coal','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2017/By-2030-Chinas-wind-and-solar-industry-could-replace-fossil-energy-sources-to-the-tune-of-300-million-tonnes-of-standard-coal-per-year/':('Press','Climate & Energy','','Renewable Energy','Coal','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/my-night-on-board-a-chinese-fishing-vessel-in/blog/59184/':('Blog','Protect Nature','','Oceans','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/you-did-it-samsung-will-finally-recycle-milli/blog/59053/':('Blog','Live Sustainably','','Detox','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/toxics/2017/Global-protests-push-Samsung-to-finally-recycle-Galaxy-Note-7---Greenpeace/':('Press','Live Sustainably','','Detox','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/three-things-rex-tillerson-should-learn-from-/blog/58983/':('Blog','Climate & Energy','','Renewable Energy','Coal','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2017/Despite-claims-of-cuts-China-sees-steel-capacity-increase-in-2016-air-quality-to-suffer---Greenpeace/':('Press','Climate & Energy','','Coal','Reduce Air Pollution','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2017/China-forecasts-fourth-year-of-stable-or-declining-CO2-emissions-as-world-awaits-Trump-climate-action---Greenpeace/':('Press','Climate & Energy','','Coal','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/friday-five-chinas-burning-problem-and-coal-t/blog/58819/':('Blog','Climate & Energy','','Coal','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/toxics/2017/ovc-hk-spending-25-billion/':('Press','Live Sustainably','','Consumption','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/toxics/2017/Samsung-fails-to-share-a-plan-to-deal-with-43-million-Galaxy-Note-7---Greenpeace/':('Press','Live Sustainably','','Detox','Consumption','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2017/Cancelling-new-coal-plants-in-Southeast-Asia-Korea-Japan-would-save-50000-lives-a-year/':('Press','Climate & Energy','','Coal','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2017/China-raises-hopes-for-continued-climate-change-action-at-Davos---Greenpeace/':('Press','Climate & Energy','','Coal','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2017/Almost-three-quarters-of-Chinese-cities-yet-to-reach-air-quality-national-standards-Greenpeace/':('Press','Climate & Energy','','Coal','Reduce Air Pollution','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/5-chinese-artivists-that-took-on-chinas-air-p/blog/58468/':('Blog','Live Sustainably','','Reduce Air Pollution','Coal','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2017/China-releases-its-energy-sector-development-13th-five-year-plan-Greenpeace-response/':('Press','Climate & Energy','','Coal','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/good-news-we-shut-down-illegal-mining-in-chin/blog/58375/':('Blog','Protect Nature','','Forest','Biodiversity','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/460-million-people-in-china-are-choking-under/blog/58343/':('Blog','Live Sustainably','','Reduce Air Pollution','Coal','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2016/Smog-engulfs-area-home-to-460-million-citizens-as-Northern-China-sees-worst-air-pollution-of-2016---Greenpeace/':('press','Live Sustainably','','Reduce Air Pollution','Coal','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/red-alert-whats-happening-with-beijings-air-p/blog/58325/':('Blog','Live Sustainably','','Reduce Air Pollution','Coal','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2016/Beijings-first-air-pollution-red-alert-of-2016-coal-burning-the-culprit---Greenpeace/':('Press','Live Sustainably','','Reduce Air Pollution','Coal','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/toxics/2016/China-averaged--29-chemical-accidents-per-month-so-far-this-year---Greenpeace/':('Press','Live Sustainably','','Detox','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/samsung-its-time-for-you-to-share-your-plan-t/blog/58208/':('Blog','Live Sustainably','','Detox','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/singles-day-is-a-disaster-for-our-pockets-and/blog/57973/':('Blog','Live Sustainably','','Consumption','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/from-student-environmentalist-to-solar-pionee/blog/58029/':('Blog','Climate & Energy','','Renewable Energy','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2016/heavy-metal-content-falls/':('Publication','Climate & Energy','','Coal','Reduce Air Pollution','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/the-startup-heroes-of-chinas-renewables-revol/blog/57957/':('Blog','Climate & Energy','','Renewable Energy','','','news-list','Migrate'),
            # 'http://www.greenpeace.org/eastasia/news/blog/the-startup-heroes-of-chinas-renewables-revol/blog/57957/':('Blog','Climate & Energy','','Renewable Energy','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/will-43-million-samsung-galaxy-note-7-phones-/blog/57890/':('Blog','Live Sustainably','','Detox','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/toxics/2016/samsung-phones/':('Press','Live Sustainably','','Detox','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/shaking-up-chinas-food-system-in-shanghai-and/blog/57846/':('Blog','Live Sustainably','','Food','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2016/Xian-Environmental-Protection-Bureau-caught-tampering-with-air-quality-readings---Greenpeace-response/':('Press','Live Sustainably','','Reduce Air Pollution','Coal','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/oceans/2016/Greenpeace-finds-microplastics-in-all-5-leading-cosmetic-retailers--Inadequate-labelling-found-in-almost-50-of-products/':('Press','Live Sustainably','','oceans','Plastic','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/microbeads-how-did-companies-respond/blog/57339/':('Blog','Live Sustainably','','Plastic','consumption','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/how-can-we-avoid-microbeads-in-hong-kong/blog/57683/':('Blog','Live Sustainably','','Plastic','consumption','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/g20-is-over-now-its-time-for-action/blog/57440/':('Blog','Climate & Energy','','Climate Impacts','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/why-were-mapping-chinas-hazardous-chemicals-f/blog/57555/':('Blog','Live Sustainably','','Detox','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/pushing-brands-to-detox-another-domino-has-fa/blog/57610/':('Blog','Live Sustainably','','Detox','','','news-list','Migrate'),

            # B2
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2016/Greenpeace-urges-G20-governments-to-bring-Paris-Agreement-into-force-this-year/':('Press','Climate & Energy','','Climate Impacts','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/illegal-logging-panda/blog/54513/':('Blog','Protect Nature','','Biodiversity','Forest','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/chinas-toxic-school-was-just-the-tip-of-the-i/blog/56348/':('Blog','Live Sustainably','','Detox','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/which-country-is-most-likely-to-repair-their-/blog/57275/':('Blog','Live Sustainably','','Detox','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2016/Over-1-trillion-rmb-wasted-coal-power-China/':('Press','Climate & Energy','','Coal','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/which-fashion-brands-are-going-toxic-free/blog/56947/':('Blog','Live Sustainably','','Detox','Consumption','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/others/20161/Greenpeace-releases-Hong-Kong-and-Taiwan-consumer-report-/':('Press','Live Sustainably','','Consumption','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/others/20161/Greenpeace-Urges-Hong-Kong-Residents-to-Buy-Smart-Buy-Less/':('press','Live Sustainably','','Consumption','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2016/Greenpeace-East-Asia-responds-to-IEA-report-on-Energy-and-Air-Pollution/':('press','Climate & Energy','','Coal','Reduce Air Pollution','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2016/Greenpeace-demands-suspension/':('press','Climate & Energy','','','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/wen-fang-maskbook/blog/56686/':('Blog','Climate & Energy','','Reduce Air Pollution','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/toxics/2016/China-releases-its-first-ever-soil-pollution-prevention-plan-Greenpeace-response/':('Press','Live Sustainably','','Detox','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/6-examples-of-chinas-amazing-biodiversity/blog/56508/':('Blog','Protect Nature','','Biodiversity','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/campaigns/forests/problems/':('Blog','Protect Nature','','Forest','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/campaigns/forests/problems/china-remaining-forests/':('Blog','Protect Nature','','Forest','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/5-species-bouncing-back-from-the-brink-of-ext/blog/55726/':('Blog','Protect Nature','','Biodiversity','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/publications/reports/climate-energy/2016/Coal-Power-Bubble-2/':('Publication','Climate & Energy','','Coal','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/on-world-forests-day-were-celebrating-the-con/blog/55936/':('Blog','Protect Nature','','Forest','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/toxics/2016/More-than-80-of-shallow-groundwater-wells-in-China-unfit-for-human-use-Greenpeace-reaction/':('press','Live Sustainably','','Detox','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/toxics/2016/15000-people-and-key-Yangtze-River-ecosystem-areas-in-close-proximity-to-Jiangsu-Deqiao-Chemical-Storage-facility-fire-Greenpeace/':('press','Live Sustainably','','Detox','','','article','Migrate'),
            # 'http://www.greenpeace.org/eastasia/press/releases/toxics/2016/15000-people-and-key-Yangtze-River-ecosystem-areas-in-close-proximity-to-Jiangsu-Deqiao-Chemical-Storage-facility-fire-Greenpeace/':('press','Live Sustainably','','Detox','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/china-air-pollution-heading-west/blog/56213/':('Blog','Live Sustainably','','Reduce Air Pollution','Coal','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2016/As-eastern-Chinas-air-quality-improves-rapidly-69-cities-in-central-and-western-China-see-air-quality-deteriorating--Greenpeace/':('press','Live Sustainably','','Reduce Air Pollution','Coal','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/publications/reports/forests/2015/report-illegal-logging-sichuan/':('Publication','Protect Nature','','Forest','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/toxics/2016/Pollution-linked-to-cases-of-cancer-in-Changzhou-middle-school--Greenpeace-response/':('press','Live Sustainably','','Detox','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2016/Data-shows-Chinas-economy-is-breaking-free-from-coal---Greenpeace/':('press','Climate & Energy','','Coal','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/China-glyphosate-carcinogenic/blog/53446/':('Blog','Live Sustainably','','Food','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/china-should-seek-inspiration-from-paris-to-r/blog/56079/':('Blog','Protect Nature','','oceans','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/seeds-of-change-cadmium-rice/blog/52829/':('Blog','Live Sustainably','','Food','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/publications/reports/climate-energy/2016/Boom-and-Bust-2016/':('Publication','Climate & Energy','','Coal','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/world-food-day-farmers/blog/54449/':('Blog','Live Sustainably','','Food','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2016/China-begins-to-suspend-coal-fired-power-plant-approvals-Greenpeace-response/':('press','Climate & Energy','','Coal','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/publications/reports/climate-energy/2016/How-the-Coal-Industry-is-Aggravating-the-Global-Water-Crisis/':('Publication','Climate & Energy','','Coal','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2016/45-of-Chinas-coal-fired-power-plants-in-areas-of-water-over-withdrawal-Greenpeace/':('press','Climate & Energy','','Coal','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/opportunity-knocks/blog/54874/':('Blog','Protect Nature','','Forest','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2016/Chinas-13th-Five-Year-Plan-hints-at-stronger-climate-ambition---Greenpeace/':('press','Climate & Energy','','Coal','Climate Impact','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/7-reasons-to-claim-water-for-life-not-for-coa/blog/50466/':('Blog','Climate & Energy','','Coal','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/others/20161/Greenpeace-response-to-the-Chinese-governments-MEP-press-conference/':('press','About Greenpeace','','AboutUs','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/food-agriculture/2015/93-GE-corn-contamination/':('press','Live Sustainably','','Food','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/food-agriculture/2016/ChinaChem-to-takeover-Syngenta---Greenpeace-statement/':('press','Live Sustainably','','Food','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/china-releases-tianjin-report-but-questions-a/blog/55496/':('Blog','Live Sustainably','','Detox','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/toxics/2015/buy-nothing-day/':('press','Live Sustainably','','Detox','Consumption','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/toxics/2016/Greenpeace-reaction-to-the-State-Council-investigation-report-on-the-Tianjin-Blasts/':('Press','Live Sustainably','','Detox','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/contamination-on-the-great-north-eastern-plai/blog/55234/':('Blog','Live Sustainably','','Food','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2016/Q4-City-Rankings-2015/':('Press','Live Sustainably','','Reduce Air Pollution','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/publications/reports/climate-energy/2016/clean-air-action/':('Publication','Live Sustainably','','Reduce Air Pollution','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/publications/reports/climate-energy/2016/coal-power-bubble-update/':('Publication','Climate & Energy','','Coal','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2016/Greenpeace-In-spite-of-Chinas-overcapacity-crisis-210-new-coal-fired-power-plants-received-environmental-permits-in-2015/':('Press','Climate & Energy','','Coal','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2016/Chinas-CO2-emissions-continued-to-fall-in-2015--Greenpeace-response/':('Press','Climate & Energy','','Coal','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/publications/reports/climate-energy/climate-energy-2015/Pipe-Dreams-/':('Publication','Climate & Energy','','Coal','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/year-in-year-out-let-there-be-fish/blog/55497/':('Blog','Protect Nature','','oceans','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/blasts-tianjin/blog/55179/':('Blog','Live Sustainably','','Detox','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2015/suspected-illegal-construction/':('press','Climate & Energy','','Coal','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/friday-five-january-22/blog/55365/':('Blog','Live Sustainably','','Coal','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/publications/reports/climate-energy/2016/city-rankings-2015-Q4/':('publication','Live Sustainably','','Reduce Air Pollution','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/bad-to-worse-ranking-74-chinese-cities-by-air/blog/48181/':('Blog','Live Sustainably','','Reduce Air Pollution','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/367-shades-of-grey-why-china-needs-a-coal-cap/blog/54429/':('Blog','Climate & Energy','','Coal','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/bearing-witness-drone/blog/53201/':('Blog','Live Sustainably','','Detox','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/we-did-it-victory-for-chinas-giant-pandas/blog/55262/':('Blog','Protect Nature','','Biodiversity','Forest','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2015/China-declares-no-new-coal-mines-for-next-three-years---Greenpeace-response1/':('Press','Climate & Energy','','Coal','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/publications/reports/food-agriculture/2015/GPEAs-discovery-of-illegal-GE-corn-in-the-corn-supply-chain-in-north-east-China/':('Press','Live Sustainably','','Food','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/the-affect-of-steve-jobs-on-the-lives-of-impo/blog/37331/':('Blog','Live Sustainably','','Detox','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/publications/reports/climate-energy/climate-energy-2015/coal-power-overcapacity/':('publication','Climate & Energy','','Coal','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/wildlife-crime/blog/55146/':('press','Live Sustainably','','Reduce Air Pollution','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2015/COP21-Hong-Kong-Nuclear/':('press','Climate & Energy','','','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/red-alert/blog/54935/':('Blog','Live Sustainably','','Reduce Air Pollution','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/forests/2015/Greenpeace-China-could-lead-global-fight-against-illegal-logging-in-the-Congo-Basin/':('press','Protect Nature','','Forest','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/publications/reports/forests/2015/opportunity-knocks/':('publication','Protect Nature','','Forest','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2015/Greenpeace-report-estimates-13th-Five-Year-Plan-period-could-see-700-billion-RMB-wasted-on-coal-fired-electricity/':('press','Climate & Energy','','Coal','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/publications/reports/climate-energy/climate-energy-2015/doubling-down/':('publication','Climate & Energy','','Coal','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2015/Greenpeace-Despite-falling-coal-consumption-China-could-add-as-many-as-four-idle-coal-power-plants-per-week/':('press','Climate & Energy','','Coal','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2015/Greenpeace-Response-to-China-France-Joint-Statement-on-Climate-Change/':('press','Climate & Energy','','','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/forests/2015/illegal-logging-sichuan/':('press','Protect Nature','','Forest','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/you-are-what-you-eat/blog/54183/':('Blog','Live Sustainably','','Food','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/rainbow-warrior-illegal-fishing-pacific/blog/54109/':('Blog','Protect Nature','','oceans','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/taking-the-law-lightly/blog/54099/':('Blog','Climate & Energy','','Coal','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/no-PFCs/blog/54060/':('Blog','Live Sustainably','','Detox','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/hazardous-chemicals-remote/blog/54031/':('Blog','Live Sustainably','','Detox','','','news-list','Migrate'),
            # 'http://www.greenpeace.org/eastasia/news/blog/hazardous-chemicals-remote/blog/54031/':('Press','Live Sustainably','','Detox','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/searching-for-blue/blog/53975/':('Blog','Live Sustainably','','Reduce Air Pollution','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/Tianjin-blast-response/blog/53955/':('Blog','Live Sustainably','','Detox','','','news-list','Migrate'),
            # 'http://www.greenpeace.org/eastasia/news/blog/Tianjin-blast-response/blog/53955/':('Blog','Live Sustainably','','Detox','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/toxics/2015/Tianjin-blast-update-satellite-images-of-blast-site-/':('press','Live Sustainably','','Detox','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/toxics/2015/Tianjin-blast-update-Greenpeace-East-Asia-investigates-factories-in-Tianjin-port/':('press','Live Sustainably','','Detox','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/Tianjin-blast/blog/53831/':('Blog','Live Sustainably','','Detox','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/toxics/2015/Update-Greenpeaces-Independent-Testing-for-Sodium-Cyanide-in-Tianjin/':('press','Live Sustainably','','Detox','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/toxics/2015/Tianjin-Blast-Update-Comments-on-current-hazardous-chemicals-policies-and-their-implementation/':('press','Live Sustainably','','Detox','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/toxics/2015/Tianjin-blast-update-authorities-evacuate-area-surrounding-blast-site/':('press','Live Sustainably','','Detox','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/the-beautiful-beast-world-elephant-day/blog/53772/':('Blog','protect Nature','','Biodiversity','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/oceans/2015/BREAKING---Standard-Chartered-ditches-giant-coal-mine-threatening-Great-Barrier-Reef/':('press','protect Nature','','oceans','Coal','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/searching-for-shangri-la-conscientious-villag/blog/53717/':('Blog','Live Sustainably','','Detox','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/Shangri-la-rules-5000m/blog/53625/':('Blog','Live Sustainably','','Detox','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/falling-fast/blog/53580/':('Blog','Live Sustainably','','Reduce Air Pollution','Coal','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/searching-for-shangri-la-return-to-haba-snow-/blog/53533/':('Blog','Live Sustainably','','Detox','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2015/Greenpeace-Jiangsu-a-potential-leader-of-Chinas-energy-revolution/':('press','Climate & Energy','','Renewable Energy','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2015/China-submits-post-2020-climate-targets/':('press','Climate & Energy','','','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/china-long-march-paris/blog/53402/':('Blog','Climate & Energy','','','','','news-list','Migrate'),
            # 'http://www.greenpeace.org/eastasia/press/releases/climate-energy/2015/China-submits-post-2020-climate-targets/':('press','Climate & Energy','','','','','article','Migrate'),
            'http://www.greenpeace.org/eastasia/news/blog/INDC-China/blog/53341/':('Blog','Climate & Energy','','','','','news-list','Migrate'),
            'http://www.greenpeace.org/eastasia/press/releases/oceans/2015/choose-coral-not-coal/':('press','Climate & Energy','','Coal','','','article','Migrate'),
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
                # body_text = body_text + response.xpath(' //*[@id="content"]/div[4]/div/div[2]/p').extract_first()

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
            'author': 'Greenpeace East Asia',
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
            'Ocak': 'January',
            'ינואר': 'January',
            'Şubat': 'February',
            'פברואר': 'February',
            'מרץ': 'March',
            'אפריל': 'April',
            'Mayıs': 'May',
            'מאי': 'May',
            'יוני': 'June',
            'יולי': 'July',
            'אוגוסט': 'August',
            'ספטמבר': 'September',
            'אוקטובר': 'October',
            'Kasım': 'November',
            'נובמבר': 'November',
            'דצמבר': 'December',
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
