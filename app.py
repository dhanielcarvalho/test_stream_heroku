import pandas as pd
import streamlit as st
from handlers.dbcheck import validCollar


def main():
    """
    function responsable for run streamlit app
    """
    st.header(body='Check Collar Dhaniel BIRL')


    survey = st.sidebar.file_uploader(label="Survey",
                                      encoding=None,
                                      type=["csv"])

    assay = st.sidebar.file_uploader(label="Assay",
                                     encoding=None,
                                     type=["csv"])

    collar = st.sidebar.file_uploader(label="Collar",
                                      encoding=None,
                                      type=["csv"])

    if st.sidebar.button('Process'):
        st.write('clicked')

if __name__ == '__main__':
    main()
