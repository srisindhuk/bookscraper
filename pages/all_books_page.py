import re
from bs4 import BeautifulSoup
from locaters.all_books_pages import AllBooksPageLocators
from parsers.BookParser import BookParser


class AllBooksPage:
    def __init__(self,page_content):
        self.soup = BeautifulSoup(page_content, 'html.parser')

    @property
    def books(self):
        return (BookParser(e) for e in self.soup.select(AllBooksPageLocators.BOOKS))

    @property
    def pagecount(self):
        content = self.soup.select_one(AllBooksPageLocators.PAGER).string
        pattern = 'Page [0-9]+ of ([0-9]+)'
        matcher = re.search(pattern, content)
        noofpages = int(matcher.group(1))
        return noofpages


