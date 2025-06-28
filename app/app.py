"""Streamlit UI for the Book Recommender System."""

import os
import sys

import streamlit as st

from src.llm_explainer import explain_recommendations
from src.preprocessing import load_filtered_data
from src.recommender import build_model, predict_ratings

# Add src to path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Set app title
st.title("📚 Book Recommender System")

# Load and process data
df = load_filtered_data()
book_pivot, similarity_df = build_model(df)

# User input
user_id = st.selectbox("Select a User ID", sorted(book_pivot.columns))

# Button to trigger recommendations
if st.button("Get Recommendations"):
    recommended_books = predict_ratings(
        user_id, book_pivot, similarity_df, top_n=5
    )

    if (
        isinstance(recommended_books, list)
        and recommended_books[0] == "User not found."
    ):
        st.error("User ID not found in the data.")
    else:
        st.subheader("Top 5 Book Recommendations:")
        for i, title in enumerate(recommended_books, 1):
            st.write(f"{i}. {title}")

        # LLM explanation
        explanation = explain_recommendations(recommended_books)
        st.markdown("### 🤖 LLM Explanation")
        st.write(explanation)
