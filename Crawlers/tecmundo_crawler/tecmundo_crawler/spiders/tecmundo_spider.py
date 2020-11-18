import scrapy
import datetime
from tecmundo_crawler import my_utils 

class Tecmundo_Spider(scrapy.Spider):
    name = "tecmundo"
    start_urls = [
        'https://www.tecmundo.com.br/cultura-geek'
    ]

    def parse(self, response):
        news_titles_href = response.css('.z--w-2-3 div:nth-child(2) a::attr(href)')
        if len(news_titles_href) == 0:
            raise Exception("Missing links from the Jovem Nerd initial site.")

        for href in news_titles_href.getall():
            yield scrapy.Request(href, self.parse_news_article)

    def parse_news_article(self, response):

        def glue_together_text(ls):
            paragraph_separator = '\n'
            return paragraph_separator.join(ls)

        def extract(query, obj = None):
            if obj is None:
                return response.css(query).get(default='').strip()
            elif obj == 'corpus':
                # Getting and filtering the first two components
                # Because it is the author's and.
                corpus = response.xpath(query).getall()[2:]
                corpus = my_utils.delete_since('PUBLICIDADE', corpus)
                return len(corpus), glue_together_text(corpus)
            elif obj == 'date':
                return response.css(query).get(default='').strip().split('/')

        n_paragraph, corpus = extract('.//p//text()', 'corpus')

        yield {
            'title': extract('#js-article-title::text'),
            'subtitle': '',
            'corpus': corpus,
            'author': extract('.author a::text'),
            'date': extract('#js-article-date strong', 'date'),
            'tag': extract('.tec--badge--primary::text'),
            'url': response.url,
            'n_paragraphs': n_paragraph
        }