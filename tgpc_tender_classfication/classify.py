import streamlit as st
import pandas as pd

# Load CSV
uploaded_file = st.file_uploader("Upload CSV", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Filter options
    classes = ['Respite Care', 'Supported Living', 'Supported Accommodation', 'Domiciliary Care']
    selected_classes = st.multiselect("Select Tender Classes", classes)
    st.write("\n")
    num_tenders = st.number_input("Number of Tenders", min_value=1, value=5, step=1)

    if selected_classes:
        filtered_df_full = df[df['class'].isin(selected_classes)]
        filtered_df = filtered_df_full.head(num_tenders)
        st.write(f"### {len(filtered_df_full)} tenders found")
        
        for index, row in filtered_df.iterrows():
            st.write(f"### {row['Title']}")
            st.write(row['Description'])
