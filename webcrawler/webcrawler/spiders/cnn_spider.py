import scrapy

class CNNSpider(scrapy.Spider):
    name = "CNN"
    start_urls = [
        'https://www.cnnbrasil.com.br/nacional'
    ]

    def parse(self, response):
        news_titles_href = response.css('.news-list a::attr(href)')
        if len(news_titles_href) == 0:
            raise Exception("Missing links from the CNN initial site, or the site structure has changed.")
        n_news = 0
        for href in news_titles_href.getall():
            href = response.urljoin(href)
            yield scrapy.Request(href, self.parse_news_article)
            n_news += 1
        print(f'NEWS N: {n_news}')
        #return 

    def parse_news_article(self, response):
        def extract_with_css(query, obj = None):
            if obj is None:
                return response.css(query).get(default='').strip()
            elif obj == 'corpus':
                # The [:-1] is so we can ignore the last text which is 'Tópicos'.
                return response.css(query).getall()[:-1] 
        def extract_date(url):
            # YYYY/MM/DD format
            return url.split('/')[4:7]

        yield {
            'title': extract_with_css('.news-title::text'),
            'corpus': extract_with_css('p::text', 'corpus'),
            'author': extract_with_css('.authors-container::text'),
            'date': extract_date(response.url)
        }