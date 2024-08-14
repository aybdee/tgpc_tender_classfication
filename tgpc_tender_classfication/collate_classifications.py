import csv
from io import StringIO

import pandas as pd
import streamlit as st


def load_data(uploaded_file):
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        return data
    return None


def save_classifications(data):
    csv = data.to_csv(index=False)
    return csv


st.title("Tender Classification App")

# Input for categories
categories_input = st.text_input("Enter categories (comma-separated):")
categories = (
    [cat.strip() for cat in categories_input.split(",")] if categories_input else []
)

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    data = load_data(uploaded_file)

    if data is not None:
        st.write("Classify the following tenders:")

        for index, row in data.iterrows():
            st.write(f"Title: {row['Title']}")
            st.write(f"Description: {row['Description']}")

            # Use the existing category if available, otherwise default to the first category
            default_category = (
                row["Category"]
                if "Category" in row and row["Category"] in categories
                else (categories[0] if categories else "")
            )

            selected_category = st.selectbox(
                f"Select category for tender {index + 1}",
                options=categories,
                key=f"tender_{index}",
                index=(
                    categories.index(default_category)
                    if default_category in categories
                    else 0
                ),
            )

            # Update the category in the dataframe
            data.at[index, "Category"] = selected_category

            st.write("---")

        # Download button
        if st.button("Download Classified Tenders"):
            csv = save_classifications(data)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="classified_tenders.csv",
                mime="text/csv",
            )
