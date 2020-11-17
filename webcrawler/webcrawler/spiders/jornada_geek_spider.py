import scrapy
import datetime
from webcrawler import my_utils 

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chrome_options
from webdriver_manager.chrome import ChromeDriverManager

def setup_selenium_driver():
    """Setting up a selenium driver with Google Chrome. It can be modified to use for an server.
    Or with different browsers: Firefox, Chromium, etc.
    """

    options = chrome_options()
    # silent or without browser mode
    options.add_argument('--headless')
    # no printing log in the terminal
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), \
         chrome_options=options)

    return(driver)

def selenium_extract_until_keyword_find(driver, url, keyword, query, xpath = True):
    """If we need to activate a JavaScript action, like scrolling down
    to find the end of the article, we must use Selenium to do such a task.
    The bad thing is that it is slow. Really slow.
    """
    # Opening the url in the browser
    driver.get(url)
    sleep(3)

    # We must clean our query to not retrieve text only but retrieve the html block.
    query = query.replace('//text()', '')
    
    # Extracting what we want
    if xpath:
        corpus = [result.text for result in driver.find_elements_by_xpath(query)]
    else:
        corpus = [result.text for result in driver.find_elements_by_css_selector(query)]
    
    def keyword_in_list(keyword, ls):
        return (True in map(lambda x: keyword in x, ls))

    safeguard = 0
    while not keyword_in_list(keyword, corpus) and safeguard < 3:
        # Scrolling down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)
        # Extracting what we want
        if xpath:
            corpus = [result.text for result in driver.find_elements_by_xpath(query)]
        else:
            corpus = [result.text for result in driver.find_elements_by_css_selector(query)]

        safeguard += 1
    if safeguard == 3:
        # Closing webdriver
        driver.close()
        raise Exception('There is no Keyword in the page.')
    # Closing webdriver
    driver.quit()
    return corpus
    

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

                keyword = 'Confira também:'
                if keyword in corpus:
                    corpus = my_utils.delete_since(keyword, corpus)
                else:
                    corpus = selenium_extract_until_keyword_find(setup_selenium_driver(), \
                        response.url, \
                        keyword, \
                        query)
                    corpus = my_utils.delete_since(keyword, corpus)
                
                return glue_together_text(corpus)

            elif obj == 'date':
                return format_date(response.css(query).get(default='').strip())

        yield {
            'corpus': extract(".//p//text()|//*[contains(text(),'Confira também:')]", 'corpus'),
            'title': extract('.tdb-title-text::text'),
            'subtitle': extract('p:nth-child(1)::text'),
            'author': extract('.tdb-author-name::text'),
            'date': extract('.td-module-date::text', 'date'),
            'tag': extract('.tdb-tags a::text'),
            'url': response.url
        }