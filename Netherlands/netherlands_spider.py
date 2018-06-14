import scrapy
import logging
import locale
import dateutil.parser
import re
import dateparser
from datetime import datetime, date


locale.setlocale(locale.LC_ALL, '')

class AllSpider(scrapy.Spider):
    name = 'all'

    custom_settings = {
        'ROBOTSTXT_OBEY': 0,
        'FEED_URI': 'gpnl_staging_v2_P3_test.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def start_requests(self):

        '''
        start_urls = {
            # - 1st batch
            # News
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Klimaat--Energie/Luchtvaartmanifest-zet-de-luchtvaart-op-het-juiste-spoor/':('Feature','klimaat & energie','klimaat en energie', 'luchtvaart', 'Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Landbouw/GOED-NIEUWS-VOOR-DE-BIJEN/':('Feature','landbouw','duurzame landbouw', 'bijen', 'Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Klimaat--Energie/Gezamenlijke-oproep-Kabinet-weeg-milieu-volledig-mee-in-uitbreidingsplannen-luchtvaart/':('Feature','klimaat & energie','klimaat en energie', 'luchtvaart', 'Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Corporate/Rainbow-Warriors/':('Feature','over ons','over ons', '', 'Migrate'),

            # Press releases
            'http://www.greenpeace.nl/2018/Persberichten/Milieuorganisaties-slaan-handen-ineen-stop-groei-luchtvaart/': ('Press Release', 'klimaat & energie', 'klimaat en energie', 'luchtvaart', 'Migrate'),
            'http://www.greenpeace.nl/2018/Persberichten/Overwinning-voor-de-bijen-Greenpeace-blij-met-ban-op-neonics/': ('Press Release', 'landbouw', 'duurzame landbouw', 'bijen', 'Migrate'),
            'http://www.greenpeace.nl/2018/Persberichten/Greenpeace-blij-met-Schouten-toezegging-ban-neonics/': ('Press Release', 'landbouw', 'duurzame landbouw', 'neonics', 'Migrate'),

            # Publications
            'http://www.greenpeace.nl/2018/Publicaties/Klimaat--Energie/Brief-aan-kamerleden-overleg-duurzaam-vervoer-over-Klimaatakkoord-voor-mobiliteit-en-biobrandstoffen/': ('Publication', 'over ons', 'correspondentie', 'klimaat en energie', 'Migrate'),
            'http://www.greenpeace.nl/2018/Publicaties/Klimaat--Energie/Brief-aan-ministerie-van-Infrastructuur-en-Waterstaat-over-de-toekomst-van-de-Noordzee/': ('Publication', 'over ons', 'correspondentie', 'klimaat en energie', 'Migrate'),
            'http://www.greenpeace.nl/2018/Publicaties/Landbouw/Minder-vlees-en-zuivel-voor-een-betere-wereld-en-een-gezonder-leven/': ('Publication', 'landbouw', 'duurzame landbouw', 'veestapel', 'Migrate'),
        }
        '''

        start_urls = {
            # - 2nd batch
            'http://www.greenpeace.nl/2018/Publicaties/Landbouw/Minder-vlees-en-zuivel-voor-een-betere-wereld-en-een-gezonder-leven/':('Publication','Natuur','Landbouw','Vlees','Migrate'),
            'http://www.greenpeace.nl/2018/Publicaties/Landbouw/Brief-aan-Kamerleden-Algemeen-Overleg-LNV-Commissie-over-bestrijdingsmiddelen/':('Publication','Natuur','Landbouw','Bijen','Migrate'),
            'http://www.greenpeace.nl/2018/Publicaties/Klimaat--Energie/Brief-aan-ministerie-van-Infrastructuur-en-Waterstaat-over-de-toekomst-van-de-Noordzee/':('Publication','Klimaat','Oceanen','Noordzee','Migrate'),
            'http://www.greenpeace.nl/2018/Publicaties/Klimaat--Energie/Brief-aan-kamerleden-overleg-duurzaam-vervoer-over-Klimaatakkoord-voor-mobiliteit-en-biobrandstoffen/':('Publication','Klimaat','Duurzaamheid','Politiek','Migrate'),
            'http://www.greenpeace.nl/2018/Publicaties/Klimaat--Energie/Brief-aan-Kamerleden-met-input-natuur-en-milieuorganisaties-op-de-informele-bijeenkomst-van-milieuministers-op-10-en-11-april-2018/':('Publication','Klimaat','Duurzaamheid','Politiek','Migrate'),
            'http://www.greenpeace.nl/2018/Publicaties/Klimaat--Energie/Brief-aan-Kamerleden-vaste-commissie-voor-landbouw-natuur-en-voedselkwaliteit-over-gewasbeschermingsmiddelen--/':('Publication','Klimaat','Landbouw','Bijen','Migrate'),
            'http://www.greenpeace.nl/2018/Publicaties/Klimaat--Energie/Brief-aan-mevrouw-van-Loon-directeur-Shell-Nederland-over-mensenrechtencommissie-Filipijnen/':('Publication','Klimaat','Duurzaamheid','Shell','Migrate'),
            'http://www.greenpeace.nl/2018/Publicaties/Klimaat--Energie/Brief-aan-de-heer-van-Beurden-directeur-Shell-over-mensenrechtencommissie-Filipijnen/':('Publication','Klimaat','Duurzaamheid','Shell','Migrate'),
            'http://www.greenpeace.nl/2018/Publicaties/Klimaat--Energie/Brief-aan-Zijne-Koninklijke-Hoogheid-Koning-Willem-Alexander-over-Predicaat-Koninklijk-Shell-/':('Publication','Klimaat','Olie','Shell','Migrate'),
            'http://www.greenpeace.nl/2018/Publicaties/Klimaat--Energie/Brief-aan-Kamerleden-Algemeen-Overleg-Milieuraad-van-Milieudefensie-Natuur--Milieu--en-Greenpeace/':('Publication','Klimaat','Duurzaamheid','Politiek','Migrate'),
            'http://www.greenpeace.nl/2018/Publicaties/Klimaat--Energie/Brief-aan-Minister-E-Wiebes-over-Klimaat--en-Energieakkoord/':('Publication','Klimaat','Duurzaamheid','Politiek','Migrate'),
            'http://www.greenpeace.nl/2018/Publicaties/Klimaat--Energie/Brief-aan-Kamerleden-Algemeen-Overleg-Klimaat-over-plan-van-aanpak-55-CO2-reductie-in-2030-/':('Publication','Klimaat','Duurzaamheid','Politiek','Migrate'),
            'http://www.greenpeace.nl/2018/Publicaties/Klimaat--Energie/Brief-aan-Minister-E-Wiebes-over-salderingsregeling/':('Publication','Klimaat','Duurzaamheid','Politiek','Migrate'),
            'http://www.greenpeace.nl/2018/Publicaties/Houden-bloemisten-van-bijen/':('Publication','Natuur','Landbouw','Bijen','Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Klimaat--Energie/Gezamenlijke-oproep-Kabinet-weeg-milieu-volledig-mee-in-uitbreidingsplannen-luchtvaart/':('Story','Klimaat','Duurzaamheid','Luchtvaart','Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Klimaat--Energie/Luchtvaartmanifest-zet-de-luchtvaart-op-het-juiste-spoor/':('Story','Klimaat','Duurzaamheid','Luchtvaart','Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Klimaat--Energie/Einde-van-kolentijdperk-in-zicht/':('Story','Klimaat','Kolen','','Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Klimaat--Energie/Vul-de-enquete-in-over-vliegen/':('Story','Klimaat','Duurzaamheid','Luchtvaart','Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Klimaat--Energie/Spectaculair-stroom-uit-wind-zonder-subsidie/':('Story','Klimaat','GroeneStroom','Oplossingen','Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Klimaat--Energie/Einde-tijdperk-traditionele-CV-ketel-in-zicht/':('Story','Klimaat','Duurzaamheid','Oplossingen','Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Klimaat--Energie/Greenpeace-onderhandelt-mee-over-klimaat--en-energieakkoord/':('Story','Klimaat','Duurzaamheid','Politiek','Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Klimaat--Energie/Shell-frustreert-onderzoek-mensenrechtencommissie/':('Story','Klimaat','Duurzaamheid','Shell','Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Klimaat--Energie/LIVE-ACTIE-BLOG-WADDENZEE/':('Story','Klimaat','Gas','','Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Klimaat--Energie/Campaigner-Cas-zo-was-het-om-actie-te-voeren-tegen-gasboringen-op-de-Noordzee/':('Story','Klimaat','Gas','','Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Klimaat--Energie/Vraag-de-Koning-Shell-te-ontkronen/':('Story','Klimaat','Olie','Shell','Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Klimaat--Energie/New-York-daagt-Shell-voor-de-rechter-om-klimaatverandering/':('Story','Klimaat','Olie','Shell','Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Landbouw/GOED-NIEUWS-VOOR-DE-BIJEN/':('Story','Natuur','Landbouw','Bijen','Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Landbouw/Veestapel-moet-krimpen-met-beleid/':('Story','Natuur','Landbouw','Oplossingen','Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Landbouw/Vergiftig-jij-je-relatie-deze-Valentijn/':('Story','Natuur','Landbouw','Bijen','Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Oceanen/106533-handtekeningen-voor-statiegeld-zo-reageren-supermarkten/':('Story','Natuur','Oceanen','Plastic','Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Oceanen/Statiegeld-dreigt-uitgesteld-te-worden-Dit-kan-jij-doen/':('Story','Natuur','Oceanen','Plastic','Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Oceanen/Mysterieuze-pinguin/':('Story','Natuur','Oceanen','Zuidpool','Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Oceanen/Download-de-app/':('Story','Natuur','Oceanen','Zuidpool','Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Oceanen/De-dans-die-het-internet-wilde-zien/':('Story','Natuur','Oceanen','Zuidpool','Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Oceanen/ACTIE-Neptunus--friends-duiken-op-bij-statiegelddebat/':('Story','Natuur','Oceanen','Plastic','Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Oceanen/Supermarkten-lobbyen-tegen-statiegeld-met-kleine-flesjes-en-blikjes/':('Story','Natuur','Oceanen','Plastic','Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Oceanen/Een-wereldwijde-mars-van-de-pinguins-voor-de-Zuidpool/':('Story','Natuur','Oceanen','Zuidpool','Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Oceanen/Zo-kun-jij-het-grootste-beschermde-gebied-TER-WERELD-realiseren/':('Story','Natuur','Oceanen','Zuidpool','Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Corporate/Rainbow-Warriors/':('Story','Greenpeace','OverOns','','Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Corporate/Vaarwel-Sirius/':('Story','Greenpeace','Duurzaamheid','OverOns','Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Corporate/Postcode-Loterij-helpt-Russische-bossen-uit-de-brand/':('Story','Greenpeace','Postcodeloterij','Bossen','Migrate'),
            'http://www.greenpeace.nl/2018/Nieuwsoverzicht/Corporate/Zo-geven-we-bedrijven-dus-vrij-spel/':('Story','Greenpeace','Duurzaamheid','Politiek','Migrate'),
            'http://www.greenpeace.nl/2018/Persberichten/Allereerste-missie-ooit-naar-de-Zuidpoolzeebodem-van-start-als-aftrap-wereldwijde-campagne-Greenpeace/':('Press Release','Natuur','Oceanen','Zuidpool','Migrate'),
            'http://www.greenpeace.nl/2018/Persberichten/-Mogelijk-weren-van-online-verkoop-bestrijdingsmiddelen-door-minister-Schouten-is-niet-afdoende/':('Press Release','Natuur','Landbouw','Bijen','Migrate'),
            'http://www.greenpeace.nl/2018/Persberichten/Majesteit-ontkroon-Shell/':('Press Release','Klimaat','Olie','Shell','Migrate'),
            'http://www.greenpeace.nl/2018/Persberichten/Ekoplaza-als-eerste-supermarkt-in-Nederland-voor-uitbreiding-van-statiegeld/':('Press Release','Natuur','Plastic','Oplossingen','Migrate'),
            'http://www.greenpeace.nl/2018/Persberichten/zeldzame-beelden-van-met-leven-bezaaide-bodem-zuidpoolzee-vastgelegd-door-greenpeace-onderzeeer/':('Press Release','Natuur','Oceanen','Zuidpool','Migrate'),
            'http://www.greenpeace.nl/2018/Persberichten/Minister-laat-kans-grootschalig-pesticidegebruik-aan-banden-te-leggen-onbenut/':('Press Release','Natuur','Landbouw','Bijen','Migrate'),
            'http://www.greenpeace.nl/2018/Persberichten/2409000--voor-Russische-brandweerteams-in-strijd-tegen-klimaatverandering/':('Press Release','Klimaat','Bossen','','Migrate'),
            'http://www.greenpeace.nl/2018/Persberichten/Valentijnsboeketten-blijken-rouwboeketten-voor-de-bijen/':('Press Release','Natuur','Landbouw','Bijen','Migrate'),
            'http://www.greenpeace.nl/2018/Persberichten/Greenpeace-actie-tegen-gasboringen-bij-Schiermonnikoog/':('Press Release','Klimaat','Gas','','Migrate'),
            'http://www.greenpeace.nl/2018/Persberichten/Actie-boorplatform-Schiermonnikoog-ten-einde/':('Press Release','Klimaat','Gas','','Migrate'),
            'http://www.greenpeace.nl/2018/Persberichten/Meerderheid-Rotterdammers-wil-af-van-kolen/':('Press Release','Klimaat','Kolen','','Migrate'),
            'http://www.greenpeace.nl/2018/Persberichten/15-miljoen-pinguins-ontdekt/':('Press Release','Natuur','Oceanen','Zuidpool','Migrate'),
            'http://www.greenpeace.nl/2018/Persberichten/Nagenoeg-alle-supermarkten-stappen-over-op-bij-vriendelijker-milieukeurmerk-On-the-way-to-PlanetProof/':('Press Release','Natuur','Landbouw','Bijen','Migrate'),
            'http://www.greenpeace.nl/2018/Persberichten/Europees-wetenschappelijk-bureau-EFSA-bevestigt-opnieuw-gevaar-van-chemische-bestrijdingsmiddelen-voor-bijen/':('Press Release','Natuur','Landbouw','Bijen','Migrate'),
            'http://www.greenpeace.nl/2018/Persberichten/God-van-de-Zee-roept-politici-op-voor-statiegeld-te-kiezen/':('Press Release','Natuur','Plastic','Oceanen','Migrate'),
            'http://www.greenpeace.nl/2018/Persberichten/Uitstellen-statiegeld-negeert-roep-van-samenleving-en-is-slechte-zaak-voor-het-milieu1/':('Press Release','Natuur','Plastic','Oceanen','Migrate'),
            'http://www.greenpeace.nl/2018/Persberichten/Greenpeace-voert-campagne-voor-bescherming-Zuidpool-met-augmented-reality-app/':('Press Release','Natuur','Oceanen','Zuidpool','Migrate'),
            'http://www.greenpeace.nl/2018/Persberichten/Denkbeeldige-Ipe-bomen-leiden-tot-echte-destructie-in-de-Amazone/':('Press Release','Natuur','Bossen','Amazone','Migrate'),
            'http://www.greenpeace.nl/2018/Persberichten/De-Tuinen--Holland-and-Barrett-stopt-met-verkoop-krillproducten/':('Press Release','Natuur','Oceanen','Successen','Migrate'),
            'http://www.greenpeace.nl/2018/Persberichten/Verandering-in-het-Greenpeace-lidmaatschap-van-de-Forest-Stewardship-Council-FSC/':('Press Release','Natuur','Bossen','OverOns','Migrate'),
            'http://www.greenpeace.nl/2018/Persberichten/Milieuorganisaties-slaan-handen-ineen-stop-groei-luchtvaart/':('Press Release','Klimaat','Duurzaamheid','Luchtvaart','Migrate'),
            'http://www.greenpeace.nl/2018/Persberichten/Greenpeace-blij-met-Schouten-toezegging-ban-neonics/':('Press Release','Natuur','Landbouw','Bijen','Migrate'),
            'http://www.greenpeace.nl/2018/Persberichten/Overwinning-voor-de-bijen-Greenpeace-blij-met-ban-op-neonics/':('Press Release','Natuur','Landbouw','Bijen','Migrate'),
            'http://www.greenpeace.nl/campaigns/landbouw/QuestionMark/Vragen-over-Palmolie/':('Story','Natuur','Bossen','Landbouw','Migrate'),
            'http://www.greenpeace.nl/campaigns/landbouw/Monsanto/':('Campaign','Natuur','Landbouw','','Migrate'),
            'http://www.greenpeace.nl/campaigns/landbouw/Gouden-Rijst/':('Story','Natuur','Landbouw','','Migrate'),
            'http://www.greenpeace.nl/campaigns/landbouw/milieu-impact-van-de-veehouderij/':('Campaign','Natuur','Landbouw','Vlees','Migrate'),
            'http://www.greenpeace.nl/2014/Nieuwsberichten/Klimaat--Energie/Als-je-dit-leest-twijfel-je-nooit-meer-aan-windmolens/':('Story','Klimaat','GroeneStroom','Oplossingen','Migrate'),
            'http://www.greenpeace.nl/campaigns/schone-energie/het-probleem/Kernenergie-onnodig-onveilig-en-duur/':('Campaign','Klimaat','Kernenergie','','Migrate'),
            'http://www.greenpeace.nl/about/Overleg-en-lobby/':('Campaign','Greenpeace','OverOns','Politiek','Migrate'),
            #'http://www.greenpeace.nl/Global/nederland/2012/Jaarverslag2011/Jaarverslag%202011.pdf':('Publication','Greenpeace','OverOns','Jaarverslag','Migrate'),
            #'http://www.greenpeace.nl/Global/nederland/2013/Jaarverslag2012/Jaarverslag%202012_DEF.pdf':('Publication','Greenpeace','OverOns','Jaarverslag','Migrate'),
            #'http://www.greenpeace.nl/Global/nederland/2014/Jaarverslag%202013/Greenpeace%20Nederland%20jaarverslag%202013.pdf':('Publication','Greenpeace','OverOns','Jaarverslag','Migrate'),
            #'http://www.greenpeace.nl/Global/nederland/2014/Jaarverslag%202014/PDF%20GP_jaarverslag_2014-defdef.pdf':('Publication','Greenpeace','OverOns','Jaarverslag','Migrate'),
            #'http://www.greenpeace.nl/Global/nederland/2016/corporate/GP_jaarverslag_jaarrekening_2015_DEF.pdf':('Publication','Greenpeace','OverOns','Jaarverslag','Migrate'),
            #'http://www.greenpeace.nl/Global/nederland/2017/Jaarverslag%202016/DEF%20DEF%20JVS%20GP%202016.pdf':('Publication','Greenpeace','OverOns','Jaarverslag','Migrate'),
            #'http://www.greenpeace.nl/Global/nederland/2018/Jaarverslag%202017/GP_jaarverslag_2017.pdf':('Publication','Greenpeace','OverOns','Jaarverslag','Migrate'),
            'http://www.greenpeace.nl/2016/Nieuwsberichten/Bossen/Eerste-boete-in-Nederland-voor-import-fout-hout/':('Story','Natuur','Bossen','Successen','Migrate'),
            'http://www.greenpeace.nl/2014/Nieuwsberichten/Klimaat--Energie/Goed-nieuws-voor-de-Noordpool/':('Story','Klimaat','Noordpool','Successen','Migrate'),
            'http://www.greenpeace.nl/2015/Nieuwsberichten/Klimaat--Energie/Shell-stopt-met-boren-in-Noordpoolgebied/':('Story','Klimaat','Noordpool','Olie','Migrate'),
            'http://www.greenpeace.nl/2017/Nieuwsberichten/Oceanen/grootste-tonijn-inblikker-kiest-een-duurzame-koers/':('Story','Natuur','Oceanen','Successen','Migrate'),
            'http://www.greenpeace.nl/2016/Nieuwsberichten/Oceanen/Nederlandse-supertrawlers-laat-Noord--en-Zuidpoolgebied-met-rust/':('Story','Natuur','Oceanen','Noordpool','Migrate'),
            'http://www.greenpeace.nl/2016/Nieuwsberichten/Landbouw/Supermarkten-op-de-bres-voor-de-bij/':('Story','Natuur','Bijen','Successen','Migrate'),
            'http://www.greenpeace.nl/2015/Nieuwsberichten/Landbouw/Praxis-bant-giftige-onkruidbestrijdingsmiddelen/':('Story','Natuur','Bijen','Successen','Migrate'),
            'http://www.greenpeace.nl/2014/Nieuwsberichten/Landbouw/Intratuin-kiest-voor-blije-bijen/':('Story','Natuur','Bijen','Successen','Migrate'),
            'http://www.greenpeace.nl/2016/Nieuwsberichten/Corporate/Geheime-TTIP-documenten-onthuld/':('Story','Greenpeace','Politiek','Successen','Migrate'),
            'http://www.greenpeace.nl/2016/Nieuwsberichten/Klimaat--Energie/Obama-weert-oliebedrijven-permanent-uit-Noordpoolgebied/':('Story','Klimaat','Noordpool','Olie','Migrate'),
            'http://www.greenpeace.nl/2017/Nieuwsberichten/Klimaat--Energie/Ziekenhuizen-musea-en-universiteiten-kopen-massaal-kolenstroom/':('Story','Klimaat','GroeneStroom','Oplossingen','Migrate'),
            'http://www.greenpeace.nl/2017/Nieuwsberichten/Klimaat--Energie/Hoe-groen-is-jouw-energiebedrijf/':('Story','Klimaat','GroeneStroom','Oplossingen','Migrate'),
            'http://www.greenpeace.nl/2017/Publicaties/Klimaat--Energie/Onderzoek-duurzaamheid-Nederlandse-stroomleveranciers-2017/':('Publication','Klimaat','GroeneStroom','Oplossingen','Migrate'),
            'http://www.greenpeace.nl/campaigns/schone-energie/het-probleem/':('Campaign','Klimaat','GroeneStroom','Kolen','Migrate'),
            'http://www.greenpeace.nl/campaigns/schone-energie/het-probleem/De-gevolgen-van-klimaatverandering-/':('Campaign','Klimaat','','','Migrate'),
            'http://www.greenpeace.nl/campaigns/schone-energie/zonnepanelen-windmolens-en-onderzoek-naar-ons-klimaat/':('Campaign','Klimaat','GroeneStroom','Oplossingen','Migrate'),
            #'http://www.greenpeace.nl/bestemark/':('Story','Klimaat','Duurzaamheid','Oplossingen','Migrate')
        }

        for url,data in start_urls.iteritems():
            post_type, categories, tags1, tags2, action = data
            if ( post_type=='Story' ):
                request = scrapy.Request(url, callback=self.parse_feature, dont_filter='true')
            elif ( post_type=='Publication' ):
                request = scrapy.Request(url, callback=self.parse_publication, dont_filter='true')
            elif ( post_type=='Press release' or post_type=='Press Release' ):
                request = scrapy.Request(url, callback=self.parse_press, dont_filter='true')
            elif ( post_type=='Feature' ):
                request = scrapy.Request(url, callback=self.parse_blog, dont_filter='true')
            elif ( post_type=='Campaign' ):
                request = scrapy.Request(url, callback=self.parse_campaign, dont_filter='true')

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
            'greenpeace':       'Greenpeace P4',
        }

        # Read in the file
        with open( 'gpnl_staging_v1_test.xml', 'r' ) as file :
            filedata = file.read()

        # Replace with correct usernames.
        for p3_author_username, p4_author_username in author_usernames.iteritems():
            filedata = filedata.replace('<author_username>' + p3_author_username, '<author_username>' + p4_author_username)

        # Remove dir="ltr" attributes from elements as requested.
        filedata = filedata.replace('dir="ltr"', '')

        # Write the file out again
        with open('gpnl_staging_v1_test.xml', 'w') as file:
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
                image_file = image_file.replace('/','http://www.greenpeace.nl/',1)
            imagesB_generated.append(image_file)


        pdfFiles=response.css('div.article a[href$=".pdf"]::attr(href)').extract()
        pdf_files_generated = list()
        for pdf_file in pdfFiles:
            print pdf_file
            if (pdf_file.startswith('/')):
                pdf_file = pdf_file.replace('/','http://www.greenpeace.nl/',1)
                print pdf_file
            pdf_files_generated.append(pdf_file)
            print pdf_files_generated

        date_field = response.xpath('//*[@id="content"]/div[4]/div/div[2]/span/text()').re_first(r' - \s*(.*)')
        date_field = self.filter_month_name(date_field)
        if date_field:
            date_field = dateutil.parser.parse(date_field)

        lead_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[1]/div').extract()[0]
        body_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[2]').extract()[0]
        if body_text:
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.nl/').replace('href="/', 'href="http://www.greenpeace.nl/')
            body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)
            if lead_text:
                body_text = '<div class="leader">' + lead_text + '</div>' + body_text + response.xpath(' //*[@id="content"]/div[4]/div/div[2]/p').extract_first()

        body_text = self.filter_post_content(body_text, response)

        subtitle = extract_with_css('div.article h2 span::text')
        if subtitle:
            body_text = '<h2>' + subtitle + '</h2><br />' + body_text

        yield {
            'type': 'Story',
            'p3_image_gallery': p3_image_gallery,
            #'title': extract_with_css('#content > div.happen-box.article > h1::text'),
            'title': response.xpath('//*[@id="content"]/div[4]/h1/span/text()').extract()[0],
            'subtitle': extract_with_css('div.article h1 span::text'),
            'author': 'Greenpeace NL',
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
                image_file = image_file.replace('/','http://www.greenpeace.nl/',1)
            imagesA_generated.append(image_file)

        imagesB=response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img/@src').extract()
        imagesB_generated = list()
        for image_file in imagesB:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.nl/',1)
            imagesB_generated.append(image_file)

        imagesEnlarge=response.xpath('//div[@class="news-list"]//div[@class="post-content"]//a[@class="open-img EnlargeImage"]/@href').extract()
        imagesEnlarge_generated = list()
        for image_file in imagesEnlarge:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.nl/',1)
            imagesEnlarge_generated.append(image_file)

        pdfFiles=response.css('div.article a[href$=".pdf"]::attr(href)').extract()
        pdf_files_generated = list()
        for pdf_file in pdfFiles:
            print pdf_file
            if (pdf_file.startswith('/')):
                pdf_file = pdf_file.replace('/','http://www.greenpeace.nl/',1)
                print pdf_file
            pdf_files_generated.append(pdf_file)
            print pdf_files_generated

        date_field = response.css('div.news-list .caption::text').re_first(r' - \s*(.*)')
        date_field = self.filter_month_name(date_field);
        if date_field:
            date_field = dateutil.parser.parse(date_field)

        image_gallery=response.xpath("//*[contains(@class, 'embedded-image-gallery')]")
        p3_image_gallery = 'false'
        if image_gallery:
            p3_image_gallery = 'true'

        body_text = response.css('div.news-list div.post-content').extract_first()
        if body_text:
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.nl/').replace('href="/', 'href="http://www.greenpeace.nl/')
            body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)

        body_text = self.filter_post_content(body_text, response)

        subtitle = extract_with_css('div.article h2 span::text')
        if subtitle:
            body_text = '<h2>' + subtitle + '</h2><br />' + body_text

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
            'thumbnail': thumbnail,
        }

    def parse_press(self, response):

        def extract_with_css(query):
            return response.css(query).extract_first()

        imagesA=response.xpath('//div[@class="news-list"]//div[@class="post-content"]//a[img]/@href').extract()
        imagesA_generated = list()
        for image_file in imagesA:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.nl/',1)
            imagesA_generated.append(image_file)

        imagesB=response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img/@src').extract()
        imagesB_generated = list()
        for image_file in imagesB:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.nl/',1)
            imagesB_generated.append(image_file)


        pdfFiles=response.css('div.article a[href$=".pdf"]::attr(href)').extract()
        pdf_files_generated = list()
        for pdf_file in pdfFiles:
            print pdf_file
            if (pdf_file.startswith('/')):
                pdf_file = pdf_file.replace('/','http://www.greenpeace.nl/',1)
                print pdf_file
            pdf_files_generated.append(pdf_file)
            print pdf_files_generated

        image_gallery=response.xpath("//*[contains(@class, 'embedded-image-gallery')]")
        p3_image_gallery = 'false'
        if image_gallery:
            p3_image_gallery = 'true'

        lead_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[1]/div/text()').extract()[0]
        body_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[2]').extract()[0]
        if body_text:
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.nl/').replace('href="/', 'href="http://www.greenpeace.nl/')
            body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)
            if lead_text:
                body_text = '<div class="leader">' + lead_text + '</div>' + body_text + response.xpath(' //*[@id="content"]/div[4]/div/div[2]/p').extract_first()

        body_text = self.filter_post_content(body_text, response)

        subtitle = extract_with_css('div.article h2 span::text')
        if subtitle:
            body_text = '<h2>' + subtitle + '</h2><br />' + body_text

        thumbnail = response.xpath('string(head//link[@rel="image_src"]/@href)').extract_first()
        date_field = response.xpath('string(//*[@id="content"]/div[4]/div/div[2]/span)').re_first(r' - \s*(.*)')
        date_field = self.filter_month_name(date_field);
        if date_field:
            date_field = dateutil.parser.parse(date_field)

        yield {
            'type': 'Press Release',
            'p3_image_gallery': p3_image_gallery,
            'title': extract_with_css('div.article h1 span::text'),
            #'subtitle': '',
            'author': 'Greenpeace NL',
            'author_username': 'greenpeace',
            #'date': response.css('#content > div.happen-box.article > div > div.text > span').re_first(r' - \s*(.*)'),
            'date': date_field,
            #'lead': extract_with_css('div.news-list div.post-content *:first-child strong::text'),
            'lead': lead_text,
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
            'url': response.url,
        }
     
               
    def parse_publication(self, response):

        def extract_with_css(query):
            return response.css(query).extract_first()

        imagesA=response.xpath('//div[@class="text"]/div[not(@id) and not(@class)]//a[img]/@href').extract()
        imagesA_generated = list()
        for image_file in imagesA:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.nl/',1)
            imagesA_generated.append(image_file)

        imagesB=response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[2]//img/@src').extract()
        imagesB_generated = list()
        for image_file in imagesB:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.nl/',1)
            imagesB_generated.append(image_file)
        
        pdfFiles=response.css('div.article a[href$=".pdf"]::attr(href)').extract()
        pdf_files_generated = list()
        for pdf_file in pdfFiles:
            if (pdf_file.startswith('/')):
                pdf_file = pdf_file.replace('/','http://www.greenpeace.nl/',1)
            pdf_files_generated.append(pdf_file)
            print pdf_files_generated

        date_field = response.css('div.article div.text span.author::text').re_first(r' - \s*(.*)')
        date_field = self.filter_month_name(date_field);
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
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.nl/').replace('href="/', 'href="http://www.greenpeace.nl/')
            body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)

        body_text = self.filter_post_content(body_text, response)

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
            'author': 'Greenpeace NL',
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


    def parse_campaign(self, response):

        def extract_with_css(query):
            return response.css(query).extract_first()

        image_gallery=response.xpath("//*[contains(@class, 'embedded-image-gallery')]")
        p3_image_gallery = 'false'
        if image_gallery:
            p3_image_gallery = 'true'

        # Extract Campaign banner image.
        campaign_banner = ''
        imagesA = response.xpath('//div[@class="visual-wrapper"]//img/@src').extract()
        imagesA_generated = list()
        for image_file in imagesA:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/', 'http://www.greenpeace.nl/', 1)
                campaign_banner = image_file
            imagesA_generated.append(image_file)

        imagesA = response.xpath('//div[@id="content"]//a[img]/@href').extract()
        for image_file in imagesA:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/', 'http://www.greenpeace.nl/', 1)
            imagesA_generated.append(image_file)

        imagesB=response.xpath('//*[@id="content"]//img/@src').extract()
        imagesB_generated = list()
        for image_file in imagesB:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.nl/',1)
            imagesB_generated.append(image_file)

        imagesEnlarge = response.xpath('//div[@id="content"]//a[@class="open-img EnlargeImage"]/@href').extract()
        imagesEnlarge_generated = list()
        for image_file in imagesEnlarge:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/', 'http://www.greenpeace.nl/', 1)
            imagesEnlarge_generated.append(image_file)
        if len(imagesB_generated) == 0 and len(imagesEnlarge_generated):
            imagesB_generated = imagesEnlarge_generated

        pdfFiles=response.css('div.article a[href$=".pdf"]::attr(href)').extract()
        pdf_files_generated = list()
        for pdf_file in pdfFiles:
            print pdf_file
            if (pdf_file.startswith('/')):
                pdf_file = pdf_file.replace('/','http://www.greenpeace.nl/',1)
                print pdf_file
            pdf_files_generated.append(pdf_file)
            print pdf_files_generated

        date_field = response.xpath('//*[@id="content"]/div[4]/div/div[2]/span/text()').re_first(r' - \s*(.*)')
        date_field = self.filter_month_name(date_field)
        if date_field:
            date_field = dateutil.parser.parse(date_field)

        heading_text = response.xpath('//*[@id="content"]/div[4]/div/h1').extract_first()
        body_text = response.xpath('//*[@id="content"]/div[4]').extract()[0]

        extra_body_text = response.xpath('//*[@id="content"]/div[@class="hub-text-below"]').extract()[0]
        if extra_body_text:
            body_text = body_text + extra_body_text

        if body_text:
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.nl/').replace('href="/', 'href="http://www.greenpeace.nl/')
            body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)
            # The heading was within the main content, hence removed.
            if heading_text:
                body_text = body_text.replace(heading_text, '')

        # Attache campaign banner image at top of post.
        if campaign_banner != '':
            body_text = '<img src="' + campaign_banner + '" ><br>' + body_text

        body_text = self.filter_post_content(body_text, response)

        title = response.xpath('//*[@id="content"]/div[4]/div/h1/text()').extract_first()
        # if title text is missing, pick first h2 or h3 from article content.
        if not title:
            title = response.xpath('//*[@id="content"]/div[4]/div/h2').extract_first()
            if title:
                title = re.sub('\<h2\>\<strong\>(.*)\<br\><\/strong\>\<\/h2\>', '\g<1>', title)
        if not title:
            title = response.xpath('//*[@id="content"]/div[4]/div/h3/text()').extract_first()

        yield {
            'type': 'Story',
            'p3_image_gallery': p3_image_gallery,
            #'title': extract_with_css('#content > div.happen-box.article > h1::text'),
            'title': title,
            'subtitle': extract_with_css('div.article h1 span::text'),
            'author': 'Greenpeace NL',
            'date': date_field,
            #'lead': extract_with_css('div.news-list div.post-content *:first-child strong::text'),
            'lead': '',
            'categories': response.meta['categories'],
            'text':  body_text,
            'imagesA': imagesA_generated,
            'imagesEnlarge': imagesEnlarge_generated,
            'imagesB': imagesB_generated,
            #'imagesB': response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img[not(ancestor::a)]/@src').extract(), #don't import image if there's an a tag around it
            'imagesC': response.xpath('//div[@class="gallery"]//div[@class="img-nav"]//a/@rel').extract(), # Galleries (horrible html)
            'pdfFiles': pdf_files_generated,
            'tags1': response.meta['tags1'],
            'tags2': response.meta['tags2'],
            'url': response.url,
        }


    def filter_month_name(self, month_name):
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

        if month_name:
            # Replace with dutch month name with english month name.
            for nl_month, en_month in month_nl_en.iteritems():
                month_name = month_name.replace(nl_month, en_month)

        return month_name;

    def filter_post_content(self, post_data, response):
        # Search and replace the related articles section from article.
        post_data = re.sub('\<li class="ccsnlink"\>([\w\W]*)\<\/li\>', '', post_data)
        post_data = re.sub('\<h3 title\=\"Gerelateerde berichten\:?\"\>Gerelateerde berichten\:?\<\/h3\>', '', post_data, flags=re.IGNORECASE)
        post_data = re.sub('\<input class="hidAjaxInput" .*\>', '', post_data)
        post_data = re.sub('\<div class="ccsnlink">[\s\<ul\>\\n\/]*\<\/div\>', '', post_data)
        post_data = re.sub('\<div class="csn listings items">[\s\\n]*\<\/div\>', '', post_data)

        return post_data
