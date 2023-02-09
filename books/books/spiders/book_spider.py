import scrapy


class BookSpider(scrapy.Spider):
    name = 'labirint'
    start_urls = ['https://www.labirint.ru/foreignbooks/']

    def parse(self, response, **kwargs):
        for link in response.css('div.product-cover a::attr(href)'):
            yield response.follow(link, callback=self.parse_book)

        for page in range(1, 11):
            next_page = f'https://www.labirint.ru/books/?page={page}'
            yield response.follow(next_page, callback=self.parse)

    @staticmethod
    def parse_book(response):
        name = response.css('h1::text').get()
        price = response.css('div.buying-priceold-val span.buying-priceold-val-number::text').get()
        if name != 'Рецензии на книгу «' and price is not None:
            yield {
                'name': name,
                'price': price
            }
