import re
import requests
from bs4 import BeautifulSoup
from locaters.books_locator import BookLocaters


class BookParser:
    RATINGS ={
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5

    }

    def __init__(self,parent):
        self.parent = parent

    def __repr__(self):
        return f'({self.name}, {self.price}, {self.description}, {self.rating} )'

    @property
    def name(self):
        locator = BookLocaters.NAME_LOCATOR
        item_link = self.parent.select_one(locator)
        item_name=item_link.attrs['title']
        return item_name

    @property
    def link(self):
        locator = BookLocaters.LINK_LOCATOR
        items_link = self.parent.select_one(locator).attrs['href']
        return items_link

    @property
    def price(self):
        locator = BookLocaters.PRICE_LOCATOR
        item_price = self.parent.select_one(locator).string
        pattern = '([0-9]+\.[0-9]+)'
        matcher = re.search(pattern, item_price)
        return float(matcher.group(1))

    @property
    def rating(self):
        locator = BookLocaters.RATING_LOCATOR
        star_rating = self.parent.select_one(locator).attrs['class']
        rating_class = [r for r in star_rating if r != 'star-rating']
        rating_number = BookParser.RATINGS.get(rating_class[0])
        return rating_number

    @property
    def description(self):
        locator = BookLocaters.DESCRIPTION_LOCATOR
        booklink = f"http://books.toscrape.com/catalogue/{self.link}"
        page_content = requests.get(booklink).content

        soup = BeautifulSoup(page_content, 'html.parser')
        newparent = soup.select(locator)
        book_desc = newparent[2].attrs['content']
        return book_desc



