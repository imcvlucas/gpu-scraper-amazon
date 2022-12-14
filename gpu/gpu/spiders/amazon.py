import scrapy


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['www.amazon.ca']
    start_urls = [
        'https://www.amazon.ca/s?k=graphics+card+3060&crid=1539D0IUMM0IU&sprefix=graphics+card+3060+%2Caps%2C96&ref=nb_sb_noss',
        'https://www.amazon.ca/s?k=graphics+card+3060+ti&crid=1Z8GJA5BY8DFW&sprefix=graphics+card+3060+ti%2Caps%2C111&ref=nb_sb_noss',
        'https://www.amazon.ca/s?k=graphics+card+3070&crid=16U73G3JHP29I&sprefix=graphics+card+3070+%2Caps%2C92&ref=nb_sb_noss',
        'https://www.amazon.ca/s?k=graphics+card+3070+ti&crid=2DCFES58X63NJ&sprefix=graphics+card+3070+ti%2Caps%2C106&ref=nb_sb_noss',
        'https://www.amazon.ca/s?k=graphics+card+3080&crid=TI694OTJJXR6&sprefix=graphics+card+3080%2Caps%2C111&ref=nb_sb_noss',
        'https://www.amazon.ca/s?k=graphics+card+3080+ti&crid=R3RL2VJM6O9B&sprefix=graphics+card+3080+ti%2Caps%2C160&ref=nb_sb_noss',

        ]


    def parse(self, response):
        # Product frame
        products = response.css('div.s-card-container.s-overflow-hidden.aok-relative.s-expand-height.s-include-content-margin.s-latency-cf-section.s-card-border')
        # Iterate through all the products
        for product in products: 
            # Data points
            name = product.css('h2.a-size-mini span.a-size-base-plus::text').get()
            cur_price = product.css('div.a-row span.a-offscreen::text').get()
            orig_price = product.css('div.a-row span.a-text-price span.a-offscreen::text').get()
            shipping = product.css('div.a-row span.a-color-base::text').get()
            review = product.css('div.a-row span::attr(aria-label)').get()
            link = 'https://www.amazon.ca' + product.css('h2.a-size-mini a.a-link-normal::attr(href)').get()
            # Get Brand
            words = name.upper().split(' ')
            brand = [word for word in words if word in ['MSI','ZOTAC','ASUS','EVGA','GIGABYTE']]
            # Get GPU Series
            series = [words[i] + ' ' + words[i+1] if words[i+1] == 'TI' else words[i] for i in range(len(words)) if words[i] in ['3060','3070','3080'] ]
            series = ' '.join(set(series))

            item = {
                'Brand' : brand,
                'GPU Series' : series,
                'Product Name' : name,
                'Current Price' : cur_price,
                'Original Price' : orig_price,
                'Shipping' : shipping,
                'Reviews' : review,
                'Link' : link,
            }
            yield item

        # Pagination
        pagination_link = response.css('a.s-pagination-item::attr(href)').get() # Find the link to the next page
        if pagination_link is not None:
            yield response.follow(pagination_link, callback=self.parse)

