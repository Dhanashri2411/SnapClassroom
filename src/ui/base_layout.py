import streamlit as st
def base_layout_home():
    st.markdown(
        """
        <style>
        .stApp{
            background-color: light purple !important;
        }
        </style>
        """, unsafe_allow_html=True)
def base_layout_home():
    st.markdown(
        """
        <style>
        .stApp{
            background-color:  purple !important;
        }
        </style>
        """, unsafe_allow_html=True)
def base_layout_dashboard():
    st.markdown(
        """
        <style>
        .stApp{
            background-color: pink !important;
        }
        </style>
        """, unsafe_allow_html=True)
def base_layout_overall():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');
        /*Hide Top Bar of Streamlit*/
        #MainMenu ,header,footer
        {visibility: hidden;}
        .block-container{
            padding-top: 1.5rem;
    
        }
        h2 {
            font-family: 'Climate Crisis', sans-serif !important;
            font-size: 3.5rem !important;
            text-align: center !important;
            margin-bottom: 0rem !important;
        }
        h3,h4,p{
        
            font-family: 'Outfit', sans-serif !important;
            color: #333 !important;
            }
        button [kind="secondary"]{
            background-color: green !important;
            border-radius: 1.5rem !important;
            padding: 10px 20px !important;
            transition: background-color 0.3s ease !important;

        }
        button [kind="tertiary"]:hover{
            background-color: darkgreen !important;
            border-radius: 1.5rem !important;
            padding: 10px 20px !important
            transition: background-color 0.3s ease !important;

        }
        button{
            background-color: darkgreen !important;
            border-radius: 1.5rem !important;
            padding: 10px 20px !important
            transition: background-color 0.3s ease !important;
        }
        button [kind="secondary"]:hover{
        transform: scale(1.05) !important;
        }
        </style>
        """, unsafe_allow_html=True)