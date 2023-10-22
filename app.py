# core pkg
import streamlit as st

import radon.raw as rr
import radon.metrics as rm
import radon.complexity as rc
from app_utils import get_reserved_word_frequency
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px
import paser


import pandas as pd
def convert_to_df(mydict):
    return pd.DataFrame(list(mydict.items()),columns = ['Word','Count'])

def plot_wordcloud(docx):
    wordcloud = WordCloud().generate(docx)
    fig = plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(fig)

def main():
    st.title("Python Code Analysis")


    #forms
    with st.form(key='my_form'):
        raw_code = st.text_area("Enter your python code here", height=300)
        submit_button = st.form_submit_button(label='Analyze')

    #tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Code Analytics", "Reserved", "Identifiers", "AST"])
    results = get_reserved_word_frequency(raw_code)

    if submit_button:
        with tab1:
            st.subheader("Code Analytics")
            with st.expander("Original Code"):
                st.code(raw_code)

                st.subheader("Raw SCA Metrics")
                basic_analysis = rr.analyze(raw_code)
                st.write(basic_analysis)

                #maintainability index
                mi_results = rm.mi_visit(raw_code, True)

                #cyclomatic complexity
                cc_results = rc.cc_visit(raw_code)
                st.write(cc_results[0])

                #halstead :bugs, difficulty, effort, length, time, vocabulary, volume
                hal_results = rm.h_visit(raw_code)

                #Column Layout
                col1, col2 = st.columns(2)
                col1.metric("Maintainability Index", value = mi_results)
                col2.metric("Cyclomatic Complexity", value =f"{cc_results[0]}")

            
            with st.expander("Halstead Metrics"):
                st.write(hal_results[0])
                # st.write(dir(rr))

        
            with tab2:
                st.subheader("Reserved")
                
                results_to_df = convert_to_df(results["reserved"])

                #plot with altair
                my_chart = alt.Chart(results_to_df).mark_bar().encode(
                    x='Word',
                    y='Count',
                    color='Word'

                )
                st.altair_chart(my_chart, use_container_width = True)

                t1, t2, t3 = st.tabs(["Code Cloud", "WordFreq", "Pie Chart"])
                
                with t1:
                    plot_wordcloud(raw_code)

                with t2:
                    st.dataframe(results_to_df)

                with t3:
                    fig2 = px.pie(values = results["reserved"].values(), names = results["reserved"].keys())
                    st.plotly_chart(fig2)

            with tab3:
                st.subheader("Identifiers")
                st.write(results["identifiers"])

                results_to_df = convert_to_df(results["identifiers"])

                #plot with altair
                my_chart = alt.Chart(results_to_df).mark_bar().encode(
                    x='Word',
                    y='Count',
                    color='Word'

                )
                st.altair_chart(my_chart, use_container_width = True)

                plot_wordcloud(raw_code)


            with tab4:
                st.subheader("AST")
                
                ast_results = paser.make_ast(raw_code)
                st.write(ast_results)


if __name__ == '__main__':
    main()