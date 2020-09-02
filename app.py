import base64
from io import StringIO
import pandas as pd

import streamlit as st
from handlers.dbcheck import validCollar

st.set_option('deprecation.showfileUploaderEncoding', False)


def main():
    """
    function responsable for run streamlit app
    """
    st.header(body='Check Collar Dhaniel BIRL')


    # survey = st.sidebar.file_uploader(label="Survey",
    #                                   encoding=None,
    #                                   type=["csv"])

    # assay = st.sidebar.file_uploader(label="Assay",
    #                                  encoding=None,
    #                                  type=["csv"])

    collar = st.sidebar.file_uploader(label="Collar",
                                      encoding='utf-8',
                                      type=["csv"])
    
    dfcollar = pd.read_csv(StringIO(collar.read()))
    bhid = st.selectbox('Select BHID column:',dfcollar.columns)
    xcol = st.selectbox('Select X column:',dfcollar.columns)
    ycol = st.selectbox('Select Y column:',dfcollar.columns)
    zcol = st.selectbox('Select Z column:',dfcollar.columns)
    if st.sidebar.button('Process'):
        if collar:
            df_csv = validCollar(bhid,xcol,ycol,zcol,StringIO(collar.read()))
            st.markdown(get_csv_download_link(df_csv, 'error_collar'),
                        unsafe_allow_html=True)


def get_csv_download_link(dataframe, filename):
    """
    Function that creates a link to download file
    Arguments:
        csv {não sei ainda} -- output from function with errors
    Returns:
        str -- html that creates hyperlink to file in cache
    """

    # csv = to_csv(csv)
    csv =  dataframe.to_csv(index=False)
    b64 = base64.b64encode(csv.encode())
    return ('<p style="text-align:center;">'
            f'<a href="data:application/octet-stream;base64,{b64.decode()}" '
            f'download="{filename}.csv">Download CSV file</a></p>')

if __name__ == '__main__':
    main()
