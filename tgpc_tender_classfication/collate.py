import io
import json

import pandas as pd
import streamlit as st


def main():
    st.title("Tender Data Collection App")

    # Initialize session state
    if "categories" not in st.session_state:
        st.session_state.categories = []
    if "data" not in st.session_state:
        st.session_state.data = {}

    # Option to upload existing CSV
    st.header("Upload Existing Data (Optional)")
    uploaded_file = st.file_uploader(
        "Choose a CSV file to continue from where you left off", type="csv"
    )
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        for _, row in df.iterrows():
            category = row["Category"]
            keywords = json.loads(row["Keywords"])
            sentences = json.loads(row["Key Sentences"])

            if category not in st.session_state.categories:
                st.session_state.categories.append(category)

            st.session_state.data[category] = {
                "keywords": keywords,
                "sentences": sentences,
            }

        st.success("Existing data loaded successfully!")

    # Step 1: Enter tender categories
    st.header("Step 1: Enter Tender Categories")
    new_category = st.text_input("Enter a new category:")
    if st.button("Add Category"):
        if new_category and new_category not in st.session_state.categories:
            st.session_state.categories.append(new_category)
            st.session_state.data[new_category] = {"keywords": [], "sentences": []}

    st.write("Current Categories:", st.session_state.categories)

    # Step 2: Enter keywords and key sentences for each category
    if st.session_state.categories:
        st.header("Step 2: Enter Keywords and Key Sentences")
        category = st.selectbox("Select a category:", st.session_state.categories)

        keywords = st.text_input(
            f"Enter keywords for {category} (comma-separated):",
            value=", ".join(
                st.session_state.data.get(category, {}).get("keywords", [])
            ),
        )
        key_sentences = st.text_area(
            f"Enter key sentences for {category} (one per line):",
            value="\n".join(
                st.session_state.data.get(category, {}).get("sentences", [])
            ),
        )

        if st.button("Update Data"):
            keywords_list = [kw.strip() for kw in keywords.split(",") if kw.strip()]
            sentences_list = [
                sent.strip() for sent in key_sentences.split("\n") if sent.strip()
            ]

            if category not in st.session_state.data:
                st.session_state.data[category] = {}
            st.session_state.data[category]["keywords"] = keywords_list
            st.session_state.data[category]["sentences"] = sentences_list
            st.success("Data updated successfully!")

    # Step 3: Display collected data
    if st.session_state.data:
        st.header("Collected Data")
        for category, item in st.session_state.data.items():
            st.subheader(category)
            st.write("Keywords:", ", ".join(item["keywords"]))
            st.write("Key Sentences:")
            for sentence in item["sentences"]:
                st.write("- " + sentence)
            st.write("---")

    # Step 4: Download data as CSV
    if st.session_state.data:
        st.header("Download Data")
        df_data = []
        for category, item in st.session_state.data.items():
            df_data.append(
                {
                    "Category": category,
                    "Keywords": json.dumps(item["keywords"]),
                    "Key Sentences": json.dumps(item["sentences"]),
                }
            )
        df = pd.DataFrame(df_data)

        csv = df.to_csv(index=False)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name="tender_data.csv",
            mime="text/csv",
        )


if __name__ == "__main__":
    main()
