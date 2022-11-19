# CarAdvertismentStatistics

Application that scrapes data using Scrapy framework from SS.COM for creating some statistics about car adverts. 

NOTE: Tested on python 3.7.9.

Installation: 
1) Clone the repo
2) Open the project folder
3) Create virtual environment 
4) Activate venv
5) Run 'pip install -r requirements.txt' command.

Usage:
To Scrape the data, run the 'run.py' script.
To create diagrams from scraped data, run diagramCreator.py

To scrape the data you have to run the run.py script (/advertscrape/some_py_scripts/run.py). After it's done run diagramCreator.py script (/advertscrape/some_py_scripts/diagramCreator.py) and it will open 4 diagrams in your browser (the diagramCreator.py script is hardcoded to create the diagrams from the data that was scraped on 2020-05-28; you can change that).
