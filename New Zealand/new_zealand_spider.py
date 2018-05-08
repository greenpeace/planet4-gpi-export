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
        'FEED_URI': 'gpnz_production_v3_1.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def start_requests(self):

        start_urls = {
            # Story
            # - 1st batch
            'http://www.greenpeace.org/new-zealand/en/blog/life-aboard-the-stop-deep-sea-oil-flotilla/blog/34474/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/fonterra-embarrasses-the-government-over-palm/blog/33265/':('Story','Protect','Forests', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/petition-sign-the-deep-water-oil-drilling-in-/blog/24877/':('Story','Resist','Oil&Gas', 'Oceans', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/remember-the-rainbow-warrior-and-the-marshall/blog/24895/':('Story','Greenpeace','AboutUs', '', 'Migrate'),

            # - 2nd batch
            'http://www.greenpeace.org/new-zealand/en/blog/tiama-joins-the-flotilla-to-stop-deep-sea-oil/blog/34473/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/iwi-fishing-boat-disrupts-oil-survey-ship/blog/34408/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/stopping-deep-sea-oil-vanessas-log-12042011/blog/34252/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/stopping-deep-sea-oil-vanessas-log/blog/34249/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/vanessas-blog-seismic-events-at-sea/blog/34156/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/jefs-blog-toward-whangaparoa/blog/34155/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/fighting-spirit-at-flotilla-send-off/blog/33965/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/brownlee-and-oil-relics-of-a-dying-age/blog/24866/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/are-the-governments-deep-water-oil-plans-runn/blog/35784/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/busting-the-oil-and-gas-industrys-alternative/blog/61405/':('Story','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/rena-oil-spill-an-unfortunate-lesson/blog/37226/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/the-oil-is-less-obvious-but-the-problem-is-sp/blog/37351/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/rena-oil-spill-could-make-deep-sea-oil-drilli/blog/37303/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/toxic-rena-oil-washes-ashore/blog/37291/':('Story','Resist','Oil&Gas', '', 'Migrate'),

            # - 3rd batch
            'http://www.greenpeace.org/new-zealand/en/blog/telling-the-oil-companies-the-truth/blog/38153/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/enthusiasm-for-oil-requires-cognitive-shut-do/blog/38751/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/eat-it-up-monsanto/blog/39016/':('Story','Resist','Food&Farming', 'Health', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/top-10-reasons-why-arctic-oil-drilling-is-a-r/blog/39288/':('Story','Resist','Oil&Gas', 'Oceans', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/we-can-enjoy-a-good-life-without-extreme-oil-/blog/39520/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/deep-sea-oil-still-a-thousand-times-worse/blog/39869/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/taking-the-deep-sea-oil-battle-to-the-high-co/blog/40803/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/shellfail-inside-story-greenpeace-yes-men/blog/40876/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/greenpeace-uncovers-gazproms-expired-oil-spil/blog/41765/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/mauis-dolphin-shame/blog/42365/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/oily-people-point-to-a-dirty-reality/blog/24905/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/a-new-dawn/blog/43602/':('Greenpeace','Resist','RainbowWarrior', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/captain-of-the-most-famous-ship-in-the-world/blog/43626/':('Greenpeace','Resist','RainbowWarrior', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/snake-oil/blog/43669/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/when-big-oil-comes-to-town/blog/43713/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/an-indivisible-link/blog/43757/':('Story','Resist','Oil&Gas', 'RainbowWarrior', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/whale-oil/blog/43842/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/too-precious-to-risk/blog/43838/':('Story','Resist','Oil&Gas', 'Oceans', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/we-did-it-for-the-future/blog/43904/':('Story','Resist','Oil&Gas', 'Oceans', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/getting-used-to-the-new-normal/blog/44295/':('Story','Resist','Food&Farming', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/pull-the-other-one-sealord/blog/44546/':('Story','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/government-shows-foreign-oil-companies-deep-s/blog/44791/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/john-key-and-the-oil-cowboys/blog/45014/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/sealords-change-of-tuna/blog/45349/':('Story','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/an-eyewitness-account-of-the-gulf-of-mexico-d/blog/45456/':('Story','Resist','Oil&Gas', 'Oceans', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/oil-slick-politics/blog/45476/':('Story','Resist','Oil&Gas', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/new-zealand-sits-idly-by-as-the-mauis-dolphin/blog/45867/':('Story','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/its-simple-simon/blog/45960/':('Story','Resist','Oil&Gas', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/this-really-is-the-prime-minister-of-new-zeal/blog/46070/':('Story','Resist','Oil&Gas', 'Coal', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/our-charitable-status-legal-marathon/blog/46119/':('Story','Greenpeace','AboutUs', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/i-was-targeted-by-terrorists-and-i-dont-need-/blog/46305/':('Story','Resist','Freedom', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/youtube-takes-down-greenpeace-shell-video/blog/46402/':('Story','Resist','Oil&Gas', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/deep-sea-oil-and-gas-drilling-not-in-new-zeal/blog/46639/':('Story','Resist','Oil&Gas', 'Oceans', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/a-letter-of-thanks-from-david-haussmann-detai/blog/47012/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/oil-on-the-sea-of-our-souls-the-delusion-of-d/blog/47133/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/deep-sea-oil-drilling-in-new-zealands-waters-/blog/47132/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/government-too-cosy-for-the-truth-on-oil-risk/blog/47201/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/seabirds-and-oil-spills-a-cautionary-tale/blog/47203/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/new-zealand-at-risk-of-becoming-the-next-oil-/blog/47263/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/where-our-leaders-fail-us-new-zealand-oil-and/blog/47354/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/the-oil-free-seas-flotilla-and-greenpeace/blog/47315/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/standing-up-against-dangerous-oil-drilling-fr/blog/47399/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/banners-on-the-beach-for-oil-free-seas/blog/47501/':('Story','Resist','Oil&Gas', 'Oceans', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/tide-turns-on-keys-oil-drilling-plans/blog/47603/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/high-noon-at-the-high-court/blog/47656/':('Story','Resist','Oil&Gas', 'Oceans', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/banners-on-the-beach-oily-people-at-new-brigh/blog/48341/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/photos-from-the-orangutan-cemetery/blog/48396/':('Story','Protect','Oil&Gas', 'Forests', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/the-christchurch-floods/blog/48408/':('Story','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/anadarko-springs-a-leak-and-spills-the-beans-/blog/48477/':('Story','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/stop-the-tppa-join-the-nationwide-day-of-acti/blog/48589/':('Story','Resist','Freedom', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/nz-govt-energy-policy-fiscal-idiocy-and-atmos/blog/48765/':('Story','Protect','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/sack-simon-the-forgotten-forest-is-a-bridge-t/blog/48848/':('Story','Protect','Forests', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/tuna-the-quick-species-guide/blog/49113/':('Story','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/bridges-admits-his-all-of-the-above-energy-ap/blog/48610/':('Story','Resist','Oil&Gas', 'Renewables', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/is-the-green-party-banking-on-an-oily-future/blog/49222/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/a-frosty-reception-for-john-keys-budget-from-/blog/49248/':('Story','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/from-truffle-to-light-crude-oil-doesnt-come-c/blog/50119/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/greenpeaces-supreme-court-win-made-new-zealan/blog/50202/':('Story','Greenpeace','AboutUs', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/on-the-cusp/blog/50569/':('Story','Protect','Oceans', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/at-the-end-of-the-day-decision-2014/blog/50731/':('Story','Protect','Climate', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/auckland-march-to-stop-deep-sea-oil/blog/50782/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/march-to-stopdeepseaoil-and-stopstatoil/blog/50808/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/a-week-of-protest-against-deep-sea-oil/blog/50847/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/the-berlin-wall-of-oil-begins-to-crumble/blog/50884/':('Story','Transform','Oil&Gas', 'Renewables', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/shell-oil-cowboys-caught-illegal-drilling-in-/blog/51060/':('Story','Resist','Oil&Gas', 'Oceans', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/7-solar-wonders-of-the-world/blog/51105/':('Story','Transform','Renewables', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/statoil-licensed-to-spill/blog/51645/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/seismic-testing-stopped-in-norway-but-coming-/blog/50342/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/statoils-deafening-silence/blog/51680/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/deepwater-drilling-in-new-zealand-in-deep-tro/blog/51865/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/statoil-go-home/blog/52063/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/a-big-swing-against-deep-sea-drilling-for-auc/blog/52045/':('Story','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/climate-change-minister-reveals-hes-clueless/blog/53019/':('Story','Protect','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/realclimateaction/blog/53338/':('Story','Resist','Climate', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/breaking-activists-stop-shell-vessel-as-it-at/blog/53637/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/huntly-switch-to-clean-energy-leaves-soot-on-/blog/53714/':('Story','Tranform','Renewables', 'Coal', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/statoil-heading-for-whangarei-with-greenwash-/blog/53852/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/russel-norman-to-lead-greenpeace-new-zealand/blog/54040/':('Story','Greenpeace','AboutUs', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/block-the-offer-to-stop-deep-sea-oil/blog/54107/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/living-on-the-brink-what-happens-if-all-the-s/blog/54139/':('Story','Protect','Oceans', 'RainbowWarrior', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/5-reasons-not-to-drill-for-deep-sea-oil-in-nz/blog/54479/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/why-i-chained-myself-to-a-government-oil-expl/blog/54853/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/key-gets-ready-to-give-away-our-ocean-to-oil-/blog/55043/':('Story','Resist','Oil&Gas', 'Oceans', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/new-zealand-not-john-keyland/blog/55482/':('Story','Resist','Oil&Gas', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/palm-oil-whos-still-trashing-forests/blog/55725/':('Story','Protect','Forests', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/peaceful-civil-disobedience-for-realclimateac/blog/55579/':('Story','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/realclimateaction-how-nz-stood-up-to-the-foss/blog/55955/':('Story','Protect','Forests', 'Freshwater', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/new-zealands-clean-rivers-damned-by-industria/blog/56167/':('Story','Protect','Freshwater', 'Food&Farming', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/ecological-farming-farming-for-the-future/blog/56322/':('Story','Transform','Freshwater', 'Food&Farming', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/coal-is-not-lol-10-reasons-to-shut-huntly-coa/blog/55970/':('Story','Transform','Coal', 'Renewables', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/why-piss-is-the-problem-with-industrial-dairy/blog/56360/':('Story','Transform','Food&Farming', 'Freshwater', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/10-years-ago-the-amazon-was-being-bulldozed-f/blog/56419/':('Story','Protect','Forests', 'Food&Farming', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/the-music-of-the-voices-for-the-arctic/blog/56805/':('Story','Protect','Oceans', 'Oil&Gas', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/nzs-electricity-watchdog-afraid-of-the-light/blog/57045/':('Story','Transform','Renewables', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/5-small-things-that-explain-the-big-problem-w/blog/57079/':('Story','Resist','Plastics', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/drought-is-real-but-dams-and-irrigation-are-n/blog/57116/':('Story','Transform','Food&Farming', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/victory-mega-dam-in-the-heart-of-amazon-cance/blog/57190/':('Story','Protect','Forests', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/three-myths-the-electricity-industry-want-you/blog/57284/':('Story','Transform','Renewables', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/john-key-is-the-last-man-standing-as-shell-pr/blog/57318/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/havelock-water-and-ruataniwha-its-time-to-joi/blog/57327/':('Story','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/3-big-reasons-why-we-need-ocean-sanctuaries-n/blog/57394/':('Story','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/ruataniwha-looks-dead-in-the-dirty-water/blog/57395/':('Story','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/is-there-a-dirty-big-irrigation-scheme-planne/blog/57409/':('Story','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/ruataniwha-dam-down-but-not-out-yet/blog/57463/':('Story','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/heres-why-we-took-the-site-office-at-the-ruat/blog/57479/':('Story','Resist','Food&Farming', 'Freshwater', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/te-ohu-kaimoana-crying-crocodile-tears-over-k/blog/57540/':('Story','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/our-government-the-blockheads-again/blog/57543/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/its-time-to-push-statoil-out-for-good/blog/57740/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/this-is-not-a-drill/blog/57755/':('Story','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/why-we-are-taking-arctic-oil-to-court/blog/57823/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/victory-worlds-largest-marine-protected-area-/blog/57878/':('Story','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/every-single-piece-of-plastic-ever-made-still/blog/58443/':('Story','Resist','Plastics', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/top-5-movies-set-in-the-arctic/blog/43396/':('Story','Protect','Oil&Gas', 'Oceans', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/cease-and-desist-message-delivered-to-seismic/blog/58481/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/neonicotinoids-a-serious-threat-for-flower-ho/blog/58497/':('Story','Transform','Food&Farming', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/our-rsvp-to-petroleum-new-zealand/blog/58727/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/dont-get-freaked-by-the-eco/blog/58823/':('Story','Transform','Food&Farming', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/is-nick-smith-minister-for-magic/blog/58827/':('Story','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/to-save-the-climate-we-must-all-push-beyond-o/blog/58932/':('Story','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/help-name-our-new-boat/blog/58969/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/cut-the-cows-a-double-whammy-for-the-environm/blog/59038/':('Story','Transform','Food&Farming', 'Freshwater', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/taitu-and-a-long-history-of-protest-in-boats/blog/59099/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/taitus-first-voyage-as-a-greenpeace-boat/blog/59107/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/dairy-bosses-plot-their-own-demise/blog/59385/':('Story','Transform','Food&Farming', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/school-bullying-woeful-opportunism-by-dairy-l/blog/59633/':('Story','Protect','Freshwater', 'Food&Farming', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/pure-dairy-pure-fiction-a-parody/blog/59645/':('Story','Protect','Freshwater', 'Food&Farming', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/battle-of-the-parodies-fonterra-answers-green/blog/59654/':('Story','Transform','Food&Farming', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/how-much-longer-can-we-take-our-water-for-gra/blog/59740/':('Story','Protect','Freshwater', 'Health', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/winning-on-the-worlds-largest-tuna-company-an/blog/59830/':('Story','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/with-love-from-the-arctic/blog/60053/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/cabbages-and-kings/blog/60067/':('Story','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/how-does-plastic-end-up-in-the-ocean/blog/60072/':('Story','Resist','Plastics', 'Oceans', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/9-ways-to-reduce-your-plastic-use/blog/60088/':('Story','Resist','Plastics', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/the-dairy-farmers-daughter-who-locked-herself/blog/60100/':('Story','Resist','Food&Farming', 'Freshwater', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/11-things-political-parties-should-do-now-if-/blog/60134/':('Story','Transform','Climate', 'Renewables', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/lightning-occupation-of-central-plains-water/blog/60169/':('Story','Resist','Freshwater', 'Food&Farming', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/thursday-september-7-occupying-central-plains/blog/60197/':('Story','Resist','Freshwater', 'Food&Farming', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/civil-disobedience-against-big-irrigation/blog/60037/':('Story','Resist','Freshwater', 'Food&Farming', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/we-have-one-year-to-create-the-largest-ever-p/blog/60455/':('Story','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/capitalism-moral-maze/blog/60434/':('Story','Transform','Freedom', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/the-ocean-plastic-crisis/blog/60456/':('Story','Resist','Plastics', 'Oceans', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/drinking-water-nitrate-a-ticking-time-bomb-fo/blog/60537/':('Story','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/3-reasons-this-small-countrys-court-decision-/blog/60649/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/antarctic-krill-not-just-whale-food/blog/60671/':('Story','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/big-oil-is-destructive-in-more-ways-than-one/blog/60689/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/plastic-is-everyones-problem-so-why-are-we-fo/blog/60739/':('Story','Resist','Plastics', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/can-we-create-healthy-oceans-and-tackle-clima/blog/60758/':('Story','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/great-news-for-the-arctic-and-the-antarctic/blog/60844/':('Story','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/is-fonterras-industrial-dairying-fuelling-for/blog/54688/':('Story','Transform','Food&Farming', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/too-many-holes-in-dam-scheme/blog/56860/':('Story','Protect','Food&Farming', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/a-view-from-waitangi-by-mike-smith/blog/58643/':('Story','Protect','Climate', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/why-petrobras-has-no-rights-to-drill-for-deep/blog/36880/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/something-anadarko-ought-to-know/blog/43954/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/a-message-to-anadarko/blog/44031/':('Story','Resist','Oil&Gas', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/deep-sea-drilling-does-not-add-up-to-a-win/blog/47179/':('Story','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/anadarko-court-case-lost-but-cowboys-exposed/blog/49629/':('Story','Resist','Oil&Gas', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/blog/anadarko-are-facing-the-biggest-ever-environm/blog/51300/':('Story','Resist','Oil&Gas', '', 'Migrate'),

            # Press Release
            # - 1st batch
            'http://www.greenpeace.org/new-zealand/en/press/John-Key-Should-Resign-as-Tourism-Minister-Greenpeace/':('Press Release','Protect','Freshwater', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Backdoor-talks-to-keep-coal-powering-NZ-an-absolute-disgrace/':('Press Release','Resist','Coal', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-Response-to-TPP-Protests/':('Press Release','Resist','Freedom', '', 'Migrate'),

            # - 2nd batch
            'http://www.greenpeace.org/new-zealand/en/press/Record-shattering-NASA-announcement-indicates-NZ-faces-extreme-weather-events/':('Press Release','Protect', 'Climate', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-activists-convicted-but-receive-no-further-punishment-over-10-hour-occupation-of-the-Tangaroa/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Governments-failing-oil-agenda-hits-hurdle-as-all-NZ-exploration-plans-are-trashed/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Genesis-letter/':('Press Release','Resist','Coal', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-launches-civil-disobedience-campaign-against-NZs-largest-oil-event/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Climate-action-a-matter-of-life-and-death-after-February-temperatures-smash-global-records/':('Press Release','Protect','Climate', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Landcorp-Ditches-Industrial-Dairy-Plans-Over-Pollution-Fears-Greenpeace-Response/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Whiskas-Embroiled-in-Modern-Day-Slavery-Scandal/':('Press Release','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Dairy-Irrigation-Subsidies-Must-Be-Ditched-to-Avert-Crisis-Greenpeace-Says/':('Press Release','Resist','Freedom', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-response-to-MRAG-Asia-Pacific-report-into-IUU-fishing-in-the-Pacific/':('Press Release','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/US-environmental-kingpin-Bill-McKibben-throws-his-weight-behind-civil-disobedience-in-NZ/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Hundreds-descend-on-Central-Auckland-to-blockade-NZs-largest-oil-event/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Oil-Block-Offer-a-Desperate-Last-Ditch-Bid-by-the-Government-to-Try-and-Save-Failing-Oil-Plans/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),

            # - 3rd batch
            'http://www.greenpeace.org/new-zealand/en/press/Whiskas-Clearly-Unable-to-Deny-Cat-Food-Linked-to-Slavery/':('Press Release','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Tax-on-solar-and-batteries-shocks-industry-green-and-consumer-groups/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/New-International-Executive-Directors-take-the-helm-at-Greenpeace/':('Press Release','Greenpeace','AboutUs', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Government-Should-Pull-Plug-on-Billion-Dollar-Dam-Say-Greenpeace/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Huntly-must-close-in-wake-of-worlds-largest-coal-company-filing-for-bankruptcy/':('Press Release','Resist','Coal', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Taiwans-fisheries-plagued-by-human-rights-abuses-and-shark-finning---Greenpeace-investigation/':('Press Release','Protect','Oceans', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Organised-crime-scandal-shows-NZs-climate-policy-is-a-total-bloody-waste-of-time/':('Press Release','Protect','Climate', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Kiwis-will-soon-have-to-compete-with-the-dairy-industry-for-freshwater-report-reveals/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-Ship-Targets-Thai-Unions-Destructive-Fishing-in-Indian-Ocean1/':('Press Release','Protect','Oceans', 'Esperanza', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/NZs-climate-plan-slammed-as-a-sham-as-Paula-Bennett-prepares-to-sign-Paris-agreement/':('Press Release','Protect','Climate', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Doomed-Ruataniwha-Scheme-Should-be-Ditched-by-Council-Tomorrow/':('Press Release','Protect','Freshwater', 'Health', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Genesis-about-to-face-the-climate-fight-of-2016-following-revelations-it-will-keep-coal-burning/':('Press Release','Resist','Coal', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Six-Tonnes-of-Dairy-Sewage-Used-to-Blockade-Capital-City-ACC-Office/':('Press Release','Protect','Freshwater', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-demands-investigation-into-Mauis-dolphin-death-cover-up-/':('Press Release','Protect','Oceans', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Overfishing-denier-fails-to-disclose-millions-in-seafood-industry-cash-for-research/':('Press Release','Protect','Oceans', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Explosive-fisheries-research-paper-reveals-more-than-twice-as-much-fish-taken-as-reported/':('Press Release','Protect','Oceans', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-shuts-down-Whiskas-factory-after-slavery-connection-confirmed/':('Press Release','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-blockade-ends-as-Mars-heads-into-industry-round-table/':('Press Release','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Government-must-end-industrial-dairying-subsidies-in-light-of-damning-greenhouse-gas-report/':('Press Release','Protect','Climate', 'Freshwater', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Activists-at-sea-call-lights-out-on-Thai-Unions-destructive-seafood-supply-chain/':('Press Release','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Fisheries-companies-win-contract-to-monitor-themselves/':('Press Release','Protect','Oceans', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Minister-confirms-Greenpeace-allegations-of-fishing-industry-policing-itself/':('Press Release','Protect','Oceans', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Councillors-conflict-of-interest-over-controversial-1b-dam-exposed/':('Press Release','Protect','Freshwater', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-joins-Amazon-People-in-community-led-battle-to-save-their-land/':('Press Release','Protect','Freshwater', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-gears-up-to-fight-NZs-first-ever-solar-tax-with-launch-of-hot-desk/':('Press Release','Transform','Renewables', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Environment-Commissioner-sends-please-explain-note-to-Government/':('Press Release','Protect','Climate', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-launches-legal-challenge-against-controversial-1b-dam-plan/':('Press Release','Protect','Freshwater', 'Food', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/New-Rainbow-Warrior-to-make-first-ever-visit-to-New-Zealand-in-January/':('Press Release','Greenpeace','AboutUs', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Government-Oil-Announcement-Tomorrow-Greenpeace-Comment/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-Response-to-MPIs-Multi-Million-Dollar-Hand-Out-for-Irrigation-Scheme/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Investment-company-requests-urgent-access-to-ratepayers-80m-for-controversial-dam/':('Press Release','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/IWC-paper-reveals-Government-and-fishing-industry-cover-up-dolphin-deaths-/':('Press Release','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/New-Zealands-electricity-watchdog-gives-green-light-to-kill-solar-electricity/':('Press Release','Transform','Renewables', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/New-Zealand-must-act-fast-in-wake-of-record-smashing-new-temperature-data/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/US-ship-decision-a-victory-for-people-power/':('Press Release','Resist','Freedom', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/NZ-Government-must-move-fast-to-ban-killer-microbeads-/':('Press Release','Resist','Plastics', 'Health', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Govt-plan-for-Hawkes-Bay-glosses-over-dam-risks-/':('Press Release','Protect','Freshwater', 'Health', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-welcomes-Landcorps-landmark-palm-kernel-ban/':('Press Release','Protect','Forests', 'Freshwater', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-welcomes-first-step-from-Fonterra-on-palm-kernel/':('Press Release','Protect','Forests', 'Freshwater', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Genesis-Energys-link-to-organised-crime-scandal-highly-disturbing-says-Greenpeace-/':('Press Release','Resist','Coal', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Nationals-climate-denialist-policies-will-undermine-Paris-Agreement/':('Press Release','Protect','Climate', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Gastro-outbreak-shows-Ruataniwha-must-be-scrapped/':('Press Release','Protect','Freshwater', 'Health', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Government--oil-programme-in-death-throes-as-oil-giant-Shell-looks-to-bail-out-of-NZ-/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Thousands-of-NZers-call-on-Hawkes-Bay-Regional-Council-to-scrap-dam/':('Press Release','Protect','Freshwater', 'Health', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/New-CEOs-plan-to-boost-coal-burning-at-Huntly-Power-Station-regressive/':('Press Release','Resist','Coal', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Hawkes-Bay-water-management-issues-show-Ruataniwha-Dam-must-be-scrapped-/':('Press Release','Protect','Freshwater', 'Health', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Keys-drilling-plan-in-freefall-as-NZs-biggest-offshore-oil-prospector-bails/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-at-Hawkes-Bay-Regional-Council-meeting-to-push-for-end-to-dam/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Ruataniwha-Dam-plan-dead-in-the-dirty-water/':('Press Release','Protect','Freshwater', 'Health', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-on-Forest--Bird-CEO-Appointment/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Mars-rejects-human-rights-tainted-seafood-following-Greenpeace-campaign/':('Press Release','Protect','Oceans', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Russel-Norman-to-ACC-dont-invest-in-Ruataniwha-Dam/':('Press Release','Protect','Freshwater', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/BREAKING-Greenpeace-uplifts-Ruataniwha-dam-site-office--returns-to-sender/':('Press Release','Protect','Freshwater', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Heron-report-shows-MPI-caught-by-fishing-industry---hook-line-and-sinker/':('Press Release','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Leading-Environmental-NGOs-Labour-Party-needs-to-support-not-undermine-the-Kermadec-Ocean-Sanctuary/':('Press Release','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-demands-end-to-public-subsidies-for-irrigation-after-damning-report/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Anti-dam-billboards-go-up-around-Hawkes-Bay/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Dam-promoters-look-to-acquire-land-under-Public-Works-Act/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-welcomes-Hawkes-Bay-anti-dam-council/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Tiki-Taane-and-Greenpeace-serenade-Electricity-Authority-with-45000-suns-to-protest-solar-tax/':('Press Release','Transform','Renewables', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-promises-summer-of-action-as-oil-giant-Statoil-signals-retreat/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/New-Regional-Council-must-drop-Supreme-Court-dam-bid/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Unprecedented-lawsuit-involving-Statoil-launched-on-eve-of-oil-giants-Northland-exit/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-on-PCE-report-into-agricultural-emissions/':('Press Release','Transform','Climate', 'Food', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Government-urged-to-better-protect-Mui-dolphin-in-wake-of-new-population-estimate/':('Press Release','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-teams-up-with-scientists-to-search-for-Mui-dolphin/':('Press Release','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/New-Zealands-promise-dead-in-the-water-as-Paris-Climate-Agreement-comes-into-force/':('Press Release','Protect','Climate', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Goffs-new-Auckland-Council-takes-first-vote-on-oil-drilling/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Auckland-Council-passes-historic-vote-to-oppose-deep-sea-oil-drilling/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Worlds-biggest-oil-survey-ship-flouts-safety-law-in-NZ-waters-during-78-earthquake/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/NZ-taxpayers-forced-to-fund-dirty-rivers-again/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Burning-our-future-Genesis-plan-to-burn-dirty-fuels-at-Huntly-for-next-20-years-revealed/':('Press Release','Resist','Coal', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/-Dropping-like-flies-Anadarko-the-latest-company-to-cull-search-for-oil-in-NZ/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-NZ-calls-out-meaningless-moratorium/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Thai-fishing-fleet-moving-to-Indian-ocean-to-avoid-regulation-finds-Greenpeace-investigation/':('Press Release','Protect','Oceans', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Thumbs-up-for-controversial-Greenpeace-TV-ad/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/NZ-climate-groups-form-coalition-and-announce-plans-to-disrupt-major-oil-summit/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Governments-oil-permit-announcement-shows-broken-NZ-oil-industry-/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/ASA-rejects-challenge-to-Greenpeaces-solar-tax-campaign-/':('Press Release','Transform','Renewables', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-reccy-reveals-worlds-biggest-seismic-ship-blasting-for-oil-off-East-Coast/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Sanford-and-Moana-take-small-step-to-save-Mui-dolphins---what-about-Talleys-and-Govt/':('Press Release','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-warns-more-algal-blooms-to-come-with-planned-Hurunui-irrigation-dams/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-NZ-boats-tailing-worlds-biggest-seismic-blasting-ship/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-inflatables-intercept-worlds-biggest-seismic-oil-ship-50-miles-out-to-sea/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/HSBC-exposed-as-the-banker-behind-Indonesias-deforestation-crisis/':('Press Release','Protect','Forests', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/New-oil-exploration-for-NZ-as-2016-officially-declared-hottest-on-record/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Irrigation-attack---Greenpeace-says-public-frustration-about-dirty-rivers-spilling-over-/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-calls-on-the-Dairy-Industry-to-come-clean-about-its-plans-for-expansion/':('Press Release','Protect','Freshwater', 'Food', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-on-Auckland-sewage-overflows/':('Press Release','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Battle-over-solar-tax-heats-up-as-full-hearing-announced/':('Press Release','Transform','Renewables', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/blooming-dangerous-in-canterbury/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/New-HSBC-no-deforestation-policy-first-step-towards-sustainable-palm-oil-finance/':('Press Release','Protect','Forests', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Swimmable-rivers-Greenpeace-says-look-below-the-surface/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-NZ-crowdfunding-boat-to-confront-seismic-blaster-The-Beast/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Oil-conference-in-lockdown-as-protesters-blockade-entrance/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-prepares-to-confront-Donald-Trumps-climate-madness-at-sea-in-a-crowdfunded-boat/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-reveals-worrying-web-of-connections-between-MPI-and-fishing-industry/':('Press Release','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-NZ-sets-out-in-crowdfunded-boat-to-confront-Amazon-Warrior/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-swimmers-stop-Amazon-Warrior-seismic-blasting-50-miles-out-to-sea/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Bill-English-crying-crocodile-tears-over-flood-devastation-says-Greenpeace/':('Press Release','Protect','Climate', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-accuses-Government-of-aggravating-water-crisis/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Nothing-new-in-Ruataniwha-review---irrigation-dam-still-a-bad-idea/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Havelock-contamination-scandal-not-a-one-off/':('Press Release','Protect','Freshwater', 'Health', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/DairyNZ-undermining-environmental-efforts-of-dairy-farmers-across-NZ-/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/government-absence-backbone-destroying-NZ-Rivers/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Joyce-Budget-billion-dollar-handout-to-polluters/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Government-delays-morally-repugnant-case-against-Greenpeace-activists/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Tens-of-Thousands-of-Homes-Face-Climate-Flooding-Disaster-Greenpeace-Response/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-activists-occupy-Government-climate-ship-caught-searching-for-oil-/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/John-Key-poised-to-hand-out-more-oil-drilling-permits-in-wake-of-Paris-climate-talks/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Fossil-Fuel-President-Trump-cant-kill-Paris-Climate-Agreement/':('Press Release','Resist','Climate', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-climbers-prepare-message-above-Beehive-for-US-Secretary-of-State/':('Press Release','Resist','Climate', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Leaked-report-shows-public-misled-over-snapper-policing/':('Press Release','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Labours-freshwater-policy-more-ambitious-than-Govt-but-still-has-some-leaks-in-it/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Dairy-Bosses-climate-change-plan-is-all-talk-and-no-trousers/':('Press Release','Protect','Climate', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Time-for-diseased-electricity-industry-overhaul/':('Press Release','Transform','Renewables', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/student-battles-new-zealand-government-in-climate-lawsuit/':('Press Release','Protect','Climate', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Too-Many-Cows-Could-Make-Us-Sick---New-Greenpeace-NZ-Report/':('Press Release','Protect','Freshwater', 'Health', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Dam-decision-huge-victory-against-big-irrigation---GreenpeaceDam-decision-huge-victory-against-big-irrigation/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-launches-new-educational-website-on-anniversary-of-Rainbow-Warrior-bombing/':('Press Release','Protect','Freedom', 'Health', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Farmers-star-in-Greenpeace-film-/':('Press Release','Transform','Food', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-says-council-decision-means-dam-is-dea/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Pressure-on-as-Freshwater-Rescue-Plan-gains-support/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Actress-Lucy-Lawless-sets-off-in-Greenpeace-ship-to-confront-Arctic-oil-drillers/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Lucy-Lawless-joins-climate-change-survivor-in-protest-against-Statoils-Arctic-oil-exploitation/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Watershed-indigenous-rights-case-could-set-precedent-for-blocking-NZ-oil-exploration/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-launches-campaign-to-ban-single-use-plastic-bags-in-NZ/':('Press Release','Resist','Plastics', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-activists-lock-themselves-inside-Canterbury-irrigation-pipes/':('Press Release','Resist','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Well-be-back-vows-Greenpeace-after-successful-pipeline-protest-in-Canterbury/':('Press Release','Resist','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Labours-Plan-to-Cull-Irrigation-Fund-a-Watershed-Policy-for-Clean-Rivers/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/NZ-Govt-implicated-in-oil-industrys-multi-year-covert-spy-operation-on-Greenpeace-/':('Press Release','Protect','Freedom', 'AboutUs', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Big-Irrigations-death-grip-costs-farmers-more-than-water-charge-would-Greenpeace/':('Press Release','Transform','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Super-Funds-fossil-fuel-divestment-an-aha-moment-for-NZ-economy/':('Press Release','Transform','Climate', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Microbead-policy-a-good-start---Greenpeace-urges-Government-to-ban-the-bags/':('Press Release','Resist','Plastics', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-activists-stop-Statoil-rig-drilling-in-the-Arctic-/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/22-August-2017----Greenpeace-tell-farming-leadership---show-us-the-substance/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greens-Ban-the-Bag-policy-needs-to-happen-sooner/':('Press Release','Resist','Plastics', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeaces-Taitu-crew-plead-Not-Guilty-in-historic-climate-court-case/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Governments-agriculture-research-fund-pitiful/':('Press Release','Transform','Food', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Leaked-report-shows-climate-must-be-key-election-issue/':('Press Release','Protect','Climate', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-uses-lightning-occupation-to-shut-down-big-irrigation-scheme/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Arrests-made-at-Greenpeace-irrigation-dam-occupation/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Labour-climate-policy-a-good-start-but-not-strong-enough/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/On-climate-policy-Jacinda-has-the-talk-but-Greens-have-the-walk/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Jacinda-Ardern-refuses-to-stop-deep-sea-oil-nuclear-bombJacinda-Ardern-refuses-to-stop-deep-sea-oil-nuclear-bomb/':('Press Release','Protect','Freedom', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Water-activists-flood-into-Ecan-offices-to-save-rivers/':('Press Release','Protect','Freshwater', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Labour-and-Greens-confirm-commitment-to-restoring-democracy-in-Christchurch-following-mass-occupation/':('Press Release','Transform','Freedom', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/New-Worlds-plastic-bag-poll-rigged-says-Greenpeace-/':('Press Release','Resist','Plastics', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/New-Government-must-take-action-on-environment---Greenpeace/':('Press Release','Protect','Freshwater', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Environmental-supergroup-puts-future-government-on-notice/':('Press Release','Protect','Freshwater', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-calls-for-post-election-deal-to-reject-monstrous-new-offshore-oil-project/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Countdowns-Bold-Bag-Ban-praised-by-Greenpeace/':('Press Release','Resist','Plastics', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/We-Wont-Back-Down-Greenpeace-activists-charged-under-Anadarko-Amendment-head-to-trial1/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/A-victory-for-people-power-New-World-topples-under-pressure-to-Ban-the-Bag-/':('Press Release','Resist','Plastics', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Govt-must-put-search-for-new-oil-on-hold-after-release-of-disturbing-MfE-climate-report/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-cautiously-hopeful-about-new-Government/':('Press Release','Transform','Climate', 'Food', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Close-the-back-door-on-big-irrigation/':('Press Release','Protect','Freshwater', 'Food', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-launches-campaign-to-create-largest-protected-area-on-Earth-/':('Press Release','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Broadcasting-Standards-Authority-confirms-accuracy-of-Greenpeace-criticism-of-fishing-industry-/':('Press Release','Protect','Oceans', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Hearing-is-believing-Scientist-exposes-impacts-of-oil-blasting-on-NZ-blue-whalesHearing-is-believing-Scientist-exposes-impacts-of-oil-blasting-on-NZ-blue-whales/':('Press Release','Resist','Oil&Gas', 'Oceans', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Sarah-Thomsons-epic-court-battle-gives-strong-mandate-for-climate-action/':('Press Release','Protect','Climate', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Good-COP-or-bad-COP-Greenpeace-calls-on-Govt-to-stand-up-for-the-Pacific/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-on-Speech-from-the-Throne-Bold-words-now-need-bold-action/':('Press Release','Transform','Climate', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/United-Nations-showcases-kiwi-farmers-featured-in-Greenpeace-film-The-Regenerators/':('Press Release','Transform','Food', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Modern-day-villain-holds-special-access-card-to-NZ-Parliament/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-transforms-Parliament-lawn-into-a-riverbed-/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Targets-a-good-first-step-but-Fonterra-must-reduce-the-dairy-herd/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/New-Zealands-rivers-need-more-than-empty-headlines-from-Fonterra/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Coca-Cola--Not-always-the-real-thing/':('Press Release','Resist','Plastics', 'Oceans', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/DairyNZs-latest-water-plan-a-gutless-betrayal/':('Press Release','Protect','Freshwater', 'Food', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Amazon-Warrior-steaming-to-NZ-to-blast-blue-whale-habitat/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Government-has-the-power-to-stop-giant-oil-ship/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Expect-resistance-Greenpeace-warning-to-Amazon-Warrior/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-calls-out-new-Government-for-muddying-the-waters/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-launches-legal-challenge-against-Amazon-Warrior-at-Parliament-protest-/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-damn-concerned-public-money-still-being-spent-on-polluting-rivers/':('Press Release','Protect','Freshwater', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Govt-refusal-to-rule-out-fossil-fuel-expansion-undermines-new-Climate-Commission/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Environmental-heavyweights-pen-letter-to-Govt---End-new-fossil-fuels-now/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/New-permit-issued-for-oil-and-gas-exploration-must-be-NZs-last/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/The-Irrigation-Industrys-opening-up-an-early-Christmas-present/':('Press Release','Protect','Freshwater', 'Food', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Disappointing-Arctic-legal-decision-will-strengthen-movement-to-end-oil/':('Press Release','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-launches-landmark-expedition-to-bottom-of-the-Antarctic-Ocean/':('Press Release','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-activists-jump-on-Amazon-Warrior-support-vessel-as-it-arrives-in-port/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Climate-activists-locked-on-oil-supply-ship-threatened-with-draconian-Anadarko-Amendment/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-amused-at-negative-survey-oil-industry-releases-about-itself/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Genesis-plan-to-keep-coal-burning-until-2030-stuns/':('Press Release','Resist','Coal', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/What-the-heck-is-Sam-Neill-doing/':('Press Release','Resist','Plastics', 'Oceans', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Govt-urged-to-use-regional-development-fund-for-just-transitions/':('Press Release','Transform','Renewables', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Richie-McCaw-fails-to-convert---Fonterras-PR-falling-flat/':('Press Release','Protect','Freshwater', 'Food', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Get-off-the-gas---Greenpeace-to-new-Government/':('Press Release','Protect','Freshwater', 'Food', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Helen-Clark-Joins-Tidal-Wave-Of-Support-To-Ban-The-Bag/':('Press Release','Resist','Plastics', 'Oceans', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/A-global-report-out-today-could-present-a-major-opportunity-for-New-Zealand-agriculture/':('Press Release','Protect','Freshwater', 'Food', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Oil-search-undermines-Arderns-Pacific-climate-pledge/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Russel-Norman-Climate-Commission-needs-teeth-like-Reserve-Bank/':('Press Release','Protect','Climate', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Leading-NZers-urge-Ardern-to-end-oil-exploration/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Licensed-to-krill-Greenpeace-report-exposes-Antarctic-fishing-industry/':('Press Release','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Jane-Campion-and-Taika-Waititi-sign-letter-urging-PM-to-end-oil-exploration/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-calls-for-Govt-inquiry-into-spy-agency-to-include-MBIE/':('Press Release','Protect','Oil&Gas', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Ardern-Government-to-accept-end-oil-petition-outside-Parliament-today/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-isnt-a-charity-its-a-necessity/':('Press Release','Resist','AboutUs', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Janet-the-17m-blue-whale-makes-oil-conference-debut/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/End-of-Govt-funded-irrigation-a-huge-win-for-rivers-and-for-people-power/':('Press Release','Protect','Freshwater', 'Food&Farming', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Even-the-banks-are-saying-we-need-climate-action/':('Press Release','Resist','Climate', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Ardern-makes-oil-history-Huge-win-for-climate-and-people-power---Greenpeace/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Seabed-mining-Court-case-a-fight-for-the-future-of-our-precious-oceans/':('Press Release','Protect','Oceans', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Former-President-and-NASA-scientist-confirmed-as-witnesses-in-Greenpeace-trial/':('Press Release','Resist','Oil&Gas', 'Climate', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Wake-up-call-on-NZ-land-use/':('Press Release','Protect','Freshwater', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/press/Greenpeace-is-calling-on-New-Zealanders-to-start-turning-up-the-heat-on-big-business-to-help-solve-the-plastics-crisis/':('Press Release','Resist','Plastics', '', 'Migrate'),

            # Publication
            # - 1st batch
            'http://www.greenpeace.org/new-zealand/en/reports/Made-in-Taiwan/':('Publication','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/global-wind-energy-outlook/':('Publication','Transform','Renewables', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/OIA-Docs-for-Thompson-and-Clark-MBIE-Relationship/':('Publication','Resist','Freedom', 'Oil&Gas', 'Migrate'),

            # - 2nd batch
            'http://www.greenpeace.org/new-zealand/en/reports/future-investment-energy/':('Publication','Transform','Renewables', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/the-power-and-appeal-of-wind/':('Publication','Transform','Renewables', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/dirty-old-coal/':('Publication','Resist','Coal', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/enviro-impacts-of-coal/':('Publication','Resist','Coal', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/Save-our-beaches-from-oil-disaster/':('Publication','Resist','Oil&Gas', 'Coal', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/Changing-Tuna/':('Publication','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/Out-Of-Our-Depth-Deep-sea-oil-exploration-in-New-Zealand/':('Publication','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/The-Future-is-Here-report/':('Publication','Transform','Renewables', 'Oil&Gas', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/Joint-Statement-on-Crown-Minerals-Bill-Amendment-2013/':('Publication','Resist','Oil&Gas', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/-Response-to-Minister-of-Energy-and-Resources-July-2013/':('Publication','Resist','Oil&Gas', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/New-Zealand-Oil-Spill-Report/':('Publication','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/Fewer-boats-more-fish/':('Publication','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/Out-of-line---The-failure-of-the-global-tuna-longline-fisheries/':('Publication','Protect','Oceans', '', 'Migrate'),

            # - 3rd batch
            'http://www.greenpeace.org/new-zealand/en/reports/nz-energy-Transform-report/':('Publication','Transform','Renewables', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/The-silent-Energy-Transform/':('Publication','Transform','Renewables', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/Legal-opinion-on-the-proposed-Crown-Minerals-Act-amendments/':('Publication','Resist','Oil&Gas', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/Transforming-Tuna-Fisheries-in-Pacific-Island-Countries/':('Publication','Protect','Oceans', 'Freedom', 'Migrate'),
            #'http://www.greenpeace.org/new-zealand/en/reports/Energy-Transform-2015/':('Publication','Transform','Renewables', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/Dam-Wrong-Why-the-Ruataniwha-Dam-will-mean-more-local-water-pollution/':('Publication','Protect','Freshwater', 'Food&Farming', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/Sold-Down-River-How-Big-Irrigation-Will-Destroy-Our-Water/':('Publication','Protect','Freshwater', 'Food&Farming', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/Turn-The-Tide-Human-Rights-Abuses-and-Illegal-Fishing-in-Thailands-Overseas-Fishing-Industry/':('Publication','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/Greenpeace-NZ-Television---Complaint-16400/':('Publication','Transform','Food&Farming', 'Freshwater', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/sick-of-too-many-cows/':('Publication','Transform','Food&Farming', 'Freshwater', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/Election-2017-ENGO-Letter-to-political-leadership/':('Publication','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/Open-letter-to-Jacinda-Ardern/':('Publication','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/Licence-to-Krill/':('Publication','Protect','Oceans', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/OIA-Docs-for-Thompson-and-Clark-MBIE-Relationship/':('Publication','Resist','Oil&Gas', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/Russel-Norman-letter-to-SSC/':('Publication','Resist','Oil&Gas', 'Freedom', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/Greenpeace-Submission-on-Re-Exclusive-Economic-Zone-and-Continental-Shelf-Environmental-EffectsPermitted-Activities-Regulations-2013/':('Publication','Resist','Oil&Gas', '', 'Migrate'),
            'http://www.greenpeace.org/new-zealand/en/reports/A-Deadly-Trade-Off/':('Publication','Protect','Forests', '', 'Migrate'),
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
            'author': 'Greenpeace NZ',
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
            body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)

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
            if ( ( len(Segments) == 4 ) and Segments[4] ):
                author_username = Segments[4]

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
            body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)
            if lead_text:
                body_text = '<div class="leader">' + lead_text + '</div>' + body_text + response.xpath(' //*[@id="content"]/div[4]/div/div[2]/p').extract_first()

        yield {
            'type': 'Press Release',
            'p3_image_gallery': p3_image_gallery,
            'title': extract_with_css('div.article h1 span::text'),
            #'subtitle': '',
            'author': 'Greenpeace NZ',
            'author_username': 'greenpeace',
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

        yield {
            'type': 'Publication',
            'p3_image_gallery': p3_image_gallery,
            'title': extract_with_css('div.article h1 span::text'),
            #'subtitle': subtitle,
            'author': 'Greenpeace NZ',
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
