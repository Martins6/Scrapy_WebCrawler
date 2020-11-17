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
    #options.add_argument('--headless')
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
    while not keyword_in_list(keyword, corpus) and safeguard < 2:
        # Scrolling down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        sleep(5)
        # Extracting what we want
        if xpath:
            corpus = [result.text for result in driver.find_elements_by_xpath(query)]
        else:
            corpus = [result.text for result in driver.find_elements_by_css_selector(query)]

        safeguard += 1
    print(f'CORPUS: {corpus}')
    if safeguard == 2:
        # Closing webdriver
        driver.close()
        raise Exception('There is no Keyword in the page.')
    
    # Closing webdriver
    driver.close()
    return corpus

url = 'https://www.jornadageek.com.br/videogame/spider-man-miles-morales-review/' 
selenium_extract_until_keyword_find(setup_selenium_driver(),\
    url, \
        'Confira também:', \
            "//*[contains(text(),'Confira também:')]")
