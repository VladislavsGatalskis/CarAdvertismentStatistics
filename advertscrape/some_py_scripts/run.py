import os
import json
import time
from datetime import date

start = time.time()
today = date.today()

projectLocation = "C:/Users/vlads/Desktop/LU/2.kurss/4.sem/Python/Codes/GalaDarbs_v3"

# adStatus is meant for checking if the data is correctly scraped so it could be used in the WebApp (in the future)
adStatus = open(f"{projectLocation}/advertscrape/adverts_{today}_status.txt","w")
adStatus.write("unfinished") # At the beginning set to unfinished; if successfully scraped, changes to finished
adStatus.close()

# Makes adverts file EMPTY (overwrites existing file of the particular date or creates a new one)
file = open(f"{projectLocation}/advertscrape/adverts_{today}.json","w")
file.write("")
file.close()

# Changes direction to the folder where ?scrapy.cfg is located? (terminal command line below (os.system..) only executes if in specified dir below)
os.chdir(f"{projectLocation}/advertscrape")
os.system(f"scrapy crawl adverts_v2 -o adverts_{today}.json")

# import json file to variable 'data' and sort it
with open(f'{projectLocation}/advertscrape/adverts_{today}.json', encoding='utf-8') as json_file:
    data = json.load(json_file)
    data = sorted(data, key=lambda k: (k.get('Marka', 0), k.get('Modelis',0))) # (SORTING INFO: https://www.geeksforgeeks.org/ways-sort-list-dictionaries-values-python-using-lambda-function/)
    # data = sorted(data, key=lambda k: k.get('Marka', 0), reverse=False)

# export sorted data
with open(f'{projectLocation}/advertscrape/adverts_{today}.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

adStatus = open(f"{projectLocation}/advertscrape/adverts_{today}_status.txt","w")
adStatus.write("finished")
adStatus.close()

print('It took', time.time()-start, f'seconds ({(time.time()-start) / 60} minutes) to get all the necassery information.')
