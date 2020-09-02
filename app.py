import base64

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


def get_csv_download_link(csv, filename):
    """
    Function that creates a link to download file
    Arguments:
        csv {não sei ainda} -- output from function with errors
    Returns:
        str -- html that creates hyperlink to file in cache
    """

    val = bytes(csv, 'utf-8')
    b64 = base64.b64encode(val)
    return ('<p style="text-align:center;">'
            f'<a href="data:application/octet-stream;base64,{b64.decode()}" '
            f'download="{filename}.csv">Download CSV file</a></p>')


if __name__ == '__main__':
    main()
