# -*- coding: utf-8 -*-
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


class JpMobileSpider(scrapy.Spider):
    name = 'jp_mobile'
    allowed_domains = ['greenpeace.jp']
    start_urls = ['http://greenpeace.jp/']
    base_url = 'http://greenpeace.jp/'

    custom_settings = {
        'ROBOTSTXT_OBEY': 0,
        'FEED_URI': 'gpjp_mobile_v2.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    authors = {
        u'パブリックエンゲージメント 林': 'ehayashi',
        u'プラスチックフリーチーム 石原': 'kishihara',
        u'エネルギーチーム 鈴木': 'ksuzuki',
        u'広報 城野': 'cjono',
        u'広報 松本': 'smatsumoto',
        u'広報チーム': '',
        u'ファンドレイジングチーム 江島': 'rejima',
        u'広報 土屋': 'atsuchiy',
        u'食と農業チーム 関根': 'asekine',
        u'ボランティア＆インターン': '',
        u'ファンドレイジングチーム 吉野': 'ryoshino',
        u'グリーンピース・ジャパン事務局長代理 ミリンダ・ブーンクオ': '',
        'Hisayo Takada, Energy Project Leader of Greenpeace Japan': 'htakada',
        u'エネルギーチーム': '',
        u'エネルギーチーム 石川': 'sishikawa'
    }

    def parse(self, response):

        # v2 production
        start_urls = {

            'http://greenpeace.jp/blog/plastic/3955/': ('Story', 'サステナブルに生きる', 'プラスチック', '', 'Migrate'),
            'http://greenpeace.jp/blog/ocean/3961/': ('Story', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/blog/energy/3991/': ('Story', 'サステナブルに生きる', '原発', '', 'Migrate'),
            'http://greenpeace.jp/blog/energy/4005/': ('Story', '自然を守る', '気候変動', '石炭', 'Migrate'),
            'http://greenpeace.jp/blog/energy/4020/': ('Story', 'サステナブルに生きる', '自然エネルギー', '', 'Migrate'),
            'http://greenpeace.jp/blog/plastic/4035/': ('Story', 'サステナブルに生きる', 'プラスチック', '', 'Migrate'),
            'http://greenpeace.jp/blog/energy/4049/': ('Story', 'サステナブルに生きる', '原発', '', 'Migrate'),
            'http://greenpeace.jp/blog/plastic/4076/': ('Story', 'サステナブルに生きる', 'プラスチック', '', 'Migrate'),
            'http://greenpeace.jp/blog/energy/4055/': ('Story', 'サステナブルに生きる', '自然エネルギー', '', 'Migrate'),
            'http://greenpeace.jp/blog/energy/4094/': ('Story', 'サステナブルに生きる', '自然エネルギー', '', 'Migrate'),
            'http://greenpeace.jp/blog/energy/4118/': ('Story', 'サステナブルに生きる', '自然エネルギー', '', 'Migrate'),
            'http://greenpeace.jp/blog/plastic/3979/': ('Story', 'サステナブルに生きる', 'プラスチック', '', 'Migrate'),
            'http://greenpeace.jp/blog/energy/4139/': ('Story', '自然を守る', '気候変動', '海洋生態系', 'Migrate'),
            'http://greenpeace.jp/blog/energy/4129/': ('Story', 'サステナブルに生きる', '自然エネルギー', '食と農業', 'Migrate'),
            'http://greenpeace.jp/blog/energy/4138/': ('Story', 'サステナブルに生きる', '自然エネルギー', '', 'Migrate'),
            'http://greenpeace.jp/blog/forest/4174/': ('Story', '自然を守る', '森林', '', 'Migrate'),
            'http://greenpeace.jp/blog/forest/4182/': ('Story', '自然を守る', '森林', '', 'Migrate'),
            'http://greenpeace.jp/blog/plastic/4192/': ('Story', 'サステナブルに生きる', 'プラスチック', '', 'Migrate'),
            'http://greenpeace.jp/blog/event/4205/': ('Story', 'サステナブルに生きる', '原発', '', 'Migrate'),
            'http://greenpeace.jp/blog/energy/4213/': ('Story', '自然を守る', '気候変動', '石炭', 'Migrate'),
            'http://greenpeace.jp/blog/plastic/3931/': ('Story', 'サステナブルに生きる', 'プラスチック', '', 'Migrate'),
            'http://greenpeace.jp/blog/plastic/3899/': ('Story', 'サステナブルに生きる', 'プラスチック', 'イベント', 'Migrate'),
            'http://greenpeace.jp/blog/plastic/3889/': ('Story', 'サステナブルに生きる', 'プラスチック', '船', 'Migrate'),
            'http://greenpeace.jp/blog/plastic/607/': ('Story', 'サステナブルに生きる', 'プラスチック', '', 'Migrate'),
            'http://greenpeace.jp/blog/plastic/870/': ('Story', 'サステナブルに生きる', 'プラスチック', '', 'Migrate'),
            'http://greenpeace.jp/blog/plastic/2456/': ('Story', 'サステナブルに生きる', 'プラスチック', '', 'Migrate'),
            'http://greenpeace.jp/blog/event/3926/': ('Story', 'サステナブルに生きる', '原発', 'イベント', 'Migrate'),
            'http://greenpeace.jp/blog/event/3849/': ('Story', 'サステナブルに生きる', '原発', 'イベント', 'Migrate'),
            'http://greenpeace.jp/blog/event/2447/': ('Story', 'つながる', 'イベント', 'プラスチック', 'Migrate'),
            'http://greenpeace.jp/blog/event/2440/': ('Story', 'つながる', '平和と民主主義', 'イベント', 'Migrate'),
            'http://greenpeace.jp/blog/event/2714/': ('Story', 'サステナブルに生きる', '自然エネルギー', 'イベント', 'Migrate'),
            'http://greenpeace.jp/blog/ocean/3682/': ('Story', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/blog/ocean/3323/': ('Story', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/blog/ocean/3325/': ('Story', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/blog/ocean/2764/': ('Story', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/blog/ocean/2806/': ('Story', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/blog/ocean/2822/': ('Story', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/blog/food/3405/': ('Story', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/blog/food/877/': ('Story', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/blog/food/885/': ('Story', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/blog/food/2783/': ('Story', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/blog/food/2830/': ('Story', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/blog/food/3260/': ('Story', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/blog/energy/3838/': ('Story', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/blog/energy/3824/': ('Story', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/blog/energy/3816/': ('Story', 'サステナブルに生きる', '原発', '', 'Migrate'),
            'http://greenpeace.jp/blog/energy/3797/': ('Story', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/blog/energy/3674/': ('Story', 'サステナブルに生きる', '原発', '', 'Migrate'),
            'http://greenpeace.jp/blog/energy/3666/': ('Story', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/blog/good_life/2675/': ('Story', '自然を守る', '有害物質', 'グリーンピースについて', 'Migrate'),
            'http://greenpeace.jp/blog/good_life/2466/': ('Story', '自然を守る', '有害物質', 'プラスチック', 'Migrate'),
            'http://greenpeace.jp/blog/good_life/863/': ('Story', 'サステナブルに生きる', '食と農業', '気候変動', 'Migrate'),
            'http://greenpeace.jp/blog/good_life/2537/': ('Story', 'サステナブルに生きる', '食と農業', '気候変動', 'Migrate'),
            'http://greenpeace.jp/blog/good_life/3724/': ('Story', 'サステナブルに生きる', 'イベント', '', 'Migrate'),
            'http://greenpeace.jp/blog/others/2759/': ('Story', 'つながる', '平和と民主主義', '', 'Migrate'),
            'http://greenpeace.jp/blog/peace/3789/': ('Story', 'つながる', '平和と民主主義', '船', 'Migrate'),
            'http://greenpeace.jp/blog/peace/3205/': ('Story', 'つながる', '平和と民主主義', 'グリーンピースについて', 'Migrate'),
            'http://greenpeace.jp/blog/forest/3709/': ('Story', '自然を守る', '森林', '', 'Migrate'),
            'http://greenpeace.jp/blog/forest/3689/': ('Story', '自然を守る', '森林', '', 'Migrate'),
            'http://greenpeace.jp/release/4162/': ('Press Release', '自然を守る', '森林', '', 'Migrate'),
            'http://greenpeace.jp/release/4158/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/4091/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/4065/': ('Press Release', 'サステナブルに生きる', '石炭', '気候変動', 'Migrate'),
            'http://greenpeace.jp/release/4047/': ('Press Release', 'サステナブルに生きる', 'プラスチック', '', 'Migrate'),
            'http://greenpeace.jp/release/4001/': ('Press Release', 'サステナブルに生きる', 'プラスチック', '', 'Migrate'),
            'http://greenpeace.jp/release/3949/': ('Press Release', 'サステナブルに生きる', 'プラスチック', '', 'Migrate'),
            'http://greenpeace.jp/release/3945/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/3938/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/3919/': ('Press Release', 'サステナブルに生きる', '石炭', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/3917/': ('Press Release', 'サステナブルに生きる', 'プラスチック', '', 'Migrate'),
            'http://greenpeace.jp/release/3861/': ('Press Release', 'サステナブルに生きる', '気候変動', '石炭', 'Migrate'),
            'http://greenpeace.jp/release/3854/': ('Press Release', 'サステナブルに生きる', 'プラスチック', '海洋生態系', 'Migrate'),
            'http://greenpeace.jp/release/3807/': ('Press Release', '自然を守る', '海洋生態系', 'プラスチック', 'Migrate'),
            'http://greenpeace.jp/release/3804/': ('Press Release', '自然を守る', '森林', '', 'Migrate'),
            'http://greenpeace.jp/release/3707/': ('Press Release', '自然を守る', '森林', '', 'Migrate'),
            'http://greenpeace.jp/release/3681/': ('Press Release', 'サステナブルに生きる', '石炭', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/3671/': ('Press Release', 'サステナブルに生きる', '石炭', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/3665/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/3662/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/3650/': ('Press Release', 'サステナブルに生きる', '自然エネルギー', '気候変動', 'Migrate'),
            'http://greenpeace.jp/release/3612/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/3605/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/3619/': ('Press Release', '自然を守る', '気候変動', '石炭', 'Migrate'),
            'http://greenpeace.jp/release/3553/': ('Press Release', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/release/3419/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/3320/': ('Press Release', 'サステナブルに生きる', '石炭', '気候変動', 'Migrate'),
            'http://greenpeace.jp/release/2750/': ('Press Release', '自然を守る', '気候変動', '石炭', 'Migrate'),
            'http://greenpeace.jp/release/2846/': ('Press Release', 'サステナブルに生きる', '石炭', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/2843/': ('Press Release', 'サステナブルに生きる', '石炭', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/2426/': ('Press Release', '自然を守る', '気候変動', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/2395/': ('Press Release', 'サステナブルに生きる', '有害物質', '', 'Migrate'),
            'http://greenpeace.jp/release/2305/': ('Press Release', 'サステナブルに生きる', '自然エネルギー', '原発', 'Migrate'),
            'http://greenpeace.jp/release/2329/': ('Press Release', 'サステナブルに生きる', '自然エネルギー', '原発', 'Migrate'),
            'http://greenpeace.jp/release/2307/': ('Press Release', 'サステナブルに生きる', '石炭', '気候変動', 'Migrate'),
            'http://greenpeace.jp/release/2330/': ('Press Release', 'サステナブルに生きる', '石炭', '気候変動', 'Migrate'),
            'http://greenpeace.jp/release/2333/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/2332/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/2335/': ('Press Release', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/release/2337/': ('Press Release', 'サステナブルに生きる', '石炭', '森林', 'Migrate'),
            'http://greenpeace.jp/release/2336/': ('Press Release', 'サステナブルに生きる', '石炭', '森林', 'Migrate'),
            'http://greenpeace.jp/release/2338/': ('Press Release', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/release/2339/': ('Press Release', 'サステナブルに生きる', '石炭', '森林', 'Migrate'),
            'http://greenpeace.jp/release/2341/': ('Press Release', 'サステナブルに生きる', '自然エネルギー', '', 'Migrate'),
            'http://greenpeace.jp/release/2340/': ('Press Release', 'サステナブルに生きる', '石炭', '森林', 'Migrate'),
            'http://greenpeace.jp/release/2342/': ('Press Release', 'サステナブルに生きる', 'プラスチック', '海洋生態系', 'Migrate'),
            'http://greenpeace.jp/release/2343/': ('Press Release', 'サステナブルに生きる', 'プラスチック', '海洋生態系', 'Migrate'),
            'http://greenpeace.jp/release/2345/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/2344/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/2348/': ('Press Release', '自然を守る', '海洋生態系', 'プラスチック', 'Migrate'),
            'http://greenpeace.jp/release/2349/': ('Press Release', 'サステナブルに生きる', 'プラスチック', '海洋生態系', 'Migrate'),
            'http://greenpeace.jp/release/2350/': ('Press Release', 'サステナブルに生きる', '石炭', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/2351/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/2352/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/2353/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/2354/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/2356/': ('Press Release', 'サステナブルに生きる', '石炭', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/2355/': ('Press Release', 'サステナブルに生きる', '石炭', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/2358/': ('Press Release', 'サステナブルに生きる', '石炭', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/2357/': ('Press Release', 'サステナブルに生きる', '石炭', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/2359/': ('Press Release', 'サステナブルに生きる', '石炭', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/2361/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/2360/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/2362/': ('Press Release', 'サステナブルに生きる', '石炭', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/2363/': ('Press Release', 'サステナブルに生きる', '石炭', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/2365/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/2368/': ('Press Release', 'サステナブルに生きる', '石炭', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/2367/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/2366/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/2847/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/2856/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/2864/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/2862/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/2860/': ('Press Release', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/release/2865/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/2867/': ('Press Release', '自然を守る', '海洋生態系', '有害物質', 'Migrate'),
            'http://greenpeace.jp/release/2868/': ('Press Release', 'サステナブルに生きる', '気候変動', '有害物質', 'Migrate'),
            'http://greenpeace.jp/release/2874/': ('Press Release', '自然を守る', '有害物質', '海洋生態系', 'Migrate'),
            'http://greenpeace.jp/release/2873/': ('Press Release', '自然を守る', '有害物質', '海洋生態系', 'Migrate'),
            'http://greenpeace.jp/release/2875/': ('Press Release', 'サステナブルに生きる', '自然エネルギー', '', 'Migrate'),
            'http://greenpeace.jp/release/1072/': ('Press Release', '自然を守る', '有害物質', '海洋生態系', 'Migrate'),
            'http://greenpeace.jp/release/1073/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1074/': ('Press Release', '自然を守る', '気候変動', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1076/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/1075/': ('Press Release', '自然を守る', '海洋生態系', '有害物質', 'Migrate'),
            'http://greenpeace.jp/release/2877/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/1077/': ('Press Release', '自然を守る', '気候変動', '', 'Migrate'),
            'http://greenpeace.jp/release/2879/': ('Press Release', '自然を守る', '気候変動', '', 'Migrate'),
            'http://greenpeace.jp/release/1078/': ('Press Release', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/release/2881/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1079/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1080/': ('Press Release', 'サステナブルに生きる', '自然エネルギー', '気候変動', 'Migrate'),
            'http://greenpeace.jp/release/2883/': ('Press Release', '自然を守る', '気候変動', '', 'Migrate'),
            'http://greenpeace.jp/release/2885/': ('Press Release', '自然を守る', '気候変動', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1083/': ('Press Release', '自然を守る', '気候変動', '', 'Migrate'),
            'http://greenpeace.jp/release/1082/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1081/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1084/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/2888/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/2894/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/2895/': ('Press Release', '自然を守る', '森林', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1085/': ('Press Release', '自然を守る', '森林', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1086/': ('Press Release', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/release/2897/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/2899/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/2901/': ('Press Release', 'サステナブルに生きる', '石炭', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1087/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/1088/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1089/': ('Press Release', 'サステナブルに生きる', '自然エネルギー', '', 'Migrate'),
            'http://greenpeace.jp/release/2907/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1090/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1092/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1093/': ('Press Release', 'グリーンピースとは', 'グリーンピースについて', '', 'Migrate'),
            'http://greenpeace.jp/release/1094/': ('Press Release', 'つながる', '平和と民主主義', '', 'Migrate'),
            'http://greenpeace.jp/release/1095/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/1096/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/1097/': ('Press Release', '自然を守る', '海洋生態系', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1098/': ('Press Release', '自然を守る', '海洋生態系', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1099/': ('Press Release', '自然を守る', '森林', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1100/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/1101/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/1102/': ('Press Release', '自然を守る', '気候変動', '', 'Migrate'),
            'http://greenpeace.jp/release/2909/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1103/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/2912/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1104/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1105/': ('Press Release', 'サステナブルに生きる', '自然エネルギー', '', 'Migrate'),
            'http://greenpeace.jp/release/2916/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1106/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1107/': ('Press Release', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/release/1108/': ('Press Release', 'つながる', '平和と民主主義', '', 'Migrate'),
            'http://greenpeace.jp/release/2920/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/1109/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/1110/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/2924/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1111/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1112/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/2927/': ('Press Release', '自然を守る', '気候変動', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1114/': ('Press Release', '自然を守る', '気候変動', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1113/': ('Press Release', '自然を守る', '気候変動', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1115/': ('Press Release', '自然を守る', '森林', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1116/': ('Press Release', '自然を守る', '気候変動', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1117/': ('Press Release', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/release/2929/': ('Press Release', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/release/2931/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/2930/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1118/': ('Press Release', 'つながる', '平和と民主主義', '', 'Migrate'),
            'http://greenpeace.jp/release/1119/': ('Press Release', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/release/1120/': ('Press Release', '自然を守る', '海洋生態系', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1121/': ('Press Release', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/release/1122/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/2934/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1123/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1124/': ('Press Release', '自然を守る', '気候変動', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/2938/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1125/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/2940/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1126/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1127/': ('Press Release', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/release/2945/': ('Press Release', '自然を守る', '海洋生態系', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1128/': ('Press Release', '自然を守る', '海洋生態系', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/2949/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1130/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/2956/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1131/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1132/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/1133/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/2960/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1135/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1134/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1136/': ('Press Release', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/release/1137/': ('Press Release', '自然を守る', '海洋生態系', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1138/': ('Press Release', '自然を守る', '有害物質', '', 'Migrate'),
            'http://greenpeace.jp/release/1139/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/1140/': ('Press Release', '自然を守る', '森林', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1141/': ('Press Release', '自然を守る', '森林', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1142/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1144/': ('Press Release', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/release/1143/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1145/': ('Press Release', '自然を守る', '森林', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1146/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/1147/': ('Press Release', '自然を守る', '有害物質', '', 'Migrate'),
            'http://greenpeace.jp/release/1148/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1150/': ('Press Release', '自然を守る', '気候変動', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1149/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/1151/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/1152/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1153/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1155/': ('Press Release', '自然を守る', '気候変動', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1157/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1160/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/1158/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1161/': ('Press Release', 'サステナブルに生きる', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/1162/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1164/': ('Press Release', '自然を守る', '森林', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1166/': ('Press Release', '自然を守る', '森林', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1167/': ('Press Release', '自然を守る', '森林', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1168/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1171/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/1172/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/1173/': ('Press Release', 'グリーンピースについて', 'グリーンピースについて', '', 'Migrate'),
            'http://greenpeace.jp/release/1174/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1176/': ('Press Release', '自然を守る', '森林', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1178/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1181/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1179/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/1182/': ('Press Release', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/release/1183/': ('Press Release', 'サステナブルに生きる', '有害物質', '', 'Migrate'),
            'http://greenpeace.jp/release/1184/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1186/': ('Press Release', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/release/1188/': ('Press Release', 'サステナブルに生きる', '原発', '', 'Migrate'),
            'http://greenpeace.jp/release/1187/': ('Press Release', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/release/1190/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1191/': ('Press Release', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/release/1192/': ('Press Release', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/release/1194/': ('Press Release', '自然を守る', '気候変動', '', 'Migrate'),
            'http://greenpeace.jp/release/1193/': ('Press Release', '自然を守る', '気候変動', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1196/': ('Press Release', 'つながる', '平和と民主主義', '', 'Migrate'),
            'http://greenpeace.jp/release/1197/': ('Press Release', 'サステナブルに生きる', '石炭', '', 'Migrate'),
            'http://greenpeace.jp/release/1199/': ('Press Release', 'サステナブルに生きる', '石炭', '', 'Migrate'),
            'http://greenpeace.jp/release/1201/': ('Press Release', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/release/1202/': ('Press Release', 'サステナブルに生きる', '自然エネルギー', '', 'Migrate'),
            'http://greenpeace.jp/release/1203/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1205/': ('Press Release', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/release/1206/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1208/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1209/': ('Press Release', 'サステナブルに生きる', '自然エネルギー', '', 'Migrate'),
            'http://greenpeace.jp/release/1210/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1211/': ('Press Release', 'つながる', '平和と民主主義', '', 'Migrate'),
            'http://greenpeace.jp/release/1212/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1214/': ('Press Release', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/release/1218/': ('Press Release', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/release/1217/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1220/': ('Press Release', 'サステナブルに生きる', '原発', '平和と民主主義', 'Migrate'),
            'http://greenpeace.jp/release/1225/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1227/': ('Press Release', 'サステナブルに生きる', '原発', 'グリーンピースについて', 'Migrate'),
            'http://greenpeace.jp/release/1226/': ('Press Release', 'サステナブルに生きる', '自然エネルギー', '', 'Migrate'),
            'http://greenpeace.jp/release/1229/': ('Press Release', 'サステナブルに生きる', '原発', 'グリーンピースについて', 'Migrate'),
            'http://greenpeace.jp/release/1231/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1232/': ('Press Release', '自然を守る', '海洋生態系', '', 'Migrate'),
            'http://greenpeace.jp/release/1233/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1234/': ('Press Release', 'サステナブルに生きる', '原発', '自然エネルギー', 'Migrate'),
            'http://greenpeace.jp/release/1235/': ('Press Release', 'サステナブルに生きる', '食と農業', '', 'Migrate'),
            'http://greenpeace.jp/release/1236/': ('Press Release', 'つながる', '平和と民主主義', '', 'Migrate'),
        }

        for url, data in start_urls.iteritems():
            post_type, categories, tags1, tags2, action = data
            if (post_type == 'Story'):
                request = scrapy.Request(url, callback=self.parse_blog, dont_filter='true')
            elif (post_type == 'Press Release'):
                request = scrapy.Request(url, callback=self.parse_release, dont_filter='true')

            if (action.lower() == 'migrate'):
                request.meta['status'] = 'publish'
            if (action.lower() == 'archive'):
                request.meta['status'] = 'draft'
            request.meta['categories'] = categories
            request.meta['tags'] = '|'.join([tags1, tags2])
            request.meta['action'] = action
            request.meta['p4_post_type'] = post_type
            yield request

    def parse_blog(self, response):

        # parse post content
        body_text = response.xpath('//div[@class="contents"]').extract_first()

        # parse post date
        post_title = response.css('section.text h1::text').extract_first()

        # parse post date
        date_field = response.css('section.text .date::text').extract_first()
        date_field = date_field.replace('.', '-')

        # parse author
        author_override = response.xpath('//section["writer"]//div[@class="text"]/h4[1]/text()').extract_first().strip()
        author_override = author_override.replace('  ', ' ')
        author_username = ''

        for k in self.authors:
            if author_override in k:
                author_username = self.authors[k]
        if author_username.strip() is not '':
            author_override = ''

        # parse featured image
        fimage = response.xpath('//main["detail"]/img[1]/@src').extract_first()
        fimage_tag = response.xpath('//main["detail"]/img[1]').extract_first()
        if fimage.strip() == '/img/no-image.png':
            fimage = ''
            fimage_tag = ''


        # parse content images
        imagesA=response.xpath('//div[@class="contents"]//img/@src').extract()
        imagesA_generated = list()
        for image_file in imagesA:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/', self.base_url,1)
            imagesA_generated.append(image_file)

        images_concatenated = '|'.join(imagesA_generated)


        # parse content documents
        pdfFiles=response.css('div.contents a[href$=".pdf"]::attr(href)').extract()
        pdf_files_generated = list()
        for pdf_file in pdfFiles:
            print pdf_file
            if (pdf_file.startswith('/')):
                pdf_file = pdf_file.replace('/', self.base_url,1)
                print pdf_file
            pdf_files_generated.append(pdf_file)
            print pdf_files_generated

        yield {
            'type': response.meta['p4_post_type'],
            'title': post_title,
            'featured_image': fimage,
            'featured_image_tag': fimage_tag,
            'date': date_field,
            'post_content':  body_text,
            'url': response.url,
            'images': images_concatenated.replace('\r', '').replace('\n', '').strip(),
            'pdfs': pdf_files_generated,
            'author_override': author_override,
            'author_username': author_username,
            'categories': response.meta['categories'],
            'tags': response.meta['tags'],
            'status': response.meta['status'],
        }

    def parse_release(self, response):

        # parse post content
        body_text = response.css('div.contents').extract_first()

        # parse post date
        post_title = response.css('section.text h1::text').extract_first()

        # parse post date
        date_field = response.css('section.text .date::text').extract_first()
        date_field = date_field.replace('.', '-')

        # parse featured image
        fimage = response.xpath('//main["detail"]/div/img[1]/@src').extract_first()
        fimage_tag = response.xpath('//main["detail"]/div/img[1]').extract_first()
        if fimage.strip() == '/img/no-image.png':
            fimage = ''
            fimage_tag = ''


        author_override = 'Greenpeace Japan'

        # parse content images
        imagesA=response.xpath('//div[@class="contents"]//img/@src').extract()
        imagesA_generated = list()
        for image_file in imagesA:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/', self.base_url,1)
            imagesA_generated.append(image_file)

        images_concatenated = '|'.join(imagesA_generated)


        # parse content documents
        pdfFiles=response.css('div.contents a[href$=".pdf"]::attr(href)').extract()
        pdf_files_generated = list()
        for pdf_file in pdfFiles:
            print pdf_file
            if (pdf_file.startswith('/')):
                pdf_file = pdf_file.replace('/', self.base_url,1)
                print pdf_file
            pdf_files_generated.append(pdf_file)
            print pdf_files_generated

        yield {
            'type': response.meta['p4_post_type'],
            'title': post_title,
            'featured_image': fimage,
            'featured_image_tag': fimage_tag,
            'date': date_field,
            'post_content':  body_text,
            'url': response.url,
            'images': images_concatenated,
            'pdfs': pdf_files_generated,
            'author_override': author_override,
            'categories': response.meta['categories'],
            'tags': response.meta['tags'],
            'status': response.meta['status'],
        }