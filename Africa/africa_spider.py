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
        'FEED_URI': 'gpaf_staging_v2_FR_B2.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    __connector_csv_filename = "connector_v2_final.csv"
    __connector_csv_log_file = "connector_csv_log_v2"

    def start_requests(self):

        #v1 EN
        start_urls = {
            # Blogs
            'http://www.greenpeace.org/africa/en/getinvolved/cyberactivist/':('Blogs','Inspire the Movement','Activism','','','article','Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/10-good-reasons-to-protect-whales/blog/57806/':('Blogs','Protect the Environment','Oceans','Water','','news-list','Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/12-things-you-can-do-to-start-eco-food-revolu/blog/56718/':('Blogs','Change My Community','Farming','Lifestyle','','news-list','Migrate'),

            # Blogs
            'http://www.greenpeace.org/africa/en/News/news/a-beginners-guide-to-nuclear-power/':('Blogs','Inspire the Movement','Energy','Nuclear','','article','Migrate'),
            'http://www.greenpeace.org/africa/en/News/news/Africans-care-about-the-environment-too/':('Blogs','Inspire the Movement','Energy','','','article','Migrate'),
            'http://www.greenpeace.org/africa/en/News/news/Poisoned-Sugar-Exposes-Kenyas-Broken-Food-System/':('Blogs','Change My Community','Farming','','Kenya','article','Migrate'),

            # Press Release
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/--Greenpeace-and-Guinea-Bissau-authorities-arrest-fishing-vessels/':('Press Release','Protect the Environment','Oceans','Fishing','','article','Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/-Greenpeaces-Project-Sunshine-delivers-in-Diepsloot/':('Press Release','Protect the Environment','Energy','SouthAfrica','','article','Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/10-more-steps-back-for-Eskom-on-the-precipice-of-Molefes-return/':('Press Release','Protect the Environment','Energy','SouthAfrica','','article','Migrate'),

            # Publications
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Publications/Africas-forests-under-threat-/':('Publications','Protect the Environment','Forest','','','article','Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Publications/Africas-Forests-Under-Threat/':('Publications','Protect the Environment','Forest','GreenpeaceAfrica','','article','Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Publications/Crisis-for-FSC-in-the-Congo-Basin/':('Publications','Protect the Environment','Forest','','','article','Migrate'),
        }

        # v1 FR
        start_urls = {
            # Blogs
            'http://www.greenpeace.org/africa/fr/Actualities/actualites/Alors-que-la-RDC-sapproche-des-elections-nationales-le-gouvernement-cherche-a-convertir-sa-foret-et-sa-faune-sauvage-en-argent-comptant/':('Blogs', "Protéger l'Environnement",'Forêts','Biodiversité','RDC', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/actualites/Dans-le-Bassin-Du-Congo-le-mythe-de-Lexploitation-selective-du-bois-mord-la-poussiere/':('Blogs', "Protéger l'Environnement",'Forêts','','RDC', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/actualites/LUNESCO-echoue-a-proteger-la-Reserve-du-Dja-au-Cameroun-de-multiples-menaces-y-compris-la-plantation-dhevea-Sudcam/':('Blogs', "Protéger l'Environnement",'Forêts','','Cameroun', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/2016-lanne-o-on-dit-adieu-au-charbon/blog/55503/':('Blogs', 'Inspirer le Mouvement', 'Energie', 'Charbon','','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/45-ans-de-pouvoir-citoyen/blog/57508/':('Blogs', '', 'GreenpeaceAfrica', 'Activisme', '','news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/5-resolutions-oceans-plastiques/blog/55257/':('Blogs', 'Inspirer le Mouvement', 'Plastiques', 'Océans', '','news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/afrique-besoin-FiTI/blog/55554/':('Blogs', "Protéger l'Environnement",'Océans','Pêche','','news-list','Migrate'),

            # Publications
            'http://www.greenpeace.org/africa/fr/Presse/Publications/Couper-le-droit-de-parole-/':('Publications', "Protéger l'Environnement",'Forêts','','','article','Migrate'),
            'http://www.greenpeace.org/africa/fr/Presse/Publications/Herakles-FarmsSGSOC-Histoire-dun-projet-dhuile-de-palme-destructeur-au-Cameroun/':('Publications', "Protéger l'Environnement",'Forêts','','Cameroun','article','Migrate'),
            'http://www.greenpeace.org/africa/fr/Presse/Publications/La-Norvege-et-la-France-menacent-les-forets-de-la-RDC1/':('Publications', "Protéger l'Environnement",'Forêts','','RDC','article','Migrate'),
            'http://www.greenpeace.org/africa/fr/Presse/Publications/Le-Cout-de-la-Destruction-des-Oceans1/':('Publications', "Protéger l'Environnement",'Océans','Pêche','','article','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/actualites/La-deuxieme-foret-tropicale-au-monde-menacee-par-lhuile-de-palme-et-lexploitation-forestiere/': ('Publications', "Protéger l'Environnement", 'Forêts', '', '', 'article', 'Migrate'),

            # Press Release
            'http://www.greenpeace.org/africa/fr/Presse/des-recommandations-fortes-pour-les-etats-ouest-africains/':('Communiqués de presse', "Protéger l'Environnement",'Océans','Pêche','','article','Migrate'),
            'http://www.greenpeace.org/africa/fr/Presse/Enquete-sur-les-investissements-du-groupe-Bollore-dans-des-plantations-africaines/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','RDC','article','Migrate'),
            'http://www.greenpeace.org/africa/fr/Presse/Fraud-sur-le-Tonnage-des-Navires-de-Peche-Industriels/':('Communiqués de presse', "Protéger l'Environnement",'Océans','Pêche','Sénégal','article','Migrate'),
            'http://www.greenpeace.org/africa/fr/Presse/Greenpeace-21e-COPACE/':('Communiqués de presse', "Protéger l'Environnement",'Océans','Pêche','','article','Migrate'),
        }

        # v2 En post.
        ## - multilingual posts.
        #### - duplicate post.
        start_urls = {
            ####B1####
            'http://www.greenpeace.org/africa/en/News/Blog/10-good-reasons-to-protect-whales/blog/57806/': ('Blogs', 'Protect the Environment', 'Oceans', 'Water', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/12-things-you-can-do-to-start-eco-food-revolu/blog/56718/':('Blogs', 'Change My Community', 'Farming', 'Lifestyle', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/16-adorable-reasons-to-protect-canadas-boreal/blog/59455/':('Blogs', 'Protect the Environment', 'Forest', '', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/3-water-related-petitions-to-sign-this-world-/blog/61298/':('Blogs', 'Inspire the Movement', 'Water', 'Activism', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/5-madiba-quotes-to-reflect-on-this-mandela-da/blog/61734/':('Blogs', 'Inspire the Movement', 'GreenpeaceAfrica', 'Activism', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/5-more-things-businesses-can-do-now-that-they/blog/61179/':('Blogs', 'Inspire the Movement', 'Plastics', 'Oceans', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/5-things-you-probably-didnt-know-about-the-an/blog/61103/':('Blogs', 'Protect the Environment', 'Oceans', 'Fishing', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/6-ways-corporate-lawsuits-kill-free-speech-an/blog/59424/':('Blogs', 'Protect the Environment', 'Forest', '', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/7-reasons-why-i-will-donate-today-create-hope/blog/59852/':('Blogs', 'Inspire the Movement', 'Energy', '', 'SouthAfrica', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/7-things-you-can-do-for-the-planet-this-earth/blog/56248/':('Blogs', 'Change My Community', 'Plastics', 'Lifestyle', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/a-cost-that-curses/blog/60808/':('Blogs', 'Protect the Environment', 'Oceans', 'Fishing', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/a-day-at-sea-wildlife-encounters/blog/58913/':('Blogs', 'Protect the Environment', 'Oceans', 'Fishing', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/a-little-more-on-plastics/blog/61182/':('Blogs', 'Inspire the Movement', 'Plastics', 'Activism', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/a-new-era-is-opening/blog/61278/':('Blogs', 'Protect the Environment', 'Oceans', 'Fishing', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/a-wealth-of-life-the-beauty-of-west-africa/blog/59286/':('Blogs', 'Protect the Environment', 'Oceans', 'Activism', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/authors-around-the-world-stand-up-for-free-sp/blog/59558/':('Blogs', 'Protect the Environment', 'Forest', '', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/black-anniversary-to-sgsoc/blog/58121/':('Blogs', 'Protect the Environment', 'Forest', '', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/bridgesnotwalls-its-time-for-solidarity-love-/blog/58534/':('Blogs', 'Inspire the Movement', 'Activism', 'AboutUs', 'GreenpeaceAfrica', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/can-the-world-come-to-its-senses-on-nuclear-w/blog/60118/':('Blogs', 'Inspire the Movement', 'Coal', 'Energy', 'SouthAfrica', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/celebrating-womens-day-with-jenn-coles/blog/60007/':('Blogs', 'Inspire the Movement', 'Energy', 'Coal', 'GreenpeaceAfrica', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/could-2016-be-the-year-we-break-free-from-coa/blog/55487/':('Blogs', 'Inspire the Movement', 'Energy', '', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/donors-remain-indifferent-as-moratorium-breac/blog/58646/':('Blogs', 'Protect the Environment', 'Forest', '', 'DRC', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/election-time-what-progress-since-1994/blog/57161/':('Blogs', 'Inspire the Movement', 'Energy', '', 'SouthAfrica', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/evening-on-the-esperanza/blog/55917/':('Blogs', 'Protect the Environment', 'Oceans', 'Activism', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/fishing-from-the-sky-empty-nets-dead-fish-and/blog/59146/':('Blogs', 'Protect the Environment', 'Oceans', 'Activism', 'GreenpeaceAfrica', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/give-the-congo-basin-forest-a-chance/blog/60446/':('Blogs', 'Protect the Environment', 'Forest', 'Farming', 'DRC', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/greenpeace-leaves-the-cecaf-meeting-with-mixe/blog/56317/':('Blogs', 'Protect the Environment', 'Oceans', 'Lifestyle', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/greenpeace-ships-warriors-at-sea/blog/58715/':('Blogs', 'Inspire the Movement', 'Activism', 'AboutUs', 'GreenpeaceAfrica', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/greenpeace-turns-45/blog/57510/':('Blogs', 'Inspire the Movement', 'AboutUs', 'GreenpeaceAfrica', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/heres-your-chance-to-make-a-real-change/blog/59696/':('Blogs', 'Inspire the Movement', 'Energy', '', 'SouthAfrica', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/honourable-minister-fix-this/blog/56128/':('Blogs', 'Protect the Environment', 'Oceans', 'Lifestyle', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/how-does-organic-food-affect-your-body/blog/58426/':('Blogs', 'Change My Community', 'Farming', 'GreenpeaceAfrica', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/how-trump-succeeds-to-put-himself-on-the-wron/blog/59581/':('Blogs', 'Inspire the Movement', 'Energy', 'GreenpeaceAfrica', 'SouthAfrica', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/i-can-still-feel-the-enthusiasm-of-our-camero/blog/61266/':('Blogs', 'Protect the Environment', 'Oceans', 'Activism', 'AboutUs', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/i-saw-the-plunder-of-our-oceans/blog/59235/':('Blogs', 'Protect the Environment', 'Oceans', 'Biodiversity', 'GreenpeaceAfrica', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/if-you-cant-reuse-it-refuse-it/blog/61594/':('Blogs', 'Protect the Environment', 'Forest', 'Oceans', 'Kenya', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/investigation-how-illegal-timber-from-cameroo/blog/55951/':('Blogs', 'Protect the Environment', 'Forest', '', 'Cameroon', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/its-5-goals-to-green-oclock/blog/58472/':('Blogs', 'Inspire the Movement', 'Plastics', 'Water', 'SouthAfrica', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/let-the-installation-begin/blog/60192/':('Blogs', 'Inspire the Movement', 'Energy', '', 'SouthAfrica', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/let-the-moratorium-be/blog/60744/':('Blogs', 'Protect the Environment', 'Forest', '', 'DRC', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/lets-make-it-a-green-peace/blog/57562/':('Blogs', 'Inspire the Movement', 'Energy', 'Activism', 'GreenpeaceAfrica', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/loud-alarm-bells-for-growth-in-environmental-/blog/56870/':('Blogs', 'Protect the Environment', 'Forest', '', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/maiden-machakos-farmers-network/blog/61499/':('Blogs', 'Protect the Environment', 'Farming', 'Food', 'AboutUs', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/mandela-an-instrument-of-hope/blog/57091/':('Blogs', 'Inspire the Movement', 'Activism', 'GreenpeaceAfrica', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/march-of-the-penguins/blog/60999/':('Blogs', 'Inspire the Movement', 'Oceans', 'Water', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/my-night-on-board-a-chinese-fishing-vessel-in/blog/59077/':('Blogs', 'Protect the Environment', 'Oceans', 'Fishing', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/my-vote-will-change-the-world/blog/57162/':('Blogs', 'Inspire the Movement', 'Energy', 'Activism', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/new-trade-protections-for-sharks-but-are-they/blog/58040/':('Blogs', 'Protect the Environment', 'Oceans', 'Fishing', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/new-years-plastic-resolution-5-simple-ways-to/blog/55343/':('Blogs', 'Inspire the Movement', 'Plastics', 'Oceans', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/news-worth-celebrating-megadam-in-the-heart-o/blog/57214/':('Blogs', 'Protect the Environment', 'Forest', 'Oceans', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/nuclear-testing-is-not-a-path-to-security-and/blog/57377/':('Blogs', 'Inspire the Movement', 'Energy', 'Activism', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/one-million-stand-up-for-the-tapajs-river/blog/57007/':('Blogs', 'Protect the Environment', 'Conservation', 'Oceans', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/our-land-should-unite-not-antagonist-us/blog/60090/':('Blogs', 'Protect the Environment', 'Forest', 'Conservation', 'DRC', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/our-oceans-our-responsibility/blog/58820/':('Blogs', 'Protect the Environment', 'Oceans', 'Fishing', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/penguins-march-to-cape-town/blog/61181/':('Blogs', 'Protect the Environment', 'Oceans', 'Conservation', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/plastic-ban-more-can-be-done-towards-waste-ma/blog/60286/':('Blogs', 'Inspire the Movement', 'Plastics', 'Oceans', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/precious-intact-forests-in-the-congo-must-be-/blog/60379/':('Blogs', 'Protect the Environment', 'Forest', 'Conservation', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/pressing-forward-with-greenpeace-africa-gende/blog/61218/':('Blogs', 'Inspire the Movement', 'GreenpeaceAfrica', 'AboutUs', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/prisca-nafula-mayende-a-rural-activist-transf/blog/61194/':('Blogs', 'Change My Community', 'Farming', 'Forest', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/project-sunshine-powering-off-grid-communitie/blog/59717/':('Blogs', 'Inspire the Movement', 'Energy', 'Activism', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/rio-olympics-why-the-opening-ceremonys-spotli/blog/57292/':('Blogs', 'Inspire the Movement', 'Energy', 'Forest', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/setting-sail-to-protect-the-antarctic/blog/61029/':('Blogs', 'Protect the Environment', 'Oceans', 'Biodiversity', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/shopping-on-sunshine/blog/56608/':('Blogs', 'Inspire the Movement', 'Energy', 'Plastics', 'SouthAfrica', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/sight-on-the-target-tackling-destructive-fish/blog/56792/':('Blogs', 'Protect the Environment', 'Oceans', 'Fishing', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/stop-sgsoc-palm-oil-plantation-project/blog/57654/':('Blogs', 'Protect the Environment', 'Forest', 'Conservation', 'Cameroon', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/strength-in-numbers-sensitising-retailers-and/blog/61714/':('Blogs', 'Inspire the Movement', 'Plastics', '', 'Kenya', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/take-the-better-eating-challenge/blog/56794/':('Blogs', 'Change My Community', 'Farming', 'Lifestyle', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/taking-the-pirates-down/blog/61240/':('Blogs', 'Protect the Environment', 'Oceans', 'Fishing', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/talking-forest-with-city-dwellers-in-yaounde/blog/61342/':('Blogs', 'Protect the Environment', 'Forest', '', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/thank-you-for-letting-me-be-a-part-of-your-jo/blog/55222/':('Blogs', 'Inspire the Movement', 'GreenpeaceAfrica', 'AboutUs', '', 'news-list', 'Migrate'),

            ####B2####
            'http://www.greenpeace.org/africa/en/News/Blog/the-biggest-sun-plant-in-the-solar-orchard/blog/56855/':('Blogs', 'Inspire the Movement', 'Energy', '', 'SouthAfrica', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/The-Congo-Basin-Forests-made-us-dance/blog/60647/':('Blogs', 'Protect the Environment', 'Forest', '', 'DRC', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/the-department-of-environmental-affairs-is-se/blog/60798/':('Blogs', 'Inspire the Movement', 'Energy', '', 'SouthAfrica', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/the-shoppers-voice/blog/56752/':('Blogs', 'Inspire the Movement', 'Energy', '', 'SouthAfrica', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/the-sun-is-the-center-of-it-all/blog/56669/':('Blogs', 'Inspire the Movement', 'Energy', '', 'SouthAfrica', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/the-urgency-of-now-the-fate-of-the-lungs-of-a/blog/59411/':('Blogs', 'Protect the Environment', 'Forest', '', 'DRC', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/the-world-stood-up-in-arms-for-the-congo-basi/blog/60709/':('Blogs', 'Protect the Environment', 'Forest', 'Energy', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/this-is-why-the-antarctic-needs-your-help/blog/61280/':('Blogs', 'Protect the Environment', 'Oceans', 'Conservation', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/trumps-attack-on-the-paris-climate-agreement-/blog/59576/':('Blogs', 'Inspire the Movement', 'Energy', '', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/volunteer-spotlight-delwyn-pillay/blog/55559/':('Blogs', 'Inspire the Movement', 'Activism', 'GreenpeaceAfrica', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/walking-through-the-tropical-swamps-of-drc/blog/61297/':('Blogs', 'Protect the Environment', 'Forest', '', 'DRC', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/waste-no-time-start-volunteering/blog/58195/':('Blogs', 'Inspire the Movement', 'Activism', 'GreenpeaceAfrica', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/we-bring-culture-and-nature-together-to-celeb/blog/59695/':('Blogs', 'Inspire the Movement', 'Activism', 'GreenpeaceAfrica', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/we-speak-for-the-trees/blog/59650/':('Blogs', 'Protect the Environment', 'Forest', 'GreenpeaceAfrica', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/whale-fail-no-new-sanctuary-in-the-south-atla/blog/57829/':('Blogs', 'Protect the Environment', 'Oceans', 'Fishing', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/what-made-me-embark-on-a-life-changing-missio/blog/60597/':('Blogs', 'Protect the Environment', 'Forest', 'Activism', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/what-to-expect-during-cop22-our-expectations-/blog/57936/':('Blogs', 'Inspire the Movement', 'Energy', '', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/which-is-the-antarctics-top-penguin/blog/61032/':('Blogs', 'Protect the Environment', 'Oceans', 'Biodiversity', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/who-is-tampering-with-our-water/blog/61295/':('Blogs', 'Inspire the Movement', 'Water', '', 'SouthAfrica', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/why-we-must-never-take-clean-drinking-water-f/blog/61763/':('Blogs', 'Inspire the Movement', 'Energy', 'Water', 'SouthAfrica', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/Why-we-sailing-into-the-Congo-Basin-forest/blog/60546/':('Blogs', 'Protect the Environment', 'Forest', '', 'DRC', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/world-water-day-2018-more-needs-to-be-done/blog/61304/':('Blogs', 'Change My Community', 'Water', '', '', 'news-list', 'Migrate'),
            ####'http://www.greenpeace.org/africa/en/News/Blog/why-we-must-never-take-clean-drinking-water-f/blog/61763/':('Press Release', 'Protect the Environment', 'Water', '', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/Blog/from-fires-to-floods-the-worlds-weird-weather/blog/61829/':('Blogs', 'Inspire the Movement', 'Biodiversity', 'Lifestyle', '', 'news-list', 'Migrate'),

            'http://www.greenpeace.org/africa/en/News/news/a-beginners-guide-to-nuclear-power/':('Blogs', 'Inspire the Movement', 'Energy', 'Nuclear', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/news/Africans-care-about-the-environment-too/':('Blogs', 'Inspire the Movement', 'Energy', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/news/Poisoned-Sugar-Exposes-Kenyas-Broken-Food-System/':('Blogs', 'Change My Community', 'Farming', '', 'Kenya', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/news/Can-we-count-on-Jeff-to-deliver-renewable-energy/':('Blogs', 'Inspire the Movement', 'Energy', 'Coal', 'SouthAfrica', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/news/Mega-coal-plants-versus-people-of-South-Africa-/':('Blogs', 'Inspire the Movement', 'Energy', 'Coal', 'SouthAfrica', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/News/news/IN-THE-CONGO-BASIN-THE-MYTH-OF-SELECTIVE-LOGGING-BITES-THE-DUST/':('Blogs', 'Protect the Environment', 'Forest', 'Conservation', 'DRC', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/news/The-New-Name-Behind-the-threat-to-Cameroons-Forests/':('Blogs', 'Protect the Environment', 'Forest', 'Conservation', 'Cameroon', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/news/Cooperation-urgently-required-to-ensure-a-future-for-West-African-fisheries/':('Blogs', 'Protect the Environment', 'Oceans', 'Fishing', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/news/Climate-change-renewable-energy-municipal-elections-2016/':('Blogs', 'Inspire the Movement', 'Energy', '', 'SouthAfrica', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/News/news/UNESCO-fails-to-protect-Cameroons-Dja-Reserve-from-multiple-threats-including-the-Sudcam-rubber-plantation/':('Blogs', 'Protect the Environment', 'Forest', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/news/Eskom-Accelerates-Looming-Water-Crisis/':('Blogs', 'Protect the Environment', 'Lifestyle', 'Water', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/news/Eskom-Clean-Up-Your-Act/':('Press Release', 'Protect the Environment', 'Energy', 'SouthAfrica', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/news/Eskom-has-failed-South-Africans-its-time-for-new-management/':('Press Release', 'Protect the Environment', 'Energy', 'SouthAfrica', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/News/news/IN-THE-CONGO-BASIN-THE-MYTH-OF-SELECTIVE-LOGGING-BITES-THE-DUST/':('Blogs', '', 'Forest', 'Biodiversity', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/news/Powering-The-Future-Renewable-Energy-Rollout-in-South-Africa/':('Blogs', 'Protect the Environment', 'Energy', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/news/Solar-Kickoff/':('Blogs', 'Inspire the Movement', 'Energy', '', '', 'article', 'Migrate'),
            ####'http://www.greenpeace.org/africa/en/News/news/The-New-Name-Behind-the-threat-to-Cameroons-Forests/':('Blogs', 'Protect the Environment', 'Forest', 'Cameroon', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/news/The-True-Cost-of-Coal/':('Publications', 'Inspire the Movement', 'Energy', 'Coal', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/news/The-True-Cost-of-Nuclear-Energy/':('Publications', 'Protect the Environment', 'Energy', 'Nuclear', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/News/news/UNESCO-fails-to-protect-Cameroons-Dja-Reserve-from-multiple-threats-including-the-Sudcam-rubber-plantation/':('Blogs', 'Protect the Environment', 'Forest', 'Cameroon', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/news/Zuma-Must-Not-Get-Caught-in-a-Nuclear-Trap/':('Blogs', 'Protect the Environment', 'Energy', 'Nuclear', 'SouthAfrica', 'article', 'Migrate'),
            ####'http://www.greenpeace.org/africa/en/News/news/Can-we-count-on-Jeff-to-deliver-renewable-energy/':('Blogs', 'Protect the Environment', 'Energy', 'Coal', 'SouthAfrica', 'article', 'Migrate'),
            ####'http://www.greenpeace.org/africa/en/News/news/Poisoned-Sugar-Exposes-Kenyas-Broken-Food-System/':('Blogs', 'Protect the Environment', 'Farming', 'Food', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/News/news/Six-Renewable-Energy-Myths-Busted/ ':('Blogs', 'Protect the Environment', 'Energy', '', '', 'article', 'Migrate'),

            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/--Greenpeace-and-Guinea-Bissau-authorities-arrest-fishing-vessels/':('Press Release', 'Protect the Environment', 'Oceans', 'Fishing', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/-Greenpeaces-Project-Sunshine-delivers-in-Diepsloot/':('Press Release', 'Protect the Environment', 'Energy', 'SouthAfrica', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/10-more-steps-back-for-Eskom-on-the-precipice-of-Molefes-return/':('Press Release', 'Protect the Environment', 'Energy', 'SouthAfrica', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/13-infractions-found-in-twenty-days/':('Press Release', 'Protect the Environment', 'Oceans', 'Fishing', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/3-Retailers-commit-to-Lobby-for-Renewable-Energy/':('Press Release', 'Protect the Environment', 'Energy', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/4-illegal-fishing-cases-found-Sierra-Leone/':('Press Release', 'Protect the Environment', 'Oceans', 'Fishing', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Activists-close-down-the-Department-of-Environmental-Affairs-Pretoria/':('Press Release', 'Protect the Environment', 'Energy', 'Nuclear', 'Coal', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/African-farmers-embark-on-4-day-journey-to-demand-investment-in-ecological-farming/':('Press Release', 'Protect the Environment', 'Farming', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Africans-want-the-continent-to-BreakFree-from-fossil-fuels/':('Press Release', 'Inspire the Movement', 'Energy', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Africas-largest-Wind-farm-will-reduce-reliance-on-fossil-fuels-in-Kenya/':('Press Release', 'Protect the Environment', 'Energy', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/An-irrational-IRP-can-expect-legal-challenge-from-human-rights-organisations/':('Press Release', 'Protect the Environment', 'Energy', 'SouthAfrica', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Chinese-companies-subsidies-cancelled-permits-removed-for-illegal-fishing-in-West-Africa/':('Press Release', 'Protect the Environment', 'Oceans', 'Fishing', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Civil-society-rejects-IRP-base-case-scenario-unreservedly-/':('Press Release', 'Protect the Environment', 'Energy', 'Coal', 'Nuclear', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Climate-change-and-a-failing-food-system-armyworm-pest/':('Press Release', 'Protect the Environment', 'Farming', 'Food', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Climate-outcast-Trump-surrenders-US-global-leadership---Greenpeace/':('Press Release', 'Inspire the Movement', 'Energy', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Commission-slams-weak-implementation-of-EU-law-against-illegal-logging/':('Press Release', 'Protect the Environment', 'Forest', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Congolese-officials-stop-Greenpeace-Africa-awareness-campaign/':('Press Release', 'Protect the Environment', 'Forest', '', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/conviction-besingi-judicial-harrassment-Greenpeace/':('Press Release', 'Protect the Environment', 'Farming', 'Lifestyle', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Destroying-Kenyas-Ecosystem-destroys-Livelihood-says-Greenpeace/':('Press Release', 'Protect the Environment', 'Forest', 'Kenya', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Donors-Dish-out-Millions-while-the-DRC-government-ups-the-moratorium-breaches/':('Press Release', 'Protect the Environment', 'Forest', 'DRC', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/DRC-Forest-Minister-seeking-to-allocate-an-area-the-size-of-Belgium-for-industrial-logging/':('Press Release', 'Protect the Environment', 'Forest', 'DRC', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/DRC-must-halt-plans-to-open-up-second-largest-rainforest-to-loggers/':('Press Release', 'Protect the Environment', 'Forest', 'DRC', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/DRC-reinstates-illegal-logging-concessions-breaching-its-own-moratorium/':('Press Release', 'Protect the Environment', 'Forest', 'DRC', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/DRC-threatens-to-open-worlds-second-largest-rainforest-to-new-industrial-loggers/':('Press Release', 'Protect the Environment', 'Forest', 'DRC', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Durban-citizens-join-the-world-in-saying-no-to-single-use-plastics/':('Press Release', 'Protect the Environment', 'Plastics', 'SouthAfrica', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Dutch-court-slams-Fibois-BV-on-Cameroons-Timber/':('Press Release', 'Protect the Environment', 'Forest', 'Cameroon', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Dutch-impose-sanctions-for-violation-of-EU-timber-regulations/':('Press Release', 'Protect the Environment', 'Forest', '', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/eactive-on-the-latest-developments-regarding-Virunga-and-Salonga-National-Parks-in-the-DRC/':('Press Release', 'Protect the Environment', 'Forest', 'Energy', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Ecological-farmers-teach-methods-to-face-drought-to-conventional-farmers/':('Press Release', 'Protect the Environment', 'Farming', 'Water', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Ensure-Safe-and-Healthy-Food-for-Citizens-Greenpeace-Africa-Urges-Kenyas-Government/':('Press Release', 'Protect the Environment', 'Farming', 'Food', 'Kenya', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/eskom-anti-renewables-campaign/':('Press Release', 'Protect the Environment', 'Energy', 'Coal', 'SouthAfrica', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Farmers-against-SGSOC/':('Press Release', 'Protect the Environment', 'Forest', 'Cameroon', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Fraud-on-the-gross-tonnage-by-industrial-fishing-vessels/':('Press Release', 'Protect the Environment', 'Oceans', 'Fishing', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Fukushima-5-years-on-South-Africa-prioritizes-nuclear-over-economy-and-education-1/':('Press Release', 'Protect the Environment', 'Energy', 'Nuclear', 'SouthAfrica', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Funeral-Procession-outside-the-Department-of-Energy-to-highlight-the-impacts-of-Fossil-Fuels/':('Press Release', 'Protect the Environment', 'Energy', 'Lifestyle', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Georgia-Court-Agrees-with-Greenpeace-Transfers-Logging-Companys-RICO-Case-to-Northern-California/':('Press Release', 'Protect the Environment', 'Forest', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-activists--protested-at-ANAMs-offices-to-demand-the-complete-re-calculation-of-fishing-vessels-tonnage-in-Senegal/':('Press Release', 'Protect the Environment', 'Fishing', 'Senegal', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Africa-and-stakeholders-discuss-solutions-to-ailing-forest-management-in-Cameroon/':('Press Release', 'Protect the Environment', 'Forest', 'Cameroon', '', 'article', 'Migrate'),
            ####'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Africa-Applauds-Kitui-County-Government-for-Setting-Aside-Funds-Towards-Climate-Change-Adaptation/':('Press Release', 'Protect the Environment', 'Energy', 'Kenya', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Africa-calls-For-a-Thorough-Investigation-into-the-Death-of-8--Rhinos/':('Press Release', 'Protect the Environment', 'Forest', 'AboutUs', '', 'article', 'Migrate'),

            ####B3####
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Africa-calls-for-a-total-ban-on-illegal-logging/':('Press Release', 'Protect the Environment', 'Forest', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Africa-calls-on-President-Cyril-Ramaphosa-to-act-on-energy/':('Press Release', 'Protect the Environment', 'Energy', 'SouthAfrica', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Africa-commends-Uganda-for-the-ban-on-plastic-bags/':('Press Release', 'Protect the Environment', 'Plastics', 'Kenya', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Africa-critiques-the-budget-speech-failure-to-support-a-new-energy-future-/':('Press Release', 'Protect the Environment', 'Energy', 'AboutUs', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Africa-Executive-Director-calls-for-Peatland-protection-after-visit-to-DR-Congo/':('Press Release', 'Protect the Environment', 'Forest', 'AboutUs', '', 'article', 'Migrate'),
            ####'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Africa-expresses-shock-over-Wijma-activities-in-Cameroon/':('Press Release', 'Protect the Environment', 'Forest', 'Cameroon', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Africa-in-Solidarity-with-Nakuru-Residents-/':('Press Release', 'Inspire the Movement', 'AboutUs', 'Lifestyle', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Africa-in-total-solidarity-with-the-People-of-Sierra-Leone/':('Press Release', 'Inspire the Movement', 'Oceans', 'Lifestyle', 'AboutUs', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Africa-instils-forest-values-to-youths-during-the-5th-World-Forest-Day-commemoration/':('Press Release', 'Protect the Environment', 'Forest', 'Activism', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Africa-Launches-Online-Campaign-Platform-to-strengthen-Environmental-activism-in-Africa/':('Press Release', 'Protect the Environment', 'Activism', '', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Africa-opens-pilot-green-space-in-Yaounde/':('Press Release', 'Protect the Environment', 'Forest', 'Lifestyle', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Africa-renewable-energy-deals-a-step-towards-a-just-energy-transition/':('Press Release', 'Protect the Environment', 'Energy', 'SouthAfrica', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Africa-Responds-to-Minister-of-Environment-and-Sustainable-Development-Amy-Ambatobe/':('Press Release', 'Protect the Environment', 'Forest', '', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Africa-responds-to-PIDMA-Cameroon-importing-1000-tons-of-corn-seeds/':('Press Release', 'Protect the Environment', 'Farming', 'Food', 'Cameroon', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Africa-response-to-the-coal-truck-driver-strike-action-in-Tshwane/':('Press Release', 'Protect the Environment', 'Lifestyle', 'Coal', 'SouthAfrica', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Africa-Urges-Halcyon-Agri-to-Stop-Destroying-Livelihood--Biodiversity-in-Cameroon/':('Press Release', 'Protect the Environment', 'Biodiversity', 'Lifestyle', 'Cameroon', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Africa-Urges-Machakos-County-Government-to-Allocate-Budget-Towards-Sustainable-Farming/':('Press Release', 'Protect the Environment', 'Farming', 'Kenya', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Africa-urges-NEMA-to-enforce-Plastic-ban/':('Press Release', 'Protect the Environment', 'Plastics', 'Kenya', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Africa-volunteers-urging-corporations-to-stop-single-use-plastic/':('Press Release', 'Protect the Environment', 'Plastics', 'Cameroon', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Africa-welcomes-Kenyas-stance-on-Lamu-Coal-Power-Plant/':('Press Release', 'Protect the Environment', 'Energy', 'Coal', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Africa-Welcomes-Move-to-Ban-Plastic-Bags-in-Kenya-/':('Press Release', 'Protect the Environment', 'Plastics', 'Kenya', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Africas-Executive-Director-Wins-a-Prestigious-Human-Rights-Award/':('Press Release', 'Protect the Environment', 'AboutUs', 'GreenpeaceAfrica', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-asks-for-investigation-of-the-Modern-Express-cargo/':('Press Release', 'Inspire the Movement', 'Forest', '', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-briefing-to-the-21st-Session-of-the--Fishery-Committee-for-the-Eastern-Central-Atlantic-/':('Press Release', 'Protect the Environment', 'Fishing', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-calls-for-decrease-in-meat-and-dairy-production-and-consumption-for-a-healthier-planet/':('Press Release', 'Protect the Environment', 'Lifestyle', 'Food', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-calls-on-AGRF-to-rethink-its-Approach-to-Agriculture-in-Africa/':('Press Release', 'Protect the Environment', 'Forest', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-challenges-Shoprite-shareholders-to-engage-on-renewable-energy/':('Press Release', 'Protect the Environment', 'Energy', 'SouthAfrica', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-condemns-appointment-of-Matshela-Koko-as-Acting-Eskom-CEO/':('Press Release', 'Protect the Environment', 'Energy', 'SouthAfrica', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-condemns-deportation-of-French-filmmaker--and-cancellation-of-employees-visa-in-the-DRC/':('Press Release', 'Protect the Environment', 'Forest', 'Lifestyle', 'DRC', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-demands-that-Shell-and-Sasol-show-up-at-climate-change-and-human-rights-inquiry1/':('Press Release', 'Inspire the Movement', 'Energy', '', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Exposes-Logging-Companys-Attack-on-Free-Speech-in-New-Report/':('Press Release', 'Inspire the Movement', 'Forest', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-hopes-for-stability-and-consistency-for-South-Africas-energy-future/':('Press Release', 'Protect the Environment', 'Energy', 'SouthAfrica', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-implores-President-to-declare-Cape-Town-a-national-disaster/':('Press Release', 'Protect the Environment', 'Water', 'Lifestyle', 'SouthAfrica', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Michelin-Zero-Deforestation-Commitment/':('Press Release', 'Inspire the Movement', 'Forest', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-President-Ramaphosa-yet-to-take-decisive-action-on-energy/':('Press Release', 'Protect the Environment', 'Energy', 'Nuclear', 'SouthAfrica', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-ranks-Pick-n-Pay-Massmart-Spar-Woolworths-and-Shoprite-on-commitments-to-a-100-renewable-energy-vision/':('Press Release', 'Protect the Environment', 'Energy', '', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-reaction-plastic-bag-ban-Senegal/':('Press Release', 'Protect the Environment', 'Plastics', 'Senegal', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Reaction-to-Microplastic-Pollution-on-South-Africas-Tap-Water-The-Scourge-of-Plastic-Pollution-is-a-Living-Reality/':('Press Release', 'Protect the Environment', 'Water', 'Plastics', 'SouthAfrica', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-reacts-to-Zumas-late-night-cabinet-reshuffle/':('Press Release', 'Protect the Environment', 'Lifestyle', 'Energy', 'SouthAfrica', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-reveal-new-cases-of-bad-fishing-practices-in-West-Africa/':('Press Release', 'Protect the Environment', 'Oceans', 'Fishing', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-ship-arrives-for-the-first-time-in-Cameroon-with-a-message-for-the-protection-of-the-Congo-Basin-forest-/':('Press Release', 'Protect the Environment', 'Oceans', '', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-ship-MY-Esperanza-sails-into-West-Africa-waters/':('Press Release', 'Protect the Environment', 'Oceans', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/greenpeace-slams-eskom-renewable-energy/':('Press Release', 'Protect the Environment', 'Energy', 'SouthAfrica', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-slams-nuclear-power-station-authorisation/':('Press Release', 'Inspire the Movement', 'Energy', 'Nuclear', 'SouthAfrica', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-welcomes-Brian-Molefes-resignation-as-CEO-of-Eskom/':('Press Release', 'Protect the Environment', 'Energy', 'SouthAfrica', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-welcomes-the-announcement-of-the-DRC--Minister-of-Environment-to-cancel-illegal-concessions--but-says-more-needs-to-be-done/':('Press Release', 'Protect the Environment', 'Forest', 'DRC', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/How-Cameroons-Stolen-Wood-Reaches-International-Markets/':('Press Release', 'Protect the Environment', 'Forest', 'Cameroon', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/How-the-DRC-government-has-secretly-breached--its-own-logging-moratorium/':('Press Release', 'Protect the Environment', 'Forest', 'DRC', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Kenya-Needs-to-Diversity-Energy-Sources-to-Reduce-Electricity-Cost/':('Press Release', 'Inspire the Movement', 'Energy', 'Coal', 'Kenya', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Kenyas-Youths-Demand-Big-Corporations-to-Stop-Single-Use-Plastics/':('Press Release', 'Protect the Environment', 'Oceans', 'Plastics', 'Kenya', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Lannulation-de-trois-concessions-forestieres-illegales-en-RDC-est-un-premier-pas-essentiel-mais-pas-suffisant-selon-Greenpeace-Afrique/':('Press Release', 'Protect the Environment', 'Forest', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Light-at-the-end-of-the-tunnel/':('Press Release', 'Inspire the Movement', 'Energy', 'Nuclear', 'SouthAfrica', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Lost-health-and-homes-the-legacies-of-Chernobyl-and-Fukushima/':('Press Release', 'Inspire the Movement', 'Energy', 'Nuclear', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Massive-irregular-expenditure-at-Department-of-Water-and-Sanitation-outrageous/':('Press Release', 'Protect the Environment', 'Water', 'SouthAfrica', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Minister-of-Energy-makes-the-first-move-to-break-renewable-energy-stalemate/':('Press Release', 'Inspire the Movement', 'Energy', 'SouthAfrica', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/More-than-180-000-people-send-a-petition-to-the-President-of-Cameroon--to-put-an-end-to-SGSOC-oil-palm-plantation/':('Press Release', 'Protect the Environment', 'Forest', 'Cameroon', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Njeri-Kabeberi-appointed-as-Greenpeace-Africa-Executive-Director/':('Press Release', '', 'AboutUs', 'GreenpeaceAfrica', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/No-room-for-secrecy/':('Press Release', 'Inspire the Movement', 'Energy', 'Coal', 'SouthAfrica', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Norwegian-and-French-governments-threatens-worlds-second-largest-tropical-rainforest/':('Press Release', 'Protect the Environment', 'Forest', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Nuclear-plans-for-South-Africa-will-face-resistance-at-all-levels/':('Press Release', 'Inspire the Movement', 'Energy', 'Nuclear', 'SouthAfrica', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Project_Sunshine/':('Publications', 'Change My Community', 'Lifestyle', 'SouthAfrica', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Proposed-Critical-Infrastructure-Protection-Bill-Unconstitutional/':('Publications', 'Inspire the Movement', 'Activism', 'SouthAfrica', '', 'article', 'Migrate'),

            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Publications/Africas-forests-under-threat-/':('Publications', 'Protect the Environment', 'Forest', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Publications/Africas-Forests-Under-Threat/':('Publications', 'Protect the Environment', 'Forest', 'GreenpeaceAfrica', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Publications/Crisis-for-FSC-in-the-Congo-Basin/':('Publications', 'Protect the Environment', 'Forest', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Publications/Cut-from-Congo-/':('Publications', 'Protect the Environment', 'Forest', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Publications/Deepening-green-roots-in-Africa-/':('Publications', '', 'AboutUs', '', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Publications/DRC-Donors-Release-40-million-dollars-after-illegal-award-of-4000km2-of-forest/':('Publications', 'Protect the Environment', 'Forest', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Publications/Embracing-Change-Shaping-the-Future/':('Publications', '', 'AboutUs', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Publications/Financing-Ecological-Farming-in-Africa/':('Publications', 'Protect the Environment', 'Farming', '', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Publications/Herakles-FarmsSGSOC-The-chaotic-history-of-destructive-palm-oil-project-in-Cameroon/':('Publications', 'Protect the Environment', 'Forest', 'Cameroon', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Publications/Hope-in-West-Africa-Ship-Tour-Briefer/':('Publications', 'Inspire the Movement', 'Oceans', '', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Publications/How-the-DRC-government-has-secretly-breached-its-own-logging-moratorium/':('Publications', 'Protect the Environment', 'Forest', 'DRC', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Publications/Irresponsible-Investment--Agricas-Broken-Development-Model-in-Tanzania/':('Publications', 'Protect the Environment', 'Farming', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Publications/La-Socamba/':('Publications', 'Protect the Environment', 'Forest', 'Cameroon', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Publications/License-to-Kill/':('Publications', 'Protect the Environment', 'Energy', 'Coal', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Publications/Norway-and-France-threaten-DRCs-forests/':('Publications', 'Protect the Environment', 'Forest', 'DRC', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Publications/ResilienceReports/':('Publications', 'Protect the Environment', 'Farming', '', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Publications/SGSOCS-Social-Investments-A-Cemetery-of-Broken-Promises/':('Publications', 'Protect the Environment', 'Forest', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Publications/Shopping-Clean-Retailers-and-Renewable-Energy-/':('Publications', 'Protect the Environment', 'Biodiversity', 'SouthAfrica', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Publications/Shopping-Clean/':('Publications', 'Protect the Environment', 'Biodiversity', 'SouthAfrica', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Publications/The-Cost-of-Ocean-Destruction/':('Publications', 'Protect the Environment', 'Oceans', 'Fishing', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Publications/The-Great-Water-Grab/':('Publications', 'Inspire the Movement', 'Energy', 'Coal', 'Water', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Publications/Turning-REDD-into-Green/':('Publications', 'Protect the Environment', 'Forest', 'DRC', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Publications/UMOJA---Supporter-Newsletter/':('Publications', 'Inspire the Movement', 'GreenpeaceAfrica', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Publications/UMOJA-JAN-2018/':('Publications', 'Inspire the Movement', 'GreenpeaceAfrica', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Publications/UMOJA-sept2017_issue04/':('Publications', 'Inspire the Movement', 'GreenpeaceAfrica', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Publications/Water-Hungry-Coal/':('Publications', 'Protect the Environment', 'Energy', 'Coal', 'SouthAfrica', 'article', 'Migrate'),

            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Recent-engagements-between-Minister-of-Energy-and-civil-society-organisations/':('Press Release', 'Inspire the Movement', 'Energy', 'SouthAfrica', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Republic-of-Congo-and-Democratic-Republic-of-Congo-must-translate-words-into-action-to-ensure-the-protection-of--peatlands/':('Press Release', 'Protect the Environment', 'Forest', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Revelations-on--Bollore-groups-investment--in-plantations-in-Africa/':('Press Release', 'Protect the Environment', 'Forest', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/SA-pays-the-price-The-Denton-Deception/':('Press Release', 'Inspire the Movement', 'Energy', 'Coal', 'SouthAfrica', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Sabotaging-renewable-energy-will-continue-to-cost-South-Africans/':('Press Release', 'Inspire the Movement', 'Energy', 'Coal', 'SouthAfrica', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Scientists-confirm-presence-of-peatlands-in-the-Democratic-Republic-of-Congo/':('Press Release', 'Protect the Environment', 'Forest', '', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Shark-fins-found-aboard-foreign-fishing-vessels-during-Greenpeace---Guinea-patrol/':('Press Release', 'Protect the Environment', 'Oceans', 'Fishing', 'GreenpeaceAfrica', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/SONA-exposes-lack-of-leadership-on-key-environmental-issues-Greenpeace/':('Press Release', 'Protect the Environment', 'Water', 'Coal', 'SouthAfrica', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Standard-Bank-Sets-The-Record-Straight-on-Financing-Lamu/':('Press Release', 'Inspire the Movement', 'Energy', 'Coal', 'Kenya', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/State-Capture-and-irrational-choices-at-the-heart-of-South-Africas-energy-woes/':('Press Release', 'Inspire the Movement', 'Energy', 'Coal', 'SouthAfrica', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Statement-on-the-announcement-that-the-government-of-Democratic-Republic-of-Congo-has-started-a-process-to-lift-its-moratorium-on-the-allocation-of-new-logging-concessions/':('Press Release', 'Protect the Environment', 'Forest', 'DRC', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Statoil-exploration-threatens-biodiversity-of-Algoa-Bay1/':('Press Release', 'Protect the Environment', 'Energy', 'Biodiversity', 'SouthAfrica', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/strong-recommendations-to-West-African-states/':('Press Release', 'Protect the Environment', 'Fishing', 'Senegal', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/The-gaps-and-omissions-in-the-CCT-audit-report-by-Cameroons-Ministry-of-Forestry-brings-to-light-the-need-for-an-Independent-Forest-Monitor/':('Press Release', 'Protect the Environment', 'Forest', 'Cameroon', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/UK-sanctions-Cameroon-timber-traders-for-EU-violations/':('Press Release', 'Protect the Environment', 'Forest', 'Cameroon', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Urgent-action-needed-to-solve-West-African-food-security-threat/':('Press Release', 'Protect the Environment', 'Oceans', 'Fishing', 'Senegal', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/US-Legislators-add-voice-to-Kenyas-Anti-coal-Campaign---could-this-be-the-last-straw/':('Press Release', 'Inspire the Movement', 'Energy', 'Kenya', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Will-you-marry-the-sun/':('Press Release', 'Inspire the Movement', 'Energy', 'SouthAfrica', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Woolworths-Massmart-and-Pick-n-Pay-get-tops-on-Renewable-Energy-Shoprite-scores-last-again-Greenpeace/':('Press Release', 'Inspire the Movement', 'Energy', 'SouthAfrica', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/World-Water-Day-Greenpeace-demands-more-commitment-to-defend-South-African-peoples-right-to-water/':('Press Release', 'Protect the Environment', 'Water', 'Conservation', 'SouthAfrica', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Worlds-coal-power-plants-consume-enough-freshwater-to-sustain-1-billion-people---Greenpeace/':('Press Release', 'Inspire the Movement', 'Energy', 'Coal', 'GreenpeaceAfrica', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Youths-demand-a-better-Farming-System-as-Kenya-Celebrates-World-Food-Day/':('Blogs', 'Change My Community', 'Farming', 'Food', 'Kenya', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Life-After-Coal-and-Greenpeace-Africa-Slam-Inclusion-of-New-Coal-in-Electricity-Plan/':('Press Release', 'Protect the Environment', 'Energy', 'Coal', 'SouthAfrica', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Jeff-Radebe-will-Monday-be-it---Greenpeace-Africa/':('Press Release', 'Protect the Environment', 'Energy', 'Coal', 'SouthAfrica', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Food-Safety-Should-be-Prioritised-in-Kenyattas-Big-Four-Agenda-Greenpeace-Africa/':('Press Release', 'Protect the Environment', 'Farming', 'Food', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Message-from-Greenpeace-Africa-Executive-Director-on-the-passing-of-former-UN-Secretary-General-Kofi-Annan/':('Press Release', 'Inspire the Movement', 'AboutUs', 'GreenpeaceAfrica', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Jeff-where-is-the-IRP/':('Press Release', 'Protect the Environment', 'Energy', 'SouthAfrica', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Africa-Applauds-Kitui-County-Government-for-Setting-Aside-Funds-Towards-Climate-Change-Adaptation/':('Press Release', 'Protect the Environment', 'Conservation', 'Food', 'Kenya', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/Press-Centre-Hub/Greenpeace-Africa-expresses-shock-over-Wijma-activities-in-Cameroon/':('Press Release', 'Protect the Environment', 'Forest', 'Cameroon', '', 'article', 'Migrate'),

            #'http://www.greenpeace.org/africa/en/getinvolved/cancel-eskoms-application-to-pollute-freely1/': (
            #'Blogs', 'Protect the Environment', 'Energy', 'Coal', 'SouthAfrica', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/en/getinvolved/cyberactivist/':('Blogs', 'Inspire the Movement', 'Activism', '', '', 'article', 'Migrate')
        }

        # FR Post list.

        start_urls = {
            ####'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/alors-que-la-rdc-sapproche-des-lections-natio/blog/61772/':('', '', 'AboutUs', '', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/2016-lanne-o-on-dit-adieu-au-charbon/blog/55503/':('Blogs', 'Inspirer le Mouvement', 'Energie', 'Charbon', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/45-ans-de-pouvoir-citoyen/blog/57508/':('Blogs', '', 'GreenpeaceAfrica', 'Activisme', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/5-resolutions-oceans-plastiques/blog/55257/':('Blogs', 'Inspirer le Mouvement', 'Plastiques', 'Océans', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/afrique-besoin-FiTI/blog/55554/':('Blogs', "Protéger l'Environnement",'Océans','Pêche','','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/afrique-de-louest-entre-beaut-et-nature-foiso/blog/59388/':('Blogs', "Protéger l'Environnement",'Océans','Pêche','','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/alors-que-la-rdc-sapproche-des-lections-natio/blog/61772/':('Blogs', "Protéger l'Environnement",'Forêts','Biodiversité','RDC','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/billet-de-blogue-par-ahmed-diame-charg-de-cam/blog/61267/':('Blogs', "Protéger l'Environnement",'Océans','Pêche','','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/breakfree2016-une-vague-mondiale-sans-prcdent/blog/56472/':('Blogs', 'Inspirer le Mouvement', 'Energie', '', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/cecaf-des-resultats-mitiges/blog/56316/':('Blogs', "Protéger l'Environnement",'Océans','Pêche','','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/comment-les-poursuites-judiciaires-visent-bil/blog/59449/':('Blogs', "Protéger l'Environnement",'Forêts','Activisme','','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/cooperer-vaincre-changement-climatique/blog/56267/':('Blogs', 'Inspirer le Mouvement', 'GreenpeaceAfrica', '', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/cot-sur-coup/blog/60809/':('Blogs', "Protéger l'Environnement",'Océans','Pêche','','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/delwyn-le-super-hro-de-durban/blog/55553/':('Blogs', 'Inspirer le Mouvement', 'Activisme', '', 'AfriqueduSud', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/des-poissons-qui-tombent-du-ciel-des-filets-v/blog/59228/':('Blogs', "Protéger l'Environnement",'Océans','Pêche','','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/eliane-volontaire-universit-yaounde/blog/58192/':('Blogs', 'Inspirer le Mouvement', 'Activisme', '', 'Cameroun', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/ensemble-construisons-des-ponts-pas-des-murs/blog/58535/':('Blogs', '', 'JusticeSociale', '', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/essais-nuclaires-ou-le-mirage-de-la-scurit/blog/57385/':('Blogs', 'Inspirer le Mouvement', 'Nucléaire', '', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/exploitation-ptrolire-et-gazire-au-sngal-de-n/blog/61603/':('Blogs', 'Inspirer le Mouvement', 'Energie', '', 'Sénégal', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/flotte-chinoise-afrique-ouest/blog/58634/':('Blogs', "Protéger l'Environnement",'Océans','Pêche','','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/forts-les-victoires-de-lanne-2016/blog/58219/':('Blogs', "Protéger l'Environnement",'Forêts','Biodiversité','','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/forts-libert-dexpression-des-auteurs-sengagen/blog/59555/':('Blogs', "Protéger l'Environnement",'Forêts','','','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/grand-nettoyage-de-printemps-en-guine/blog/59192/':('Blogs', 'Inspirer le Mouvement', 'Activisme', '', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/greenpeace-adresse-ses-condolances-aux-famill/blog/57619/':('Blogs', 'Inspirer le Mouvement', '', '', 'RDC', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/greenpeace-retire-strategie-huile-palme-Cameroun/blog/56715/':('Blogs', "Protéger l'Environnement",'Forêts','','Cameroun','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/ibrahima-engage-volontaire-environnement/blog/57229/':('Blogs', 'Inspirer le Mouvement', 'Activisme', '', 'Sénégal', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/jai-vu-de-mes-propres-yeux-le-pillage-de-nos-/blog/59390/':('Blogs', "Protéger l'Environnement",'Océans','Pêche','','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/joal-suffoquee-usines-farine-poissons/blog/56770/':('Blogs', "Protéger l'Environnement",'Océans','Pêche','Sénégal','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/les-dfis-de-la-coopration-rgionale-dans-la-lu/blog/57552/':('Blogs', "Protéger l'Environnement",'Océans','Pêche','Sénégal','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/les-forts-du-bassin-du-congo-nous-ont-fait-da/blog/60621/':('Blogs', "Protéger l'Environnement",'Forêts','','','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/les-navires-de-greenpeace-les-combattants-de-/blog/58724/':('Blogs', "Protéger l'Environnement",'Océans','','','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/les-photos-qui-ont-donn-envie-des-millions-de/blog/57310/':('Blogs', '', 'GreenpeaceAfrica', '', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/les-terres-devraient-nous-unir-pas-nous-oppos/blog/60091/':('Blogs', "Protéger l'Environnement",'Forêts','JusticeSociale','RDC','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/lexploitation-forestire-industrielle-ou-le-ri/blog/59409/':('Blogs', "Protéger l'Environnement",'Forêts','','RDC','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/m-le-ministre-rectifiez-tir/blog/56125/':('Blogs', "Protéger l'Environnement",'Océans','Pêche','Sénégal','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/ma-nuit-bord-dun-bateau-de-pche-chinois-en-af/blog/59227/':('Blogs', "Protéger l'Environnement",'Océans','Pêche','','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/manger-moins-viande-pour-planete/blog/56751/':('Blogs', 'Changer ma Communauté', 'Agriculture', 'Modedevie', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/merci-pour-cet-incroyable-voyage/blog/55229/':('Blogs', '', 'GreenpeaceAfrica', '', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/nos-oceans-notre-responsabilite/blog/58824/':('Blogs', "Protéger l'Environnement",'Océans','Pêche','','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/notre-anne-2016-en-8-images/blog/58397/':('Blogs', 'Inspirer le Mouvement', 'GreenpeaceAfrica', '', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/notre-expdition-dans-le-bassin-du-congo-fut-u/blog/60762/':('Blogs', "Protéger l'Environnement",'Forêts','','','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/nous-2017-six-bonnes-rsolutions-pour-la-plant/blog/58436/':('Blogs', 'Changer ma Communauté', 'GreenpeaceAfrica', '', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/nouvelles-directrices-greenpeace-international/blog/55440/':('Blogs', '', 'GreenpeaceAfrica', '', '', 'news-list', 'Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/parlement-belge-demande-renforcement-eutr/blog/55442/':('Blogs', "Protéger l'Environnement",'Forêts','','','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/RDC-societe-civile-contre-levee-moratoire/blog/56149/':('Blogs', "Protéger l'Environnement",'Forêts','','RDC','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/rdc-un-silence-complice-des-donateurs-face-au/blog/58648/':('Blogs', "Protéger l'Environnement",'Forêts','','RDC','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/senegal-pcheurs-artisans-prennent-parole/blog/56630/':('Blogs', "Protéger l'Environnement",'Océans','Pêche','Sénégal','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/sngal-vers-une-fin-de-la-fraude-au-tonnage/blog/58221/':('Blogs', "Protéger l'Environnement",'Océans','Pêche','Sénégal','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/socfin-zero-deforestation/blog/57101/':('Blogs', "Protéger l'Environnement",'Forêts','','Cameroun','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/stoppons-SGSOC-plantation-huile-palme/blog/57653/':('Blogs', "Protéger l'Environnement",'Forêts','','Cameroun','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/surveillance-participative-cogestion-peche/blog/56861/':('Blogs', "Protéger l'Environnement",'Océans','Pêche','Sénégal','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/un-anniversaire-sombre-pour-sgsoc/blog/58122/':('Blogs', "Protéger l'Environnement",'Forêts','','Cameroun','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/un-jour-au-port-le-futur-des-ocans-vu-par-les/blog/58926/':('Blogs', "Protéger l'Environnement",'Océans','','','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/un-jour-en-mer-rencontres-avec-la-nature/blog/59079/':('Blogs', "Protéger l'Environnement",'Océans','','','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/un-leadership-regional-pour-une-peche-durable/blog/59212/':('Blogs', "Protéger l'Environnement",'Océans','','','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/une-victoire-pour-nos-forts-michelin-sengage-/blog/56737/':('Blogs', "Protéger l'Environnement",'Forêts','','','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/victoire-amazonie-projet-barrage-tapajos-annule/blog/57204/':('Blogs', "Protéger l'Environnement",'Forêts','','','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/victoire-la-plus-vaste-aire-marine-du-monde-e/blog/58220/':('Blogs', "Protéger l'Environnement",'Océans','Biodiversité','','news-list','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/Blogs-de-Greenpeace-Afrique/virunga-la-soif-de-ptrole-ne-laisse-aucun-rpi/blog/49244/':('Blogs', "Protéger l'Environnement",'Forêts','Biodiversité','RDC','news-list','Migrate'),

            'http://www.greenpeace.org/africa/fr/Actualities/actualites/Alors-que-la-RDC-sapproche-des-elections-nationales-le-gouvernement-cherche-a-convertir-sa-foret-et-sa-faune-sauvage-en-argent-comptant/':('Blogs', "Protéger l'Environnement",'Forêts','Biodiversité','RDC','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Actualities/actualites/Dans-le-Bassin-Du-Congo-le-mythe-de-Lexploitation-selective-du-bois-mord-la-poussiere/':('Blogs', "Protéger l'Environnement",'Forêts','','RDC','article','Migrate'),
            'http://www.greenpeace.org/africa/fr/Actualities/actualites/La-deuxieme-foret-tropicale-au-monde-menacee-par-lhuile-de-palme-et-lexploitation-forestiere/':('Publications', "Protéger l'Environnement",'Forêts','','','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Actualities/actualites/LUNESCO-echoue-a-proteger-la-Reserve-du-Dja-au-Cameroun-de-multiples-menaces-y-compris-la-plantation-dhevea-Sudcam/':('Blogs', "Protéger l'Environnement",'Forêts','','Cameroun','article','Migrate'),

            ##'http://www.greenpeace.org/africa/fr/Presse/180-000-personnes-demandent-au-President-du-Cameroun-une-rupture-de-contrat-avec-SGSOC-/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','Cameroun','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Comment-la-RDC-a-secretement-viole-son-propre-moratoire--sur-lattribution-de-nouvelles-concessions-forestieres/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','RDC','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/condamnation-besingi-reaction-greenpeace/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','Cameroun','article','Migrate'),
            'http://www.greenpeace.org/africa/fr/Presse/Conference-coalition-acteurs-peche/':('Communiqués de presse', "Protéger l'Environnement",'Océans','Pêche','Sénégal','article','Migrate'),
            'http://www.greenpeace.org/africa/fr/Presse/Congolese-officials-stop-Greenpeace-Africa-awareness-campaign/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Des-ailerons-de-requins-trouves-a-bord-de-navires-de-peche-etrangers-au-cours-dune-patrouille-conjointe-Greenpeace---Guinee/':('Communiqués de presse', "Protéger l'Environnement",'Océans','Pêche','','article','Migrate'),
            'http://www.greenpeace.org/africa/fr/Presse/Des-militants-de-Greenpeace-ont-proteste-devant-les-locaux-de-lANAM-pour-exiger-le-re-jaugeage-complet-des-navires-de-peche-au-Senegal/':('Communiqués de presse', "Protéger l'Environnement",'Océans','Pêche','Sénégal','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/des-recommandations-fortes-pour-les-etats-ouest-africains/':('Communiqués de presse', "Protéger l'Environnement",'Océans','Pêche','','article','Migrate'),
            'http://www.greenpeace.org/africa/fr/Presse/Enquete-sur-les-investissements-du-groupe-Bollore-dans-des-plantations-africaines/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','RDC','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Fraud-sur-le-Tonnage-des-Navires-de-Peche-Industriels/':('Communiqués de presse', "Protéger l'Environnement",'Océans','Pêche','Sénégal','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Greenpeace-21e-COPACE/':('Communiqués de presse', "Protéger l'Environnement",'Océans','Pêche','','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Greenpeace-Africa-exhorte-Halcyon-Agri-a-stopper-la-destruction-des-moyens-de-subsistance-des-communautes-et-la-biodiversite-au-Cameroun-/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','Biodiversité','Cameroun','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Greenpeace-Africa-inculque-les-valeurs-de-la-foret-aux-jeunes-pendant-la-commemoration-de-la-5eme-edition-de-la-journee-internationale-de-la-foret/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','Cameroun','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Greenpeace-Africa-repond-a-PIDMA-Cameroun-en-important-1000-tonnes-de-semences-de-mais/':('Communiqués de presse', 'Changer ma Communauté', 'Agriculture', '', 'Cameroun', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Greenpeace-Africa-repond-au-Ministre-de-lEnvironnement-et-du-Developpement-Durable-Amy-Ambatobe/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','RDC','article','Migrate'),
            'http://www.greenpeace.org/africa/fr/Presse/Greenpeace-Africa-repond-aux-fuites-en-Afrique-de-lOuest/':('Communiqués de presse', 'Inspirer le Mouvement', 'Activisme', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/fr/Presse/Greenpeace-Afrique-appelle-a-une-meilleure-protection-des-defenseurs-de-lenvironnement-/':('Communiqués de presse', 'Inspirer le Mouvement', 'Activisme', '', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Greenpeace-Afrique-en-totale-solidarite-avec-le-Peuple-de-la-Sierra-Leone/':('Communiqués de presse', '', '', '', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Greenpeace-Afrique-et-ses-partenaires-examinent-des-solutions-face-a-la-mauvaise-gestion-des-forets-au-Cameroun/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','Cameroun','article','Migrate'),
            'http://www.greenpeace.org/africa/fr/Presse/Greenpeace-Afrique-exprime-son-desarroi-face-aux-activites-de-Wijma-au-Cameroun/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','Cameroun','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Greenpeace-Afrique-lance-une-plateforme-de-campagne-en-ligne-pour-renforcer-lactivisme-environnemental-en-Afrique/':('Communiqués de presse', 'Inspirer le Mouvement', 'GreenpeaceAfrica', 'Activisme', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Greenpeace-Afrique-ouvre-un-espace-vert-pilote-a-Yaounde/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','Cameroun','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Greenpeace-condamne-lexpulsion-dun-realisateur-francais--et-lannulation-du-visa-dun-employe-par-la-RDC/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','Activisme','RDC','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Greenpeace-demande-enquete-cargaison-Modern-Express/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','','article','Migrate'),
            'http://www.greenpeace.org/africa/fr/Presse/Greenpeace-invite-les-presidents-senegalais-et-mauritanien-a-oeuvrer-pour-une-gestion-regionale-de-la-peche-en-Afrique-de-lOuest/':('Communiqués de presse', "Protéger l'Environnement",'Océans','Pêche','Sénégal','article','Migrate'),
            'http://www.greenpeace.org/africa/fr/Presse/Greenpeace-Michelin-adopte-une-politique-Zero-Deforestation/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','','article','Migrate'),
            'http://www.greenpeace.org/africa/fr/Presse/Greenpeace-nouveaux-cas-mauvaises-pratiques-peche-Afrique-Ouest/':('Communiqués de presse', "Protéger l'Environnement",'Océans','Pêche','','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Greenpeace-salue-lannonce-du-Ministre-de-lEnvironnement-de-la-RDC-dannuler-les-concessions-forestieres-illegales--mais-demande-a-ce-que-plus-soit-fait/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','RDC','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/La-Chine-suspend-les-subventions-et-retire-la-licence-a-des-compagnies-impliquees-dans-des-activites-de-peche-illegale-en-Afrique-de-lOuest/':('Communiqués de presse', "Protéger l'Environnement",'Océans','Pêche','','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/La-directrice-executive-de-Greenpeace-Afrique-remporte-un-prestigieux-prix-des-droits-de-lHomme-/':('Communiqués de presse', '', 'GreenpeaceAfrica', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/fr/Presse/La-Grande-Bretagne-sanctionne-des-importateurs-de-bois-provenant-du-Cameroun/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','Cameroun','article','Migrate'),
            'http://www.greenpeace.org/africa/fr/Presse/La-RDC-menace-douvrir-la-deuxieme-plus-grande-foret-tropicale-du-monde-a-de-nouveaux-exploitants-industriels/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','RDC','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/La-Republique-du-Congo-et-la-Republique-Democratique-du-Congo-doivent-traduire-les-paroles-en-actes-pour-assurer-la-protection-des-tourbieres/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','RDC','article','Migrate'),
            'http://www.greenpeace.org/africa/fr/Presse/La-Socfin-publie-enfin-une-politique-Zero-Deforestation/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Lannulation-de-trois-concessions-forestieres-illegales-en-RDC-est-un-premier-pas-essentiel-mais-pas-suffisant-selon-Greenpeace-Afrique/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','RDC','article','Migrate'),
            'http://www.greenpeace.org/africa/fr/Presse/Le-directeur-executif-de-greenpeace-afrique-en-appelle-a-la-protection-des-tourbieres-apres-sa-visite-en-rd-congo/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','RDC','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Le-gouvernement-congolais-dois-stopper-ses-plans/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','RDC','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Le-gouvernement-de-RDC-retablit-des-concessions-forestieres-illegales-en-violation-de-son-propre-moratoire/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','RDC','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Le-Ministere-de-lenvironnement-et-du-developpement-durable-de-RDC-cherche-a-attribuer-une-zone-a-la-superficie-la-Belgique-pour-lexploitation-forestiere-industrielle/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','RDC','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Le-navire-de-Greenpeace-arrive-pour-la-premiere-fois-au-Cameroun-avec-un-message-pour-la-protection-de-la-foret-du-Bassin-du-Congo/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','Cameroun','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Le-navire-de-Greenpeace-MY-Esperanza-en-expedition-dans-les-eaux-ouest-africaines/':('Communiqués de presse', "Protéger l'Environnement",'Océans','Pêche','','article','Migrate'),
            'http://www.greenpeace.org/africa/fr/Presse/Le-president-de-la-Guinee-Bissau-Jose-Mario-Vaz-rend-visite-au-bateau-de-Greenpeace-apres-larrestation-de-navires-de-peche-illegaux/':('Communiqués de presse', "Protéger l'Environnement",'Océans','Pêche','','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Les-gouvernements-norvegien-et-francais-menacent-la-deuxieme-foret-tropicale-du-monde/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','RDC','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Les-lacunes-et-omissions-de-laudit-sur-les-activites-de-la-CCT-ordonne--par-le-Ministere-camerounais-des-Forets-et-de-la-Faune-soulignent-la-necessite--dun-systeme-de-suivi-independant-des-reglementations-forestieres/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','Cameroun','article','Migrate'),
            'http://www.greenpeace.org/africa/fr/Presse/Les-volontaires-de-Greenpeace-Afrique-exhortent-les-entreprises-a-arreter-le-plastique-a-usage-unique/':('Communiqués de presse', 'Inspirer le Mouvement', 'Plastiques', '', 'RDC', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/fr/Presse/Les-volontaires-de-Greenpeace-participent-au-mouvement-mondial-pour-la-reduction-des-plastiques-a-usage-unique/':('Communiqués de presse', 'Inspirer le Mouvement', 'Plastiques', '', 'Sénégal', 'article', 'Migrate'),
            'http://www.greenpeace.org/africa/fr/Presse/Les-volontaires-de-Greenpeace-participent-au-mouvement-mondial-pour-la-reduction-des-plastiques-a-usage-unique1/':('Communiqués de presse', 'Inspirer le Mouvement', 'Plastiques', '', 'Sénégal', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Liberte-dexpression--Greenpeace-denonce-les-attaques-dun-exploitant-forestier/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Menace-sur-la-securite-alimentaire-en-Afrique-de-lOuest--il-faut-agir-de-toute-urgence/':('Communiqués de presse', "Protéger l'Environnement",'Océans','Pêche','','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Njeri-Kabeberi-nouvelle-Directrice-Generale-de-Greenpeace-Afrique/':('Communiqués de presse', '', 'GreenpeaceAfrica', 'AboutUs', '', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/PaysBas-imposent-sanctions-violation-reglement-europeen-commerce-bois/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','Cameroun','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Plainte-contre-SGSOC/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','Cameroun','article','Migrate'),
            'http://www.greenpeace.org/africa/fr/Presse/Publications/Couper-le-droit-de-parole-/':('Publications', "Protéger l'Environnement",'Forêts','','','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Publications/Herakles-FarmsSGSOC-Histoire-dun-projet-dhuile-de-palme-destructeur-au-Cameroun/':('Publications', "Protéger l'Environnement",'Forêts','','Cameroun','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Publications/La-Norvege-et-la-France-menacent-les-forets-de-la-RDC1/':('Publications', "Protéger l'Environnement",'Forêts','','RDC','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Publications/Le-Cout-de-la-Destruction-des-Oceans1/':('Publications', "Protéger l'Environnement",'Océans','Pêche','','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Publications/Les-donateurs-de-la-RDC-decaissent-40-millions-de-dollars-apres-loctroi-illegal-de-4000km2-de-forets/':('Publications', "Protéger l'Environnement",'Forêts','','RDC','article','Migrate'),
            'http://www.greenpeace.org/africa/fr/Presse/Publications/Menaces-sur-les-forets-africaines/':('Publications', "Protéger l'Environnement",'Forêts','','','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Publications/Rapport-RDC-viole-moratoire-attribution-concessions-forestieres/':('Publications', "Protéger l'Environnement",'Forêts','','RDC','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Publications/SGSOC-un-cimetiere-de-promesses-non-tenues/':('Publications', "Protéger l'Environnement",'Forêts','','Cameroun','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/reaction-greenpeace-sacs-plastiques/':('Communiqués de presse', 'Inspirer le Mouvement', 'Plastiques', '', 'Sénégal', 'article', 'Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Reactive-sur-les-derniers-developpements-sur-les-parcs-nationaux--des-Virunga-et-de-la-Salonga-en-RDC-/':('Communiqués de presse', "Protéger l'Environnement",'Biodiversité','','RDC','article','Migrate'),
            ##'http://www.greenpeace.org/africa/fr/Presse/Retrait-des-USA-de-laccord-de-Paris--Trump-et-les-Etats-Unis-renoncent-a-leur-position-de-leader-international/':('Communiqués de presse', "Protéger l'Environnement",'','','','article','Migrate'),
            'http://www.greenpeace.org/africa/fr/Presse/Socamba-bois-vole-Cameroun-distribue-marches-internationaux/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','Cameroun','article','Migrate'),
            'http://www.greenpeace.org/africa/fr/Presse/Statement-on-the-announcement-of-the-Government-of-the-Democratic-Republic-of-Congo-to-launch-a-process-to-lift-its-moratorium/':('Communiqués de presse', "Protéger l'Environnement",'Forêts','','RDC','article','Migrate'),
            'http://www.greenpeace.org/africa/fr/Presse/Surpeche--Greenpeace-lance-une-expedition-dans-locean-Indien/':('Communiqués de presse', "Protéger l'Environnement",'Océans','Pêche','','article','Migrate')
            ##'http://www.greenpeace.org/africa/fr/Presse/Tchernobyl-Fukushima-cicatrices-visibles/':('Communiqués de presse', 'Inspirer le Mouvement', 'Nucléaire', '', '', 'article', 'Migrate')
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

        yield {
            'type': response.meta['p4_post_type'],
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

        lead_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[1]/div/text()').extract()[0]
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
        date_field = self.filter_month_name(date_field);
        date_field = date_field.replace(" at", "")
        date_field = date_field.replace(" à", "")
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
            map_url = response.xpath('//*[@class="language"]//option[2]/@value').extract()[0]
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
            'author': 'Greenpeace Africa',
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
