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
        'FEED_URI': 'gplux_staging_v3_GE_final.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    __connector_csv_filename = "connector_v2_final.csv"
    __connector_csv_log_file = "connector_csv_log_v2"

    def start_requests(self):

        #v1 FR
        start_urls = {
            # Blogs
            'http://www.greenpeace.org/luxembourg/fr/news/Mode-detox--ou-en-est-le-secteur-textile-/':('Actualités','Société','','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Echange-de-vues-constructif-sur-la-politique-dinvestissement-des-fonds-publics-entre-le-gouvernement-et-Votum-Klima/':('Actualités','Climat','EnergiesFossiles','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Diesel--les-constructeurs-automobiles-continuent-denfumer-nos-villes/':('Actualités','Climat','EnergiesFossiles','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Des-grimpeurs-bloquent-un-navire-petrolier-sur-le-pont-de-Vancouver/':('Actualités','Climat','EnergiesFossiles','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/5-manieres-daffronter-les-compagnies-pipelinieres/':('Actualités','Climat','EnergiesFossiles','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Des-actions-artistiques-de-Greenpeace-en-images/':('Actualités','Climat','ChangementClimatique','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Recif-de-lAmazone--une-nouvelle-etape-decisive/':('Actualités','Nature','Biodiversité','Océans','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/BIG-BSSSINESS/':('Actualités','Nature','Biodiversité','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Recif-de-lAmazone--deferlante-de-bonnes-nouvelles/':('Actualités','Nature','EnergiesFossiles','Océans','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Victoire--lUE-interdit-trois-pesticides-tueurs-dabeilles/':('Actualités','Nature','Biodiversité','','','article','Migrate'),
        }

        # v2 FR post.
        ## - multilingual posts.
        #### - duplicate post.
        start_urls = {
            'http://www.greenpeace.org/luxembourg/fr/news/Mode-detox--ou-en-est-le-secteur-textile-/':('Actualités','Société','','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Echange-de-vues-constructif-sur-la-politique-dinvestissement-des-fonds-publics-entre-le-gouvernement-et-Votum-Klima/':('Actualités','Climat','EnergiesFossiles','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Diesel--les-constructeurs-automobiles-continuent-denfumer-nos-villes/':('Actualités','Climat','EnergiesFossiles','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Des-grimpeurs-bloquent-un-navire-petrolier-sur-le-pont-de-Vancouver/':('Actualités','Climat','EnergiesFossiles','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/5-manieres-daffronter-les-compagnies-pipelinieres/':('Actualités','Climat','EnergiesFossiles','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Recif-de-lAmazone--une-nouvelle-etape-decisive/':('Actualités','Nature','Biodiversité','Océans','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Recif-de-lAmazone--deferlante-de-bonnes-nouvelles/':('Actualités','Nature','EnergiesFossiles','Océans','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Victoire--lUE-interdit-trois-pesticides-tueurs-dabeilles/':('Actualités','Nature','Biodiversité','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Recif-de-lAmazone--decouverte-genante-pour-Total/':('Actualités','Nature','EnergiesFossiles','Océans','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Recif-de-lAmazone--Neptune-se-fache/':('Actualités','Nature','EnergiesFossiles','Océans','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Total-nous-sommes-la-/':('Actualités','Nature','EnergiesFossiles','Océans','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Recif-de-lAmazone--Total-recidive-Nous-aussi/':('Actualités','Nature','EnergiesFossiles','Océans','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Ausgebohrt/':('Actualités','Nature','EnergiesFossiles','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Antarctique--touche-pas-a-mon-krill/':('Actualités','Nature','Biodiversité','Océans','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Creer-des-reserves-marines/':('Actualités','Nature','Biodiversité','Océans','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Journee-mondiale-des-manchots--les-stars-de-lAntarctique/':('Actualités','Nature','Océans','Biodiversité','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Les-plastiques-nont-rien-a-faire-en-Antarctique/':('Actualités','Nature','Océans','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Forets--bientot-une-decision-cruciale-de-lUnion-Europeenne-/':('Actualités','Nature','Biodiversité','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Les-premieres-images-des-fonds-marins-de-locean-Antarctique/':('Actualités','Nature','Océans','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Quest-ce-que-la-CCAMLR-/':('Actualités','Nature','Océans','Biodiversité','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Expedition--cap-sur-locean-Antarctique/':('Actualités','Nature','Océans','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Javier-Bardem-vous-emmene-en-Antarctique/':('Actualités','Nature','Océans','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Antarctique--un-peu-de-repit-pour-les-krills/':('Actualités','Nature','Océans','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/A-Million-Acts-of-Blue/':('Actualités','Nature','Pollution','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Tchernobyl--le-risque-nucleaire-toujours-dactualite/':('Actualités','Énergie','Nucléaire','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Remise-officielle-du-rapport-dexperts-a-Mayence/':('Communiqués de presse','Énergie','Nucléaire','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Denoncer-le-risque-nucleaire--ils-lont-fait-pour-nous/':('Actualités','Énergie','Nucléaire','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Fukushima--des-meres-a-lONU-a-Geneve/':('Actualités','Énergie','Nucléaire','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/A-Fukushima-limpossible-retour-des-personnes-evacuees/':('Actualités','Énergie','Nucléaire','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Nos-militants-condamnes--nous-faisons-appel/':('Actualités','Énergie','Nucléaire','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Engagez-vous-pour-un-Europe-vert/':('Actualités','Énergie','EnergieSolaire','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Les-militants-de-Greenpeace-attaques-en-justice--a-quand-le-proces-des-centrales-dEDF-/':('Actualités','Énergie','Nucléaire','Militants','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Les-5-raisons-pour-lesquelles-Fessenheim-doit-fermer-rapidement/':('Actualités','Énergie','Nucléaire','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Le-Parlement-europeen-vote-pour-augmenter-lobjectif-des-energies-renouvelables/':('Actualités','Énergie','EnergieSolaire','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Proces-de-des-militant-e-s-Greenpeace--pas-de-victoire-pour-EDF/':('Actualités','Énergie','Nucléaire','Militants','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Quand-Superman-se-plante/':('Actualités','Énergie','Nucléaire','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Action-Superman-survole-la-centrale-nucleaire-du-Bugey-et-sy-crashe/':('Actualités','Énergie','Nucléaire','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Action-bis-repetita--apres-Superman-un-second-survol-et-crash-au-Bugey/':('Actualités','Énergie','Nucléaire','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Coince-en-1957/':('Actualités','Énergie','Nucléaire','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Une-Grande-Region-sans-nucleaire---Maintenant-/':('Actualités','Énergie','Nucléaire','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Lopposition-contre-TTIP-CETA-et-Co-se-poursuit/':('Communiqués de presse','Société','CommerceEquitable','Luxembourg','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Lancement-de-lInitiative-pour-un-devoir-de-vigilance-des-entreprises-transnationales-au-Luxembourg/':('Communiqués de presse','Société','Luxembourg','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Recif-de-lAmazone--Greenpeace-et-ANV-COP21-interrompent-lAG-de-Total/':('Communiqués de presse','Nature','EnergiesFossiles','Militants','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Meng-Landwirtschaft-Revendications-2018/':('Communiqués de presse','Nature','AgricultureDurable','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Javier-Bardem-plonge-en-sous-marin-en-Antarctique-avec-Greenpeace-pour-demander-la-creation-dun-sanctuaire-marin/':('Communiqués de presse','Nature','Océans','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/DES-MANCHOTS-A-LUXEMBOURG/':('Communiqués de presse','Nature','Océans','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Des-industriels-de-la-peche-au-krill-appellent-a-la-creation-dun-sanctuaire-marin-en-Antarctique/':('Communiqués de presse','Nature','Océans','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Proces-a-Privas/':('Communiqués de presse','Énergie','Nucléaire','Militants','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Des-militants-environnementaux-accueillent-Emmanuel-Macron-a-Aix-la-Chapelle-avec-des-banderoles-anti-nucleaire/':('Communiqués de presse','Énergie','Nucléaire','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Lere-des-Energiebierger-commence-aujourdhui/':('Communiqués de presse','Énergie','EnergieSolaire','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Greenpeace--interdit-de-sejour--a-la-centrale-nucleaire-de-Cattenom/':('Communiqués de presse','Énergie','Nucléaire','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Greenpeace-France-porte-plainte-contre-la-deputee-Perrine-Goulet-pour-incitation-au-meurtre/':('Communiqués de presse','Énergie','Militants','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Tribune--la-place-des-militant-es-de-Greenpeace-nest-pas-en-prison/':('Communiqués de presse','Énergie','Nucléaire','Militants','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Des-militants-de-la-lutte-contre-le-rechauffement-climatique-appellent-les-ministres-de-lenergie-de-lUE-a-agir-pour-une-revolution-solaire-de-nos-toits/':('Communiqués de presse','Énergie','EnergieSolaire','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Reaction-de-Greenpeace-France-au-delibere-rendu-par-le-tribunal-de-Thionville-concernant-laction-a-la-centrale-nucleaire-de-Cattenom/':('Communiqués de presse','Énergie','Nucléaire','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Greenpeace-France-devant-la-justice--a-quand-le-proces-des-centrales-dEDF-/':('Communiqués de presse','Énergie','Nucléaire','Militants','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Promouvoir-le-developpement-des-energies-renouvelables-/':('Communiqués de presse','Énergie','EnergieSolaire','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/LUE-balaye-les-obstacles-a-la-revolution-solaire-mais-lobjectif-pour-les-energies-renouvelables-est-loin-detre-suffisant/':('Communiqués de presse','Énergie','EnergieSolaire','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Proces-des-militants-de-Greenpeace-France/':('Communiqués de presse','Énergie','Nucléaire','Militants','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Un-rapport-de-Greenpeace-leve-le-voile-sur-lindustrie-peu-connue-de-la-peche-au-krill-en-Antarctique/':('Communiqués de presse','Nature','Biodiversité','Océans','','article','Migrate'),
        }


        # GR Post list.
        start_urls = {
            'http://www.greenpeace.org/luxembourg/fr/news/Die-Opposition-gegen-TTIP-CETA-und-Co-geht-weiter/':('Aktualität','Gesellschaft','FairerHandel','Luxemburg','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Diese-sechs-Tiere-halten-Weltrekorde/':('Aktualität','Klima','','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Es-gab-eine-Zeit-in-der-Manner-dachten-Frauen-sollten-nicht-in-die-Antarktis-gehen-Wow---haben-wir-denen-gezeigt-dass-sie-falsch-lagen/':('Aktualität','Klima','Biodiversität','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Die-Angriffe-von-Energy-Transfer-Partners-auf-Menschenrechte-Redefreiheit-und-Umwelt-sind-zu-weit-gegangen/':('Aktualität','Klima','FossileEnergien','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Die-Leitung-Bitte-Kappen/':('Aktualität','Klima','FossileEnergien','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Braucht-kein-Mensch/':('Aktualität','Natur','Biodiversität','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/World-Penguin-Day-5-Grunde-warum-man-Pinguine-einfach-lieben-muss/':('Aktualität','Natur','Ozeane','Biodiversität','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/5-seltsame-Dinge-uber-die-Antarktis/':('Aktualität','Natur','Ozeane','FossileEnergien','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Schneeweiss-und-doch-schmutzig/':('Aktualität','Natur','Ozeane','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/In-fremden-Welten/':('Aktualität','Natur','Ozeane','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Ins-Gewissen-geredet/':('Aktualität','Natur','Ozeane','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Gentechnik-beim-Namen-nennen/':('Aktualität','Natur','NachhaltigeLandwirtschaft','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Aufstand-der-Frauen/':('Aktualität','Energie','Nuklear','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Methode-VogelstrauB/':('Aktualität','Energie','Nuklear','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Engagieren-Sie-sich-fur-ein-grunes-Europa/':('Aktualität','Energie','Solarenergie','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Sicherheit-ist-gutes-Recht/':('Aktualität','Energie','Nuklear','Ehrenamtliche','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Aktion-Superman-fliegt-uber-das-Atomkraftwerk-von-Bugey-und-zerschellt-darauf/':('Aktualität','Energie','Nuklear','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/AKW-Hinkley-Point-EuGH-weist-Klage-Osterreichs-und-Luxemburgs-ab/':('Aktualität','Energie','Nuklear','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Tschernobyl-Verstrahlt-fur-Tausende-Jahre/':('Aktualität','Energie','Nuklear','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Eine-ganz-grosse-Null/':('Aktualität','Gesellschaft','','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Meng-Landwirtschaft-Wahlforderungen-2018/':('Presseerklärungen','Natur','NachhaltigeLandwirtschaft','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Start-der-Initiative-fur-eine-Sorgfaltspflicht-der-transnationalen-Wirtschaftsunternehmen-in-Luxemburg/':('Presseerklärungen','Gesellschaft','Luxemburg','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Luxemburg-zukunftsfahig-machen/':('Presseerklärungen','Klima','NachhaltigeLandwirtschaft','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/Votum-Klima-begruBt-die-neuen-Zugpferde-der-EU-Klimapolitik/':('Presseerklärungen','Klima','Klimaschutz','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Ein-Land-macht-Schluss-mit-Ol/':('Presseerklärungen','Klima','FossileEnergien','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Aus-dem-Rhythmus/':('Presseerklärungen','Klima','Klimaschutz','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Konstruktiver-Meinungsaustausch-zwischen-RegierungsvertreterInnen-und-Votum-Klima-zur-Investitionspolitik-der-staatlichen-Fonds/':('Presseerklärungen','Klima','FossileEnergien','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Auftakt-der-Verhandlungen-gegen-47-Carbon-Majors-vor-der-philippinischen-Menschenrechtskommission/':('Presseerklärungen','Klima','FossileEnergien','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Geprufte-Sinnlosigkeit/':('Presseerklärungen','Klima','FossileEnergien','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Der-Ausschuss-des-Europaischen-Parlaments-beschrankt-umstrittene-Subventionen-fur-Kohle-Gas-und-Kernkraftwerke/':('Presseerklärungen','Klima','FossileEnergien','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Irland-beschlieBt-Divestment-aus-fossilen-Energien-Wann-folgt-endlich-Luxemburg/':('Presseerklärungen','Klima','FossileEnergien','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Gemeinsame-Aktion-fur-den-Erhalt-der-Bienenbestande/':('Presseerklärungen','Natur','Biodiversität','NachhaltigeLandwirtschaft','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Oscar-Preistrager-Javier-Bardem-fordert-antarktisches-Meeresschutzgebiet/':('Presseerklärungen','Natur','Ozeane','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Stellungnahme-zum-Wortlu-Artikel-Lugen-fur-die-gute-Sache-vom-17-Mai-2018/':('Presseerklärungen','Energie','Nuklear','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Reaktion-von-Greenpeace-Frankreich-zum-Urteil-des-Bezirksgerichts-Thionville-zur-Aktion-im-Kernkraftwerk-Cattenom/':('Presseerklärungen','Energie','Nuklear','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Greenpeace-Frankreich-vor-Gericht-Wann-wird-der-Prozess-gegen-die-EDF-Kraftwerke-stattfinden/':('Presseerklärungen','Energie','Nuklear','Militants','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Den-Ausbau-der-erneuerbaren-Energien-fordern/':('Presseerklärungen','Energie','Solarenergie','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Schlechter-Gewinner/':('Presseerklärungen','Energie','Nuklear','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Neue-Energieburger-braucht-das-Land/':('Presseerklärungen','Energie','Solarenergie','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Schwimmendes-Atomproblem/':('Presseerklärungen','Energie','Nuklear','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Offizielle-Ubergabe-des-Greenpeace-Experten-Berichts-an-Umweltministerin-Ulrike-Hofken-RLP-in-Mainz/':('Presseerklärungen','Energie','Nuklear','','','article','Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Ruckkehr-ins-Ungewisse/': ('Actualités', 'Énergie', 'Nucléaire', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/Verbrechen-Klimazerstorung/': ('Actualités', 'Climat', 'Nucléaire', '', '', 'article', 'Migrate'),
            'http://www.greenpeace.org/luxembourg/fr/news/BIG-BSSSINESS/': ('Actualités', 'Nature', 'Biodiversité', '', '', 'article', 'Migrate'),
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
                    '<a href="mailto:' + emailid.strip() + '" target="_blank">' + emailid.strip() + '</a>', body_text)

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
                    '<a href="mailto:' + emailid.strip() + '" target="_blank">' + emailid.strip() + '</a>', body_text)

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
            'author': 'Greenpeace Luxembourg',
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
