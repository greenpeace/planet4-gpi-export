import scrapy
import logging
import locale
import dateutil.parser
import re

locale.setlocale(locale.LC_ALL, '')

class AllSpider(scrapy.Spider):
    name = 'all'

    custom_settings = {
        'ROBOTSTXT_OBEY': 0,
        'FEED_URI': 'all_gpi_D13.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def start_requests(self):

        start_urls = {'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/10-reasons-why-arctic-drilling-is-a-really-st/blog/39225/':('Story','Climate & Energy, Oceans','PeopleVsOil, OceanSanctuaries'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/3-plant-based-recipes-you-need-to-try-this-world-meat-free-day/blog/56672/':('Story','Food','MeatAndDairy'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/3-reasons-why-we-need-ocean-sanctuaries/blog/57389/':('Story','Oceans','OceanSanctuaries'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/3M-Post-It-Notes-announces-sustainable-paper-buying-policy/blog/52250/':('Story','Forests','StandForForests'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/4-reasons-we-all-should-stand4forests/blog/48584/':('Story','Forests','StandForForests'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/5-lesser-known-threats-to-the-fragile-arctic-/blog/56191/':('Story','Climate & Energy','PeopleVsOil'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/5-ways-tech-companies-are-making-your-devices/blog/59728/':('Story','Detox','RethinkIT'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/6-plastic-bans-worldwide-take-the-pledge/blog/57180/':('Story','Detox','NoPlastics'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/7-reasons-bottom-trawling-is-bad-news/blog/56982/':('Story','Ships, Oceans','ArcticSunrise'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/agrotoxics-esperanza-sinaloa/blog/53800/':('Story','Ships, Food','Esperanza, FixFood'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/aldi-commits-to-detox/blog/52456/':('Story','Detox','Fashion'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/amazon-reef-brazil-new-endangered-discovery/blog/58596/':('Story','Ships, Oceans','Esperanza, OceanSanctuaries'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/arctic-fishing-fleets-threat-to-ecosystem/blog/55709/':('Story','Climate & Energy, Oceans','PeopleVsOil, OceanSanctuaries'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/arctic-protection-ocean-sanctuary-ecosystem-OSPAR/blog/55681/':('Story','Climate & Energy, Oceans','PeopleVsOil, OceanSanctuaries'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/are-you-being-slapped-how-corporations-and-go/blog/49345/':('Story','Forests','OurVoicesAreVital'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/ariculture-revolution-germany-berlin/blog/58577/':('Story','Food','MeatAndDairy'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/artivists-save-the-arctic-competition-voyage/blog/56587/':('Story','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/at-8-million-strong-the-arctic-story-is-just-/blog/56831/':('Story','Climate & Energy','PeopleVsOil'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/bees-farming-pesticides-eu/blog/59287/':('Story','Food','FixFood'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/benetton-shows-its-true-colours-and-commits-t/blog/43672/':('Story','Detox','Fashion'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/biological-restoration-of-water-land-Rex-Weyler/blog/58920/':('Story','Food','FixFood'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/black-friday-planet-cant-take-it-buy-nothing-day/blog/58077/':('Story','Detox','Fashion'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/bottom-trawling-ghost-nets-diving-arctic-sunrise/blog/56500/':('Story','Ships, Oceans','ArcticSunrise, OceanSanctuaries'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/brazil-rotten-meat-crisis-industrial-agriculture/blog/59024/':('Story','Food','MeatAndDairy'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/bring-it-on-2017-new-years-resolutions-for-pe/blog/58351/':('Story','Forests','StandForForests'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/canada-sending-wild-caribou-herd-to-a-zoo/blog/59307/':('Story','Forests','StandForForests'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/citizen-science-measuring-air-pollution/blog/57987/':('Story','Detox','Fashion'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/Clara-my-arctic-home/blog/57348/':('Story','Climate & Energy','PeopleVsOil'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/copenhagen-fashion-summit-sustainability-recycling-clothes/blog/59376/':('Story','Detox','Fashion'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/danzer-feels-the-bite-as-fsc-show-its-teeth/blog/45230/':('Story','Forests','StandForForests'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/destructive-fishing-campaign-indian-ocean-FAD/blog/56626/':('Story','Ships, Oceans','Esperanza, OceanSanctuaries'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/detox-consumption/blog/53213/':('Story','Detox','Fashion'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/detox-discounters-clothes-PFCs-aldi-lidl-edeka-kaufland/blog/55105/':('Story','Detox','Fashion'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/detox-fashion-brands-toxic-pollution-ranking/blog/56910/':('Story','Detox','Fashion'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/detox-hazardous-chemicals-open-source-research/blog/56040/':('Story','Detox','Fashion'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/detox-its-about-people-not-pfc-pollution/blog/58007/':('Story','Detox','Fashion'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/detox-outdoors-PFC-free-Gore-tex/blog/58655/':('Story','Detox','Fashion'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/detox-outdoors/blog/54001/':('Story','Detox','Fashion'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/detox-PFC-Italy-fashion-style-outdoors/blog/55522/':('Story','Detox','Fashion'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/detox-textile-Indonesia-pollution-court-victory/blog/56615/':('Story','Detox','Fashion'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/DIY-ocean-destruction-solar-energy-ship-tour/blog/56599/':('Story','Ships, Oceans','Esperanza, OceanSanctuaries'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/dont-look-now-but-there-was-just-a-mass-exodus-of-oil-companies-from-US-arctic-waters/blog/56721/':('Story','Climate & Energy','PeopleVsOil'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/earth-danger-save-ourselves-SOS/blog/56782/':('Story','Ships','RainbowWarrior'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/essity-tissue-wiping-away-forests-sweden/blog/60345/':('Story','Forests','StandForForests'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/every-single-piece-of-plastic-ever-made-still-exists/blog/58440/':('Story','Detox','NoPlastics'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/farmers-future-healthy-land/blog/56344/':('Story','Food','FixFood'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/fashion-detox-overconsumption-buying-happiness/blog/59341/':('Story','Detox','Fashion'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/fashion-revolution-sustainable-clothing/blog/59242/':('Story','Detox','Fashion'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/fashion-revolution-who-made-my-clothes/blog/52680/':('Story','Detox','Fashion'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/fashion-without-overconsumption/blog/54843/':('Story','Detox','Fashion'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/fast-fashion-drowning-world-fashion-revolution/blog/56222/':('Story','Detox','Fashion'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/fipronil-contaminated-eggs-scandal-EU/blog/60010/':('Story','Food','FixFood'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/fixing-phone-ifixit-smartphone-repair-guide/blog/57305/':('Story','Detox','RethinkIT'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/Food-for-life-cowspiracy/blog/54404/':('Story','Food','MeatAndDairy'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/food-for-life-eat-less-meat-who/blog/54640/':('Story','Food','MeatAndDairy'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/food-for-life-esperanza-mexico/blog/54540/':('Story','Ships, Food','Esperanza, FixFood'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/food-for-life-europes-pesticide-addiction/blog/54396/':('Story','Food','FixFood'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/food-for-life-I-know-who-grew-it/blog/52857/':('Story','Food','FixFood'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/food-for-life-I-know-who-grew-it/blog/52863/':('Story','Food','FixFood'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/food-for-life-I-know-who-grew-it/blog/52905/':('Story','Food','FixFood'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/food-for-life-organic-farming-bees-spain/blog/55493/':('Story','Food','FixFood'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/food-for-life-world-food-day/blog/54448/':('Story','Food','FixFood, MeatAndDairy'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/fridge-film-sustainable-food-farming/blog/56093/':('Story','Food','FixFood'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/fsc-protecting-intact-forest-landscapes-in-congo/blog/53421/':('Story','Forests','StandForForests'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/fsc-puts-business-interests-first/blog/50381/':('Story','Forests','StandForForests'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/fsc-suspends-three-certificates-of-the-worlds/blog/47684/':('Story','Forests','StandForForests'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/full-marks-for-marks-spencer/blog/42722/':('Story','Detox','Fashion'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/FunnyorDie-Alexander-Skarsgard-True-Blood-Jack-McBrayer-30Rock-savethearctic/blog/54815/':('Story','Climate & Energy','PeopleVsOil'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/future-of-food-iPES-sustainable-agriculture/blog/56793/':('Story','Food','FixFood'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/g-star-commits-to-detox/blog/43827/':('Story','Detox','Fashion'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/ghost-net-retrieval-arctic-sunrise-diving-ocean/blog/56556/':('Story','Ships, Oceans','ArcticSunrise'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/greenpeace-takes-on-vw/blog/44214/':('Story','Climate & Energy','PeopleVsOil'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/herakles-farms-palm-oil-cameroon/blog/54802/':('Story','Forests','StandForForests'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/how-does-eco-Food-affect-your-body/blog/58333/':('Story','Food','FixFood, MeatAndDairy'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/illegal-logging/blog/53531/':('Story','Forests','StandForForests'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/interview-expert-international-polar-bear-day/blog/55663/':('Story','Climate & Energy','PeopleVsOil'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/japans-uniqlo-adds-detox-commitment-to-spring/blog/43593/':('Story','Detox','Fashion'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/jennifer-morgan-melting-arctic-ice-protect-what-you-love/blog/56900/':('Story','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/join-the-food-movement/blog/51901/':('Story','Food','FixFood'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/krill-gotten-gains-to-fund-antarctic-research/blog/52187/':('Story','Oceans','OceanSanctuaries'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/lego-awesome-video/blog/49850/':('Story','Climate & Energy','PeopleVsOil'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/license-to-krill/blog/60637/':('Story','Oceans','OceanSanctuaries'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/lidl-detox/blog/51675/':('Story','Detox','Fashion'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/Ludovico-Einaudi-grand-piano-Arctic-ocean-8-million-voices/blog/56808/':('Story','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/Ludovico-Einaudi-piano-Save-the-Arctic/blog/56899/':('Story','Climate & Energy, Ships','PeopleVsOil, ArcticSunrise'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/McDonalds-Tesco-fishing-industry-to-protect-Arctic/blog/56523/':('Story','Ships, Oceans','ArcticSunrise, OceanSanctuaries'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/meat-free-day-better-eating-challenge-ecological/blog/56731/':('Story','Food','MeatAndDairy'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/meet-the-great-northern-boreal-forest/blog/58198/':('Story','Forests','StandForForests'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/melting-sea-ice-Arctic-sanctuary-urgent-Europe/blog/59028/':('Story','Climate & Energy','PeopleVsOil'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/microbeads-companies-response/blog/57314/':('Story','Detox','NoPlastics'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/microbeads-microplastics-ranking-personal-care-cosmetics/blog/57082/':('Story','Detox, Oceans','NoPlastics'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/microfibers-why-our-clothes-pollute-oceans/blog/58853/':('Story','Detox, Oceans','NoPlastics'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/my-first-time-in-the-arctic/blog/56864/':('Story','Climate & Energy, Ships','PeopleVsOil, ArcticSunrise'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/Nestle-PepsiCo-McDonalds-suppliers-consumers-forest-problem/blog/58866/':('Story','Forests','StandForForests'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/new-chapter-arctic-oil/blog/56684/':('Story','Climate & Energy','PeopleVsOil'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/new-years-plastic-5-simple-recycle/blog/55244/':('Story','Detox','NoPlastics'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/north-face-mammut-pfc-pollution/blog/55452/':('Story','Detox','Fashion'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/NPE-toxic-chemical-banned-EU-textile/blog/53582/':('Story','Detox','Fashion'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/ocean-sanctuaries-biodiversity-protection/blog/59087/':('Story','Oceans','OceanSanctuaries'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/one-phone-call-could-savethegalaxy/blog/58063/':('Story','Detox','RethinkIT'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/OSPAR-UN-ocean-sanctuary-Arctic-protection/blog/56091/':('Story','Climate & Energy, Oceans','PeopleVsOil, OceanSanctuaries'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/overconsumption-plastics-story-of-a-spoon/blog/54433/':('Story','Detox','NoPlastics'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/overfishing-illegal-fishing-west-africa-beauty-greenpeace-ship/blog/59313/':('Story','Ships, Oceans, Food','Esperanza, OceanSanctuaries, FixFood'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/overfishing-thai-union-protest-esperanza-indian-ocean/blog/56555/':('Story','Ships, Oceans','Esperanza, OceanSanctuaries'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/people-power-international-day-of-forests-protection/blog/55922/':('Story','Forests','StandForForests'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/pesticides-are-not-needed-to-feed-the-world-u/blog/59160/':('Story','Food','FixFood'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/pesticides-food-safety-reform-Shanghai-china/blog/57848/':('Story','Food','FixFood'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/protect-forest-free-speech-voice-whatsapp-message/blog/59473/':('Story','Forests','OurVoicesAreVital, StandForForests'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/protecting-antarctica-the-heart-of-the-ocean/blog/40529/':('Story','Oceans','OceanSanctuaries'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/protecting-what-protects-us/blog/58177/':('Story','Forests','StandForForests'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/Rainbow-Warrior-bombing-apology/blog/54003/':('Story','Ships','RainbowWarrior'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/rainbow-warrior-change-tuna-transhipment/blog/53914/':('Story','Ships, Oceans','RainbowWarrior, OceanSanctuaries'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/reindeer-nowhere-to-run-indigenous-Russia-UN/blog/58970/':('Story','Climate & Energy','PeopleVsOil'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/report-hazardous-chemicals-outdoor-gear/blog/55379/':('Story','Detox','Fashion'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/resolute-free-speech-authors-speak-out/blog/59550/':('Story','Forests','OurVoicesAreVital'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/RiteAid-wrong-choice/blog/53630/':('Story','Forests','StandForForests'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/russia-anthrax-reindeer-indigenous/blog/57511/':('Story','Climate & Energy','PeopleVsOil'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/Russia-Dvinsky-forest-protect-biodiversity-climate/blog/58269/':('Story','Forests','StandForForests'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/samsung-can-you-hear-us/blog/58139/':('Story','Detox','RethinkIT'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/Samsung-Galaxy-Note-7-ewaste-trash-recall/blog/57889/':('Story','Detox','RethinkIT'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/Samsung-Galaxy-Note7-ewaste-recall/blog/57923/':('Story','Detox','RethinkIT'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/save-the-arctic-art/blog/56147/':('Story','Climate & Energy','PeopleVsOil'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/save-the-arctic-lego-dumps-shell/blog/50917/':('Story','Climate & Energy','PeopleVsOil'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/save-the-arctic-shell-abandons-arctic-drilling/blog/54263/':('Story','Climate & Energy','PeopleVsOil'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/save-the-arctic/blog/51720/':('Story','Climate & Energy','PeopleVsOil'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/save-the-arctic/blog/52521/':('Story','Ships, Climate & Energy','Esperanza, PeopleVsOil'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/save-the-bees-goodbye-to-fipronil-EU/blog/60346/':('Story','Food','FixFood'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/saving-dvinsky-forest-Russia-FSC/blog/59319/':('Story','Forests','StandForForests'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/seeing-is-believing-growing-Food-for-people-Cuba-agroecology/blog/58480/':('Story','Food','FixFood'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/silent-spring-bird-extinction-rex-weyler/blog/59580/':('Story','Forests','StandForForests'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/slapp-corporate-lawsuits-free-speech-resolute/blog/59352/':('Story','Forests','OurVoicesAreVital'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/smarphones-planet-toxic-waste/blog/58828/':('Story','Detox','RethinkIT'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/StandForForests/blog/52135/':('Story','Forests','StandForForests'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/support-ocean-sanctuaries-whale-sharks/blog/53928/':('Story','Oceans','OceanSanctuaries'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/tackle-thai-union-destructive-FAD-fishing-this-world-tuna-day/blog/56356/':('Story','Ships, Oceans','Esperanza, OceanSanctuaries'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/thai-union-makes-sustainable-commitment/blog/59825/':('Story','Oceans, Food','OceanSanctuaries, FixFood'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/thai-union-needs-lead-seafood-industry-cats/blog/59529/':('Story','Oceans, Food','OceanSanctuaries, FixFood'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/the-arctic-sunrise-norway-coast-guard-arrest-oil-drilling/blog/60052/':('Story','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/the-battle-against-destructive-fishing-thai-union/blog/56479/':('Story','Ships, Oceans','Esperanza, OceanSanctuaries'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/the-lengths-illegal-wood-will-travel/blog/45814/':('Story','Forests','StandForForests'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/The-People-vs-Arctic-Oil-climate-justice-lawsuit/blog/57742/':('Story','Climate & Energy','PeopleVsOil'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/the-truth-on-congo-basin-deforestation/blog/46065/':('Story','Forests','StandForForests'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/tropical-deforestation/blog/51830/':('Story','Food, Forests','FixFood, StandForForests'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/vaquitas-mexico-findings/blog/53631/':('Story','Ships','Esperanza'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/vegetarian-tips-for-going-meat-free/blog/56351/':('Story','Food','MeatAndDairy'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/victory-massive-new-ocean-sanctuary-establish/blog/57859/':('Story','Oceans','OceanSanctuaries'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/we-speak-for-the-trees/blog/59607/':('Story','Forests','OurVoicesAreVital'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/west-africa-greenpeace-ship-shark-fins-illegal-fishing/blog/59273/':('Story','Ships, Oceans, Food','Esperanza, OceanSanctuaries, FixFood'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/west-africa-oceans-fish-our-responsibility/blog/58818/':('Story','Ships, Oceans','Esperanza, OceanSanctuaries'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/what-happened-when-we-demanded-that-publisher/blog/59680/':('Story','Forests','OurVoicesAreVital'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/what-happens-in-the-arctic-affects-us-all/blog/56675/':('Story','Climate & Energy','PeopleVsOil'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/which-country-is-most-likely-to-repair-their-/blog/57276/':('Story','Detox','RethinkIT'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/why-we-are-taking-arctic-oil-to-court/blog/57749/':('Story','Climate & Energy','PeopleVsOil'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/you-did-it-samsung-will-finally-recycle-milli/blog/59045/':('Story','Detox','RethinkIT'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/your-voice-arctic-sanctuary-OSPAR-nordic-countries/blog/56636/':('Story','Climate & Energy, Oceans','PeopleVsOil, OceanSanctuaries'),
'http://www.greenpeace.org/international/en/news/Blogs/makingwaves/zero-deforestation/blog/54940/':('Story','Forests','StandForForests'),
'http://www.greenpeace.org/international/en/news/Blogs/nuclear-reaction/marshall-islands-icj-nuclear-lawsuit/blog/55905/':('Story','Ships','RainbowWarrior'),
'http://www.greenpeace.org/international/en/news/Blogs/nuclear-reaction/nuclear-testing-not-path-to-security-peace/blog/57372/':('Story','Ships','RainbowWarrior'),
'http://www.greenpeace.org/international/en/news/features/A-Monstrous-Mess-toxic-water-pollution-in-China/':('Feature','Detox','Fashion'),
'http://www.greenpeace.org/international/en/news/features/Levis-shapes-up-to-become-a-Detox-leader/':('Feature','Detox','Fashion'),
'http://www.greenpeace.org/international/en/news/features/Primark-joins-the-5-Step-Detox-Programme/':('Feature','Detox','Fashion'),
'http://www.greenpeace.org/international/en/news/features/Zara-commits-to-go-toxic-free/':('Feature','Detox','Fashion'),
'http://www.greenpeace.org/international/en/press/releases/2013/100-days-after-they-were-seized-Arctic-30-are-leaving-Russia-/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2013/Australian-Arctic-30-activist-Colin-Russell-bailed-after-71-days-detention/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2013/Dutch-government-finalises-bank-guarantee-for-release-of-Arctic-30/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2013/Eyes-of-Arctic-30-turn-to-Russian-parliament-on-eve-of-amnesty-vote/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2013/First-case-dropped-against-Arctic-30-activist-exit-visa-sought/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2013/First-of-the-Arctic-30-get-visas-to-leave-Russia/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2013/First-of-the-Arctic-30-leaves-Russia/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2013/Four-more-Arctic-30-detainees-released-from-Russian-prison/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2013/Gazprom-begins-first-production-at-Arctic-30-oil-platform/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2013/Good-news-on-Christmas-Day-for-Arctic-301/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2013/Greenpeace-Current-draft-of-Russian-amnesty-does-not-include-Arctic-30/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2013/Greenpeace-International-welcomes-Tribunal-ruling-ordering-Russia-to-release-Arctic-30/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2013/Last-foreign-Arctic-30-activist-leaves-Russia/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2013/Lawyers-apply-for-Russian-exit-visas-for-Arctic-30/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2013/Murmansk-court-rejects-appeal-over-arrest-of-ship-Arctic-Sunrise/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2013/Russian-authorities-say-Arctic-30-cannot-return-home-/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2013/Russian-parliament-votes-for-amnesty-for-Arctic-30/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2013/UKs-Phil-Ball-released-29th-Arctic-30-detainee-to-be-freed-from-prison/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2013/UPDATE-25-foreigners-among-Arctic-30-leave-Russia/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2014/Arctic-30-jailed-in-Russia-to-take-case-to-European-Courtof-Human-Rights/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2014/Arctic-Sunrise-release-new-petition/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2014/Emma-Thompson-and-daughter-join-Greenpeace-ship-on-voyage-to-protect-the-Arctic/':('Press release','Climate & Energy, Ships','PeopleVsOil, ArcticSunrise'),
'http://www.greenpeace.org/international/en/press/releases/2014/Greenpeace-activist-hospitalised-after-Spanish-Navy-rams-boats-in-oil-protest/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2014/Greenpeace-ship-Arctic-Sunrise-departs-Russian-port-after-ten-months-in-custody/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2014/Greenpeace-ship-Arctic-Sunrise-detained-in-Spain-following-oil-protest/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2014/Greenpeace-ship-Arctic-Sunrise-welcomed-home-by-Arctic-30/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2014/Nationwide-demonstrations-in-Italy-joins-Greenpeace-oil-rig-occupation-in-Sicily/':('Press release','Ships, Climate & Energy','RainbowWarrior, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2015/Greenpeace-activist-scales-coal-ship-off-the-coast-of-Helsinki/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2015/Greenpeace-climbers-leave-Arctic-oil-drilling-rig-/':('Press release','Ships, Climate & Energy','Esperanza, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2015/Greenpeace-demands-scale-up-of-ecological-farming/':('Press release','Food','FixFood'),
'http://www.greenpeace.org/international/en/press/releases/2015/Greenpeace-Rainbow-Warrior-brings-relief-to-Vanuatus-stranded-islands/':('Press release','Ships','RainbowWarrior'),
'http://www.greenpeace.org/international/en/press/releases/2015/Greenpeace-report-reveals-farmers-are-the-most-vulnerable-to-health-risks-from-pesticides/':('Press release','Food','FixFood'),
'http://www.greenpeace.org/international/en/press/releases/2015/Injured-Greenpeace-activist-faces-Spanish-navy-culprits-who-threaten-prosecution-under-piracy-chapter-of-criminal-code/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2015/New-evidence-shows-Chinese-West-African-governments-must-rein-in-rogue-fishing-fleet/':('Press release','Oceans','OceanSanctuaries, FixFood'),
'http://www.greenpeace.org/international/en/press/releases/2015/Rainbow-Warrior-Marks-30th-Anniversary-of-Bombing-with-Action-to-Save-the-Great-Barrier-Reef/':('Press release','Ships, Oceans','RainbowWarrior, OceanSanctuaries'),
'http://www.greenpeace.org/international/en/press/releases/2015/Russian-government-broke-international-law-in-Greenpeace-Arctic-30-case---tribunal1/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2016/Black-Friday-Greenpeace-calls-timeout-for-fast-fashion/':('Press release','Detox','Fashion'),
'http://www.greenpeace.org/international/en/press/releases/2016/Esperanza-protest-overfishing-Thai-Union/':('Press release','Ships, Food','Esperanza, FixFood'),
'http://www.greenpeace.org/international/en/press/releases/2016/extreme-weather-arctic-climate-change-to-effect-of-climate-change-press-release/':('Press release','Climate & Energy','PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2016/Greenpeace-Nike-Esprit-Victorias-Secret-and-LiNing-fail-toxic-free-fashion-ranking/':('Press release','Detox','Fashion'),
'http://www.greenpeace.org/international/en/press/releases/2016/Greenpeace-ship-Esperanza-targets-Thai-Unions-destructive-fishing-in-Indian-Ocean/':('Press release','Ships, Food','Esperanza, FixFood'),
'http://www.greenpeace.org/international/en/press/releases/2016/Italys-fashion-supply-chain-Detox-hazardous-chemicals/':('Press release','Detox','Fashion'),
'http://www.greenpeace.org/international/en/press/releases/2016/Ludovico-Einaudi-live-concert-Arctic-Ocean/':('Press release','Climate & Energy, Ships','PeopleVsOil, ArcticSunrise'),
'http://www.greenpeace.org/international/en/press/releases/2016/McDonalds-seafood-Arctic-protection-overfishing/':('Press release','Oceans, Food','OceanSanctuaries, FixFood'),
'http://www.greenpeace.org/international/en/press/releases/2016/Nobel-laureates-sign-letter-on-Greenpeace-Golden-rice-position---reactive-statement/':('Press release','Food','FixFood'),
'http://www.greenpeace.org/international/en/press/releases/2016/overfishing-consumer-brands-Arctic-destruction/':('Press release','Oceans, Food','OceanSanctuaries, FixFood'),
'http://www.greenpeace.org/international/en/press/releases/2016/Personal-care-products-may-still-be-polluting-oceans-despite-promises-by-companies-says-Greenpeace/':('Press release','Detox, Oceans','NoPlastics'),
'http://www.greenpeace.org/international/en/press/releases/2016/Rainbow-Warrior-Lebanon-solar-unity-Mediterranean/':('Press release','Ships, Climate & Energy','RainbowWarrior'),
'http://www.greenpeace.org/international/en/press/releases/2016/Research-shows-switching-to-organic-food-can-reduce-pesticide-levels-in-urine/':('Press release','Food','FixFood'),
'http://www.greenpeace.org/international/en/press/releases/2016/save-Great-Northern-Forest-Convention-Biological-Diversity/':('Press release','Forests','StandForForests'),
'http://www.greenpeace.org/international/en/press/releases/2017/activists-released-after-being-arrested-for-protesting-against-oil-drillings-in-Norway/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2017/Apple-Samsung-products-among-least-repairable-Greenpeace-assessment-of-tech-brands/':('Press release','Detox','RethinkIT'),
'http://www.greenpeace.org/international/en/press/releases/2017/cca-campaign-Antarctic-nations-fall-short-on-marine-protection/':('Press release','Oceans','OceanSanctuaries'),
'http://www.greenpeace.org/international/en/press/releases/2017/Global-movement-unites-against-Norwegian-oil/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2017/Global-protests-push-Samsung-to-finally-recycle-Galaxy-Note-7---Greenpeace/':('Press release','Detox','RethinkIT'),
'http://www.greenpeace.org/international/en/press/releases/2017/Gore-hazardous-PFCs-outdoor-gear-pledge/':('Press release','Detox','Fashion'),
'http://www.greenpeace.org/international/en/press/releases/2017/Greenpeace-activists-call-on-G20-to-act-for-plastic-free-oceans/':('Press release','Detox, Oceans','NoPlastics'),
'http://www.greenpeace.org/international/en/press/releases/2017/Greenpeace-activists-confront-Norwegian-governments-Arctic-oil-drilling-site1/':('Press release','Climate & Energy, Ships','PeopleVsOil, ArcticSunrise'),
'http://www.greenpeace.org/international/en/press/releases/2017/Greenpeace-as-part-of-Break-Free-From-Plastic-presents-a-new-way-of-exposing-plastic-pollution-offenders/':('Press release','Detox','NoPlastics'),
'http://www.greenpeace.org/international/en/press/releases/2017/Greenpeace-captures-first-underwater-images-of-Amazon-Coral-Reef/':('Press release','Ships','Esperanza'),
'http://www.greenpeace.org/international/en/press/releases/2017/Justice-served-in-Greenpeace-Arctic-30-case-as-Russia-ordered-to-pay-the-Netherlands-54-million-in-damages/':('Press release','Climate & Energy, Ships','PeopleVsOil, ArcticSunrise'),
'http://www.greenpeace.org/international/en/press/releases/2017/logging-Dvinsky-Forest-Russia-press-release/':('Press release','Forests','StandForForests'),
'http://www.greenpeace.org/international/en/press/releases/2017/Lucy-Lawless-Norwegian-oil-arctic-protest/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2017/Mars-Nestle-commit-to-clean-up-pet-food-supply-chains-increasing-pressure-on-Thai-Union-to-act/':('Press release','Oceans, Food','OceanSanctuaries, FixFood'),
'http://www.greenpeace.org/international/en/press/releases/2017/Nestle-Unilever-PG-among-worst-offenders-for-plastic-pollution-in-Philippines-in-beach-audit/':('Press release','Detox, Oceans','NoPlastics'),
'http://www.greenpeace.org/international/en/press/releases/2017/New-report-breaks-the-myth-of-fast-fashions-so-called-circular-economy---Greenpeace/':('Press release','Detox','Fashion'),
'http://www.greenpeace.org/international/en/press/releases/2017/Oil-exploration-blocked-in-watershed-Supreme-Court-of-Canada-ruling-on-Indigenous-rights-/':('Press release','Oceans','PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2017/Peaceful-protest-against-Arctic-drilling-unlawfully-ended-by-Norwegian-authorities/':('Press release','Ships, Climate & Energy','ArcticSunrise, PeopleVsOil'),
'http://www.greenpeace.org/international/en/press/releases/2017/Rainbow-Warrior-arrives-in-Cuba-to-document-the-islands-eco-food-system/':('Press release','Ships, Food','RainbowWarrior, FixFood'),
'http://www.greenpeace.org/international/en/press/releases/2017/Restless-compulsive-and-unfulfilled---Greenpeace-survey-offers-insights-into-fashion-shoppers-feelings/':('Press release','Detox','Fashion'),
'http://www.greenpeace.org/international/en/press/releases/2017/Samsung-Huawei-and-Amazon-failing-Greenpeaces-green-electronics-guide/':('Press release','Detox, Climate & Energy','RethinkIT'),
'http://www.greenpeace.org/international/en/press/releases/2017/Smartphones-leaving-disastrous-environmental-footprint-warns-new-Greenpeace-report-/':('Press release','Detox','RethinkIT'),
'http://www.greenpeace.org/international/en/press/releases/2017/Tesco-publicly-commits-to-Detox-its-textile-production-as-retailers-start-tackling-throw-away-fashion/':('Press release','Detox','Fashion'),
'http://www.greenpeace.org/international/en/press/releases/2017/Thai-Union-Commits-to-More-Sustainable-Socially-Responsible-Seafood/':('Press release','Oceans, Food','OceanSanctuaries, FixFood'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Agriculture/Bees-in-Decline/':('Publication','Food','FixFood'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Agriculture/Ecological-Livestock/':('Publication','Food','MeatAndDairy'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Agriculture/Europes-Pesticide-Addiction/':('Publication','Food','FixFood'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Agriculture/Food-and-Farming-Vision/':('Publication','Food','FixFood, MeatAndDairy'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Agriculture/Pesticides-and-our-Health/':('Publication','Food','FixFood'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Agriculture/Plan-Bee-Living-Without-Pesticides/':('Publication','Food','FixFood'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Agriculture/Smart-Breeding/':('Publication','Food','FixFood'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Agriculture/The-Bees-Burden/':('Publication','Food','FixFood'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Agriculture/The-Environmental-Risks-of-neonicotinoid-pesticides/':('Publication','Food','FixFood'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Agriculture/Twenty-Years-of-Failure/':('Publication','Food','FixFood'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Climate-Reports/Apple-Clean-Energy-Road-Map/':('Publication','Detox, Climate & Energy','RethinkIT'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Climate-Reports/clicking-clean-2015/':('Publication','Detox, Climate & Energy','RethinkIT'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Climate-Reports/clicking-clean-2017/':('Publication','Detox, Climate & Energy','RethinkIT'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Climate-Reports/clickingclean/':('Publication','Detox, Climate & Energy','RethinkIT'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Climate-Reports/Climate-Change-Impacts-on-Arctic-Wildlife/':('Publication','Climate & Energy','PeopleVsOil'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Climate-Reports/Cool-IT-Leaderboard/':('Publication','Detox, Climate & Energy','RethinkIT'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Climate-Reports/How-Clean-is-Your-Cloud/':('Publication','Detox, Climate & Energy','RethinkIT'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Climate-Reports/This-Far-No-Further/':('Publication','Climate & Energy','PeopleVsOil'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Forests-Reports/Clearcutting-Free-Speech/':('Publication','Forests','OurVoicesAreVital'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Forests-Reports/Eye-on-the-Taiga/':('Publication','Forests','StandForForests'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Forests-Reports/FSC-Case-Studies/':('Publication','Forests','StandForForests'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Forests-Reports/Wiping-Away-the-Boreal/':('Publication','Forests','StandForForests'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Genetic-engineering/Golden-Illusion/':('Publication','Food','FixFood'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Oceans-Reports/arctic-sanctuary/':('Publication','Oceans','OceanSanctuaries'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Oceans-Reports/deep-seabed-mining/':('Publication','Oceans','OceanSanctuaries'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Oceans-Reports/High-Seas-Agreement/':('Publication','Oceans','OceanSanctuaries'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Oceans-Reports/Made-in-Taiwan/':('Publication','Oceans','OceanSanctuaries'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Oceans-Reports/Oceans-in-the-Balance/':('Publication','Oceans','OceanSanctuaries'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Toxics-reports/A-Little-Story-about-a-Fashionable-Lie/':('Publication','Detox','Fashion'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Toxics-reports/A-Little-Story-About-the-Monsters-In-Your-Closet/':('Publication','Detox','Fashion'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Toxics-reports/After-the-Binge-the-Hangover/':('Publication','Detox','Fashion'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Toxics-reports/Big-Fashion-Stitch-Up/':('Publication','Detox','Fashion'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Toxics-reports/detox-football/':('Publication','Detox','Fashion'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Toxics-reports/Dirty-Laundry-Reloaded/':('Publication','Detox','Fashion'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Toxics-reports/Fashion-at-the-Crossroads/':('Publication','Detox','Fashion'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Toxics-reports/Footprints-in-the-Snow/':('Publication','Detox','Fashion'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Toxics-reports/Green-Gadgets/':('Publication','Detox, Climate & Energy','RethinkIT'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Toxics-reports/Hidden-in-Plain-Sight/':('Publication','Detox','Fashion'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Toxics-reports/Leaving-Traces/':('Publication','Detox','Fashion'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Toxics-reports/PFC-Pollution-Hotspots/':('Publication','Detox','Fashion'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Toxics-reports/PFC-Revolution-in-Outdoor-Sector/':('Publication','Detox','Fashion'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Toxics-reports/Polluting-Paradise/':('Publication','Detox','Fashion'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Toxics-reports/Putting-Pollution-on-Parade/':('Publication','Detox','Fashion'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Toxics-reports/The-Toxic-Truth/':('Publication','Detox','Fashion'),
'http://www.greenpeace.org/international/en/publications/Campaign-reports/Toxics-reports/Toxic-Threads-Under-Wraps/':('Publication','Detox','Fashion'),
'http://www.greenpeace.org/international/en/publications/reports/Defining-Ecological-Farming/':('Publication','Food','FixFood'),
'http://www.greenpeace.org/international/en/publications/reports/Dirty-Laundry-2/':('Publication','Detox','Fashion'),
'http://www.greenpeace.org/international/en/publications/reports/Dirty-Laundry/':('Publication','Detox','Fashion'),
'http://www.greenpeace.org/international/en/publications/reports/Emergency-Oceans-Rescue-Plan/':('Publication','Oceans','OceanSanctuaries'),
'http://www.greenpeace.org/international/en/publications/reports/Hidden-Consequences/':('Publication','Detox','Fashion'),
'http://www.greenpeace.org/international/en/publications/reports/How-dirty-is-your-data/':('Publication','Detox, Climate & Energy','RethinkIT'),
'http://www.greenpeace.org/international/en/publications/reports/make-it-green-cloud-computing/':('Publication','Detox, Climate & Energy','RethinkIT'),
'http://www.greenpeace.org/international/en/publications/reports/med-threats-solutions/':('Publication','Oceans','OceanSanctuaries'),
'http://www.greenpeace.org/international/en/publications/reports/recycling-of-electronic-waste/':('Publication','Detox, Climate & Energy','RethinkIT'),
'http://www.greenpeace.org/international/en/publications/reports/Switching-on-Green-Electronics/':('Publication','Detox, Climate & Energy','RethinkIT'),
'http://www.greenpeace.org/international/en/publications/reports/Towards-green-electronics-Getting-greener-but-not-there-yet/':('Publication','Detox, Climate & Energy','RethinkIT'),
'http://www.greenpeace.org/international/en/publications/reports/toxic-transformers-briefing/':('Publication','Detox, Climate & Energy','RethinkIT')}
        
        for url,data in start_urls.iteritems():
            post_type, categories, tags = data
            if ( post_type=='Story' ):
                request = scrapy.Request(url, callback=self.parse_blog, dont_filter='true')
            elif ( post_type=='Publication' ):
                request = scrapy.Request(url, callback=self.parse_publication, dont_filter='true')
            elif ( post_type=='Press release' or post_type=='Press Release' ):
                request = scrapy.Request(url, callback=self.parse_press, dont_filter='true')
            elif ( post_type=='Feature' ):
                request = scrapy.Request(url, callback=self.parse_feature, dont_filter='true')
            request.meta['categories'] = categories
            request.meta['tags'] = tags
            yield request
    
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
            if lead_text:
                body_text = '<div>' + lead_text + '</div>' + body_text + response.xpath(' //*[@id="content"]/div[4]/div/div[2]/p').extract_first()
        
        yield {
            'type': 'Story',
            'p3_image_gallery': p3_image_gallery,
            #'title': extract_with_css('#content > div.happen-box.article > h1::text'),
            'title': response.xpath('//*[@id="content"]/div[4]/h1/span/text()').extract()[0],
            'subtitle': extract_with_css('div.article h1 span::text'),
            'author': 'Greenpeace International',
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
            'tags': response.meta['tags'],
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
            
        pdfFiles=response.css('div.article a[href$=".pdf"]::attr(href)').extract()
        pdf_files_generated = list()
        for pdf_file in pdfFiles:
            print pdf_file
            if (pdf_file.startswith('/')):
                pdf_file = pdf_file.replace('/','http://www.greenpeace.org/',1)
                print pdf_file
            pdf_files_generated.append(pdf_file)
            print pdf_files_generated

        date_field = response.css('div.news-list .caption::text').re_first(r' - \s*(.*)')
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

        yield {
            'type': 'Story',
            'p3_image_gallery': p3_image_gallery,
            'title': extract_with_css('div.news-list h1::text'),
            'subtitle': '',
            'author': response.xpath('string(//div[@class="news-list"]/ul/li/*/*/span[@class="caption"]/span[@class="green1"]/strong)').extract()[0],
            'date': date_field,
            #'lead': extract_with_css('div.news-list div.post-content *:first-child strong::text'),
            'lead': response.xpath('string(//div[@class="news-list"]/ul/li/div[@class="post-content"]/div//*[self::p or self::h3 or self::h2][1])').extract()[0],
            'categories': response.meta['categories'],
            'text':  body_text,
            'imagesA': imagesA_generated,
            #'imagesB': response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img[not(ancestor::a)]/@src').extract(), #don't import image if there's an a tag around it
            'imagesB': imagesB_generated,
            'imagesC': response.xpath('//div[@class="gallery"]//div[@class="img-nav"]//a/@rel').extract(), # Galleries (horrible html)
            'pdfFiles': pdf_files_generated,
            'tags': response.meta['tags'],
            'url': response.url,
        }

    def parse_press(self, response):

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

        lead_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[1]/div/text()').extract()[0]
        body_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[2]').extract()[0]
        if body_text:
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.org/').replace('href="/', 'href="http://www.greenpeace.org/')
            body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            if lead_text:
                body_text = '<div>' + lead_text + '</div>' + body_text + response.xpath(' //*[@id="content"]/div[4]/div/div[2]/p').extract_first()
            
        yield {
            'type': 'Press Release',
            'p3_image_gallery': p3_image_gallery,
            'title': extract_with_css('div.article h1 span::text'),
            'subtitle': '',
            'author': 'Greenpeace International',
            #'date': response.css('#content > div.happen-box.article > div > div.text > span').re_first(r' - \s*(.*)'),
            'date': dateutil.parser.parse(response.xpath('string(//*[@id="content"]/div[4]/div/div[2]/span)').extract()[0].replace('Press release - ', '')),
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
            'tags': response.meta['tags'],
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
                body_text = '<div>' + lead_text + '</div>' + body_text
        
        lead_text
        
        if body_text:
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.org/').replace('href="/', 'href="http://www.greenpeace.org/')
            body_text = body_text.replace('<span class="btn-open">zoom</span>', '')

        yield {
            'type': 'Publication',
            'p3_image_gallery': p3_image_gallery,
            'title': extract_with_css('div.article h1 span::text'),
            'subtitle': extract_with_css('div.article h2 span::text'),
            'author': 'Greenpeace International',
            'date': date_field,
            #'lead': extract_with_css('div.news-list div.post-content *:first-child strong::text'),
            'lead': extract_with_css('#content > div.happen-box.article > div > div.text > div.leader > div'),
            'categories': response.meta['categories'],
            'text': body_text,
            'imagesA': imagesA_generated,
            #'imagesB': response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img[not(ancestor::a)]/@src').extract(), #don't import image if there's an a tag around it
            'imagesB': imagesB_generated,
            'imagesC': response.xpath('//div[@class="gallery"]//div[@class="img-nav"]//a/@rel').extract(), # Galleries (horrible html)
            'pdfFiles': pdf_files_generated,
            'tags': response.meta['tags'],
            'url': response.url,
        }