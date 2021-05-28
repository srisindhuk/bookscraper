import pandas as pd


class createfile:

    row_list = []

    def __init__(self, books):
        self.books = books

    @property
    def createcsv(self) -> bool:
        for book in self.books:
            list = [book.name, book.price, book.rating, book.description]
            createfile.row_list.append(list)

        finaldata = pd.DataFrame(createfile.row_list, columns=["name", "price", "rating", "description"])
        finaldata.to_csv("data.csv")
        return True

