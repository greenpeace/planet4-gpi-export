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

import csv
import urllib2

locale.setlocale(locale.LC_ALL, '')

class AllSpider(scrapy.Spider):
    name = 'all'

    custom_settings = {
        'ROBOTSTXT_OBEY': 0,
        'FEED_URI': 'gpeuunit_v2_migration.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def start_requests(self):

        #v1
        start_urls = {
            'http://www.greenpeace.org/eu-unit/en/News/2016/209-pesticides-used-in-the-EU-could-endanger-humans-or-environment/':('News','NATURE & FOOD','Pesticides','Farming','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Advocate-General-opinion-EU-Singapore-deal/':('News','DEMOCRACY & EUROPE','Trade','EUaffairs','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/bee-harming-pesticides-banned-EFSA-reports/':('News','NATURE & FOOD','Pesticides','Farming','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/TTIP-Q-and-A-unpacking-EU-US-trade-talks/':('News','DEMOCRACY & EUROPE','Trade','','Migrate','Briefing'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/Improved-EU-decision-making-in-the-area-of-health-and-consumer-protection/':('News','POLLUTION','Health','EUaffairs','Migrate','Letter'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/Bratislava-summit-Europe-at-a-crossroads/':('Publications','DEMOCRACY & EUROPE','EUaffairs','Democracy','Migrate','Letter'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/CETA-SandD-progressive-trade-principles/':('Publications','DEMOCRACY & EUROPE','Trade','','Migrate','Briefing'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/Civil-society-calls-for-a-new-Europe-for-people-and-planet/':('Publications','DEMOCRACY & EUROPE','EUaffairs','Democracy','Migrate','Letter'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/Commission-fails-to-regulate-new-GMOs-after-intense-US-lobbying/':('Publications','NATURE & FOOD','GMOs','Transparency','Migrate','Briefing'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/Leaked-TiSA-texts-reveal-threats-to-climate-/':('Publications','DEMOCRACY & EUROPE','Trade','ClimateChange','Migrate','Report')
        }

        #v2
        start_urls = {
            'http://www.greenpeace.org/eu-unit/en/News/2016/209-pesticides-used-in-the-EU-could-endanger-humans-or-environment': ('News','NATURE & FOOD','Pesticides','Farming','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Advocate-General-opinion-EU-Singapore-deal': ('News','DEMOCRACY & EUROPE','Trade','EUaffairs','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/bee-harming-pesticides-banned-EFSA-reports': ('News','NATURE & FOOD','Pesticides','Farming','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Belgian-agreement-to-trigger-ECJ-ruling-on-legality-of-CETA': ('News','DEMOCRACY & EUROPE','Trade','EUaffairs','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Bratislava-protest-ends-week-of-mobilisation-against-EU-trade-deals': ('News','DEMOCRACY & EUROPE','Trade','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/CETA-fake-new-approach-on-investment-protection-': ('News','DEMOCRACY & EUROPE','Trade','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/CETA-joint-declaration-PR': ('News','DEMOCRACY & EUROPE','Trade','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/CETA-spin-unspun': ('News','DEMOCRACY & EUROPE','Trade','','Migrate','Briefing'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Commission-breaks-pledge-to-bring-EU-targets-in-line-with-Paris-climate-deal': ('News','CLIMATE & ENERGY','ClimateChange','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Commission-fails-to-regulate-new-GMOs-after-intense-US-lobbying': ('News','NATURE & FOOD','GMOs','Farming','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Commission-is-blind-to-renewables-potential-keeps-Europe-stuck-on-gas-': ('News','CLIMATE & ENERGY','Renewables','FossilFuels','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Commission-must-prepare-glyphosate-exit-plan': ('News','NATURE & FOOD','Pesticides','Food','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Commission-seeks-approval-three-GM-maizes': ('News','NATURE & FOOD','GMOs','Farming','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Commission-seeks-glyphosate-approval-by-another-name': ('News','NATURE & FOOD','Pesticides','Farming','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Commission-slams-weak-implementation-of-forest-protection-law': ('News','NATURE & FOOD','Forests','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Concerns-over-the-impacts-of-fish-aggregating-devices': ('News','NATURE & FOOD','Oceans','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Controversial-EU-Canada-trade-deal-hangs-by-a-thread': ('News','DEMOCRACY & EUROPE','Trade','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Environment-ministers-surprise-Commission-with-support-for-higher-EU-2030-carbon-target': ('News','CLIMATE & ENERGY','ClimateChange','','Migrate','Press Release'),
            #'http://www.greenpeace.org/eu-unit/en/News/2016/EU-Canada-sign-doomed-CETA-trade-deal': ('News','DEMOCRACY & EUROPE','Trade','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/EU-lifeline-to-coal-could-derail-renewable-energy-transition': ('News','CLIMATE & ENERGY','FossilFuels','Renewables','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/EU-Parliament-backs-glyphosate-restrictions': ('News','NATURE & FOOD','Pesticides','Food','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/EU-Parliament-opposes-import-of-three-herbicide-resistant-GM-crops--': ('News','NATURE & FOOD','Pesticides','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/EU-Parliament-rejects-opportunity-to-clarify-legal-status-of-CETA': ('News','DEMOCRACY & EUROPE','Trade','EUaffairs','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/EU-prepares-to-brush-aside-glyphosate-herbicide-safety-concerns': ('News','NATURE & FOOD','Pesticides','ToxicChemicals','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/EU-presidency-denies-public-access-to-CETA-TTIP-talks': ('News','DEMOCRACY & EUROPE','Trade','Transparency','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/EU-report-rethink-trade-deals-industrial-farming': ('News','DEMOCRACY & EUROPE','Trade','Farming','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/EU-US-talks-delayed-as-Greenpeace-continues-protest': ('News','DEMOCRACY & EUROPE','Trade','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Europe-failing-to-use-legal-armoury-against-illegal-logging': ('News','NATURE & FOOD','Forests','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Europe-must-reconnect-with-its-people-and-values': ('News','DEMOCRACY & EUROPE','Democracy','EUaffairs','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Flawed-Commission-analysis-backs-new-subsidies-for-obsolete-power-plants-': ('News','CLIMATE & ENERGY','FossilFuels','Nuclear','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Glyphosate-licence-renewal-suspended-in-light-of-health-concerns-': ('News','NATURE & FOOD','Pesticides','Health','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/governments-must-reconnect-with-EU-founding-values': ('News','DEMOCRACY & EUROPE','Democracy','EUaffairs','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Greenpeace-activists-block-secret-TTIP-talks': ('News','DEMOCRACY & EUROPE','Trade','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Greenpeace-blockade-against-EU-US-trade-talks-lifted': ('News','DEMOCRACY & EUROPE','Trade','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Greenpeace-calls-on-Italy-to-reconsider-position-on-EU-Canada-trade-deal': ('News','DEMOCRACY & EUROPE','Trade','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Greenpeace-calls-on-ministers-to-stop-CETA': ('News','DEMOCRACY & EUROPE','Trade','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Greenpeace-comment-EU-trade-Council': ('News','DEMOCRACY & EUROPE','Trade','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Greenpeace-comment-EU-vote-on-glyphosate-extension': ('News','NATURE & FOOD','Pesticides','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Greenpeace-comment-on-Commission-extension-of-glyphosate-licence': ('News','CLIMATE & ENERGY','Pesticides','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Greenpeace-comment-on-EU-glyphosate-decision': ('News','NATURE & FOOD','Pesticides','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Greenpeace-comment-on-the-European-Parliament-vote-on-the-authorisation-of-three-GM-maize-varieties': ('News','NATURE & FOOD','GMOs','Farming','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Greenpeace-comment-on-Walloon-Parliament-no-to-CETA': ('News','DEMOCRACY & EUROPE','Trade','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Greenpeace-EU-comment-on-Commissions-proposal-to-fund-nuclear-research': ('News','CLIMATE & ENERGY','Nuclear','EUaffairs','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Greenpeace-response-Hollande-TTIP-comments': ('News','DEMOCRACY & EUROPE','Trade','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Greenpeace-time-to-hit-the-stop-button-on-TTIP': ('News','DEMOCRACY & EUROPE','Trade','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Industry-ties-JMPR-glyphosate': ('News','NATURE & FOOD','Pesticides','Transparency','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Landmark-ECJ-ruling-research-on-dangers-of-pesticides-must-be-made-public': ('News','NATURE & FOOD','Pesticides','Transparency','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Leaked-EU-Canada-joint-declaration-has-legal-weight-of-a-holiday-brochure-Greenpeace': ('News','DEMOCRACY & EUROPE','Trade','Transparency','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Leaked-TTIP-documents-released': ('News','DEMOCRACY & EUROPE','Trade','Transparency','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/MEPs-unable-to-adjust-CETA-course-TPP-trade': ('News','DEMOCRACY & EUROPE','Trade','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/neonicotinoids-threat-wild-bees-other-animals': ('News','NATURE & FOOD','Pesticides','Farming','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/People-can-power-the-Energy-Revolution': ('News','CLIMATE & ENERGY','Renewables','EnergyTransition','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Political-concerns-delay-agreement-on-CETA': ('News','DEMOCRACY & EUROPE','Trade','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Rush-to-adopt-EU-Canada-trade-deal-would-widen-distrust-in-mainstream-politics': ('News','DEMOCRACY & EUROPE','Trade','Democracy','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/Shorter-EU-licence-would-leave-people-nature-exposed-to-glyphosate': ('News','NATURE & FOOD','Pesticides','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/TTIP-EU-and-US-show-signs-of-desperation': ('News','DEMOCRACY & EUROPE','Trade','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/TTIP-leaks-update-Greenpeace-response-to-Commission-statements': ('News','DEMOCRACY & EUROPE','Trade','Transparency','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/TTIP-Q-and-A-unpacking-EU-US-trade-talks': ('News','DEMOCRACY & EUROPE','Trade','','Migrate','Briefing'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/TTIP-talks-press-ahead-with-new-privileges-for-big-business': ('News','DEMOCRACY & EUROPE','Trade','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2016/TTIPleaks-confidential-TTIP-papers-unveil-US-position': ('News','DEMOCRACY & EUROPE','Trade','Transparency','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/500000-people-EU-ban-glyphosate': ('News','NATURE & FOOD','Pesticides','Democracy','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/Activists-EU-go-for-100-renewable-energy': ('News','CLIMATE & ENERGY','Renewables','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/Activists-keep-justice-afloat-as-CETA-threatens-to-sink-democracy': ('News','DEMOCRACY & EUROPE','Trade','Justice','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/andriukaitis-confronted-ban-glyphosate': ('News','NATURE & FOOD','Pesticides','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/Bee-killing-pesticides-dangerous-greenhouses': ('News','NATURE & FOOD','Pesticides','Farming','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/ceta-food-safety-provisional-application': ('News','DEMOCRACY & EUROPE','Trade','Food','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/CETA-MEPs-put-European-Parliament-on-the-wrong-side-of-history': ('News','DEMOCRACY & EUROPE','Trade','Democracy','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/Commission-narrow-vision-renewables-mobility': ('News','CLIMATE & ENERGY','Renewables','Transport','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/Commission-Paks-state-aid-Orban-nuclear-regulator': ('News','CLIMATE & ENERGY','Nuclear','EUaffairs','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/Commission-prepares-to-authorise-three-GM-maizes': ('News','NATURE & FOOD','GMOs','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/Commission-public-debate-trade-damning-ECJ-ruling': ('News','DEMOCRACY & EUROPE','Trade','Justice','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/commission-rejects-StopGlyphosate-ECI': ('News','NATURE & FOOD','Pesticides','Democracy','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/Commission-revises-EU-decision-making-rules-in-move-to-avoid-blame-': ('News','DEMOCRACY & EUROPE','EUaffairs','Pesticides','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/Commission-takes-major-step-to-ban-three-neonics': ('News','NATURE & FOOD','Pesticides','Farming','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/Conflict-of-interest-concerns-blight-glyphosate-new-safety-assessment': ('News','NATURE & FOOD','Pesticides','Transparency','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/Energy-ministers-coal-Christmas': ('News','CLIMATE & ENERGY','FossilFuels','Renewables','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/EU-2030-energy-package-community-power-renewables-transition': ('News','CLIMATE & ENERGY','Renewables','EnergyTransition','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/EU-at-60-Rome-activists-demand-greener-Europe': ('News','DEMOCRACY & EUROPE','Democracy','EUaffairs','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/EU-chemicals-agency-sweeps-glyphosate-cancer-evidence-under-the-carpet': ('News','POLLUTION','Pesticides','Transparency','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/EU-China-must-lead-shift-to-renewables': ('News','CLIMATE & ENERGY','ClimateChange','Renewables','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/EU-climate-leadership-boost-renewables': ('News','CLIMATE & ENERGY','ClimateChange','Renewables','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/EU-court-ruling-singapore-trade-deal': ('News','DEMOCRACY & EUROPE','Trade','Justice','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/EU-energy-plans-wont-meet-Paris-climate-commitments': ('News','CLIMATE & ENERGY','ClimateChange','Renewables','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/EU-farming-reform-plan-overlooks-impact-of-meat-sector': ('News','NATURE & FOOD','Farming','Food','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/EU-governments-reject-Commission-push-for-glyphosate': ('News','NATURE & FOOD','Pesticides','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/EU-Japan-trade-deal-corporate-protectionism': ('News','DEMOCRACY & EUROPE','Trade','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/EU-parliament-backs-people-power': ('News','CLIMATE & ENERGY','Renewables','PeoplePower','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/EU-report-on-pesticide-residues-ignores-toxic-cocktail-effect-Greenpeace': ('News','NATURE & FOOD','Pesticides','ToxicChemicals','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/EU-stop-palm-oil-deforestation-Parliament': ('News','NATURE & FOOD','Forests','Bioenergy','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/EU-to-renew-glyphosate-licence-ignoring-concerns': ('News','NATURE & FOOD','Pesticides','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/European-citizens-initiative-ECI-stop-glyphosate': ('News','NATURE & FOOD','Pesticides','PeoplePower','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/European-Parliament-and-StopGlyphosate-coalition-to-challenge-Andriukaitis': ('News','NATURE & FOOD','Pesticides','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/European-Parliament-backs-biodiversity-over-pesticides': ('News','NATURE & FOOD','Pesticides','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/European-Parliament-resoundingly-votes-to-end-glyphosate-use': ('News','NATURE & FOOD','Pesticides','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/First-pan-EU-field-study-confirms-neonic-harm': ('News','NATURE & FOOD','Pesticides','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/Giant-weedkiller-bottle-torn-down-as-Europe-debates-future-of-glyphosate-': ('News','NATURE & FOOD','Pesticides','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/Glyphosate-a-licence-is-a-licence-no-matter-how-long-its-for': ('News','NATURE & FOOD','Pesticides','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/Governments-citizens-reject-GMOs-MON810-Bt11-1507': ('News','NATURE & FOOD','GMOs','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/Greenpeace-comment-One-Planet-climate-summit': ('News','CLIMATE & ENERGY','ClimateChange','FossilFuels','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/Greenpeace-Netherlands-leaks-EU-Mercosur-trade-papers': ('News','DEMOCRACY & EUROPE','Trade','Transparency','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/Growing-number-EU-governments-oppose-glyphosate': ('News','NATURE & FOOD','Pesticides','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/Improved-EU-decision-making-in-the-area-of-health-and-consumer-protection': ('News','POLLUTION','Health','EUaffairs','Migrate','Letter'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/Lacklustre-drive-for-renewables-threatens-energy-transition-': ('News','CLIMATE & ENERGY','Renewables','EnergyTransition','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/Leaked-trade-papers': ('News','DEMOCRACY & EUROPE','Trade','Transparency','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/Monsantos-view-of-independent-science-copied-into-EU-evaluations-': ('News','NATURE & FOOD','Pesticides','Transparency','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/No-GMO-support': ('News','NATURE & FOOD','GMOs','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/One-million-Europeans-stand-against-glyphosate': ('News','NATURE & FOOD','Pesticides','PeoplePower','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/open-honest-look-eu-trade': ('News','DEMOCRACY & EUROPE','Trade','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/Over-150-civil-society-groups-call-for-reform-of-European-agricultural-policies': ('News','NATURE & FOOD','Farming','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/parliament-fires-up-energy-transition': ('News','CLIMATE & ENERGY','Renewables','EnergyTransition','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2017/tighten-rules-subsidies-coal': ('News','CLIMATE & ENERGY','FossilFuels','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2018/Activists-call-out-EU-ministers-for-failing-to-support-renewable-energy-development': ('News','CLIMATE & ENERGY','Renewables','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2018/Climate-change-activists-call-on-EU-energy-ministers-to-unlock-rooftop-revolution-': ('News','CLIMATE & ENERGY','Renewables','EnergyTransition','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2018/Commission-chemical-pesticides-producers-control-science': ('News','NATURE & FOOD','Pesticides','Transparency','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2018/Commission-study-action-deforestation': ('News','NATURE & FOOD','Forests','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2018/EFSA-confirms-pesticides-danger-bees': ('News','NATURE & FOOD','Pesticides','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2018/environment-health-ignored-agriculture-ministers': ('News','NATURE & FOOD','Farming','Health','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2018/EU-budget-environment-cold': ('News','NATURE & FOOD','Farming','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2018/EU-climate-change-second-shot': ('News','CLIMATE & ENERGY','ClimateChange','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2018/EU-court-Germany-cut-crap': ('News','NATURE & FOOD','Farming','WaterPollution','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2018/EU-court-protecting-people-nature-precedence': ('News','NATURE & FOOD','Pesticides','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2018/EU-farming-plan-disaster-environment': ('News','NATURE & FOOD','Farming','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2018/EU-overturns-barriers-to-rooftop-revolution-but-renewable-target-falls-short-of-serious-climate-action': ('News','CLIMATE & ENERGY','Renewables','EnergyTransition','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2018/EU-parliament-votes-renewable-energy': ('News','CLIMATE & ENERGY','Renewables','EnergyTransition','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2018/EU-subsidises-polluting-livestock-farms': ('News','NATURE & FOOD','Farming','WaterPollution','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2018/EU-vote-ban-three-bees-neonicotinoids-insecticides': ('News','NATURE & FOOD','Pesticides','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2018/European-Parliament-committee-restricts-controversial-subsidies-to-coal-gas-and-nuclear-plants': ('News','CLIMATE & ENERGY','FossilFuels','Nuclear','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2018/Greenpeace-activists-bare-their-lungs-for-clean-air': ('News','POLLUTION','AirPollution','Transport','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2018/halve-meat-protect-climate-nature-health': ('News','NATURE & FOOD','Farming','Food','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2018/investigation-EU-imports-Amazon-timber-fraud-Brazil': ('News','NATURE & FOOD','Forests','Justice','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2018/investigation-majority-agriculture-committee-linked-industry': ('News','NATURE & FOOD','Farming','Transparency','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2018/neonicotinoids-down-bee-killing-pesticides': ('News','NATURE & FOOD','Pesticides','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/News/2018/solar-panels-European-Parliament-renewables': ('News','CLIMATE & ENERGY','Renewables','','Migrate','Press Release'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/Bratislava-summit-Europe-at-a-crossroads': ('Publications','DEMOCRACY & EUROPE','EUaffairs','Democracy','Migrate','Letter'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/CETA-SandD-progressive-trade-principles': ('Publications','DEMOCRACY & EUROPE','Trade','','Migrate','Briefing'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/Civil-society-calls-for-a-new-Europe-for-people-and-planet': ('Publications','DEMOCRACY & EUROPE','EUaffairs','Democracy','Migrate','Statement'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/Commission-fails-to-regulate-new-GMOs-after-intense-US-lobbying': ('Publications','NATURE & FOOD','GMOs','Transparency','Migrate','Briefing'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/Commission-risks-putting-renewable-energy-transition-in-the-hands-of-reluctant-power-companies': ('Publications','CLIMATE & ENERGY','Renewables','EnergyTransition','Migrate','Briefing'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/Complaint-to-the-European-Commission-concerning-alleged-breach-of-Union-law': ('Publications','NATURE & FOOD','Forests','Justice','Migrate','Letter'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/From-ISDS-to-ICS-a-leopard-cant-change-its-spots': ('Publications','DEMOCRACY & EUROPE','Trade','Justice','Migrate','Briefing'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/Investor-protection-in-CETA': ('Publications','DEMOCRACY & EUROPE','Trade','Justice','Migrate','Report'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/Joint-NGOs-letter-to-Commissioner-Andriukaitis': ('Publications','NATURE & FOOD','Pesticides','','Migrate','Letter'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/Leaked-TiSA-texts-reveal-threats-to-climate-': ('Publications','DEMOCRACY & EUROPE','Trade','ClimateChange','Migrate','Report'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/letter-Commissioner-Andriukaitis-pesticides': ('Publications','NATURE & FOOD','Pesticides','','Migrate','Letter'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/letter-to-European-Commission-Hungarian-nuclear-regulator-plan': ('Publications','CLIMATE & ENERGY','Nuclear','','Migrate','Letter'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/letter-to-European-Commission-public-procurement-Paks-nuclear': ('Publications','CLIMATE & ENERGY','Nuclear','','Migrate','Letter'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/Media-briefing-Potential-for-citizen-produced-electricity-in-the-EU': ('Publications','CLIMATE & ENERGY','Renewables','EnergyTransition','Migrate','Briefing'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/New-techniques-of-genetic-engineering': ('Publications','NATURE & FOOD','GMOs','','Migrate','Briefing'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/NGOs-call-for-EU-to-perform-Fitness-Check-of-CAP': ('Publications','NATURE & FOOD','Farming','','Migrate','Letter'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/Paks-nuclear-project-complaint-on-state-aid': ('Publications','CLIMATE & ENERGY','Nuclear','','Migrate','Briefing'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/Paris-agreement-statement-from-the-Coalition-for-higher-ambition': ('Publications','CLIMATE & ENERGY','ClimateChange','','Migrate','Statement'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/Prosumer-Rights-Options-for-an-EU-legal-framework-post-2020': ('Publications','CLIMATE & ENERGY','Renewables','EnergyTransition','Migrate','Briefing'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/State-of-the-European-Union-after-Brexit-time-for-a-new-direction': ('Publications','DEMOCRACY & EUROPE','Democracy','EUaffairs','Migrate','Letter'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/Stepping-up-EU-action-to-protect-forests-is-not-optional-but-the-only-way-forward': ('Publications','NATURE & FOOD','Forests','ClimateChange','Migrate','Briefing'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/Tackling-illegal-logging-deforestation-and-forest-degradation': ('Publications','NATURE & FOOD','Forests','Justice','Migrate','Briefing'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/The-potential-of-energy-citizens-in-the-EU': ('Publications','CLIMATE & ENERGY','EnergyTransition','Renewables','Migrate','Report'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2016/TTIP-leaks-analysis': ('Publications','DEMOCRACY & EUROPE','Trade','Transparency','Migrate','Briefing'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2017/ECHA-response-heightens-concerns': ('Publications','NATURE & FOOD','Pesticides','','Migrate','Letter'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2017/letter-malmstrom-multilateral-investment-court': ('Publications','DEMOCRACY & EUROPE','Trade','Justice','Migrate','Letter'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2017/New-genetic-engineering-techniques': ('Publications','NATURE & FOOD','GMOs','','Migrate','Briefing'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2017/NGO-statement-deforestation-2017': ('Publications','NATURE & FOOD','Forests','','Migrate','Statement'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2017/Open-letter-on-the-independence-and-transparency-of-ECHAs-Risk-Assessment-Committee': ('Publications','NATURE & FOOD','Pesticides','Transparency','Migrate','Letter'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2017/Open-letter-presidents-EU-China-summit': ('Publications','CLIMATE & ENERGY','ClimateChange','','Migrate','Letter'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2017/Open-letter-to-Commission-President-Juncker-on-GMOs-and-democratic-principles': ('Publications','NATURE & FOOD','GMOs','Democracy','Migrate','Letter'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2017/Open-letter-to-Juncker-and-Timmermans-requesting-active-intervention-in-support-of-civil-society-and-democracy-in-Europe': ('Publications','DEMOCRACY & EUROPE','Democracy','EUaffairs','Migrate','Letter'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2017/Scenario-Sustainable-Europe-Citizens': ('Publications','DEMOCRACY & EUROPE','EUaffairs','PeoplePower','Migrate','Report'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2017/study-neonicotinoids-bees-greenhouses': ('Publications','NATURE & FOOD','Pesticides','Farming','Migrate','Report'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2017/Ten-principles-for-trade': ('Publications','DEMOCRACY & EUROPE','Trade','','Migrate','Briefing'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2017/The-EU-glyphosate-timeline': ('Publications','NATURE & FOOD','Pesticides','','Migrate','Briefing'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2017/The-Europe-we-want-Just-Sustainable-Democratic-and-Inclusive': ('Publications','DEMOCRACY & EUROPE','EUaffairs','Democracy','Migrate','Letter'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2018/investigation-CAP-promotes-pollution': ('Publications','NATURE & FOOD','Farming','WaterPollution','Migrate','Report'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2018/letter-commissioners-future-CAP': ('Publications','NATURE & FOOD','Farming','','Migrate','Letter'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2018/letter-presidents-animal-farming': ('Publications','NATURE & FOOD','Farming','','Migrate','Letter'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2018/Make-or-break-for-renewable-energy-in-Europe': ('Publications','CLIMATE & ENERGY','Renewables','EnergyTransition','Migrate','Briefing'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2018/NGO-letter-Juncker-neonicotinoids': ('Publications','NATURE & FOOD','Pesticides','','Migrate','Letter'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2018/ngo-letter-pest-committee': ('Publications','NATURE & FOOD','Pesticides','','Migrate','Letter'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2018/NGO-statement-on-deforestation': ('Publications','NATURE & FOOD','Forests','','Migrate','Statement'),
            'http://www.greenpeace.org/eu-unit/en/Publications/2018/out-of-balance-industry-links-AGRI-committee': ('Publications','CLIMATE & ENERGY','Farming','Transparency','Migrate','Report'),
            'https://www.greenpeace.org/eu-unit/en/News/2018/Stuck-in-1957-EU-court-rejects-challenge-to-state-aid-for-Hinkley-nuclear-plant': ('News','CLIMATE & ENERGY','Nuclear','Justice','Migrate','Press Release'),
            'https://www.greenpeace.org/eu-unit/en/News/2018/Unauthorised-new-GMO-field-trial-exposed-EU-hands-off': ('News','NATURE & FOOD','GMOs','','Migrate','Press Release'),
            'https://www.greenpeace.org/eu-unit/en/News/2018/New-GMOs-cannot-escape-testing-labelling-under-EU-law-EU-court-rules': ('News','CLIMATE & ENERGY','GMOs','Justice','Migrate','Press Release')
        }

        for url,data in start_urls.iteritems():
            post_type, categories, tags1, tags2, action, p4_post_type = data
            if ( post_type=='Publications' or post_type=='News' ):
                request = scrapy.Request(url, callback=self.parse_news, dont_filter='true')

            if ( action.lower()=='migrate' ):
                request.meta['status'] = 'publish'
            if ( action.lower()=='archive' ):
                request.meta['status'] = 'draft'
            request.meta['categories'] = categories
            request.meta['tags1'] = tags1
            request.meta['tags2'] = tags2
            request.meta['action'] = action
            request.meta['p4_post_type'] = p4_post_type
            request.meta['p4_title'] = ""
            yield request

    def parse_news(self, response):

        def extract_with_css(query):
            return response.css(query).extract_first()

        imagesA=response.xpath('//div[@class="text"]/div[not(@id) and not(@class)]//a[img]/@href').extract()
        imagesA_generated = list()
        for image_file in imagesA:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.org/',1)
            imagesA_generated.append(image_file)

        imagesB=response.xpath('//div[@class="text"]//img/@src').extract()
        if len(imagesB) == 0:
            imagesB = response.xpath('//div[@id="article"]//img/@src').extract()

        imagesB_generated = list()
        for image_file in imagesB:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.org/',1)
            # Custom fix for GPBR only.
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

        lead_text = response.xpath('//*[@id="content"]/div[3]/div/div[2]/div[1]/div/text()').extract()[0]
        body_text = response.xpath('//*[@id="content"]/div[3]/div/div[2]/div[2]').extract()[0]
        if body_text:
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.org/').replace('href="/', 'href="http://www.greenpeace.org/')
            body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            #body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)
            if lead_text:
                body_text = '<h4 class="leader">' + lead_text + '</h4>' + body_text
            body_text = body_text + response.xpath('//*[@id="content"]/div[3]/div/div[2]/p').extract_first()
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.org/').replace('href="/', 'href="http://www.greenpeace.org/')

        body_text = self.filter_post_content(body_text)

        subtitle = extract_with_css('div.article h2 span::text')
        if subtitle:
            body_text = '<h2>' + subtitle + '</h2><br />' + body_text

        #thumbnail = response.xpath('string(head//link[@rel="image_src"]/@href)').extract_first()

        date_field = response.css('div.article div.text span.author::text').re_first(r' - \s*(.*)')

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
                    '<a href="mailto:'+emailid.strip()+'" target="_blank">'+emailid.strip()+'</a>', body_text)

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

        p4_title = response.meta['p4_title']
        if (p4_title == ""):
            p4_title = extract_with_css('div.article h1 span::text')


        # To fix enlarge Images still leads to p3 issue  & small images issue - find and replace the src image link with anchor tag image link.
        delete_images_b = list()
        add_image_b     = list()
        for image_file_a in imagesA_generated:
            for image_file_b in imagesB_generated:
                filename_a = image_file_a.split("/")[-1]
                filename_b = image_file_b.split("/")[-1]

                if filename_a == filename_b:
                    #print "file names match " + filename_a
                    #body_text = body_text.replace(image_file_a, image_file_b)
                    body_text = body_text.replace(image_file_b, image_file_a)
                    delete_images_b.append(image_file_b)
                    add_image_b.append(image_file_a)

        # Remove small images from imagesB_generated list.
        for del_image_file_b in delete_images_b:
            imagesB_generated.remove(del_image_file_b)

        # Add enlarge images from imagesA_generated to imagesB_generated list .
        for add_image_file_a in add_image_b:
            imagesB_generated.append(add_image_file_a)
            # Remove from imagesA_generated.
            imagesA_generated.remove(add_image_file_a)

        yield {
            'type': response.meta['p4_post_type'],
            'p3_image_gallery': p3_image_gallery,
            'title': p4_title,
            #'subtitle': '',
            'author': 'Greenpeace European Unit',
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
            'url': response.url,
        }

    def filter_post_content(self, post_data):
        """
        # Filter the youtube video and add embed shortcode instead.
        post_data = re.sub(
            '\<iframe[width\=\"height0-9\s]*src\=\"([https]*\:\/\/www.youtube.com[a-zA-Z0-9\/\=\-\?\_]*)\"[\=\"a-zA-Z\/\-\s0-9]*\>[\\n\s]*(.*)[\\n\s]*\<\/iframe\>',
            '[embed]\g<1>[/embed]', post_data)

        # Search and replace youtube url with https.
        post_data = post_data.replace('http://www.youtube.com', 'https://www.youtube.com')
        """
        # Remove the <script> tags from content.
        post_data = re.sub(
            '<script[\s\S]type\=\"text\/javascript\"*?>[\s\S]*?<\/script>',
            '', post_data)

        return post_data

    def csv_writer(self, data, path):
        # Write data to a CSV file path
        with open(path, "a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(data)
