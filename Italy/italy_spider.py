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
        'FEED_URI': 'gpit_staging_v2_B6.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    __connector_csv_filename = "connector_v2_final.csv"
    __connector_csv_log_file = "connector_csv_log_v2"

    def start_requests(self):
        # v1
        start_urls = {
            'http://www.greenpeace.org/italy/it/Clima-Greenpeace-Dieci-anni-per-dire-addio-alle-auto-a-benzina-gasolio-e-alle-ibride-convenzionali/':('Comunicato Stampa','Denuncia','Petrolio&Gas','Clima','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/Glifosato-bene-il-no-dellItalia-diminuisce-il-numero-dei-paesi-a-favore-del-rinnovo/':('Comunicato Stampa','Denuncia','Agricoltura','Inquinamento','Biodiversità','article','Migrate'),
            'http://www.greenpeace.org/italy/it/La-Rainbow-Warrior-a-Fukushima-per-le-analisi-della-radioattivita-delle-acque-/':('Comunicato Stampa','Denuncia','Energia','Inchieste','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/--I-PFAS-e-altri-PFC-mettono-a-rischio-la-salute-/':('Storia','Denuncia','Inquinamento','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/-In-azione-Affondate-il-CETA-non-la-giustizia/':('Storia','Denuncia','Agricoltura','Azioni','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Abbiamo-le-prove-anche-il-nostro-mare-e-una-zuppa-di-plastica/':('Storia','Denuncia','Inquinamento','Mare','Inchieste','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/3-buoni-motivi-per-cui-abbiamo-bisogno-di-san/blog/57397/':('Storia','Proteggi','Mare','','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/6-ragioni-per-cui-lindustria-dellauto-deve-im/blog/60214/':('Storia','Denuncia','Inquinamento','Petrolio&Gas','Clima','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/al-fianco-dei-munduruku-per-proteggere-il-cuo/blog/56777/':('Storia','Proteggi','Foreste','Partecipazione','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/comunicati/Antartide-spedizione-di-Greenpeace-in-Oceano-Antartico-rivela-quattro-Ecosistemi-Marini-Vulnerabili-sul-fondo-del-mare/':('Comunicato Stampa','Proteggi','Mare','Biodiversità','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/comunicati/blocco-ingresso-Ministero-dei-Trasporti/':('Comunicato Stampa','Scegli','Partecipazione','Greenpeace','Azioni','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/comunicati/Casa-Surace-e-Greenpeace-insieme-contro-la-plastica-usa-e-getta/':('Comunicato Stampa','Scegli','Consumi','Inquinamento','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/100-rinnovabili-un-nuovo-futuro-per-le-piccole-isole/':('Rapporto','Denuncia','Energia','Rinnovabili','Clima','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/A-come-ape/':('Rapporto','Denuncia','Agricoltura','Biodiversità','Cibo','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Acciughe-al-collasso-un-piccolo-pesce-in-grande-pericolo/':('Rapporto','Proteggi','Mare','Inchieste','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Olimpiadi-Roma-2024-la-lettera-delle-associazioni/':('Storia','Denuncia','Inquinamento','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/TTIP-leaks/':('Comunicato Stampa','Denuncia','Agricoltura','Inchieste','Cibo','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/Stop-diesel-a-Milano-Greenpeace-Scelta-coraggiosa-Sala-faccia-presto-e-con-determinazione/':('Comunicato Stampa','Denuncia','Inquinamento','Petrolio&Gas','','article','Migrate'),
        }

        #v2
        #### - duplicate
        start_urls = {
            ### P1
            'http://www.greenpeace.org/italy/it/ufficiostampa/comunicati/Giornata-per-eliminazione-totale-armi-nucleari-Greenpeace-chiede-a-Presidente-Camera-Fico-e-a-Vicepremier-Di-Maio-sostegno-a-ratifica-italiana-di-trattato-ONU/':('Comunicato Stampa','Scegli','','Partecipazione','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Plastic-Radar-i-risultati/':('Storia','Denuncia','Proteggi','Inquinamento','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/comunicati/Plastic-Radar-Greenpeace-la-plastica-monouso-di-San-Benedetto-Coca-Cola-e-Nestle-inquina-i-mari-italiani/':('Comunicato Stampa','Denuncia','Proteggi','Inquinamento','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Plastic-radar/':('Rapporto','Denuncia','Proteggi','Inquinamento','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Tempo-scaduto-per-le-auto-a-benzina-e-gasolio-/':('Storia','Denuncia','Proteggi','Petrolio&Gas','Clima','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/Clima-Greenpeace-Dieci-anni-per-dire-addio-alle-auto-a-benzina-gasolio-e-alle-ibride-convenzionali/':('Comunicato Stampa','Denuncia','Proteggi','Petrolio&Gas','Clima','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/E-ora-di-dire-addio-ai-motori-fossili/':('Rapporto','Denuncia','Proteggi','Petrolio&Gas','Clima','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/final-countdown-il-nuovo-rapporto-che-inchiod/blog/61889/':('Storia','Proteggi','Scegli','Foreste','Consumi','Biodiversità','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Il-Paradiso-puo-attendere-un-lascito-per-proteggere-il-Pianeta/':('Storia','Scegli','','Partecipazione','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/comunicati/Greenpeace-in-azione-a-New-York-in-apertura-negoziati-su-accordo-globale-per-tutela-degli-oceani-Necessaria-una-rete-di-santuari-marini/':('Comunicato Stampa','Proteggi','','Mare','Biodiversità','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Vittoria-Bloccato-lampliamento-delloleodotto-Trans-Mountain-in-Canada/':('Storia','Denuncia','Proteggi','Petrolio&Gas','Clima','Biodiversità','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/comunicati/Dimissioni-Hulot-Greenpeace-Scelta-coraggiosa-Macron-deve-smettere-di-dare-precedenza-a-interessi-multinazionali/':('Comunicato Stampa','Proteggi','','Clima','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/orche-mare-di-salish-petrolio/blog/61776/':('Storia','Proteggi','Proteggi','Petrolio&Gas','Biodiversità','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/hiroshima-premio-terra-pace/blog/61769/':('Storia','Denuncia','','Partecipazione','','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/comunicati/Indagine-di-Greenpeace-rivela-che-in-Italia-un-locale-plastic-free-e-gia-possibile/':('Comunicato Stampa','Denuncia','Scegli','Consumi','Inquinamento','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/comunicati/blocco-ingresso-Ministero-dei-Trasporti/':('Comunicato Stampa','Scegli','','Partecipazione','Azioni','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/comunicati/Casa-Surace-e-Greenpeace-insieme-contro-la-plastica-usa-e-getta/':('Comunicato Stampa','Scegli','','Consumi','Inquinamento','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/comunicati/Nuovo-inquinamento-in-Veneto-Greenpeace-chiede-a-magistratura-sequestro-di-Miteni-e-verifica-di-eventuali-responsabilita-di-funzionari-pubblici/':('Comunicato Stampa','Denuncia','','Inquinamento','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/Greenpeace-I-nuovi-OGM-non-possono-sottrarsi-alla-valutazione-del-rischio-e-alletichettatura-secondo-le-norme-Ue/':('Comunicato Stampa','Denuncia','Scegli','Agricoltura','Cibo','Biodiversità','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/comunicati/Antartide-spedizione-di-Greenpeace-in-Oceano-Antartico-rivela-quattro-Ecosistemi-Marini-Vulnerabili-sul-fondo-del-mare/':('Comunicato Stampa','Proteggi','','Mare','Biodiversità','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/comunicati/Greenpeace-Regione-Veneto-e-Miteni-rendano-pubblici-documenti-sul-caso-GenX/':('Comunicato Stampa','Denuncia','','Inquinamento','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/comunicati/Greenpeace-in-azione-in-Finlandia-durante-incontro-tra-Trump-e-Putin-Agire-subito-per-combattere-i-cambiamenti-climatici/':('Comunicato Stampa','Proteggi','','Azioni','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/comunicati/PFAS-Greenpeace-Regione-Veneto-spieghi-perche-ha-autorizzato-Miteni-a-trattamento-di-rifiuti-chimici-pericolosi-che-hanno-portato-a-contaminazione-da-GenX/':('Comunicato Stampa','Denuncia','','Inquinamento','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Sette-scomode-verita-sul-GenX/':('Rapporto','Denuncia','','Inquinamento','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/comunicati/Nuovo-report-di-Greenpeace-una-moda-pulita-e-gia-possibile-/':('Comunicato Stampa','Denuncia','Scegli','Inquinamento','Consumi','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/greenpeace-dalla-parte-dei-migranti-perch-vog/blog/61712/':('Storia','Scegli','','Partecipazione','','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/greenpeace-dalla-parte-dei-migranti-perch-vog/blog/61713/':('Storia','Scegli','','Partecipazione','','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Buone-notizie-per-i-pinguini/':('Storia','Proteggi','','Biodiversità','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/comunicati/GREENPEACE-LE-PIU-GRANDI-COMPAGNIE-DI-PESCA-AL-KRILL-SI-IMPEGNANO-A-TUTELARE-LOCEANO-ANTARTICO/':('Comunicato Stampa','Proteggi','','Biodiversità','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/comunicati/Pfas-Greenpeace-Sulle-negligenze-della-Regione-Veneto-intervenga-il-ministro-Costa/':('Comunicato Stampa','Denuncia','','Inquinamento','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/In-azione-Due-balene-in-fuga-dalla-plastica/':('Storia','Proteggi','Denuncia','Inquinamento','Mare','Azioni','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/comunicati/Greenpeace-in-azione-a-Roma-La-plastica-usa-e-getta-di-Coca-cola-San-benedetto-Ferrero-Nestle-Haribo-e-Unilever-inquina-i-mari-italiani/':('Comunicato Stampa','Proteggi','Denuncia','Inquinamento','Mare','Azioni','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Stessa-spiaggia-stessa-plastica/':('Rapporto','Proteggi','Denuncia','Inquinamento','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/E-tempo-di-lasciare-il-carbone-dove-sottoterra/':('Storia','Denuncia','Proteggi','Energia','Inquinamento','Clima','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/grazie-alla-voce-di-migliaia-di-persone-samsu/blog/61682/':('Storia','Scegli','','Energia','','Consumi','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/comunicati/Greenpeace-organizza-la-Plastic-Free-Week-eventi-in-16-citta-italiane/':('Comunicato Stampa','Proteggi','Denuncia','Mare','Inquinamento','Azioni','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/comunicati/PFAS-Greenpeace-Da-tempo-chiediamo-alla-Regione-Veneto-il-censimento-di-tutte-le-fonti-inquinanti/':('Comunicato Stampa','Denuncia','','Inquinamento','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/comunicati/Plastica---Greenpeace-Il-riciclo-non-salvera-i-mari-del-pianeta/':('Comunicato Stampa','Denuncia','Proteggi','Inquinamento','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Plastica-il-riciclo-non-basta/':('Rapporto','Denuncia','Proteggi','Inquinamento','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/comunicati/Microplastica-anche-in-pesci-e-invertebrati-lo-conferma-una-ricerca-GreenpeaceUNIVPMISMAR-CNR----/':('Comunicato Stampa','Denuncia','Proteggi','Inquinamento','Mare','Biodiversità','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Microplastica-in-pesci-e-invertebrati-lungo-la-costa-del-Tirreno/':('Rapporto','Denuncia','Proteggi','Inquinamento','Mare','Biodiversità','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Mobilita-sostenibile-Milano-prima-in-classifica-Palermo-ultima/':('Storia','Denuncia','Proteggi','Inquinamento','Salute','Clima','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/comunicati/Mobilita-sostenibile-Greenpeace-compara-Milano-Torino-Roma-e-Palermo-Milano-prima-classificata-ultima-Palermo/':('Comunicato Stampa','Denuncia','Proteggi','Inquinamento','Salute','Clima','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Living-Moving-Breathing/':('Rapporto','Denuncia','Proteggi','Inquinamento','Salute','Clima','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/comunicati/Greenpeace-Ue-rimuove-le-barriere-alla-rivoluzione-energetica-ma-lobiettivo-di-crescita-delle-rinnovabili-non-e-adeguato/':('Comunicato Stampa','Proteggi','Scegli','Energia','Clima','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/carne-a-tavola-meno-meglio/blog/61621/':('Storia','Denuncia','Scegli','Consumi','Cibo','Agricoltura','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/comunicati/Energia-Greenpeace-in-azione-in-Lussemburgo-Italia-si-schieri-in-difesa-di-rinnovabili-e-clima-Ue-punti-su-democrazia-energetica/':('Comunicato Stampa','Scegli','Proteggi','Energia','Clima','Consumi','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/Stop-diesel-a-Milano-Greenpeace-Scelta-coraggiosa-Sala-faccia-presto-e-con-determinazione/':('Comunicato Stampa','Denuncia','Denuncia','Inquinamento','Petrolio&Gas','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/comunicati/Plastica-Greenpeace-Bene-annuncio-Ikea-altri-grandi-marchi-seguano-lesempio/':('Comunicato Stampa','Scegli','Denuncia','Consumi','Inquinamento','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/comunicati/Spedizione-di-Greenpeace-scopre-preoccupanti-livelli-di-inquinamento-da-plastica-in-Antartide/':('Comunicato Stampa','Denuncia','Proteggi','Inquinamento','Mare','Biodiversità','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Vivere-Spostarsi-Respirare/':('Rapporto','Denuncia','Proteggi','Petrolio&Gas','Inquinamento','Salute','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/comunicati/Giornata-mondiale-ambiente-Greenpeace-chiede-ai-governi-del-G7-e-alle-multinazionali-di-fermare-linquinamento-da-plastica/':('Comunicato Stampa','Denuncia','Proteggi','Inquinamento','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Attiva-il-tuo-Plastic-Radar/':('Storia','Denuncia','Proteggi','Inquinamento','Mare','SaliABordo','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/In-azione-alla-Regione-Lazio-vogliamo-aria-pulita-/':('Storia','Denuncia','Proteggi','Inquinamento','Petrolio&Gas','Salute','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Eroi-della-rivoluzione-urbana/':('Storia','Denuncia','Scegli','Consumi','Inquinamento','Petrolio&Gas','article','Migrate'),
            ####'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Vivere-Spostarsi-Respirare/':('Rapporto','Denuncia','Proteggi','Inquinamento','Petrolio&Gas','Salute','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Mobilita-sostenibile-ecco-la-classifica-delle-citta-europee/':('Storia','Denuncia','Proteggi','Inquinamento','Petrolio&Gas','Salute','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/in-azione-per-la-democrazia-energetica-in-eur/blog/61520/':('Storia','Scegli','Proteggi','Energia','Clima','Consumi','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/api-una-ricchezza-inestimabile/blog/61509/':('Storia','Proteggi','Denuncia','Biodiversità','Cibo','Agricoltura','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/LItalia-deferita-alla-Corte-europea-/':('Storia','Denuncia','Proteggi','Inquinamento','Petrolio&Gas','Salute','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/I-petrolieri-pronti-a-bombardare-lo-Ionio/':('Storia','Denuncia','Proteggi','Petrolio&Gas','Clima','Mare','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Troppo-rumor-per-nulla/':('Rapporto','Denuncia','Proteggi','Petrolio&Gas','Clima','Mare','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Nuova-deforestazione-massiccia-in-Indonesia-per-lolio-di-palma/':('Storia','Proteggi','Scegli','Foreste','Biodiversità','Cibo','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/VITTORIA-Le-api-ringraziano/':('Storia','Proteggi','Scegli','Biodiversità','Cibo','Inquinamento','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/centrali-galleggianti-lennesima-follia-nuclea/blog/61437/':('Storia','Denuncia','','Energia','','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Inquinano-con-lammoniaca-eppure-ricevono-fondi-comunitari/':('Storia','Proteggi','Scegli','Inquinamento','Agricoltura','Consumi','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Come-la-PAC-promuove-linquinamento/':('Rapporto','Proteggi','Scegli','Inquinamento','Agricoltura','Consumi','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Abbiamo-le-prove-anche-il-nostro-mare-e-una-zuppa-di-plastica/':('Storia','Denuncia','Proteggi','Inquinamento','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Microplastic-investigation-in-water-and-trophic-chain-along-the-Italian-coast-/':('Rapporto','Denuncia','Proteggi','Inquinamento','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/assemblea-generali-azione/':('Storia','Denuncia','Proteggi','Energia','Inquinamento','Clima','article','Migrate'),

            ### P2
            'http://www.greenpeace.org/italy/it/News1/In-azione-in-Adriatico-Ieri-oggi-sempre-stop-trivelle/':('Storia','Denuncia','Proteggi','Petrolio&Gas','Mare','Clima','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/La-Nuova-Zelanda-vieta-le-trivellazioni-offshore-Greenpeace-Decisione-storica-Italia-segua-esempio/':('Comunicato Stampa','Denuncia','Proteggi','Petrolio&Gas','Clima','Mare','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/il-pianeta-nel-piatto/blog/61358/':('Storia','Scegli','Denuncia','Inquinamento','Agricoltura','Cibo','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Meno-e-meglio1/':('Rapporto','Scegli','Denuncia','Inquinamento','Agricoltura','Cibo','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Assicurazioni-Generali-la-nostra-video-inchiesta-con-telecamera-nascosta/':('Storia','Denuncia','Proteggi','Energia','Inquinamento','Clima','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/MariellePresente/':('Storia','Scegli','','Partecipazione','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Caccia-al-Krill-in-Antartide-/':('Storia','Proteggi','','Biodiversità','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Smog-in-Lazio-e-emergenza-sanitaria/':('Storia','Denuncia','Proteggi','Inquinamento','Petrolio&Gas','Salute','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Dirty-Business/':('Rapporto','Proteggi','','Energia','Inquinamento','Clima','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Bocciatura-clamorosa-per-laria-che-i-nostri-bambini-respirano-a-scuola/':('Storia','Denuncia','Proteggi','Petrolio&Gas','Inquinamento','Salute','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Ogni-respiro-e-un-rischio/':('Rapporto','Denuncia','Proteggi','Petrolio&Gas','Inquinamento','Salute','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Una-spedizione-in-Oceano-Antartico/':('Storia','Proteggi','','Mare','Biodiversità','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/la-legge-sui-sacchetti-buona-ma-lapplicazione/blog/60979/':('Storia','Denuncia','Scegli','Inquinamento','Mare','Consumi','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/dalla-scandinavia-alla-polonia-lottiamo-per-l/blog/60856/':('Storia','Proteggi','Scegli','Foreste','Consumi','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Natale-10-consigli-per-feste-ecosostenibili/':('Storia','Scegli','','Consumi','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/In-azione-a-Venezia/':('Storia','Denuncia','Proteggi','Inquinamento','Salute','Azioni','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/lo-scandalo-hm-dei-vestiti-bruciati/blog/60771/':('Storia','Scegli','','Consumi','','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/I-bambini-di-Milano-Respirano-smog-a-pieni-polmoni/':('Storia','Denuncia','Proteggi','Inquinamento','Petrolio&Gas','Salute','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/In-azione-con-lartista-TVboy-sui-muri-di-Roma-vogliamo-aria-pulita/':('Storia','Denuncia','Proteggi','Inquinamento','Petrolio&Gas','Salute','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Il-diesel-e-una-vera-minaccia-i-nostri-polmoni/':('Storia','Denuncia','Denuncia','Inquinamento','Petrolio&Gas','Salute','article','Migrate'),
            'http://www.greenpeace.org/italy/it/Glifosato-bene-il-no-dellItalia-diminuisce-il-numero-dei-paesi-a-favore-del-rinnovo/':('Comunicato Stampa','Denuncia','Proteggi','Agricoltura','Inquinamento','Biodiversità','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Lultima-bufala-italiana-sulla-pesca-illegale-del-pesce-spada/':('Rapporto','Proteggi','Scegli','Mare','Cibo','Consumi','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/In-azione-sulla-Tangenziale-Est-di-Roma-per-dire-Stop-Diesel/':('Storia','Denuncia','Proteggi','Inquinamento','Petrolio&Gas','Salute','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Phase-out-del-carbone-al-2025-per-lItalia/':('Storia','Proteggi','Denuncia','Energia','Clima','Inquinamento','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Cosa-respirano-i-bambini-di-Roma-al-mattino-prima-di-entrare-a-scuola/':('Storia','Denuncia','Proteggi','Inquinamento','Petrolio&Gas','Salute','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Corte-statunitense-respinge-le-accuse-di-Resolute-contro-Greenpeace/':('Storia','Proteggi','','Foreste','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Glifosato-anche-il-Minstro-della-Salute-votera-NO/':('Storia','Proteggi','Denuncia','Inquinamento','Biodiversità','Cibo','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/tempo-grande-foresta-del-nord-volontari/':('Storia','Proteggi','Scegli','Foreste','Consumi','SaliABordo','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Fashion-at-the-crossroads/':('Rapporto','Denuncia','Scegli','Inquinamento','Consumi','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/CETA-standard-europei-di-sicurezza-sotto-attacco/':('Rapporto','Denuncia','Scegli','Agricoltura','Cibo','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Emergenza-PFAS-in-Veneto-Chi-paga-/':('Rapporto','Denuncia','Proteggi','Inquinamento','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/La-sostenibilita-ambientale-delle-draghe-idrauliche-Non-esiste/':('Rapporto','Proteggi','','Mare','Biodiversità','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/In-azione-al-quartier-generale-di-Tempo/':('Storia','Proteggi','Scegli','Foreste','Consumi','Azioni','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Quiz-Solare-in-tante-citta-italiane/':('Storia','Scegli','Proteggi','Energia','Clima','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Non-sprechiamo-Tempo-salviamo-la-Foresta/':('Storia','Proteggi','Scegli','Foreste','Consumi','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Allavvocato-anti-PFAS-il-Nobel-alternativo/':('Storia','Denuncia','Proteggi','Inquinamento','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Chi-inquina-paga-e-la-Miteni/':('Storia','Denuncia','Proteggi','Inquinamento','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/In-azione-contro-un-cargo-di-Volkswagen/':('Storia','Denuncia','Proteggi','Inquinamento','Petrolio&Gas','Azioni','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Il-CETA-entra-in-vigore-in-via-provvisoria/':('Storia','Denuncia','Scegli','Agricoltura','Cibo','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/6-ragioni-per-cui-lindustria-dellauto-deve-im/blog/60214/':('Storia','Denuncia','Proteggi','Inquinamento','Petrolio&Gas','Clima','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Il-piu-grande-produttore-di-olio-di-palma-al-mondo-dovra-ripristinare-oltre-1000-ettari-di-foresta-/':('Storia','Denuncia','Scegli','Foreste','Consumi','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Temer-non-svendere-lAmazzonia-alle-aziende-minerarie-/':('Storia','Proteggi','','Foreste','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/una-lunga-estate-calda/blog/60001/':('Storia','Proteggi','','Clima','','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Assolto-Difendere-il-mare-non-e-un-crimine/':('Storia','Proteggi','','Mare','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Dieci-principi-per-gli-accordi-sul-commercio/':('Storia','Denuncia','Scegli','Agricoltura','Consumi','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/In-azione-a-Camogli-Il-Mediterraneo-non-e-usa-e-getta/':('Storia','Denuncia','Proteggi','Inquinamento','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Ci-siamo-La-Rainbow-Warrior-e-arrivata-in-Italia/':('Storia','Denuncia','Proteggi','Inquinamento','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Un-Mediterraneo-di-plastica/':('Rapporto','Denuncia','Proteggi','Inquinamento','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Meno-plastica-piu-Mediterraneo/':('Storia','Denuncia','Proteggi','Inquinamento','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Trump-esce-dallAccordo-di-Parigi/':('Storia','Denuncia','Proteggi','Inquinamento','Clima','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Le-parole-non-bastano-Salvate-i-nostri-mari-dalla-plastica/':('Storia','Denuncia','Proteggi','Inquinamento','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/dopo-anni-di-mancato-rispetto-della-legge-lin/blog/59552/':('Storia','Denuncia','Scegli','Mare','Cibo','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/un-futuro-100-rinnovabile-per-le-piccole-isol/blog/59535/':('Storia','Proteggi','Scegli','Clima','Energia','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/G7-a-Taormina-siamo-entrati-in-azione-per-difendere-il-clima/':('Storia','Denuncia','Proteggi','Energia','Clima','Azioni','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/In-azione-a-Taormina-Climate-justice-now/':('Storia','Denuncia','Proteggi','Energia','Clima','Azioni','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Planet-Earth-First-Un-messaggio-per-il-Pianeta-sulla-cupola-di-San-Pietro/':('Storia','Denuncia','Proteggi','Inquinamento','Clima','Azioni','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Una-doppia-minaccia-per-le-ultime-foreste-boreali-canadesi/':('Storia','Proteggi','Scegli','Foreste','Biodiversità','Consumi','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Acqua-delle-scuole-Venete-trovati-composti-chimici-PFAS/':('Storia','Denuncia','Proteggi','Inquinamento','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Non-ce-la-beviamo/':('Rapporto','Denuncia','Proteggi','Inquinamento','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/VOLONTARI-IN-21-CITTA-MOBILITAZIONE-PER-LE-API-/':('Storia','Denuncia','Proteggi','Biodiversità','Inquinamento','SaliABordo','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/STOP-TTIP-lICE-era-valida-/':('Storia','Scegli','','Consumi','Partecipazione','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/IN-AZIONE-Sciopero-delle-api-operaie-/':('Storia','Denuncia','Proteggi','Biodiversità','Inquinamento','Azioni','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/gli-zoo-non-salveranno-i-carib-dallestinzione/blog/59327/':('Storia','Proteggi','','Biodiversità','Clima','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Gli-Ikebiri-denunciano-ENI/':('Storia','Denuncia','','Inquinamento','Petrolio&Gas','Partecipazione','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Meta-degli-italiani-compra-piu-abiti-del-necessario/':('Rapporto','Denuncia','Scegli','Inquinamento','Consumi','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Eye-on-the-Taiga/':('Rapporto','Proteggi','','Biodiversità','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/la-foresta-dvinsky-in-pericolo/blog/58345/':('Storia','Proteggi','','Biodiversità','','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Trovate-pinne-di-squalo-illegali-su-un-peschereccio-italiano-in-Sierra-Leone-chiediamo-provvedimenti-severi-/':('Storia','Proteggi','','Biodiversità','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Immagina-una-Fashion-Revolution/':('Storia','Denuncia','Scegli','Inquinamento','Consumi','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/cernobyl-le-lezioni-che-non-abbiamo-imparato/blog/59272/':('Storia','Denuncia','Proteggi','Energia','Salute','','news-list','Migrate'),

            ### P3
            'http://www.greenpeace.org/italy/it/News1/Aberrante-lattacco-alle-ONG-pace-accoglienza-e-salvaguardia-vite-umane-sono-diritti-inalienabili/':('Storia','Proteggi','','Clima','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/le-tasse-scendono-ma-solo-per-i-petrolieri/blog/59229/':('Storia','Denuncia','Proteggi','Inquinamento','Petrolio&Gas','Energia','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Apple-usera-solo-materiale-riciclato/':('Storia','Denuncia','Scegli','Inquinamento','Consumi','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/lungheria-e-la-libert-che-difendo/blog/59170/':('Storia','Denuncia','Scegli','Agricoltura','Partecipazione','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/In-azione-al-G7-Energia-a-Roma/':('Storia','Denuncia','Proteggi','Energia','Clima','Azioni','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Trivelle-entro-le-12-miglia-il-Governo-aggira-il-divieto-e-fa-contenti-i-petrolieri/':('Storia','Denuncia','Proteggi','Petrolio&Gas','Energia','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Acqua-contaminata-da-Pfas-in-Veneto-inizia-il-monitoraggio-nelle-scuole/':('Storia','Denuncia','Proteggi','Inquinamento','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Salviamo-il-Mediterraneo-dallinvasione-della-plastica/':('Storia','Denuncia','Proteggi','Inquinamento','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/lue-ha-60-anni-ma-il-meglio-deve-ancora-arriv/blog/59036/':('Storia','Scegli','','Partecipazione','','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/In-azione-per-unEuropa-unita-solidale-e-rinnovabile/':('Storia','Proteggi','','Clima','Azioni','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/mars-e-nestl-fanno-un-passo-importante-per-pr/blog/58984/':('Storia','Proteggi','Scegli','Mare','Biodiversità','Consumi','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/se-la-plastica-ci-invade/blog/58951/':('Storia','Denuncia','Proteggi','Inquinamento','Mare','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/una-vita-da-prosumer/blog/58810/':('Storia','Scegli','','Energia','Consumi','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Non-ce-pace-senza-uguaglianza-di-genere/':('Storia','Scegli','','Partecipazione','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/In-azione-Lacqua-contaminata-non-ce-la-beviamo/':('Storia','Denuncia','Proteggi','Inquinamento','Salute','Azioni','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Pfas-in-Veneto-inquinamento-sotto-controllo/':('Rapporto','Denuncia','Proteggi','Inquinamento','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Lombra-del-conflitto-di-interessi-sulla-valutazione-di-sicurezza-del-glifosato/':('Storia','Denuncia','Proteggi','Inquinamento','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Disastro-di-Fukushima-i-diritti-violati-di-donne-e-bambini/':('Rapporto','Denuncia','Proteggi','Energia','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Salviamo-la-Grande-Foresta-del-Nord/':('Storia','Proteggi','','Foreste','Biodiversità','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/La-normalita-forzata-delle-vittime-di-Fukushima/':('Storia','Denuncia','Proteggi','Energia','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Nessun-ritorno-alla-normalita-per-gli-sfollati-di-Fukushima/':('Storia','Denuncia','Proteggi','Energia','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/leuropa-deve-assumere-la-leadership-per-la-pa/blog/58773/':('Storia','Scegli','Proteggi','Energia','Clima','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/nessuno-pu-trivellare-lartico-senza-rischi-ne/blog/58756/':('Storia','Denuncia','','Energia','Petrolio&Gas','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Ci-siamo-Lo-sfruttamento-del-petrolio-artico-finisce-in-tribunale/':('Storia','Denuncia','','Energia','Petrolio&Gas','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/-In-azione-Affondate-il-CETA-non-la-giustizia/':('Storia','Denuncia','','Agricoltura','Azioni','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/I-cittadini-europei-sfidano-il-glifosato1/':('Storia','Denuncia','Proteggi','Inquinamento','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/vittoria-stiamo-disintossicando-il-settore-de/blog/58667/':('Storia','Denuncia','Scegli','Inquinamento','Consumi','Partecipazione','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/ogni-singolo-pezzo-di-plastica-prodottoesiste/blog/58653/':('Storia','Denuncia','Scegli','Inquinamento','Consumi','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/La-barriera-corallina-amazzonica-un-tesoro-appena-scoperto-gia-in-pericolo/':('Storia','Proteggi','','Biodiversità','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/HSBC-la-banca-che-finanzia-la-distruzione-delle-foreste-indonesiane-/':('Storia','Proteggi','','Foreste','Biodiversità','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Rischi-ambientali-degli-insetticidi-neonicotinoidi/':('Rapporto','Denuncia','Proteggi','Inquinamento','Biodiversità','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Gli-insetticidi-neonicotinoidi-sono-pericolosi-non-solo-per-le-api-ma-anche-per-farfalle-e-uccelli-/':('Storia','Denuncia','Proteggi','Inquinamento','Biodiversità','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Quanto-sono-verdi-app-e-grandi-compagnie-come-Google-Facebook-o-Amazon/':('Storia','Denuncia','','Inquinamento','Energia','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/non-uno-ma-due-babbi-natale-per-lartico/blog/58357/':('Storia','Denuncia','Proteggi','Energia','Petrolio&Gas','Clima','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Energia-solare-per-una-cooperativa-agricola-femminile/':('Storia','Scegli','Proteggi','Energia','Clima','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Thailandia-nuovi-violazioni-dei-diritti-dei-lavoratori-e-pesca-illegale/':('Storia','Proteggi','','Mare','Biodiversità','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Lampedusa-oggi-abbiamo-acceso-il-sole-per-la-prima-volta/':('Storia','Scegli','','Energia','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Un-ecodecalogo-per-le-feste/':('Storia','Denuncia','Scegli','Inquinamento','Consumi','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Muta-come-un-pesce/':('Rapporto','Scegli','','Consumi','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/MUTA-COME-UN-PESCE-Indagine-sulle-etichette-illegali-in-Italia/':('Storia','Scegli','','Consumi','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/respira-e-prenditi-una-pausa-il-pianeta-non-s/blog/58152/':('Storia','Denuncia','Scegli','Inquinamento','Consumi','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/morire-per-la-difesa-dellambiente/blog/58079/':('Storia','Scegli','','Partecipazione','','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Un-Natale-per-il-Pianeta/':('Storia','','','SaliABordo','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/I-progressi-della-campagna-Tonno-in-Trappola-/':('Storia','Proteggi','Scegli','Mare','Cibo','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/--I-PFAS-e-altri-PFC-mettono-a-rischio-la-salute-/':('Storia','Denuncia','Proteggi','Inquinamento','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Come-i-PFC-entrano-nel-nostro-corpo/':('Rapporto','Denuncia','Proteggi','Inquinamento','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/news/veronesi-pinocchio-nucleare/':('Storia','Denuncia','','Energia','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Clima-urgente-un-piano-biennale-per-ridurre-le-emissioni/':('Storia','Denuncia','Proteggi','Inquinamento','Energia','Clima','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/vittoria-creato-in-antartide-il-santuario-oce/blog/57873/':('Storia','Proteggi','','Biodiversità','Mare','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Balene-bocciato-ancora-una-volta-un-santuario-nellAtlantico-meridionale/':('Storia','Proteggi','','Biodiversità','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/In-azione-durante-il-Consiglio-dei-Ministri-UE/':('Storia','Proteggi','Scegli','Agricoltura','Azioni','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/ACCENDIAMO-IL-SOLE-impianto-consegnato/':('Storia','Scegli','Proteggi','Energia','Clima','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Renzi-le-bugie-hanno-le-gambe-corte-anche-quando-si-parla-di-clima/':('Storia','Denuncia','Proteggi','Petrolio&Gas','Mare','Azioni','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/come-siamo-riusciti-a-volare-intorno-alla-pi-/blog/57700/':('Storia','Proteggi','Scegli','Clima','Energia','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/In-azione-con-un-gommone-volante-e-un-paramotore/':('Storia','Proteggi','Scegli','Clima','Energia','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/In-azione-a-Saline-Joniche-contro-il-carbone/':('Storia','Denuncia','','Inquinamento','Energia','Azioni','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Parte-oggi-da-Bari-il-tour-italiano-della-Rainbow-Warrior/':('Storia','Proteggi','Scegli','Clima','Clima','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/domani-il-film-che-racconta-un-futuro-miglior/blog/57648/':('Storia','Denuncia','Proteggi','Inquinamento','Agricoltura','Clima','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Il-pesce-sta-finendo-impariamo-a-consumare-in-modo-responsabile/':('Storia','Proteggi','Scegli','Mare','Cibo','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/ioi-ora-tempo-di-agire-e-guidare-il-cambiamen/blog/57640/':('Storia','Proteggi','','Foreste','Biodiversità','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/la-rainbow-warrior-torna-in-italia-per-accend/blog/57627/':('Storia','Proteggi','Scegli','Clima','Energia','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Telecamere-nascoste-al-mercato-del-pesce/':('Storia','Scegli','','Cibo','Consumi','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/In-azione-a-Rotterdam-per-difendere-le-foreste/':('Storia','Proteggi','Scegli','Foreste','Cibo','Azioni','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/facciamo-una-pace-verde/blog/57564/':('Storia','Scegli','','Partecipazione','','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Tisaleaks-Greenpeace-Olanda-svela-testi-segreti-del-TiSA/':('Storia','Denuncia','','Inquinamento','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Vogliamo-accendere-il-sole-in-tutta-Italia/':('Storia','Proteggi','Scegli','Clima','Energia','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/FishFinder-una-guida-tascabile-per-lacquisto-responsabile-del-pesce/':('Storia','Proteggi','Scegli','Mare','Cibo','Consumi','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/ioi-il-gigante-malese-dellolio-di-palma-che-c/blog/57514/':('Storia','Proteggi','Scegli','Foreste','Cibo','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/qua-la-zampa-whiskas-ci-ha-ascoltato/blog/57454/':('Storia','Scegli','Proteggi','Mare','Cibo','Consumi','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/3-buoni-motivi-per-cui-abbiamo-bisogno-di-san/blog/57397/':('Storia','Proteggi','','Mare','','','news-list','Migrate'),

            ### P4
            'http://www.greenpeace.org/italy/it/News1/plastica-in-mare-una-bomba-tossica-a-orologeria/':('Storia','Proteggi','Scegli','Mare','Consumi','Inquinamento','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/la-plastica-nel-piatto-dal-pesce-ai-frutti-di-mare/':('Storia','Proteggi','Scegli','Mare','Consumi','Inquinamento','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/un-ricordo-di-berta-cceres-contro-la-violenza/blog/57227/':('Storia','Proteggi','Scegli','Biodiversità','Partecipazione','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/transocean-la-piattaforma-in-balia-della-temp/blog/57220/':('Storia','Denuncia','Proteggi','Petrolio&Gas','Mare','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/VITTORIA-Annullato-il-mega-progetto-della-diga-sul-Tapajos/':('Storia','Proteggi','Scegli','Foreste','Partecipazione','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/ministro-calenda-quando-inizieremo-a-puntare-/blog/57138/':('Storia','Proteggi','Scegli','Clima','Energia','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Microsfere-di-plastica-nemiche-degli-oceani/':('Storia','Proteggi','Scegli','Mare','Consumi','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Il-Mediterraneo-e-fatto-di-sole-e-di-vento-perche-non-li-sfruttiamo/':('Storia','Scegli','Proteggi','Energia','Clima','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Una-mostra-fotografica-e-un-film-a-Roma-per-festeggiare-i-nostri-30-anni/':('Storia','','','','SaliABordo','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Si-e-acceso-il-sole-chi-lo-ha-acceso-sei-tu/':('Storia','Scegli','','Energia','SaliABordo','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Il-Marocco-vieta-limportazione-dei-rifiuti-dallItalia/':('Storia','Denuncia','','Inquinamento','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Compiamo-30-anni-e-non-mettiamo-la-testa-a-posto/':('Storia','','','SaliABordo','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Altre-due-aziende-aderiscono-a-Detox/':('Storia','Scegli','','Consumi','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Accendiamo-il-Sole-raccolti-oltre-24-mila-euro-per-solarizzare-Lampedusa-Grazie/':('Storia','Scegli','','Energia','SaliABordo','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Olimpiadi-Roma-2024-la-lettera-delle-associazioni/':('Storia','Denuncia','','Inquinamento','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Siemens-ascoltaci-rinuncia-a-distruggere-lAmazzonia/':('Storia','Denuncia','Proteggi','Foreste','Azioni','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/spegniamo-il-petrolio-accendiamo-il-sole/blog/56966/':('Storia','Scegli','Proteggi','Energia','Consumi','Clima','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/CETA-si-alla-ratifica-dei-parlamenti-ma-in-tutta-troppa-fretta/':('Storia','Denuncia','Scegli','Consumi','Cibo','Agricoltura','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/sfilata-detox-2016-quali-marchi-sono-passati-/blog/56952/':('Storia','Scegli','','Consumi','','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/detox-outdoor-costruiamo-insieme-la-campagna/blog/54663/':('Storia','Denuncia','Scegli','Inquinamento','Consumi','Partecipazione','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/la-sicurezza-alimentare-non-pu-aspettare-vane/blog/56929/':('Storia','Denuncia','Scegli','Cibo','Consumi','Agricoltura','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/PER-IL-NOSTRO-COMPLEANNO-ACCENDIAMO-IL-SOLE-PER-UNA-LAMPEDUSA-100-RINNOVABILE-/':('Storia','Scegli','Proteggi','Energia','Clima','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/amazzonia-primo-successo-dei-kaapor-nella-lot/blog/56887/':('Storia','Proteggi','Scegli','Foreste','Partecipazione','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/i-munduruku-non-vogliono-abbandonare-il-loro-/blog/56825/':('Storia','Proteggi','Scegli','Foreste','Partecipazione','Biodiversità','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Musica-per-lArtico-Ludovico-Einaudi-al-piano-fra-i-ghiacci/':('Storia','Proteggi','','Clima','Azioni','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/la-croazia-chiude-i-suoi-mari-a-trivelle-e-pe/blog/56789/':('Storia','Denuncia','Proteggi','Petrolio&Gas','Energia','Clima','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/al-fianco-dei-munduruku-per-proteggere-il-cuo/blog/56777/':('Storia','Proteggi','Scegli','Foreste','Partecipazione','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Proteggi-il-cuore-dellAmazzonia/':('Storia','Proteggi','','Foreste','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Il-CETA-laccordo-commerciale-UE-Canada-non-puo-rinunciare-alla-verifica-parlamentare/':('Storia','Denuncia','Scegli','Cibo','Agricoltura','Biodiversità','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Libero-scambio-UE-Canada-escludere-i-parlamenti-nazionali-e-antidemocratico/':('Storia','Denuncia','Scegli','Cibo','Agricoltura','Biodiversità','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/LArtico-si-scalda-due-volte-piu-in-fretta-del-resto-del-Pianeta/':('Storia','Proteggi','','Clima','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Cio-che-accade-nellArtico-non-resta-confinato-nellArtico/':('Comunicato Stampa','Proteggi','','Clima','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Altre-10-aziende-scelgono-di-produrre-senza-sostanze-tossiche/':('Storia','Scegli','','Consumi','Inquinamento','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/le-bugie-dei-petrolieri/':('Rapporto','Denuncia','','Petrolio&Gas','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Offshore-IBLEO/':('Rapporto','Denuncia','','Petrolio&Gas','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/in-citt-non-si-respira-e-il-nostro-governo-vu/blog/56588/':('Storia','Denuncia','Proteggi','Petrolio&Gas','Inquinamento','Energia','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Vittoria-Stop-alla-pesca-a-strascico-nellArtico/':('Storia','Proteggi','','Mare','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/In-azione-Bloccato-stabilimento-di-Thai-Union-in-Francia/':('Storia','Proteggi','Scegli','Azioni','Mare','Consumi','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Tonno-Mareblu-sei-proprio-insostenibile/':('Storia','Scegli','Proteggi','Mare','Consumi','Cibo','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/sei-cose-da-sapere-sul-ttip/blog/56497/':('Storia','Scegli','Denuncia','Agricoltura','Cibo','Biodiversità','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/un-maestro-di-vita-un-guerriero-dellarcobalen/blog/56490/':('Storia','Scegli','','Partecipazione','','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Mareblu-smascherato-sul-luogo-di-pesca/':('Storia','Denuncia','Scegli','Mare','Cibo','Consumi','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Disastro-a-Chiloe-migliaia-di-animali-spiaggiati-senza-vita/':('Storia','Proteggi','Denuncia','Mare','Petrolio&Gas','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/incendi-in-canada-uno-dei-volti-dei-cambiamen/blog/56442/':('Storia','Proteggi','','Clima','','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/lesperanza-nelloceano-indiano-a-caccia-di-fad/blog/56406/':('Storia','Proteggi','','Mare','Azioni','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/IN-AZIONE-YES-WE-CAN-STOP-TTIP-/':('Storia','Denuncia','','Agricoltura','Azioni','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/dal-cuore-dellamazzonia-al-cuore-delle-aziend/blog/56389/':('Storia','Proteggi','','Foreste','','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/news/Cosa-si-nasconde-in-una-scatoletta-di-tonno/':('Storia','Scegli','','Consumi','Cibo','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/news/Tonno-in-trappola-Di-la-tua-I-risultati-del-sondaggio/':('Storia','Scegli','','Consumi','Cibo','Mare','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/news/Vittoria-Tonno-Mareblu-100-sostenibile-al-2016/':('Storia','Proteggi','Scegli','Cibo','Consumi','Mare','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Tonno-in-scatola-Se-alle-promesse-non-seguono-i-fatti/':('Storia','Proteggi','Scegli','Cibo','Consumi','Mare','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Tonno-ecco-il-video-shock-che-racconta-cosa-finisce-nelle-reti/':('Storia','Denuncia','Proteggi','Cibo','Consumi','Mare','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Il-lato-oscuro-dellindustria-del-tonno/':('Storia','Denuncia','Proteggi','Cibo','Consumi','Mare','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Tonno-e-ora-di-una-svolta-sostenibile/':('Storia','Proteggi','Scegli','Mare','Cibo','Consumi','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Cosa-finisce-nella-tua-scatoletta-di-tonno/':('Storia','Proteggi','Scegli','Mare','Cibo','Consumi','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/mareblu-e-la-sostenibilit-solo-promesse-da-ma/blog/54603/':('Storia','Proteggi','Scegli','Mare','Cibo','Consumi','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Basta-svuotare-il-mare-per-una-scatoletta-di-tonno/':('Storia','Proteggi','Scegli','Mare','Cibo','Consumi','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Quella-sporca-filiera/':('Storia','Proteggi','Scegli','Mare','Cibo','Consumi','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Milano-Mareblu-si-tinge-di-rosso-sangue/':('Storia','Proteggi','Scegli','Mare','Cibo','Consumi','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Esperanza-in-Oceano-Indiano-/':('Storia','Proteggi','Scegli','Mare','Cibo','Azioni','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/BREAKING-TTIP-leaks-Greenpeace-Olanda-rivela-i-testi-segreti-del-TTIP/':('Storia','Denuncia','Scegli','Agricoltura','Cibo','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/TTIP-leaks/':('Comunicato Stampa','Denuncia','Scegli','Agricoltura','Cibo','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Amazzonia-a-rischio-/':('Storia','Proteggi','','Foreste','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Cernobyl-30-anni-dopo/':('Storia','Denuncia','','Energia','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Accordo-sul-Clima-di-Parigi-abbiamo-scritto-a-Matteo-Renzi/':('Storia','Denuncia','Proteggi','Energia','Clima','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Gli-USA-fanno-pressione-sulla-Commissione-UE/':('Storia','Denuncia','Scegli','Agricoltura','Cibo','Consumi','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/La-settimana-mondiale-del-riciclo-di-HM-sette-giorni-di-di-illusioni-per-i-consumatori/':('Storia','Scegli','','Consumi','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Quella-sporca-filiera/':('Rapporto','Scegli','','Cibo','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/La-Barriera-Corallina-e-in-pericolo/':('Storia','Proteggi','','Mare','Biodiversità','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Referendum-trivelle-niente-quorum/':('Storia','Denuncia','Proteggi','Petrolio&Gas','Mare','Energia','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/In-azione-a-Roma-Torino-e-Venezia-un-Si-per-rottamare-le-fonti-fossili/':('Storia','Denuncia','Proteggi','Petrolio&Gas','Mare','Azioni','article','Migrate'),

            ### P5
            'http://www.greenpeace.org/italy/it/News1/ENI-ci-denuncia-perche-difendiamo-il-mare/':('Storia','Denuncia','Proteggi','Petrolio&Gas','Mare','Energia','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/In-azione-a-Napoli-Piattaforme-Un-rischio-inaccettabile/':('Storia','Denuncia','Proteggi','Petrolio&Gas','Mare','Azioni','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Renzi-invita-gli-italiani-a-rottamare-le-trivelle/':('Storia','Denuncia','Proteggi','Petrolio&Gas','Mare','Energia','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Referendum-mobilitazione-contro-le-trivelle-in-tutta-Italia/':('Storia','Denuncia','Proteggi','Petrolio&Gas','Mare','SaliABordo','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Una-trivella-nella-citta-di-Renzi-Ci-sara-petrolio/':('Storia','Denuncia','Proteggi','Petrolio&Gas','Mare','Azioni','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Dalle-profondita-dei-mari-un-messaggio-contro-le-trivelle/':('Storia','Denuncia','Proteggi','Petrolio&Gas','Mare','Azioni','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Ricerca-in-agricoltura-non-vuol-dire-OGM/':('Storia','Denuncia','Scegli','Agricoltura','Cibo','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/Greenpeace-a-Renzi-aspettiamo-il-confronto-promesso-il-referendum-e-vicino/':('Comunicato Stampa','Denuncia','Proteggi','Petrolio&Gas','Mare','Energia','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Referendum-trivelle-12-grandi-artisti-in-difesa-del-mare/':('Storia','Denuncia','Proteggi','Petrolio&Gas','Mare','Azioni','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/cosa-finisce-nel-mio-whiskas/blog/56041/':('Storia','Proteggi','Scegli','Mare','Cibo','Consumi','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Trivelle-vecchie-spilorce/':('Storia','Proteggi','Denuncia','Petrolio&Gas','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Far-west-nei-mari-italiani-100-piattaforme-senza-controllo/':('Storia','Denuncia','Proteggi','Petrolio&Gas','Mare','Energia','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/In-azione-su-una-piattaforma-in-Adriatico/':('Storia','Denuncia','Proteggi','Azioni','Petrolio&Gas','Mare','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Rinnovabili-nel-mirino-il-nostro-nuovo-Report/':('Rapporto','Scegli','Proteggi','Energia','Clima','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Rinnovabili-nel-mirino/':('Rapporto','Scegli','Proteggi','Energia','Clima','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/rio-tapajos-il-fiume-della-vita/blog/55945/':('Storia','Proteggi','Scegli','Foreste','Partecipazione','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Oil-men-contro-le-trivelle/':('Storia','Denuncia','Proteggi','Petrolio&Gas','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Altre-cinque-aziende-italiane-aderiscono-a-DETOX/':('Storia','Denuncia','Scegli','Inquinamento','Consumi','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/In-azione-sulla-Montagna-Spaccata-fermiamo-le-trivelle-con-il-referendum/':('Storia','Denuncia','Proteggi','Petrolio&Gas','Mare','Azioni','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Cozze-di-piattaforma-dal-mare-al-piatto/':('Storia','Denuncia','Proteggi','Inquinamento','Petrolio&Gas','Mare','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Leredita-nucleare-di-Fukushima-e-Cernobyl/':('Rapporto','Denuncia','','Energia','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/non-lasciamo-che-le-foreste-del-paradiso-bruc/blog/55769/':('Storia','Proteggi','Scegli','Foreste','Consumi','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Italia-e-petrolio-Un-matrimonio-impossibile/':('Storia','Denuncia','Proteggi','Petrolio&Gas','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Radiation-reloaded/':('Rapporto','Denuncia','','Energia','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Basta-sprechi-per-il-referendum-sulle-trivelle-serve-lElection-Day/':('Storia','Denuncia','Scegli','Petrolio&Gas','Partecipazione','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Referendum-trivelle-la-truffa-del-governo-alla-democrazia/':('Storia','Denuncia','Scegli','Petrolio&Gas','Partecipazione','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Referendum-trivelle-il-nostro-appello-a-Mattarella/':('Storia','Denuncia','Scegli','Petrolio&Gas','Partecipazione','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/LItalia-non-si-trivella-Attivisti-allAltare-della-Patria/':('Storia','Denuncia','Proteggi','Petrolio&Gas','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Trivelle-fuorilegge-la-verita-nel-nostro-nuovo-rapporto-/':('Storia','Denuncia','Proteggi','Petrolio&Gas','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/In-azione-da-The-North-Face/':('Storia','Denuncia','','Inquinamento','Azioni','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/In-azione-Stiamo-bloccando-le-trattative-sul-TTIP-/':('Storia','Proteggi','','Biodiversità','Azioni','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Trivelle-fuorilegge/':('Rapporto','Denuncia','Proteggi','Petrolio&Gas','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/La-Rainbow-Warrior-a-Fukushima-per-le-analisi-della-radioattivita-delle-acque-/':('Comunicato Stampa','Denuncia','','Energia','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/la-paura-di-renzi-fa-17-aprile/blog/55567/':('Storia','Denuncia','Proteggi','Mare','Partecipazione','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/detox-una-nuova-rivoluzione-industriale-parte/blog/55529/':('Storia','Denuncia','','Inquinamento','','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Meglio-nudi-o-in-pigiama-che-con-i-PFC/':('Storia','Denuncia','Proteggi','Inquinamento','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/impresa-di-un-alpinista-italiano-in-cima-al-f/blog/55477/':('Storia','Denuncia','','Inquinamento','','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Il-governo-da-il-via-libera-alla-piattaforma-petrolifera-Ombrina-/':('Storia','Denuncia','Proteggi','Petrolio&Gas','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Trivelle-agli-italiani-non-piacciono/':('Storia','Denuncia','Proteggi','Petrolio&Gas','Mare','Partecipazione','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Trivelle-la-Corte-Costituzionale-ammette-il-referendum/':('Storia','Denuncia','Proteggi','Petrolio&Gas','Mare','Partecipazione','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/grandi-notizie-per-gli-amanti-delloutdoor-i-p/blog/55421/':('Storia','Denuncia','','Inquinamento','','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/rapporto-pericolose-sostanze-chimiche-nellabb/blog/55387/':('Storia','Denuncia','Proteggi','Inquinamento','Salute','Consumi','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Tracce-nascoste-nelloutdoor/':('Rapporto','Denuncia','','Inquinamento','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/GENE-EDITING-OGM-che-escono-dalla-porta-e-rientrano-dalla-finestra/':('Rapporto','Denuncia','Proteggi','Agricoltura','Biodiversità','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/La-Consulta-da-ai-cittadini-la-parola-decisiva-sulle-trivelle/':('Comunicato Stampa','Denuncia','Proteggi','Petrolio&Gas','Mare','Partecipazione','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Impronte-nella-neve/':('Rapporto','Denuncia','','Inquinamento','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Greenpeace-International-annuncia-due-nuovi-co-direttori-esecutivi/':('','','','','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/spedizione-in-patagonia-sulla-vetta-del-cerro/blog/55294/':('Storia','Denuncia','','Inquinamento','','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/blog/se-questo-un-nobel/blog/55269/':('Storia','Denuncia','Proteggi','Agricoltura','Biodiversità','','news-list','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Salvo-per-ora-lhabitat-del-panda/':('Storia','Proteggi','','Foreste','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/News1/Disastro-ambientale-fuga-di-gas-a-Los-Angeles-dichiarato-lo-stato-di-emergenza/':('Storia','Denuncia','Proteggi','Petrolio&Gas','Clima','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Trivelle-in-mare-cosa-ne-pensano-gli-italiani/':('Rapporto','Denuncia','Proteggi','Petrolio&Gas','Mare','Partecipazione','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Goliat-lelefante-bianco-/':('Rapporto','Denuncia','Proteggi','Petrolio&Gas','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/100-rinnovabili-un-nuovo-futuro-per-le-piccole-isole/':('Rapporto','Proteggi','Scegli','Clima','Energia','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Labuso-di-pesticidi-nella-produzione-europea-di-mele/':('Rapporto','Denuncia','Proteggi','Agricoltura','Biodiversità','Cibo','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/La-dipendenza-da-pesticidi-dellEuropa-minaccia-il-nostro-ambiente/':('Rapporto','Denuncia','Proteggi','Agricoltura','Biodiversità','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Energy-Revolution-2015/':('Rapporto','Proteggi','Scegli','Clima','Energia','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Bombardamento-a-tappeto/':('Rapporto','Denuncia','Proteggi','Petrolio&Gas','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Acciughe-al-collasso-un-piccolo-pesce-in-grande-pericolo/':('Rapporto','Proteggi','','Mare','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Il-gusto-amaro-della-produzione-intensiva-di-mele/':('Rapporto','Denuncia','Proteggi','Agricoltura','Biodiversità','Cibo','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Health-and-economic-implications-of-alternative-emission-limits-for-coal-fired-power-plants-in-the-EU/':('Rapporto','Denuncia','Proteggi','Energia','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Sette-proposte-per-lagricoltura-sostenibile-del-futuro/':('Rapporto','Denuncia','Proteggi','Agricoltura','Biodiversità','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/A-come-ape/':('Rapporto','Denuncia','Proteggi','Agricoltura','Biodiversità','Cibo','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Api-il-bottino-avvelenato/':('Rapporto','Denuncia','Proteggi','Agricoltura','Biodiversità','Cibo','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Gocce-al-veleno/':('Rapporto','Denuncia','Proteggi','Agricoltura','Biodiversità','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Smoke-and-Mirrors---I-piu-grandi-inquinatori-dEuropa-si-dettano-le-regole/':('Rapporto','Denuncia','Proteggi','Energia','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Eden-tossico/':('Rapporto','Denuncia','Proteggi','Agricoltura','Biodiversità','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Tossico-come-un-pesticida/':('Rapporto','Denuncia','Proteggi','Agricoltura','Biodiversità','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Lettera-di-Greenpeace-a-Sua-Santita-Francesco/':('Rapporto','Denuncia','Proteggi','Energia','Clima','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Fukushima-4-anni-fa-il-disastro-nucleare/':('Rapporto','Denuncia','','Energia','','','article','Migrate'),

            ### P6
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Smart_Breeding/':('Rapporto','Denuncia','Proteggi','Agricoltura','Biodiversità','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Le-ricadute-economiche-delle-energie-rinnovabili-in-Italia/':('Rapporto','Scegli','Proteggi','Energia','Clima','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Allarme-Amazzonia-notti-di-terrore-per-le-foreste/':('Rapporto','Proteggi','','Foreste','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/la-posizione-di-greenpeace-sul-ttip/':('Rapporto','Scegli','','Partecipazione','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Lettera-al-ministro-dellambiente/':('Rapporto','Proteggi','','Mare','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/toxic-costa/':('Rapporto','Denuncia','Proteggi','Inquinamento','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/come-sta-il-mare-del-giglio/':('Rapporto','Denuncia','Proteggi','Inquinamento','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Dieci-cose-da-dire-sulla-Costa-Concordia/':('Rapporto','Denuncia','Proteggi','Inquinamento','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/tonno/':('Rapporto','Proteggi','','Mare','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/No-blood-for-coal/':('Rapporto','Denuncia','Proteggi','Energia','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Il-legno-illegale-che-distrugge-lAmazzonia/':('Rapporto','Proteggi','Scegli','Foreste','Consumi','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/G7-Energia-Vogliamo-lindipendenza-energetica-dai-combustibili-fossili-non-dalla-Russia/':('Rapporto','Scegli','Proteggi','Energia','Clima','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Costa-Concordia-il-balletto-del-traino/':('Rapporto','Denuncia','Proteggi','Inquinamento','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Quale-futuro-energetico-per-lEuropa/':('Rapporto','Denuncia','Proteggi','Energia','Clima','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/piccola-storia-di-una-bugia-fuori-moda/':('Rapporto','Denuncia','Proteggi','Inquinamento','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Lettera-al-Commissario-Borg/':('Rapporto','Denuncia','Proteggi','Agricoltura','Biodiversità','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Outdoor-clothing/':('Rapporto','Denuncia','Proteggi','Inquinamento','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Licenza-di-uccidere/':('Rapporto','Proteggi','Scegli','Foreste','Consumi','Cibo','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Energy-Revolution-2013/':('Rapporto','Scegli','Proteggi','Energia','Clima','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Le-scelte-che-dobbiamo-compiere-per-salvare-il-clima/':('Rapporto','Denuncia','Proteggi','Energia','Clima','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/MON810-Una-storia-di-mais-farfalle-e-rischi-inutili/':('Rapporto','Denuncia','Proteggi','Agricoltura','Biodiversità','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Erbe-cinesi/':('Rapporto','Denuncia','Proteggi','Agricoltura','Biodiversità','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/I-libri-piu-amati-Quelli-in-carta-riciclata/':('Rapporto','Proteggi','Scegli','Foreste','Consumi','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/I-vizi-di-Eni/':('Rapporto','Denuncia','Proteggi','Petrolio&Gas','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Una-pesca-sostenibile-per-il-futuro-del-mare/':('Rapporto','Proteggi','','Mare','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Killer-silenziosi/':('Rapporto','Denuncia','Proteggi','Energia','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Sperimentazioni-di-OGM-in-ambiente-un-affare-rischioso-e-costoso/':('Rapporto','Denuncia','Proteggi','Agricoltura','Biodiversità','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Porto-Tolle-analisi-comparativa-dellimpatto-sanitario/':('Rapporto','Denuncia','Proteggi','Energia','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Futuro-a-rischio-per-il-pesce-azzurro-nel-Canale-di-Sicilia/':('Rapporto','Proteggi','','Mare','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Api-in-declino/':('Rapporto','Denuncia','Proteggi','Agricoltura','Cibo','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Aggiornamento-sugli-stress-test-nucleari-in-UE/':('Rapporto','Denuncia','','Energia','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Un-piano-blu-per-la-Sicilia/':('Rapporto','Denuncia','Proteggi','Petrolio&Gas','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Come-distruggere-il-clima-in-14-mosse/':('Rapporto','Proteggi','Scegli','Clima','Energia','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Tessuti-tossici-contaminati-dalla-moda/':('Rapporto','Denuncia','Proteggi','Inquinamento','Salute','Consumi','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Tessuti-tossici-linquinamento-in-mostra/':('Rapporto','Denuncia','Proteggi','Inquinamento','Salute','Consumi','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Energy-Revolution-2012/':('Rapporto','Scegli','Proteggi','Energia','Clima','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Colture-resistenti-al-glifosato-nellUnione-Europea-/':('Rapporto','Denuncia','Proteggi','Agricoltura','Biodiversità','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Energy-Revolution-2012---Sintesi-in-italiano/':('Rapporto','Scegli','Proteggi','Energia','Clima','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Nuclear-Stress-Tests/':('Rapporto','Denuncia','','Energia','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Pesce-azzurro-al-collasso/':('Rapporto','Proteggi','Scegli','Mare','Consumi','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Meglio-loro-blu-delloro-nero/':('Rapporto','Denuncia','Proteggi','Petrolio&Gas','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/I-tesori-sommersi-del-Canale-di-Sicilia-/':('Rapporto','','','','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Enel---Il-carbone-costa-un-morto-al-giorno/':('Rapporto','Denuncia','Proteggi','Energia','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Enel-Today--Tomorrow/':('Rapporto','Denuncia','Proteggi','Energia','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/greenfreeze-la-tecnologia-del-freddo-che-salvera-il-clima/':('Rapporto','Denuncia','Proteggi','Energia','Clima','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/rio-20-per-una-green-economy-equa-e-giusta/':('Rapporto','Proteggi','','Foreste','Clima','Mare','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Lincidente-del-Mersa-2-allIsola-dElba/':('Rapporto','Denuncia','Proteggi','Inquinamento','Mare','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/Favole-da-incubo/':('Rapporto','Proteggi','','Foreste','','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/nuvola-digitale-quanto-e-pulita/':('Rapporto','Denuncia','Proteggi','Energia','Clima','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/enel-veri-costi-carbone/':('Rapporto','Denuncia','Proteggi','Energia','Clima','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/quale-futuro-per-il-vino-italiano/':('Rapporto','Denuncia','Proteggi','Agricoltura','Biodiversità','Cibo','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/panni-sporchi-tre/':('Rapporto','Denuncia','Proteggi','Inquinamento','Salute','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/partita-a-ramino-quello-illegale/':('Rapporto','Proteggi','Scegli','Foreste','Consumi','','article','Migrate'),
            'http://www.greenpeace.org/italy/it/ufficiostampa/rapporti/quale-futuro-per-il-santuario-dei-cetacei-nel-mar-ligure/':('Rapporto','Proteggi','','Mare','','','article','Migrate')
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
            'author': 'Greenpeace Italy',
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

        # Replace the italian month name with english month name.
        #for it_month, en_month in month_it_en.iteritems():
        #    month_name = month_name.replace(it_month, en_month)

        month_it_en = {
            'gennaio': 'January',
            'febbraio': 'February',
            'marzo': 'March',
            'aprile': 'April',
            'maggio': 'May',
            'giugno': 'June',
            'luglio': 'July',
            'agosto': 'August',
            'settembre': 'September',
            'ottobre': 'October',
            'novembre': 'November', 
            'dicembre': 'December', 
        }

        # Replace the italian month name with english month name.
        for it_month, en_month in month_it_en.iteritems():
            month_name = month_name.replace(it_month, en_month)

        return month_name;

    def csv_writer(self, data, path):
        # Write data to a CSV file path
        with open(path, "a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(data)
