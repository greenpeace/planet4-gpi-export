
1. Have python and pip working

1. Install virtualenv ( https://virtualenv.pypa.io/en/stable/installation/ )

1. make a directory where your project will run

   `mkdir p3-gpi-export`
   
1. Tell it to run in a vritualenv

   `virtualenv p3-gpi-export`
   
1. Go in the directory

   `cd p3-gpi-export`

1. Start the virtualenv   

   `source bin/activate`
   
1. Install scrapy

    `pip install Scrapy`   

1. Install dateparser

    `pip install dateparser`   

1. Initiate a scrapy project

   `scrapy startproject p3_gpi_export`

1. Download the crawler
    
    `git clone https://github.com/greenpeace/planet4-gpi-export`

1. Copy the crawler file in the scrapy project crawlers

    `cp planet4-gpi-export/all_spider.py p3_gpi_export/p3_gpi_export/spiders/all_spider.py`

1. Go in the directory of the scrapy project   

   `cd p3_gpi_export/`   

1. Run the crawler

    `scrapy crawl all`

