import os
import datetime
import json
from pathlib import Path

# Get separate data from Crawlers
t1 = datetime.datetime.now()
os.system('cd Crawlers/jornada_geek_crawler && scrapy crawl jornadageek -o data.jl')
os.system('cd Crawlers/jovem_nerd_crawler && scrapy crawl jovemnerd -o data.jl')
os.system('cd Crawlers/tecmundo_crawler && scrapy crawl tecmundo -o data.jl')
t2 = datetime.datetime.now()
crawl_duration = t2 - t1


# Writing out a single big data
def duplicate_news(json_line_dict, json_file_dict, key = 'url'):
    """Check if the json_line_dict is already in the json_file_dict by key.
    Returns True if there is a duplicate and False otherwise.

    Returns: Bool
    """
    target_value = json.loads(json_line_dict)[key]

    flag = False
    with Path(json_file_dict).open() as json_file:
        for file_line in json_file:
            flag = (target_value == json.loads(file_line)[key])
            if flag:
                return(flag)
    return(flag)

# Proof of incremental load
def file_len(fname):
    with Path(fname).open() as f:
        n = 0
        for l in f:
            n += 1
    return n

try:
    initial_len = file_len('crawled_data.jl')
except:
    initial_len = 0

crawlers = ['jovem_nerd_crawler', 'tecmundo_crawler', 'jornada_geek_crawler']
data_folder = Path('Crawlers')

with Path('crawled_data.jl').open('a') as big_file:
    for crawler in crawlers:
        data_file = data_folder / crawler / 'data.jl'
        with data_file.open() as unprocessed_data:
            for json_line in unprocessed_data:
                if not duplicate_news(json_line, 'crawled_data.jl'):
                    big_file.write(json_line)
        # Delete file
        data_file.unlink()


print(f'WHOLE PROCESS DURATION: {datetime.datetime.now() - t1}')
print(f'CRAWL DURATION: {crawl_duration}')
print(f"NEWS # BEFORE CRAWL: {initial_len}")
print(f"NEWS # AFTER CRAWL: {file_len('crawled_data.jl')}")