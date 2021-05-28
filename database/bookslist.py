import requests
from pages.all_books_page import  AllBooksPage

page_content = requests.get('http://books.toscrape.com').content
page = AllBooksPage(page_content)
# books = page.books
books = []

for pagenum in range(page.pagecount):

    url = f"http://books.toscrape.com/catalogue/page-{pagenum+1}.html"
    page_content = requests.get(url).content
    page = AllBooksPage(page_content)
    books.extend(page.books)
