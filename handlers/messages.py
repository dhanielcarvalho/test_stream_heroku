
import streamlit as st


warning_text = '''
    <div class="alert alert-danger" role="alert">
        <div class="row vertical-align">
            <div class="col-xs-1 text-center">
                <i class="fa fa-exclamation-triangle fa-2x"></i>
            </div>
            <div class="col-xs-11">
                    <strong>{warning_message}</strong>
            </div>
        </div>
    </div>
    '''


def write_warning(message):
    st.markdown(warning_text.format(warning_message=message),
                unsafe_allow_html=True)
