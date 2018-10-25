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
        'FEED_URI': 'gphu_staging_v3.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    __connector_csv_filename = "connector_v2_final.csv"
    __connector_csv_log_file = "connector_csv_log_v2"

    def start_requests(self):
        start_urls = {
            #total_posts: 375
            #bad_posts:   20
            #part1
            #'http://www.greenpeace.org/hungary/hu/sajtokozpont/250-ezer-evig-kene-tarolnunk-Paks-II-atomhulladekat/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Szaz-evig-is-kiserthet-meg-a-fukusimai-katasztrofa/':('Sajtóközlemény','Klíma & Energia','Atomenergia','Egészség','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/240-Greenpeace-aktivista-figyelmeztet-Europa-uj-veszelyzonaba-lepett/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/217-civil-szervezet-szolitotta-fel-az-unios-minisztereket-hogy-vessenek-veget-a-tengerek-tulhalaszatanak/':('Sajtóközlemény','Természet & Környezet','Élővilág','Víz','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/170412_civil_allasfoglalas/':('Sajtóközlemény','Ember & Társadalom','Béke','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/170405_romaipart/':('Sajtóközlemény','Természet & Környezet','Zöldterület','Egészség','Élővilág','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/14-millio-forintra-perli-az-allam-a-Greenpeace-t-es-Kishantost/':('Sajtóközlemény','Ember & Társadalom','ÖkológiaiGazdálkodás','Béke','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/118-civil-szervezet-kiall-a-helyi-kozossegekert-a-bekes-Magyarorszagert-dolgozo-civilekert/':('Sajtóközlemény','Ember & Társadalom','Béke','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/107-civil-szervezet-nyilt-levele-Magyarorszag-ne-tamogassa-a-CETA-elfogadasat/':('Sajtóközlemény','Ember & Társadalom','Fogyasztás','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/100-megujulo-energia-mindenkinek/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','Megújulók','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/-Totalis-energiafuggseg-es-kiszolgaltatottsag/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Valaszuton-a-mezgazdasag/':('Kiadvány','Természet & Környezet','ÖkológiaiGazdálkodás','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Progressziv-EnergiaForradalom-2011-Magyar/':('Kiadvány','Klíma & Energia','Klímavédelem','Megújulók','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Okomodszerek-szantofoldon/':('Kiadvány','Természet & Környezet','ÖkológiaiGazdálkodás','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Okologiai-allattenyesztes-a-vilagban-es-otthon/':('Kiadvány','Természet & Környezet','ÖkológiaiGazdálkodás','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Mit-tettunk-2016-ban/':('Kiadvány','','Greenpeace','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Mergek-vagy-mehek/':('Kiadvány','Természet & Környezet','Élővilág','Méhek','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Mehpusztulas/':('Kiadvány','Természet & Környezet','Élővilág','Méhek','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Megujulo-energia-megallas-nelkul/':('Kiadvány','Klíma & Energia','Megújulók','Klímavédelem','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Maszatos-adatok/':('Kiadvány','Ember & Társadalom','Fogyasztás','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Kiteregetjuk-a-szennyest/':('Kiadvány','Ember & Társadalom','Szennyezés','Fogyasztás','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/zoldterulet-kozvelemenykutatas-201708/':('Sajtóközlemény','Természet & Környezet','Zöldterület','Egészség','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Zold-civil-szervezetek-udvozlik-a-szabadkereskedelmi-egyezmenyekkel-kapcsolatos-orszaggylesi-hatarozatot/':('Sajtóközlemény','Ember & Társadalom','Fogyasztás','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Videoval-es-kozjegyzvel-bizonyitja-a-Greenpeace-hogy-a-Sparban-vasarolta-a-paprikat/':('Sajtóközlemény','Természet & Környezet','Szennyezés','Egészség','Fogyasztás','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Veszelyes-vegyszereket-talalt-markas-turaruhakban-a-Greenpeace/':('Sajtóközlemény','Természet & Környezet','Szennyezés','Fogyasztás','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Veszelyes-vegyi-anyagok-a-divatban--nemcsak-a-Zaranak-vannak-mocskos-titkai/':('Sajtóközlemény','Természet & Környezet','Szennyezés','Egészség','Fogyasztás','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Veszelybe-kerulhet-hazank-nuklearis-biztonsaga/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            #'http://www.greenpeace.org/hungary/hu/sajtokozpont/Versenyfutas-az-idvel-a-mehekert/':('Sajtóközlemény','Természet & Környezet','Méhek','Szennyezés','Élővilág','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/vegyszerkorlatozas-kell-a-mehek-erdekeben/':('Sajtóközlemény','Természet & Környezet','Méhek','Szennyezés','Élővilág','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Vegre-megsznhet-a-meregkeveres-az-almasfuziti-vorosiszap-tarozon/':('Sajtóközlemény','Természet & Környezet','Szennyezés','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Vedelmet-kaptak-a-mehek-az-EU-betiltotta-harom-mehgyilkos-vegyszer-unios-hasznalatat/':('Sajtóközlemény','Természet & Környezet','Méhek','Szennyezés','Élővilág','article','Migrate'),
            #'http://www.greenpeace.org/hungary/hu/sajtokozpont/Uszo-Csernobil-ellen-tiltakoznak-Greenpeace-aktivistak-Dania-partjainal/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Unokaink-is-fizetni-fogjak-a-paksi-bvitest/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Ujra-uton-a-Greenpeace/':('Sajtóközlemény','Természet & Környezet','ÖkológiaiGazdálkodás','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Ujra-felelotlen-dontes-szuletett-a-Romai-partrol-55-ezer-ember-biztonsaga-es-Budapest-egyik-utolso-termeszetkozeli-Duna-partja-a-tet/':('Sajtóközlemény','Természet & Környezet','Zöldterület','Egészség','Élővilág','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Ujabb-mehgyilkos-mezgazdasagi-vegyszer-hasznalatat-korlatozza-az-EU/':('Sajtóközlemény','Természet & Környezet','Méhek','Szennyezés','Élővilág','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Ujabb-kerdjelek-Magyarorszag-nuklearis-biztonsaga-korul/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Ujabb-jogi-szakvelemeny-a-Greenpeace-mellett-Almasfuzit-ugyeben/':('Sajtóközlemény','Természet & Környezet','Szennyezés','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Uj-GM-noveny-termeszteset-engedelyezne-az-Europai-Bizottsag--a-biztonsagra-vonatkozo-vizsgalatok-sulyos-hianyossagai-ellenere/':('Sajtóközlemény','Természet & Környezet','Egészség','ÖkológiaiGazdálkodás','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Tovabbra-is-rengeteg-vegyszer-van-a-ruhakban---meg-a-boltok-levegje-is-szennyezett/':('Sajtóközlemény','Természet & Környezet','Szennyezés','Egészség','Fogyasztás','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Tovabbra-is-folyik-a-fertz-szennyezes-a-Szamosba/':('Sajtóközlemény','Természet & Környezet','Szennyezés','Egészség','Élővilág','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Tovabb-huzodik-Kishantos-ugye/':('Sajtóközlemény','Ember & Társadalom','Béke','ÖkológiaiGazdálkodás','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Tobbsegi-tamogatast-kapott-a-mehgyilkos-vegyszerek-korlatozasarol-szolo-europai-bizottsagi-javaslat/':('Sajtóközlemény','Természet & Környezet','Méhek','ÖkológiaiGazdálkodás','Élővilág','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Tobb-mint-otvenezer-magyar-koveteli-az-eldobhato-manyag-szatyrok-betiltasat/':('Sajtóközlemény','Természet & Környezet','StopMűanyag','Szennyezés','Fogyasztás','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Tizenegy-Nobel-bekedijas-ir-Putyin-elnoknek-a-Greenpeace-ugy-kapcsan/':('Sajtóközlemény','Természet & Környezet','Béke','Sarkvidék','Klímavédelem','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Tiszta-Adriat-/':('Sajtóközlemény','Természet & Környezet','Víz','Fosszilis','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Tiltott-anyaggal-tiltott-modszerrel-irtjak-a-ragcsalokat-itthon/':('Sajtóközlemény','Természet & Környezet','Élővilág','Szennyezés','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Termeshozamrekord-mehgyilkos-vegyszerek-nelkul/':('Sajtóközlemény','Ember & Társadalom','ÖkológiaiGazdálkodás','Méhek','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Termesatlagrekordok-mehgyilkos-vegyszerek-hasznalata-nelkul/':('Sajtóközlemény','Ember & Társadalom','ÖkológiaiGazdálkodás','Méhek','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Szuksegtelenul-roviditik-eletunket-a-szenes-ermvek/':('Sajtóközlemény','Klíma & Energia','Fosszilis','Egészség','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Szuksegtelen-es-elkapkodott-az-uj-atomerm/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Sztarokkal-indit-kampanyt-a-Greenpeace-az-Eszaki-sark-megmenteseert/':('Sajtóközlemény','Klíma & Energia','Sarkvidék','Klímavédelem','Fosszilis','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Szabadon-engedi-Oroszorszag-a-Greenpeace-hajojat/':('Sajtóközlemény','Ember & Társadalom','Béke','Sarkvidék','Klímavédelem','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Szabad-paprikat/':('Sajtóközlemény','Természet & Környezet','Egészség','ÖkológiaiGazdálkodás','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Surgos-vedelmet-a-varosi-faknak/':('Sajtóközlemény','Természet & Környezet','Élővilág','Zöldterület','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Sulyosan-egeszsegkarosito-es-gazdasagtalan-hulladekegetket-tamogatna-a-kormany/':('Sajtóközlemény','Természet & Környezet','Szennyezés','Egészség','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Sulyos-szennyezk-a-Hortobagyi-Nemzeti-Park-hataran-mar-a-kornyezetben--a-Greenpeace-vizsgalat-eredmenyei/':('Sajtóközlemény','Természet & Környezet','Szennyezés','MérgezettÖrökségünk','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Sokan-vannak-akik-csipik-a-meheket/':('Sajtóközlemény','Természet & Környezet','Élővilág','Méhek','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Simaszkos-emberek-tortek-be-az-oroszorszagi-Greenpeace-iroda-udvaraba/':('Sajtóközlemény','Ember & Társadalom','Béke','Klímavédelem','Sarkvidék','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Sikeresen-megzavartak-Greenpeace-aktivistak-a-kishantosi-foldek-mai-arvereset/':('Sajtóközlemény','Ember & Társadalom','Béke','ÖkológiaiGazdálkodás','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Siker-vegre-megkezddhet-az-Illatos-uti-vegyianyag-telep-karmentesitese/':('Sajtóközlemény','Természet & Környezet','Szennyezés','MérgezettÖrökségünk','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/romai_fellebbezes/':('Sajtóközlemény','Természet & Környezet','Zöldterület','Élővilág','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Rabolintott-a-Parlament-Paks-2-hitelszerzdesere/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Paks2_jogserto_allami_tamogatasa/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Paks-II-zsakutca-a-jovo-a-megujuloke/':('Sajtóközlemény','Klíma & Energia','Atomenergia','Megújulók','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Paks-II-vel-kapcsolatban-eveken-at-felretajekoztatott-a-magyar-kormany/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Paks-II-nek-egyedul-a-neve-nem-titkos/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Paks-II-kornyezetvedelmi-engedelyezesenek-felfuggeszteset-keri-a-Greenpeace/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Paks-II-kornyezetvedelmi-engedelye-jogszabalysert-es-megalapozatlan/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Paks-II-Candole/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Paks-II-Ausztria-tiltott-tamogatas/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Paks-II-allami-tamogatas/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Paks-helyett-megujulokat/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Paks-es-MVM-helycseres-tamadas-a-megujulok-ellen/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Ot-evre-engedelyeztek-a-rakkockazatu-glifozat-tovabbi-hasznalatat-az-unios-tagallamok/':('Sajtóközlemény','Természet & Környezet','Szennyezés','ÖkológiaiGazdálkodás','Szennyezés','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Orszagos-eladas-sorozatra-indul-a-Greenpeace-Kishantosert-/':('Sajtóközlemény','Természet & Környezet','ÖkológiaiGazdálkodás','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Orosz-rulett--A-Roszatom-kockazatai/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Oriaskalapaccsal-tuntettek-a-CETA-ellen/':('Sajtóközlemény','Ember & Társadalom','Fogyasztás','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Orban-Putyin-Paks-II-rl/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Olyan-gat-kell-amely-a-lakossagot-es-a-Romai-part-arteri-erdejet-egyarant-megvedi/':('Sajtóközlemény','Természet & Környezet','Zöldterület','Élővilág','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Okogazdakepzest-tart-Kishantoson-a-Greenpeace/':('Sajtóközlemény','Természet & Környezet','ÖkológiaiGazdálkodás','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Nyakunkon-az-ujabb-genmodositott-kukorica/':('Sajtóközlemény','Természet & Környezet','ÖkológiaiGazdálkodás','Egészség','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Nemzetkozi-bizottsag-eltt-kell-magyarazkodnia-ma-a-kormanynak-Paks-II-miatt/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            #part2
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Nemzetkozi-birosag-kotelezi-Oroszorszagot-a-Greenpeace-aktivistak-szabadon-bocsatasara/':('Sajtóközlemény','Ember & Társadalom','Béke','Sarkvidék','Klímavédelem','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Nem-kerunk-amerikai-hormonkezelt-genmodositott-elelmiszereket/':('Sajtóközlemény','Természet & Környezet','ÖkológiaiGazdálkodás','Egészség','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Ne-tamogassa-a-magyar-kormany-hogy-a-TTIP-vel-a-nagyvallalatok-erdekei-felulkerekedjenek-a-magyar-emberek-erdekein/':('Sajtóközlemény','Ember & Társadalom','Fogyasztás','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Ne-hagyjuk-hogy-az-EU-rank-kenyszeritse-az-ujabb-genmodositott-kukoricat/':('Sajtóközlemény','Természet & Környezet','ÖkológiaiGazdálkodás','Egészség','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Ne-engedjuk-elpaksolni-a-jovonket/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Nagy-lepest-tettunk-a-tengeri-halallomanyok-megmentese-fele/':('Sajtóközlemény','Természet & Környezet','Víz','Élővilág','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Nagy-europai-almafoldteszt/':('Sajtóközlemény','Természet & Környezet','Szennyezés','Egészség','Fogyasztás','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Most-Jogtalanul-aratnak-Kishantoson/':('Sajtóközlemény','Ember & Társadalom','Béke','ÖkológiaiGazdálkodás','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/MOST-Greenpeace-aktivistak-a-kishantosi-foldarveres-epuletenek-tetejen/':('Sajtóközlemény','Ember & Társadalom','Béke','ÖkológiaiGazdálkodás','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Most-dolhet-el-a-klimaegyezmeny-sorsa/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','Megújulók','Fosszilis','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Mondjunk-nemet-a-CETA-ra/':('Sajtóközlemény','Ember & Társadalom','Fogyasztás','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Miert-szennyez-egy-ev-utan-is-a-hortobagyi-meregraktar/':('Sajtóközlemény','Természet & Környezet','Szennyezés','Egészség','MérgezettÖrökségünk','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Miert-nincsenek-tovabbra-sem-felelsei-a-kolontari-katasztrofanak/':('Sajtóközlemény','Természet & Környezet','Szennyezés','Egészség','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Mi-tortent-az-elhagyatott-veszelyes-hulladekkal-Kiskunhalason/':('Sajtóközlemény','Természet & Környezet','Szennyezés','Élővilág','MérgezettÖrökségünk','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Mergezett-oroksegunk--Szennyezett-teruletek-idzitett-vegyi-bombak-Magyarorszagon/':('Sajtóközlemény','Természet & Környezet','Szennyezés','Élővilág','MérgezettÖrökségünk','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Mergek-szivarognak-a-Hortobagyi-Nemzeti-Parkba/':('Sajtóközlemény','Természet & Környezet','Szennyezés','Élővilág','MérgezettÖrökségünk','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Meregtelenitk-es-zoldrefestk-a-Greenpeace-rangsorolta-a-detoxos-divatcegeket/':('Sajtóközlemény','Ember & Társadalom','Szennyezés','Fogyasztás','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Ments-meg-te-is-meheket-a-holnapi-Giving-Tuesday-alkalmabol/':('Sajtóközlemény','Ember & Társadalom','Greenpeace','Méhek','Élővilág','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Mehpusztulas-Balatonlelle-tersegeben/':('Sajtóközlemény','Természet & Környezet','Élővilág','Méhek','ÖkológiaiGazdálkodás','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Mehkaptarak-a-budapesti-Kossuth-teren--Tilalmat-a-mehgyilkos-vegyszerekre/':('Sajtóközlemény','Természet & Környezet','Élővilág','Méhek','ÖkológiaiGazdálkodás','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Megvan-a-hortobagyi-Greenpeace-meres-eredmenye/':('Sajtóközlemény','Természet & Környezet','Szennyezés','MérgezettÖrökségünk','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Megszabadulhatunk-a-rakkeltessel-gyanusitott-gyomirtotol/':('Sajtóközlemény','Természet & Környezet','ÖkológiaiGazdálkodás','Szennyezés','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Megoltek-a-kishantosi-fold-egy-darabjat/':('Sajtóközlemény','Ember & Társadalom','Béke','ÖkológiaiGazdálkodás','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Megint-zajlik-a-barbar-pusztitas-Kishantoson/':('Sajtóközlemény','Ember & Társadalom','Béke','ÖkológiaiGazdálkodás','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Megerkezett-hazankba-is-a-vilag-egyik-vezet-meregkeverje-a-GAP/':('Sajtóközlemény','Ember & Társadalom','Fogyasztás','Egészség','Szennyezés','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Meg-tehetunk-a-Paksi-paktum-elkeruleseert/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Meg-mindig-nem-tudjuk-szabalyszeren-uzemeltettek-e-a-vorosiszap-tarozot-a-kolontari-katasztrofa-eltt/':('Sajtóközlemény','Természet & Környezet','Szennyezés','Egészség','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Meg-mindig-mergeznek-a-regi-oroksegek/':('Sajtóközlemény','Természet & Környezet','MérgezettÖrökségünk','Szennyezés','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Median---Varosliget/':('Sajtóközlemény','Természet & Környezet','Zöldterület','Élővilág','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Matol-eletbe-lep-a-parizsi-klimaegyezmeny/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','Fosszilis','Megújulók','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Maradjon-igazi-park-a-Varosliget-a-vilag-els-kozparkja/':('Sajtóközlemény','Természet & Környezet','Zöldterület','Élővilág','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Magyarorszagnak-volt-igaza-torvenysert-az-Amflora-GM-burgonya-unios-engedelye-es-maga-az-engedelyezesi-eljaras-is/':('Sajtóközlemény','Természet & Környezet','ÖkológiaiGazdálkodás','Szennyezés','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Magyarorszagnak-tamogatnia-kell-a-mehgyilkos-vegyszerek-tilalmat-/':('Sajtóközlemény','Természet & Környezet','ÖkológiaiGazdálkodás','Egészség','Méhek','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Magyarorszag-sikerrel-allt-ki-az-unios-halaszati-reform-mellett/':('Sajtóközlemény','Természet & Környezet','Víz','Élővilág','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Magyarorszag-meg-megallithatja-a-CETA-t/':('Sajtóközlemény','Ember & Társadalom','Fogyasztás','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Magyarorszag-az-unios-halaszati-reform-nyertese-lehet/':('Sajtóközlemény','Természet & Környezet','Víz','Élővilág','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/MagyarokPaks-II-20/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Magyarok-PaksII-1-0/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Magyar-mveszek-is-kialltak-a-Greenpeace-aktivistakert/':('Sajtóközlemény','Klíma & Energia','Béke','Sarkvidék','Klímavédelem','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Magasabb-klimavedelmi-cel-az-Unioban-amellyel-a-magyar-gazdasag-is-jo-jar/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Ma-lepett-eletbe-a-CETA-veszelyben-az-europai-unios-elelmiszeripari-es-mezgazdasagi-elirasok/':('Sajtóközlemény','Ember & Társadalom','Fogyasztás','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Luxus-a-meregtelenites/':('Sajtóközlemény','Ember & Társadalom','Fogyasztás','Egészség','Szennyezés','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Lenduletbl-atugrhato-a-szakadek-az-energiabiztonsag-fele/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Legyztek-a-vasarlok-a-vilag-legnagyobb-divatmarkajat-a-Zarat/':('Sajtóközlemény','Ember & Társadalom','Egészség','Fogyasztás','Szennyezés','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Legszennyezettsegben-az-Unio-legrosszabbjai-kozott-vagyunk/':('Sajtóközlemény','Ember & Társadalom','Egészség','Szennyezés','Levegő','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Lakott-teruleten-is-kimutathatoak-a-Budapesti-Vegyimvek-szennyezi--a-Greenpeace-harompontos-kovetelese/':('Sajtóközlemény','Ember & Társadalom','Szennyezés','MérgezettÖrökségünk','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Kozos-nyilatkozatban-keri-21-szervezet-a-kormanyt-a-menekultvalsag-humanus-kezelesere/':('Sajtóközlemény','Ember & Társadalom','Béke','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Kozos-nyilatkozat-A-batorsagot-nem-lehet-beszantani/':('Sajtóközlemény','Ember & Társadalom','ÖkológiaiGazdálkodás','Béke','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Kozmeghallgatas-Paks-2-epiteserl-aldemokratikus-szinjatek1/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Kozelhallgatas-Pakson/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Kozel-2000-helyen-el-tovabb-Kishantos/':('Sajtóközlemény','Természet & Környezet','ÖkológiaiGazdálkodás','Béke','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Komoly-allampolgari-nyomas-es-jo-par-nap-kellett-ahhoz-hogy-beengedjek-a-fuggetlen-szakertket-a-volt-Hungexpo-teruletere/':('Sajtóközlemény','Természet & Környezet','Zöldterület','Szennyezés','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Kiszivarogtatasi-botrany-a-CETA-korul-is/':('Sajtóközlemény','Ember & Társadalom','Fogyasztás','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Kiszivarogtak-a-TTIP-dokumentumok-valoban-veszelyben-a-klima-a-kornyezet-es-a-fogyasztok-vedelme-st-unios-alapelvek-is/':('Sajtóközlemény','Ember & Társadalom','Fogyasztás','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Kiszivarogtak-a-TiSA-dokumentumok-is-veszelyben-a-klima-a-kornyezet-es-az-emberek-erdeke/':('Sajtóközlemény','Ember & Társadalom','Fogyasztás','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Kiskapukkal-teli-a-GM-novenyek-EU-tagallami-szint-tiltasanak-terve/':('Sajtóközlemény','Természet & Környezet','ÖkológiaiGazdálkodás','Egészség','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Kishantos-pert-nyert-a-magyar-allammal-szemben/':('Sajtóközlemény','Ember & Társadalom','Béke','ÖkológiaiGazdálkodás','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Kiderult-kik-felelsek-a-klimavaltozasert-a-Gazprom-es-a-Shell-az-els-tizben/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Kiderul-e_hogy_a_MAL_Zrt_mukodese_szabalyos_volt_a_vorosiszap-katasztrofat_megelozoen/':('Sajtóközlemény','Természet & Környezet','Szennyezés','Egészség','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Ki-ellenrizheti-a-kishantosi-foldpalyazatokat-ha-a-birosag-sem/':('Sajtóközlemény','Ember & Társadalom','ÖkológiaiGazdálkodás','Béke','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Jogsert-az-almasfuziti-vorosiszap-tarozon-folyo-tevekenyseg/':('Sajtóközlemény','Természet & Környezet','Szennyezés','Egészség','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Jogersen-pert-nyert-a-szennyezesek-felszamolasaert-dolgozo-Greenpeace-a-torvenysert-Baranya-Megyei-Kormanyhivatallal-szemben/':('Sajtóközlemény','Ember & Társadalom','Szennyezés','Béke','MérgezettÖrökségünk','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Jo-hir-Kishantosnak/':('Sajtóközlemény','Ember & Társadalom','ÖkológiaiGazdálkodás','Béke','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Japan-unnepli-els-atomenergia-nelkuli-evet-es-a-tiszta-energiaju-jov-szuleteset/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Japan-lekapcsolja-az-utolso-atomeromuvet--Magyarorszag-is-kovethetne-a-peldat/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Illegalis-a-Mohi-atomerm-epitese/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Illatos-ut-fontos-lepes-hogy-eltntek-a-hordok-de-a-nagy-feladat-meg-hatra-van/':('Sajtóközlemény','Természet & Környezet','MérgezettÖrökségünk','Szennyezés','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Illatos-ut-a-kalyhakban-evi-sok-ezer-aldozatot-kovetel-es-tobb-millio-torvenysertest-jelent-a-haztartasi-szemetegetes-/':('Sajtóközlemény','Természet & Környezet','MérgezettÖrökségünk','Szennyezés','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Hogyan-teszik-tonkre-a-novenyved-szerek-az-elvilagot/':('Sajtóközlemény','Természet & Környezet','ÖkológiaiGazdálkodás','Szennyezés','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Haztaji-tojasokat-vizsgalt-a-Greenpeace-az-Illatos-ut-kornyeken/':('Sajtóközlemény','Természet & Környezet','MérgezettÖrökségünk','Szennyezés','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Hany-mehek-napja-lesz-meg-hatra/':('Sajtóközlemény','Természet & Környezet','Élővilág','Méhek','ÖkológiaiGazdálkodás','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Halaszhajo-a-Hosok-teren/':('Sajtóközlemény','Természet & Környezet','Élővilág','Víz','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Halalos-csapas-lehet-a-magyar-videkre-a-foldkiarusitas--temetessel-tiltakozott-a-Greenpeace/':('Sajtóközlemény','Természet & Környezet','ÖkológiaiGazdálkodás','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Gyzott-a-Greenpeace-Magyarorszag-a-baranyai-adatkeresi-perben/':('Sajtóközlemény','Ember & Társadalom','Szennyezés','MérgezettÖrökségünk','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Gyzelem-Levonul-a-Shell-az-Eszaki-sarkvidekrl/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','Fosszilis','Sarkvidék','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Gyzelem-Kishantoson-ervenytelen-az-egyik-uj-nyertes-szerzdese-uj-eljaras-indul/':('Sajtóközlemény','Természet & Környezet','ÖkológiaiGazdálkodás','Béke','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Gyzelem-Hortobagyon-felszamoljak-a-meregraktart/':('Sajtóközlemény','Természet & Környezet','Szennyezés','MérgezettÖrökségünk','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Gyomrost-kapott-egyik-aktivistank-Kishantoson/':('Sajtóközlemény','Ember & Társadalom','Béke','ÖkológiaiGazdálkodás','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Greenpeace-paprikavizsgalat-mergezett-vagy-tiszta/':('Sajtóközlemény','Természet & Környezet','Szennyezés','Egészség','Fogyasztás','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Greenpeace-hajotura-indul-Europa-tengerein-a-kishalaszok-tamogatasaert-/':('Sajtóközlemény','Természet & Környezet','Víz','Élővilág','','article','Migrate'),
            #part3
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Greenpeace-erdment-allomas-a-Fogarasi-havasokban/':('Sajtóközlemény','Természet & Környezet','Élővilág','Erdő','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Greenpeace-aktivistak-ravilagitottak-a-nuklearis-energia-veszelyeire/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Greenpeace-aktivistak-napelemeket-helyeztek-az-Europai-Parlament-epuletere-mikozben-a-megujulo-energia-jovjerl-folyt-a-targyalas/':('Sajtóközlemény','Klíma & Energia','Megújulók','Klímavédelem','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Greenpeace-aktivistak-foglaltak-el-ket-Shell-kutat/':('Sajtóközlemény','Klíma & Energia','Fosszilis','Sarkvidék','Klímavédelem','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Greenpeace-aktivistak-foglaltak-el-egy-jegtoro-hajot-Helsinki-kikotojeben/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','Fosszilis','Sarkvidék','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Greenpeace-aktivistak-a-Jov-zaszlaja-elhelyezesevel-jelkepesen-vedett-terulette-nyilvanitottak-az-Eszaki-sarkot/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','Sarkvidék','Fosszilis','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Greenpeace-akcio-a-Forma-1-Belga-Nagydijon-a-Shell-ellen/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','Fosszilis','Sarkvidék','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Globalis-eghajlatvedelmi-megallapodast-irnak-ala-New-Yorkban-a-Fold-napjan/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/glifozat_nyilt_level_fm/':('Sajtóközlemény','Természet & Környezet','ÖkológiaiGazdálkodás','Szennyezés','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Genmodositott-elelmiszerek-a-boltokban-De-melyekben-/':('Sajtóközlemény','Természet & Környezet','ÖkológiaiGazdálkodás','Egészség','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/G7-csucs-tortenelmi-felelsseg-a-klimavalsag-elleni-harcban/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/G20-A-Greenpeace-gyors-es-hatekony-eghajlatvedelmi-lepeseket-surget/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Fukusima-tanulsaga-milliok-elnek-tovabbra-is-egy-atomkatasztrofa-fenyegeteseben/':('Sajtóközlemény','Klíma & Energia','Atomenergia','Egészség','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Fukusima-ket-ev-utan-is-kilatastalan-a-tulelk-sorsa/':('Sajtóközlemény','Klíma & Energia','Atomenergia','Egészség','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Fukusima-5-Csernobil-30-atom-helyett-forduljunk-a-megujulok-fele/':('Sajtóközlemény','Klíma & Energia','Atomenergia','Megújulók','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Fuggetlen-e-az-Orszagos-Atomenergia-Hivatal-Paks-II-tl/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Fotoriporter-is-a-megvadoltak-kozt-a-Greenpeace-akcioban/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','Béke','Sarkvidék','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Forradalmi-meregmentesites-az-outdoor-szektorban/':('Sajtóközlemény','Ember & Társadalom','Szennyezés','Egészség','Fogyasztás','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Foldrengesveszelyes-teruletre-epulne-Paks-II-Fuggetlen-szakerti-vizsgalatot-es-a-munkalatok-azonnali-leallitasat-koveteli-a-Greenpeace-Magyarorszag/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Foldarveresek-Fejer-megyeben-csak-a-teruletek-20-at-nyertek-helyiek/':('Sajtóközlemény','Ember & Társadalom','ÖkológiaiGazdálkodás','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Fokozodik-a-kishantosi-botrany-a-Greenpeace-szerint/':('Sajtóközlemény','Ember & Társadalom','ÖkológiaiGazdálkodás','Béke','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Fertozo-veszelyes-hulladek-omlik-a-Szamosba/':('Sajtóközlemény','Ember & Társadalom','Szennyezés','Víz','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Felfuggesztettek-az-allam-14-millio-forintos-karteritesi-keresetet-Kishantos-es-a-Greenpeace-ellen/':('Sajtóközlemény','Ember & Társadalom','ÖkológiaiGazdálkodás','Béke','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Feladatok-Parizs-utan/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Feher-foltok-az-Europai-Elelmiszer-biztonsagi-Hivatal-mehekkel-es-mas-beporzokkal-kapcsolatos-kockazatelemzeseiben/':('Sajtóközlemény','Természet & Környezet','Élővilág','Méhek','Szennyezés','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/EU-klimakonferencia-megujulo-ervel-vagy-maszatolgatva-/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','Megújulók','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Engedjuk-be-a-napenergiat-a-magyar-otthonokba/':('Sajtóközlemény','Klíma & Energia','Megújulók','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Energiafuggseget-vagy-szabadsagot/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Energiaforradalmat-Magyarorszagon-is/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','Megújulók','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Emlekezzunk-a-nagybanyai-katasztrofara--nem-kell-cianidos-aranybanya-Romanianak-sem/':('Sajtóközlemény','Természet & Környezet','Szennyezés','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Elmult-a-birtokhaboritas-veszelye-Kishantoson-most-a-birosagon-a-dontes-sora/':('Sajtóközlemény','Ember & Társadalom','ÖkológiaiGazdálkodás','Béke','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Ellentmondasos-iteletek-a-kishantosi-birtokvedelmi-perekben/':('Sajtóközlemény','Ember & Társadalom','ÖkológiaiGazdálkodás','Béke','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Ellenrizetlen-novenyved-szerek-a-hazai-vizekben/':('Sajtóközlemény','Természet & Környezet','Szennyezés','Élővilág','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Elharcosok-es-sereghajtok-az-elektronikai-kutyuk-zolduleseben/':('Sajtóközlemény','Ember & Társadalom','Fogyasztás','Szennyezés','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Elhalasztottak-az-EUKanada-csucstalalkozot--itt-az-ideje-hogy-a-magyar-kormany-erdemi-tarsadalmi-vitat-kezdemenyezzen-a-CETA-rol/':('Sajtóközlemény','Ember & Társadalom','Fogyasztás','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Elhagyatott-veszelyes-hulladekok-Kiskunhalas-tersegeben-katasztrofalis-allapotban/':('Sajtóközlemény','Természet & Környezet','Szennyezés','MérgezettÖrökségünk','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Egyre-tobb-EU-tagorszag-ellenzi-a-rakkeltessel-gyanusitott-glifozat-hasznalatat/':('Sajtóközlemény','Természet & Környezet','Szennyezés','ÖkológiaiGazdálkodás','MérgezettÖrökségünk','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Egy-jegesmedve-a-Shell-szekhaznal-tuntet/':('Sajtóközlemény','Klíma & Energia','Sarkvidék','Klímavédelem','Élővilág','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/efovi-energiaunioja-a-Greenpeace-reakcioja/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','Atomenergia','Fosszilis','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Eddig-2-uj-nyertes-nem-kapott-3-kapott-els-fokon-birtokvedelmet-Kishantoson/':('Sajtóközlemény','Természet & Környezet','ÖkológiaiGazdálkodás','Béke','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Divatcegek-a-merlegen-divatdiktatorok-zoldrefestk-es-sereghajtok/':('Sajtóközlemény','Ember & Társadalom','Fogyasztás','Szennyezés','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/derogacio/':('Sajtóközlemény','Természet & Környezet','Szennyezés','Élővilág','Méhek','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Csipnek-a-mehek-a-minisztert-ha-vedene-ket/':('Sajtóközlemény','Természet & Környezet','Élővilág','Méhek','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Csernobil-30-eve-tortent-es-meg-tobb-tizezer-evig-tart/':('Sajtóközlemény','Klíma & Energia','Atomenergia','Egészség','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Csernobil-28--Greenpeace-demonstracio-kepekkel/':('Sajtóközlemény','Klíma & Energia','Atomenergia','Egészség','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Civilek-szazai-vonultak-ma-ki-tiltakozasul-a-varsoi-klimacsucsrol/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Civilek-nelkul-nem-megy-Magyarorszagnak-szuksege-van-rank/':('Sajtóközlemény','Ember & Társadalom','Béke','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Civilek-es-meheszek-jogi-uton-vedik-meg-a-mehgyilkos-vegyszerek-unios-korlatozasat-a-Syngenta-es-a-Bayer-ellen2/':('Sajtóközlemény','Természet & Környezet','Méhek','Élővilág','Szennyezés','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Civilek-a-ttip-targyalasi-mandatum-visszavonasat-kerik-Orban-Viktortol/':('Sajtóközlemény','Ember & Társadalom','Fogyasztás','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Civilek_az_Okotars_mellett/':('Sajtóközlemény','Ember & Társadalom','Béke','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Civil-szovetseg-alakult-a-romai-parti-mobilgatrol-szolo-nepszavazas-tamogatasara/':('Sajtóközlemény','Ember & Társadalom','Zöldterület','Élővilág','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Civil-allasfoglalas-az-allami-foldek-eladasarol-szolo-nepszavazasi-kezdemenyezesrl/':('Sajtóközlemény','Ember & Társadalom','ÖkológiaiGazdálkodás','Béke','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Burberry-A-meregtelenites-nemcsak-egy-mulo-divat/':('Sajtóközlemény','Ember & Társadalom','Fogyasztás','Szennyezés','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Bulgariaban-mar-letettek-az-uj-atomermrl/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Budapesti-Vegyimvek--a-Greenpeace-harompontos-intezkedesi-javaslata/':('Sajtóközlemény','Természet & Környezet','Szennyezés','Egészség','MérgezettÖrökségünk','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Brusszelbe-viszi-az-almasfuziti-tarozok-ugyet-a-Greenpeace/':('Sajtóközlemény','Természet & Környezet','Szennyezés','Egészség','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Bokaig-PET-palackokban-a-Tisza-parton/':('Sajtóközlemény','Természet & Környezet','StopMűanyag','Szennyezés','Fogyasztás','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Bnosok-es-szentek-a-Greenpeace-13-europai-varos-legszennyezettseget-pontozta/':('Sajtóközlemény','Természet & Környezet','Levegő','Szennyezés','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Biztonsagos-jovt-a-napenergias-kisermveknek/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','Megújulók','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Birosaghoz-fordul-a-Greenpeace-es-az-Energiaklub-mert-Paks-II-a-lakossagot-es-a-kornyezetet-is-veszelyeztetheti/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Bioeteleket-az-ovodai-iskolai-etkeztetesbe/':('Sajtóközlemény','Ember & Társadalom','Étkezés','ÖkológiaiGazdálkodás','Fogyasztás','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Bevetesen-a-Greenpeace-Kishantosert/':('Sajtóközlemény','Természet & Környezet','ÖkológiaiGazdálkodás','Béke','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Barbar-pusztitas-es-erdemonstracio-Kishantoson/':('Sajtóközlemény','Természet & Környezet','ÖkológiaiGazdálkodás','Béke','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Azonnal-zarjak-be-az-almasfuziti-veszelyeshulladek-lerakot--koveteli-a-Greenpeace/':('Sajtóközlemény','Természet & Környezet','Szennyezés','Egészség','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Azonnal-allitsak-le-Paks-II-t--Reakcio-a-ma-kiszivargott-dokumentumokra/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Az-orosz-parlament-amnesztiat-szavazott-a-Greenpeace-aktivistaknak/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','Sarkvidék','Béke','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Az-orosz-hatosagok-a-sarkvideki-harmincak-fogva-tartasanak-harom-honapos-meghosszabbitasat-kerik/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','Sarkvidék','Béke','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Az-orosz-elnok-szerint-sem-kalozok-a-Greenpeace-aktivistai/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','Sarkvidék','Fosszilis','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Az-NFA-a-Greenpeace-szel-akarja-kifizettetni-a-kishantosi-koltsegeit/':('Sajtóközlemény','Ember & Társadalom','ÖkológiaiGazdálkodás','Béke','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Az-Europai-Unio-Birosaga-torvenysertnek-itelte-a-fakivagasokat-a-lengyelorszagi-Biaowiea-erdben/':('Sajtóközlemény','Természet & Környezet','Élővilág','Erdő','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Az-Europai-Bizottsag-vedene-a-meheket-de-a-dontes-a-tagallamok-kezeben-van/':('Sajtóközlemény','Természet & Környezet','Élővilág','Méhek','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Az-Europai-Bizottsag-ket-het-alatt-masodszor-sem-tudott-donteni-a-rakkeltessel-gyanusitott-glifozat-ujraengedelyezeserl/':('Sajtóközlemény','Ember & Társadalom','Egészség','Szennyezés','ÖkológiaiGazdálkodás','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Az-Europai-Birosaghoz-fordul-Kishantos-a-magyar-videk-igazaert/':('Sajtóközlemény','Ember & Társadalom','ÖkológiaiGazdálkodás','Béke','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Az-EU-vezeti-behuztak-a-kezifeket-a-megujulokra/':('Sajtóközlemény','Klíma & Energia','Megújulók','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Az-Energiaklub-es-a-Greenpeace-megfellebbezi-Paks-II-kornyezetvedelmi-engedelyet/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Az-Energiaklub-az-EMLA-es-a-Greenpeace-felfuggesztik-reszveteluket-az-atomenergia-kerdeseivel-foglalkozo-nemzeti-kerekasztalban/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Az-emberiseg-a-vilag-legeldugottabb-helyeit-is-beszennyezte-a-veszelyes-PFC-kkel/':('Sajtóközlemény','Természet & Környezet','Szennyezés','Egészség','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Az-elvilag-vedelme-erdekeben-vissza-kell-szoritanunk-a-hus--es-tejtermekfogyasztasunkat/':('Sajtóközlemény','Természet & Környezet','Étkezés','Klímavédelem','Élővilág','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Az-elkeszites-nelkuli-faatultetes-valojaban-egy-nagyon-draga-fakivagas/':('Sajtóközlemény','Természet & Környezet','Élővilág','Egészség','Zöldterület','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Az-Apple-piszkos-energiaval-uzemelteti-az-iCloudot/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','Fosszilis','','article','Migrate'),
            #part4
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Az-Apple-az-Amazon-es-a-Microsoft-piszkos-energiaval-uzemeltetik-adatkozpontjaikat/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','Fosszilis','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Az-allampolgarok-is-beleszolhatnak--mondta-ki-az-Europai-Birosag-a-TTIP-es-CETA-kapcsan/':('Sajtóközlemény','Ember & Társadalom','Fogyasztás','','','article','Migrate'),
            #'http://www.greenpeace.org/hungary/hu/sajtokozpont/Az-Adidas-a-valodi-meregtelenites-utjara-lepett/':('Sajtóközlemény','Ember & Társadalom','Fogyasztás','Szennyezés','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Aranyat-as-a-Greenpeace-a-romaniai-parlament-udvaran-a-verespataki-beruhazas-ellen-tuntetve/':('Sajtóközlemény','Természet & Környezet','Szennyezés','Fogyasztás','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Almasfuzit-hiaba-magasak-a-gatak-ha-szivarog-a-tarozo/':('Sajtóközlemény','Természet & Környezet','Szennyezés','Egészség','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Almasfuzit-ervenyes-engedely-nelkul-kezel-a-TKV-veszelyes-hulladekot/':('Sajtóközlemény','Természet & Környezet','Szennyezés','Egészség','','article','Migrate'),
            #'http://www.greenpeace.org/hungary/hu/sajtokozpont/Almasfuzit-A-Tatai-Zrt-a-Greenpeace-hazugsaganak-titulalja-az-MTA-nem-cafolt-megallapitasait/':('Sajtóközlemény','Természet & Környezet','Szennyezés','Egészség','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Allasfoglalas-egy-GMO-elterjesztes-kapcsan/':('Sajtóközlemény','Természet & Környezet','ÖkológiaiGazdálkodás','Egészség','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/allasfoglalas-allami-foldeladas/':('Sajtóközlemény','Ember & Társadalom','ÖkológiaiGazdálkodás','','','article','Migrate'),
            #'http://www.greenpeace.org/hungary/hu/sajtokozpont/Allasfoglalas-a-vilag-els-nyilvanos-parkjaban-a-Varosligetben-megkezdett-fakivagasokrol/':('Sajtóközlemény','Természet & Környezet','Zöldterület','Élővilág','Egészség','article','Migrate'),
            #'http://www.greenpeace.org/hungary/hu/sajtokozpont/Allampolgarok-termelhetnek-meg-az-EU-aramszuksegletenek-45-at-2050-re/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','Megújulók','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Adjukosszehu-legyel-Fejs-Eva-regenyhse/':('Sajtóközlemény','Ember & Társadalom','Greenpeace','Szennyezés','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Ader-Janos-koztarsasagi-elnok-fenntartas-nelkul-atengedte-a-Paksi-paktumot/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/Adatkeres-a-Liget-Projekttel-kapcsolatos-faatultetesekrl--nyilt-level/':('Sajtóközlemény','Ember & Társadalom','Zöldterület','','','article','Migrate'),
            #'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-zold-szervezet-kifogasolja-hogy-most-is-elkendzes-es-elhallgatas-ovezi-az-ujabb-paksi-zavart/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-valodi-vezetk-a-megujulokat-valasztjak1/':('Sajtóközlemény','Klíma & Energia','Megújulók','Atomenergia','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-valodi-vezetk-a-megujulokat-valasztjak/':('Sajtóközlemény','Klíma & Energia','Megújulók','Atomenergia','Klímavédelem','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-tudomany-es-az-Europai-Parlament-is-a-mehgyilkos-vegyszerek-ellen-van/':('Sajtóközlemény','Természet & Környezet','Élővilág','Méhek','ÖkológiaiGazdálkodás','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-torveny-es-az-igazsag-Kishantos-oldalan/':('Sajtóközlemény','Ember & Társadalom','ÖkológiaiGazdálkodás','Béke','','article','Migrate'),
            #'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-tajepitesz-palyazok-7-es-sorszamu-tervlapjai-bizonyitjak-fel-lehet-ujitani-a-Ligetet-uj-epuletek-nelkul-is/':('Sajtóközlemény','Természet & Környezet','Zöldterület','Élővilág','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-sulyos-hazai-legszennyezettseg-ugye-mar-az-Europai-Birosagon/':('Sajtóközlemény','Ember & Társadalom','Levegő','Szennyezés','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Shell-visszavonul-a-Sarkvidekrl/':('Sajtóközlemény','Klíma & Energia','Sarkvidék','Klímavédelem','Élővilág','article','Migrate'),
            #'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Samsung-elkotelezi-magat-a-100-megujulo-energia-mellett-a-vilagmeret-tarsadalmi-nyomasgyakorlas-hatasara/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Roszatom-kockazatai/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-romaiak-amfiteatrumot-mi-atomhulladekot-hagyunk-hatra/':('Sajtóközlemény','Klíma & Energia','Atomenergia','Klímavédelem','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Romai-partot-ved-civil-csoportok-allasfoglalasa/':('Sajtóközlemény','Természet & Környezet','Zöldterület','Élővilág','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Pecsi-Torvenyszek-elutasitotta-hogy-Paks-II-nyitott-kerdeseirl-az-igazsagszolgaltatas-eltt-folyhasson-erdemi-vita/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-paksi-bvites-elszenvedte-az-els-komoly-csapast-es-meg-ennel-is-komolyabbakat-kaphat/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-paksi-atomerm-rejtett-koltsegei/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            #'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Paks-II-t-epit-Roszatom-is-szerepel-a-Greenpeace-davosi-Vilaggazdasagi-Forumra-keszult-feketelistajan/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-nuklearis-kockazatok-uj-korszakaban/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-nepszavazas-megoldast-hozhat-a-Romai-part-arvizvedelmere/':('Sajtóközlemény','Természet & Környezet','Zöldterület','Élővilág','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-neonikotinoid-novenyved-szerek-nemcsak-a-hazi-meheket-hanem-a-vadvilagot-is-veszelyeztetik/':('Sajtóközlemény','Természet & Környezet','Méhek','Élővilág','ÖkológiaiGazdálkodás','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Nemzeti-Foldalapkezel-Szervezet-NFA-kepviselje-felrugna-a-Kishantost-vedket/':('Sajtóközlemény','Ember & Társadalom','ÖkológiaiGazdálkodás','Béke','','article','Migrate'),
            #'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-nagy-gyermekruhateszt/':('Sajtóközlemény','Ember & Társadalom','Egészség','Fogyasztás','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-nagy-divatmarkak-ruhainak-mosasakor-mergezzuk-a-vizeket/':('Sajtóközlemény','Ember & Társadalom','Egészség','Fogyasztás','Víz','article','Migrate'),
            #'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-meheket-vedje-Magyarorszag-ne-a-veszelyes-vegyszereket/':('Sajtóközlemény','Természet & Környezet','Méhek','Élővilág','ÖkológiaiGazdálkodás','article','Migrate'),
            #'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-magyaroknak-tovabbra-sem-erdeke-Paks-II-megepitese/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-magyarok-tulnyomo-tobbsege-ellenzi-Paks-II-t-fkent-a-projekt-veszelyessege-miatt/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-magyarok-ketharmada-tiszta-energiat-akar-orosz-energiafuggseg-helyett/':('Sajtóközlemény','Klíma & Energia','Atomenergia','Megújulók','','article','Migrate'),
            #'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-magyarok-85--a-bizik-a-hazai-elelmiszerekben/':('Sajtóközlemény','Ember & Társadalom','Egészség','Étkezés','Fogyasztás','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Magyar-Tudomanyos-Akademia-szerint-is-sulyos-veszelyt-jelentenek-az-almasufuzitoi-tarozok/':('Sajtóközlemény','Ember & Társadalom','Szennyezés','','','article','Migrate'),
            #'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-lignit-elleni-tuntetes-uj-hatarokat-feszeget/':('Sajtóközlemény','Klíma & Energia','Fosszilis','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Lidl-is-meregteleniti-a-ruhatarat/':('Sajtóközlemény','Ember & Társadalom','Fogyasztás','Egészség','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Levis-beadta-a-derekat/':('Sajtóközlemény','Ember & Társadalom','Fogyasztás','Egészség','Szennyezés','article','Migrate'),
            #'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-labdarugo-vb-mocskos-titkai-karos-vegyszerek-a-sportruhakban/':('Sajtóközlemény','Ember & Társadalom','Fogyasztás','Egészség','Szennyezés','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Kuria-kimondta-torvenytelen-volt-az-NFA-eljarasa-Kishantos-ugyeben/':('Sajtóközlemény','Ember & Társadalom','ÖkológiaiGazdálkodás','Béke','','article','Migrate'),
            #'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-klimavaltozasbol-nem-lehet-kilepni-Trump-mai-dontesevel-az-USA-globalis-vezet-poziciojat-kockaztatja/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Kishantosi-Videkfejlesztesi-Kozpont-pert-inditott-a-Nemzeti-Foldalapkezel-Szervezet-dontese-ellen/':('Sajtóközlemény','Ember & Társadalom','ÖkológiaiGazdálkodás','Béke','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-hatarerteket-sokszorosan-atlep-rakkelt-anyagok-a-talajvizben-Gyomrn/':('Sajtóközlemény','Természet & Környezet','Szennyezés','Egészség','MérgezettÖrökségünk','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Greenpeace-ujabb-unios-szabadkereskedelmi-egyezmeny-titkos-dokumentumait-szivarogtatta-ki/':('Sajtóközlemény','Ember & Társadalom','Fogyasztás','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Greenpeace-teljes-atlathatosagot-kovetel-Kishantos-ugyeben/':('Sajtóközlemény','Ember & Társadalom','ÖkológiaiGazdálkodás','Béke','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Greenpeace-reakcioja-a-2016-aprilis-19-en-az-indexhu-n-megjelent-Panikot-kelt-a-Greenpeace-Fazekasek-szerint-cim-cikkre/':('Sajtóközlemény','Természet & Környezet','Élővilág','Méhek','ÖkológiaiGazdálkodás','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Greenpeace-Paks-II-ellen-tiltakozik-az-osztrak-es-magyar-kormanyfk-talalkozojan-Becsben/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Greenpeace-Orban-Viktorhoz-fordul-Kishantos-ugyeben/':('Sajtóközlemény','Ember & Társadalom','ÖkológiaiGazdálkodás','Béke','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Greenpeace-nyilatkozata-a-2016-julius-6-i-varosligeti-esemenyek-kapcsan/':('Sajtóközlemény','Természet & Környezet','Zöldterület','Élővilág','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Greenpeace-nek-bizonyiteka-van-a-kishantosi-uj-berlk-vegyszerhasznalatarol/':('Sajtóközlemény','Ember & Társadalom','ÖkológiaiGazdálkodás','Béke','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Greenpeace-mintavetelezessel-tisztazna-az-azbeszt-helyzetet-a-Ligetben/':('Sajtóközlemény','Ember & Társadalom','Zöldterület','Egészség','Élővilág','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Greenpeace-Magyarorszagon-is-cselekvesre-szolitja-fel-a-donteshozokat-a-klimavaltozas-megfekezese-erdekeben/':('Sajtóközlemény','Klíma & Energia','Klímavédelem','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Greenpeace-kijott-a-Liget-Park-Forumrol/':('Sajtóközlemény','Ember & Társadalom','Zöldterület','Egészség','Élővilág','article','Migrate'),
            #part5
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Greenpeace-htlen-kezeles-miatt-perel-Kishantos-vedelmeben/':('Sajtóközlemény','Ember & Társadalom','ÖkológiaiGazdálkodás','Béke','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Greenpeace-Fukusima---Arnyekvilag-mondd-te-mit-valasztanal-cim-kiallitasa-bemutatja-az-atomenergia-valodi-arat/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            #'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Greenpeace-es-az-Energiaklub-birosagon-tamadta-meg-Paks-II-kornyezetvedelmi-engedelyet-az-erm-a-lakossagot-es-a-kornyezetet-is-veszelyeztetheti/':('Sajtóközlemény','Klíma & Energia','Atomenergia','Egészség','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Greenpeace-es-a-meheszek-bejutottak-a-mehgyilkos-vegyszereket-gyarto-Syngenta-kozgylesere/':('Sajtóközlemény','Természet & Környezet','ÖkológiaiGazdálkodás','Méhek','Élővilág','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Greenpeace-es-a-Ligetvedk-nem-vesznek-reszt-a-Liget-Park-Forumokon-mert-a-forumokon-nincs-lehetseg-a-Varosliget-megujitasanak-koncepciojarol-egyeztetni/':('Sajtóközlemény','Természet & Környezet','Zöldterület','Élővilág','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Greenpeace-eliteli-a-roman-kormany-verespataki-beruhazast-elsegit-donteset/':('Sajtóközlemény','Természet & Környezet','Szennyezés','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Greenpeace-az-okostelefonok-ujrahasznositasat-koveteli-a-Mobil-Vilagkongresszuson/':('Sajtóközlemény','Ember & Társadalom','Fogyasztás','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Greenpeace-aktivistak-szabadon-engedeseert--tuntettek-ma-delutan-a-vilag-50-orszagaban/':('Sajtóközlemény','Ember & Társadalom','Béke','Sarkvidék','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Greenpeace-7-pontos-megoldasi-javaslata-a-vilag-elelmezesi-valsagara/':('Sajtóközlemény','Ember & Társadalom','Étkezés','ÖkológiaiGazdálkodás','Fogyasztás','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-genmodositast-elutasito-orszagok-osszefogasa-es-a-transzatlanti-szabadkereskedelmi-egyezmenyek/':('Sajtóközlemény','Ember & Társadalom','ÖkológiaiGazdálkodás','Fogyasztás','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Gazprom-olajfuro-platformjan-a-Greenpeace-igazgatoja/':('Sajtóközlemény','Klíma & Energia','Fosszilis','Klímavédelem','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Fvarosi-Kozgyles-semmibe-veszi-az-emberek-akaratat/':('Sajtóközlemény','Természet & Környezet','Zöldterület','Egészség','Élővilág','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-Fold-napjahoz-kozeledve-tobb-mint-1-millioan-kovetelik-hogy-az-oriasvallalatok-csokkentsek-az-eldobhato-manyagok-hasznalatat/':('Sajtóközlemény','Természet & Környezet','StopMűanyag','Fogyasztás','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-dontes-megszuletett-a-vita-most-kezddik/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-civilek-csalodottak-mert-a-kormany-alairna-a-CETA-t/':('Sajtóközlemény','Ember & Társadalom','Fogyasztás','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-budapestiek-termeszetrombolas-nelkul-akarnak-arvizvedelmet-a-Romai-parton/':('Sajtóközlemény','Természet & Környezet','Zöldterület','Egészség','Élővilág','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/A-budapestiek-72-a-nem-a-Varosligetben-hanem-inkabb-a-Nyugati-palyaudvar-mogott-szeretne-muzeumnegyedet/':('Sajtóközlemény','Természet & Környezet','Zöldterület','Egészség','Élővilág','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/80-energiafuggseg/':('Sajtóközlemény','Klíma & Energia','Megújulók','Atomenergia','Fosszilis','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/75-kornyezet--es-termeszetved-civil-szervezet-allasfoglalasa-a-kulfoldrl-tamogatott-szervezetek-atlathatosagarol-szolo-torvenyjavaslatrol/':('Sajtóközlemény','Ember & Társadalom','Béke','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/5-evvel-a-kolontari-vorosiszap-katasztrofa-utan-mi-kell-a-jovbeni-balesetek-elkerulesehez/':('Sajtóközlemény','Ember & Társadalom','Szennyezés','','','article','Migrate'),
            #part6
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/32-evvel-Csernobil-utan-jon-az-ujabb-rulet-az-uszo-atomerm/':('Sajtóközlemény','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/sajtokozpont/3-mehgyilkos-rovarolo-szer-korlatozasa-lepett-eletbe-az-Unioban/':('Sajtóközlemény','Természet & Környezet','Méhek','Élővilág','ÖkológiaiGazdálkodás','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/torokbalint/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/tiszapalkonya/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/szormegyar/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/szentendre/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/soroksar/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/pevdi/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/nitrokemia/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/neszmely/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/naplas/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/motim/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/lkm/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/koporc/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/kiskunhalas/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/kenutca/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/hortobagy/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/gazgyar/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/fenyestanya/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/feltaratlanszennyezesek/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/emv/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/dunaferr/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/digep/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/csery/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            #'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/bvm/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/bucka-to/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/borsodchem/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/berva/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/bakonymuvek/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/Almasfuzito/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/alkaloida/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/ajka/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/abasar/':('Sajtóközlemény','','MérgezettÖrökségünk','','','article','Migrate'),
            #'http://www.greenpeace.org/hungary/hu/mergezett-oroksegunk/':('Sajtóközlemény','Természet & Környezet','MérgezettÖrökségünk','Szennyezés','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Kisokos-a-neonikotinoidok-hatasairol-meheszek-szamara/':('Kiadvány','Ember & Társadalom','Élővilág','Méhek','ÖkológiaiGazdálkodás','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Kis-mese-a-szekrenyedben-lakozo-szornyekrl/':('Kiadvány','Ember & Társadalom','Szennyezés','Fogyasztás','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Halozatok-harca-2011/':('Kiadvány','Klíma & Energia','Klímavédelem','Atomenergia','Megújulók','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Glifozat-tanulmany/':('Kiadvány','Természet & Környezet','ÖkológiaiGazdálkodás','Szennyezés','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Fuszeres-viragos-biokert/':('Kiadvány','Természet & Környezet','ÖkológiaiGazdálkodás','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Fukusima-tanulsagai/':('Kiadvány','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Felpaprikazva--Miert-kell-elutasitani-a-Syngenta-paprikaszabadalmat/':('Kiadvány','Természet & Környezet','ÖkológiaiGazdálkodás','Egészség','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Europa-novenyvedoszer-fuggsege/':('Kiadvány','Természet & Környezet','ÖkológiaiGazdálkodás','Szennyezés','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Divatos-es-toxikus/':('Kiadvány','Ember & Társadalom','ÖkológiaiGazdálkodás','Fogyasztás','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Csepego-mereg/':('Kiadvány','Természet & Környezet','ÖkológiaiGazdálkodás','Egészség','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Bio--Nemcsak-etet-taplal-is/':('Kiadvány','Természet & Környezet','ÖkológiaiGazdálkodás','Étkezés','Fogyasztás','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Az-okologiai-gazdalkodas-7-alapelve/':('Kiadvány','Természet & Környezet','ÖkológiaiGazdálkodás','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/Az-eloreged-atomermvek-elettartam-hosszabbitasa/':('Kiadvány','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/A-Roszatom-kockazatai/':('Kiadvány','Klíma & Energia','Atomenergia','','','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/A-novenyved-szerek-hatasai-az-emberi-egeszsegre/':('Kiadvány','Ember & Társadalom','ÖkológiaiGazdálkodás','Fogyasztás','Egészség','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/A-neonikotinoid-novenyved-szerek-veszelyei-a-kornyezetunkre/':('Kiadvány','Ember & Társadalom','ÖkológiaiGazdálkodás','Fogyasztás','Élővilág','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/A-mehek-terhe/':('Kiadvány','Természet & Környezet','Élővilág','Méhek','ÖkológiaiGazdálkodás','article','Migrate'),
            'http://www.greenpeace.org/hungary/hu/hirek/publikaciok/A-Greenpeace-ertekelese-Paks-II-kornyezeti-hatastanulmanyarol/':('Kiadvány','Klíma & Energia','Atomenergia','','','article','Migrate'),
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
            #f1=open('/tmp/debug.txt', 'a+')
            if ("/emailimages/" in image_file):
                # PHP webservice script url.
                api_url = "http://127.0.0.1/ocr-api-test/email_img_to_text.php"
                end_point_url = api_url + "?url=" + image_file
                emailid = urllib2.urlopen(end_point_url).read(1000)
                # Search replace the \n, <BR>, spaces from email id.
                emailid = emailid.replace('\n', '')
                emailid = emailid.replace('<br>', '')
                emailid = emailid.replace('<BR>', '')
                emailid = emailid.replace(' ', '')
                emailid = emailid.replace('qreenpeace', 'greenpeace')
                emailid = emailid.replace('aqreenpeace', '@greenpeace')
                emailid = emailid.replace('@qreenpeace', '@greenpeace')
                emailid = emailid.replace('agreenpeace', '@greenpeace')
                #f1.write(emailid)
                delete_images.append(image_file)
                # Remove the email images from Post body and replace it with email text.
                body_text = re.sub(
                    '<img[a-zA-Z0-9="\s\_]*src=\"' + image_file + '\"[a-zA-Z0-9="\s]*>',
                    emailid, body_text)
            #f1.close()

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
            'author': 'Greenpeace Magyarország',
            'author_username': 'greenpeacehu',
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
                body_text = '<div class="leader">' + lead_text + '</div>' + body_text + response.xpath(' //*[@id="content"]/div[4]/div/div[2]/p').extract_first()

        subtitle = extract_with_css('div.article h2 span::text')
        if subtitle:
            body_text = '<h2>' + subtitle + '</h2><br />' + body_text

        # Get the thumbnail of the post as requested.
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
            #f1=open('/tmp/debug.txt', 'a+')
            if ("/emailimages/" in image_file):
                api_url = "http://127.0.0.1/ocr-api-test/email_img_to_text.php"
                end_point_url = api_url+"?url="+image_file
                emailid = urllib2.urlopen(end_point_url).read(1000)
                # Search replace the \n, <BR>, spaces from email id.
                emailid = emailid.replace('\n', '')
                emailid = emailid.replace('<br>', '')
                emailid = emailid.replace('<BR>', '')
                emailid = emailid.replace(' ', '')
                emailid = emailid.replace('qreenpeace', 'greenpeace')
                emailid = emailid.replace('aqreenpeace', '@greenpeace')
                emailid = emailid.replace('@qreenpeace', '@greenpeace')
                emailid = emailid.replace('agreenpeace', '@greenpeace')
                #f1.write(emailid)
                delete_images.append(image_file)
                # Remove the email images from Post body and replace it with email text.
                body_text = re.sub(
                    '<img[a-zA-Z0-9="\s\_]*src=\"'+image_file+'\"[a-zA-Z0-9="\s]*>',
                    emailid, body_text)
            #f1.close()

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
            'author': 'Greenpeace Magyarország',
            'author_username': 'greenpeacehu',
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
            'thumbnail': thumbnail,
        }

    def filter_post_content(self, post_data):
        # Filter the youtube video and add embed shortcode instead.
        post_data = re.sub(
            '\<object[width\=\"height0-9\s]*data\=\"([https]*\:\/\/www.youtube.com[a-zA-Z0-9\/\=\-\?\_]*)\"[\=\"a-zA-Z\/\-\s0-9]*\>[\\n\s]*(.*)[\\n\s]*\<\/object\>',
            '[embed]\g<1>[/embed]', post_data)

        return post_data

    def filter_month_name(self, month_name):

        month_hu_en = {
            'január': 'January',
            'február': 'February',
            'március': 'March',
            'április': 'April',
            'május': 'May',
            'június': 'June',
            'július': 'July',
            'augusztus': 'August',
            'szeptember': 'September',
            'október': 'October',
            'november': 'November',
            'december': 'December',
        }

        # Replace the hungarian month name with english month name.
        for hu_month, en_month in month_hu_en.iteritems():
            month_name = month_name.replace(hu_month, en_month)

        return month_name;

    def csv_writer(self, data, path):
        # Write data to a CSV file path
        with open(path, "a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(data)
