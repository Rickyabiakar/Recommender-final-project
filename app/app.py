import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.preprocessing import load_filtered_data
from src.recommender import build_model, predict_ratings
from src.llm_explainer import explain_recommendations

st.title("📚 Book Recommender System")

df = load_filtered_data()
book_pivot, similarity_df = build_model(df)

user_id = st.selectbox("Select a User ID", sorted(book_pivot.columns))

if st.button("Get Recommendations"):
    recommended_books = predict_ratings(user_id, book_pivot, similarity_df, top_n=5)

    if isinstance(recommended_books, list) and recommended_books[0] == "User not found.":
        st.error("User ID not found in the data.")
    else:
        st.subheader(" Top 5 Book Recommendations:")
        for i, title in enumerate(recommended_books, 1):
            st.write(f"{i}. {title}")

        # ✅ LLM explanation
        explanation = explain_recommendations(recommended_books)
        st.markdown("### 🤖 LLM Explanation")
        st.write(explanation)
