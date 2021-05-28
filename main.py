from flask import Flask, request, render_template
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import pickle
from recsys.analysis import finaldata, title_matrix


data = finaldata

def get_id(name):
    if data['name'].str.contains(name).any():
        result = data[data['name'].str.contains(name)]
        return result['id']


def writetohtml(bookid, title_matrix,vect):
    if bookid is None:
        print("bookid is null")
        return False
    else:
        res = return_sim_books(int(bookid), title_matrix, vect, top_n=20)
        html = res.to_html()
        file = open('templates/displaybook.html', 'w')
        file.write(html)
        file.close()
        return True
# lets wrap the above code in a function
def return_sim_books(book_id, title_matrix, vectorizer, top_n=10):
    # generate sim matrix
    sim_matrix = cosine_similarity(title_matrix, title_matrix)
    features = vectorizer.get_feature_names()

    top_n_idx = np.flip(np.argsort(sim_matrix[book_id,]), axis=0)[:top_n]
    top_n_sim_values = sim_matrix[book_id, top_n_idx]

    # find top n with values > 0
    top_n_idx = top_n_idx[top_n_sim_values > 0]
    scores = top_n_sim_values[top_n_sim_values > 0]

    # find features from the vectorized matrix
    sim_books_idx = data['name'].iloc[top_n_idx].index
    words = []
    for book_idx in sim_books_idx:
        try:
            feature_array = np.squeeze(title_matrix[book_idx,].toarray())
        except:
            feature_array = np.squeeze(title_matrix[book_idx,])
        idx = np.where(feature_array > 0)
        words.append([" , ".join([features[i] for i in idx[0]])])

    # collate results
    res = pd.DataFrame({"name": data['name'].iloc[book_id],
                        "sim_books": data['name'].iloc[top_n_idx].values, "words": words,
                        "scores": scores}, columns=["name", "sim_books", "scores", "words"])

    return res

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('post.html')


@app.route('/suggest')
def suggest():
    return render_template('post.html')


@app.route('/post')
def recommendbook():
    # Works only for a single sample
    bookdata = request.args.get('title')  # Get data posted as a json
    model = pickle.load(open('books.pkl', 'rb'))
    if writetohtml(get_id(bookdata),title_matrix, vect=model):
        print("came here")
        return render_template('displaybook.html')
    else:
        return render_template('404.html',message =f" no books related to{bookdata} found")


if __name__ == '__main__':
    app.run(debug=True)