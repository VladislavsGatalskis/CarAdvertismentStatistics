import os
import json
import time
from datetime import date
from halo import Halo   # INFO about Halo (https://pythonawesome.com/beautiful-spinners-for-terminal-ipython-and-jupyter/)

start = time.time()
today = date.today()

# Location of the scrapy project
scrapyBaseLocation = os.path.dirname(os.path.realpath(__file__))
print("PATH: ", scrapyBaseLocation)

# adStatus is meant for checking if the data is correctly scraped so it could be used in the WebApp (in the future)
adStatus = open(f"{scrapyBaseLocation}/adverts/adverts_{today}_status.txt","w")
adStatus.write("unfinished") # At the beginning set to unfinished; if successfully scraped, changes to finished
adStatus.close()

# Makes adverts file EMPTY (overwrites existing file of the particular date or creates a new one)
file = open(f"{scrapyBaseLocation}/adverts/adverts_{today}.json","w")
file.write("")
file.close()

# If output.log exists, clear the content for new logging (MAYBE CREATE FOLDER WITH logs for every run???)
file = open(f"{scrapyBaseLocation}/output.log","w")
file.write("")
file.close()

# Changes direction to the folder where ?scrapy.cfg is located? (terminal command line below (os.system..) only executes if in specified dir below)
os.chdir(f"{scrapyBaseLocation}")
with Halo(text='Scraping in progress', spinner='dots'):
    os.system(f"scrapy crawl adverts_v2 -o adverts/adverts_{today}.json --logfile output.log")
    # os.system(f"scrapy crawl adverts_v2 -o adverts/adverts_{today}.json")

# import json file to variable 'data' and sort it
with open(f'{scrapyBaseLocation}/adverts/adverts_{today}.json', encoding='utf-8') as json_file:
    data = json.load(json_file)
    data = sorted(data, key=lambda k: (k.get('Marka', 0), k.get('Modelis',0))) # (SORTING INFO: https://www.geeksforgeeks.org/ways-sort-list-dictionaries-values-python-using-lambda-function/)
    # data = sorted(data, key=lambda k: k.get('Marka', 0), reverse=False)

# export sorted data
with open(f'{scrapyBaseLocation}/adverts/adverts_{today}.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

adStatus = open(f"{scrapyBaseLocation}/adverts/adverts_{today}_status.txt","w")
adStatus.write("finished")
adStatus.close()

print('It took', time.time()-start, f'seconds ({(time.time()-start) / 60} minutes) to get all the necassery information.')

# # For automatic diagram creation after the data scraping
# os.chdir(f"{projectLocation}/CarAdvertismentStatistics/")
# os.system(f'python {projectLocation}/CarAdvertismentStatistics/advertscrape/some_py_scripts/diagramCreator.py')