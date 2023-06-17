import streamlit as st
import pandas as pd
from content_similarity import sentence_similarity
import time

def main():
    st.set_page_config(page_title="Semantic Search Engine", layout="wide", page_icon="🔎")
    # Create a menu to select the option
    menu = ["Retrieve from DB", "Check Similarity"]
    choice = st.sidebar.radio("Select an option", menu)

    if choice == "Retrieve from DB":
        st.title("Semantic Search Engine")

        data = None
        uploaded_file = st.file_uploader("Upload the database (CSV or excel file)", type=("xlsx", "csv"))
        if uploaded_file is not None:
            file_extension = uploaded_file.name.split(".")[-1]
            if file_extension == "csv":
                data = pd.read_csv(uploaded_file)
            else:
                data = pd.read_excel(uploaded_file)

        # Get user input and show results
        if data is not None:
            with st.spinner('Loading data...'):
                time.sleep(3)
            st.write(data)

            # st.subheader("Search your Query")
            input_question = st.text_input("Search your query")
            if input_question:
                similarity_scores = []
                for question in data["Question"]:
                    score = sentence_similarity(input_question, question)
                    similarity_scores.append(score)
                max_score = max(similarity_scores)
                print("The max score is:", max_score)
                if max_score >= 50:
                    index = similarity_scores.index(max_score)
                    matching_question = data.iloc[index]["Question"]
                    matching_answer = data.iloc[index]["Answer"]
                    st.write("Matching question:", matching_question)
                    st.write("Matching answer:", matching_answer)
                    st.write("Similarity confidence:", str(max_score) + " %")
                else:
                    st.write("No matching question found")

    else:
        st.title("Sentence Similarity Checker")
        input1 = st.text_area("Enter sentence 1")
        input2 = st.text_area("Enter sentence 2")
        submit_button = st.button('Calculate similarity')
        if submit_button:
            if input1 and input2:
                similarity_score = sentence_similarity(input1, input2)
                # st.write("Similarity between two sentences is:", str(similarity_score) + " %")
                st.write("Similarity between two sentences using Sentence transformer is:", str(similarity_score) + " %")
            else:
                st.write("Please enter two sentences to check their similarity.")

if __name__ == "__main__":
    main()
