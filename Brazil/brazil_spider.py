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
        'FEED_URI': 'gpbr_v2_migration.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def start_requests(self):

        #v1
        start_urls = {
            'http://www.greenpeace.org/brasil/pt/Noticias/Desmatamento-A-falta-de-agua-comeca-aqui/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Desmatamento: A falta de água começa aqui'),
            'http://www.greenpeace.org/brasil/pt/Blog/os-corais-da-amaznia-surpreenderam-nossa-expe/blog/58736/':('Blog','Proteja a Natureza','Biodiversidade','','Migrate','Story','Os Corais da Amazônia surpreenderam nossa expectativa e imaginação'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Rio-Doce-1-Ano-de-Lama-e-Luta/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Rio Doce: 1 Ano de Lama e Luta'),
            'http://www.greenpeace.org/brasil/pt/Blog/ambientalistas-pedem-que-mercado-pare-o-desma/blog/60195/':('Blog','Proteja a Natureza','Florestas','','Migrate','Story','Ambientalistas exigem que mercado pare o desmatamento do Cerrado'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Hidreletricas-na-Amazonia-um-mau-negocio-para-o-Brasil-e-para-o-mundo/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Story','Hidrelétricas na Amazônia: um mau negócio para o Brasil e para o mundo'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Lutas-e-vitorias-Munduruku/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Story','Lutas e vitórias Munduruku'),
            'http://www.greenpeace.org/brasil/pt/Noticias/PL-do-Veneno-volta-a-tramitar-na-Camara-e-pode-seguir-para-votacao/':('News','Transforme a Sociedade','Agricultura','Resista','Migrate','Story','Mais agrotóxico no prato: PL do Veneno caminha à passos largos'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Hidreletrica-no-Tapajos-esta-cancelada/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Story','Hidrelétrica no Tapajós está cancelada'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Corais-da-Amazonia-Nosso-tesouro-recem-descoberto-e-ja-ameacado/':('News','Proteja a Natureza','Biodiversidade','','Migrate','Story','Corais da Amazônia: Nosso tesouro recém-descoberto e já ameaçado'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Rio-essa-merenda-nao-parece-legal/':('News','Transforme a Sociedade','Agricultura','Resista','Migrate','Story','Rio, essa merenda não parece legal!'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Ruralistas-tentam-aprovar-PL-que-libera-mais-veneno-na-nossa-comida/':('News','Transforme a Sociedade','Agricultura','Resista','Migrate','Story','Ruralistas tentam aprovar PL que libera mais veneno na nossa comida'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Carne-Fraca-o-modelo-de-producao-e-falho/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Carne Fraca: o modelo de produção é falho'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Segura-este-abacaxi/':('News','Transforme a Sociedade','Agricultura','Resista','Migrate','Story','Segura este abacaxi!'),
            'http://www.greenpeace.org/brasil/pt/Blog/a-extenso-da-tragdia-da-lama-e-da-dor-na-foz-/blog/59597/':('Blog','Transforme a Sociedade','Resista','','Migrate','Story','A extensão da tragédia da lama e da dor na Foz do Rio Doce'),
            'http://www.greenpeace.org/brasil/pt/Noticias/O-misterioso-caso-da-plantacao-de-Ipe/':('News','Proteja a Natureza','Florestas','','Migrate','Story','O misterioso caso da plantação de Ipê'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Esta-no-Congresso-projeto-para-reduzir-uso-de-agrotoxicos/':('News','Transforme a Sociedade','Agricultura','Resista','Migrate','Story','Está no Congresso: projeto para reduzir uso de agrotóxicos'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Mudancas-climaticas-vao-agravar-a-desigualdade-social-no-Brasil/':('News','Transforme a Sociedade','Clima','Energia','Migrate','Publication','Mudanças climáticas vão agravar a desigualdade social no Brasil'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Criacao-do-Santuario-de-Baleias-do-Atlantico-Sul-e-negada-mas-nao-desistiremos/':('News','Proteja a Natureza','Biodiversidade','','Migrate','Story','Criação do Santuário de Baleias é negada, mas não desistiremos'),
            #'http://www.greenpeace.org/brasil/Global/brasil/image/2015/Dezembro/2016/Revolu%C3%A7%C3%A3o%20Energ%C3%A9tica%202016.%20Greenpeace%20Brasil.pdf','Documents','Transforme a Sociedade','Clima','Energia','Migrate','Publication','Revolução Energética: Rumo a um Brasil com 100% de energias limpas e renováveis'),
            #'http://www.greenpeace.org/brasil/Global/brasil/documentos/2016/E%20agora,%20Jose%CC%81.%20Resumo.%20Greenpeace%20Brasil.pdf','Documents','Transforme a Sociedade','Clima','Energia','Migrate','Publication','E agora José? O Brasil em tempos de mudanças climáticas'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Comunicado-do-Greenpeace-sobre-o-protesto-nas-Linhas-de-Nazca-no-Peru/':('News','Greenpeace','Institucional','','Migrate','Press Release','Comunicado do Greenpeace sobre o protesto nas Linhas de Nazca, no Peru'),
        }

        #v2
        start_urls = {
            'http://www.greenpeace.org/brasil/pt/Noticias/Desmatamento-A-falta-de-agua-comeca-aqui/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Desmatamento: A falta de água começa aqui'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Criacao-do-Santuario-de-Baleias-do-Atlantico-Sul-e-negada-mas-nao-desistiremos/':('News','Proteja a Natureza','Biodiversidade','','Migrate','Story','Criação do Santuário de Baleias é negada, mas não desistiremos'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Carne-Fraca-o-modelo-de-producao-e-falho/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Carne Fraca: o modelo de produção é falho'),
            'http://www.greenpeace.org/brasil/pt/Blog/ambientalistas-pedem-que-mercado-pare-o-desma/blog/60195/':('Blog','Proteja a Natureza','Florestas','','Migrate','Story','Ambientalistas exigem que mercado pare o desmatamento do Cerrado'),
            'http://www.greenpeace.org/brasil/pt/Noticias/PL-do-Veneno-volta-a-tramitar-na-Camara-e-pode-seguir-para-votacao/':('News','Transforme a Sociedade','Agricultura','Resista','Migrate','Story','Mais agrotóxico no prato: PL do Veneno caminha à passos largos'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Rio-essa-merenda-nao-parece-legal/':('News','Transforme a Sociedade','Agricultura','Resista','Migrate','Story','Rio, essa merenda não parece legal!'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Ruralistas-tentam-aprovar-PL-que-libera-mais-veneno-na-nossa-comida/':('News','Transforme a Sociedade','Agricultura','Resista','Migrate','Story','Ruralistas tentam aprovar PL que libera mais veneno na nossa comida'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Segura-este-abacaxi/':('News','Transforme a Sociedade','Agricultura','Resista','Migrate','Story','Segura este abacaxi!'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Esta-no-Congresso-projeto-para-reduzir-uso-de-agrotoxicos/':('News','Transforme a Sociedade','Agricultura','Resista','Migrate','Story','Está no Congresso: projeto para reduzir uso de agrotóxicos'),
            'http://www.greenpeace.org/brasil/pt/Noticias/O-misterioso-caso-da-plantacao-de-Ipe/':('News','Proteja a Natureza','Florestas','','Migrate','Story','O misterioso caso da plantação de Ipê'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Mudancas-climaticas-vao-agravar-a-desigualdade-social-no-Brasil/':('News','Transforme a Sociedade','Clima','Energia','Migrate','Publication','Mudanças climáticas vão agravar a desigualdade social no Brasil'),
            'http://www.greenpeace.org/brasil/pt/Blog/os-corais-da-amaznia-surpreenderam-nossa-expe/blog/58736/':('Blog','Proteja a Natureza','Biodiversidade','','Migrate','Story','Os Corais da Amazônia surpreenderam nossa expectativa e imaginação'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Corais-da-Amazonia-Nosso-tesouro-recem-descoberto-e-ja-ameacado/':('News','Proteja a Natureza','Biodiversidade','','Migrate','Story','Corais da Amazônia: Nosso tesouro recém-descoberto e já ameaçado'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Comunicado-do-Greenpeace-sobre-o-protesto-nas-Linhas-de-Nazca-no-Peru/':('News','Greenpeace','Institucional','','Migrate','Press Release','Comunicado do Greenpeace sobre o protesto nas Linhas de Nazca, no Peru'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Rio-Doce-1-Ano-de-Lama-e-Luta/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Rio Doce: 1 Ano de Lama e Luta'),
            'http://www.greenpeace.org/brasil/pt/Blog/a-extenso-da-tragdia-da-lama-e-da-dor-na-foz-/blog/59597/':('Blog','Transforme a Sociedade','Resista','','Migrate','Story','A extensão da tragédia da lama e da dor na Foz do Rio Doce'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Hidreletricas-na-Amazonia-um-mau-negocio-para-o-Brasil-e-para-o-mundo/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Publication','Hidrelétricas na Amazônia: um mau negócio para o Brasil e para o mundo'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Lutas-e-vitorias-Munduruku/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Story','Lutas e vitórias Munduruku'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Hidreletrica-no-Tapajos-esta-cancelada/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Story','Hidrelétrica no Tapajós está cancelada'),
            'http://www.greenpeace.org/brasil/pt/Blog/518-anos-de-resistncia-indgena-no-brasil-o-ca/blog/61401/':('Blog','Proteja a Natureza','Florestas','Resista','Migrate','Story','518 anos de resistência indígena no Brasil: o caso emblemático dos Karipuna'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Em-Brasilia-indigenas-Karipuna-denunciam-loteamento-e-roubo-de-madeira-em-terra-demarcada-ha-28-anos/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Story','Em Brasília, indígenas Karipuna denunciam loteamento e roubo de madeira em terra demarcada há 28 anos'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Adriano-Karipuna-vai-a-ONU-denunciar-graves-violencias-contra-seu-povo/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Story','Adriano Karipuna vai à ONU denunciar graves violências contra seu povo'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Sem-floresta-nao-tem-agua/':('News','Transforme a Sociedade','Clima','','Migrate','Story','Sem floresta não tem água'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Novo-Codigo-Florestal-e-falta-de-agua-tudo-a-ver/':('News','Transforme a Sociedade','Clima','','Migrate','Story','Novo Código Florestal e falta de água: tudo a ver'),
            'http://www.greenpeace.org/brasil/pt/Blog/extra-extra-a-crise-hdrica-acabou-ooops-a-gua/blog/55790/':('Blog','Transforme a Sociedade','Clima','','Migrate','Story','Extra, extra: a crise hídrica acabou – ooops, a água acabou!'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Bebeu-agua-Ta-com-sede-Apague-a-luz/':('News','Transforme a Sociedade','Clima','','Migrate','Story','Bebeu água? Tá com sede? Apague a luz!'),
            'http://www.greenpeace.org/brasil/pt/Blog/gua-no-mercadoria-um-bem-comum/blog/56291/':('Blog','Transforme a Sociedade','Clima','','Migrate','Story','Água não é mercadoria, é um bem comum'),
            'http://www.greenpeace.org/brasil/pt/Noticias/A-crise-da-agua-nao-da-desconto-/':('News','Transforme a Sociedade','Clima','','Migrate','Story','A crise da água não dá desconto'),
            'http://www.greenpeace.org/brasil/pt/Blog/por-que-um-dia-para-a-gua/blog/55963/':('Blog','Transforme a Sociedade','Clima','','Migrate','Story','Por que um dia para a água?'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Sem-agua-sem-clima/':('News','Transforme a Sociedade','Clima','','Migrate','Story','Sem água, sem clima'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Faltou-agua-Entenda-mais/':('News','Transforme a Sociedade','Clima','','Migrate','Story','Faltou água? Entenda mais'),
            'http://www.greenpeace.org/brasil/pt/Blog/qual-o-pinguim-mais-irresistvel-da-antrtida/blog/61091/':('Blog','Transforme a Sociedade','Clima','Biodiversidade','Migrate','Story','Qual o pinguim mais irresistível da Antártida?'),
            'http://www.greenpeace.org/brasil/pt/Blog/temos-um-ano-para-criar-a-maior-rea-protegida/blog/60901/':('Blog','Transforme a Sociedade','Clima','Biodiversidade','Migrate','Story','Temos um ano para criar a maior área protegida da Terra'),
            'http://www.greenpeace.org/brasil/pt/Blog/uma-nova-aventura-rumo-antrtida/blog/60968/':('Blog','Transforme a Sociedade','Clima','Biodiversidade','Migrate','Story','Uma nova aventura rumo à Antártida'),
            'http://www.greenpeace.org/brasil/pt/Blog/a-marcha-dos-pinguins/blog/61005/':('Blog','Transforme a Sociedade','Clima','Biodiversidade','Migrate','Story','A marcha dos pinguins'),
            'http://www.greenpeace.org/brasil/pt/Blog/memrias-da-antrtida/blog/60920/':('Blog','Transforme a Sociedade','Clima','Biodiversidade','Migrate','Story','Memórias da Antártida'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Ativistas-do-Greenpeace-confrontam-plataforma-de-petroleo-norueguesa-no-Artico-/':('News','Transforme a Sociedade','Clima','Biodiversidade','Migrate','Story','Ativistas do Greenpeace confrontam plataforma de petróleo norueguesa no Ártico'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Retrospectiva-Salve-o-Artico/':('News','Transforme a Sociedade','Clima','Biodiversidade','Migrate','Story','Retrospectiva Salve o Ártico'),
            'http://www.greenpeace.org/brasil/pt/Blog/shell-desiste-de-explorar-petrleo-do-rtico-ap/blog/54242/':('Blog','Transforme a Sociedade','Clima','Biodiversidade','Migrate','Story','Vitória! Shell desiste de explorar petróleo do mar do Ártico'),
            'http://www.greenpeace.org/brasil/pt/Noticias/LEGO-abandona-a-Shell/':('News','Transforme a Sociedade','Clima','Biodiversidade','Migrate','Story','LEGO abandona a Shell'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Um-gigante-faz-frente-a-Shell/':('News','Transforme a Sociedade','Clima','Biodiversidade','Migrate','Story','Uma gigante enfrenta a Shell'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Explosoes-no-Oceano-Artico/':('News','Transforme a Sociedade','Clima','Biodiversidade','Migrate','Story','Explosões no Oceano Ártico'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Pesca-predatoria-no-Oceano-Artico-sera-interrompida/':('News','Transforme a Sociedade','Clima','Biodiversidade','Migrate','Story','Pesca predatória no Oceano Ártico será interrompida'),
            'http://www.greenpeace.org/brasil/pt/Noticias/As-cinco-maiores-vitorias-do-Artico-em-2014/':('News','Transforme a Sociedade','Clima','Biodiversidade','Migrate','Story','As quatro maiores conquistas do Ártico em 2014'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Brasil-na-luta-internacional-pelo-Artico/':('News','Transforme a Sociedade','Clima','Biodiversidade','Migrate','Story','Brasil na luta internacional pelo Ártico'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Shell-na-iminencia-de-explorar-o-Artico1/':('News','Transforme a Sociedade','Clima','Biodiversidade','Migrate','Story','Shell na iminência de explorar o Ártico'),
            'http://www.greenpeace.org/brasil/pt/Blog/unido-sob-uma-bandeira-rtico-declarado-santur/blog/44767/':('Blog','Transforme a Sociedade','Clima','Biodiversidade','Migrate','Story','Sob uma bandeira, Ártico é declarado santuário'),
            'http://www.greenpeace.org/brasil/pt/Noticias/artico-continua-diminuindo-e-rapido/':('News','Transforme a Sociedade','Clima','Biodiversidade','Migrate','Story','Ártico continua diminuindo, e rápido'),
            'http://www.greenpeace.org/brasil/pt/Blog/democracia-direitos-e-os-30-do-rtico/blog/50678/':('Blog','Transforme a Sociedade','Clima','Biodiversidade','Migrate','Story','Democracia, direitos e os 30 do Ártico'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Justica-decide-a-favor-do-Greenpeace-Arctic-30-e-exige-que-a-Russia-pague-54-milhoes-a-Holanda/':('News','Transforme a Sociedade','Clima','Biodiversidade','Migrate','Story','Justiça decide a favor do Greenpeace Arctic 30 e exige que a Rússia pague €5,4 milhões à Holanda'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Russia-e-julgada-culpada-por-invadir-navio-do-Greenpeace/':('News','Transforme a Sociedade','Clima','Biodiversidade','Migrate','Story','Rússia é considerada culpada por invadir navio do Greenpeace'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Ha-dois-anos-o-mundo-conhecia-os-30-do-Artico/':('News','Transforme a Sociedade','Clima','Biodiversidade','Migrate','Story','Lá e aqui, hoje e sempre'),
            'http://www.greenpeace.org/brasil/pt/Blog/o-greenpeace-e-os-ursos-polares/blog/56395/':('Blog','Transforme a Sociedade','Clima','Biodiversidade','Migrate','Story','O Greenpeace e os ursos polares'),
            'http://www.greenpeace.org/brasil/pt/Blog/caa-cientfica-de-baleias-balela/blog/57666/':('Blog','Proteja a Natureza','Biodiversidade','','Migrate','Story','Caça científica de baleias é balela'),
            'http://www.greenpeace.org/brasil/pt/Noticias/As-baleias-nao-podem-mais-esperar/':('News','Proteja a Natureza','Biodiversidade','','Migrate','Story','As baleias não podem mais esperar'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Peticao-pelo-Santuario-de-Baleias-e-entregue-ao-governo-brasileiro/':('News','Proteja a Natureza','Biodiversidade','','Migrate','Story','Petição pelo Santuário de Baleias é entregue ao governo brasileiro'),
            'http://www.greenpeace.org/brasil/pt/Blog/o-que-rolou-na-reunio-da-comisso-internaciona/blog/57954/':('Blog','Proteja a Natureza','Biodiversidade','','Migrate','Story','O que rolou na reunião da Comissão Internacional da Baleia'),
            'http://www.greenpeace.org/brasil/pt/Blog/greenpeace-e-santos-fc-unidos-pelas-baleias/blog/57685/':('Blog','Proteja a Natureza','Biodiversidade','','Migrate','Story','Greenpeace e Santos FC unidos pelas baleias'),
            'http://www.greenpeace.org/brasil/pt/Blog/mais-proteo-s-baleias/blog/48740/':('Blog','Proteja a Natureza','Biodiversidade','','Migrate','Story','Mais proteção às baleias'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Governo-derruba-mais-uma-vez-divulgacao-da-Lista-Suja-de-Trabalho-Escravo/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Governo derruba mais uma vez divulgação da Lista Suja do Trabalho Escravo'),
            'http://www.greenpeace.org/brasil/pt/Noticias/-Principais-supermercados-do-Brasil-fecham-o-cerco-contra-a-carne-de-desmatamento/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Principais supermercados do Brasil fecham o cerco contra a carne de desmatamento'),
            'http://www.greenpeace.org/brasil/pt/Noticias/carne-fria-greenpeace-suspende-negociacoes-com-jbs/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Carne Fria: Greenpeace suspende negociações com JBS'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Relatorio-do-Greenpeace-indica-que-o-desmatamento-pode-estar-na-mesa-do-brasileiro/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Relatório do Greenpeace indica que o desmatamento pode estar na mesa do brasileiro'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Pao-de-Acucar-se-compromete-com-Desmatamento-Zero/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Grupo Pão de Açúcar se compromete com Desmatamento Zero'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Apos-escandalos-Greenpeace-suspende-participacao-no-Compromisso-da-Pecuaria/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Após escândalos, Greenpeace suspende participação no Compromisso da Pecuária'),
            'http://www.greenpeace.org/brasil/pt/Noticias/O-combate-ao-avanco-da-pecuaria-na-Amazonia/':('News','Proteja a Natureza','Florestas','','Migrate','Story','O combate ao avanço da pecuária na Amazônia'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Auditorias-reforcam-sucesso-do-Compromisso-Publico-da-Pecuaria/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Auditorias reforçam sucesso do Compromisso Público da Pecuária'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Frigorificos-devem-manter-monitoramento-socioambiental-para-compra-de-carne/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Frigoríficos devem manter monitoramento socioambiental para compra de carne'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Amapa-no-olho-do-furacao-do-agronegocio-e-da-especulacao-fundiaria-/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Amapá: no olho do furacão do agronegócio e da especulação fundiária'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Reducao-de-agrotoxicos-pode-se-tornar-realidade/':('News','Transforme a Sociedade','Agricultura','Resista','Migrate','Story','Redução de agrotóxicos pode se tornar realidade!'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Reducao-de-agrotoxicos-vira-Projeto-de-Lei/':('News','Transforme a Sociedade','Agricultura','Resista','Migrate','Story','Redução de agrotóxicos vira Projeto de Lei'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Ruralistas-criam-Comissao-para-acelerar-a-liberacao-de-agrotoxicos/':('News','Transforme a Sociedade','Agricultura','Resista','Migrate','Story','Ruralistas criam Comissão para acelerar a liberação de agrotóxicos'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Um-pra-la-tres-pra-ca/':('News','Transforme a Sociedade','Agricultura','Resista','Migrate','Story','Um pra lá, três pra cá'),
            'http://www.greenpeace.org/brasil/pt/Blog/mais-de-20-de-todos-os-agrotxicos-usados-no-b/blog/58124/':('Blog','Transforme a Sociedade','Agricultura','Resista','Migrate','Story','Mais de 20% de todos os agrotóxicos usados no Brasil são ilegais'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Greenpeace-toca-sirene-em-alerta-contra-PL-do-Veneno/':('News','Transforme a Sociedade','Agricultura','Resista','Migrate','Story','Greenpeace toca sirene em alerta contra PL do Veneno'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Madeira-manchada-de-sangue/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Madeira manchada de sangue'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Arvores-imaginarias-destruicao-real/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Árvores imaginárias, destruição real'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Madeira-ilegal-na-Amazonia-lavou-ficou-legal/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Madeira ilegal: na Amazônia, lavou, ficou legal'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Povo-indigena-Kaapor-integra-tecnologia-no-monitoramento-e-protecao-do-seu-territorio-tradicional/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Povo indígena Ka’apor integra tecnologia no monitoramento e proteção do seu território tradicional'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Madeira-ilegal-da-Amazonia-chega-impunemente-a-Europa-/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Madeira ilegal da Amazônia chega impunemente à Europa'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Rastreamento-de-caminhoes-revela-destruicao-silenciosa-da-floresta/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Rastreamento de caminhões revela destruição silenciosa da floresta'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Chega-de-madeira-ilegal-na-TI-Cachoeira-Seca/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Chega de madeira ilegal na TI Cachoeira Seca!'),
            'http://www.greenpeace.org/brasil/pt/Blog/24-de-agosto-de-2050-uma-viagem-ao-brasil-do-/blog/57321/':('Blog','Transforme a Sociedade','Clima','Energia','Migrate','Story','Agosto de 2050: uma viagem ao Brasil do futuro'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Acordo-de-Paris-que-visa-combater-as-mudancas-climaticas-vira-lei-no-Brasil/':('News','Transforme a Sociedade','Clima','Energia','Migrate','Story','Acordo de Paris, que visa combater as mudanças climáticas, vira lei no Brasil'),
            'http://www.greenpeace.org/brasil/pt/Noticias/2015-o-ano-em-que-o-carvao-entrou-em-decadencia/':('News','Transforme a Sociedade','Clima','Energia','Migrate','Story','2015: o ano em que o carvão entrou em decadência'),
            'http://www.greenpeace.org/brasil/pt/Blog/voc-sabia-que-as-mulheres-so-as-mais-impactad/blog/61212/':('Blog','Transforme a Sociedade','Clima','Energia','Migrate','Story','Você sabia que as mulheres são as mais impactadas pela mudança do clima?'),
            'http://www.greenpeace.org/brasil/pt/Blog/o-acordo-de-paris-e-as-lies-de-casa-para-o-br/blog/55110/':('Blog','Transforme a Sociedade','Clima','Energia','Migrate','Story','O Acordo de Paris e as lições de casa para o Brasil'),
            'http://www.greenpeace.org/brasil/pt/Blog/leo-na-casa-dos-outros-no-refresco/blog/60334/':('Blog','Proteja a Natureza','Biodiversidade','Energia','Migrate','Story','Óleo na casa dos outros não é refresco'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Amazonia-em-aguas-profundas-Como-o-petroleo-ameaca-os-Corais-da-Amazonia/':('News','Proteja a Natureza','Biodiversidade','Energia','Migrate','Story','Amazônia em águas profundas: Como o petróleo ameaça os Corais da Amazônia'),
            'http://www.greenpeace.org/brasil/pt/Blog/descobrimos-corais-da-amaznia-na-guiana-franc/blog/61490/':('Blog','Proteja a Natureza','Biodiversidade','Energia','Migrate','Story','Descobrimos Corais da Amazônia na Guiana Francesa'),
            'http://www.greenpeace.org/brasil/pt/Blog/como-ns-estamos-ganhando-das-grandes-petrolfe/blog/60159/':('Blog','Proteja a Natureza','Biodiversidade','Energia','Migrate','Story','Como mostramos que temos mais força que as grandes petrolíferas'),
            'http://www.greenpeace.org/brasil/pt/Blog/brasil-celebra-o-dia-mundial-dos-corais-da-am/blog/61073/':('Blog','Proteja a Natureza','Biodiversidade','Energia','Migrate','Story','Brasil celebra o Dia Mundial dos Corais da Amazônia'),
            'http://www.greenpeace.org/brasil/pt/Blog/para-defender-os-corais-da-amaznia-ativistas-/blog/61580/':('Blog','Proteja a Natureza','Biodiversidade','Energia','Migrate','Story','Para defender os Corais da Amazônia, ativistas barram reunião da Total'),
            'http://www.greenpeace.org/brasil/pt/Blog/5-fatos-que-so-vergonhatotal-nos-planos-de-pe/blog/61454/':('Blog','Proteja a Natureza','Biodiversidade','Energia','Migrate','Story','5 fatos que são #VergonhaTotal nos planos de perfuração na foz do rio Amazonas'),
            'http://www.greenpeace.org/brasil/pt/Blog/corais-da-amaznia-como-chegamos-at-aqui/blog/61352/':('Blog','Proteja a Natureza','Biodiversidade','Energia','Migrate','Story','Relembre a jornada em defesa dos Corais da Amazônia'),
            'http://www.greenpeace.org/brasil/pt/Blog/5-coisas-que-voc-precisa-saber-sobre-os-corai/blog/61513/':('Blog','Proteja a Natureza','Biodiversidade','Energia','Migrate','Story','5 coisas que você precisa saber sobre os Corais da Amazônia'),
            'http://www.greenpeace.org/brasil/pt/Blog/a-riqueza-da-biodiversidade-dos-corais-da-ama/blog/61528/':('Blog','Proteja a Natureza','Biodiversidade','Energia','Migrate','Story','A rica biodiversidade dos Corais da Amazônia'),
            'http://www.greenpeace.org/brasil/pt/Blog/7-razes-do-porqu-as-esponjas-so-animais-muito/blog/59747/':('Blog','Proteja a Natureza','Biodiversidade','Energia','Migrate','Story','7 razões do porquê as esponjas-do-mar são animais MUITO legais'),
            'http://www.greenpeace.org/brasil/pt/Blog/as-primeiras-imagens-de-um-novo-mundo/blog/58609/':('Blog','Proteja a Natureza','Biodiversidade','Energia','Migrate','Story','Corais da Amazônia: as primeiras imagens de um novo mundo'),
            'http://www.greenpeace.org/brasil/pt/Blog/mais-gado-mais-desmatamento/blog/36623/':('Blog','Proteja a Natureza','Florestas','','Migrate','Story','Mais gado, mais desmatamento'),
            'http://www.greenpeace.org/brasil/pt/Blog/colocando-mais-gasolina-na-motosserra/blog/58707/':('Blog','Proteja a Natureza','Florestas','','Migrate','Story','Colocando mais gasolina na motosserra'),
            'http://www.greenpeace.org/brasil/pt/Blog/europa-a-grande-vil-global-das-florestas/blog/45818/':('Blog','Proteja a Natureza','Florestas','','Migrate','Story','Europa, a grande vilã global das florestas?'),
            'http://www.greenpeace.org/brasil/pt/Blog/evoluo-do-desmatamento-em-rondnia/blog/41582/':('Blog','Proteja a Natureza','Florestas','','Migrate','Story','Evolução do desmatamento em Rondônia'),
            'http://www.greenpeace.org/brasil/pt/Blog/desmatamento-e-trabalho-escravo/blog/43490/':('Blog','Proteja a Natureza','Florestas','','Migrate','Story','Desmatamento e trabalho escravo'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Projeto-de-lei-do-Desmatamento-Zero-e-entregue-no-Congresso/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Projeto de lei do Desmatamento Zero é entregue no Congresso'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Projeto-de-Lei-do-Desmatamento-Zero-completa-um-ano-no-Congresso-/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Desmatamento Zero completa um ano no Congresso'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Companhias-globais-anunciam-apoio-ao-desmatamento-zero-no-Cerrado/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Companhias globais anunciam apoio ao desmatamento zero no Cerrado'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Desmatamento-Zero-uma-historia-sua-e-do-Greenpeace/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Desmatamento Zero: uma história sua e do Greenpeace'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Acao-alerta-para-as-queimadas-em-florestas-e-o-desmatamento-na-Amazonia/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Ação alerta para as queimadas em florestas e o desmatamento na Amazônia'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Congresso-volta-a-debater-Desmatamento-Zero/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Congresso volta a debater Desmatamento Zero'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Dia-da-Mobilizacao-Nacional-pelo-Desmatamento-Zero/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Dia da Mobilização Nacional pelo Desmatamento Zero'),
            'http://www.greenpeace.org/brasil/pt/Blog/Gisele-Bundchen-apoia-Desmatamento-Zero/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Gisele Bündchen apoia Desmatamento Zero'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Para-especialistas-zerar-o-desmatamento-e-possivel-E-urgente/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Para especialistas, zerar o desmatamento é possível. E urgente'),
            'http://www.greenpeace.org/brasil/pt/Blog/Um-CAR-sozinho-nao-faz-Desmatamento-Zero/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Um CAR sozinho não faz Desmatamento Zero'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Conheca-os-vencedores-do-Desafio-Salve-as-Florestas/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Conheça os vencedores do Desafio Salve as Florestas'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Desmatamento-Zero--Aumentando-a-pressao/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Desmatamento Zero – Aumentando a pressão'),
            'http://www.greenpeace.org/brasil/pt/Blog/a-importncia-das-grandes-rvores/blog/47917/':('Blog','Proteja a Natureza','Florestas','','Migrate','Story','A importância das grandes árvores'),
            'http://www.greenpeace.org/brasil/pt/Blog/qual-o-problema-do-novo-cdigo-florestal/blog/34976/':('Blog','Proteja a Natureza','Florestas','','Migrate','Story','Qual o problema do novo Código Florestal?'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Brasil-nacao-indigena/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Brasil: nação indígena'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Dia-do-Indio-temos-motivos-para-comemorar/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Dia do Índio: temos motivos para comemorar?'),
            'http://www.greenpeace.org/brasil/pt/Noticias/ONU-apresenta-relatorio-sobre-violacao-de-direitos-indigenas-no-Brasil/':('News','Transforme a Sociedade','Resista','','Migrate','Story','ONU apresenta relatório sobre violação de direitos indígenas no Brasil'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Temer-pode-liberar-exploracao-agropecuaria-em-terras-indigenas/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Temer pode liberar exploração agropecuária em terras indígenas'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Temer-violenta-direitos-indigenas-para-impedir-proprio-julgamento/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Temer violenta direitos indígenas para impedir próprio julgamento'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Deixa-o-indio-la/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Deixa o índio lá'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Protesto-pacifico-de-povos-indigenas-acaba-em-violencia-policial/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Protesto pacífico de povos indígenas acaba em violência policial'),
            'http://www.greenpeace.org/brasil/pt/Blog/em-carta-onu-lideranas-indgenas-e-organizaes-/blog/59998/':('Blog','Transforme a Sociedade','Resista','','Migrate','Story','Em carta à ONU, lideranças indígenas e organizações denunciam violações aos seus direitos'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Munduruku-resistirao-ate-serem-atendidos/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Munduruku resistirão até serem atendidos'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Ministro-da-Justica-desqualifica-luta-dos-povos-indigenas1/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Ministro da Justiça desqualifica luta dos povos indígenas'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Governo-dificulta-ainda-mais-a-demarcacao-de-terras-indigenas-no-pais/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Governo dificulta mais a demarcação de terras indígenas no país'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Infraestrutura-para-o-agronegocio-destruicao-para-os-povos-indigenas/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Infraestrutura para o agronegócio, destruição para os povos indígenas'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Munduruku-protestam-por-demarcacao-e-contra-desmonte-da-Funai/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Munduruku protestam por demarcação e contra desmonte da Funai'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Mais-de-cem-povos-indigenas-participam-da-abertura-do-ATL/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Mais de cem povos indígenas participam da abertura do ATL'),
            'http://www.greenpeace.org/brasil/pt/Blog/violnia-ao-indgena-uma-realidade-concreta-e-c/blog/45761/':('Blog','Transforme a Sociedade','Resista','','Migrate','Story','Violência ao índio: uma realidade crescente'),
            'http://www.greenpeace.org/brasil/pt/Blog/direitos-indgenas-violados/blog/46052/':('Blog','Transforme a Sociedade','Resista','','Migrate','Story','Direitos indígenas violados'),
            'http://www.greenpeace.org/brasil/pt/Blog/ndios-alvo-certeiro-da-violncia-fundiria/blog/49099/':('Blog','Transforme a Sociedade','Resista','','Migrate','Story','Índios: alvo certeiro da violência fundiária'),
            'http://www.greenpeace.org/brasil/pt/Blog/dirio-de-bordo-histrias-de-esperanza/blog/61529/':('Blog','Inspire Ativismo','Mobilização','','Migrate','Story','Diário de Bordo - Histórias de Esperanza'),
            'http://www.greenpeace.org/brasil/pt/Blog/c-entre-ns-um-doador-dentro-do-greenpeace/blog/61388/':('Blog','Inspire Ativismo','Mobilização','','Migrate','Story','Cá entre nós... um doador dentro do Greenpeace'),
            'http://www.greenpeace.org/brasil/pt/Blog/conhea-victor-o-doador-que-participou-da-camp/blog/61233/':('Blog','Inspire Ativismo','Mobilização','','Migrate','Story','Conheça Victor, o doador que participou da campanha do Greenpeace'),
            'http://www.greenpeace.org/brasil/pt/Blog/teresa-uma-menina-de-70-anos-doadora-desde-19/blog/61171/':('Blog','Inspire Ativismo','Mobilização','','Migrate','Story','Teresa, uma menina de 70 anos, doadora desde 1994.'),
            'http://www.greenpeace.org/brasil/pt/Blog/doador-economista-nadador/blog/60390/':('Blog','Inspire Ativismo','Mobilização','','Migrate','Story','Cá entre nós - Entrevista com Doador'),
            'http://www.greenpeace.org/brasil/pt/Blog/c-entre-ns-doador-annimo-relata-sou-um-funcio/blog/61034':('Blog','Inspire Ativismo','Mobilização','','Migrate','Story','Doador relata: “Sou um funcionário da indústria e apaixonado pela natureza”'),
            'http://www.greenpeace.org/brasil/pt/Blog/conhea-cinthia-professora-doadora-e-voluntria/blog/60911':('Blog','Inspire Ativismo','Mobilização','','Migrate','Story','Conheça Cinthia, professora, doadora e voluntária'),
            'http://www.greenpeace.org/brasil/pt/Blog/a-doadora-que-criou-uma-petio-e-salvou-mais-d/blog/60669':('Blog','Inspire Ativismo','Mobilização','','Migrate','Story','A doadora que criou uma petição e salvou mais de 2000 animais'),
            'http://www.greenpeace.org/brasil/pt/Blog/o-greenpeace-faz-o-que-eu-tenho-vontade-mas-c/blog/61658/':('Blog','Inspire Ativismo','Mobilização','','Migrate','Story','O Greenpeace faz o que eu tenho vontade, com a paciência e \'peace\' que eu não tenho.'),
            'http://www.greenpeace.org/brasil/pt/Noticias/aviao-utilizado-pelo-greenpeace-brasil-sofre-acidente-rio-negro/':('News','Greenpeace','Institucional','','Migrate','Press Release','Avião utilizado pelo Greenpeace Brasil sofre acidente no Rio Negro'),
            'http://www.greenpeace.org/brasil/pt/Blog/o-dia-do-meio-ambiente-so-todos-os-dias/blog/61593/':('Blog','Greenpeace','Institucional','','Migrate','Story','Todo dia é Dia do Meio Ambiente'),
            'http://www.greenpeace.org/brasil/pt/Blog/26-anos-de-greenpeace-brasil-e-milhares-de-at/blog/61439/':('Blog','Greenpeace','Institucional','','Migrate','Story','26 anos de Greenpeace Brasil e milhares de atos de coragem'),
            'http://www.greenpeace.org/brasil/pt/Blog/frases-clebres-em-20-anos-de-histria/blog/39007/':('Blog','Greenpeace','Institucional','','Migrate','Story','Frases célebres em 20 anos de história'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Lama-ate-o-pescoco/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Lama até o pescoço'),
            'http://www.greenpeace.org/brasil/pt/Blog/rio-doce-guas-subterrneas-tambm-esto-contamin/blog/59171/':('Blog','Transforme a Sociedade','Resista','','Migrate','Story','Rio Doce: águas subterrâneas também estão contaminadas'),
            'http://www.greenpeace.org/brasil/pt/Blog/da-lama-ao-p-o-impacto-da-tragdia-do-rio-doce/blog/59083/':('Blog','Transforme a Sociedade','Resista','','Migrate','Story','Da lama ao pó: o impacto da tragédia do Rio Doce para a saúde'),
            'http://www.greenpeace.org/brasil/pt/Blog/animais-esto-sendo-contaminados-pela-lama-do-/blog/59934/':('Blog','Transforme a Sociedade','Resista','','Migrate','Story','Animais estão sendo contaminados pela lama do Rio Doce'),
            'http://www.greenpeace.org/brasil/pt/Blog/desastre-em-mariana-uma-tragdia-ainda-em-curs/blog/57906/':('Blog','Transforme a Sociedade','Resista','','Migrate','Story','Desastre em Mariana: uma tragédia ainda em curso'),
            'http://www.greenpeace.org/brasil/pt/Blog/rio-doce-impactos-da-lama-no-corpo-e-na-alma-/blog/59204/':('Blog','Transforme a Sociedade','Resista','','Migrate','Story','Rio Doce: impactos da lama no corpo e na alma do povo Krenak'),
            'http://www.greenpeace.org/brasil/pt/Blog/a-vida-contra-a-lama-como-recuperar-a-flora-d/blog/59418/':('Blog','Transforme a Sociedade','Resista','','Migrate','Story','Como trazer o verde de volta à paisagem do Rio Doce?'),
            'http://www.greenpeace.org/brasil/pt/Blog/criolo-grava-mensagem-para-lembrar-um-ano-do-/blog/57915/':('Blog','Transforme a Sociedade','Resista','','Migrate','Story','Criolo grava mensagem para lembrar um ano do desastre de Mariana'),
            'http://www.greenpeace.org/brasil/pt/Blog/tragdia-de-mariana-governo-e-empresa-juntos-n/blog/54721/':('Blog','Transforme a Sociedade','Resista','','Migrate','Story','Tragédia de Mariana: governo e empresa juntos no mar de lama'),
            'http://www.greenpeace.org/brasil/pt/Blog/ativistas-pressionam-vw-a-dar-resposta-fraude/blog/54819/':('Blog','Transforme a Sociedade','Resista','','Migrate','Story','Ativistas pressionam VW a se posicionar sobre fraude de emissões'),
            'http://www.greenpeace.org/brasil/pt/Blog/o-alto-custo-dos-nibus-da-morte/blog/59450/':('Blog','Transforme a Sociedade','Cidades','','Migrate','Story','O alto custo dos ônibus da morte'),
            'http://www.greenpeace.org/brasil/pt/Blog/6-motivos-para-investir-j-nos-nibus-eltricos/blog/60163/':('Blog','Transforme a Sociedade','Cidades','','Migrate','Story','7 motivos para investir já nos ônibus elétricos'),
            'http://www.greenpeace.org/brasil/pt/Blog/a-morte-no-pede-carona-anda-de-nibus/blog/60255/':('Blog','Transforme a Sociedade','Cidades','','Migrate','Story','A morte não pede carona, anda de ônibus'),
            'http://www.greenpeace.org/brasil/pt/Blog/nibus-eltricos-so-viveis-em-so-paulo-e-um-gra/blog/58047/':('Blog','Transforme a Sociedade','Cidades','','Migrate','Story','Ônibus elétricos são viáveis em São Paulo e um grande passo na redução de emissões'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Sao-Paulo-aprova-lei-para-reduzir-poluicao-dos-onibus-/':('News','Transforme a Sociedade','Cidades','','Migrate','Story','São Paulo aprova lei para reduzir poluição dos ônibus'),
            'http://www.greenpeace.org/brasil/pt/Blog/paulistanos-querem-nibus-no-poluentes-em-so-p/blog/58801/':('Blog','Transforme a Sociedade','Cidades','','Migrate','Story','Paulistanos querem ônibus não poluentes em São Paulo'),
            'http://www.greenpeace.org/brasil/pt/Blog/esttuas-de-so-paulo-usam-mscaras-contra-a-pol/blog/60050/':('Blog','Transforme a Sociedade','Cidades','','Migrate','Story','Estátuas de São Paulo usam máscaras contra a poluição do ar'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Maioria-dos-brasileiros-quer-menos-espaco-para-carro-nas-ruas/':('News','Transforme a Sociedade','Cidades','','Migrate','Story','Maioria dos brasileiros quer menos espaço para carro nas ruas'),
            'http://www.greenpeace.org/brasil/pt/Blog/queremos-onibus-que-nao-poluem/blog/55157/':('Blog','Transforme a Sociedade','Cidades','','Migrate','Story','Queremos ônibus que não poluem'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Artigo-O-caminho-correto-passa-longe-do-petroleo/':('News','Transforme a Sociedade','Cidades','','Migrate','Story','O caminho correto passa longe do petróleo'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Voluntario-leva-campanha-do-Desmatamento-Zero-a-milhares-de-pessoas-em-Porto-Alegre-/':('News','Inspire Ativismo','Mobilização','','Migrate','Story','Voluntário leva campanha do Desmatamento Zero a milhares de pessoas em Porto Alegre'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Superei-a-depressao-quando-mergulhei-de-cabeca-na-campanha-pelo-Desmatamento-Zero-diz-voluntario/':('News','Inspire Ativismo','Mobilização','','Migrate','Story','“Superei a depressão quando mergulhei de cabeça na campanha pelo Desmatamento Zero”, diz voluntário'),
            'http://www.greenpeace.org/brasil/pt/Blog/uma-voz-pelo-clima-e-por-justia-que-se-recusa/blog/61223/':('Blog','Inspire Ativismo','Mobilização','','Migrate','Story','Uma voz pelo clima e por justiça que se recusa a calar'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Acao-de-voluntarios-retira-42-kg-de-lixo-em-praia-do-Rio-Grande-do-Sul-/':('News','Inspire Ativismo','Mobilização','','Migrate','Story','Ação de voluntários retira 42 kg de lixo em praia do Rio Grande do Sul'),
            'http://www.greenpeace.org/brasil/pt/Blog/saem-os-carros-entram-as-pessoas/blog/60297/':('Blog','Inspire Ativismo','Mobilização','','Migrate','Story','Saem os carros, entram as pessoas'),
            #'http://www.greenpeace.org/brasil/pt/Blog/brasil-celebra-o-dia-mundial-dos-corais-da-am/blog/61073/':('Blog','Inspire Ativismo','Mobilização','','Migrate','Story','Brasil celebra o Dia Mundial dos Corais da Amazônia'),
            'http://www.greenpeace.org/brasil/pt/Blog/juventude-cheia-de-energia/blog/44922/':('Blog','Inspire Ativismo','Mobilização','','Migrate','Story','Juventude cheia de energia'),
            'http://www.greenpeace.org/brasil/pt/Blog/uma-nova-gerao-de-voluntrios-surge-no-rainbow/blog/59317/':('Blog','Inspire Ativismo','Mobilização','','Migrate','Story','Uma nova geração de voluntários surge no Rainbow Warrior'),
            'http://www.greenpeace.org/brasil/pt/Blog/grupo-de-voluntrios-de-porto-alegre-mostram-p/blog/54864/':('Blog','Inspire Ativismo','Mobilização','','Migrate','Story','Grupo de Voluntários de Porto Alegre mostram porque Juntos Somos Mais'),
            'http://www.greenpeace.org/brasil/pt/Blog/meio-ambiente-baleias-e-os-voluntrios-do-gree/blog/57797/':('Blog','Inspire Ativismo','Mobilização','','Migrate','Story','Meio Ambiente, Baleias e os Voluntários do Greenpeace: Uma velha história de amor e mobilização!'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Voluntaria-defende-Desmatamento-Zero-para-manter-a-floresta-viva/':('News','Inspire Ativismo','Mobilização','','Migrate','Story','Voluntária defende Desmatamento Zero para manter a floresta viva'),
            'http://www.greenpeace.org/brasil/pt/Noticias/morat-ria-da-soja-um-exemplo/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Moratória da soja: um exemplo de que é possível produzir sem desmatar'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Moratoria-da-Soja-completa-dez-anos/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Moratória da Soja completa dez anos'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Amazonia-a-salvo-da-soja-de-desmatamento-por-tempo-indeterminado/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Moratória da Soja é renovada por tempo indeterminado'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Moratoria-da-Soja-na-Amazonia-dez-anos-de-resultados/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Moratória da Soja na Amazônia: dez anos de resultados'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Moratoria-da-Soja-mais-de-uma-decada-de-combate-ao-desmatamento-na-Amazonia/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Moratória da Soja: mais de uma década de combate ao desmatamento na Amazônia'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Greenpeace-recebe-reconhecimento-por-Moratoria-da-Soja/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Greenpeace recebe reconhecimento por Moratória da Soja'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Artigo-publicado-na-revista-Science-reconhece-eficacia-da-Moratoria-da-Soja/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Artigo publicado na revista Science reconhece eficácia da Moratória da Soja'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Desastre-nuclear-de-Chernobyl-completa-29-anos/':('News','Transforme a Sociedade','Energia','','Migrate','Story','Desastre nuclear de Chernobyl completa 29 anos'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Uma-licao-de-Fukushima/':('News','Transforme a Sociedade','Energia','','Migrate','Story','Uma lição de Fukushima'),
            'http://www.greenpeace.org/brasil/pt/Noticias/A-triste-recompensa-pelo-trabalho-em-Fukushima/':('News','Transforme a Sociedade','Energia','','Migrate','Story','A triste recompensa pelo trabalho em Fukushima'),
            'http://www.greenpeace.org/brasil/pt/Blog/energia-nuclear-renovvel/blog/547/':('Blog','Transforme a Sociedade','Energia','','Migrate','Story','Energia nuclear é renovável?'),
            'http://www.greenpeace.org/brasil/pt/Blog/os-piores-acidentes-com-usinas-nucleares-e-su/blog/33736/':('Blog','Transforme a Sociedade','Energia','','Migrate','Story','Os piores acidentes com usinas nucleares e suas consequências'),
            'http://www.greenpeace.org/brasil/pt/Blog/vtimas-de-chernobyl/blog/33819/':('Blog','Transforme a Sociedade','Energia','','Migrate','Story','Vítimas de Chernobyl'),
            'http://www.greenpeace.org/brasil/pt/Blog/15-fatos-que-voc-no-sabia-sobre-o-desastre-de/blog/56265/':('Blog','Transforme a Sociedade','Energia','','Migrate','Story','15 fatos que você não sabia sobre o desastre de Chernobyl'),
            'http://www.greenpeace.org/brasil/pt/Blog/vazamento-de-angra-completa-25-anos/blog/37259/':('Blog','Transforme a Sociedade','Energia','','Migrate','Story','Vazamento de Angra completa 25 anos'),
            'http://www.greenpeace.org/brasil/pt/Blog/por-que-salvar-os-oceanos-to-importante/blog/293/':('Blog','Proteja a Natureza','Biodiversidade','Clima','Migrate','Story','Por que salvar os oceanos é tão importante?'),
            'http://www.greenpeace.org/brasil/pt/Blog/nossos-oceanos-e-o-clima/blog/274/':('Blog','Proteja a Natureza','Biodiversidade','Clima','Migrate','Story','Nossos oceanos e o clima'),
            'http://www.greenpeace.org/brasil/pt/Blog/greenpeace-25-anos-no-brasil-lutando-pelo-mei/blog/59261/':('Blog','Greenpeace','Institucional','','Migrate','Story','Greenpeace: 25 anos no Brasil lutando pelo meio ambiente e pela vida'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Brasil-e-o-pais-que-mais-mata-ativistas/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Brasil é o país que mais mata ativistas'),
            'http://www.greenpeace.org/brasil/pt/Blog/entre-consumo-e-sustentabilidade/blog/48693/':('Blog','Greenpeace','Institucional','','Migrate','Story','Entre consumo e sustentabilidade'),
            'http://www.greenpeace.org/brasil/pt/Blog/-Vamos-salvar-a-floresta-Boreal/':('News','Proteja a Natureza','Florestas','','Migrate','Story','Vamos salvar a floresta Boreal?'),
            'http://www.greenpeace.org/brasil/pt/Blog/o-combate-ao-trabalho-anlogo-ao-escravo/blog/40573/':('Blog','Transforme a Sociedade','Resista','','Migrate','Story','O combate ao trabalho análogo ao escravo'),
            'http://www.greenpeace.org/brasil/pt/Blog/o-planeta-que-voc-vai-deixar-para-seus-filhos/blog/50947/':('Blog','Proteja a Natureza','Florestas','','Migrate','Story','O planeta que você vai deixar para seus filhos'),
            'http://www.greenpeace.org/brasil/pt/Blog/leo-de-palma-o-daqui-sustentvel/blog/11738/':('Blog','Proteja a Natureza','Florestas','','Migrate','Story','Óleo de palma: o daqui é sustentável?'),
            'http://www.greenpeace.org/brasil/pt/Blog/o-leo-de-palma-no-seu-dia-a-dia/blog/48265/':('Blog','Proteja a Natureza','Florestas','','Migrate','Story','O óleo de palma no seu dia a dia'),
            'http://www.greenpeace.org/brasil/pt/Blog/gs-de-xisto-uma-ddiva-perigosa/blog/45220/':('Blog','Transforme a Sociedade','Clima','Energia','Migrate','Story','Gás de xisto, um tema controverso'),
            'http://www.greenpeace.org/brasil/pt/Blog/os-efeitos-do-pr-sal/blog/41005/':('Blog','Transforme a Sociedade','Clima','','Migrate','Story','Os efeitos do pré-sal'),
            'http://www.greenpeace.org/brasil/pt/Blog/agroecologia-a-bola-da-vez/blog/51945/':('Blog','Transforme a Sociedade','Agricultura','','Migrate','Story','Agroecologia, a bola da vez'),
            'http://www.greenpeace.org/brasil/pt/Blog/o-que-o-greenpeace-acha-sobre-o-consumo-de-ca/blog/48220/':('Blog','Transforme a Sociedade','Resista','','Migrate','Story','O que o Greenpeace acha sobre comer carne?'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Propostas-do-governo-e-do-Congresso-para-Jamanxim-tambem-vao-beneficiar-mineradoras/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Propostas do governo e do Congresso para Jamanxim também vão beneficiar mineradoras'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Nenhuma-arvore-a-menos/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Nenhuma árvore a menos!'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Liberacao-de-cana-na-Amazonia-joga-contra-as-florestas-e-o-etanol-brasileiro/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Liberação de cana na Amazônia joga contra as florestas e o etanol brasileiro'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Apos-pressao-de-organizacoes-Janot-pede-inconstitucionalidade-da-Lei-da-Grilagem/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Após pressão de organizações, Janot pede inconstitucionalidade da Lei da Grilagem'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Sem-Licenca-Para-Destruir/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Sem Licença Para Destruir'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Licenciamento-ambiental-um-acordo-no-almoco-outro-no-cafe/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Licenciamento ambiental: um acordo no almoço, outro no café'),
            'http://www.greenpeace.org/brasil/pt/Noticias/PL-Licenciamento-ambiental-propostas-de-ruralistas-sao-inconstitucionais/':('News','Transforme a Sociedade','Resista','','Migrate','Story','PL Licenciamento ambiental: propostas de ruralistas são inconstitucionais'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Em-ato-publico-resista-convoca-sociedade-para-enfrentar-retrocessos-socioambientais/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Em ato público, #resista convoca sociedade para enfrentar retrocessos socioambientais'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Bancada-ruralista-garante-a-manutencao-de-Temer-na-Presidencia/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Bancada ruralista garante a manutenção de Temer na Presidência'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Na-Noruega-Temer-encara-protesto-corte-de-verbas-para-Amazonia-e-bronca-da-primeira-ministra/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Na Noruega, Temer encara protesto, corte de verbas para Amazônia e “bronca”'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Eleicoes-diretas-ja/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Eleições diretas já'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Resista-Dezenas-de-organizacoes-da-sociedade-civil-se-unem-em-movimento-de-resistencia-contra-retrocessos-do-governo-e-bancada-ruralista/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Resista: Sociedade civil se une em movimento contra Temer e ruralistas'),
            'http://www.greenpeace.org/brasil/pt/Blog/qual-o-valor-de-um-desastre-ambiental-no-bras/blog/55741/':('Blog','Transforme a Sociedade','Resista','','Migrate','Story','Qual é o valor de um desastre ambiental no Brasil?'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Conheca-o-Brasil-que-esta-sendo-transformado-pela-energia-solar/':('News','Transforme a Sociedade','Energia','Clima','Migrate','Story','Conheça o Brasil que está sendo transformado pela energia solar'),
            'http://www.greenpeace.org/brasil/pt/Noticias/A-alvorada-da-energia-solar/':('News','Transforme a Sociedade','Energia','Clima','Migrate','Story','A alvorada da energia solar'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Solariza-simula-um-Brasil-movido-a-energia-solar/':('News','Transforme a Sociedade','Energia','Clima','Migrate','Story','Solariza simula um Brasil movido a energia solar'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Energia-solar-brilha-para-o-povo-Munduruku/':('News','Transforme a Sociedade','Energia','Clima','Migrate','Story','Energia solar brilha para o povo Munduruku'),
            'http://www.greenpeace.org/brasil/pt/Blog/Seminario-discute-investimentos-e-empreendedorismo-em-energia-solar/':('News','Transforme a Sociedade','Energia','Clima','Migrate','Story','Seminário discute investimentos e empreendedorismo em energia solar'),
            'http://www.greenpeace.org/brasil/pt/Noticias/-Queremos-saber-da-sua-ideia-para-bombar-a-energia-solar-no-Brasil/':('News','Transforme a Sociedade','Energia','Clima','Migrate','Story','Queremos saber a sua ideia para bombar a energia solar no Brasil'),
            'http://www.greenpeace.org/brasil/pt/Noticias/O-Sol-brilha-mais-forte-na-periferia-de-Sao-Paulo/':('News','Transforme a Sociedade','Energia','Clima','Migrate','Story','O Sol brilha mais forte na periferia de São Paulo'),
            'http://www.greenpeace.org/brasil/pt/Noticias/O-trem-solar-chega-em-Uberlandia--/':('News','Transforme a Sociedade','Energia','Clima','Migrate','Story','O “trem” solar chega em Uberlândia'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Levy-deixa-o-Sol-brilhar-/':('News','Transforme a Sociedade','Energia','Clima','Migrate','Story','Levy, deixa o Sol brilhar'),
            'http://www.greenpeace.org/brasil/pt/Blog/doaes-que-multiplicam-o-poder-do-sol/blog/52615/':('Blog','Transforme a Sociedade','Energia','Clima','Migrate','Story','Doações que multiplicam o poder do Sol'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Demarcacao-Ja-indigenas-Munduruku-protestam-pela-garantia-e-protecao-de-seu-territorio/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Story','Demarcação Já: indígenas Munduruku protestam pela garantia e proteção de seu território'),
            'http://www.greenpeace.org/brasil/pt/Blog/experincia-munduruku-traz-a-amaznia-para-o-ce/blog/59624/':('Blog','Proteja a Natureza','Florestas','Resista','Migrate','Story','“Experiência Munduruku” traz a Amazônia para o centro de São Paulo'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Sob-ameaca-de-grandes-hidreletricas--povo-Munduruku-exige-demarcacao-de-territorio-tradicional-no-rio-Tapajos/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Story','Sob ameaça de hidrelétricas, povo Munduruku exige demarcação de território tradicional no Tapajós'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Cancelamento-de-Sao-Luiz-do-Tapajos-um-passo-para-o-futuro/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Story','Cancelamento de São Luiz do Tapajós: um passo para o futuro'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Funai-reconhece-territorio-tradicional-dos-Munduruku-no-rio-Tapajos/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Story','Funai reconhece território tradicional do povo Munduruku no rio Tapajós'),
            #'http://www.greenpeace.org/brasil/pt/Noticias/Funai-reconhece-territorio-tradicional-dos-Munduruku-no-rio-Tapajos/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Story','Funai reconhece território tradicional do povo Munduruku no rio Tapajós'),
            'http://www.greenpeace.org/brasil/pt/Noticias/O-mapa-da-vida/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Story','O mapa da vida'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Hidreletricas-ameacam-os-rios-da-Amazonia/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Story','14 de março: Dia Internacional de Luta Contra as Barragens e pelos Rios'),
            #'http://www.greenpeace.org/brasil/pt/Noticias/Energia-solar-brilha-para-o-povo-Munduruku/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Story','Energia solar brilha para o povo Munduruku'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Para-garantir-a-demarcacao-povo-Munduruku-lanca-o-Mapa-da-Vida/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Story','Para garantir a demarcação, povo Munduruku lança o “Mapa da Vida”'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Um-milhao-pelo-Tapajos/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Story','Um milhão pelo Tapajós!'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Made-in-Munduruku/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Story','Made in Munduruku'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Todos-Pela-Amazonia-a-pressao-vai-continuar/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Story','Todos Pela Amazônia: a pressão vai continuar!'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Nos-somos-todos-Amazonia/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Story','“Nós somos todos Amazônia”'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Pela-Amazonia-artistas-indigenas-e-ambientalistas-entregam-15-milhao-de-assinaturas-no-Congresso/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Story','Pela Amazônia, artistas e indígenas entregam 1,5 milhão de assinaturas no Congresso'),
            #'http://www.greenpeace.org/brasil/pt/Noticias/O-mapa-da-vida/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Story','O mapa da vida'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Apos-pressao-Temer-deve-revogar-extincao-da-Renca/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Story','Vitória! Após pressão, Temer revoga decreto que extingue a Renca'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Greenpeace-denuncia-garimpos-ilegais-na-Renca/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Story','Greenpeace denuncia garimpos ilegais na Renca'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Mobilizacao-pela-Amazonia-reune-milhares-em-13-cidades-brasileiras/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Story','Mobilização pela Amazônia reúne milhares em 14 cidades brasileiras'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Governo-Temer-ira-provocar-danos-irreversiveis-na-Amazonia/':('News','Proteja a Natureza','Florestas','Resista','Migrate','Story','Governo Temer irá provocar danos irreversíveis à Amazônia'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Sobre-transgenicos-hidreletricas-e-o-mau-uso-de-informacao-/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Sobre transgênicos, hidrelétricas e o mau uso de informação'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Decreto-pode-acabar-com-rotulagem-de-transgenico/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Decreto pode acabar com rotulagem de transgênico'),
            'http://www.greenpeace.org/brasil/pt/Noticias/Nao-tirem-o-nosso-Tesao/':('News','Transforme a Sociedade','Resista','','Migrate','Story','Não tirem o nosso Tesão!'),
        }

        for url,data in start_urls.iteritems():
            post_type, categories, tags1, tags2, action, p4_post_type, p4_title = data
            if ( post_type=='Blog' ):
                request = scrapy.Request(url, callback=self.parse_blog, dont_filter='true')
            elif ( post_type=='News' ):
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
            request.meta['p4_title'] = p4_title
            yield request

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

        imagesEnlarge=response.xpath('//div[@class="news-list"]//div[@class="post-content"]//a[@class="open-img EnlargeImage"]/@href').extract()
        imagesEnlarge_generated = list()
        for image_file in imagesEnlarge:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.org/',1)
            imagesEnlarge_generated.append(image_file)

        pdfFiles=response.css('div.news-list a[href$=".pdf"]::attr(href)').extract()
        pdf_files_generated = list()
        for pdf_file in pdfFiles:
            #print pdf_file
            if (pdf_file.startswith('/')):
                pdf_file = pdf_file.replace('/','http://www.greenpeace.org/',1)
                #print pdf_file
            pdf_files_generated.append(pdf_file)
            #print pdf_files_generated

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


        # Filter email id image and replace it with email text.
        delete_images = list()
        for image_file in imagesB_generated:
            if ("/emailimages/" in image_file):
                # PHP webservice script url.
                api_url = "http://localhost_test/test_script/email_img_to_text.php"
                end_point_url = api_url + "?url=" + image_file
                emailid = urllib2.urlopen(end_point_url).read(1000)
                delete_images.append(image_file)
                # Remove the email images from Post body and replace it with email text.
                body_text = re.sub(
                    '<img[a-zA-Z0-9="\s\_]*src=\"' + image_file + '\"[a-zA-Z0-9="\s]*>',
                    emailid, body_text)

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
            p4_title = extract_with_css('div.news-list h1::text')

        # To fix enlarge Images still leads to p3 issue - find and replace the anchor tag image link with src image link.
        delete_images_en = list()
        for image_file_en in imagesEnlarge_generated:
            for image_file_b in imagesB_generated:
                filename_en = image_file_en.split("/")[-1]
                filename_b  = image_file_b.split("/")[-1]

                if filename_en == filename_b:
                    # print "file names match " + filename_en
                    body_text = body_text.replace(image_file_en, image_file_b)
                    delete_images_en.append(image_file_en)

        # Remove the replaced enlarge images from list.
        for del_image_file_en in delete_images_en:
            imagesEnlarge_generated.remove(del_image_file_en)

        yield {
            'type': response.meta['p4_post_type'],
            'p3_image_gallery': p3_image_gallery,
            'title': p4_title,
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

        lead_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[1]/div/text()').extract()[0]
        body_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[2]').extract()[0]
        if body_text:
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.org/').replace('href="/', 'href="http://www.greenpeace.org/')
            body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)
            if lead_text:
                body_text = '<h4 class="leader">' + lead_text + '</h4>' + body_text + response.xpath(' //*[@id="content"]/div[4]/div/div[2]/p').extract_first()

        body_text = self.filter_post_content(body_text)

        #subtitle = extract_with_css('div.article h2 span::text')
        #if subtitle:
        #    body_text = '<h2>' + subtitle + '</h2><br />' + body_text

        #thumbnail = response.xpath('string(head//link[@rel="image_src"]/@href)').extract_first()

        date_field = response.css('div.article div.text span.author::text').re_first(r' - \s*(.*)')
        date_field = self.filter_month_name(date_field);
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
                    emailid, body_text)

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


        # To fix enlarge Images still leads to p3 issue - find and replace the anchor tag image link with src image link.
        delete_images_a = list()
        for image_file_a in imagesA_generated:
            for image_file_b in imagesB_generated:
                filename_a = image_file_a.split("/")[-1]
                filename_b = image_file_b.split("/")[-1]

                if filename_a == filename_b:
                    #print "file names match " + filename_a
                    body_text = body_text.replace(image_file_a, image_file_b)
                    delete_images_a.append(image_file_a)

        # Remove the replaced enlarge images from list.
        for del_image_file_a in delete_images_a:
            imagesA_generated.remove(del_image_file_a)

        yield {
            'type': response.meta['p4_post_type'],
            'p3_image_gallery': p3_image_gallery,
            'title': p4_title,
            #'subtitle': '',
            'author': 'Greenpeace Brasil',
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
        # Filter the youtube video and add embed shortcode instead.
        post_data = re.sub(
            '\<iframe[width\=\"height0-9\s]*src\=\"([https]*\:\/\/www.youtube.com[a-zA-Z0-9\/\=\-\?\_]*)\"[\=\"a-zA-Z\/\-\s0-9]*\>[\\n\s]*(.*)[\\n\s]*\<\/iframe\>',
            '[embed]\g<1>[/embed]', post_data)

        # Search and replace youtube url with https.
        post_data = post_data.replace('http://www.youtube.com', 'https://www.youtube.com')

        # Remove the <script> tags from content.
        post_data = re.sub(
            '<script[\s\S]type\=\"text\/javascript\"*?>[\s\S]*?<\/script>',
            '', post_data)

        return post_data

    def filter_month_name(self, month_name):
        month_br_en = {
            'jan': 'January',
            'fev': 'February',
            'mar': 'March',
            'abr': 'April',
            'mai': 'May',
            'jun': 'June',
            'jul': 'July',
            'ago': 'August',
            'set': 'September',
            'out': 'October',
            'nov': 'November',
            'dez': 'December',
        }

        if month_name:
            # Filter extra char from date string.
            month_name = month_name.replace(" at", "")
            month_name = month_name.replace(" às", "")
            # Replace the Portuguese month name with english month name.
            for br_month, en_month in month_br_en.iteritems():
                month_name = month_name.replace(br_month, en_month)

        return month_name;

    def csv_writer(self, data, path):
        # Write data to a CSV file path
        with open(path, "a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(data)
