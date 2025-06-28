"""Module for building similarity model and generating recommendations."""

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def build_model(filtered_df):
    """
    Build pivot table and cosine similarity matrix.

    Args:
        filtered_df (pd.DataFrame): Filtered dataset.

    Returns:
        tuple: (pivot table, similarity matrix)
    """
    book_pivot = filtered_df.pivot_table(
        index="book_title", columns="user_id", values="rating"
    ).fillna(0)
    book_pivot.index = book_pivot.index.str.strip()
    similarity = cosine_similarity(book_pivot)
    similarity_df = pd.DataFrame(
        similarity, index=book_pivot.index, columns=book_pivot.index
    )
    return book_pivot, similarity_df


def predict_ratings(user_id, book_pivot, similarity_df, top_n=5):
    """
    Predict top-N recommended books for a given user.

    Args:
        user_id (str): The user ID.
        book_pivot (pd.DataFrame): Book-user rating matrix.
        similarity_df (pd.DataFrame): Book-book similarity matrix.
        top_n (int): Number of recommendations.

    Returns:
        list: List of book titles.
    """
    if user_id not in book_pivot.columns:
        return ["User not found."]

    user_ratings = book_pivot[user_id]
    predicted_ratings = pd.Series(index=book_pivot.index, dtype=float)

    for book in book_pivot.index:
        if book not in similarity_df.columns:
            continue
        sim_scores = similarity_df[book]
        mask = user_ratings > 0
        numerator = (sim_scores[mask] * user_ratings[mask]).sum()
        denominator = sim_scores[mask].abs().sum()
        predicted_ratings[book] = (
            numerator / denominator if denominator != 0 else 0
        )

    rated_books = book_pivot[user_id][book_pivot[user_id] > 0].index
    predicted_ratings = predicted_ratings.drop(rated_books)
    return (
        predicted_ratings.sort_values(ascending=False)
        .head(top_n)
        .index.tolist()
    )
