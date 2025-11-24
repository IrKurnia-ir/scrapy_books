import scrapy

class BooksSpider(scrapy.Spider):
    name = "category"

    def __init__(self, category="mystery", max_page=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category = category.lower()
        self.max_page = int(max_page)
        self.current_page = 1

    def start_requests(self):
        url = "http://books.toscrape.com/catalogue/category/books_1/index.html"
        yield scrapy.Request(url, callback=self.parse_categories)

    def parse_categories(self, response):
        for cat in response.css("div.side_categories ul li ul li"):
            name = cat.css("a::text").get().strip().lower()

            if self.category == name:
                category_url = response.urljoin(cat.css("a::attr(href)").get())
                yield scrapy.Request(category_url, callback=self.parse_category)
                return

    def parse_category(self, response):
        # batas halaman
        if self.current_page > self.max_page:
            return

        # scrape data
        for book in response.css("article.product_pod"):
            yield {
                "title": book.css("h3 a::attr(title)").get(),
                "price": book.css("p.price_color::text").get(),
            }

        # next page
        next_page = response.css("li.next a::attr(href)").get()
        if next_page and self.current_page < self.max_page:
            self.current_page += 1
            yield response.follow(next_page, callback=self.parse_category)
