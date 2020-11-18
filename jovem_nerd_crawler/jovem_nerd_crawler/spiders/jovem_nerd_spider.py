import scrapy
import datetime
from jovem_nerd_crawler import my_utils 

class Jovem_Nerd_Spider(scrapy.Spider):
    name = "jovemnerd"
    start_urls = [
        'https://jovemnerd.com.br/nerdbunker/'
    ]

    def parse(self, response):
        news_titles_href = response.css('.title a::attr(href)')
        if len(news_titles_href) == 0:
            raise Exception("Missing links from the Jovem Nerd initial site.")

        for href in news_titles_href.getall():
            yield scrapy.Request(href, self.parse_news_article)

    def parse_news_article(self, response):

        def glue_together_text(ls):
            paragraph_separator = '\n'
            return paragraph_separator.join(ls)


        def format_date(date_string):
            """ Transform this '12 de novembro de 2020 às 17h13 • Atualizado há 1 dia'
            into this [12,11,2020]'
            """ 
            # Focusing on the first part, ignoring exact hour
            date_string = my_utils.delete_since(' às', date_string).replace('de', '').replace('  ', ' ')
            # Transforming into a list [12, Nov, 2020]
            date_list = date_string.split(' ')
            date_list[1] = my_utils.month_pt_to_en(date_list[1], abv=False)
            # Transforming 'Nov' into 11
            date_list[1] = datetime.datetime.strptime(date_list[1], "%b").month

            return date_list

        def extract(query, obj = None):
            if obj is None:
                return response.css(query).get(default='').strip()
            elif obj == 'corpus':
                # Getting and filtering the first component
                # Because it is already the subtitle.
                corpus = response.css(query).getall()[1:]
                print(corpus)
                corpus = my_utils.delete_since('Leia mais sobre: ', corpus)
                return len(corpus), glue_together_text(corpus)
            elif obj == 'date':
                return format_date(response.css(query).get(default='').strip())

        n_paragraph, corpus = extract('p::text, p a::text', 'corpus')

        yield {
            'title': extract('.title::text'),
            'subtitle': extract('.excerpt::text'),
            'corpus': corpus,
            'author': extract('.author a::text'),
            'date': extract('.postedon::text', 'date'),
            'tag': extract('.post-tags a::text'),
            'url': response.url,
            'n_paragraphs': n_paragraph
        }