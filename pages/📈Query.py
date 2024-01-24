'''This module provides 10 queries to choose and fetches the result from the SQL database.'''
import streamlit as st
import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()
import pandas as pd

try:
    #Connecting to mysql
    password= os.getenv("password")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password = password,
        database="youtube"
    )
    mycursor = mydb.cursor()

    #Page configuration
    st.set_page_config(
        page_title= "Query"
    )

    # Defining the options for the dropdown
    options = ['',
            'What are the names of all the videos and their corressponding channels?',
            'Which channels have the most number of videos, and how many videos do they have?',
            'What are the top 10 most viewed videos and their respective channels?',
            'How many comments were made on each video, and what are their corresponding video names?',
            'Which videos have the highest number of likes, and what are their corresponding channel names?',
            'What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
            'What are the names of all the channels that have published videos in the year 2022?',
            'What is the average duration of all videos in each channel, and what are their corresponding channel names?',
            'Which videos have the highest number of comments, and what are their corresponding channel names?']

    # Displaying the dropdown with label
    selected_option = st.selectbox(
        'Choose an option from the dropdown:',
        options
    )

    if selected_option:
        # Displaying the selected option
        st.write('You selected:', selected_option)

        #Drafting Query based on the selected option
        if selected_option == options[1]:
            QUERY = """SELECT v.video_name, c.channel_name
                    FROM video AS v
                    INNER JOIN playlist AS p ON v.playlist_id = p.playlist_id
                    INNER JOIN channel AS c ON p.channel_id = c.channel_id;
                    """
            query_columns = ["Video Name", "Channel Name"]
        elif selected_option == options[2]:
            QUERY = """SELECT c.channel_name, COUNT(v.video_id) AS number_of_videos
                    FROM channel AS c
                    JOIN playlist AS p ON c.channel_id = p.channel_id
                    JOIN video AS v ON p.playlist_id = v.playlist_id
                    GROUP BY c.channel_name
                    ORDER BY COUNT(v.video_id) DESC;"""
            query_columns = ["Channel Name", "Number of Videos"]
        elif selected_option == options[3]:
            QUERY = """SELECT v.video_name, c.channel_name, v.view_count
                    FROM video AS v
                    JOIN playlist AS p ON v.playlist_id = p.playlist_id
                    JOIN channel AS c ON p.channel_id = c.channel_id
                    ORDER BY v.view_count DESC
                    LIMIT 10;
                    """
            query_columns = ["Video Name", "Channel Name", "View Count"]
        elif selected_option == options[4]:
            QUERY = """SELECT v.video_name, count(c.comment_id) as number_of_comments
                    from video as v
                    INNER JOIN comments as c ON c.video_id = v.video_id
                    GROUP BY c.video_id;"""
            query_columns = ["Video Name", "Number of Comments"]
        elif selected_option == options[5]:
            QUERY = """SELECT c.channel_name, v.like_count
                    FROM video as v
                    INNER JOIN playlist as p ON p.playlist_id = v.playlist_id
                    INNER JOIN channel as c ON c.channel_id = p.channel_id
                    ORDER BY v.like_count DESC
                    LIMIT 10;"""
            query_columns = ["Channel Name", "Like Count"]
        elif selected_option == options[6]:
            QUERY = """SELECT video_name, like_count, dislike_count
                    FROM video;"""
            query_columns = ["Video Name", "Like Count", "Dislike Count"]
        elif selected_option == options[7]:
            QUERY = """SELECT distinct(c.channel_name) FROM channel as c
                        INNER JOIN playlist as p ON c.channel_id = p.channel_id
                        INNER JOIN video as v ON v.playlist_id = p.playlist_id
                        WHERE YEAR(video_published_at) = 2022;"""
            query_columns = ["Channel Name"]
        elif selected_option == options[8]:
            QUERY = """SELECT c.channel_name, avg(time_to_sec(v.duration))/60 as Average_Duration_in_mins
                    FROM channel as c
                    INNER JOIN playlist as p ON c.channel_id = p.channel_id
                    INNER JOIN video as v ON p.playlist_id = v.playlist_id
                    GROUP BY c.channel_id"""
            query_columns = ["Channel Name", "Average_Duration_in_mins"]
        elif selected_option == options[9]:
            QUERY = """SELECT ch.channel_name, count(c.comment_id)
                    from comments as c
                    INNER JOIN video as v ON c.video_id = v.video_id
                    INNER JOIN playlist as p ON v.playlist_id = p.playlist_id
                    INNER JOIN channel as ch ON ch.channel_id = p.channel_id
                    GROUP BY c.video_id
                    ORDER BY count(c.comment_id) DESC;"""
            query_columns = ["Channel Name", "Number of Comments"]
        
        #Executing the query
        mycursor.execute(QUERY)

        #Fetching the results
        query_result = mycursor.fetchall()
        df = pd.DataFrame(query_result, columns = query_columns)
        
        #Displaying the dataframe on the screen
        st.table(df)

except Exception as e:
    st.error(e)

