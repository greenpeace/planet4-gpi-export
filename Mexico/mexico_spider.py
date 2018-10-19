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
        'FEED_URI': 'gpmx_staging_v1.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    __connector_csv_filename = "connector_v2_final.csv"
    __connector_csv_log_file = "connector_csv_log_v2"

    def start_requests(self):
        # v1
        start_urls = {
            'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/sargazo/blog/61768/':('Blog','Biodiversidad','Océanos','','','news-list','Migrate'),
            'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/lunessincarne-ensalada-de-nopales/blog/61767/':('Blog','Comunidad','ConsumoResponsable','Activismo ','','news-list','Migrate'),
            'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/aprende-a-hacer-tu-propia-pasta-de-dientes/blog/61751/':('Blog','Comunidad','ConsumoResponsable','Activismo ','','news-list','Migrate'),
            'http://www.greenpeace.org/mexico/es/Noticias/2018/Mayo/Excelentes-noticias-Veracruz-camina-hacia-un-futuro-libre-de-plasticos/':('Blog','Biodiversidad','Océanos','Plásticos','','article','Migrate'),
            'http://www.greenpeace.org/mexico/es/Noticias/2018/Marzo/La-mala-calidad-del-aire-afecta-a-todo-Mexico/':('Blog','Cambio Climático','ContaminaciónDelAire','','','article','Migrate'),
            'http://www.greenpeace.org/mexico/es/Noticias/2018/Enero/La-bioseguridad-en-Mexico-no-existe-Greenpeace/':('Blog','Biodiversidad','Transgénicos','','','article','Migrate'),
            'http://www.greenpeace.org/mexico/es/Footer/Descargas/reports/2018/No-apto-para-pulmones-pequenos-Diagnostico-de-calidad-del-aire-y-el-derecho-de-ninas-ninos-y-adolescentes-al-aire-limpio/':('Publication','Cambio Climático','ContaminaciónDelAire','Transporte','','article','Migrate'),
            'http://www.greenpeace.org/mexico/es/Footer/Descargas/reports/2018/No-apto-para-pulmones-pequenos/':('Publication','Cambio Climático','ContaminaciónDelAire','Transporte','','article','Migrate'),
            'http://www.greenpeace.org/mexico/es/Footer/Descargas/reports/2018/EL-AIRE-QUE-RESPIRO/':('Publication','Cambio Climático','ContaminaciónDelAire','Transporte','','article','Migrate'),
            'http://www.greenpeace.org/mexico/es/Prensa1/2018/Octubre/Coca-Cola-PepsiCo-y-Nestle-los-mayores-contaminadores-plasticos-en-el-mundo-revelan-limpiezas-y-auditorias-de-marca-/':('Press Release','Biodiversidad','Plásticos','Océanos','','article','Migrate'),
            'http://www.greenpeace.org/mexico/es/Prensa1/2018/Septiembre/Funcionarios-del-Senasica-y-la-Cofepris-atentan-contra-la-bioseguridad-del-pais-AMLO-no-debe-ratificarlos-en-sus-cargos-Greenpeace-/':('Press Release','Biodiversidad','Transgénicos','','','article','Migrate'),
            'http://www.greenpeace.org/mexico/es/Prensa1/2018/Septiembre/Greenpeace-demanda-justicia-para-Berta-Caceres-y-recuerda-que-los-autores-intelectuales-aun-estan-libres/':('Press Release','Comunidad','Activismo','','','article','Migrate'),
            'http://www.greenpeace.org/mexico/es/Noticias/2014/Diciembre/El-poder-de-la-gente-para-proteger-al-maiz-mexicano/':('Press Release','Biodiversidad','Transgénicos','','','article','Migrate'),
            'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/5-razones-por-las-que-debemos-liberar-la-ciud/blog/61935/':('Blog','Cambio Climático','Transporte','ContaminaciónDelAire','','news-list','Migrate')
        }


         # v2
        start_urls = {
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/sargazo/blog/61768/':('Blog','Biodiversidad','Océanos','','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/lunessincarne-ensalada-de-nopales/blog/61767/':('Blog','Comunidad','ConsumoResponsable','Activismo ','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/aprende-a-hacer-tu-propia-pasta-de-dientes/blog/61751/':('Blog','Comunidad','ConsumoResponsable','Activismo ','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Noticias/2018/Mayo/Excelentes-noticias-Veracruz-camina-hacia-un-futuro-libre-de-plasticos/':('Blog','Biodiversidad','Océanos','Plásticos','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Noticias/2018/Marzo/La-mala-calidad-del-aire-afecta-a-todo-Mexico/':('Blog','Cambio Climático','ContaminaciónDelAire','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Noticias/2018/Enero/La-bioseguridad-en-Mexico-no-existe-Greenpeace/':('Blog','Biodiversidad','Transgénicos','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Footer/Descargas/reports/2018/No-apto-para-pulmones-pequenos-Diagnostico-de-calidad-del-aire-y-el-derecho-de-ninas-ninos-y-adolescentes-al-aire-limpio/':('Publication','Cambio Climático','ContaminaciónDelAire','Transporte','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Footer/Descargas/reports/2018/No-apto-para-pulmones-pequenos/':('Publication','Cambio Climático','ContaminaciónDelAire','Transporte','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Footer/Descargas/reports/2018/EL-AIRE-QUE-RESPIRO/':('Publication','Cambio Climático','ContaminaciónDelAire','Transporte','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Octubre/Coca-Cola-PepsiCo-y-Nestle-los-mayores-contaminadores-plasticos-en-el-mundo-revelan-limpiezas-y-auditorias-de-marca-/':('Press Release','Biodiversidad','Plásticos','Océanos','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Septiembre/Funcionarios-del-Senasica-y-la-Cofepris-atentan-contra-la-bioseguridad-del-pais-AMLO-no-debe-ratificarlos-en-sus-cargos-Greenpeace-/':('Press Release','Biodiversidad','Transgénicos','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Septiembre/Greenpeace-demanda-justicia-para-Berta-Caceres-y-recuerda-que-los-autores-intelectuales-aun-estan-libres/':('Press Release','Comunidad','Activismo','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Noticias/2014/Diciembre/El-poder-de-la-gente-para-proteger-al-maiz-mexicano/':('Press Release','Biodiversidad','Transgénicos','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/5-razones-por-las-que-debemos-liberar-la-ciud/blog/61935/':('Blog','Cambio Climático','Transporte','ContaminaciónDelAire','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/estas-10-empresas-estn-llenando-el-planeta-de/blog/61942/':('Blog','Biodiversidad','Plásticos','Océanos','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/pendar-ms-alla-del-automvil/blog/61929/':('Blog','Cambio Climático','Transporte','','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/descubre-cul-es-el-mejor-transporte-para-move/blog/61885/':('Blog','Cambio Climático','Transporte','','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/justicia-para-berta-cceres-justicia-para-el-p/blog/61873/':('Blog','Comunidad','Activismo ','','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/3-cosas-que-tienen-que-cambiar-en-mxico-para-/blog/61864/':('Blog','Cambio Climático','ContaminaciónDelAire','Transporte','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/cmo-abr-los-ojos-respecto-al-problema-de-la-c/blog/61859/':('Blog','Biodiversidad','Océanos','Plásticos','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/llvelo-llvelo-greenpeace-distribuye-aire-enva/blog/61856/':('Blog','Cambio Climático','ContaminaciónDelAire','','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/lunessincarne-pozole-vegetariano/blog/61854/':('Blog','Comunidad','ConsumoResponsable','Activismo','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/lo-hicimos-san-luis-potos-prohibe-bolsas-y-po/blog/61853/':('Blog','Biodiversidad','Océanos','Plásticos','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/san-luis-potos-puede-ser-el-prximo-estado-en-/blog/61843/':('Blog','Biodiversidad','Océanos','Plásticos','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/tortugas-ecocidio-y-poltica-ambiental/blog/61834/':('Blog','Biodiversidad','Océanos','','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/el-da-en-que-la-bici-nos-ayud-a-levantarnos/blog/61891/':('Blog','Cambio Climático','Activismo','Transporte','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/en-bici-la-vida-es-ms-sabrosa/blog/61898/':('Blog','Cambio Climático','Transporte','Activismo','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/alas-del-paraso-desplegadas-para-huir/blog/61899/':('Blog','Biodiversidad','Deforestación','','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/cmo-moverte-en-la-ciudad-de-una-manera-buena-/blog/61902/':('Blog','Cambio Climático','Transporte','','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/estas-marcas-estn-detrs-de-la-deforestacin-pa/blog/61903/':('Blog','Biodiversidad','Deforestación','','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/parar-la-produccin-de-autos-contaminantes-par/blog/61913/':('Blog','Cambio Climático','Transporte','ContaminaciónDelAire','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/supenden-juicio-contra-inculpados-en-asesinat/blog/61911/':('Blog','Comunidad','Activismo ','','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/pendar-ms-alla-del-automvil/blog/61929/':('Blog','Cambio Climático','Transporte','ContaminaciónDelAire','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/5-razones-por-las-que-debemos-liberar-la-ciud/blog/61935/':('Blog','Cambio Climático','Transporte','ContaminaciónDelAire','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/qu-marcas-estn-en-tu-alacena-haz-una-auditora/blog/61824/':('Blog','Biodiversidad','Plásticos','Océanos','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/imagina-que-un-da-el-gobirno-te-informa-y-con/blog/61807/':('Blog','Comunidad','Activismo ','','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/lunessincarne-sopa-tarasca/blog/61806/':('Blog','Comunidad','ConsumoResponsable','Activismo ','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/10-cosas-que-tal-vez-no-sabas-sobre-los-orang/blog/61799/':('Blog','Biodiversidad','Deforestación','','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/monsanto-en-el-banquillo-de-los-acusados/blog/61835/':('Blog','Biodiversidad','Transgénicos','Activismo ','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/esta-es-rang-tan-y-su-hogar-esta-amenazado-po/blog/61791/':('Blog','Biodiversidad','Deforestación','Activismo ','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/llamamos-para-preguntar-por-el-trolebici-y-es/blog/61789/':('Blog','Cambio Climático','Transporte','Activismo ','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/una-experiencia-maravillosa/blog/61787/':('Blog','Biodiversidad','Océanos','Plásticos','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/vivir-sin-plstico-y-cules-son-las-alternativa/blog/61782/':('Blog','Biodiversidad','Océanos','Plásticos','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/te-decimos-cmo-organizar-una-limpieza-comunit/blog/61788/':('Blog','Biodiversidad','Océanos','Plásticos','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/estamos-trabajando-por-un-aire-limpio/blog/61779/':('Blog','Cambio Climático','ContaminaciónDelAire','','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/da-interamericano-de-la-calidad-del-aire-algo/blog/61778/':('Blog','Cambio Climático','ContaminaciónDelAire','Transporte','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Noticias/2018/Marzo/Dia-Internacional-de-la-Mujer/':('Blog','Comunidad','Activismo','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Noticias/2018/Abril/Positiva-apertura-de-JUCOPO-a-consultar-Ley-General-de-Biodiversidad-vigilaremos-que-no-haya-simulacion-del-proceso-organizaciones/':('Blog','Biodiversidad','Transgénicos','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Abril/Nestle-fracasa-en-como-abordar-su-problema-de-plasticos-de-un-solo-uso/':('Blog','Biodiversidad','Océanos','Plásticos','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Noticias/2018/Febrero/En-pie-de-lucha-contra-los-transgenicos/':('Blog','Biodiversidad','Transgénicos','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Noticias/2018/Agosto-2018/Porque-no-es-suficiente-Greenpeace-pide-a-PG-Mexico-ir-mas-alla-del-reciclaje-/':('Blog','Biodiversidad','Océanos','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Noticias/2018/Febrero/Autoridades-acuerdan-con-ONG-y-comunidad-cientifica-blindar-el-refugio-de-las-ultimas-vaquitas-marinas--del-mundo/':('Blog','Biodiversidad','Océanos','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Noticias/2013/Enero/Activistas-cierran-gasolinera-de-Shell-en-Davos/':('Blog','Comunidad','Activismo','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Blog/Blog-de-Greenpeace-Verde/es-el-reciclaje-la-solucin-a-la-contaminacin-/blog/61332/':('Blog','Biodiversidad','Océanos','Plásticos','','news-list','Migrate'),
        'http://www.greenpeace.org/mexico/es/Footer/Descargas/reports/2018/BIO-IN-SEGURIDAD-EN-MEXICO/':('Publication','Biodiversidad','Transgénicos','Desforestación','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Footer/Descargas/reports/General/Incineracion-de-residuos-en-la-Ciudad-de-Mexico/':('Publication','Cambio Climático','ContaminaciónDelAire','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Footer/Descargas/reports/Oceanos-y-costas/Estado-de-conservacion-de-los-arrecifes-de-coral-de-la-Peninsula-de-Yucatan/':('Publication','Biodiversidad','Océanos','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Footer/Descargas/reports/Oceanos-y-costas/vaquita-Marina-el-ocaso-de-una-especiepor-negligencia-gubernamental/':('Publication','Biodiversidad','Océanos','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Footer/Descargas/reports/Oceanos-y-costas/vaquita-Marina-el-ocaso-de-una-especiepor-negligencia-gubernamental/':('Publication','Biodiversidad','Océanos','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Footer/Descargas/reports/Agricultura-sustentable-y-transgenicos/Derechos-humanos-y-plaguicidas/':('Publication','Biodiversidad','Transgénicos','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Footer/Descargas/reports/El-caso-contra-Coca-Cola/':('Publication','Biodiversidad','Océanos','Plásticos','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Footer/Descargas/reports/Bosques/Corta-de-raiz-la-libertad-de-expresion/':('Publication','Comunidad','Activismo','Deforestación','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Footer/Descargas/reports/Agricultura-sustentable-y-transgenicos/Navegando-hacia-la-agricultura-ecologica/':('Publication','Biodiversidad','Transgénicos','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Footer/Descargas/reports/Toxicos/CLICKING-CLEAN/':('Publication','Comunidad','ConsumoResponsable','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Footer/Descargas/reports/Clima-y-energia/Impactos-ambientales-del-petroleo/':('Publication','Cambio Climático','ContaminaciónDelAire','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Footer/Descargas/reports/Agricultura-sustentable-y-transgenicos/Cultivos-transgenicos-Quien-pierde/':('Publication','Biodiversidad','Transgénicos','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Footer/Descargas/reports/Toxicos/Rios-toxicos-en-Mexico/':('Publication','Biodiversidad','Océanos','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Footer/Descargas/reports/Agricultura-sustentable-y-transgenicos/encuesta-sobre-alimentos-tran/':('Publication','Biodiversidad','Transgénicos','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Footer/Descargas/reports/2010/Cultivos-transgenicos-cero-ganancias/':('Publication','Biodiversidad','Transgénicos','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Footer/Descargas/reports/Clima-y-energia/energ-a-termoelectrica-genera/':('Publication','Cambio Climático','ContaminaciónDelAire','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Footer/Descargas/reports/Clima-y-energia/destruccion_mexico/':('Publication','Cambio Climático','ContaminaciónDelAire','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Footer/Descargas/reports/Clima-y-energia/destruccion_mexico/':('Publication','Cambio Climático','ContaminaciónDelAire','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Footer/Descargas/reports/Agricultura-sustentable-y-transgenicos/ma-ces-nativos-h-bridos-y-tra/':('Publication','Biodiversidad','Transgénicos','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Footer/Descargas/reports/Agricultura-sustentable-y-transgenicos/ma-ces-nativos-h-bridos-y-tra/':('Publication','Biodiversidad','Océanos','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Footer/Descargas/reports/Manual-de-acciones-colectivas-y-amparo-para-lograr-la-justicia-ambiental/':('Publication','Comunidad','Activismo','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Footer/Descargas/reports/Clima-y-energia/7-acciones-para-detener-el-cam/':('Publication','Cambio Climático','ContaminaciónDelAire','Transporte','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Footer/Descargas/reports/Bosques/Revolucion-Forestal/':('Publication','Biodiversidad','Deforestación','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Septiembre/Impulsa-Greenpeace-prohibicion-de-bolsas-de-plastico-y-popotes-en-todo-Mexico-/':('Press Release','Biodiversidad','Océanos','Plásticos','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Septiembre/Catastrofes-la-marca-del-sexenio-de-Pena-Nieto-en-materia-ambiental/':('Press Release','Biodiversidad','Océanos','ContaminaciónDelAire','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Agosto-/Greenpeace-pide-a-Secretaria-de-Salud-acatar-Recomendacion-de-CNDH-para-evitar-mas-danos-por-contaminacion-atmosferica/':('Press Release','Cambio Climático','ContaminaciónDelAire','Transporte','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Agosto-/Comites-de-Cuenca-Rio-Sonora-y-FPDT-Atenco-se-unen-para-exigir-a-SCJN-derecho--a-participacion-ante-megaproyectos/':('Press Release','Comunidad','Activismo','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Agosto-/Suprema-Corte-decidira-si-comunidades-pueden-participar-en-asuntos--que-afectan-el-medio-ambiente/':('Press Release','Comunidad','Activismo','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Agosto-/Greenpeace-urge-a-Cofepris-incluir-recomendaciones-de-la-sociedad-civil-en-modificacion-de-Norma-de-calidad-del-aire-/':('Press Release','Cambio Climático','ContaminaciónDelAire','Transporte','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Agosto-/Esto-es-suyo-les-dice-Greenpeace-a-las-corporaciones-que-mas-contaminan-con-basura-plastica-desde-Tamaulipas/':('Press Release','Biodiversidad','Océanos','Plásticos','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Agosto-/ONGs-academia-y-gobierno-trabajan-juntos-para-impulsar-modificacion-de-Normas-Oficiales-sobre-salud-ambiental-y-monitoreo-de-la-calidad-del-aire/':('Press Release','Cambio Climático','ContaminaciónDelAire','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Agosto-/Organizaciones-de-la-sociedad-civil-se-posicionan-sobre-la-cancelacion-del-proyecto-de-la-planta-de-termovalorizacion/':('Press Release','Cambio Climático','ContaminaciónDelAire','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Agosto-/Greenpeace-presenta-queja-ante-CNDH-por-omisiones-del-gobierno-federal-en-la-preservacion-de-la-vaquita-marina/':('Press Release','Biodiversidad','Océanos','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Julio/Contaminacion-delaire-factor-de-riesgo-para-la-salud-de-ninas-ninos-y-adolescentes-en-Mexico/':('Press Release','Cambio Climático','ContaminaciónDelAire','Transporte','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Julio/Piden-a-Sagarpa-declarar-Zona-Libre-de-Transgenicos-a-territorios-mayas/':('Press Release','Biodiversidad','Transgénicos','Deforestación','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Junio/El-agua-si-esta-en-peligro-los-decretos-dejan-sin-proteccion-casi-70-del-agua-disponible-en-esas-cuencas/':('Press Release','Biodiversidad','Océanos','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Junio/Posicionamiento-de-Greenpeace-sobre-la-politica-migratoria-sin-escrupulos-de-Trump/':('Press Release','Comunidad','Activismo','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Junio/Disponible-en-ingles-Informe-sobre-Plaguicidas-Altamente-Peligrosos-en-Mexico/':('Press Release','Biodiversidad','Transgénicos','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Junio/ONG-y-personas-demandan-frenar-ola-de-violencia-contra-activistas-ambientales/':('Press Release','Comunidad','Activismo','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Junio/Comunidades-de-todo-el-estado-piden-a-candidatos-un-modelo-agroecologico/':('Press Release','Biodiversidad','Transgénicos','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Junio/Greenpeace-frente-a-la-contingencia-ambiental-en-la-ZMVM/':('Press Release','Cambio Climático','ContaminaciónDelAire','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Mayo/El-aire-en-Mexico-mata-Greenpeace/':('Press Release','Cambio Climático','ContaminaciónDelAire','SobreGreenpeace ','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Mayo/ONG-condenan-amenazas-de-muerte-a-integrantes--de-El-Barzon-en-Chihuahua/':('Press Release','Comunidad','Activismo','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Mayo/Candidatos-de-Yucatan-deben-comprometerse-por-la-agricultura-ecologica-y-apicultura-organica-Greenpeace-y-Ma-OGM/':('Press Release','Biodiversidad','Transgénicos','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Mayo/Cambio-Climatico-debe-ser-prioridad-para-la-y-los-candidatos-a-la-Presidencia-de-la-Republica-ONG-/':('Press Release','Cambio Climático','ContaminaciónDelAire','Transporte','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Mayo/Al-final-del-sexenio-de-Pena-Nieto--autoridad-agricola-busca-eliminar-la-mencion-de-transgenicos-dentro-del-etiquetado-de-los-productos-organicos/':('Press Release','Biodiversidad','Transgénicos','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Abril/OSC-urgen-a-las-y-los-candidatos-de-los-tres-niveles-de-gobierno-a-asumir-compromiso-con-la-movilidad-urbana/':('Press Release','Cambio Climático','Transporte','ContaminaciónDelAire','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Abril/Cuestiona-Greenpeace-a-Semovi-Y-los-150-millones-de-pesos-para-Trolebici-que-/':('Press Release','Cambio Climático','Transporte','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Abril/Expansion-del-area-de-refugio-de-la-Vaquita-Marina-anunciado-por-Semarnat-es-insuficiente-para-salvar-a-la-especie-ONG/':('Press Release','Biodiversidad','Océanos','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Abril/Quienes-estan-llenando-de-plastico-nuestro-planeta-Greenpeace-recolecta-evidencia/':('Press Release','Biodiversidad','Océanos','Plásticos','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Abril/Mas-de-1-millon-de-personas-demandan-a-las-empresas-que-reduzcan-los-plasticos-de-un-solo-uso/':('Press Release','Biodiversidad','Océanos','Plásticos','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Abril/TLCAN-20-aceleraria-el-cambio-climatico-en-Norte-America/':('Press Release','Cambio Climático','ContaminaciónDelAire','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Abril/Incorporar-agricultura-y-biodiversidad-en-programa-de-gobierno-compromiso-ineludible-por-candidatos-sociedad-civil/':('Press Release','Biodiversidad','Transgénicos','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Abril/Sus-envases-no-desaparecen-dice-Greenpeace-a-responsables-de-contaminacion-plastica/':('Press Release','Biodiversidad','Océanos','Plásticos','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Abril/Nestle-fracasa-en-como-abordar-su-problema-de-plasticos-de-un-solo-uso/':('Press Release','Biodiversidad','Océanos','Plásticos','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Abril/No-mas-envases-y-contenedores-de-plastico-Pide-Greenpeace-a-7-gigantes-del-mercado/':('Press Release','Biodiversidad','Océanos','Plásticos','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Marzo/Muertes-por-contaminacion-atmosferica-podrian-evitarse-si-Cofepris-ajustara-normas-Greenpeace/':('Press Release','Cambio Climático','ContaminaciónDelAire','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Marzo/Sin-Consulta-este-jueves-pretenden-votar-la-Ley-General-de-Biodiversidad/':('Press Release','Comunidad','Activismo','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Marzo/Ciudades-mexicanas-exigen-a-Cofepris-aire-limpio-/':('Press Release','Cambio Climático','ContaminaciónDelAire','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Febrero/Greenpeace-denuncia-en-foro-global-retrasos-para-frenar-cambio-climatico-en-la-CDMX/':('Press Release','Cambio Climático','ContaminaciónDelAire','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Febrero/Exige-Greenpeace-a-Cofepris-mejor-calidad-de-aire/':('Press Release','Cambio Climático','ContaminaciónDelAire','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Febrero/ConsultaMaya-SalvemosLaSelvaMaya-UnidosPorLaSelva/':('Press Release','Biodiversidad','Transgénicos','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Febrero/Autoridades-acuerdan-con-ONG-y-comunidad-cientifica-blindar-el-refugio-de-las-ultimas-vaquitas-marinas--del-mundo/':('Press Release','Biodiversidad','Océanos','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Enero/La-bioseguridad-en-Mexico-no-existe-Greenpeace/':('Press Release','Biodiversidad','Transgénicos','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Enero/Sociedad-civil-manda-mensaje-a-los-lideres-en-el-Foro-Economico-Mundial/':('Press Release','Comunidad','Activismo','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Enero/futuro-sin-tlc/':('Press Release','Comunidad','Activismo','','','article','Migrate'),
        'http://www.greenpeace.org/mexico/es/Prensa1/2018/Enero/Justicia-para-la-gente-y-el-planeta/':('Press Release','Comunidad','Activismo','','','article','Migrate')
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
        """
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
        """


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
        """

        yield {
            'type': response.meta['p4_post_type'],
            'p3_image_gallery': p3_image_gallery,
            'title': extract_with_css('div.article h1 span::text'),
            #'subtitle': '',
            'author': 'Greenpeace Mexico',
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

        # Replace the spanish month name with english month name.
        #for mx_month, en_month in month_mx_en.iteritems():
        #    month_name = month_name.replace(mx_month, en_month)

        month_mx_en = {
            'enero': 'January',
            'febrero': 'February',
            'marzo': 'March',
            'abril': 'April',
            'mayo': 'May',
            'junio': 'June',
            'julio': 'July',
            'agosto': 'August',
            'septiembre': 'September',
            'octubre': 'October',
            'noviembre': 'November', 
            'diciembre': 'December', 
        }

        # Replace the Spanish month name with english month name.
        for mx_month, en_month in month_mx_en.iteritems():
            month_name = month_name.replace(mx_month, en_month)

        return month_name;

    def csv_writer(self, data, path):
        # Write data to a CSV file path
        with open(path, "a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(data)
