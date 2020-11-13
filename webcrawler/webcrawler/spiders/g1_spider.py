import scrapy

class g1Spider(scrapy.Spider):
    name = "g1"
    start_urls = [
        'https://g1.globo.com/'
    ]

    def parse(self, response):
        n_news = 0

        if len(response.css('.feed-post-link::attr(href)')) == 0:
            raise Exception('Missing links from the G1 initial site.')

        for news_title_hyperlink in response.css('.feed-post-link::attr(href)').getall():            
            yield from scrapy.Request(news_title_hyperlink, callback=self.parse_news_article)
            
            n_news += 1
        print(f'NEWS N: {n_news}')

    def parse_news_article(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'title': extract_with_css('.content-head__title'),
            'subtitle': extract_with_css('.content-head__subtitle'),
            'corpus': extract_with_css('.author-description::text'),
        }