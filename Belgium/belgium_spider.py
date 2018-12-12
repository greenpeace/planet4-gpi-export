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
        'FEED_URI': 'gpbe_staging_v2_NL.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    __connector_csv_filename = "connector_v2_final.csv"
    __connector_csv_log_file = "connector_csv_log_v2"

    def start_requests(self):
        # v1
        start_urls = {
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/english-version-impacts-of-cl/':('Rapport','','','Klimaat','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/Grenzen-aan-biomassa-in-Belgie/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/Onze-energietoekomst1/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/klimaat-energie/blog/klassieke-auto-heeft-geen-toekomst-meer/blog/60242/':('Blog','Werken aan een betere toekomst','','Verkeer','Mobiliteit','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/klimaat-energie/blog/belgie-neemt-definitief-afscheid-van-steenkool/blog/56043/':('Blog','Samen sterk: onze succesverhalen','','Energie','Klimaat','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/landbouw/blog/overwinning-roundup-co-verdwijnen-uit-de-wink/blog/59290/':('Blog','Samen sterk: onze succesverhalen','','Landbouw','Gezondheid','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/landbouw/blog/fail-eu-gaat-vergunning-glyfosaat-hernieuwen/blog/60794/':('Blog','Werken aan een betere toekomst','','Landbouw','Gezondheid','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/landbouw/blog/belg-eet-te-veel-vlees-maar-wil-daar-iets-aan/blog/61204/':('Blog','Kleine veranderingen, grote gevolgen','','Food','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/bossen/blog/bedrijven-blijven-het-indonesische-regenwoud-/blog/54887/':('Blog','De natuur heeft je nodig','','Bossen','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/bossen/blog/ook-belgische-bedrijf-handelt-in-conflicthout/blog/53520/':('Blog','De natuur heeft je nodig','','Bossen','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/bossen/blog/bescherm-de-cerrado-die-andere-natuur-in-braz/blog/60238/':('Blog','De natuur heeft je nodig','','GiftigeStoffen','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/pers/Illegaal-hout-EU-roept-Belgie-op-het-matje/':('Persbericht','','','','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/pers/Belgie-importeert-bloedhout-uit-Amazonewoud/':('Persbericht','','','Bossen','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/pers/Energiepact-Denken-Durven-Doen-Greenpeace-voert-actie-voor-de-zetel-van-N-VA/':('Persbericht','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/Samenstelling-en-voedingswaarde-van-kindercharcuterie/':('Rapport','','','Food','Gezondheid','','article','Migrate'),
        }

        # French lang
        start_urls = {
            'http://www.greenpeace.org/belgium/fr/presse/70-des-citadins-wallons-respirent-un-air-malsain/':('Communiqué de presse','','','Santé','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/presse/Action-de-Greenpeace-au-Cinquantenaire-pour-exiger-un-air-de-qualite/':('Communiqué de presse','','','Santé','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/presse/Bois-illegal-la-Belgique-mise-en-cause-par-lUE/':('Communiqué de presse','','','Forêts','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/presse/Du-plastique-et-des-residus-chimiques-trouves-en-Antarctique/':('Communiqué de presse','','','Antarctique','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/presse/Greenpeace-installe-des-panneaux-solaires-sur-le-toit-du-Parlement-europeen/':('Communiqué de presse','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/presse/La-decision-inattendue-de-la-KBC-est-une-victoire-pour-le-climat/':('Communiqué de presse','','','Climat','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/presse/Le-Belge-mange-beaucoup-trop-de-viande-mais-veut-changer/':('Communiqué de presse','','','Alimentation','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/presse/Les-forets-boreales-sont-au-bout-du-rouleau/':('Communiqué de presse','','','Forêts','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/presse/Mauvaise-qualite-de-lair-dans-pres-de-deux-ecoles-sur-trois/':('Communiqué de presse','','','Santé','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/presse/Mobilite-Bruxelles-mauvaise-eleve-europeenne-na-pas-quitte-le-20e-siecle/':('Communiqué de presse','','','Mobilité','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/presse/Pacte-energetique-Penser-Oser-Agir-Greenpeace-mene-une-action-devant-le-siege-de-la-N-VA/':('Communiqué de presse','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/climat-energie/blog/les-comprims-diode-en-8-questions/blog/61217/':('Blog','Petits changements, grandes conséquences','','Santé','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/forets/blog/10-faits-choquants-rvlant-le-rle-des-entrepri/blog/54886/':('Blog','Préserver la beauté de notre planète','','Forêts','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/forets/blog/amazonie-finie-la-dforestation-au-profit-des-/blog/56412/':('Blog','Préserver la beauté de notre planète','','Forêts','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/forets/blog/du-bois-qui-sert-les-conflits-en-Afrique/blog/53528/':('Blog','Préserver la beauté de notre planète','','Forêts','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/forets/blog/faire-confiance-au-rspo-cest-donner-un-laisse/blog/46546/':('Blog','Préserver la beauté de notre planète','','Forêts','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/forets/blog/huile-de-palme-qui-massacre-encore-les-forts/blog/55745/':('Blog','Préserver la beauté de notre planète','','Forêts','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/forets/blog/la-russie-cre-le-grand-parc-naturel-des-ladog/blog/61002/':('Blog','Préserver la beauté de notre planète','','Forêts','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/forets/blog/nos-mouchoirs-synonymes-de-destruction-forest/blog/60354/':('Blog','Préserver la beauté de notre planète','','Forêts','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/forets/blog/protgeons-les-forts-du-grand-nord/blog/58346/':('Blog','Préserver la beauté de notre planète','','Forêts','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/forets/blog/protger-le-cerrado-lautre-nature-du-brsil/blog/60239/':('Blog','Préserver la beauté de notre planète','','Forêts','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/forets/blog/quatre-facons-de-stopper-les-feux-de-foret/blog/54614/':('Blog','Préserver la beauté de notre planète','','Forêts','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/forets/blog/une-nouvelle-tude-montre-que-les-derniers-pay/blog/58520/':('Blog','Préserver la beauté de notre planète','','Forêts','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/forets/blog/victoire-au-canada-un-accord-historique-pour-/blog/55476/':('Blog','Préserver la beauté de notre planète','','Forêts','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/2028-Fin-de-parcours-pour-les-moteurs-a-combustion/':('Rapport','','','Mobilité','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/Classement-des-5-principales-villes-belges-en-matiere-de-mobilite-urbaine-et-durable/':('Rapport','','','Mobilité','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/Greenpeace-demande-la-creation-dun--Fonds-national-des-provisions-nucleaires--pour-y-mettre-les-provisions-nucleaires-en-securite/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/La-nouvelle-proposition-de-lONDRAF-sur-les-dechets-nucleaires-nest-pas-une--modification-mineure-/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/LE-DROIT-DE-RESPIRER---Repenser-la-mobilite-urbaine/':('Rapport','','','Santé','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/Leaving-moving-breathing/':('Rapport','','','Transport','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/Mon-air-mon-ecole/':('Rapport','','','Santé','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/Passez-a-lelectricite-verte-/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/SYNATOM---Analyse-critique-de-la-Societe-belge-des-combustibles-nucleaires/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/presse/Amazonie--la-Belgique-importe-du-bois-tache-de-sang/':('Communiqué de presse','','','Forêts','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/agriculture/blog/au-revoir-glyphosate/blog/61577/':('Blog','Ensemble, nous sommes la solution','','Agriculture','Santé','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/agriculture/blog/des-clients-en-action-dans-leur-brico-contre-/blog/56580/':('Blog','Petits changements, grandes conséquences','','Agriculture','Santé','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/agriculture/blog/et-si-ce-soir-je-ne-consommais-pas-de-viande/blog/61234/':('Blog','Petits changements, grandes conséquences','','Alimentation','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/agriculture/blog/fail-lue-renouvelle-la-licence-du-glyphosate/blog/60796/':('Blog','Il est encore temps','','Agriculture','Santé','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/agriculture/blog/farmerasmus-des-fermiers-belges-invits-par-le/blog/58592/':('Blog','Il est encore temps','','Agriculture','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/agriculture/blog/initiative-citoyenne-europenne-pour-linterdic/blog/58687/':('Blog','Petits changements, grandes conséquences','','Agriculture','Santé','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/agriculture/blog/la-liste-noire-des-pesticides/blog/57470/':('Blog','Il est encore temps','','Agriculture','Santé','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/agriculture/blog/la-publicit-pour-la-charcuterie-ce-nest-pas-u/blog/61676/':('Blog','Il est encore temps','','Alimentation','Santé','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/agriculture/blog/le-belge-mange-beaucoup-trop-de-viande-mais-v/blog/61203/':('Blog','Petits changements, grandes conséquences','','Alimentation','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/agriculture/blog/les-nonicotinodes-ne-menacent-pas-que-les-abe/blog/58474/':('Blog','Il est encore temps','','Agriculture','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/agriculture/blog/les-pesticides-nocifs-pour-lenvironnement/blog/54403/':('Blog','Il est encore temps','','Agriculture','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/agriculture/blog/les-pesticides-sont-morts/blog/58979/':('Blog','Il est encore temps','','Agriculture','Santé','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/agriculture/blog/les-schtroumpfs-se-dbarrassent-de-leurs-charc/blog/61456/':('Blog','Ensemble, nous sommes la solution','','Alimentation','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/agriculture/blog/mangeons-moins-de-viande-et-de-meilleure-qual/blog/61254/':('Blog','Petits changements, grandes conséquences','','Alimentation','Conseils','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/agriculture/blog/mangerons-nous-encore-de-la-viande-en-2050/blog/61343/':('Blog','Petits changements, grandes conséquences','','Alimentation','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/agriculture/blog/que-mettre-sur-nos-tartines/blog/61868/':('Blog','Petits changements, grandes conséquences','','Alimentation','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/agriculture/blog/un-nouvel-outil-pour-lagriculture-cologique/blog/57764/':('Blog','Il est encore temps','','Agriculture','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/agriculture/blog/victoire-le-roundup-co-disparaissent-des-rayo/blog/59291/':('Blog','Ensemble, nous sommes la solution','','Agriculture','Santé','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/agriculture/blog/video-brico-continue-recommander-du-roundup/blog/59111/':('Blog','Il est encore temps','','Agriculture','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/climat-energie/blog/5-menaces-moins-connues-qui-psent-sur-locan-a/blog/56243/':('Blog','Préserver la beauté de notre planète','','Arctique','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/climat-energie/blog/7-manires-de-vous-protger-de-la-pollution-de-/blog/60935/':('Blog','Petits changements, grandes conséquences','','Santé','Mobilité','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/climat-energie/blog/arme-nuclaire-quand-la-fin/blog/60117/':('Blog','Il est encore temps','','Paix ','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/climat-energie/blog/bombes-atomiques-sur-hiroshima-nagasaki-plus-jamais/blog/53723/':('Blog','Il est encore temps','','Paix ','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/climat-energie/blog/classement-des-fournisseurs-dlectricit-seuls-/blog/61915/':('Blog','Petits changements, grandes conséquences','','Energie','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/climat-energie/blog/climat-le-moment-de-vrit-est-arriv/blog/61952/':('Blog','Il est encore temps','','Climat','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/climat-energie/blog/detox-aldi-sengage/blog/52464/':('Blog','Ensemble, nous sommes la solution','','SubstancesToxiques','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/climat-energie/blog/divestment-une-histoire-succs-en-2017/blog/60966/':('Blog','Ensemble, nous sommes la solution','','Energie','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/climat-energie/blog/engie-prend-sa-place-au-soleil/blog/57330/':('Blog','Il est encore temps','','Energie','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/climat-energie/blog/industrie-automobile-6-raisons-de-changer-san/blog/60216/':('Blog','Il est encore temps','','Transport','Mobilité','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/climat-energie/blog/la-belgique-dit-adieu-au-charbon/blog/56042/':('Blog','Ensemble, nous sommes la solution','','Energie','Climat','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/climat-energie/blog/la-core-du-sud-renonce-au-nuclaire-et-au-char/blog/59714/':('Blog','Ensemble, nous sommes la solution','','Energie','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/climat-energie/blog/la-russie-doit-verser-des-indemnites/blog/53900/':('Blog','Il est encore temps','','Paix ','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/climat-energie/blog/la-voiture-lectrique-rend-elle-notre-air-nouv/blog/59995/':('Blog','Petits changements, grandes conséquences','','Mobilité','Santé','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/climat-energie/blog/le-climat-ne-comporte-pas-de-faits-alternatif/blog/58700/':('Blog','Il est encore temps','','Climat','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/climat-energie/blog/les-7-merveilles-solaires-du-monde/blog/51098/':('Blog','Préserver la beauté de notre planète','','Energie','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/climat-energie/blog/les-armes-nuclaires-officiellement-interdites/blog/59865/':('Blog','Ensemble, nous sommes la solution','','Paix ','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/climat-energie/blog/les-belges-doivent-tre-consults-sur-les-dchet/blog/61376/':('Blog','Il est encore temps','','Energie','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/climat-energie/blog/les-citadins-wallons-respirent-un-air-malsain/blog/61922/':('Blog','Il est encore temps','','Santé','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/climat-energie/blog/lulg-met-fin-ses-investissements-lis-aux-nerg/blog/58566/':('Blog','Ensemble, nous sommes la solution','','Energie','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/climat-energie/blog/pacte-nergtique-plus-de-chiffre-mais-des-dcis/blog/61189/':('Blog','Il est encore temps','','Energie','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/climat-energie/blog/quelle-ville-belge-est-la-plus-performante-en/blog/61871/':('Blog','Il est encore temps','','Mobilité','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/climat-energie/blog/tchernobyl-15-choses-savoir/blog/56183/':('Blog','Il est encore temps','','Energie','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/climat-energie/blog/total-rachte-lampiris-totalement-pas-daccord/blog/56769/':('Blog','Il est encore temps','','Energie','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/climat-energie/blog/total-rachte-poweo/blog/61397/':('Blog','Il est encore temps','','Energie','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/climat-energie/blog/vos-apps-sont-elles-colos/blog/58516/':('Blog','Petits changements, grandes conséquences','','Multimedia','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/divers/blog/comment-vritablement-responsabiliser-les-entr/blog/61055/':('Blog','Petits changements, grandes conséquences','','Climat','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/divers/blog/vos-donnes-restent-les-vtres-notre-notice-de-/blog/61693/':('Blog','','','','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/forets/blog/la-fort-tropicale-congolaise-ne-peut-se-passe/blog/59425/':('Blog','Préserver la beauté de notre planète','','Forêts','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/forets/blog/les-forts-borales-et-greenpeace-sont-menaces/blog/59433/':('Blog','Préserver la beauté de notre planète','','Forêts','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/forets/blog/un-nouvel-hibou-dcouvert-dans-les-forts-indon/blog/44000/':('Blog','Préserver la beauté de notre planète','','Forêts','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/oceans/blog/de-loral-revlon-qui-sera-le-champion-de-la-po/blog/57145/':('Blog','Préserver la beauté de notre planète','','Océans','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/oceans/blog/lunesco-tient-loeil-la-grande-barriere-de-corail/blog/53439/':('Blog','Préserver la beauté de notre planète','','Océans','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/oceans/blog/une-tape-importante-pour-la-protection-des-oc/blog/51990/':('Blog','Préserver la beauté de notre planète','','Océans','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/oceans/blog/yes-le-plus-grand-producteur-de-thon-en-conse/blog/59847/':('Blog','Préserver la beauté de notre planète','','Océans','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/9-mythes-sur-la-transition-energetique-allemande-refutes/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/Battle-of-the-grids1/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/briefing-energy-revolution/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/briefing-fukushima-belgique/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/Briefing-Notre-avenir-energetique-2016/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/Composition-et-valeur-nutritionnelle-de-la-charcuterie-pour-enfants/':('Rapport','','','Alimentation','Santé','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/dechets-nucleaires/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/dissemination-possible-de-la-c/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/Energie-nucleaire-voie-sans-issue/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/energie-resume/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/energy-revolution-a-sustainab-2/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/english-version-impacts-of-cl/':('Rapport','','','Climat','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/er-scenario2008-summary-fr/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/faux-espoirs/':('Rapport','','','Climat','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/fukushima-2-ans-apres-des-victimes-livrees-a-elles-memes/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/impacts-des-changements-climat-2/':('Rapport','','','Climat','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/impacts-des-changements-climat/':('Rapport','','','Climat','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/issemination-possible-de-la-co/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/le-risque-non-assure-des-centr/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/Les-limites-de-la-biomasse-en-Belgique/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/lessons-from-fukushima/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/Moins-mais-mieux/':('Rapport','','','Agriculture','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/Notre-avenir-energetique/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/Notre-avenir-energetique1/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/nuclearreactorhazardsreport/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/Our-Energy-Future/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/plans-d-urgence-nucleaire-insuffisants-pour-proteger-la-population/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/Production-et-consommation-de-viande-en-Belgique/':('Rapport','','','Agriculture','Alimentation','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/Recherche-sur-la-promotion-de-la-viande-transformee-aupres-des-enfants-en-Belgique/':('Rapport','','','Alimentation','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/revolution-energetique-2015/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/revolution-energetique/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/roulette-russe/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/synth-egrave-se-impacts-des/':('Rapport','','','Climat','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/rapports/working-for-the-climate/':('Rapport','','','Climat','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/substances-toxiques/blog/ensemble-nous-pouvons-deplacer-des-montagnes/blog/57035/':('Blog','Petits changements, grandes conséquences','','SubstancesToxiques','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/substances-toxiques/blog/mode-detox-o-en-est-le-secteur-textile/blog/61727/':('Blog','Petits changements, grandes conséquences','','SubstancesToxiques','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/substances-toxiques/blog/pourquoi-nos-smartphones-se-cassent-ils-si-vi/blog/59734/':('Blog','Petits changements, grandes conséquences','','SubstancesToxiques','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/substances-toxiques/blog/smartphones-une-consommation-ingrable/blog/58830/':('Blog','Il est encore temps','','SubstancesToxiques','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/fr/vous-informer/substances-toxiques/blog/tanche-sans-poison-gore-tex-se-dtoxifie-grce-/blog/58670/':('Blog','Ensemble, nous sommes la solution','','SubstancesToxiques','','','news-list','Migrate'),
        }

        # Dutch lang
        start_urls = {
            'http://www.greenpeace.org/belgium/nl/nieuws/bossen/blog/4-manieren-om-bosbranden-in-indonesi-te-stopp/blog/54638/':('Blog','De natuur heeft je nodig','','Bossen','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/bossen/blog/4-redenen-om-het-boreale-woud-te-beschermen/blog/58347/':('Blog','De natuur heeft je nodig','','Bossen','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/bossen/blog/bedrijven-blijven-het-indonesische-regenwoud-/blog/54887/':('Blog','De natuur heeft je nodig','','Bossen','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/bossen/blog/bescherm-de-cerrado-die-andere-natuur-in-braz/blog/60238/':('Blog','De natuur heeft je nodig','','GiftigeStoffen','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/bossen/blog/boreale-bossen-n-greenpeace-bedreigd/blog/59431/':('Blog','De natuur heeft je nodig','','Bossen','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/bossen/blog/bosbranden-indonesi-nog-lang-niet-uitgedoofd/blog/46547/':('Blog','De natuur heeft je nodig','','Bossen','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/bossen/blog/congolees-regenwoud-kan-niet-zonder-moratoriu/blog/59412/':('Blog','De natuur heeft je nodig','','Bossen','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/bossen/blog/gedaan-met-ontbossen-voor-soja-in-amazonewoud/blog/56411/':('Blog','De natuur heeft je nodig','','Bossen','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/bossen/blog/hoe-zakdoekjes-majestueuze-bossen-wegvegen/blog/60353/':('Blog','De natuur heeft je nodig','','Bossen','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/bossen/blog/nieuwe-studie-laatste-grote-intacte-bosgebied/blog/58519/':('Blog','De natuur heeft je nodig','','Bossen','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/bossen/blog/ook-belgische-bedrijf-handelt-in-conflicthout/blog/53520/':('Blog','De natuur heeft je nodig','','Bossen','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/bossen/blog/rusland-creert-groot-natuurpark-ladoga-skerri/blog/61000/':('Blog','De natuur heeft je nodig','','Bossen','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/bossen/blog/uniek-canadees-regenwoud-krijgt-bescherming/blog/55485/':('Blog','Samen sterk: onze succesverhalen','','GiftigeStoffen','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/giftige-stoffen/blog/10-jaar-smartphone-rampzalig-voor-milieu/blog/58833/':('Blog','Kleine veranderingen, grote gevolgen','','GiftigeStoffen','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/giftige-stoffen/blog/mode-zonder-gif-waar-staat-de-textielsector/blog/61728/':('Blog','Kleine veranderingen, grote gevolgen','','GiftigeStoffen','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/giftige-stoffen/blog/samen-kunnen-we-bergen-verzetten/blog/57034/':('Blog','De natuur heeft je nodig','','GiftigeStoffen','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/giftige-stoffen/blog/waarom-gaat-elektronica-zo-snel-kapot/blog/59732/':('Blog','Kleine veranderingen, grote gevolgen','','GiftigeStoffen','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/giftige-stoffen/blog/waterdicht-zonder-gif-gore-tex-gaat-detox-dan/blog/58669/':('Blog','Werken aan een betere toekomst','','GiftigeStoffen','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/klimaat-energie/blog/15-dingen-over-tsjernobyl-die-je-nog-niet-wis/blog/56182/':('Blog','Werken aan een betere toekomst','','Energie','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/klimaat-energie/blog/5-minder-bekende-bedreigingen-voor-de-noordpo/blog/56245/':('Blog','De natuur heeft je nodig','','Noordpool','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/klimaat-energie/blog/7-manieren-om-je-te-beschermen-tegen-luchtver/blog/60934/':('Blog','Kleine veranderingen, grote gevolgen','','Gezondheid','Mobiliteit','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/klimaat-energie/blog/8-antwoorden-over-jodiumtabletten/blog/61216/':('Blog','Kleine veranderingen, grote gevolgen','','Gezondheid','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/klimaat-energie/blog/atoombommen-op-hiroshima-nagasaki-dat-nooit-meer/blog/53722/':('Blog','Werken aan een betere toekomst','','Peace ','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/klimaat-energie/blog/belg-verdient-inspraak-over-kernafval/blog/61375/':('Blog','Werken aan een betere toekomst','','Energie','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/klimaat-energie/blog/belgie-neemt-definitief-afscheid-van-steenkool/blog/56043/':('Blog','Samen sterk: onze succesverhalen','','Energie','Klimaat','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/klimaat-energie/blog/de-zeven-zonnigste-wereldwonderen/blog/51101/':('Blog','De natuur heeft je nodig','','Energie','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/klimaat-energie/blog/deze-belgische-stad-scoort-best-op-duurzame-m/blog/61872/':('Blog','Werken aan een betere toekomst','','Mobiliteit','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/klimaat-energie/blog/divestment-kende-ongezien-succes-in-2017/blog/60965/':('Blog','Samen sterk: onze succesverhalen','','Energie','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/klimaat-energie/blog/eerste-universiteiten-keren-fossiele-brandsto/blog/58567/':('Blog','Samen sterk: onze succesverhalen','','Energie','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/klimaat-energie/blog/energiepact-geen-cijfers-meer-maar-politieke-/blog/61188/':('Blog','Werken aan een betere toekomst','','Energie','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/klimaat-energie/blog/engie-kiest-zon-boven-kernenergie/blog/57331/':('Blog','Werken aan een betere toekomst','','Energie','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/klimaat-energie/blog/het-is-nu-of-nooit-voor-het-klimaat/blog/61951/':('Blog','Werken aan een betere toekomst','','Klimaat','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/klimaat-energie/blog/kernwapens-officieel-verboden/blog/59855/':('Blog','Samen sterk: onze succesverhalen','','Peace ','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/klimaat-energie/blog/klassement-energieleveranciers-slechts-8-op-d/blog/61916/':('Blog','Kleine veranderingen, grote gevolgen','','Energie','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/klimaat-energie/blog/klassieke-auto-heeft-geen-toekomst-meer/blog/60242/':('Blog','Werken aan een betere toekomst','','Verkeer','Mobiliteit','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/klimaat-energie/blog/klimaat-verdraagt-geen-alternatieve-feiten/blog/58699/':('Blog','Werken aan een betere toekomst','','Klimaat','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/klimaat-energie/blog/lampiris-totaal-niet-ok/blog/56768/':('Blog','Werken aan een betere toekomst','','Energie','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/klimaat-energie/blog/maakt-elektrische-auto-onze-lucht-weer-zuiver/blog/59994/':('Blog','Kleine veranderingen, grote gevolgen','','Mobiliteit','Gezondheid','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/klimaat-energie/blog/palmolie-wie-verwoest-nu-nog-het-woud/blog/55749/':('Blog','De natuur heeft je nodig','','Bossen','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/klimaat-energie/blog/poweo-totaal-niet-ok/blog/61396/':('Blog','Werken aan een betere toekomst','','Energie','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/klimaat-energie/blog/president-zuid-korea-kondigt-uitstap-kernener/blog/59715/':('Blog','Samen sterk: onze succesverhalen','','Energie','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/klimaat-energie/blog/rusland-moet-compensatie-betalen-voor-arctic-/blog/53899/':('Blog','Werken aan een betere toekomst','','Politiek','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/klimaat-energie/blog/tijd-voor-een-waalse-curieuzeneuzen/blog/61926/':('Blog','Werken aan een betere toekomst','','Gezondheid','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/klimaat-energie/blog/wanneer-krijgen-we-nucleaire-ontwapening/blog/60121/':('Blog','Werken aan een betere toekomst','','Peace ','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/klimaat-energie/blog/zijn-jouw-favoriete-apps-groen/blog/58515/':('Blog','Kleine veranderingen, grote gevolgen','','Multimedia','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/landbouw/blog/belg-eet-te-veel-vlees-maar-wil-daar-iets-aan/blog/61204/':('Blog','Kleine veranderingen, grote gevolgen','','Food','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/landbouw/blog/beter-vlees-wat-is-dat-eigenlijk/blog/61255/':('Blog','Kleine veranderingen, grote gevolgen','','Food','HowTo','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/landbouw/blog/bye-bye-glyfosaat/blog/61576/':('Blog','Samen sterk: onze succesverhalen','','Landbouw','Gezondheid','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/landbouw/blog/de-smurfen-dumpen-hun-smurfenvlees/blog/61457/':('Blog','Samen sterk: onze succesverhalen','','Food','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/landbouw/blog/eten-we-nog-vlees-in-2050/blog/61341/':('Blog','Kleine veranderingen, grote gevolgen','','Food','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/landbouw/blog/europees-burgerinitiatief-om-glyfosaat-te-ver/blog/58686/':('Blog','Kleine veranderingen, grote gevolgen','','Landbouw','Gezondheid','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/landbouw/blog/europees-pesticidegebruik-schaadt-het-milieu/blog/54402/':('Blog','Werken aan een betere toekomst','','Landbouw','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/landbouw/blog/fail-eu-gaat-vergunning-glyfosaat-hernieuwen/blog/60794/':('Blog','Werken aan een betere toekomst','','Landbouw','Gezondheid','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/landbouw/blog/farmerasmus-belgische-boeren-bezoeken-franse-/blog/58587/':('Blog','Werken aan een betere toekomst','','Landbouw','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/landbouw/blog/greenpeace-publiceert-zwarte-lijst-van-pestic/blog/57471/':('Blog','Werken aan een betere toekomst','','Landbouw','Gezondheid','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/landbouw/blog/klanten-in-actie-tegen-roundup-in-hun-brico/blog/56578/':('Blog','Kleine veranderingen, grote gevolgen','','Landbouw','Gezondheid','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/landbouw/blog/neonicotinoden-bedreigen-niet-alleen-bijen/blog/58475/':('Blog','De natuur heeft je nodig','','Bossen','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/landbouw/blog/nieuw-platform-voor-ecolandbouw-in-europa/blog/57763/':('Blog','Werken aan een betere toekomst','','Landbouw','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/landbouw/blog/overwinning-roundup-co-verdwijnen-uit-de-wink/blog/59290/':('Blog','Samen sterk: onze succesverhalen','','Landbouw','Gezondheid','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/landbouw/blog/pesticiden-zijn-out/blog/58980/':('Blog','Werken aan een betere toekomst','','Landbouw','Gezondheid','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/landbouw/blog/reclame-voor-charcuterie-geen-kinderspel/blog/61674/':('Blog','Werken aan een betere toekomst','','Food','Gezondheid','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/landbouw/blog/video-brico-blijft-lustig-roundup-promoten/blog/59112/':('Blog','Werken aan een betere toekomst','','Landbouw','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/landbouw/blog/wij-gaan-voluit-voor-minder-vlees-en-jij/blog/61236/':('Blog','Kleine veranderingen, grote gevolgen','','Food','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/oceanen/blog/belangrijke-mijlpaal-voor-de-oceanen/blog/51995/':('Blog','De natuur heeft je nodig','','Oceanen','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/oceanen/blog/unesco-houdt-bedreigd-groot-barrirerif-nauwle/blog/53438/':('Blog','De natuur heeft je nodig','','Oceanen','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/oceanen/blog/welke-merken-vervuilen-de-oceanen-met-plastic/blog/57146/':('Blog','De natuur heeft je nodig','','Oceanen','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/oceanen/blog/yes-grootste-inblikker-van-tonijn-kiest-duurz/blog/59834/':('Blog','De natuur heeft je nodig','','Oceanen','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/2028-Game-over-voor-de-verbrandingsmotor/':('Rapport','','','Mobiliteit','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/9-mythes-over-de-Duitse-Energiewende-weerlegd/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/Battle-of-the-grids/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/briefing-energy-revolution/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/briefing-fukushima-belgie/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/Briefing-Our-Energy-Future-2016/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/De-productie-en-consumptie-van-vlees-in-Belgie/':('Rapport','','','Landbouw','Food','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/DE-VRIJHEID--OM-TE-ADEMEN---Een-nieuwe-kijk-op-stedelijk-vervoer/':('Rapport','','','Gezondheid','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/energy-revolution-a-sustainab-2/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/energy-revolution/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/english-version-impacts-of-cl/':('Rapport','','','Klimaat','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/er-scenario2008-summary/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/erfenis-kernafval/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/false-hope-why-carbon-capture/':('Rapport','','','Klimaat','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/fukushima-fallout-nuclear-business-makes-people-pay-and-suffer/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/greenjobs/':('Rapport','','','Klimaat','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/Grenzen-aan-biomassa-in-Belgie/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/het-onverzekerde-risico-van-ke/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/Kernenergie-dood-spoor/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/Klassement-van-de-vijf-belangrijkste-Belgische-steden-op-het-vlak-van-stedelijke-en-duurzame-mobiliteit/':('Rapport','','','Mobiliteit','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/Leaving-moving-breathing/':('Rapport','','','Verkeer','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/Less-is-more/':('Rapport','','','Landbouw','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/lessons-from-fukushima/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/Mijn-lucht-mijn-school/':('Rapport','','','Gezondheid','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/mogelijke-verspreiding-van-de-2/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/mogelijke-verspreiding-van-de/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/NIRAS-nieuwe-kernafvalvoorstel-geen-kleine-aanpassing/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/nucleaire-noodplanning-beschermt-de-bevolking-niet/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/nuclearreactorhazardsreport/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/Onderzoek-naar-hoe-bewerkt-vlees-in-Belgie-naar-kinderen-wordt-gepromoot/':('Rapport','','','Food','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/Onze-energietoekomst/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/Onze-energietoekomst1/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/Our-Energy-Future/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/russische-roulette-risicos-van-kerncentrales/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/Samenstelling-en-voedingswaarde-van-kindercharcuterie/':('Rapport','','','Food','Gezondheid','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/Stap-over-op-groene-stroom/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/rapporten/SYNATOM---Kritische-analyse-over-Belgische-maatschappij-voor-kernbrandstoffen/':('Rapport','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/varia/blog/hoe-maken-we-bedrijven-echt-verantwoordelijk/blog/61052/':('Blog','Kleine veranderingen, grote gevolgen','','Klimaat','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/nieuws/varia/blog/jouw-gegevens-blijven-jouw-eigendom-we-hebben/blog/61692/':('Blog','','','','','','news-list','Migrate'),
            'http://www.greenpeace.org/belgium/nl/pers/Belg-eet-te-veel-vlees-maar-wil-daar-iets-aan-doen/':('Persbericht','','','Food','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/pers/Belgie-importeert-bloedhout-uit-Amazonewoud/':('Persbericht','','','Bossen','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/pers/Bijna-2-scholen-op-3-kampen-met-ongezonde-lucht/':('Persbericht','','','Gezondheid','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/pers/Energiepact-Denken-Durven-Doen-Greenpeace-voert-actie-voor-de-zetel-van-N-VA/':('Persbericht','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/pers/Europees-mobiliteitsonderzoek-Brussel-bij-de-slechtste-leerlingen-van-de-klas/':('Persbericht','','','Mobiliteit','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/pers/Greenpeace-eist-gezonde-lucht-met-adembenemend-spandoek-/':('Persbericht','','','Gezondheid','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/pers/Greenpeace-installeert-zonnepanelen-op-het-dak-van-het-Europees-Parlement/':('Persbericht','','','Energie','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/pers/Greenpeace-Onverwachte-beslissing-van-KBC-is-overwinning-voor-klimaat/':('Persbericht','','','Klimaat','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/pers/Greenpeace-wil-Waalse-CurieuzeNeuzen/':('Persbericht','','','Gezondheid','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/pers/Illegaal-hout-EU-roept-Belgie-op-het-matje/':('Persbericht','','','','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/pers/Plasticdeeltjes-en-chemische-stoffen-aangetroffen-in-afgelegen-gebieden-Antarctica/':('Persbericht','','','Antarctica','','','article','Migrate'),
            'http://www.greenpeace.org/belgium/nl/pers/Tweede-grootste-zakdoekjesfabrikant-veegt-boreaal-bos-weg/':('Persbericht','','','','','','article','Migrate'),
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
            date_field = date_field.replace(" om ", " ") #dutch
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
                if ( Segments[4] ):
                    author_username = Segments[4]
            except IndexError:
                author_username = ''

        # Get the thumbnail of the post as requested.
        thumbnail = response.xpath('string(head//link[@rel="image_src"]/@href)').extract_first()

        # custom transalation mapping logic
        unique_map_id = int(random.randint(0, 999999999)+time.time())
        map_url = ''

        if "/fr/" in response.url:
            # For French language POSTs

            # Check the POST transalation availability
            try:
                # Check the map url in csv, if available
                with open('URL_mapping_NL_to_FR.csv', "rb") as file_obj:
                    reader = csv.reader(file_obj)
                    for row in reader:
                        if (row[1] == response.url):
                            print "=======Match found======="
                            map_url = row[0]
            except IndexError:
                map_url = ''

            if "/nl/" not in map_url:
                map_url = ''

            if map_url:
                # The Post mapping data added into csv file.
                data = [unique_map_id, response.url, map_url]
                self.csv_writer(data, self.__connector_csv_filename)

                data = [response.url, response.meta['p4_post_type'], response.meta['category1'],
                        response.meta['category2'], response.meta['tags1'], response.meta['tags2'],
                        response.meta['tags3'], response.meta['post_type'], response.meta['action']]
                self.csv_writer(data, "Language_mapping_fr_list.csv")
        else:
            # For Dutch language(NL) POSTs

            # Check the POST transalation if available
            with open(self.__connector_csv_filename, "rb") as file_obj:
                reader = csv.reader(file_obj)
                for row in reader:
                    if (row[2] == response.url):
                        # print "=======Match found======="
                        unique_map_id = row[0]
                        map_url = row[1]
                        # Log the details
                        data = ["NL==>", unique_map_id, response.url, map_url, "FR==>", row[0], row[1], row[2]]
                        # print data
                        self.csv_writer(data, self.__connector_csv_log_file)

                        data = [response.url, response.meta['p4_post_type'], response.meta['category1'],
                                response.meta['category2'],
                                response.meta['tags1'], response.meta['tags2'], response.meta['tags3'],
                                response.meta['post_type'], response.meta['action']]
                        self.csv_writer(data, "Language_mapping_nl_list.csv")
        # Post data mapping logic ends.

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

        # List authors name.
        # a_data = [response.xpath('string(//div[@class="news-list"]/ul/li/*/*/span[@class="caption"]/strong/span[@class="green1"])').extract()[0]]
        # self.csv_writer(a_data, "post_author_list_fr.txt")
        
        #list images urls
        for image_file in imagesB_generated:
            if ("/emailimages/" in image_file):
                data = [image_file]
                self.csv_writer(data, "email_images_url_list_fr_story.csv")


        yield {
            'type': response.meta['p4_post_type'],
            'p3_image_gallery': p3_image_gallery,
            'title': extract_with_css('div.news-list h1::text'),
            #'subtitle': '',
            'author': response.xpath('string(//div[@class="news-list"]/ul/li/*/*/span[@class="caption"]/strong/span[@class="green1"])').extract()[0],
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
            date_field = date_field.replace(" om ", "") #dutch
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
        
        
        #list images urls
        for image_file in imagesB_generated:
            if ("/emailimages/" in image_file):
                data = [image_file]
                self.csv_writer(data, "email_images_url_list_fr.csv")

        # Post data mapping logic start.
        unique_map_id = int(random.randint(0, 999999999)+time.time())
        map_url = ''

        if "/fr/" in response.url:
            # For French language POSTs

            # Check the POST transalation availability
            try:
                # Check the map url in csv, if available
                with open('URL_mapping_NL_to_FR.csv', "rb") as file_obj:
                    reader = csv.reader(file_obj)
                    for row in reader:
                        if (row[1] == response.url):
                            print "=======Match found======="
                            map_url = row[0]
            except IndexError:
                map_url = ''

            if "/nl/" not in map_url:
                map_url = ''

            if map_url:
                # The Post mapping data added into csv file.
                data = [unique_map_id, response.url, map_url]
                self.csv_writer(data, self.__connector_csv_filename)

                data = [response.url, response.meta['p4_post_type'], response.meta['category1'],
                        response.meta['category2'], response.meta['tags1'], response.meta['tags2'],
                        response.meta['tags3'], response.meta['post_type'], response.meta['action']]
                self.csv_writer(data, "Language_mapping_fr_list.csv")
        else:
            # For Dutch language(NL) POSTs

            # Check the POST transalation if available
            with open(self.__connector_csv_filename, "rb") as file_obj:
                reader = csv.reader(file_obj)
                for row in reader:
                    if (row[2] == response.url):
                        # print "=======Match found======="
                        unique_map_id = row[0]
                        map_url = row[1]
                        # Log the details
                        data = ["NL==>", unique_map_id, response.url, map_url, "FR==>", row[0], row[1], row[2]]
                        # print data
                        self.csv_writer(data, self.__connector_csv_log_file)

                        data = [response.url, response.meta['p4_post_type'], response.meta['category1'],
                                response.meta['category2'],
                                response.meta['tags1'], response.meta['tags2'], response.meta['tags3'],
                                response.meta['post_type'], response.meta['action']]
                        self.csv_writer(data, "Language_mapping_nl_list.csv")
        # Post data mapping logic ends.

        yield {
            'type': response.meta['p4_post_type'],
            'p3_image_gallery': p3_image_gallery,
            'title': extract_with_css('div.article h1 span::text'),
            #'subtitle': '',
            'author': 'Greenpeace Belgique',
            #'author': 'Greenpeace België',
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
        """
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

        # Replace the english month name with french month name.
        for fr_month, en_month in month_fr_en.iteritems():
            month_name = month_name.replace(fr_month, en_month)
        """

        month_nl_en = {
            'januari': 'January',
            'februari': 'February',
            'maart': 'March',
            'april': 'April',
            'mei': 'May',
            'juni': 'June',
            'juli': 'July',
            'augustus': 'August',
            'september': 'September',
            'oktober': 'October',
            'november': 'November',
            'december': 'December',
        }

        # Replace the english month name with dutch month name.
        for nl_month, en_month in month_nl_en.iteritems():
            month_name = month_name.replace(nl_month, en_month)

        return month_name;

    def csv_writer(self, data, path):
        # Write data to a CSV file path
        with open(path, "a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(data)
