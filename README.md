# WebCrawler

This is a project to crawl 3 news brazillian websites with a focus on Geek content. Jovem Nerd, Jornada Geek and Tecmundo. It was written with Python and we used two frameworks Scrapy and Selenium to crawl the websites. The result is a JSON Lines file with all the websites' news crawled.

## Setup

Install Anaconda and Scrapy.

## Usage

All you got to do is run the *Data_Processing.py* script with the necessary Python packages installed in the environment. It will run all the Crawlers and generate a JSON Lines file named *crawled_data.jl* coded in the Unicode format in the WebCrawler folder.

If you wish to check the logs of each site crawler, for example the 'Jornada Geek' site: just acess *Crawler/jornada_geek_crawler/logfile_jornada_geek.log* .

## Text Analysis

There is also some example of text analysis with Juypter Notebooks in the __ folder.
