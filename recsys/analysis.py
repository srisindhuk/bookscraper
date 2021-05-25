import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import pickle
from database.bookslist import books
from database.csvdatafile import createfile

finaldata = []
title_matrix = []

csvfile = createfile(books)
#if csvfile.createcsv:
    # data = pd.read_csv("../database/data.csv")
finaldata = pd.read_csv("data.csv")
finaldata.columns = ["id","name","price","rating","description"]


vect = CountVectorizer(analyzer='word', ngram_range=(1, 2), stop_words='english', min_df = 0.001)
vect.fit(finaldata['name'])
title_matrix = vect.transform(finaldata['name'])
pickle.dump(vect, open('books.pkl', 'wb'))







