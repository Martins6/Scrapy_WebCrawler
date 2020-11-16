import scrapy
import datetime
from webcrawler import my_utils 
from scrapy_selenium import SeleniumRequest


class Jornada_Geek_Spider(scrapy.Spider):
    name = "jornadageek"

    
    start_urls = [
        'https://www.jornadageek.com.br/novidades/'
    ]

    def parse(self, response):
        news_titles_href = response.css('.td-module-title a::attr(href)')
        if len(news_titles_href) == 0:
            raise Exception("Missing links from the jornadageek initial site.")
        
        n_news = 0
        for href in news_titles_href.getall():
            #href = response.urljoin(href)
            yield scrapy.Request(href, self.parse_news_article)
            n_news += 1
        print(f'NEWS N: {n_news}')

    def parse_news_article(self, response):

        def glue_together_text(ls):
            paragraph_separator = '\n'
            return paragraph_separator.join(ls)

        def format_date(date_string):
            """ Transform this 'jul 8, 2020' into this [8,7,2020]'
            """ 
            # Transforming into a list [jul, 8, 2020]
            date_list = date_string.replace(',', '').split(' ')
            date_list[0] = my_utils.month_pt_to_en(date_list[0])
            # Transforming 'Jul' into 7
            date_list[0] = datetime.datetime.strptime(date_list[0], "%b").month
            # Changing format from MM/DD/YYYY to be DD/MM/YYYY.
            day = date_list[1]
            month = date_list[0]
            date_list[0] = day
            date_list[1] = month

            return date_list

        def extract(query, obj = None):
            if obj is None:
                return response.css(query).get(default='').strip()
            elif obj == 'corpus':
                corpus = response.xpath(query).getall()
                try:
                    corpus = my_utils.delete_since('Confira também:\xa0', corpus)
                except:
                    print('NÃO DEU BOM')
                
                return glue_together_text(corpus)
            elif obj == 'date':
                return format_date(response.css(query).get(default='').strip())

        yield {
            'title': extract('.tdb-title-text::text'),
            'subtitle': extract('p:nth-child(1)::text'),
            'corpus': extract('.//p//text()|//h3//strong//text()', 'corpus'),
            'author': extract('.tdb-author-name::text'),
            'date': extract('.td-module-date::text', 'date'),
            'tag': extract('.tdb-tags a::text'),
            'url': response.url
        }