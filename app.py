import pandas as pd
import streamlit as st


def main():
    """
    function responsable for run streamlit app
    """
    st.header(body='Check Collar Dhaniel BIRL')

    file_upload = st.sidebar.file_uploader(label="Upload CSV",
                                           encoding=None,
                                           type=["csv"])


if __name__ == '__main__':
    main()
