import os
import datetime


t1 = datetime.datetime.now()

os.system('cd Crawlers/jornada_geek_crawler && scrapy crawl jornadageek -o data.jl')
os.system('cd Crawlers/jovem_nerd_crawler && scrapy crawl jovemnerd -o data.jl')
os.system('cd Crawlers/tecmundo_crawler && scrapy crawl tecmundo -o data.jl')


t2 = datetime.datetime.now()

print(t2 - t1)