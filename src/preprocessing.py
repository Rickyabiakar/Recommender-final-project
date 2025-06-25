import pandas as pd

def load_filtered_data():
    ratings = pd.read_csv("data/BX-Book-Ratings.csv", sep=";", encoding="ISO-8859-1")
    books = pd.read_csv("data/BX-Books.csv", sep=";", encoding="ISO-8859-1", on_bad_lines='skip', low_memory=False)

    ratings.columns = ['user_id', 'isbn', 'rating']
    books.columns = ['isbn', 'book_title', 'book_author', 'year_of_publication', 'publisher',
                     'image_url_s', 'image_url_m', 'image_url_l']

    merged = pd.merge(ratings, books[['isbn', 'book_title']], on='isbn')

    active_users = merged['user_id'].value_counts()[merged['user_id'].value_counts() > 5].index
    popular_books = merged['book_title'].value_counts()[merged['book_title'].value_counts() > 10].index
    filtered = merged[(merged['user_id'].isin(active_users)) & (merged['book_title'].isin(popular_books))]

    return filtered
