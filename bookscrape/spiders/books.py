import scrapy

class BooksListSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]

    max_pages = 10   
    current_page = 1

    start_urls = ["https://books.toscrape.com/catalogue/page-1.html"]

    def parse(self, response):
        books = response.css("article.product_pod")

        for book in books:
            yield {
                "title": book.css("h3 a::attr(title)").get(),
                "price": book.css("p.price_color::text").get(),
                "rating": book.css("p.star-rating::attr(class)").get().replace("star-rating ", ""),
                "availability": book.css("p.instock.availability::text").get().strip(),
                "detail_url": response.urljoin(book.css("h3 a::attr(href)").get()),
            }

        if self.current_page < self.max_pages:
            next_page = response.css("li.next a::attr(href)").get()
            if next_page:
                self.current_page += 1
                next_url = response.urljoin(next_page)
                yield scrapy.Request(next_url, callback=self.parse)
