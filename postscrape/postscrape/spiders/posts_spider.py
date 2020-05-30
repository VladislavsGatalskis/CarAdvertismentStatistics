import scrapy

class PostsSpider(scrapy.Spider):
    name = "posts"
    start_urls = [
        'https://blog.scrapinghub.com/'
    ]    

    def parse(self, response):
        for post in response.css('div.post-item'):
            yield{
                'title': post.css('.post-header h2 a::text')[0].get(),
                'date': post.css('.post-header a::text')[1].get(),
                'author': post.css('.post-header a::text')[2].get()
            }