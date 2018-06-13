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
        'FEED_URI': 'gpca_staging_v2_FR_B2.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    __connector_csv_filename = "connector_v2_final.csv"
    __connector_csv_log_file = "connector_csv_log_v2_final"

    def start_requests(self):

        #v1
        '''
        start_urls = {
            # Story
            # - 1st batch
            'http://www.greenpeace.org/canada/en/Blog/what-the-oil-industry-wants-the-harper-govern/blog/43617/':('Story','Transform Energy','Oil','Indigenous','Migrate'),
            'http://www.greenpeace.org/canada/en/Blog/why-enbridge-is-afraid-of-takaiya-blaney/blog/33920/':('Story','Transform Energy','Oil','Indigenous','Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/12-totally-awesome-eco-friendly-and-affordabl/blog/58342/':('Story','Live Sustainably','Consumption','','Migrate'),
            'http://www.greenpeace.org/canada/en/Blog/golden-rice-the-true-story/blog/42223/':('Story','Live Sustainably','Food','Health','Migrate'),

            # Press Release
            # - 1st batch
            'http://www.greenpeace.org/canada/en/Press-Center/2018/Banking-giant-HSBC-rules-out-financing-controversial-Keystone-XL-pipeline-/':('Press Release','Transform Energy','Oil','','Migrate'),
            'http://www.greenpeace.org/canada/en/Press-Center/2017/clyde-river-suprem-court/':('Press Release','Transform Energy','Oil','Indigenous','Migrate'),
            'http://www.greenpeace.org/canada/en/Press-Center/2017/PRESS-RELEASE---Greenpeace-slams-Coca-Cola-plastic-announcement-as-dodging-the-main-issue-More-plastic-production-means-more-ocean-plastic-pollution/':('Press Release','Live Sustainably','Consumption','','Migrate'),
            'http://www.greenpeace.org/canada/en/Press-Center/2017/PRESS-RELEASE-Dutch-Bank-ING-the-latest-to-reject-financing-of-Kinder-Morgan-pipeline/':('Press Release','Transform Energy','Oil','Victory','Migrate'),
            'http://www.greenpeace.org/canada/en/Press-Center/2018/PRESS-RELEASE-120-personalities-and-organizations-in-Quebec-call-for-an-emergency-mobilization-against-the-expansion-of-the-Kinder-Morgan-pipeline---/':('Press Release','Transform Energy','Oil','','Migrate'),
            'http://www.greenpeace.org/canada/en/Press-Center/2017/STATEMENT---Greenpeace-reaction-to-Desjardins-moratorium-on-pipeline-financing/':('Press Release','Transform Energy','Oil','','Migrate'),
        }
        '''

        # v2
        start_urls = {
            # English
            'http://www.greenpeace.org/canada/en/Blog/what-the-oil-industry-wants-the-harper-govern/blog/43617/': ('Story', 'Transform Energy', 'Oil', 'Indigenous', 'Migrate'),
            'http://www.greenpeace.org/canada/en/Blog/why-enbridge-is-afraid-of-takaiya-blaney/blog/33920/': ('Story', 'Transform Energy', 'Oil', 'Indigenous', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/12-totally-awesome-eco-friendly-and-affordabl/blog/58342/': ('Story', 'Live Sustainably', 'Consumption', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/Blog/golden-rice-the-true-story/blog/42223/': ('Story', 'Live Sustainably', 'Food', 'Health', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/how-the-federal-parties-rate-on-climate/blog/54339/': ('Story', 'Protect Nature', 'Climate', 'EnergySolutions', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/where-does-greenpeace-stand-on-seal-hunting/blog/55360/': ('Story', 'Protect Nature', 'Arctic', 'Indigenous', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/greenpeace-and-the-sisiutl-cultural-appropria/blog/54565/': ('Story', 'Protect Nature', 'Ships', 'Indigenous', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/dont-let-greenpeace-disappear/blog/59421/': ('Story', 'Protect Nature', 'Forests', 'PeacefulProtest', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/building-a-solar-dream-in-a-tar-sands-nightma/blog/54190/': ('Story', 'Transform Energy', 'Oil', 'EnergySolutions', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/share-your-photos-of-cokes-plastic-pollution/blog/59528/': ('Story', 'Live Sustainably', 'Consumption', 'Oceans', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/so-loud-it-can-kill-a-whale/blog/57367/': ('Story', 'Protect Nature', 'Arctic', 'Indigenous', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/clyde-river-wins-case-at-the-supreme-court-of/blog/59937/': ('Story', 'Protect Nature', 'Indigenous', 'Victory', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/share-your-pics-of-ridiculous-packaging/blog/61347/': ('Story', 'Live Sustainably', 'Consumption', 'Food', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/bc-finds-kinder-morgans-achilles-heel/blog/61101/': ('Story', 'Transform Energy', 'Oil', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/100-authors-around-the-world-stand-with-green/blog/59521/': ('Story', 'Protect Nature', 'Forests', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/victory-people-power-just-stopped-another-pip/blog/60381/': ('Story', 'Transform Energy', 'Oil', 'Victory', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/youre-closer-than-you-think-nuclear-threats-o/blog/59826/': ('Story', 'Transform Energy', 'Nuclear', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/tell-td-to-dump-kinder-morgan/blog/59334/': ('Story', 'Transform Energy', 'Oil', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/greenpeaces-new-open-project-your-plastic-fre/blog/61399/': ('Story', 'Live Sustainably', 'Consumption', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/greenpeace-heads-to-supreme-court-to-defend-p/blog/61147/': ('Story', 'Transform Energy', 'Oil', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/plastic-pollution-why-coca-cola-bears-respons/blog/59398/': ('Story', 'Live Sustainably', 'Consumption', 'Oceans', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/tiny-houses-take-on-big-banks/blog/60183/': ('Story', 'Live Sustainably', 'EnergySolutions', 'Oil', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/2017-tuna-ranking-reveals-more-green-tuna-pro/blog/59794/': ('Story', 'Live Sustainably', 'Food', 'Oceans', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/5-reasons-why-we-were-outside-coca-colas-hq/blog/59191/': ('Story', 'Live Sustainably', 'Consumption', 'Oceans', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/my-week-on-a-plastic-beach-calling-out-pollut/blog/60367/': ('Story', 'Live Sustainably', 'Consumption', 'Oceans', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/can-a-nuclear-accident-happen-in-canada-quest/blog/33777/': ('Story', 'Transform Energy', 'Nuclear', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/indigenous-leaders-and-supporters-to-take-bol/blog/61277/': ('Story', 'Transform Energy', 'Oil', 'Indigenous', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/top-10-solar-facts/blog/56834/': ('Story', 'Transform Energy', 'EnergySolutions', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/q-a-why-campaign-against-td-bank-over-tar-san/blog/60293/': ('Story', 'Transform Energy', 'Oil', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/10000-people-stand-strong-to-protectthepacifi/blog/61252/': ('Story', 'Transform Energy', 'Oil', 'Indigenous', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/five-ways-people-are-standing-up-to-oil-pipel/blog/61458/': ('Story', 'Transform Energy', 'Oil', 'EnergySolutions', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/announcing-the-winners-of-the-2017-greenpeace/blog/59813/': ('Story', 'Protect Nature', 'Forests', 'Oceans', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/calgary-oil-patch-not-laughing-at-climate-law/blog/60292/': ('Story', 'Transform Energy', 'Oil', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/shells-retreat-from-canadian-arctic-creates-s/blog/56720/': ('Story', 'Transform Energy', 'Oil', 'Victory', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/how-does-solar-work-in-the-arctic/blog/57366/': ('Story', 'Transform Energy', 'EnergySolutions', 'Arctic', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/resolute-responds-to-greenpeace-campaigns-by-/blog/58562/': ('Story', 'Protect Nature', 'Forests', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/16-adorable-reasons-to-protect-canadas-boreal/blog/59486/': ('Story', 'Protect Nature', 'Forests', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/four-tar-sands-pipelines-are-heavily-financed/blog/59653/': ('Story', 'Transform Energy', 'Oil', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/why-does-the-government-ignore-the-nuclear-th/blog/60417/': ('Story', 'Transform Energy', 'Nuclear', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/growing-ghgs-from-oil-industry-put-canadian-c/blog/61183/': ('Story', 'Transform Energy', 'Oil', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/worlds-8th-largest-banks-says-it-wont-finance/blog/60466/': ('Story', 'Transform Energy', 'Oil', 'Victory', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/a-world-without-greenpeace-how-one-corporatio/blog/58974/': ('Story', 'Protect Nature', 'Forests', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/protecting-intact-forests-fscs-motion-65-gett/blog/55126/': ('Story', 'Protect Nature', 'Forests', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/an-inevitable-alliance/blog/53216/': ('Story', 'Protect Nature', '', 'Indigenous', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/whether-by-land-or-by-sea-resistance-to-tar-s/blog/60515/': ('Story', 'Transform Energy', 'Oil', 'PeacefulProtest', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/this-is-big-the-fishing-industry-major-brands/blog/56544/': ('Story', 'Protect Nature', 'Oceans', 'Food', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/you-did-it-big-win-for-the-arctic/blog/58385/': ('Story', 'Protect Nature', 'Oil', 'Victory', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/canada-bans-microbeads-another-step-to-tackle/blog/58000/': ('Story', 'Live Sustainably', 'Consumption', 'Victory', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/diving-to-the-antarctic-sea-floor-is-a-scient/blog/61074/': ('Story', 'Protect Nature', 'Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/call-on-provincial-premiers-to-protect-caribo/blog/60630/?ea.tracking.id=20180312-forest-engagingnetworks-email-en-forest-email--signers-qc-gives-up-on-val-dor-caribou_SL_SL_Death_sentence/': ('Story', 'Protect Nature', 'Forests', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/whats-hiding-inside-your-tuna-can/blog/28396/': ('Story', 'Live Sustainably', 'Food', 'Oceans', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/faces-of-greenpeace-meet-the-people-behind-ou/blog/61284/': ('Story', 'Transform Energy', 'Indigenous', '', 'Migrate'),
            'https://www.greenpeace.org/canada/en/blog/Blogentry/setting-sail-to-protect-the-antarctic/blog/60994/': ('Story', 'Transform Energy', 'Oceans', 'Ships', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/greenpeace-occupies-canadas-environment-minis/blog/61449/': ('Story', 'Protect Nature', 'Forests', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/greenpeace-calls-out-minister-blanchettes-fai/blog/61275/': ('Story', 'Protect Nature', 'Forests', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/behind-the-scenes-visiting-the-cree-nation-of/blog/61039/': ('Story', 'Protect Nature', 'Forests', 'Indigenous', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/the-last-man-standing/blog/61060/': ('Story', 'Protect Nature', 'Forests', 'Indigenous', 'Migrate'),
            'https://www.greenpeace.org/canada/en/blog/Blogentry/keeping-warm-in-the-boreal-forest/blog/61064/': ('Story', 'Protect Nature', 'Forests', 'Indigenous', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/why-rudolph-the-reindeer-really-has-a-red-nos/blog/60866/': ('Story', 'Protect Nature', 'Forests', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/our-vision-for-sustainable-forests-includes-w/blog/59402/': ('Story', 'Protect Nature', 'Forests', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/consent-vs-communication-a-tale-of-two-forest/blog/60323/': ('Story', 'Protect Nature', 'Forests', '', 'Migrate'),
            #'http://www.greenpeace.org/canada/en/campaigns/forests/boreal/Learn-about/What-is-Greenpeace-asking-Resolute-to-do-in-the-boreal-forest1/': ('Story', 'Protect Nature', 'Forests', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/celebrating-twenty-years-of-campaigning-to-sa/blog/55436/': ('Story', 'Protect Nature', 'Forests', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/overcoming-the-impossible-safeguarding-the-gr/blog/55504/': ('Story', 'Protect Nature', 'Forests', 'Indigenous', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/from-the-great-bear-to-the-boreal-seven-ways-/blog/55428/': ('Story', 'Protect Nature', 'Forests', 'Indigenous', 'Migrate'),
            'http://www.greenpeace.org/canada/en/Blogentry/return/blog/52938/': ('Story', 'Protect Nature', 'Forests', 'Indigenous', 'Migrate'),
            'https://www.greenpeace.org/canada/en/blog/Blogentry/guest-blog-action-on-plastics-shouldnt-make-l/blog/61370/': ('Story', 'Live Sustainably', 'Consumption', 'Oceans', 'Migrate'),
            'http://www.greenpeace.org/canada/en/blog/Blogentry/winning-on-the-worlds-largest-tuna-company-an/blog/59844/': ('Story', 'Protect Nature', 'Oceans', '', 'Migrate'),
            'https://www.greenpeace.org/canada/en/blog/Blogentry/diving-to-the-antarctic-sea-floor-is-a-scient/blog/61074/': ('Story', 'Protect Nature', 'Oceans', '', 'Migrate'),
            'https://www.greenpeace.org/canada/en/blog/Blogentry/do-ocean-sanctuaries-really-work/blog/61061/': ('Story', 'Protect Nature', 'Oceans', '', 'Migrate'),
            'https://www.greenpeace.org/canada/en/blog/Blogentry/5-things-you-probably-didnt-know-about-the-an/blog/60971/': ('Story', 'Protect Nature', 'Oceans', '', 'Migrate'),
            'https://www.greenpeace.org/canada/en/blog/Blogentry/my-week-on-a-plastic-beach-calling-out-pollut/blog/60367/': ('Story', 'Protect Nature', 'Oceans', 'Consumption', 'Migrate'),
            'https://www.greenpeace.org/canada/en/blog/Blogentry/2017-tuna-ranking-reveals-more-green-tuna-pro/blog/59794/': ('Story', 'Protect Nature', 'Oceans', '', 'Migrate'),
            'https://www.greenpeace.org/canada/en/blog/Blogentry/update-towards-justtuna-how-a-big-canadian-br/blog/59588/': ('Story', 'Protect Nature', 'Oceans', '', 'Migrate'),
            'https://www.greenpeace.org/canada/en/Blog/major-breakthrough-for-ocean-lovers-un-takes-/blog/51974/': ('Story', 'Protect Nature', 'Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/Press-Center/2018/Banking-giant-HSBC-rules-out-financing-controversial-Keystone-XL-pipeline-/': ('Press Release', 'Transform Energy', 'Oil', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/Press-Center/2017/clyde-river-suprem-court/': ('Press Release', 'Transform Energy', 'Oil', 'Indigenous', 'Migrate'),
            'http://www.greenpeace.org/canada/en/Press-Center/2017/PRESS-RELEASE---Greenpeace-slams-Coca-Cola-plastic-announcement-as-dodging-the-main-issue-More-plastic-production-means-more-ocean-plastic-pollution/': ('Press Release', 'Live Sustainably', 'Consumption', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/Press-Center/2017/PRESS-RELEASE-Dutch-Bank-ING-the-latest-to-reject-financing-of-Kinder-Morgan-pipeline/': ('Press Release', 'Transform Energy', 'Oil', 'Victory', 'Migrate'),
            'http://www.greenpeace.org/canada/en/Press-Center/2018/PRESS-RELEASE-120-personalities-and-organizations-in-Quebec-call-for-an-emergency-mobilization-against-the-expansion-of-the-Kinder-Morgan-pipeline---/': ('Press Release', 'Transform Energy', 'Oil', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/Press-Center/2017/STATEMENT---Greenpeace-reaction-to-Desjardins-moratorium-on-pipeline-financing/': ('Press Release', 'Transform Energy', 'Oil', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/Press-Center/2017/Nestle-Unilever-PG-among-worst-offenders-for-plastic-pollution-in-Philippines-in-beach-audit/': ('Press Release', 'Live Sustainably', 'Consumption', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/Press-Center/2017/US-Court-Dismisses-Resolutes-Racketeering-Case-Against-Greenpeace/': ('Press Release', 'Protect Nature', 'Forests', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/Press-Center/2017/Greenpeace-reacts-to-cancellation-of-Energy-East-pipeline/': ('Press Release', 'Transform Energy', 'Oil', 'Victory', 'Migrate'),
            'http://www.greenpeace.org/canada/en/Press-Center/2017/French-bank-BNP-Paribas-the-latest-to-reject-financing-of-tar-sands-pipelines/?id=496214/': ('Press Release', 'Transform Energy', 'Oil', 'Victory', 'Migrate'),
            'http://www.greenpeace.org/canada/en/Press-Center/2018/STATEMENT-Greenpeace-Canada-remains-a-member-of-the-Forest-Stewardship-Council/': ('Press Release', 'Protect Nature', 'Forests', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/Press-Center/2017/PRESS-RELEASE---Greenpeace-activist-climbs-BC-Legislature-flagpole-to-deliver-hopeful-message-to-NDP-and-Greens/': ('Press Release', 'Transform Energy', 'Oil', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/Press-Center/2017/Greenpeace-launches-worldwide-campaign-for-free-speech-/': ('Press Release', 'Protect Nature', 'Forests', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/Press-Center/2018/STATEMENT-On-Kinder-Morgan-pipeline-activity-suspension-The-writing-is-on-the-wall/': ('Press Release', 'Transform Energy', 'Oil', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/Press-Center/2017/Appeal-Court-confirms-Resolutes-claims-against-Greenpeace-scandalous-and-vexatious/': ('Press Release', 'Protect Nature', 'Forests', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/Press-Center/2018/PRESS-RELEASE-Alberta-Securities-Commission-reviewing-Greenpeace-complaint-of-inadequate-disclosure-of-climate-risk-by-Kinder-Morgan/': ('Press Release', 'Transform Energy', 'Oil', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/canada/en/Press-Center/2018/STATEMENT-Federal-government-volunteers-to-captain-the-Titanic-of-tar-sands-oil-pipelines-and-risks-45B-of-Canadians-money-in-the-process/': ('Press Release', 'Transform Energy', 'Oil', 'Indigenous', 'Migrate'),
            'http://www.greenpeace.org/canada/en/Press-Center/2018/press-release-over-1000-people-attend-emergency-rally-against-Kinder-Morgan-in-Montreal/': ('Press Release', 'Transform Energy', 'Oil', 'PeacefulProtest', 'Migrate'),
            'http://www.greenpeace.org/canada/en/Press-Center/2018/Greenpeace-supports-Squamish-Nation-in-the-face-of-Kinder-Morgan-court-ruling-and-urges-governments-to-do-better-on-Indigenous-rights/': ('Press Release', 'Transform Energy', 'Oil', 'Indigenous', 'Migrate'),
            'http://www.greenpeace.org/canada/en/Press-Center/2018/STATEMENT-New-Protected-Areas-Network-in-Alberta-is-a-major-milestone-for-forest-conservation-says-Greenpeace-/': ('Press Release', 'Protect Nature', 'Forests', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/Press-Center/2018/Greenpeace-responds-to-federal-governments-willingness-to-indemnify-Trans-Mountain-Expansion/': ('Press Release', 'Transform Energy', 'Oil', '', 'Migrate'),
            'http://www.greenpeace.org/canada/en/Press-Center/2018/Breaking-Greenpeace-USA-Mosquito-Fleet-activists-block-barge-from-entering-Kinder-Morgans-Seattle-facility--/': ('Press Release', 'Transform Energy', 'Oil', 'PeacefulProtest', 'Migrate'),
            'http://www.greenpeace.org/canada/en/Press-Center/2018/STATEMENT---Greenpeace-Canada-must-use-G7-presidency---to-tackle-plastic-pollution-at-the-source/': ('Press Release', 'Live Sustainably', 'Consumption', 'Oceans', 'Migrate'),
            'http://www.greenpeace.org/canada/en/Press-Center/2018/Greenpeace-occupies-Environment-and-Climate-Change-Canada-with-51-tombstones--to-denounce-failure-on-caribou-protection/': ('Press Release', 'Protect Nature', 'Forests', 'Climate', 'Migrate'),
        }


        # v2
        start_urls = {
            # French
            'http://www.greenpeace.org/canada/fr/Blog/loi-de-protection-de-monsanto-adopte-aux-tats/blog/44548/': ('Story', 'Vivre de façon durable', 'Santé', 'Alimentation', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Blog/cacouna-les-baleines-stoppent-les-travaux-de-/blog/50656/': ('Story', 'Transformer l’énergie', 'Pétrole', 'Océans', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Blog/des-groupes-montent-au-front-pour-sauver-les-/blog/50392/': ('Story', 'Transformer l’énergie', 'Pétrole', 'Océans', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Blog/on-na-pas-toujours-les-amis-quon-voudrait/blog/51403/': ('Story', 'Transformer l’énergie', 'Pétrole', 'Climat', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/en-rponse-aux-questions-sur-cowspiracy/blog/52754/': ('Story', 'Vivre de façon durable', 'Consommation', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/ogm-code-sur-les-fruits-et-lgumes/blog/4875/': ('Story', 'Vivre de façon durable', 'Consommation', 'Alimentation', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Blog/saumon-dlevage-biovraiment/blog/40615/': ('Story', 'Vivre de façon durable', 'Alimentation', 'Océans', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Blog/pourquoi-sopposer-lexploitation-du-ptrole-ext/blog/49149/': ('Story', 'Transformer l’énergie', 'Pétrole', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/les-eaux-uses-parlons-en/blog/54337/': ('Story', 'Vivre de façon durable', 'Santé', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/150-mtres-des-maisons-tes-vous-srieux-m-couil/blog/60282/': ('Story', 'Transformer l’énergie', 'Pétrole', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/partagez-la-pollution-plastique-de-coca-cola-/blog/59525/': ('Story', 'Vivre de façon durable', 'Consommation', 'Océans', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/partagez-vos-photos-des-pires-emballages-plas/blog/61344/': ('Story', 'Vivre de façon durable', 'Consommation', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/la-pollution-plastique-est-le-problme-de-tous/blog/60740/': ('Story', 'Vivre de façon durable', 'Consommation', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/notre-classement-2017-du-thon-en-conserve-mai/blog/59788/': ('Story', 'Vivre de façon durable', 'Consommation', 'Océans', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/expdition-cap-sur-locan-antarctique/blog/61011/': ('Story', 'Protéger la nature', 'Océans', 'Navires', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/ne-laissez-pas-greenpeace-disparatre/blog/59420/': ('Story', 'Protéger la nature', 'Forêts', 'ActionsPacifiques', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/sept-actions-entreprendre-pour-un-futur-sans-/blog/61414/': ('Story', 'Vivre de façon durable', 'Consommation', 'Alimentation', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/gaspillage-surconsommation-et-pauvret-aliment/blog/4171/': ('Story', 'Vivre de façon durable', 'Consommation', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/debouts-en-solidarit-avec-louest-le-qubec-dit/blog/61314/': ('Story', 'Transformer l’énergie', 'Pétrole', 'ActionsPacifiques', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/le-plastique-est-partout/blog/59214/': ('Story', 'Vivre de façon durable', 'Consommation', 'Océans', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/a-commence-chauffer-pour-desjardins-au-sujet-/blog/60523/': ('Story', 'Transformer l’énergie', 'Pétrole', 'Autochtones', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/100-auteurs-du-monde-entier-soutiennent-la-li/blog/59523/': ('Story', 'Protéger la nature', 'Forêts', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/sauver-le-caribou-cest-sauver-la-fort-borale/blog/60588/': ('Story', 'Protéger la nature', 'Forêts', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/quand-trudeau-tourne-le-dos-la-science-du-cli/blog/60166/': ('Story', 'Protéger la nature', 'Climat', 'Pétrole', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/petcoke-inquitante-drogue-issue-des-sables-bi/blog/45346/': ('Story', 'Transformer l’énergie', 'Pétrole', 'Climat', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/pourquoi-rudolphe-le-renne-a-le-nez-rouge/blog/60876/': ('Story', 'Protéger la nature', 'Forêts', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/saumon-dlevage-biovraiment/blog/40615/': ('Story', 'Vivre de façon durable', 'Consommation', 'Océans', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/5-raisons-de-rendre-visite-coca-cola/blog/59268/': ('Story', 'Vivre de façon durable', 'Consommation', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/victoire-la-justice-amricaine-rejette-la-pour/blog/60483/': ('Story', 'Protéger la nature', 'Forêts', 'Victoires', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/non-aux-forages-protgeons-le-qubec-des-ptroli/blog/60576/': ('Story', 'Transformer l’énergie', 'Pétrole', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/pourquoi-sopposer-lexploitation-du-ptrole-ext/blog/49149/': ('Story', 'Transformer l’énergie', 'Pétrole', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/trousse-daction-desjardins-doit-dire-nonauxpi/blog/61169/': ('Story', 'Transformer l’énergie', 'Pétrole', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/le-thon-rouge-de-latlantique-en-voie-de-dispa/blog/34732/': ('Story', 'Protéger la nature', 'Océans', 'Consommation', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/la-pollution-plastique-quelle-est-la-responsa/blog/59462/': ('Story', 'Vivre de façon durable', 'Consommation', 'Océans', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/dsinvestissements-massifs-la-fin-du-ptrole-et/blog/60882/': ('Story', 'Transformer l’énergie', 'Pétrole', 'Victoires', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/td-la-banque-qui-finance-les-pipelines/blog/59857/': ('Story', 'Transformer l’énergie', 'Pétrole', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/alena-quand-les-profits-menacent-les-peuples-/blog/61048/': ('Story', 'Transformer l’énergie', 'Pétrole', 'ActionsPacifiques', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/notre-vritable-position-sur-la-chasse-au-phoq/blog/55396/': ('Story', 'Protéger la nature', 'Océans', 'Arctique', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/clyde-river-obtient-gain-de-cause-devant-la-c/blog/59936/': ('Story', 'Transformer l’énergie', 'Pétrole', 'Autochtones', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/lnergie-solaire-passive/blog/36927/': ('Story', 'Transformer l’énergie', 'SolutionsÉnergétiques', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/comment-fonctionnent-les-herbicides-au-glypho/blog/35566/': ('Story', 'Vivre de façon durable', 'Consommation', 'Alimentation', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/90-organisations-exhortent-le-gant-forestier-/blog/59644/': ('Story', 'Protéger la nature', 'Forêts', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/des-minimaisons-pour-faire-obstacle-au-pipel/blog/60315/': ('Story', 'Transformer l’énergie', 'SolutionsÉnergétiques', 'Autochtones', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Blog/arrtons-de-nous-sentir-coupables-et-agissons/blog/50212/': ('Story', 'Protéger la nature', 'Climat', 'Arctique', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/autres-victoires-citoyennes-sortons-desjardin/blog/61387/': ('Story', 'Transformer l’énergie', 'Pétrole', 'Victoires', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/victoire-le-gant-mondial-du-thon-en-bote-recu/blog/59841/': ('Story', 'Protéger la nature', 'Océans', 'Victoires', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/quatre-axes-de-dveloppement-pour-que-larctiqu/blog/57351/': ('Story', 'Transformer l’énergie', 'SolutionsÉnergétiques', 'Autochtones', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/quatre-femmes-incroyables-aux-cts-desquelles-/blog/61235/': ('Story', 'Protéger la nature', 'ActionsPacifiques', 'Autochtones', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Blog/merci-madame-marois-qubec-sort-du-nuclaire/blog/42421/': ('Story', 'Transformer l’énergie', 'Nucléaire', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/greenpeace-occupe-le-ministre-de-lenvironneme/blog/61450/': ('Story', 'Protéger la nature', 'Forêts', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/devant-le-parlement-du-qubec-greenpeace-dnonc/blog/61276/': ('Story', 'Protéger la nature', 'Forêts', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/dans-les-coulisses-de-notre-visite-la-nation-/blog/61041/': ('Story', 'Protéger la nature', 'Forêts', 'Autochtones', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/lhomme-qui-a-rsist/blog/61059/': ('Story', 'Protéger la nature', 'Forêts', 'Autochtones', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/se-maintenir-au-chaud-dans-la-fort-borale/blog/61065/': ('Story', 'Protéger la nature', 'Forêts', 'Autochtones', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/notre-vision-pour-les-forts-durables-inclut-u/blog/59403/': ('Story', 'Protéger la nature', 'Forêts', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/blogue/Blogentry/ce-que-vous-ne-savez-peut-tre-pas-propos-de-l/blog/58784/': ('Story', 'Protéger la nature', 'Forêts', '', 'Migrate'),
            #'http://www.greenpeace.org/canada/fr/campagnes/Forets/foret-boreale/en-savoir-plus/Quest-ce-que-Greenpeace-demande-a-Resolu-de-faire-dans-la-foret-boreale-/': ('Story', 'Protéger la nature', 'Forêts', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Salle-des-medias/2017/Demande-de-fermeture-durgence-du-pipeline-Trans-Nord/': ('Press Release', 'Transformer l’énergie', 'Pétrole', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Salle-des-medias/2017/REACTION---Desjardins-decrete-un-moratoire-sur-tout-projet-dinvestissement-ou-de-financement-doleoducs/': ('Press Release', 'Transformer l’énergie', 'Pétrole', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Salle-des-medias/2018/COMMUNIQUE-Greenpeace-lance-une-trousse-dactions-pour-un-Futur-Sans-Plastique/': ('Press Release', 'Vivre de façon durable', 'Consommation', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Salle-des-medias/2018/COMMUNIQUE-Puits-abandonnes--Greenpeace-revele-un-rapport-preoccupant-que-le-gouvernement-refuse-de-rendre-public/': ('Press Release', 'Transformer l’énergie', 'Pétrole', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Salle-des-medias/2017/Greenpeace-souligne-lincoherence-des-pratiques-de-Desjardins--dans-la-lutte-contre-les-changement-climatiques/': ('Press Release', 'Transformer l’énergie', 'Pétrole', 'Climat', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Salle-des-medias/2017/BNP-Paribas-se-retire-a-son-tour--du-financement-des-pipelines-de-sables-bitumineux/': ('Press Release', 'Transformer l’énergie', 'Pétrole', 'Victoires', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Salle-des-medias/2017/Rassemblement-devant-la-Caisse-de-Depot-et-Placement-du-Quebec/': ('Press Release', 'Transformer l’énergie', 'Pétrole', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Salle-des-medias/2018/REACTION-La-condamnation-a-mort-des-caribous-de-Val-dOr---le-gouvernement-du-Quebec-nassume-pas-ses-responsabilites-et-abandonne-/': ('Press Release', 'Protéger la nature', 'Forêts', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Salle-des-medias/2017/Greenpeace-lance-une-campagne-globale-pour-le-droit-de-parole/': ('Press Release', 'Protéger la nature', 'Forêts', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Salle-des-medias/2017/La-cour-americaine-rejette-la-poursuite-RICO-de-Resolu-contre-Greenpeace/': ('Press Release', 'Protéger la nature', 'Forêts', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Salle-des-medias/2017/REACTION---Le-deplacement-in-extremis-de-la-harde-de-caribous-de-Val-d-Or-vers-un-zoo-montre-lampleur-de-la-crise-dans-les-forets-du-Quebec-/': ('Press Release', 'Protéger la nature', 'Forêts', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Salle-des-medias/2018/REACTION-Greenpeace-appelle-a-laction-devant-le-constat-dechec/COMMUNIQUE-Kinder-Morgan-lopposition-gronde-aussi-au-Quebec--Desjardins-doit-desinvestir-des-pipelines/': ('Press Release', 'Transformer l’énergie', 'Pétrole', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Salle-des-medias/2018/40-GROUPES--AU-QUEBEC-EXHORTENT-JUSTIN-TRUDEAU-/': ('Press Release', 'Transformer l’énergie', 'Pétrole', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Salle-des-medias/2018/REACTION-Greenpeace-Le-gouvernement-federal-se-portera-acquereur-de-loleoduc-Trans-Mountain-en-gageant-45-milliards-de-largent-des-Canadiens/': ('Press Release', 'Transformer l’énergie', 'Pétrole', 'Autochtones', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Salle-des-medias/2018/COMMUNIQUE-Rassemblement-ENSEMBLECONTREKINDERMORGAN/': ('Press Release', 'Transformer l’énergie', 'Pétrole', 'ActionsPacifiques', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Salle-des-medias/2018/Pour-une-souverainete-energetique-du-Quebec--le-Sommet-pour-une-transition-energetique-juste-est-lance-/': ('Press Release', 'Transformer l’énergie', 'SolutionsÉnergétiques', 'Autochtones', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Salle-des-medias/2018/REACTION-Le-Quebec-devrait-suivre-lexemple-de-la-nouvelle-grande-aire-protegee-en-Alberta-dit-Greenpeace/': ('Press Release', 'Protéger la nature', 'Forêts', 'Autochtones', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Salle-des-medias/2018/Greenpeace-repond-a-la-volonte-du-gouvernement-federal-dindemniser-Kinder-Morgan-pour-le-projet-de-pipeline-Trans-Mountain/': ('Press Release', 'Transformer l’énergie', 'Pétrole', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Salle-des-medias/2018/COMMUNIQUE-120-personnalites-et-organisations-du-Quebec-appellent-a-la-mobilisation-durgence-contre-lexpansion-du-pipeline-de-Kinder-Morgan/': ('Press Release', 'Transformer l’énergie', 'Pétrole', 'Autochtones', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Salle-des-medias/2018/Greenpeace-Couillard-condamne-les-caribous--au-detriment-des-emplois-forestiers/': ('Press Release', 'Protéger la nature', 'Forêts', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Salle-des-medias/2018/COMMUNIQUE-35-caisses-exhortent-le-Mouvement-Desjardins---a-se-detourner-des-pipelines-et-du-projet-de-Kinder-Morgan/': ('Press Release', 'Transformer l’énergie', 'Pétrole', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Salle-des-medias/2018/COMMUNIQUE-Une-coalition-historique-de-groupes-environnementaux-et-citoyens--depose-ses-propositions-aux-partis-politiques/': ('Press Release', 'Protéger la nature', 'Forêts', 'Climat', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Salle-des-medias/2018/COMMUNIQUE-Greenpeace-expose-et-occupe-le-tunnelier--parasite---de-Kinder-Morgan---/': ('Press Release', 'Transformer l’énergie', 'Pétrole', 'Autochtones', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Salle-des-medias/2018/Communique-conjoint-Le-premier-et-tant-attendu-rapport-du-gouvernement-canadien-sur-lhabitat-critique-du-caribou-conclut-que-celui-ci-nest-pas-protege--/': ('Press Release', 'Protéger la nature', 'Forêts', 'Autochtones', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Salle-des-medias/2018/REACTION-Des-groupes-restent-sceptiques-devant-le-nouveau-plan-dinspection-des-puits-inactifs-et-abandonnes-au-Quebec/': ('Press Release', 'Transformer l’énergie', 'Pétrole', '', 'Migrate'),
            'http://www.greenpeace.org/canada/fr/Salle-des-medias/2018/Greenpeace-occupe-les-lieux-du-ministere-de-lEnvironnement-avec-51-pierres-tombales--pour-denoncer-lechec-de-la-protection-du-caribou/': ('Press Release', 'Protéger la nature', 'Forêts', '', 'Migrate'),
        }

        for url,data in start_urls.iteritems():
            post_type, categories, tags1, tags2, action = data
            if ( post_type=='Story' ):
                request = scrapy.Request(url, callback=self.parse_blog, dont_filter='true')
            elif ( post_type=='Publication' ):
                request = scrapy.Request(url, callback=self.parse_publication, dont_filter='true')
            elif ( post_type=='Press release' or post_type=='Press Release' ):
                request = scrapy.Request(url, callback=self.parse_press, dont_filter='true')
            elif ( post_type=='Feature' ):
                request = scrapy.Request(url, callback=self.parse_feature, dont_filter='true')

            if ( action.lower()=='migrate' ):
                request.meta['status'] = 'publish'
            if ( action.lower()=='archive' ):
                request.meta['status'] = 'draft'
            request.meta['categories'] = categories
            request.meta['tags1'] = tags1
            request.meta['tags2'] = tags2
            request.meta['action'] = action
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

    def parse_feature(self, response):

        def extract_with_css(query):
            return response.css(query).extract_first()

        image_gallery=response.xpath("//*[contains(@class, 'embedded-image-gallery')]")
        p3_image_gallery = 'false'
        if image_gallery:
            p3_image_gallery = 'true'

        imagesB=response.xpath('//*[@id="content"]//img/@src').extract()
        imagesB_generated = list()
        for image_file in imagesB:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.org/',1)
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

        date_field = response.xpath('//*[@id="content"]/div[4]/div/div[2]/span/text()').extract()[0]
        if (date_field.startswith('Feature story - ')):
            date_field = date_field.replace('Feature story - ','',1)
        if date_field:
            if (date_field.startswith('Feature story - ')):
                date_field = date_field.replace('Feature story - ','',1)
            date_field = dateutil.parser.parse(date_field)

        lead_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[1]/div').extract()[0]
        body_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[2]').extract()[0]
        if body_text:
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.org/').replace('href="/', 'href="http://www.greenpeace.org/')
            body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)
            if lead_text:
                body_text = '<div class="leader">' + lead_text + '</div>' + body_text + response.xpath(' //*[@id="content"]/div[4]/div/div[2]/p').extract_first()

        yield {
            'type': 'Story',
            'p3_image_gallery': p3_image_gallery,
            #'title': extract_with_css('#content > div.happen-box.article > h1::text'),
            'title': response.xpath('//*[@id="content"]/div[4]/h1/span/text()').extract()[0],
            'subtitle': extract_with_css('div.article h1 span::text'),
            'author': 'Greenpeace Canada',
            'date': date_field,
            #'lead': extract_with_css('div.news-list div.post-content *:first-child strong::text'),
            'lead': lead_text,
            'categories': response.meta['categories'],
            'text':  body_text,
            'imagesA': response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img/@src').extract(),
            'imagesB': imagesB_generated,
            #'imagesB': response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img[not(ancestor::a)]/@src').extract(), #don't import image if there's an a tag around it
            'imagesC': response.xpath('//div[@class="gallery"]//div[@class="img-nav"]//a/@rel').extract(), # Galleries (horrible html)
            'pdfFiles': pdf_files_generated,
            'tags1': response.meta['tags1'],
            'tags2': response.meta['tags2'],
            'url': response.url,
        }


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

        imagesEnlarge=response.xpath('//div[@class="news-list"]//div[@class="post-content"]//a[@class="open-img BlogEnlargeImage"]/@href').extract()
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
        date_field = date_field.replace(" à", "")
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
                self.csv_writer(data, "email_images_url_list_fr_story.csv")
        """

        yield {
            'type': 'Story',
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
            'url': response.url,
            'status': response.meta['status'],
            'map_url': '',
            'unique_map_id': unique_map_id,
            'thumbnail': thumbnail,
        }

    def parse_press(self, response):

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
            # Custom fix for GPCA only.
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

        #lead_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[1]/div/text()').extract()[0]
        body_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[2]').extract()[0]
        if body_text:
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.org/').replace('href="/', 'href="http://www.greenpeace.org/')
            body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)
            #if lead_text:
                #body_text = '<div class="leader">' + lead_text + '</div>' + body_text + response.xpath(' //*[@id="content"]/div[4]/div/div[2]/p').extract_first()

        subtitle = extract_with_css('div.article h2 span::text')
        if subtitle:
            body_text = '<h2>' + subtitle + '</h2><br />' + body_text

        thumbnail = response.xpath('string(head//link[@rel="image_src"]/@href)').extract_first()

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
                self.csv_writer(data, "email_images_url_list_fr.csv")
        """


        # Post data mapping logic start.
        unique_map_id = int(time.time() + random.randint(0, 999))

        if "/en/" in response.url:
            # For English language POSTs

            # Check the POST transalation availability
            map_url = response.xpath('//*[@class="language"]//option[2]/@value').extract()[0]
            if "/fr/" not in map_url:
                map_url = ''

            if map_url:
                map_url = 'http://www.greenpeace.org' + map_url

                # The Post mapping data added into csv file.
                data = [unique_map_id, response.url, map_url]
                self.csv_writer(data, self.__connector_csv_filename)
        else:
            # For French language POSTs

            # Check the POST transalation if available
            map_url = response.xpath('//*[@class="language"]//option[1]/@value').extract()[0]
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
        # Post data mapping logic ends.

        yield {
            'type': 'Press Release',
            'p3_image_gallery': p3_image_gallery,
            'title': extract_with_css('div.article h1 span::text'),
            #'subtitle': '',
            'author': 'Greenpeace Canada',
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
            'map_url': map_url,
            'unique_map_id': unique_map_id,
            'url': response.url,
        }
     
               
    def parse_publication(self, response):

        def extract_with_css(query):
            return response.css(query).extract_first()

        imagesA=response.xpath('//div[@class="text"]/div[not(@id) and not(@class)]//a[img]/@href').extract()
        imagesA_generated = list()
        for image_file in imagesA:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.org/',1)
            imagesA_generated.append(image_file)

        imagesB=response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[2]//img/@src').extract()
        imagesB_generated = list()
        for image_file in imagesB:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.org/',1)
            imagesB_generated.append(image_file)
        
        pdfFiles=response.css('div.article a[href$=".pdf"]::attr(href)').extract()
        pdf_files_generated = list()
        for pdf_file in pdfFiles:
            if (pdf_file.startswith('/')):
                pdf_file = pdf_file.replace('/','http://www.greenpeace.org/',1)
            pdf_files_generated.append(pdf_file)
            print pdf_files_generated

        date_field = response.css('div.article div.text span.author::text').re_first(r' - \s*(.*)')
        if date_field:
            date_field = dateutil.parser.parse(date_field)

        lead_text = extract_with_css('#content > div.happen-box.article > div > div.text > div.leader > div')

        image_gallery=response.xpath("//*[contains(@class, 'embedded-image-gallery')]")
        p3_image_gallery = 'false'
        if image_gallery:
            p3_image_gallery = 'true'
        
        body_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[2]').extract_first()
        attachment_field = response.xpath('//*[@id="content"]/div[4]/div/div[2]/p/a').extract_first()
        if body_text:
            if attachment_field:
                body_text = body_text + attachment_field
            if lead_text:
                body_text = '<div class="leader">' + lead_text + '</div>' + body_text

        if body_text:
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.org/').replace('href="/', 'href="http://www.greenpeace.org/')
            body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)

        subtitle = extract_with_css('div.article h2 span::text')
        if subtitle:
            body_text = '<h2>' + subtitle + '</h2><br />' + body_text

        images=response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[2]//img[contains(@style, "float:")]').extract()   #img[@style="margin: 9px; float: left;"]
        imagesD_generated = list()
        for image in images:
            imagesD_generated.append(image)

        thumbnail = response.xpath('string(head//link[@rel="image_src"]/@href)').extract_first()

        yield {
            'type': 'Publication',
            'p3_image_gallery': p3_image_gallery,
            'title': extract_with_css('div.article h1 span::text'),
            #'subtitle': subtitle,
            'author': 'Greenpeace CA',
            'author_username': 'greenpeace',
            'date': date_field,
            #'lead': extract_with_css('div.news-list div.post-content *:first-child strong::text'),
            'lead': extract_with_css('#content > div.happen-box.article > div > div.text > div.leader > div'),
            'categories': response.meta['categories'],
            'text': body_text,
            'imagesA': imagesA_generated,
            #'imagesB': response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img[not(ancestor::a)]/@src').extract(), #don't import image if there's an a tag around it
            'imagesB': imagesB_generated,
            'imagesC': response.xpath('//div[@class="gallery"]//div[@class="img-nav"]//a/@rel').extract(), # Galleries (horrible html)
            'imagesD': imagesD_generated,
            'pdfFiles': pdf_files_generated,
            'tags1': response.meta['tags1'],
            'tags2': response.meta['tags2'],
            'url': response.url,
        }

    def filter_post_content(self, post_data):
        # Filter the youtube video and add embed shortcode instead.
        post_data = re.sub(
            '\<object[width\=\"height0-9\s]*data\=\"([https]*\:\/\/www.youtube.com[a-zA-Z0-9\/\=\-\?\_]*)\"[\=\"a-zA-Z\/\-\s0-9]*\>[\\n\s]*(.*)[\\n\s]*\<\/object\>',
            '[embed]\g<1>[/embed]', post_data)

        return post_data

    def filter_month_name(self, month_name):
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

        # Replace the french month name with english month name.
        for fr_month, en_month in month_fr_en.iteritems():
            month_name = month_name.replace(fr_month, en_month)

        return month_name;

    def csv_writer(self, data, path):
        # Write data to a CSV file path
        with open(path, "a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(data)
