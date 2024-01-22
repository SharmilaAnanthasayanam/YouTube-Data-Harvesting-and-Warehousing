import streamlit as st
import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()

try:
    password= os.getenv("password")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password = password,
        database="youtube"
    )
    mycursor = mydb.cursor()
    st.set_page_config(
        page_title= "Query"
    )
    # Define the options for the dropdown
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

    # Display the dropdown with a descriptive label
    selected_option = st.selectbox(
        'Choose an option from the dropdown:',
        options
    )

    # Display the selected option
    if selected_option:
        
        st.write('You selected:', selected_option)

        if selected_option == options[1]:
            QUERY = """SELECT v.video_name, c.channel_name
                    FROM video AS v
                    INNER JOIN playlist AS p ON v.playlist_id = p.playlist_id
                    INNER JOIN channel AS c ON p.channel_id = c.channel_id;
                    """
        elif selected_option == options[2]:
            QUERY = """SELECT c.channel_name, COUNT(v.video_id) AS number_of_videos
                    FROM channel AS c
                    JOIN playlist AS p ON c.channel_id = p.channel_id
                    JOIN video AS v ON p.playlist_id = v.playlist_id
                    GROUP BY c.channel_name;"""
        elif selected_option == options[3]:
            QUERY = """SELECT v.video_name, c.channel_name, v.view_count
                    FROM video AS v
                    JOIN playlist AS p ON v.playlist_id = p.playlist_id
                    JOIN channel AS c ON p.channel_id = c.channel_id
                    ORDER BY v.view_count DESC
                    LIMIT 10;
                    """
        elif selected_option == options[4]:
            QUERY = """SELECT v.video_name, count(c.comment_id) as number_of_comments
                    from video as v
                    INNER JOIN comments as c ON c.video_id = v.video_id
                    GROUP BY c.video_id;"""
        elif selected_option == options[5]:
            QUERY = """SELECT v.like_count, c.channel_name 
                    FROM video as v
                    INNER JOIN playlist as p ON p.playlist_id = v.playlist_id
                    INNER JOIN channel as c ON c.channel_id = p.channel_id
                    ORDER BY v.like_count DESC
                    LIMIT 10;"""
        elif selected_option == options[6]:
            QUERY = """SELECT like_count, video_name
                    FROM video;"""
        elif selected_option == options[7]:
            QUERY = """SELECT channel_name FROM channel
                    WHERE YEAR(channel_published_at) = 2022;"""
        elif selected_option == options[8]:
            QUERY = """SELECT avg(time_to_sec(v.duration))/60 as Average_Duration_in_mins, c.channel_name
                    FROM channel as c
                    INNER JOIN playlist as p ON c.channel_id = p.channel_id
                    INNER JOIN video as v ON p.playlist_id = v.playlist_id
                    GROUP BY c.channel_id"""
        elif selected_option == options[9]:
            QUERY = """SELECT distinct(count(c.comment_id)), ch.channel_name
                    from comments as c
                    INNER JOIN video as v ON c.video_id = v.video_id
                    INNER JOIN playlist as p ON v.playlist_id = p.playlist_id
                    INNER JOIN channel as ch ON ch.channel_id = p.channel_id
                    GROUP BY c.video_id
                    ORDER BY count(c.comment_id) DESC;"""
        mycursor.execute(QUERY)
        st.table(mycursor.fetchall())

except Exception as e:
    st.error(e)

