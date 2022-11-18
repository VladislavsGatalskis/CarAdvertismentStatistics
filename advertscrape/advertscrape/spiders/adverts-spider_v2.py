import scrapy

class AdvertsSpider(scrapy.Spider):
    name = "adverts_v2"
    start_urls = [
        "https://www.ss.com/transport/cars/"
    ]

    def parse (self,response):
        for section in response.css('form table:nth-child(3) td'):
            for el in section.css('h4 a'):
                section_url = el.attrib['href']
                section_url = response.urljoin(section_url)
                yield scrapy.Request(section_url, callback=self.parseSection)
            break

    def parseSection (self,response):
        isFirst = True
        for ad in response.css('form table:nth-child(3) tr'):
            if(isFirst): # skiping first elem which is 'header' tr element
                isFirst = False
                continue
            if ad.css('td:nth-child(3) div a::attr(href)').get() is not None:
                # Parse each url
                adUrl = "http://www.ss.com" + ad.css('td:nth-child(3) div a').attrib['href']
                yield scrapy.Request(adUrl, callback=self.parseAd)

        # Getting the next page url from "Nākamie" button
        next_page_url = response.css('form#filter_frm div.td2 a:last-child').attrib['href']
        
        if "page" in next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parseSection)


    def parseAd(self, response):
        current = {}

        make = response.css('div#msg_div_msg table table tr:first-child')
        make = make.css('td:last-child ::text').get()

        model = response.css('h2 a:nth-child(3)::text').get() 
        newMake = make[:make.find(model)-1]

        # Marka
        current['Marka'] = newMake

        # Modelis
        current['Modelis'] = model

        # Citi (except Marka)
        isFirst = True
        for i in response.css('div#msg_div_msg table table tr'):
            # skiping first elem which is 'header' tr element
            if(isFirst):
                isFirst = False
                continue
            current[i.css('td:first-child ::text').get()] = i.css('td:last-child ::text').get()

        # Cena
        current['Cena'] = response.css('span#tdo_8::text').get()

        # Vieta
        for i in response.css('div#content_main_div div#tr_cont tr'):     
            if type(i.css('td:first-child ::text').get()) is str: 
                if "Vieta" in i.css('td:first-child ::text').get():
                    current[i.css('td:first-child ::text').get()] = i.css('td:last-child ::text').get()
                    break

        current['url'] = response.request.url
        yield current