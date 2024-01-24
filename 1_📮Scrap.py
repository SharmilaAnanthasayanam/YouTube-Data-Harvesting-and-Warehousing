'''This module gets the channel id as input and displays the channel details in Streamlit.'''
import streamlit as st
from googleapiclient.discovery import build
import channel
from dotenv import load_dotenv
import os
load_dotenv()

try:
    #initialising the session data
    if "data" not in st.session_state:
        st.session_state["data"] = "Enter your channel id in Scrap section"  # Set initial data
    if "channel_id" not in st.session_state:
        st.session_state["channel_id"] = ""
    
    #Page Configuration
    st.set_page_config(
        page_title= "Youtube Scrap"
    )
    st.title("YouTube Data Harvesting and Warehousing")

    #Getting the channel id
    channel_id = st.text_input("Enter the channel ID: ")
    if not channel_id:
        st.write("Please enter a channel ID to retrieve details.") 
    else:
        st.session_state["channel_id"] = channel_id
        #Connecting to youtube API
        api_service_name = "youtube"
        api_version = "v3"
        api_key = os.getenv("developerKey")
        youtube = build(api_service_name, api_version,developerKey=api_key)
        #Fetching complete channel info
        channel_details = channel.channel_request(channel_id, youtube)
        if channel_details:
            st.session_state.data = channel_details
        #Displaying the info
        st.write("Please find your channel details")          
        st.write(channel_details)

except Exception as e:
    print(e)


